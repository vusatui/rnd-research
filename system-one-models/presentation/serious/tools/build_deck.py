#!/usr/bin/env python3
"""Serious variant of the System One / Jev deck: 23 Excalidraw frames (2 of them play recorded demo clips in present.html) (1600x900), hand-drawn style
(Excalifont, roughness 1), restrained navy + one orange accent, no characters.
   python3 build_deck.py     -> ../presentation.excalidraw (+ ../qr.png)
Reuses ../../tools/excal.py (the scene builder of the light deck)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from excal import Scene, validate, measure
ROOT = os.path.abspath(os.path.join(HERE, ".."))

NAVY, SLATE, LIGHT, MID = "#1c2b4a", "#5b6b82", "#e8edf4", "#c5cfdd"
ACC, ACC_L = "#e8590c", "#ffe3d1"
W, H, GAP, COLS = 1600, 900, 240, 4
REPO = "https://github.com/vusatui/rnd-research"

s = Scene(seed=11)
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


# =====================================================================
# 01 Title
new_frame("Title")
s.text(100, 250, "System One models", 120, NAVY)
s.line([(104, 400), (700, 404), (1180, 399)], stroke=ACC, sw=7)
s.text(104, 430, "AI that decides, instead of writes", 52, SLATE)
# doodle: document -> chip -> bars
doc(130, 640, 90, 118)
arr([(250, 700), (400, 700)], NAVY)
chip(450, 650, 120, 100)
arr([(640, 700), (790, 700)], ACC)
bars(840, 640, [0.25, 0.9, 0.35], bw=36, hmax=120, hi=1)
s.text(1500, 150, "Internal talk · 30 min", 30, SLATE, align="right")

# 02 Two kinds of models
new_frame("Two kinds of models")
title("Two kinds of AI models")
s.text(100, 250, "Generator", 44, SLATE)
doc(100, 320, 90, 115, 3)
arr([(220, 378), (450, 378)])
box(470, 330, 340, 96, "Text generator", 40)
arr([(830, 378), (1060, 378)])
doc(1090, 316, 110, 130, 5)
doc(1220, 316, 110, 130, 5)
s.text(1360, 350, "…", 70, SLATE)
s.text(100, 520, "Decider", 44, ACC)
doc(100, 590, 90, 115, 3)
arr([(220, 648), (450, 648)], ACC)
box(470, 600, 340, 96, "Decision model", 40, fill=ACC_L, stroke=ACC)
arr([(830, 648), (1060, 648)], ACC)
s.rect(1090, 580, 330, 135, fill="#ffffff", stroke=ACC, sw=3)
bars(1130, 600, [0.2, 0.85, 0.3], bw=36, hmax=95, hi=1)
check(1290, 625, 1.0, ACC, 8)
caption("Text out   vs   a decision out", 810)

# 03 Fast and slow
new_frame("Fast and slow")
title("Two ways to think")
s.rect(100, 240, 650, 400, fill=ACC_L, stroke=ACC, sw=3)
bolt(380, 290, 1.0)
s.label(425, 520, "System 1", 56, ACC)
s.label(425, 590, "fast · instinct", 38, NAVY)
s.rect(850, 240, 650, 400, fill=LIGHT, stroke=NAVY, sw=3)
magnifier(1090, 300, 1.4)
s.label(1175, 520, "System 2", 56, NAVY)
s.label(1175, 590, "slow · deliberate", 38, SLATE)
arr([(425, 665), (425, 735)], ACC)
caption("Decision models are built for System 1 jobs", 780, NAVY, 42, 800)
s.text(1500, 660, "idea from Kahneman", 28, SLATE, align="right")

# 04 What is Jev
new_frame("What is Jev")
title("What is Jev?")
s.text(100, 165, "A hosted System One model from TypeSafe AI", 38, SLATE)
s.ellipse(560, 300, 480, 260, fill=ACC_L, stroke=ACC, sw=4)
s.label(800, 430, "Jev", 110, ACC)
for (x, t) in [(120, "one HTTP call"), (590, "no generated text"), (1060, "typed answers")]:
    box(x, 660, 420, 100, t, 40)
arr([(330, 650), (610, 540)], SLATE, sw=3)
arr([(800, 650), (800, 570)], SLATE, sw=3)
arr([(1270, 650), (990, 540)], SLATE, sw=3)

# 05 One call
new_frame("One call, one decision")
title("One call, one decision")
doc(110, 280, 100, 130, 4)
s.label(160, 445, "state", 40, NAVY)
s.text(110, 480, "(the text)", 30, SLATE)
s.rect(110, 570, 140, 130, fill="#ffffff", stroke=NAVY, sw=3)
for i, r in enumerate([0, 1, 0]):
    s.ellipse(135, 592 + i * 34, 20, 20, stroke=NAVY, sw=2, fill=ACC_L if r else "#ffffff", fillStyle="solid")
    s.line([(172, 602 + i * 34), (225, 602 + i * 34)], stroke=SLATE, sw=3)
s.label(180, 735, "questions", 40, NAVY)
arr([(270, 345), (470, 450)])
arr([(270, 635), (470, 520)])
box(480, 400, 340, 150, "Jev", 80, fill=ACC_L, stroke=ACC, color=ACC)
arr([(840, 475), (1010, 475)], ACC)
s.rect(1030, 300, 470, 340, fill="#ffffff", stroke=ACC, sw=3)
s.text(1060, 325, "department", 36, NAVY)
bars(1070, 375, [0.12, 0.88, 0.1], bw=40, hmax=100, hi=1)
s.text(1260, 400, "technical", 40, ACC)
s.text(1060, 520, "urgent?", 36, NAVY)
gauge(1230, 525, 230, 0.9)
s.label(1265, 695, "numbers, not sentences", 38, SLATE)
tag(1180, 740, "illustrative")

# 06 Question types
new_frame("Three kinds of questions")
title("Three kinds of questions")
cards = [("Choice", "pick one", 100), ("Score", "rate on a scale", 580), ("Yes / no", "probability of yes", 1060)]
for name, sub, x in cards:
    s.rect(x, 250, 440, 480, fill=LIGHT, stroke=NAVY, sw=3)
    s.label(x + 220, 320, name, 56, ACC)
    s.label(x + 220, 385, sub, 36, SLATE)
# choice: three options, one picked
for i, t in enumerate(["billing", "technical", "sales"]):
    yy = 460 + i * 70
    s.ellipse(150, yy, 34, 34, stroke=NAVY, sw=3, fill=ACC_L if i == 1 else "#ffffff")
    s.text(205, yy - 4, t, 38, ACC if i == 1 else NAVY)
# score: scale
s.line([(630, 560), (980, 560)], stroke=NAVY, sw=4)
for i in range(5):
    s.line([(630 + i * 87.5, 540), (630 + i * 87.5, 580)], stroke=NAVY, sw=3)
s.ellipse(759, 538, 44, 44, fill=ACC_L, stroke=ACC, sw=4)
s.text(630, 620, "calm", 34, SLATE)
s.text(980, 620, "angry", 34, SLATE, align="right")
# yes/no: gauge
gauge(1110, 545, 340, 0.82, 0.5)
s.text(1110, 600, "no", 34, SLATE)
s.text(1450, 600, "yes", 34, ACC, align="right")
s.label(1280, 480, "urgent?", 40, NAVY)

# 07 Not only Jev
new_frame("Not only Jev")
title("Not only Jev")
s.label(800, 330, "Same shape", 60, ACC)
s.label(800, 400, "text + questions  →  typed answers", 38, SLATE)
for x, t, sub in [(100, "OpenAI", "Decisions API (beta)"), (580, "Cloudflare", "Clef, open weights"), (1060, "Unsloth", "recipe to train your own")]:
    s.rect(x, 540, 440, 200, fill=LIGHT, stroke=NAVY, sw=3)
    s.label(x + 220, 600, t, 52, NAVY)
    s.label(x + 220, 675, sub, 34, SLATE)
    arr([(x + 220, 535), (800 + (x + 220 - 800) * 0.3, 450)], SLATE, sw=3)

# 08 Where it fits
new_frame("Where it fits")
title("Where it fits")
items = ["Routing", "Moderation", "Fraud triage", "Form checks", "Intent detection", "Approvals"]


def icon(i, cx, cy):
    if i == 0: fork(cx - 45, cy - 40)
    elif i == 1: shield(cx - 45, cy - 55, 0.65)
    elif i == 2: magnifier(cx - 40, cy - 45, 0.9)
    elif i == 3:
        s.rect(cx - 40, cy - 40, 80, 80, fill="#ffffff", stroke=NAVY, sw=3, round_=False); check(cx - 25, cy - 28, 0.8, ACC, 6)
    elif i == 4:
        s.rect(cx - 55, cy - 40, 110, 70, fill="#ffffff", stroke=NAVY, sw=3)
        s.line([(cx - 20, cy + 30), (cx - 30, cy + 55), (cx + 5, cy + 30)], stroke=NAVY, sw=3)
        s.label(cx, cy - 5, "?", 56, ACC)
    else:
        s.ellipse(cx - 45, cy - 45, 90, 90, fill=ACC_L, stroke=ACC, sw=3, fillStyle="hachure"); check(cx - 28, cy - 25, 0.9, NAVY, 6)


for i, t in enumerate(items):
    x, y = 100 + (i % 3) * 480, 240 + (i // 3) * 290
    s.rect(x, y, 440, 250, fill=LIGHT, stroke=NAVY, sw=3)
    icon(i, x + 220, y + 95)
    s.label(x + 220, y + 200, t, 44, NAVY)

# 09 Routing
new_frame("Use case: routing")
title("Routing")
doc(100, 380, 100, 130, 3)
s.text(90, 530, "ticket", 36, SLATE)
arr([(230, 445), (400, 445)])
box(420, 395, 240, 100, "Jev", 56, fill=ACC_L, stroke=ACC, color=ACC)
arr([(680, 425), (950, 280)], SLATE)
arr([(680, 445), (950, 445)], ACC)
arr([(680, 465), (950, 610)], SLATE)
box(960, 220, 300, 100, "Billing", 42)
box(960, 395, 300, 100, "Technical", 42, fill=ACC_L, stroke=ACC, color=ACC)
box(960, 570, 300, 100, "Sales", 42)
arr([(540, 510), (540, 690)], SLATE, style="dashed", sw=3)
s.text(565, 570, "unsure", 36, SLATE)
person(540, 700, 0.6, SLATE)
s.text(590, 730, "human", 36, SLATE)
tag(1290, 235, "illustrative", size=26)

# 12 Cascade
new_frame("Fast first")
title("Fast first")
for i in range(8):
    s.ellipse(100 + (i % 2) * 50, 300 + (i // 2) * 60, 32, 32, fill=MID, stroke=NAVY, sw=2)
s.text(100, 550, "all requests", 34, SLATE)
arr([(230, 400), (420, 400)])
box(440, 340, 300, 120, "Fast model", 46, fill=ACC_L, stroke=ACC, color=ACC)
arr([(760, 370), (1060, 370)], ACC)
s.label(910, 335, "most", 36, ACC)
s.rect(1080, 330, 380, 90, fill=LIGHT, stroke=NAVY, sw=3)
s.label(1270, 375, "answered", 40, NAVY)
arr([(590, 480), (590, 640), (1060, 640)], SLATE, style="dashed", roundness=None)
s.text(610, 540, "unsure", 36, SLATE)
box(1080, 590, 380, 100, "Big LLM", 46)
arr([(1270, 700), (1270, 770)], SLATE)
s.label(1270, 810, "answered", 36, SLATE)


# ---------- Why not structured output + confidence? (measured section) ----------
# The real alternative
new_frame("The real alternative")
title("The real alternative")
s.text(100, 200, "Chat LLM + structured output", 40, SLATE)
doc(100, 300, 90, 115, 3)
arr([(210, 358), (300, 358)])
box(310, 310, 210, 96, "LLM", 46)
arr([(415, 416), (415, 462)])
code_panel(100, 470, 660, ['{', '  "department": "technical",', '  "confidence": 0.9', '}'], size=30)
s.text(840, 200, "Decision model", 40, ACC)
doc(840, 300, 90, 115, 3)
arr([(950, 358), (1040, 358)], ACC)
box(1050, 310, 210, 96, "Jev", 46, fill=ACC_L, stroke=ACC, color=ACC)
arr([(1155, 416), (1155, 462)], ACC)
s.rect(840, 470, 660, 250, fill="#ffffff", stroke=ACC, sw=3)
bars(880, 510, [0.04, 0.9, 0.02, 0.02, 0.02], bw=56, hmax=130, hi=1)
for i, t in enumerate(["bill", "tech", "acct", "sales", "other"]):
    s.label(908 + i * 68, 670, t, 22, SLATE)
s.text(1260, 540, "technical", 40, ACC)
s.text(1260, 600, "p = 0.90", 36, NAVY)
caption("Both give a label and a number", 800, NAVY, 42)

# Where the number comes from
new_frame("Where the number comes from")
title("Where the number comes from")
s.rect(100, 230, 680, 480, fill=LIGHT, stroke=NAVY, sw=3)
s.label(440, 290, "Written", 56, NAVY)
for i, t in enumerate(["0", ".", "9"]):
    s.rect(230 + i * 100, 380, 80, 90, fill="#ffffff", stroke=NAVY, sw=3)
    s.label(270 + i * 100, 425, t, 52, NAVY)
    if i:
        arr([(214 + i * 100, 425), (228 + i * 100, 425)], SLATE, sw=2)
s.label(440, 540, "a token the model writes", 34, SLATE)
s.label(440, 600, "one guess · coarse", 34, SLATE)
s.label(440, 650, "costs output tokens", 34, SLATE)
s.rect(820, 230, 680, 480, fill=ACC_L, stroke=ACC, sw=3)
s.label(1160, 290, "Computed", 56, ACC)
bars(985, 360, [0.05, 0.75, 0.12, 0.05, 0.03], bw=44, hmax=120, hi=1)
s.label(1160, 540, "a probability for every option", 34, NAVY)
s.label(1160, 600, "one pass · fine-grained", 34, NAVY)
s.label(1160, 650, "output not billed", 34, NAVY)
caption("Different kinds of number. Measure both.", 790, NAVY, 42)

# How we tested
new_frame("How we tested")
title("How we tested")
box(100, 250, 380, 150, "250 tickets\nsynthetic", 40)
arr([(500, 325), (590, 325)])
box(610, 250, 380, 150, "2 blind\nlabellers", 40)
arr([(1010, 325), (1100, 325)])
box(1120, 250, 380, 150, "150 held-out\ntest tickets", 40, fill=ACC_L, stroke=ACC, color=ACC)
arr([(1310, 420), (1310, 470), (800, 470), (800, 510)], SLATE, roundness=None)
box(300, 520, 1000, 110, "8 methods · same tickets · same options", 40)
for i, t in enumerate(["accuracy", "calibration", "latency", "$ per 1,000"]):
    tag(150 + i * 340, 690, t, NAVY, 34)
s.text(100, 820, "data: free models · paid calls only for models under test", 28, SLATE)

# Same 150 tickets: the numbers
new_frame("Same 150 tickets")
title("Same 150 tickets")
cols = [("", 100, 400), ("accuracy", 500, 200), ("ECE", 700, 170), ("values", 870, 190), ("latency", 1060, 220), ("$ / 1k", 1280, 220)]
rows_ = [("Jev", "93%", "0.04", "35", "0.16 s", "$0.025", True),
         ("GPT-6 Sol", "93%", "0.04", "19", "2.1 s", "$1.34", False),
         ("Claude Sonnet", "94%", "0.11", "17", "1.0 s", "$2.00", False),
         ("DeepSeek Flash", "95%", "0.07", "12", "0.5 s", "$0.046", False),
         ("DeepSeek × 5 votes", "97%", "0.02", "3", "0.8 s", "$0.15", False)]
y0, rh = 215, 92
for (t, x, w) in cols[1:]:
    s.label(x + w / 2, y0 + 40, t, 32, SLATE)
for r, row in enumerate(rows_):
    y = y0 + rh * (r + 1)
    hi = row[-1]
    s.rect(100, y + 6, 1400, rh - 12, fill=ACC_L if hi else LIGHT, stroke=ACC if hi else MID, sw=3 if hi else 2)
    s.text(130, y + 22, row[0], 38, ACC if hi else NAVY)
    for (t, x, w), v in zip(cols[1:], row[1:6]):
        s.label(x + w / 2, y + rh / 2, v, 38, ACC if hi else NAVY)
s.text(130, 795, "department question  ·  differences within noise", 26, SLATE)
s.text(130, 835, "values = distinct confidences  ·  ECE = calibration error (lower is better)", 26, SLATE)

# What the numbers say
new_frame("What the numbers say")
title("What the numbers say")
verdict = [(True, "50-80× cheaper than strong LLMs"), (True, "6-13× faster"), (True, "one call, every option scored"),
           (None, "same accuracy, similar calibration")]
for i, (ok, t) in enumerate(verdict):
    y = 250 + i * 100
    if ok:
        check(130, y, 0.75, ACC, 7)
    else:
        s.label(155, y + 25, "≈", 64, SLATE)
    s.text(220, y - 4, t, 46, NAVY if ok else SLATE)
s.rect(100, 680, 1400, 120, fill=ACC_L, stroke=ACC, sw=3)
s.label(800, 740, "Not more accurate. Measure confidence on your data.", 44, ACC)

# 13 Demo: request
new_frame("Demo: request")
title("Demo: the request")
req = ['POST /v1/systemone', '{', '  "model": "jev-latest",', '  "state": "API returns 500 on every',
       '            request for 20 minutes…",', '  "questions": {', '    "department": {', '      "type": "choice",',
       '      "criteria": { "billing": …,', '                    "technical": …,', '                    "sales": … }',
       '    },', '    "urgent": { "type": "noul" }', '  }', '}']
h = code_panel(100, 215, 820, req, size=28, hl={0: ACC_L})
arr([(950, 372), (1050, 372)], ACC, sw=3)
s.text(1070, 340, "state", 44, ACC)
s.text(1070, 390, "the text", 30, SLATE)
arr([(950, 470), (1050, 470)], ACC, sw=3)
s.text(1070, 440, "questions", 44, ACC)
s.text(1070, 490, "what we want", 30, SLATE)
tag(1070, 660, "shortened", size=28)
s.text(100, 835, "real Jev via OpenRouter · make lite-jev", 30, SLATE)

# Recorded demo: two short clips (Remotion replay of the real files + real recorded runs, ../demo/).
# The static frame shows a poster of the clip; present.html plays the mp4 exactly over the VIDEO_BOX.
VIDEO_BOX = (176, 150, 1248, 702)
DEMOS = [("demo-1-one-call", "One call"), ("demo-2-same-tickets", "Same tickets")]


def clip_len(path):
    try:
        import subprocess
        sec = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                   capture_output=True, text=True, check=True).stdout)
        t = int(round(sec))
        return f"{t // 60}:{t % 60:02d}"
    except Exception:
        return ""


for n, (vid, name) in enumerate(DEMOS, 1):
    new_frame(f"Demo {n} {name}")
    s.text(100, 42, f"Demo {n}/{len(DEMOS)} · {name}", 56, NAVY)
    w, _ = measure(f"Demo {n}/{len(DEMOS)} · {name}", 56)
    s.line([(100, 110), (100 + w * 0.6, 112), (100 + w, 109)], stroke=ACC, sw=5)
    ln = clip_len(os.path.join(ROOT, "demo", "videos", f"{vid}.mp4"))
    s.text(1500, 60, f"recorded · {ln}" if ln else "recorded", 30, SLATE, align="right")
    x, y, bw, bh = VIDEO_BOX
    poster = os.path.join(ROOT, "demo", "videos", f"{vid}.poster.jpg")
    if os.path.exists(poster):
        s.image(poster, x, y, bw, bh)
    else:  # clip not rendered yet (re-recording after review)
        s.rect(x, y, bw, bh, fill=LIGHT, stroke=MID, sw=2)
        s.label(x + bw / 2, y + bh / 2 + 110, "recorded clip · being re-recorded", 34, SLATE)
    s.rect(x - 6, y - 6, bw + 12, bh + 12, stroke=NAVY, sw=3)
    # play badge (hidden by the video while it plays)
    s.ellipse(x + bw / 2 - 60, y + bh / 2 - 60, 120, 120, fill="#ffffff", stroke=ACC, sw=4)
    s.line([(x + bw / 2 - 18, y + bh / 2 - 32), (x + bw / 2 + 34, y + bh / 2), (x + bw / 2 - 18, y + bh / 2 + 32)], stroke=ACC, fill=ACC, closed=True, sw=3)

# 15 Use it / skip it
new_frame("Use it, skip it")
title("Use it. Skip it.")
s.rect(100, 230, 680, 520, fill=ACC_L, stroke=ACC, sw=3)
s.text(140, 255, "Use it for", 50, ACC)
for i, t in enumerate(["sorting", "yes / no checks", "high volume", "fast answers"]):
    check(150, 360 + i * 92, 0.7, ACC, 6)
    s.text(215, 352 + i * 92, t, 44, NAVY)
s.rect(820, 230, 680, 520, fill=LIGHT, stroke=NAVY, sw=3)
s.text(860, 255, "Skip it for", 50, SLATE)
for i, t in enumerate(["writing text", "explaining why", "multi-step reasoning", "open chat"]):
    cross(860, 360 + i * 92, 0.7, SLATE, 6)
    s.text(935, 352 + i * 92, t, 44, NAVY)

# 16 Limits
new_frame("Honest limits")
title("Honest limits")
lim = [("Text first", "no audio, no video"), ("English works best", "other languages weaker"),
       ("Test on your data", "check the probabilities"), ("Vendor numbers", "are claims, not proof")]
for i, (a, b) in enumerate(lim):
    x, y = 100 + (i % 2) * 740, 240 + (i // 2) * 270
    s.rect(x, y, 700, 230, fill=LIGHT, stroke=NAVY, sw=3)
    s.line([(x + 28, y + 40), (x + 30, y + 120), (x + 27, y + 190)], stroke=ACC, sw=6)
    s.text(x + 50, y + 55, a, 52, NAVY)
    s.text(x + 50, y + 130, b, 38, SLATE)

# 17 Takeaways
new_frame("Three takeaways")
title("Three takeaways")
for i, t in enumerate(["Pick it for price,\nspeed and format", "The model answers,\nyour code decides", "Measure confidence\non your data"]):
    x = 100 + i * 490
    s.ellipse(x + 150, 250, 120, 120, fill=ACC_L, stroke=ACC, sw=4)
    s.label(x + 210, 312, str(i + 1), 72, ACC)
    s.rect(x, 420, 420, 260, fill=LIGHT, stroke=NAVY, sw=3)
    s.label(x + 210, 550, t, 38, NAVY)

# 18 Try it yourself
new_frame("Try it yourself")
title("Try it yourself")
s.text(100, 250, REPO, 44, ACC)
s.text(100, 315, "→ system-one-models/", 40, NAVY)
for i, t in enumerate(["Run the workshop", "Compare the approaches", "Read the sources"]):
    s.ellipse(110, 450 + i * 95 + 12, 26, 26, fill=ACC, stroke=ACC, sw=2)
    s.text(165, 448 + i * 95, t, 48, NAVY)
qr_path = os.path.join(ROOT, "qr.png")  # made by make_qr.py (segno)
s.rect(1030, 230, 460, 460, fill="#ffffff", stroke=NAVY, sw=3)
s.image(qr_path, 1050, 250, 420, 420)
s.label(1260, 740, "scan me", 38, SLATE)
s.rect(1030, 230, 460, 460, stroke=ACC, sw=3, fill="transparent", opacity=0)

# 19 Questions
new_frame("Questions")
s.label(800, 380, "Questions?", 140, NAVY)
s.line([(430, 480), (800, 486), (1170, 479)], stroke=ACC, sw=7)
s.label(800, 600, "System One models · Jev", 40, SLATE)

out = s.to_json()
probs = validate(out)
if probs:
    print("PROBLEMS:", *probs[:20], sep="\n"); sys.exit(1)
json.dump(out, open(os.path.join(ROOT, "presentation.excalidraw"), "w"))
print("presentation.excalidraw:", count[0], "frames,", len(out["elements"]), "elements")
