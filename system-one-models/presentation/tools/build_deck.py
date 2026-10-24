#!/usr/bin/env python3
"""Generate ../presentation.excalidraw  (18 frames, 1600x900 each, 4 per row).

Images: put PNGs named like the slots (see ../image-prompts.md) into ../images/ and re-run;
slots without an image are drawn as dashed placeholders.
   python3 build_deck.py
"""
import glob, json, os, sys
from excal import Scene, validate, INK

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMG = os.path.join(ROOT, "images")
W, H, GAP, COLS = 1600, 900, 240, 4

BLUE, BLUE_L = "#339af0", "#d0ebff"
PURP, PURP_L = "#7048e8", "#e5dbff"
YEL, YEL_L = "#fab005", "#fff3bf"
GRN, GRN_L = "#2f9e44", "#d3f9d8"
RED, RED_L = "#e03131", "#ffe3e3"
ORG, ORG_L = "#f76707", "#ffe8cc"
GRAY = "#868e96"

s = Scene()
n = [0]
SLOTS = []


def new_frame(title, bg):
    i = n[0]
    n[0] += 1
    s.frame(f"Slide {i + 1:02d} {title}", (i % COLS) * (W + GAP), (i // COLS) * (H + GAP), W, H, bg)


def slot(name, x, y, w, h, hint=""):
    """Reserved illustration slot; replaced by the image if images/<name>.* exists."""
    SLOTS.append(name)
    found = [p for p in glob.glob(os.path.join(IMG, name + ".*")) if p.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))]
    if found:
        s.image(found[0], x, y, w, h)
        return
    s.rect(x, y, w, h, fill="#ffffff", stroke=GRAY, style="dashed", sw=3, opacity=70)
    s.label(x + w / 2, y + h / 2 - 24, "IMAGE SLOT", 40, GRAY)
    s.label(x + w / 2, y + h / 2 + 30, name, 36, GRAY)


# ---------------- doodles ----------------
def bolt(x, y, k=1.0, fill=YEL):
    pts = [(0, 0), (60, 0), (35, 55), (80, 55), (10, 150), (28, 75), (-10, 75)]
    s.line([(x + px * k, y + py * k) for px, py in pts], stroke=INK, fill=fill, closed=True, sw=3)


def star(x, y, r=26, fill=YEL):
    import math
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    s.line(pts, fill=fill, closed=True, sw=2)


def card(x, y, w, h, txt, size=40, fill="#ffffff", stroke=INK):
    s.box(x, y, w, h, txt, size, fill=fill, stroke=stroke)


def bubble(x, y, w, h, txt, size=44, fill="#ffffff", tail="left"):
    s.rect(x, y, w, h, fill=fill, sw=3)
    if tail == "left":
        s.line([(x + 40, y + h - 2), (x + 10, y + h + 45), (x + 95, y + h - 2)], fill=fill, closed=True, sw=3)
        s.line([(x + 42, y + h - 3), (x + 94, y + h - 3)], stroke=fill, sw=5, rough=0)
    else:
        s.line([(x + w - 95, y + h - 2), (x + w - 10, y + h + 45), (x + w - 40, y + h - 2)], fill=fill, closed=True, sw=3)
        s.line([(x + w - 94, y + h - 3), (x + w - 42, y + h - 3)], stroke=fill, sw=5, rough=0)
    if txt:
        s.label(x + w / 2, y + h / 2, txt, size)


def squiggles(x, y, w, rows=4, gap=34, color=GRAY):
    import random
    r = random.Random(3)
    for i in range(rows):
        ww = w if i < rows - 1 else w * 0.55
        pts, cx = [], 0
        while cx < ww:
            pts.append((x + cx, y + i * gap + (8 if len(pts) % 2 else 0)))
            cx += 22
        s.line(pts, stroke=color, sw=3)


def robot(x, y, k=1.0, fill=BLUE_L):
    s.line([(x + 80 * k, y), (x + 80 * k, y - 40 * k)], sw=4)
    s.ellipse(x + 68 * k, y - 62 * k, 24 * k, 24 * k, fill=RED, sw=3)
    s.rect(x, y, 160 * k, 120 * k, fill=fill, sw=4)
    s.ellipse(x + 32 * k, y + 30 * k, 28 * k, 28 * k, fill="#ffffff", sw=3)
    s.ellipse(x + 100 * k, y + 30 * k, 28 * k, 28 * k, fill="#ffffff", sw=3)
    s.ellipse(x + 42 * k, y + 40 * k, 9 * k, 9 * k, fill=INK, sw=1)
    s.ellipse(x + 110 * k, y + 40 * k, 9 * k, 9 * k, fill=INK, sw=1)
    s.line([(x + 45 * k, y + 88 * k), (x + 80 * k, y + 102 * k), (x + 115 * k, y + 88 * k)], sw=4)
    s.rect(x + 20 * k, y + 135 * k, 120 * k, 100 * k, fill=fill, sw=4)
    bolt(x + 68 * k, y + 150 * k, 0.45 * k)


def bars(x, y, vals, colors, labels=None, bw=70, maxh=200, gap=36, size=30):
    for i, v in enumerate(vals):
        h = max(8, maxh * v)
        bx = x + i * (bw + gap)
        s.rect(bx, y + maxh - h, bw, h, fill=colors[i], sw=3, round_=False)
        if labels:
            s.label(bx + bw / 2, y + maxh + 28, labels[i], size)


def arrow_r(x1, y, x2, color=INK, sw=5):
    s.arrow([(x1, y), (x2, y)], stroke=color, sw=sw)


def title(txt, size=72, color=INK, y=50):
    s.label(W / 2, y + size * 0.6, txt, size, color)


# ======================= SLIDES =======================
# 01 title
new_frame("Title", "#fff9db")
s.text(100, 200, "System One", 130, INK)
s.line([(110, 360), (500, 367), (820, 358)], stroke=YEL, sw=14)
s.text(100, 420, "the fast brain for software", 52, PURP)
s.text(100, 520, "Jev & friends", 44, GRAY)
bolt(110, 650, 1.0)
star(300, 700, 30); star(380, 640, 20, ORG); star(450, 720, 24, BLUE_L)
slot("duo", 920, 90, 620, 720)

# 02 hook
new_frame("Hook: overkill", "#fff5f5")
bubble(80, 90, 620, 130, "Is this email urgent?", 52, "#ffffff")
s.arrow([(390, 290), (390, 380)], sw=6)
s.rect(150, 400, 480, 300, fill="#ffffff", sw=4)
squiggles(190, 440, 400, rows=6, gap=38)
s.label(390, 740, "3 pages later…", 52, RED)
s.text(80, 800, "We needed: YES or NO", 56, GRN)
slot("wizard_essay", 840, 80, 680, 740)

# 03 two brains
new_frame("Two ways to think", "#ffffff")
s.rect(0, 0, 800, H, fill=BLUE_L, stroke=BLUE_L, sw=1, rough=0, roundness=None)
s.rect(800, 0, 800, H, fill=PURP_L, stroke=PURP_L, sw=1, rough=0, roundness=None)
slot("hero_fast", 80, 90, 640, 520)
slot("prof_slow", 880, 90, 640, 520)
s.label(400, 690, "Fast", 100, BLUE)
s.label(400, 790, "gut feeling", 48)
s.label(1200, 690, "Slow", 100, PURP)
s.label(1200, 790, "careful thinking", 48)
s.ellipse(745, 330, 110, 110, fill="#ffffff", sw=4)
s.label(800, 385, "vs", 52)

# 04 two kinds of models
new_frame("Two kinds of AI models", "#f8f9fa")
title("Two kinds of AI models", 72)
for ox, col, colL, head, sub in ((100, PURP, PURP_L, "Writers", "LLMs"), (860, BLUE, BLUE_L, "Deciders", "System One")):
    s.rect(ox, 200, 640, 620, fill=colL, stroke=col, sw=4)
    s.label(ox + 320, 270, head, 80, col)
    s.label(ox + 320, 770, sub, 48, GRAY)
card(140, 400, 190, 120, "text", 44)
arrow_r(340, 460, 430, PURP)
bubble(440, 380, 260, 160, "", tail="left")
squiggles(465, 415, 210, rows=3, gap=34)
card(900, 400, 190, 120, "text", 44)
arrow_r(1100, 460, 1190, BLUE)
s.rect(1200, 380, 260, 160, fill="#ffffff", sw=3)
bars(1235, 400, [0.25, 0.9, 0.15], [GRAY, GRN, GRAY], bw=50, maxh=110, gap=22)
s.label(420, 650, "✍️", 100)
s.label(1180, 650, "🎯", 100)

# 05 how it works
new_frame("How it works", "#ffffff")
title("One call. One decision.", 72)
card(60, 250, 360, 160, "“Charged\ntwice!!”", 48, fill=YEL_L)
s.text(240, 190, "text", 40, GRAY, "center")
s.label(240, 470, "+", 70, GRAY)
card(60, 520, 360, 150, "Which team?", 48, fill=BLUE_L)
for i, (t, c) in enumerate((("billing", GRN_L), ("tech", ORG_L), ("sales", PURP_L))):
    s.box(40 + i * 130, 700, 120, 60, t, 28, fill=c, stroke=GRAY, sw=2)
s.text(240, 770, "question + options", 36, GRAY, "center")
arrow_r(450, 470, 650, INK)
s.rect(670, 300, 320, 340, fill=YEL_L, stroke=INK, sw=5)
robot(786, 380, 0.55)
s.label(830, 590, "Jev", 64)
arrow_r(1010, 470, 1130, INK)
s.rect(1150, 250, 400, 440, fill="#ffffff", sw=4)
bars(1200, 320, [0.92, 0.06, 0.02], [GRN, GRAY, GRAY], ["billing", "tech", "sales"], bw=80, maxh=260, gap=30, size=28)
s.label(1350, 740, "(example)", 34, GRAY)
s.label(800, 840, "No essay. Just numbers.", 52, PURP)

# 06 meet Jev
new_frame("Meet Jev", "#fff4e6")
s.rect(150, 160, 700, 360, fill="#ffffff", stroke=ORG, sw=6)
s.label(500, 340, "Jev", 220, INK)
bolt(790, 90, 0.8)
s.label(500, 610, "by TypeSafe AI", 64, ORG)
s.label(500, 720, "the first “System One” model", 50, GRAY)
robot(1050, 300, 1.2, fill=YEL_L)
star(1000, 200, 28); star(1330, 240, 22, ORG); star(1280, 640, 26, BLUE_L)

# 07 same idea, many logos
new_frame("Same idea, many names", "#f3f0ff")
title("Same idea. Many names.", 72)
cards = [(100, 200, "Jev", "TypeSafe", ORG_L), (860, 200, "Decisions API", "OpenAI", GRN_L),
         (100, 520, "Clef", "Cloudflare · open", BLUE_L), (860, 520, "DIY", "open-source recipe", YEL_L)]
for x, y, a, b, c in cards:
    s.rect(x, y, 640, 280, fill=c, sw=4)
    s.label(x + 320, y + 110, a, 84)
    s.label(x + 320, y + 210, b, 44, GRAY)
s.ellipse(710, 450, 180, 100, fill="#ffffff", sw=4)
s.label(800, 500, "🧠⚡", 60)

# 08 three question types
new_frame("Three kinds of questions", "#ebfbee")
title("Three kinds of questions", 72)
for i, (x, head, code, col) in enumerate(((80, "Pick one", "choice", BLUE_L), (580, "Rate it", "score", YEL_L),
                                          (1080, "Yes or no?", "noul", RED_L))):
    s.rect(x, 190, 440, 600, fill=col, sw=4)
    s.label(x + 220, 270, head, 64)
    s.label(x + 220, 730, code, 40, GRAY)
for k, (t, hit) in enumerate((("A", 0), ("B", 1), ("C", 0))):
    s.ellipse(150 + k * 130, 400, 110, 110, fill=GRN if hit else "#ffffff", sw=4)
    s.label(205 + k * 130, 455, t, 56)
s.label(300, 590, "🎯", 90)
s.line([(640, 470), (960, 470)], sw=8, stroke=GRAY)
s.ellipse(850, 440, 60, 60, fill=ORG, sw=4)
for k in range(5):
    star(655 + k * 70, 600, 30, YEL if k < 4 else "#ffffff")
s.rect(1180, 400, 240, 110, fill="#ffffff", sw=4)
s.label(1300, 455, "97% yes", 48, GRN)
s.label(1300, 590, "✅", 90)

# 09 use-case overview
new_frame("Where it shines", "#fff9db")
title("Where it shines", 72)
tiles = [("🎫", "Ticket routing"), ("🛡️", "Moderation"), ("🕵️", "Fraud triage"),
         ("✅", "Form checks"), ("💬", "Intent detection"), ("📝", "Approvals")]
cols = [BLUE_L, RED_L, YEL_L, GRN_L, PURP_L, ORG_L]
for i, (em, t) in enumerate(tiles):
    x, y = 90 + (i % 3) * 490, 200 + (i // 3) * 330
    s.rect(x, y, 440, 290, fill=cols[i], sw=4)
    s.label(x + 220, y + 110, em, 110)
    s.label(x + 220, y + 225, t, 48)

# 10 tickets
new_frame("Use case: ticket routing", "#e7f5ff")
slot("sorting_robot", 60, 110, 700, 680)
s.text(850, 110, "Ticket routing", 72, BLUE)
card(850, 260, 640, 140, "“App crashes at checkout!”", 40, fill=YEL_L)
s.arrow([(1170, 410), (1170, 500)], sw=6)
s.box(960, 520, 420, 130, "🔧 Tech team", 52, fill=BLUE_L, stroke=BLUE, sw=4)
s.label(1170, 700, "in a blink", 52, PURP)
s.label(1170, 780, "(illustrative)", 32, GRAY)

# 11 moderation
new_frame("Use case: moderation", "#fff5f5")
slot("bouncer", 60, 110, 700, 680)
s.text(850, 110, "Moderation", 72, RED)
rows = [("“You are all idiots”", "🚫 Block", RED_L, RED), ("“Nice docs, thanks!”", "✅ Allow", GRN_L, GRN),
        ("“Hmm, borderline…”", "👀 Human", YEL_L, YEL)]
for i, (a, b, c, col) in enumerate(rows):
    y = 270 + i * 190
    card(850, y, 400, 120, a, 34, fill="#ffffff")
    arrow_r(1260, y + 60, 1320, INK, 4)
    s.box(1330, y, 220, 120, b, 36, fill=c, stroke=col, sw=4)
s.label(1200, 830, "(illustrative)", 32, GRAY)

# 12 fraud
new_frame("Use case: fraud triage", "#f3f0ff")
slot("detective", 60, 110, 700, 680)
s.text(850, 110, "Fraud triage", 72, PURP)
rows = [("$9,999 · 3 a.m.\nabroad", "🚩 Look closer", RED_L, RED), ("Coffee · $4", "✅ Fine", GRN_L, GRN)]
for i, (a, b, c, col) in enumerate(rows):
    y = 300 + i * 230
    card(850, y, 340, 160, a, 36, fill="#ffffff")
    arrow_r(1200, y + 80, 1250, INK, 4)
    s.box(1260, y, 300, 160, b, 36, fill=c, stroke=col, sw=4)
s.label(1200, 800, "a fast first look", 52, PURP)

# 13 cascade
new_frame("Fast first, big model if unsure", "#fff9db")
title("Fast first. Big brain if unsure.", 68)
card(50, 240, 220, 130, "request", 40, fill="#ffffff")
arrow_r(280, 305, 380, INK)
s.rect(390, 210, 300, 190, fill=BLUE_L, stroke=BLUE, sw=5)
s.label(540, 270, "⚡", 80)
s.label(540, 350, "Fast model", 44)
s.arrow([(700, 270), (900, 270)], sw=5, stroke=GRN)
s.label(800, 230, "sure", 40, GRN)
s.box(910, 210, 300, 120, "Done ✅", 52, fill=GRN_L, stroke=GRN, sw=4)
s.label(1060, 370, "most of the time", 38, GRAY)
s.arrow([(540, 420), (540, 620), (700, 620)], sw=5, stroke=RED)
s.label(420, 520, "unsure", 40, RED)
s.rect(710, 540, 320, 160, fill=PURP_L, stroke=PURP, sw=5)
s.label(870, 600, "🧙", 70)
s.label(870, 670, "Big LLM", 44)
s.label(870, 750, "slower · pricier", 38, GRAY)
slot("relay", 1100, 450, 450, 400)

# 14 live demo
new_frame("Live demo", "#e9ecef")
s.rect(150, 120, 1300, 520, fill="#212529", stroke=INK, sw=5)
for i, c in enumerate((RED, YEL, GRN)):
    s.ellipse(190 + i * 56, 155, 36, 36, fill=c, sw=2)
s.text(200, 250, ">_  python jev_client.py", 60, "#69db7c")
s.text(200, 360, "text in", 60, "#ffd43b")
s.arrow([(520, 392), (900, 392)], stroke="#ffffff", sw=6)
s.text(940, 360, "decision out", 60, "#74c0fc")
s.rect(200, 480, 40, 80, fill="#69db7c", stroke="#69db7c", sw=1, rough=0)
s.label(800, 770, "LIVE DEMO", 130, RED)
star(250, 760, 36); star(1350, 760, 36, ORG)

# 15 when / when not
new_frame("Use it / skip it", "#ffffff")
s.rect(40, 40, 740, 820, fill=GRN_L, stroke=GRN, sw=4)
s.rect(820, 40, 740, 820, fill=RED_L, stroke=RED, sw=4)
s.label(410, 130, "✅  Use it for", 64, GRN)
s.label(1190, 130, "❌  Not for", 64, RED)
for i, t in enumerate(("🗂️  Sorting", "🔘  Yes / no checks", "📈  Huge volume", "⚡  Need speed")):
    s.text(110, 250 + i * 150, t, 56)
for i, t in enumerate(("✍️  Writing", "💬  Chatting", "🗣️  Explaining why", "🧩  Hard reasoning")):
    s.text(890, 250 + i * 150, t, 56)

# 16 caveats
new_frame("Honest caveats", "#fff9db")
title("Be honest about limits", 72)
notes = [(110, 210, -3, "Text only\n(for now)", YEL_L), (840, 230, 2, "English works\nbest", BLUE_L),
         (130, 520, 2, "Test it on\nYOUR data", GRN_L), (850, 520, -2, "Vendor numbers\n≠ proof", RED_L)]
for x, y, ang, t, c in notes:
    r = s.rect(x, y, 600, 260, fill=c, sw=4, angle=ang * 0.0175, round_=False)
    s.label(x + 300, y + 130, t, 60)

# 17 takeaways
new_frame("Takeaways", "#ebfbee")
title("Remember 3 things", 72)
items = [("Pick the right brain\nfor the job", BLUE), ("Model answers,\ncode decides", GRN), ("Fast first,\nbig LLM if unsure", PURP)]
for i, (t, c) in enumerate(items):
    y = 210 + i * 210
    s.ellipse(80, y, 130, 130, fill=c, stroke=c, sw=3)
    s.label(145, y + 65, str(i + 1), 80, "#ffffff")
    s.text(260, y + 5, t, 56)
slot("duo", 1040, 200, 500, 560)

# 18 Q&A
new_frame("Questions", "#fff0f6")
s.label(800, 330, "?", 420, PURP)
s.label(800, 700, "Questions?", 120)
s.label(800, 810, "thank you!", 56, GRAY)
bolt(200, 200, 1.3); star(1300, 250, 40); star(1380, 600, 28, ORG); star(220, 650, 32, BLUE_L)
bolt(1250, 330, 0.9, fill=BLUE_L)

# ---------------- output ----------------
out = s.to_json()
probs = validate(out)
if probs:
    print("INVALID:", *probs[:20], sep="\n  ")
    sys.exit(1)
with open(os.path.join(ROOT, "presentation.excalidraw"), "w") as f:
    json.dump(out, f, indent=1)
print(f"OK: {len(s.frames)} frames, {len(out['elements'])} elements, {len(out['files'])} embedded images; "
      f"slots: {sorted(set(SLOTS))}")
