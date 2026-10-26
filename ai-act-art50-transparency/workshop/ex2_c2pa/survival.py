"""Experiment: which marking layer survives which everyday transformation?

For each source image the 'provider pipeline' is: embed invisible watermark -> save JPEG q95 -> sign with C2PA
(AI-generated claim) -> register a perceptual fingerprint in a registry. Then the signed file is pushed through
transformations that happen to real images (re-save, messenger recompression, resize, crop, rotate, mirror, noise,
a real browser screenshot, a C2PA-aware edit) and every layer is checked again:

  C2PA        state of the Content Credentials a verifier would see (Trusted / Invalid / NoManifest ...)
  watermark   bit accuracy of the 64-bit payload (50% = chance; detected if >= 50/64 bits, p ~ 1e-5 by chance)
  fingerprint Hamming distance (of 256 bits) to the registered hash, and to the NEAREST OTHER registered image

    python ex2_c2pa/survival.py                    # 3 synthetic images, ~15 transformations
    python ex2_c2pa/survival.py --image my.png     # add your own image (e.g. real model output)
"""
from __future__ import annotations

import argparse
import datetime
import io
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.paths import OUT, RESULTS  # noqa: E402
from ex2_c2pa import lab  # noqa: E402

CHROME = next((c for c in ("google-chrome", "chromium", "chromium-browser", "chrome") if shutil.which(c)), None)
FP_MATCH = 40          # <= 40 of 256 bits (16%) counts as 'same image' (checked against the nearest other image)


def save(img: Image.Image, path: Path, **kw):
    img.save(path, **kw)
    return path


def t_screenshot(src: Path, dst: Path, scale: float = 1.0, margin: int = 0) -> Path | None:
    """Real screenshot: render the file in headless Chrome and capture the page (needs Chrome/Chromium).
    scale = display scaling factor (1.25 = a 125% Windows/HiDPI display); margin = white page border in CSS px."""
    if not CHROME:
        return None
    w, h = Image.open(src).size
    html = dst.with_suffix(".html")
    html.write_text(f'<html><body style="margin:{margin}px;background:#fff"><img src="{src.resolve().as_uri()}" '
                    f'width="{w}" height="{h}" style="display:block"></body></html>')
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={scale}", f"--window-size={w + 2 * margin},{h + 2 * margin}",
                    f"--screenshot={dst}", html.as_uri()],
                   capture_output=True, timeout=60)
    html.unlink(missing_ok=True)
    return dst if dst.exists() else None


def transformations(signed: Path, work: Path):
    """name -> (description, producer(src)->Path|None)."""
    im = lambda: Image.open(signed).convert("RGB")  # noqa: E731
    w, h = im().size

    def copy_file():
        return Path(shutil.copy(signed, work / "t_copy.jpg"))

    def byte_flip():
        b = bytearray(signed.read_bytes()); b[int(len(b) * .9)] ^= 0xFF     # one corrupted byte inside the image data
        p = work / "t_byteflip.jpg"; p.write_bytes(b); return p

    def lossless_strip():   # same pixels, new container: what any non-C2PA-aware tool does on 'Save as PNG'
        return save(im(), work / "t_strip.png")

    def jpeg(q):
        return lambda: save(im(), work / f"t_jpeg{q}.jpg", quality=q)

    def resize50():
        return save(im().resize((w // 2, h // 2), Image.LANCZOS), work / "t_resize50.jpg", quality=90)

    def crop80():
        dx, dy = int(w * .1), int(h * .1)
        return save(im().crop((dx, dy, w - dx, h - dy)), work / "t_crop80.jpg", quality=92)

    def rotate5():
        return save(im().rotate(5, resample=Image.BICUBIC), work / "t_rot5.jpg", quality=92)

    def mirror():
        return save(im().transpose(Image.FLIP_LEFT_RIGHT), work / "t_mirror.jpg", quality=92)

    def noise():
        a = np.asarray(im(), dtype=np.float32) + np.random.default_rng(0).normal(0, 8, (h, w, 3))
        return save(Image.fromarray(np.clip(a, 0, 255).astype("uint8")), work / "t_noise.jpg", quality=92)

    def messenger():        # downscale to 1280 long edge-ish + q70: typical chat-app recompression (SIMULATED, not a real app)
        s = min(1.0, 1280 / max(w, h))
        return save(im().resize((int(w * s), int(h * s)), Image.LANCZOS), work / "t_messenger.jpg", quality=70)

    def screenshot():
        return t_screenshot(signed, work / "t_screenshot.png")

    def screenshot_scaled():    # what a user on a 125% display with the image in a page with a border really captures
        return t_screenshot(signed, work / "t_screenshot_scaled.png", scale=1.25, margin=37)

    def c2pa_edit():        # a C2PA-aware editor crops and re-signs, keeping the parent as an ingredient
        dx, dy = int(w * .1), int(h * .1)
        tmp = save(im().crop((dx, dy, w - dx, h - dy)), work / "t_edit_src.jpg", quality=92)
        out = work / "t_c2pa_edit.jpg"
        lab.sign_ai_image(tmp, out, generator="Workshop Editor", parent=signed, edit_action="c2pa.cropped")
        return out

    return {
        "none (file copy)": copy_file, "1 byte changed": byte_flip, "re-save as PNG (strip metadata)": lossless_strip,
        "JPEG q85": jpeg(85), "JPEG q60": jpeg(60), "messenger-like (1280px, q70)": messenger, "resize 50%": resize50,
        "gaussian noise s=8": noise, "crop 80% center": crop80, "rotate 5 deg": rotate5, "mirror": mirror,
        "browser screenshot 1:1 (headless Chrome)": screenshot,
        "browser screenshot, 125% scaling + page border": screenshot_scaled, "C2PA-aware crop + re-sign": c2pa_edit,
    }


def provider_pipeline(src_img: Image.Image, name: str, work: Path, bits: list[int]) -> Path:
    marked = lab.embed_watermark(np.asarray(src_img.convert("RGB")), bits)
    tmp = save(Image.fromarray(marked), work / f"{name}_marked.jpg", quality=95)
    signed = work / f"{name}_signed.jpg"
    lab.sign_ai_image(tmp, signed)
    return signed


def evaluate(path: Path, bits: list[int], registry: dict[str, np.ndarray], own: str) -> dict:
    cred = lab.read_credentials(path)
    img = Image.open(path).convert("RGB")
    got = lab.decode_watermark(np.asarray(img))
    acc = lab.bit_accuracy(got, bits)
    fp = lab.dhash(img)
    d_own = lab.hamming(fp, registry[own])
    d_other = min((lab.hamming(fp, v) for k, v in registry.items() if k != own), default=256)   # one image only: nothing to confuse it with
    return {"c2pa": cred["state"], "c2pa_codes": cred.get("codes", []), "c2pa_manifests": cred.get("manifests"),
            "wm_acc": round(acc, 3), "wm_detected": lab.watermark_detected(got, bits),
            "fp_dist_own": d_own, "fp_dist_nearest_other": d_other, "fp_match": d_own <= FP_MATCH and d_own < d_other}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", action="append", default=[], help="extra source image(s); any format PIL reads")
    ap.add_argument("--seeds", type=int, default=3, help="number of synthetic source images")
    a = ap.parse_args()

    work = OUT / "survival"
    shutil.rmtree(work, ignore_errors=True); work.mkdir(parents=True)
    lab.make_test_pki()
    bits = lab.payload_bits()
    sources = {f"synthetic{i}": lab.synthetic_image(100 + i) for i in range(a.seeds)}
    for p in a.image:
        sources[Path(p).stem] = Image.open(p).convert("RGB").resize((768, 768))

    signed, registry = {}, {}
    for name, im in sources.items():
        signed[name] = provider_pipeline(im, name, work, bits)
        registry[name] = lab.dhash(Image.open(signed[name]))                      # the 'log' layer: hash of what we issued
    print("baseline (signed original):")
    rows = []
    for name, p in signed.items():
        r = evaluate(p, bits, registry, name); rows.append({"image": name, "transform": "ORIGINAL (as issued)", **r}); print(" ", name, r)

    tnames = None
    for name, p in signed.items():
        wdir = work / name; wdir.mkdir()
        ts = transformations(p, wdir)
        tnames = list(ts)
        for tname, fn in ts.items():
            out = fn()
            if out is None:
                rows.append({"image": name, "transform": tname, "skipped": "tool not available"}); continue
            r = evaluate(out, bits, registry, name); rows.append({"image": name, "transform": tname, **r})

    # aggregate
    import collections
    agg = collections.OrderedDict()
    for t in ["ORIGINAL (as issued)"] + (tnames or []):
        rs = [r for r in rows if r["transform"] == t and "skipped" not in r]
        if not rs:
            agg[t] = {"n": 0}; continue
        n = len(rs)
        agg[t] = {"n": n,
                  "c2pa": dict(collections.Counter(r["c2pa"] for r in rs)),
                  "wm_detected": f"{sum(r['wm_detected'] for r in rs)}/{n}",
                  "wm_acc_mean": round(float(np.mean([r["wm_acc"] for r in rs])), 3),
                  "fp_match": f"{sum(r['fp_match'] for r in rs)}/{n}",
                  "fp_dist_own_mean": round(float(np.mean([r["fp_dist_own"] for r in rs])), 1),
                  "fp_dist_other_min": int(min(r["fp_dist_nearest_other"] for r in rs))}
    res = {"date": datetime.datetime.now().isoformat(timespec="seconds"), "images": list(sources), "chrome": CHROME,
           "wm_method": lab.WM_METHOD, "wm_threshold_bits": f"{lab.WM_THRESHOLD_BITS}/{lab.WM_BITS}",
           "wm_chance_p": lab.binom_tail(lab.WM_THRESHOLD_BITS), "fp_match_rule": f"<= {FP_MATCH}/256 bits and closer than any other image",
           "rows": rows, "aggregate": agg}
    RESULTS.mkdir(exist_ok=True)
    jp = RESULTS / f"ex2_survival_{datetime.date.today()}.json"
    jp.write_text(json.dumps(res, indent=1))
    md = ["| transformation | C2PA verdict | watermark detected (mean bit acc.) | fingerprint match (mean dist.) |", "|---|---|---|---|"]
    for t, v in agg.items():
        if not v.get("n"):
            md.append(f"| {t} | skipped (tool missing) | | |"); continue
        md.append(f"| {t} | {', '.join(f'{k} x{c}' for k, c in v['c2pa'].items())} | {v['wm_detected']} ({v['wm_acc_mean']}) | "
                  f"{v['fp_match']} ({v['fp_dist_own_mean']}/256) |")
    (RESULTS / f"ex2_survival_{datetime.date.today()}.md").write_text("\n".join(md) + "\n")
    print("\n".join(md)); print("saved", jp)


if __name__ == "__main__":
    main()
