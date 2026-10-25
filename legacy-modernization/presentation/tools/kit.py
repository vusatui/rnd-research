"""Shared drawing kit (palette, frame/title helpers, doodle icons) for the serious Excalidraw decks.
Copied from system-one-models/presentation/serious/tools/build_deck.py (unchanged helpers)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from excal import Scene, validate, measure
ROOT = os.path.abspath(os.path.join(HERE, ".."))

NAVY, SLATE, LIGHT, MID = "#1c2b4a", "#5b6b82", "#e8edf4", "#c5cfdd"
ACC, ACC_L = "#e8590c", "#ffe3d1"
W, H, GAP, COLS = 1600, 900, 240, 4
REPO = "https://github.com/vusatui/rnd-research"

s = Scene(seed=int(os.environ.get("DECK_SEED", "11")))
count = [0]


def new_frame(title):
    i = count[0]; count[0] += 1
    s.frame(f"Slide {i + 1:02d} {title}", (i % COLS) * (W + GAP), (i // COLS) * (H + GAP), W, H, "#ffffff")
    s.text(1530, 842, f"{i + 1}", 28, MID, align="right")


def title(t, sub=None):
    s.text(100, 64, t, 64, NAVY)
    w, _ = measure(t, 64)
    s.line([(100, 140), (100 + w * 0.6, 142), (100 + w, 139)], stroke=ACC, sw=5)
    if sub:
        s.text(100, 165, sub, 36, SLATE)


def caption(t, y=800, color=SLATE, size=38, x=800):
    s.label(x, y, t, size, color)


def tag(x, y, t, color=ACC, size=28):
    w, h = measure(t, size)
    s.rect(x, y, w + 36, h + 14, fill="#ffffff", stroke=color, sw=2, style="dashed")
    s.text(x + 18, y + 7, t, size, color)


def box(x, y, w, h, t, size=40, fill=LIGHT, stroke=NAVY, color=NAVY, **kw):
    s.rect(x, y, w, h, fill=fill, stroke=stroke, **kw)
    s.label(x + w / 2, y + h / 2, t, size, color)


def arr(pts, color=NAVY, **kw):
    kw.setdefault("sw", 4)
    return s.arrow(pts, stroke=color, **kw)


# ---------- doodle icons (all Excalidraw primitives) ----------
def doc(x, y, w=100, h=130, lines=4, color=NAVY, fill="#ffffff"):
    s.rect(x, y, w, h, fill=fill, stroke=color, sw=3, round_=False)
    for i in range(lines):
        ln = w - 36 if i < lines - 1 else (w - 36) * 0.6
        s.line([(x + 18, y + 28 + i * 24), (x + 18 + ln, y + 28 + i * 24)], stroke=SLATE, sw=3)


def person(cx, y, k=1.0, color=NAVY):
    s.ellipse(cx - 20 * k, y, 40 * k, 40 * k, stroke=color, sw=3)
    s.line([(cx - 36 * k, y + 110 * k), (cx - 36 * k, y + 70 * k), (cx, y + 55 * k), (cx + 36 * k, y + 70 * k), (cx + 36 * k, y + 110 * k)], stroke=color, sw=3)


def chip(x, y, w, h, color=NAVY, fill=LIGHT):
    for i in range(1, 4):
        px = x + w * i / 4
        s.line([(px, y - 16), (px, y)], stroke=color, sw=3)
        s.line([(px, y + h), (px, y + h + 16)], stroke=color, sw=3)
        py = y + h * i / 4
        s.line([(x - 16, py), (x, py)], stroke=color, sw=3)
        s.line([(x + w, py), (x + w + 16, py)], stroke=color, sw=3)
    s.rect(x, y, w, h, fill=fill, stroke=color, sw=3)


def bars(x, y, vals, bw=34, hmax=100, hi=0, color=NAVY):
    for i, v in enumerate(vals):
        bh = max(6, hmax * v)
        c = ACC if i == hi else color
        s.rect(x + i * (bw + 12), y + hmax - bh, bw, bh, fill=ACC_L if i == hi else MID, stroke=c, sw=3, fillStyle="hachure", round_=False)
    s.line([(x - 8, y + hmax), (x + len(vals) * (bw + 12), y + hmax)], stroke=color, sw=3)


def check(x, y, k=1.0, color=ACC, sw=7):
    s.line([(x, y + 28 * k), (x + 22 * k, y + 52 * k), (x + 62 * k, y)], stroke=color, sw=sw)


def cross(x, y, k=1.0, color=SLATE, sw=7):
    s.line([(x, y), (x + 50 * k, y + 50 * k)], stroke=color, sw=sw)
    s.line([(x + 50 * k, y), (x, y + 50 * k)], stroke=color, sw=sw)


def bolt(x, y, k=1.0, fill=ACC_L, color=ACC):
    pts = [(0, 0), (60, 0), (35, 55), (80, 55), (10, 150), (28, 75), (-10, 75)]
    s.line([(x + px * k, y + py * k) for px, py in pts], stroke=color, fill=fill, closed=True, sw=3, fillStyle="hachure")


def magnifier(x, y, k=1.0, color=NAVY):
    s.ellipse(x, y, 56 * k, 56 * k, stroke=color, sw=4)
    s.line([(x + 50 * k, y + 50 * k), (x + 84 * k, y + 84 * k)], stroke=color, sw=7)


def shield(x, y, k=1.0, color=NAVY):
    s.line([(x, y), (x + 70 * k, y + 14 * k), (x + 140 * k, y), (x + 136 * k, y + 70 * k), (x + 70 * k, y + 130 * k), (x + 4 * k, y + 70 * k)],
           stroke=color, closed=True, sw=4, fill=LIGHT)
    check(x + 40 * k, y + 40 * k, 0.9 * k, ACC, 6)


def fork(x, y, color=NAVY):
    arr([(x, y + 40), (x + 40, y + 40), (x + 40, y + 8), (x + 90, y + 8)], color, sw=4)
    arr([(x + 40, y + 40), (x + 90, y + 40)], color, sw=4)
    arr([(x + 40, y + 40), (x + 40, y + 72), (x + 90, y + 72)], ACC, sw=4)


def gauge(x, y, w=240, level=0.7, thr=None):
    s.rect(x, y, w, 26, fill="#ffffff", stroke=NAVY, sw=3)
    s.rect(x + 3, y + 3, (w - 6) * level, 20, fill=ACC_L, stroke=ACC, sw=2, fillStyle="hachure", round_=False)
    if thr:
        s.line([(x + w * thr, y - 18), (x + w * thr, y + 44)], stroke=NAVY, sw=4, style="dashed")


def code_panel(x, y, w, lines, size=30, pad=28, hl=None):
    """Dark code panel; Cascadia (monospace) text. hl = {line_index: color}"""
    lh = size * 1.3
    h = len(lines) * lh + pad * 2
    s.rect(x, y, w, h, fill=NAVY, stroke=NAVY, sw=3, round_=True)
    for i, ln in enumerate(lines):
        if not ln:
            continue
        col = (hl or {}).get(i, "#e8edf4")
        s._base("text", x + pad, y + pad + i * lh, len(ln) * size * 0.586, size * 1.25, stroke=col, text=ln, originalText=ln,
                fontSize=size, fontFamily=3, textAlign="left", verticalAlign="top", containerId=None, autoResize=True, lineHeight=1.25)
    return h


