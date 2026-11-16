#!/usr/bin/env python3
"""Combine export/slide-*.png into presentation.pdf (one 16:9 page per slide)."""
import glob, os
from PIL import Image
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ims = [Image.open(f).convert("RGB") for f in sorted(glob.glob(os.path.join(root, "export", "slide-*.png")))]
ims[0].save(os.path.join(root, "presentation.pdf"), save_all=True, append_images=ims[1:], resolution=100)
print("presentation.pdf", len(ims), "pages")
