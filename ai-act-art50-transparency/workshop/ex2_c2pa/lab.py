"""Building blocks for the marking lab: C2PA signing/reading, an open invisible watermark, a perceptual fingerprint.

The three layers correspond to the techniques named in the Code of Practice on Transparency of AI-generated Content
(Section 1, Measure 1.1): digitally signed metadata (1.1.1), imperceptible watermark (1.1.2), fingerprinting/logging
(1.1.3, optional). They are WORKSHOP-GRADE stand-ins, not what a production generator ships:
  - signing uses a throw-away test CA created below (validators will say 'untrusted' unless you load that CA);
  - the watermark is the open DWT-DCT-SVD one from `invisible-watermark`, not SynthID/TrustMark/Video Seal;
  - the 'AI image' is a procedurally generated stand-in (no image model is called).
"""
from __future__ import annotations

import datetime
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image

from common.paths import OUT

CERT_DIR = OUT / "certs"
AI_SOURCE_TYPE = "http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia"   # IPTC: 'created by AI'
MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}


# ---------------------------------------------------------------- test PKI -------------------------------------------
def make_test_pki(force: bool = False) -> dict[str, Path]:
    """A throw-away root CA + leaf signing cert (ES256). Leaf: digitalSignature + emailProtection EKU, as c2pa-rs expects."""
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

    files = {"certs": CERT_DIR / "certs.pem", "key": CERT_DIR / "key.pem", "ca": CERT_DIR / "ca.pem"}
    if all(p.exists() for p in files.values()) and not force:
        return files
    CERT_DIR.mkdir(parents=True, exist_ok=True)

    def name(cn):
        return x509.Name([x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Art50 Workshop (TEST ONLY)"),
                          x509.NameAttribute(NameOID.COMMON_NAME, cn)])

    now = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=5)
    ca_key, leaf_key = ec.generate_private_key(ec.SECP256R1()), ec.generate_private_key(ec.SECP256R1())
    ku = dict(digital_signature=False, content_commitment=False, key_encipherment=False, data_encipherment=False,
              key_agreement=False, key_cert_sign=False, crl_sign=False, encipher_only=False, decipher_only=False)
    ca = (x509.CertificateBuilder().subject_name(name("Workshop Test Root CA")).issuer_name(name("Workshop Test Root CA"))
          .public_key(ca_key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(now)
          .not_valid_after(now + datetime.timedelta(days=3650))
          .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
          .add_extension(x509.KeyUsage(**{**ku, "key_cert_sign": True, "crl_sign": True}), critical=True)
          .add_extension(x509.SubjectKeyIdentifier.from_public_key(ca_key.public_key()), critical=False)
          .sign(ca_key, hashes.SHA256()))
    leaf = (x509.CertificateBuilder().subject_name(name("Workshop Image Generator (test signer)")).issuer_name(ca.subject)
            .public_key(leaf_key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(now)
            .not_valid_after(now + datetime.timedelta(days=365))
            .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
            .add_extension(x509.KeyUsage(**{**ku, "digital_signature": True}), critical=True)
            .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.EMAIL_PROTECTION]), critical=False)
            .add_extension(x509.SubjectKeyIdentifier.from_public_key(leaf_key.public_key()), critical=False)
            .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()), critical=False)
            .sign(ca_key, hashes.SHA256()))
    enc = serialization.Encoding.PEM
    files["certs"].write_bytes(leaf.public_bytes(enc) + ca.public_bytes(enc))
    files["ca"].write_bytes(ca.public_bytes(enc))
    files["key"].write_bytes(leaf_key.private_bytes(enc, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
    return files


# ---------------------------------------------------------------- C2PA ----------------------------------------------
def _signer_parts():
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    pki = make_test_pki()
    key = serialization.load_pem_private_key(pki["key"].read_bytes(), password=None)
    return (lambda data: key.sign(data, ec.ECDSA(hashes.SHA256()))), pki["certs"].read_text()


def _settings(trust_test_ca: bool):
    import c2pa
    if not trust_test_ca:
        return c2pa.Settings.from_dict({})
    return c2pa.Settings.from_dict({"trust": {"trust_anchors": make_test_pki()["ca"].read_text()}})


def sign_ai_image(src: Path, dst: Path, generator: str = "Workshop ImageGen", parent: Path | None = None,
                  edit_action: str | None = None) -> None:
    """Sign `src` -> `dst` with a C2PA manifest saying 'created by AI' (c2pa.created + IPTC trainedAlgorithmicMedia).
    With `parent` + `edit_action` (e.g. 'c2pa.cropped') the parent's manifest is kept as an ingredient: a C2PA-aware
    edit that preserves the provenance chain."""
    import c2pa
    sign_cb, certs = _signer_parts()
    if parent is None:
        actions = [{"action": "c2pa.created", "digitalSourceType": AI_SOURCE_TYPE}]
    else:
        actions = [{"action": "c2pa.opened", "parameters": {"ingredientIds": ["parent1"]}, "digitalSourceType": AI_SOURCE_TYPE},
                   {"action": edit_action or "c2pa.edited"}]
    manifest = {"claim_generator_info": [{"name": generator, "version": "0.1"}], "title": dst.name,
                "assertions": [{"label": "c2pa.actions.v2", "data": {"actions": actions}}]}
    with c2pa.Context(_settings(True)) as ctx, c2pa.Signer.from_callback(sign_cb, c2pa.C2paSigningAlg.ES256, certs, None) as signer:
        with c2pa.Builder(manifest, ctx) as b:
            if parent is not None:
                with open(parent, "rb") as f:
                    b.add_ingredient(json.dumps({"title": parent.name, "relationship": "parentOf", "label": "parent1"}),
                                     MIME[parent.suffix.lower()], f)
            b.sign_file(str(src), str(dst), signer)


def read_credentials(path: Path, trust_test_ca: bool = True) -> dict:
    """What a verifier sees. state: Trusted / Valid / Invalid / NoManifest (as returned by c2pa-rs).
    Without our test CA in the trust list a perfectly intact file is 'Valid' but with failure code signingCredential.untrusted."""
    import c2pa
    mime = MIME.get(path.suffix.lower())
    if mime is None:
        return {"state": "UnsupportedFormat"}
    try:
        with c2pa.Context(_settings(trust_test_ca)) as ctx, open(path, "rb") as f, c2pa.Reader(mime, f, context=ctx) as r:
            j = json.loads(r.json())
            am = j["manifests"][j["active_manifest"]]
            acts = [a for x in am.get("assertions", []) if x["label"].startswith("c2pa.actions") for a in x["data"]["actions"]]
            return {"state": r.get_validation_state(), "codes": [x["code"] for x in j.get("validation_status", [])],
                    "manifests": len(j["manifests"]), "generator": am["claim_generator_info"][0]["name"],
                    "signer": am.get("signature_info", {}).get("common_name"),
                    "ai_created": any(a.get("digitalSourceType") == AI_SOURCE_TYPE for a in acts),
                    "actions": [a["action"] for a in acts]}
    except Exception as e:      # c2pa raises ManifestNotFound for files without Content Credentials
        return {"state": "NoManifest" if "ManifestNotFound" in type(e).__name__ or "ManifestNotFound" in str(e) else "Error",
                "detail": str(e)[:120]}


# ---------------------------------------------------------------- invisible watermark -------------------------------
WM_BITS = 64
WM_METHOD = "dwtDctSvd"


def payload_bits(seed: int = 2026) -> list[int]:
    return np.random.default_rng(seed).integers(0, 2, WM_BITS).tolist()


def embed_watermark(rgb: np.ndarray, bits: list[int]) -> np.ndarray:
    import cv2
    from imwatermark import WatermarkEncoder
    enc = WatermarkEncoder()
    enc.set_watermark("bits", bits)
    out = enc.encode(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), WM_METHOD)
    return cv2.cvtColor(out, cv2.COLOR_BGR2RGB)


def decode_watermark(rgb: np.ndarray) -> list[int]:
    import cv2
    from imwatermark import WatermarkDecoder
    return list(WatermarkDecoder("bits", WM_BITS).decode(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), WM_METHOD))


def bit_accuracy(got: list[int], want: list[int]) -> float:
    return float(np.mean(np.array(got) == np.array(want)))


def binom_tail(k: int, n: int = WM_BITS) -> float:
    """P(X >= k) for X ~ Binomial(n, 0.5): chance that random bits agree this well with the payload."""
    return sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n


WM_THRESHOLD_BITS = 50   # 50/64 bits = 78%: p = %.1e under 'no watermark' (computed in tests)


def watermark_detected(got: list[int], want: list[int]) -> bool:
    return int(round(bit_accuracy(got, want) * WM_BITS)) >= WM_THRESHOLD_BITS


# ---------------------------------------------------------------- fingerprint (perceptual hash) --------------------
def dhash(img: Image.Image, size: int = 16) -> np.ndarray:
    """Difference hash: 16x16 = 256 bits. Survives re-compression/resizing; changes under crop/rotate/mirror."""
    g = np.asarray(img.convert("L").resize((size + 1, size), Image.LANCZOS), dtype=np.int16)
    return (g[:, 1:] > g[:, :-1]).flatten()


def hamming(a: np.ndarray, b: np.ndarray) -> int:
    return int(np.count_nonzero(a != b))


# ---------------------------------------------------------------- synthetic stand-in for an AI image ----------------
def synthetic_image(seed: int, n: int = 768) -> Image.Image:
    """Photo-like multi-octave noise texture. A PROCEDURAL STAND-IN for generator output (no model is called)."""
    rng = np.random.default_rng(seed)
    img = np.zeros((n, n, 3))
    for o in range(1, 7):
        low = rng.random((2 ** o, 2 ** o, 3))
        up = np.asarray(Image.fromarray((low * 255).astype("uint8")).resize((n, n), Image.BICUBIC)) / 255.0
        img += up / (1.6 ** o)
    img = (img - img.min()) / (img.max() - img.min())
    return Image.fromarray((img * 255).astype("uint8"))
