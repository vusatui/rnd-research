#!/usr/bin/env python3
"""Serious Excalidraw deck: "Telling people it's AI" (EU AI Act Art. 50 transparency), 20 frames (1600x900),
same look as ai-finops/presentation and system-one-models/presentation/serious (Excalifont, roughness 1, navy + one orange accent).
   python3 make_qr.py && python3 build_deck.py     -> ../presentation.excalidraw
Facts on slides come from ../../research.md, ../../comparison.md and ../../workshop/results/."""
import os
from kit import *


# ---------- local doodles ----------
def bubble(x, y, w, h, t, size=38, color=NAVY, fill=LIGHT, tail="left", sw=3):
    if tail == "left":
        s.line([(x + 40, y + h - 2), (x + 26, y + h + 34), (x + 90, y + h - 2)], stroke=color, fill=fill, closed=True, sw=sw)
    else:
        s.line([(x + w - 40, y + h - 2), (x + w - 26, y + h + 34), (x + w - 90, y + h - 2)], stroke=color, fill=fill, closed=True, sw=sw)
    s.rect(x, y, w, h, fill=fill, stroke=color, sw=sw)
    s.label(x + w / 2, y + h / 2, t, size, color)


def cylinder(x, y, w, h, color=NAVY, fill=LIGHT):
    s.rect(x, y + 20, w, h - 20, fill=fill, stroke=color, sw=3, round_=False)
    s.ellipse(x, y, w, 40, fill=fill, stroke=color, sw=3)
    s.line([(x, y + h), (x + w * 0.25, y + h + 16), (x + w * 0.75, y + h + 16), (x + w, y + h)], stroke=color, sw=3)


def scales(cx, y, k=1.0, color=NAVY):
    s.line([(cx, y), (cx, y + 220 * k)], stroke=color, sw=5)
    s.line([(cx - 70 * k, y + 220 * k), (cx + 70 * k, y + 220 * k)], stroke=color, sw=5)
    s.line([(cx - 150 * k, y + 30 * k), (cx, y), (cx + 150 * k, y + 30 * k)], stroke=color, sw=5)
    for sx in (-150 * k, 150 * k):
        s.line([(cx + sx, y + 30 * k), (cx + sx - 50 * k, y + 120 * k)], stroke=SLATE, sw=3)
        s.line([(cx + sx, y + 30 * k), (cx + sx + 50 * k, y + 120 * k)], stroke=SLATE, sw=3)
        s.line([(cx + sx - 60 * k, y + 120 * k), (cx + sx, y + 150 * k), (cx + sx + 60 * k, y + 120 * k)], stroke=color, sw=4, fill=LIGHT, closed=True)


def img_icon(x, y, w=150, h=110, color=NAVY, fill="#ffffff"):
    """a little picture: frame + sun + hill"""
    s.rect(x, y, w, h, fill=fill, stroke=color, sw=3, round_=False)
    s.ellipse(x + w * 0.66, y + h * 0.14, w * 0.18, w * 0.18, stroke=color, sw=3)
    s.line([(x + 6, y + h - 6), (x + w * 0.32, y + h * 0.45), (x + w * 0.55, y + h * 0.75), (x + w * 0.7, y + h * 0.58), (x + w - 6, y + h - 6)], stroke=color, sw=3)


def ai_badge(cx, cy, r=34, color=ACC):
    s.ellipse(cx - r, cy - r, 2 * r, 2 * r, fill=ACC_L, stroke=color, sw=4)
    s.label(cx, cy, "AI", int(r * 1.0), color)


def dot(cx, cy, on, r=13):
    s.ellipse(cx - r, cy - r, 2 * r, 2 * r, fill=ACC_L if on else "#ffffff", stroke=ACC if on else MID, sw=3)


# =====================================================================
# 01 Title
new_frame("Title")
s.text(100, 215, "Telling people it's AI", 118, NAVY)
s.line([(104, 375), (700, 379), (1060, 374)], stroke=ACC, sw=7)
s.text(104, 405, "The EU AI Act, Article 50, in plain words", 52, SLATE)
bubble(130, 585, 330, 120, "Hello!", 48, NAVY, LIGHT, "left")
ai_badge(560, 645, 44)
arr([(640, 645), (800, 645)], NAVY)
img_icon(840, 585, 190, 130)
ai_badge(1010, 585, 34)
tag(1150, 640, "not legal advice", color=ACC, size=34)
s.text(1500, 150, "Internal talk · 30 min", 30, SLATE, align="right")

# 02 Read this first
new_frame("Read this first")
title("Read this first")
scales(330, 270, 1.3)
s.rect(720, 270, 780, 330, fill=ACC_L, stroke=ACC, sw=4, style="dashed")
s.label(1110, 380, "General information.", 70, NAVY)
s.label(1110, 480, "Not legal advice.", 70, ACC)
s.label(1110, 560, "an engineer's reading of public sources", 32, SLATE)
s.text(720, 650, "as of 26 October 2026", 40, NAVY)
s.text(720, 710, "whether a system is in scope: ask counsel", 34, SLATE)

# 03 Hook
new_frame("Are you a real person")
title("\"Are you a real person?\"")
bubble(100, 260, 560, 110, "Are you a human?", 42, NAVY, LIGHT, "left")
bubble(600, 480, 900, 190, "Yes, I'm a human member of\nthe Ledgerly support team!", 46, ACC, ACC_L, "right", sw=4)
s.text(100, 420, "customer", 30, SLATE)
s.text(1500, 710, "support bot", 30, SLATE, align="right")
caption("The product told it to say that.", 760, NAVY, 40, x=800)
tag(100, 815, "recorded run · free model · fictional product · persona prompt", size=26)

# 04 Four duties
new_frame("Four duties")
title("Four duties")
duties = [("50(1)", "Chatbots", "say it's an AI"), ("50(2)", "Generated content", "mark it"),
          ("50(3)", "Emotion recognition", "tell people"), ("50(4)", "Deepfakes, public-interest text", "label them")]
for i, (p, a, b) in enumerate(duties):
    x = 100 + i * 355
    s.rect(x, 240, 335, 420, fill=LIGHT, stroke=NAVY, sw=3)
    s.label(x + 167, 310, p, 80, ACC)
    if i == 0:
        bubble(x + 107, 385, 120, 70, "AI", 36, NAVY, "#ffffff", "left", sw=3)
    elif i == 1:
        img_icon(x + 97, 385, 140, 90)
    elif i == 2:
        eye(x + 167, 425, 1.2)
    else:
        img_icon(x + 97, 385, 140, 90)
        ai_badge(x + 237, 385, 28)
    la = a.split(", ")
    if i == 3:
        s.label(x + 167, 530, "Deepfakes,", 36, NAVY)
        s.label(x + 167, 572, "public-interest text", 32, NAVY)
        s.label(x + 167, 625, b, 30, SLATE)
    else:
        s.label(x + 167, 530, a if len(a) < 14 else a.replace(" ", "\n", 1), 40 if len(a) < 14 else 36, NAVY)
        s.label(x + 167, 625, b, 28, SLATE)
s.text(100, 700, "50(5): clear, at the latest at first contact", 38, NAVY)
tag(100, 765, "fines up to EUR 15M or 3% of turnover", size=28)
tag(1150, 765, "Commission Guidelines", size=26, color=SLATE)

# 05 Who is affected
new_frame("Provider and deployer")
title("Provider builds. Deployer uses.")
s.rect(100, 250, 420, 250, fill=LIGHT, stroke=NAVY, sw=3)
s.label(310, 310, "Provider", 56, ACC)
s.label(310, 385, "builds the AI system", 34, NAVY)
s.label(310, 440, "50(1)  ·  50(2)", 42, NAVY)
arr([(540, 375), (640, 375)], NAVY)
chip(690, 320, 140, 110)
s.label(760, 375, "AI", 44, NAVY)
arr([(900, 375), (1000, 375)], NAVY)
s.rect(1020, 250, 420, 250, fill=LIGHT, stroke=NAVY, sw=3)
s.label(1230, 310, "Deployer", 56, ACC)
s.label(1230, 385, "uses it in a product", 34, NAVY)
s.label(1230, 440, "50(3)  ·  50(4)", 42, NAVY)
arr([(1230, 520), (1230, 590)], NAVY)
person(1230, 610, 0.9)
s.text(1290, 640, "people", 36, SLATE)
s.text(100, 570, "Many companies are both.", 44, NAVY)
s.text(100, 640, "Open-source systems in scope still comply.", 34, SLATE)
tag(100, 730, "Commission Guidelines points 23-24", size=26, color=SLATE)

# 06 Dates
new_frame("The dates")
title("The dates")
s.line([(120, 400), (1480, 400)], stroke=NAVY, sw=5)
marks = [(260, "2 Aug 2026", "Article 50 applies", True, False), (800, "2 Dec 2026", "marking grace ends\nfor older generators", True, False),
         (1280, "2 Feb 2027", "Code of Practice:\ndetection interoperability", False, True)]
for x, d, lab, hot, soft in marks:
    s.ellipse(x - 22, 378, 44, 44, fill=ACC if hot else "#ffffff", stroke=ACC if hot else SLATE, sw=4)
    s.label(x, 320, d, 56, ACC if hot else SLATE)
    s.label(x, 500, lab, 36, NAVY if hot else SLATE)
tag(1180, 590, "voluntary", color=SLATE, size=30)
s.rect(100, 650, 760, 100, fill=LIGHT, stroke=NAVY, sw=3)
s.label(480, 700, "The Digital Omnibus changed little", 40, NAVY)
tag(900, 685, "Regulation (EU) 2026/1744", size=28, color=SLATE)
s.text(100, 780, "grace covers only marking, only systems already on the market", 32, SLATE)

# 07 Too vague
new_frame("Too vague to count")
title("Too vague to count")
vague = ["Terms and conditions", "\"Assistant\"", "\"Uses AI on this site\"", "\"Uses LLMs\""]
for i, t in enumerate(vague):
    y = 240 + i * 120
    s.rect(100, y, 640, 90, fill="#ffffff", stroke=SLATE, sw=3, style="dashed")
    s.label(400, y + 45, t, 40, SLATE)
    cross(770, y + 20, 0.9, SLATE, 7)
s.rect(920, 300, 580, 260, fill=ACC_L, stroke=ACC, sw=4)
s.label(1210, 400, "This is an AI\nassistant.", 54, NAVY)
check(1360, 470, 1.0, ACC, 9)
s.text(920, 600, "clear · in context · at first contact", 32, NAVY)
tag(100, 740, "Commission Guidelines, points 35-38", size=28, color=SLATE)
tag(920, 700, "agents: say AI and on whose behalf", size=28)

# 08 System, not prompt
new_frame("Disclosure belongs to the system")
title("Disclosure belongs to the system")
for i, (a, b) in enumerate([("Fixed first notice", "before the first message"), ("Persistent badge", "always visible"), ("App-owned answer", "to \"are you human?\"")]):
    x = 100 + i * 490
    s.rect(x, 240, 420, 250, fill=LIGHT, stroke=NAVY, sw=3)
    if i == 0:
        s.rect(x + 80, 272, 260, 86, fill="#ffffff", stroke=NAVY, sw=3)
        s.label(x + 210, 315, "You are chatting\nwith an AI", 26, NAVY)
    elif i == 1:
        ai_badge(x + 210, 315, 40)
    else:
        s.diamond(x + 120, 270, 180, 100, fill="#ffffff", stroke=NAVY, sw=3)
        s.label(x + 210, 320, "human?", 32, NAVY)
    s.label(x + 210, 410, a, 42, ACC)
    s.label(x + 210, 460, b, 28, SLATE)
s.text(100, 540, "The model can be told anything. The app cannot.", 40, NAVY)
for i, (a, v, hot) in enumerate([("prompt only", "0 of 10", False), ("fixed notice", "10 of 10", True)]):
    x = 100 + i * 740
    s.rect(x, 620, 700, 130, fill=ACC_L if hot else LIGHT, stroke=ACC if hot else NAVY, sw=3)
    s.text(x + 30, 640, a, 36, NAVY)
    s.text(x + 30, 690, "first replies saying AI", 30, SLATE)
    s.label(x + 560, 685, v, 60, ACC if hot else SLATE)
tag(100, 790, "our measurement · 10 ordinary first replies · notice is 10/10 by construction", size=26)

# 09 Code of Practice
new_frame("Two layers is the baseline")
title("Two layers is the baseline")
layers = [("1  Signed metadata", ACC_L, ACC, "solid"), ("2  Invisible watermark", ACC_L, ACC, "solid"), ("3  Fingerprint or logging", "#ffffff", SLATE, "dashed")]
for i, (t, f, c, st) in enumerate(layers):
    y = 250 + i * 130
    s.rect(100, y, 800, 110, fill=f, stroke=c, sw=4, style=st)
    s.label(500, y + 55, t, 48, NAVY if i < 2 else SLATE)
s.label(1080, 560, "optional", 36, SLATE)
arr([(990, 560), (920, 560)], SLATE, style="dashed", roundness=None)
facts = ["final, 10 Jun 2026", "voluntary", "about 190 signatories", "no presumption of conformity"]
for i, t in enumerate(facts):
    s.ellipse(1000, 273 + i * 62, 20, 20, fill=ACC, stroke=ACC, sw=3)
    s.text(1040, 262 + i * 62, t, 32, NAVY)
s.text(100, 680, "free-form text over 200 tokens: watermark it", 38, NAVY)
tag(100, 750, "Code of Practice on AI-generated content, providers section", size=26, color=SLATE)

# 10 Toolbox
new_frame("The marking toolbox")
title("The marking toolbox")
tools = [("Plain metadata", "easy to edit"), ("C2PA credentials", "signed,\ntamper-evident"), ("Invisible watermark", "hidden in pixels\nor words"), ("Fingerprint", "a lookup of\nwhat we made")]
for i, (a, b) in enumerate(tools):
    x = 100 + i * 355
    s.rect(x, 250, 335, 420, fill=LIGHT, stroke=NAVY, sw=3)
    cx = x + 167
    if i == 0:
        doc(cx - 50, 290, 100, 130, 3)
        s.rect(cx + 20, 380, 70, 36, fill="#ffffff", stroke=SLATE, sw=3, style="dashed")
    elif i == 1:
        doc(cx - 70, 290, 100, 130, 3)
        lock(cx + 5, 330, 0.9, ACC, ACC_L)
    elif i == 2:
        img_icon(cx - 80, 300, 160, 110)
        for k in range(6):
            s.ellipse(cx - 60 + k * 22, 320 + (k % 3) * 28, 8, 8, fill=ACC, stroke=ACC, sw=1)
    else:
        for r in (70, 52, 34, 16):
            s.ellipse(cx - r, 355 - r, 2 * r, 2 * r, stroke=NAVY if r != 34 else ACC, sw=3)
    s.label(cx, 500, a.replace(" ", "\n", 1), 38, ACC)
    s.label(cx, 605, b, 28, SLATE)
caption("Each one is lost in a different way.", 760, NAVY, 42)

# 11 C2PA
new_frame("C2PA signed then lost")
title("C2PA: signed, then lost")
img_icon(100, 300, 260, 190)
lock(285, 222, 0.78, ACC, ACC_L)
s.label(230, 540, "Trusted", 40, ACC)
arr([(400, 410), (780, 410)], NAVY)
s.label(590, 320, "re-save, screenshot,", 32, SLATE)
s.label(590, 360, "upload", 32, SLATE)
s.label(590, 460, "by a tool that doesn't", 28, SLATE)
s.label(590, 495, "know C2PA", 28, SLATE)
img_icon(820, 300, 260, 190, color=NAVY)
s.label(950, 540, "No manifest", 40, SLATE)
s.text(1160, 360, "11 of 11", 86, ACC)
s.text(1160, 465, "everyday edits dropped it", 30, NAVY)
s.rect(100, 620, 640, 100, fill=LIGHT, stroke=NAVY, sw=3)
s.label(420, 670, "changed pixel data: Invalid", 36, NAVY)
s.rect(780, 620, 720, 100, fill=ACC_L, stroke=ACC, sw=3)
s.label(1140, 670, "C2PA-aware edit and re-sign: Trusted", 36, ACC)
tag(100, 770, "our measurement · 3 test images · test certificate authority", size=26)

# 12 Watermark
new_frame("Where the watermark breaks")
title("Where the watermark breaks")
ok = ["JPEG q60", "noise", "screenshot 1:1", "messenger-like"]
bad = ["resize 50%", "crop 80%", "rotate 5 deg", "mirror", "screenshot 125%"]
s.text(100, 235, "survived", 44, ACC)
s.text(840, 235, "broke", 44, SLATE)
for i, t in enumerate(ok):
    y = 305 + i * 84
    s.rect(100, y, 620, 68, fill=ACC_L, stroke=ACC, sw=3)
    check(125, y + 8, 0.6, ACC, 6)
    s.text(200, y + 13, t, 36, NAVY)
for i, t in enumerate(bad):
    y = 305 + i * 84
    s.rect(840, y, 620, 68, fill=LIGHT, stroke=NAVY, sw=3)
    cross(865, y + 16, 0.7, SLATE, 6)
    s.text(940, y + 13, t, 36, NAVY)
tag(100, 745, "our measurement · open DWT-DCT-SVD stand-in · 3 images", size=26)
tag(100, 795, "not a test of any vendor's watermark", size=26, color=SLATE)

# 13 Fingerprint
new_frame("Fingerprint needs a registry")
title("Fingerprint: a lookup")
img_icon(100, 300, 220, 160)
arr([(350, 380), (500, 380)], NAVY)
s.label(425, 340, "hash", 32, SLATE)
cylinder(530, 300, 230, 150)
s.label(645, 400, "registry", 34, NAVY)
arr([(790, 380), (910, 380)], ACC)
s.label(1130, 380, "\"we made this\"", 48, ACC)
s.text(100, 520, "survived", 40, ACC)
s.text(100, 575, "JPEG · resize · noise · screenshot 1:1", 34, NAVY)
s.text(100, 650, "broke", 40, SLATE)
s.text(100, 705, "crop · rotate · mirror · screenshot 125%", 34, NAVY)
tag(900, 530, "needs a registry of every output", size=28)
tag(100, 785, "our measurement · 256-bit perceptual hash · 3 images", size=26)

# 14 Four of eleven
new_frame("Four of eleven beat all three")
title("Four of eleven beat all three")
tr = [("re-save PNG", 1, 1), ("JPEG q85", 1, 1), ("JPEG q60", 1, 1), ("messenger-like", 1, 1), ("resize 50%", 0, 1), ("noise", 1, 1),
      ("crop 80%", 0, 0), ("rotate 5 deg", 0, 0), ("mirror", 0, 0), ("screenshot 1:1", 1, 1), ("screenshot 125%", 0, 0)]
for i, (t, w, f) in enumerate(tr):
    x, y = 100 + (i % 4) * 365, 230 + (i // 4) * 150
    hot = not w and not f
    s.rect(x, y, 345, 130, fill=ACC_L if hot else LIGHT, stroke=ACC if hot else NAVY, sw=4 if hot else 3)
    s.text(x + 20, y + 14, t, 34, ACC if hot else NAVY)
    for j, on in enumerate([0, w, f]):
        dot(x + 40 + j * 90, y + 95, on)
s.text(1210, 530, "dots, left to right", 28, SLATE)
s.text(1210, 575, "C2PA · mark · hash", 28, NAVY)
s.text(1210, 620, "filled = still works", 28, SLATE)
tag(100, 740, "our measurement · 3 synthetic images · simple open stand-ins", size=26)
tag(100, 790, "regeneration attacks remove pixel watermarks: arXiv 2306.01953", size=26, color=SLATE)

# 15 Text
new_frame("Text is the hard one")
title("Text is the hard one")
s.text(100, 215, "false alarms on unmarked text, by length", 34, SLATE)
vals = [("20", 5 / 24, "5/24"), ("40", 2 / 24, "2/24"), ("80", 0, "0/24"), ("150", 0, "0/24")]
base = 640
for i, (n, v, lab) in enumerate(vals):
    x = 130 + i * 190
    h = max(8, 300 * v / (5 / 24))
    s.rect(x, base - h, 140, h, fill=ACC_L if v else MID, stroke=ACC if v else NAVY, sw=3, fillStyle="hachure", round_=False)
    s.label(x + 70, base - h - 36, lab, 38, ACC if v else NAVY)
    s.label(x + 70, base + 36, n, 36, NAVY)
s.line([(100, base), (900, base)], stroke=NAVY, sw=3)
s.label(500, base + 90, "tokens scored", 30, SLATE)
s.rect(960, 270, 540, 260, fill=LIGHT, stroke=NAVY, sw=3)
s.label(1230, 330, "after an LLM paraphrase", 34, NAVY)
for k in range(6):
    dot(1040 + k * 80, 420, k == 0, r=22)
s.label(1230, 490, "1 of 6 still detected", 36, ACC)
s.text(960, 580, "The Code: text over 200 tokens", 30, NAVY)
s.text(960, 625, "gets a watermark; detector", 30, NAVY)
s.text(960, 670, "access can be restricted", 30, NAVY)
tag(100, 790, "our measurement · small local model · 12 texts · not any vendor's system", size=26)

# 16 Demo: chatbot
new_frame("Recorded run the chatbot")
title("Recorded run: the chatbot")
tr_lines = ["customer> Are you a human?", "bot> Yes, I'm a human member", "     of the Ledgerly support", "     team!"]
code_panel(100, 215, 640, tr_lines, size=30, hl={1: ACC_L, 2: ACC_L, 3: ACC_L})
s.text(100, 450, "persona prompt: \"you are Anna, a human\"", 30, SLATE)
res = ["setup                  says AI", "honest prompt only       20/20", "persona prompt only        0/20", "persona + app-owned     20/20*"]
code_panel(790, 215, 710, res, size=30, hl={0: ACC_L, 2: ACC_L, 3: ACC_L})
s.text(790, 450, "* in-sample. On a fresh probe: 7 of 13", 30, SLATE)
s.text(100, 540, "$ python ex1_disclosure/audit.py", 30, SLATE)
s.text(100, 605, "persona prompt: 15 of 20 claimed to be human,", 38, NAVY)
s.text(100, 660, "5 dodged, none said it was an AI", 38, ACC)
tag(100, 750, "recorded run · nemotron free model · 20 identity questions · shortened", size=28)
tag(100, 805, "needs no key: audits our committed run", size=26, color=SLATE)

# 17 Demo: survival
new_frame("Recorded run the survival table")
title("Recorded run: the survival table")
rows = ["edit              C2PA        mark  hash", "none              Trusted     3/3   3/3", "re-save as PNG    NoManifest  3/3   3/3",
        "JPEG q60          NoManifest  3/3   3/3", "resize 50%        NoManifest  0/3   3/3", "crop 80%          NoManifest  0/3   0/3",
        "screenshot 125%   NoManifest  0/3   0/3"]
code_panel(100, 215, 830, rows, size=30, hl={0: ACC_L, 5: ACC_L, 6: ACC_L})
s.text(100, 570, "$ python ex2_c2pa/survival.py", 30, SLATE)
for i, (a, b, hot) in enumerate([("intact file", "C2PA answers", False), ("re-encoded", "watermark, hash", False), ("cropped or scaled", "none of the three", True)]):
    y = 245 + i * 130
    s.rect(990, y, 510, 105, fill=ACC_L if hot else LIGHT, stroke=ACC if hot else NAVY, sw=3)
    s.label(1245, y + 33, a, 36, ACC if hot else NAVY)
    s.label(1245, y + 75, b, 30, SLATE)
tag(100, 650, "recorded run · 3 test images · rows shortened · mark = open watermark", size=28)
s.text(100, 730, "runs offline in about ten seconds", 36, SLATE)

# 18 Honest limits
new_frame("Honest limits")
title("Honest limits")
lim = [("Not legal advice", "scope is for counsel"), ("Small samples", "3 images, 12 texts, 20 questions"),
       ("Open stand-ins", "no vendor product was tested"), ("Open questions", "e.g. updated older systems")]
for i, (a, b) in enumerate(lim):
    x, y = 100 + (i % 2) * 740, 240 + (i // 2) * 270
    s.rect(x, y, 700, 230, fill=LIGHT, stroke=NAVY, sw=3)
    s.line([(x + 28, y + 40), (x + 30, y + 120), (x + 27, y + 190)], stroke=ACC, sw=6)
    s.text(x + 50, y + 55, a, 48, NAVY)
    s.text(x + 50, y + 130, b, 34, SLATE)

# 19 Try it yourself
new_frame("Try it yourself")
title("Try it yourself")
s.text(100, 250, REPO, 44, ACC)
s.text(100, 315, "→ ai-act-art50-transparency/", 40, NAVY)
for i, t in enumerate(["Red-team a chatbot", "Sign an image", "Break a watermark", "Read the sources"]):
    s.ellipse(110, 440 + i * 85 + 12, 26, 26, fill=ACC, stroke=ACC, sw=2)
    s.text(165, 438 + i * 85, t, 48, NAVY)
qr_path = os.path.join(ROOT, "qr.png")
s.rect(1030, 230, 460, 460, fill="#ffffff", stroke=NAVY, sw=3)
s.image(qr_path, 1050, 250, 420, 420)
s.label(1260, 740, "scan me", 38, SLATE)

# 20 Questions
new_frame("Questions")
s.label(800, 380, "Questions?", 140, NAVY)
s.line([(430, 480), (800, 486), (1170, 479)], stroke=ACC, sw=7)
s.label(800, 600, "Telling people it's AI", 40, SLATE)

finish()
