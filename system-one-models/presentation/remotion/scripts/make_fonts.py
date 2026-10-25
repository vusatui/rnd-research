#!/usr/bin/env python3
"""Merge the unicode-range subsets of Excalifont shipped with @excalidraw/excalidraw into ONE woff2
subset Liberation Sans to its arrows (Excalifont has no →) and copy Cascadia Code, so the deck needs no network at runtime.
Needs: pip install fonttools brotli, and ../tools/node_modules (npm install in ../tools)."""
import glob, os, shutil, tempfile
from fontTools.ttLib import TTFont
from fontTools.merge import Merger

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "..", "tools", "node_modules", "@excalidraw", "excalidraw", "dist", "prod", "fonts")
OUT = os.path.join(HERE, "..", "src", "assets", "fonts")
os.makedirs(OUT, exist_ok=True)

tmp = tempfile.mkdtemp()
parts = []
for i, p in enumerate(sorted(glob.glob(os.path.join(FONTS, "Excalifont", "*.woff2")))):
    f = TTFont(p); f.flavor = None
    out = os.path.join(tmp, f"{i}.ttf"); f.save(out); parts.append(out)
merged = Merger().merge(parts)
merged.flavor = "woff2"
merged.save(os.path.join(OUT, "Excalifont.woff2"))
# Excalifont has no arrows (→); like Excalidraw, fall back to Liberation Sans, subset to the arrows block only
from fontTools import subset
opts = subset.Options(); opts.flavor = "woff2"
lib = subset.load_font(os.path.join(FONTS, "Liberation", "LiberationSans-Regular.woff2"), opts)
sub = subset.Subsetter(opts); sub.populate(unicodes=range(0x2190, 0x2200)); sub.subset(lib)
subset.save_font(lib, os.path.join(OUT, "LiberationSans-Arrows.woff2"), opts)
shutil.copy(os.path.join(FONTS, "Cascadia", "CascadiaCode-Regular.woff2"), os.path.join(OUT, "CascadiaCode-Regular.woff2"))
print("fonts ->", OUT, sorted(os.listdir(OUT)))
