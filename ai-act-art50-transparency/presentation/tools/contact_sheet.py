#!/usr/bin/env python3
"""Montage of export/slide-*.png -> contact-sheet.png (3 columns). Optional arg: output path, e.g. a/b/c to make partial sheets."""
import glob, os, sys
from PIL import Image, ImageDraw
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
files = sorted(glob.glob(os.path.join(root, "export", "slide-*.png")))
tw, th, cols, pad = 640, 360, 3, 16
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (tw + pad) + pad, rows * (th + pad) + pad), "#dee2e6")
for i, f in enumerate(files):
    im = Image.open(f).convert("RGB").resize((tw, th), Image.LANCZOS)
    x, y = pad + (i % cols) * (tw + pad), pad + (i // cols) * (th + pad)
    sheet.paste(im, (x, y)); ImageDraw.Draw(sheet).rectangle([x, y, x + tw, y + th], outline="#868e96", width=2)
sheet.save(os.path.join(root, "contact-sheet.png"))
print("contact-sheet.png", sheet.size)
