#!/usr/bin/env python3
"""Serious variant of the System One / Jev deck: 19 Excalidraw frames (1600x900), hand-drawn style
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

# 10 Moderation
new_frame("Use case: moderation")
title("Moderation")
s.rect(100, 300, 330, 150, fill="#ffffff", stroke=NAVY, sw=3)
s.label(265, 345, "comment", 40, NAVY)
for i in range(2):
    s.line([(135, 395 + i * 28), (395 - i * 60, 395 + i * 28)], stroke=SLATE, sw=3)
arr([(450, 375), (570, 375)])
box(590, 325, 200, 100, "Jev", 56, fill=ACC_L, stroke=ACC, color=ACC)
arr([(810, 375), (880, 375)], ACC)
# three lanes on a confidence strip
lanes = [("Allow", 900, 180, LIGHT, NAVY), ("Human review", 1090, 290, ACC_L, ACC), ("Block", 1390, 130, LIGHT, NAVY)]
for t, x, w, f, c in lanes:
    s.rect(x, 330, w - 10, 90, fill=f, stroke=c, sw=3)
    s.label(x + (w - 10) / 2, 375, t, 32, c)
check(960, 470, 0.9, NAVY, 6)
person(1225, 450, 0.55, ACC)
cross(1430, 470, 0.9, NAVY, 6)
arr([(900, 590), (1510, 590)], SLATE, tail="arrow", sw=3)
s.text(900, 610, "sure it's fine", 30, SLATE)
s.text(1510, 610, "sure it's not", 30, SLATE, align="right")
s.label(800, 760, "unsure → ask a person", 42, ACC)
tag(100, 240, "illustrative", size=26)

# 11 Fraud triage
new_frame("Use case: fraud triage")
title("Fraud triage")
s.rect(100, 330, 330, 190, fill="#ffffff", stroke=NAVY, sw=3)
s.label(265, 380, "payment", 42, NAVY)
s.label(265, 445, "unusual?", 42, SLATE)
arr([(450, 425), (580, 425)])
box(600, 375, 200, 100, "Jev", 56, fill=ACC_L, stroke=ACC, color=ACC)
arr([(820, 425), (940, 425)], ACC)
s.text(960, 285, "risk", 40, NAVY)
gauge(960, 340, 480, 0.8, 0.6)
s.text(960, 395, "low", 30, SLATE)
s.text(1440, 395, "high", 30, SLATE, align="right")
arr([(1300, 450), (1300, 560)], ACC)
magnifier(1260, 580, 1.0, ACC)
s.label(1300, 730, "closer look", 40, ACC)
arr([(1010, 450), (1010, 560)], SLATE)
check(980, 580, 1.0, NAVY, 7)
s.label(1010, 730, "fast path", 40, NAVY)
caption("a first look, not a verdict", 835, SLATE, 36)
tag(100, 240, "illustrative", size=26)

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

# 13 Demo: request
new_frame("Live demo: request")
title("Live demo: request")
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
s.text(100, 835, "workshop-lite/jev_client.py · local emulator unless a Jev key is set", 30, SLATE)

# 14 Demo: response
new_frame("Live demo: response")
title("Live demo: response")
resp = ['{', '  "department": {', '    "type": "choice",', '    "choice": "technical",', '    "confidence": 1.0,',
        '    "probabilities": {', '      "billing": 0.0,', '      "technical": 1.0,', '      "sales": 0.0 }', '  },',
        '  "urgent": { "type": "noul",', '              "noul": 1.0 }', '}']
code_panel(100, 215, 720, resp, size=26, hl={3: ACC_L})
arr([(850, 450), (960, 450)], ACC)
code = ['d = answers["department"]', '', 'if d["confidence"] >= 0.7:', '    route(d["choice"])', 'else:', '    ask_a_human()']
s.rect(980, 215, 520, 300, fill="#ffffff", stroke=ACC, sw=3)
for i, ln in enumerate(code):
    if ln:
        s._base("text", 1005, 240 + i * 38, len(ln) * 26 * 0.586, 34, stroke=NAVY if i != 2 else ACC, text=ln, originalText=ln, fontSize=26,
                fontFamily=3, textAlign="left", verticalAlign="top", containerId=None, autoResize=True, lineHeight=1.25)
s.label(1240, 570, "our code decides", 42, ACC)
tag(100, 745, "EMULATOR output, not real Jev", size=32)
s.text(100, 815, "A free LLM behind a Jev-shaped endpoint (workshop-lite/sample_output.txt)", 30, SLATE)

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
for i, t in enumerate(["Right model\nfor the job", "The model answers,\nyour code decides", "Fast first,\nbig model if unsure"]):
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
for i, t in enumerate(["Run the workshop", "Poke the API calls", "Compare the approaches", "Read the sources"]):
    s.ellipse(110, 440 + i * 85 + 12, 26, 26, fill=ACC, stroke=ACC, sw=2)
    s.text(165, 438 + i * 85, t, 48, NAVY)
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
