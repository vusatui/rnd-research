"""Offline tests for ex2 (no network, no API key): C2PA round trip, tamper, strip; watermark; fingerprint."""
import sys
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ex2_c2pa import lab  # noqa: E402


@pytest.fixture(scope="module")
def signed(tmp_path_factory):
    d = tmp_path_factory.mktemp("c2pa")
    src = d / "src.jpg"
    lab.synthetic_image(7).save(src, quality=95)
    out = d / "signed.jpg"
    lab.sign_ai_image(src, out)
    return out


def test_signed_file_is_trusted_and_says_ai_generated(signed):
    r = lab.read_credentials(signed)
    assert r["state"] == "Trusted" and r["ai_created"] and r["actions"] == ["c2pa.created"]


def test_without_trust_anchor_it_is_only_valid(signed):
    r = lab.read_credentials(signed, trust_test_ca=False)
    assert r["state"] == "Valid" and "signingCredential.untrusted" in r["codes"]


def test_tampered_pixels_make_it_invalid(signed, tmp_path):
    b = bytearray(signed.read_bytes()); b[int(len(b) * .9)] ^= 0xFF
    p = tmp_path / "t.jpg"; p.write_bytes(b)
    assert lab.read_credentials(p)["state"] == "Invalid"


def test_resave_strips_credentials(signed, tmp_path):
    p = tmp_path / "r.png"; Image.open(signed).save(p)
    assert lab.read_credentials(p)["state"] == "NoManifest"
    p2 = tmp_path / "r.jpg"; Image.open(signed).save(p2, quality=95)
    assert lab.read_credentials(p2)["state"] == "NoManifest"


def test_c2pa_aware_edit_keeps_chain(signed, tmp_path):
    im = Image.open(signed); w, h = im.size
    c = tmp_path / "c.jpg"; im.crop((40, 40, w - 40, h - 40)).save(c, quality=92)
    out = tmp_path / "edit.jpg"
    lab.sign_ai_image(c, out, parent=signed, edit_action="c2pa.cropped")
    r = lab.read_credentials(out)
    assert r["state"] == "Trusted" and r["manifests"] == 2 and r["actions"] == ["c2pa.opened", "c2pa.cropped"]


def test_watermark_roundtrip_and_jpeg_survival(tmp_path):
    bits = lab.payload_bits()
    marked = lab.embed_watermark(np.asarray(lab.synthetic_image(3)), bits)
    assert lab.watermark_detected(lab.decode_watermark(marked), bits)
    p = tmp_path / "w.jpg"; Image.fromarray(marked).save(p, quality=75)
    assert lab.watermark_detected(lab.decode_watermark(np.asarray(Image.open(p).convert("RGB"))), bits)


def test_watermark_not_found_in_unmarked_image_and_not_after_crop():
    bits = lab.payload_bits()
    clean = np.asarray(lab.synthetic_image(4))
    assert not lab.watermark_detected(lab.decode_watermark(clean), bits)
    marked = lab.embed_watermark(clean, bits)
    assert not lab.watermark_detected(lab.decode_watermark(marked[60:-60, 60:-60]), bits)   # geometric change breaks this simple scheme


def test_detection_threshold_false_alarm_probability():
    assert lab.binom_tail(lab.WM_THRESHOLD_BITS) < 1e-4       # 50/64 bits agreeing by chance


def test_fingerprint_survives_recompression_but_not_mirror(tmp_path):
    im = lab.synthetic_image(5); p = tmp_path / "f.jpg"; im.save(p, quality=50)
    h0 = lab.dhash(im)
    assert lab.hamming(h0, lab.dhash(Image.open(p))) <= 10
    assert lab.hamming(h0, lab.dhash(im.transpose(Image.FLIP_LEFT_RIGHT))) > 80
    assert lab.hamming(h0, lab.dhash(lab.synthetic_image(6))) > 80    # unrelated image is far away
