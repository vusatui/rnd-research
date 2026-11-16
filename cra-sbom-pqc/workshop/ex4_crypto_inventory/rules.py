"""Detection rules: regex over source/config text -> cryptographic algorithm findings.

Deliberately simple (a "grep with opinions"): it finds *declared use* in text. It does not see crypto inside binaries, third-party
libraries, TLS terminators, HSMs, or data that is simply encrypted somewhere else. Real programs combine this with dependency
analysis (e.g. cdxgen/CBOMkit/Sonar rules), binary scanning and network probing (see ex5 `probe_tls`).

quantum: how a cryptographically relevant quantum computer (CRQC) changes the picture (NIST IR 8547, Shor/Grover):
  "broken-by-Shor"  - RSA, DH, ECDH, ECDSA, EdDSA, X25519: deprecate after 2030 / disallow after 2035 in NIST standards (IR 8547)
  "grover-halved"   - symmetric keys and hashes: security level halves; AES-256 / SHA-256 stay fine
  "classically-broken" - MD5, SHA-1 collisions: replace regardless of quantum
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    family: str
    primitive: str          # CycloneDX 1.6 algorithmProperties.primitive
    function: str           # confidentiality | authenticity | integrity | key-establishment
    quantum: str
    pqc_target: str
    pattern: re.Pattern
    curve: str | None = None


def R(family, primitive, function, quantum, target, pat, curve=None):
    return Rule(family, primitive, function, quantum, target, re.compile(pat, re.I), curve)


RULES = [
    R("RSA", "pke", "key-establishment/authenticity", "broken-by-Shor", "ML-KEM (FIPS 203) for key establishment, ML-DSA (FIPS 204) / SLH-DSA (FIPS 205) for signatures",
      r"rsa\.generate_private_key|generateKeyPairSync\(\s*['\"]rsa|KeyPairGenerator\.getInstance\(\"RSA\"\)|ECDHE-RSA|ssh_host_rsa_key|\bRS256\b|PKCS1v15|RSA-\d{4}"),
    R("ECDH", "key-agree", "key-establishment", "broken-by-Shor", "hybrid X25519MLKEM768 now, then ML-KEM-768 (FIPS 203)",
      r"ec\.ECDH\(\)|createECDH|KeyAgreement\.getInstance\(\"ECDH\"\)|ssl_ecdh_curve|ecdh-sha2-nistp\d+", None),
    R("ECDSA", "signature", "authenticity", "broken-by-Shor", "ML-DSA (FIPS 204) / SLH-DSA (FIPS 205); FN-DSA (FIPS 206) is not yet published",
      r"ec\.ECDSA|ECDHE-ECDSA|withECDSA"),
    R("EC key (NIST P-curve)", "key-agree", "key-establishment/authenticity", "broken-by-Shor", "see ECDH / ECDSA",
      r"ec\.generate_private_key|KeyPairGenerator\.getInstance\(\"EC\"\)|prime256v1|secp256r1", "P-256"),
    R("X25519", "key-agree", "key-establishment", "broken-by-Shor", "hybrid X25519MLKEM768 now, then ML-KEM-768",
      r"x25519\.X25519PrivateKey|curve25519-sha256|\bX25519\b"),
    R("Ed25519", "signature", "authenticity", "broken-by-Shor", "ML-DSA / SLH-DSA", r"ssh_host_ed25519_key|Ed25519PrivateKey|\bed25519\b"),
    R("MD5", "hash", "integrity", "classically-broken", "SHA-256 / SHA3-256", r"hashlib\.md5|createHash\(['\"]md5|MessageDigest\.getInstance\(\"MD5\"\)"),
    R("SHA-1", "hash", "integrity", "classically-broken", "SHA-256 / SHA3-256", r"hashlib\.sha1|createHash\(['\"]sha1|MessageDigest\.getInstance\(\"SHA-?1\"\)"),
    R("AES-256-GCM", "ae", "confidentiality", "grover-halved", "keep (256-bit key = ~128-bit post-quantum margin)", r"aes-256-gcm|AESGCM"),
    R("SHA-256 / HMAC-SHA-256", "hash", "integrity", "grover-halved", "keep", r"hashlib\.sha256|hashes\.SHA256\(\)|MessageDigest\.getInstance\(\"SHA-256\"\)|hmac\.new"),
    R("TLS 1.2 allowed", "other", "protocol", "n/a", "require TLS 1.3 (hybrid ML-KEM groups exist only there)", r"TLSv1_2|ssl_protocols\s+TLSv1\.2|TLSv1\.2"),
]

KEY_BITS = [re.compile(p) for p in (r"key_size\s*=\s*(\d+)", r"modulusLength:\s*(\d+)", r"initialize\((\d+)\)")]
SUFFIXES = {".py", ".js", ".ts", ".java", ".go", ".conf", ".cfg", ".yaml", ".yml", ".json", ""}
SKIP_DIRS = {"node_modules", ".git", "__pycache__", ".venv"}
