#!/usr/bin/env python3
"""AI-assisted legacy modernization: 20 Excalidraw frames (1600x900), same hand-drawn serious style
as system-one-models/presentation/serious (Excalifont, roughness 1, navy + one orange accent, no characters).
   python3 build_deck.py     -> ../presentation.excalidraw   (needs ../qr.png from make_qr.py)"""
from kit import *

TOPIC = "legacy-modernization"


def tag_r(t, y, size=26, color=ACC):
    w, _ = measure(t, size)
    tag(1500 - (w + 36), y, t, color, size)


def cyl(x, y, w=110, h=100, color=NAVY, fill=LIGHT):
    """database cylinder"""
    s.rect(x, y + 14, w, h - 14, fill=fill, stroke=color, sw=3, round_=False)
    s.ellipse(x, y, w, 30, fill=fill, stroke=color, sw=3)
    s.rect(x + 4, y + h - 8, w - 8, 18, fill="#ffffff", stroke="#ffffff", sw=1, rough=0, round_=False)
    s.line([(x, y + h), (x + w * 0.5, y + h + 12), (x + w, y + h)], stroke=color, sw=3)


def key(x, y, k=1.0, color=ACC):
    s.ellipse(x, y, 40 * k, 40 * k, stroke=color, sw=4)
    s.line([(x + 40 * k, y + 20 * k), (x + 110 * k, y + 20 * k)], stroke=color, sw=4)
    s.line([(x + 90 * k, y + 20 * k), (x + 90 * k, y + 40 * k)], stroke=color, sw=4)
    s.line([(x + 106 * k, y + 20 * k), (x + 106 * k, y + 36 * k)], stroke=color, sw=4)


def old_computer(x, y, k=1.0, color=NAVY):
    s.rect(x, y, 150 * k, 190 * k, fill=LIGHT, stroke=color, sw=3, round_=False)
    for i in range(3):
        s.line([(x + 20 * k, y + 28 * k + i * 22 * k), (x + 130 * k, y + 28 * k + i * 22 * k)], stroke=SLATE, sw=3)
    s.rect(x + 20 * k, y + 110 * k, 110 * k, 60 * k, fill="#ffffff", stroke=color, sw=3)
    s.ellipse(x + 100 * k, y + 130 * k, 14 * k, 14 * k, fill=ACC_L, stroke=ACC, sw=2)


# =====================================================================
# 01 Title
new_frame("Title")
s.text(100, 235, "AI and legacy code", 120, NAVY)
s.line([(104, 395), (700, 399), (1060, 394)], stroke=ACC, sw=7)
s.text(104, 425, "Translating is easy. Proving it is the job.", 52, SLATE)
doc(130, 630, 100, 130, 4)
s.text(110, 775, "COBOL", 32, SLATE)
arr([(260, 695), (410, 695)], NAVY)
box(430, 645, 200, 100, "AI", 56, fill=ACC_L, stroke=ACC, color=ACC)
arr([(650, 695), (800, 695)], ACC)
doc(830, 630, 100, 130, 4, color=ACC)
s.text(815, 775, "new code", 32, SLATE)
arr([(960, 695), (1100, 695)], SLATE, style="dashed")
s.text(1130, 650, "same\nbehaviour?", 44, ACC)
s.text(1500, 150, "Internal talk · 30 min", 30, SLATE, align="right")

# 02 Translation is getting cheap
new_frame("Translation is getting cheap")
title("Translation is getting cheap")
s.rect(100, 260, 560, 360, fill=LIGHT, stroke=NAVY, sw=3)
s.label(380, 320, "Before", 44, SLATE)
s.label(380, 440, "priced per line\nof code", 48, NAVY)
cross(350, 530, 1.0, SLATE, 7)
arr([(690, 440), (850, 440)], ACC, sw=5)
s.rect(880, 260, 620, 360, fill=ACC_L, stroke=ACC, sw=4)
s.label(1190, 320, "March 2026", 44, ACC)
s.label(1190, 440, "AWS Transform:\ncode transformation\nat no cost", 44, NAVY)
caption("So what are people paying for?", 760, ACC, 52)
tag_r("AWS announcement, 17 Mar 2026", 178)

# 03 A program is not the system
new_frame("A program is not the system")
title("A program is not the system")
s.text(100, 165, "one interest job from AWS CardDemo, drawn by our dependency graph", 32, SLATE)
box(100, 420, 230, 100, "JCL job", 40)
arr([(340, 470), (470, 470)], NAVY)
box(480, 400, 280, 140, "CBACT04C", 46, fill=ACC_L, stroke=ACC, color=ACC)
for i, (t, yy) in enumerate([("reads 3 files", 270), ("updates accounts", 400), ("writes transactions", 530)]):
    arr([(770, 440 + i * 30), (950, yy + 50)], SLATE, sw=3)
    s.rect(960, yy, 540, 100, fill=LIGHT, stroke=NAVY, sw=3)
    s.label(1230, yy + 50, t, 38, NAVY)
arr([(620, 550), (620, 640)], SLATE, sw=3)
box(480, 650, 280, 80, "5 copybooks", 34)
s.label(300, 760, "+ an abend service", 32, SLATE)
s.text(1500, 790, "whole tree: 157 nodes, 385 edges", 32, ACC, align="right")

# 04 Few know the dependencies
new_frame("Few know the dependencies")
title("Few know the dependencies")
for i in range(100):
    cx, cy = 130 + (i % 10) * 62, 250 + (i // 10) * 52
    hot = i < 9
    s.ellipse(cx, cy, 34, 34, fill=ACC if hot else MID, stroke=ACC if hot else NAVY, sw=2, fillStyle="solid")
s.text(850, 300, "9 %", 200, ACC)
s.text(860, 520, "fully understand their\napplication dependencies", 44, NAVY)
tag(860, 700, "survey of 2,000 IT leaders, Oct 2026", size=28)
s.text(860, 760, "Kyndryl, a services vendor", 30, SLATE)

# 05 Two schools
new_frame("Two schools")
title("Two schools")
s.rect(100, 230, 650, 280, fill=LIGHT, stroke=NAVY, sw=3)
s.label(425, 290, "Rule-based converters", 44, NAVY)
s.label(425, 380, "provable,\nbut reads like COBOL in Java", 34, SLATE)
s.rect(850, 230, 650, 280, fill=ACC_L, stroke=ACC, sw=3)
s.label(1175, 290, "LLM pipelines", 44, ACC)
s.label(1175, 380, "idiomatic code,\nbut it must be proven", 34, SLATE)
arr([(425, 530), (700, 640)], NAVY)
arr([(1175, 530), (900, 640)], ACC)
box(430, 650, 740, 110, "An oracle: the running system", 40, fill="#ffffff", stroke=ACC, color=ACC, sw=4)
s.text(1200, 690, "everyone is\nconverging here", 30, SLATE)

# 06 Read vs write
new_frame("Models read COBOL better than they write it")
title("Better readers than writers")
s.text(100, 165, "tests passed by GPT-4o on small, single-file tasks", 34, SLATE)
s.rect(300, 640 - 85.3 * 4, 260, 85.3 * 4, fill=ACC_L, stroke=ACC, sw=3, fillStyle="hachure", round_=False)
s.rect(900, 640 - 2.2 * 4, 260, 2.2 * 4 + 2, fill=MID, stroke=NAVY, sw=3, fillStyle="hachure", round_=False)
s.line([(240, 642), (1260, 642)], stroke=NAVY, sw=4)
s.label(430, 640 - 85.3 * 4 - 40, "85 %", 64, ACC)
s.label(1030, 640 - 2.2 * 4 - 45, "2 %", 64, NAVY)
s.label(430, 700, "COBOL → Java", 44, NAVY)
s.label(1030, 700, "Java → COBOL", 44, NAVY)
tag_r("COBOL-Coder paper, arXiv 2604.03986", 785)
s.text(100, 790, "no copybooks, no job control, no other programs", 32, SLATE)

# 07 Below the business rules
new_frame("Where it breaks: below the business rules")
title("Where it breaks")
s.text(100, 165, "below the business rules", 40, ACC)
tiles = [("How a minus\nsign is stored", "-5"), ("Rounding or\ntruncating", "12.49"), ("What a keyed\nfile really does", None), ("Codes that\nschedulers watch", "999")]
for i, (t, g) in enumerate(tiles):
    x = 100 + i * 360
    s.rect(x, 260, 330, 470, fill=LIGHT, stroke=NAVY, sw=3)
    if g:
        s.label(x + 165, 400, g, 90 if len(g) < 4 else 78, ACC)
    else:
        key(x + 105, 375, 1.0, ACC)
    s.label(x + 165, 600, t, 38, NAVY)

# 08 Truncation, not rounding
new_frame("Truncation, not rounding")
title("One missing word")
code = ["COMPUTE WS-MONTHLY-INT =", "  (TRAN-CAT-BAL * DIS-INT-RATE)", "  / 1200", "", "no ROUNDED => truncate"]
code_panel(100, 235, 760, code, size=32, hl={4: ACC_L})
s.text(100, 520, "the old job cuts off the extra digits", 38, SLATE)
s.text(100, 585, "it never rounds", 38, ACC)
s.rect(920, 235, 580, 160, fill="#ffffff", stroke=NAVY, sw=3)
s.label(1210, 290, "old COBOL", 36, SLATE)
s.label(1210, 350, "12.49", 72, NAVY)
s.rect(920, 425, 580, 160, fill=ACC_L, stroke=ACC, sw=3)
s.label(1210, 480, "model, from COBOL only", 34, SLATE)
s.label(1210, 540, "12.50", 72, ACC)
caption("One cent, on every transaction, every month", 800, NAVY, 44)
tag_r("our measurement", 178)

# 09 The forgotten last account
new_frame("The forgotten last account")
title("The forgotten last account")
for i in range(5):
    y = 235 + i * 85
    last = i == 4
    s.rect(100, y, 620, 66, fill=ACC_L if last else LIGHT, stroke=ACC if last else NAVY, sw=3)
    s.text(130, y + 12, f"account {i + 1}", 34, ACC if last else NAVY)
    s.text(380, y + 14, "balance updated", 28, SLATE)
    if last:
        cross(660 - 5, y + 8, 0.9, ACC, 6)
    else:
        check(668, y + 6, 0.6, NAVY, 5)
s.text(100, 680, "the last one never gets its balance updated", 36, ACC)
s.text(100, 735, "found by running the job, not by reading it", 32, SLATE)
s.rect(800, 235, 700, 190, fill=LIGHT, stroke=NAVY, sw=3)
s.label(1150, 290, "Fix the bug?", 46, NAVY)
s.label(1150, 365, "9 of 25 scenarios still match", 36, ACC)
s.rect(800, 470, 700, 190, fill=ACC_L, stroke=ACC, sw=3)
s.label(1150, 530, "Copy it or fix it?", 46, ACC)
s.label(1150, 605, "a business decision", 40, NAVY)
tag_r("our measurement", 178)

# 10 The diamond
new_frame("The diamond")
title("The diamond")
box(100, 440, 230, 110, "Same input", 40)
arr([(340, 470), (520, 340)], NAVY)
arr([(340, 520), (520, 600)], ACC)
box(530, 270, 400, 140, "Running\nold system", 40)
box(530, 540, 400, 140, "New code", 44, fill=ACC_L, stroke=ACC, color=ACC)
arr([(940, 340), (1110, 450)], NAVY)
arr([(940, 610), (1110, 520)], ACC)
s.diamond(1120, 400, 250, 190, fill="#ffffff", stroke=ACC, sw=4)
s.label(1245, 495, "Compare", 38, ACC)
arr([(1380, 495), (1450, 495)], ACC)
check(1440, 530, 0.8, ACC, 7)
s.text(1430, 440, "same", 30, SLATE)
caption("The running system is the spec", 800, ACC, 48)
tag_r("our harness: 25 scenarios, 0.5 s", 178)

# 11 Demo: reference
new_frame("Live demo: the reference")
title("Live demo: the reference")
lines = ["$ python ex4_equivalence/diamond.py", "", "carddemo-sample-data      ok   EQUIVALENT", "edge-amounts              ok   EQUIVALENT",
         "...", "abend-unknown-account    abend 999   EQUIVALENT", "", "25/25 scenarios equivalent in 0.5s"]
code_panel(100, 215, 1000, lines, size=30, hl={7: ACC_L})
s.text(1150, 300, "the real COBOL\nruns on a laptop", 40, NAVY)
s.text(1150, 440, "GnuCOBOL,\nunchanged source", 34, SLATE)
tag(100, 745, "shortened · recorded in a clean-clone run", size=28)
s.text(100, 810, "workshop/ex4_equivalence/diamond.py", 30, SLATE)

# 12 Demo: a wrong candidate
new_frame("Live demo: a wrong candidate")
title("Live demo: a wrong candidate")
lines = ["$ python ex4_equivalence/diamond.py \\", "    --impl out/candidate_cobol.py", "", "tx#1  amount  legacy=12.49  modern=12.50", "tx#5  amount  legacy=0.99   modern=1.00",
         "acct 9  curr_bal  legacy=560.00", "                  modern=12500560.00"]
code_panel(100, 215, 1000, lines, size=30, hl={3: ACC_L, 4: ACC_L, 6: ACC_L})
s.text(1150, 300, "written by a free\nmodel from COBOL only", 36, NAVY)
s.text(1150, 440, "it rounded, and it\nposted the last account", 34, ACC)
tag(100, 700, "simplified from a recorded run", size=28)
s.text(100, 770, "Looks like clean Python. Code review would miss it.", 38, SLATE)

# 13 Reading rules with a model
new_frame("Reading rules with a model")
title("Reading rules with a model")
s.text(100, 165, "how many of 15 hand-checked rules did the model find?", 34, SLATE)
x0, sc = 330, 1000
s.line([(x0, 420), (x0 + sc, 420)], stroke=NAVY, sw=4)
for v in (0, 0.5, 1.0):
    s.line([(x0 + v * sc, 405), (x0 + v * sc, 435)], stroke=NAVY, sw=3)
    s.text(x0 + v * sc - (12 if v == 0 else 0), 445, f"{v:g}", 28, SLATE)
s.rect(x0 + 0.60 * sc, 360, 0.13 * sc, 60, fill=ACC_L, stroke=ACC, sw=3, fillStyle="hachure", round_=False)
s.ellipse(x0 + 0.87 * sc - 18, 366, 36, 36, fill=NAVY, stroke=NAVY, sw=2)
s.text(100, 330, "Nemotron", 34, NAVY); s.text(100, 372, "4 runs", 28, SLATE)
s.text(x0 + 0.60 * sc - 20, 290, "0.60–0.73", 36, ACC)
s.label(x0 + 0.87 * sc, 300, "0.87", 36, NAVY)
s.text(x0 + 0.87 * sc - 40, 510, "Laguna, 1 run", 28, SLATE)
s.text(100, 590, "Always missed", 44, ACC)
for i, t in enumerate(["truncation, not rounding", "the last account is never posted"]):
    cross(100, 665 + i * 70, 0.6, ACC, 6)
    s.text(160, 662 + i * 70, t, 40, NAVY)
tag_r("our measurement · free models", 178)

# 14 Cited and still wrong
new_frame("Cited, and still wrong")
title("Cited, and still wrong")
s.rect(100, 255, 1400, 200, fill=LIGHT, stroke=NAVY, sw=3)
s.text(135, 275, "Rule 17, lines 219–221", 34, SLATE)
s.text(135, 330, "“At end of file, the program updates the last\naccount’s interest.”", 40, NAVY)
for i, (t, ok) in enumerate([("right lines", True), ("right symbols", True), ("right meaning", False)]):
    x = 100 + i * 480
    s.rect(x, 520, 440, 150, fill=ACC_L if not ok else "#ffffff", stroke=ACC if not ok else NAVY, sw=3)
    if ok:
        check(x + 40, 565, 1.0, NAVY, 8)
    else:
        cross(x + 40, 565, 1.0, ACC, 8)
    s.text(x + 130, 570, t, 42, ACC if not ok else NAVY)
caption("That branch never runs", 775, ACC, 52)
s.text(100, 825, "A citation tells you where, not whether", 34, SLATE)
tag_r("our measurement", 178)

# 15 Three ways to generate
new_frame("Three ways to generate")
title("Three ways to generate")
s.text(100, 165, "scenarios that match the old system, out of 25", 34, SLATE)
groups = [("From verified\nrules", [25, 25, 25]), ("From the model’s\nown rules", [2, 1, 0]), ("From COBOL\nonly", [1, 3, 2])]
base, sc = 630, 12
for gi, (gl, vals) in enumerate(groups):
    gx = 150 + gi * 470
    for vi, v in enumerate(vals):
        bx = gx + vi * 110
        hot = gi == 0
        s.rect(bx, base - max(v * sc, 6), 90, max(v * sc, 6), fill=ACC_L if hot else MID, stroke=ACC if hot else NAVY, sw=3, fillStyle="hachure", round_=False)
        s.label(bx + 45, base - max(v * sc, 6) - 28, str(v), 40, ACC if hot else NAVY)
    s.label(gx + 160, base + 65, gl, 34, NAVY)
s.line([(110, base + 2), (1500, base + 2)], stroke=NAVY, sw=4)
s.text(100, 785, "A later clean re-run of the first group scored 2 of 25: one wrong character.", 30, SLATE)
tag_r("our measurement · free models", 178)

# 16 Who sells what
new_frame("Who sells what")
title("Who sells what")
vend = [("AWS Transform", "code conversion at no cost"), ("IBM Bob for Z", "can run on your own servers"), ("Google MAT + Dual Run", "run both, compare outputs"),
        ("Microsoft agents", "open source, no built-in checks"), ("Mechanical Orchard", "verifies on real data flows")]
for i, (a, b) in enumerate(vend):
    x, y = (100 + i * 490, 240) if i < 3 else (345 + (i - 3) * 490, 520)
    s.rect(x, y, 450, 230, fill=ACC_L if i in (2, 4) else LIGHT, stroke=ACC if i in (2, 4) else NAVY, sw=3)
    s.label(x + 225, y + 85, a, 42 if len(a) < 20 else 34, ACC if i in (2, 4) else NAVY)
    s.label(x + 225, y + 160, b, 26, SLATE)
tag_r("from their docs · we did not run them", 178)
s.text(100, 800, "highlighted: the ones built around checking", 30, SLATE)

# 17 Honest limits
new_frame("Honest limits")
title("Honest limits")
lim = [("One batch program", "no online screens, no packed decimal"), ("Free models", "few runs, a small sample"),
       ("Vendor tools not run", "we read their documentation"), ("Vendor numbers", "are claims, prices mostly unpublished")]
for i, (a, b) in enumerate(lim):
    x, y = 100 + (i % 2) * 740, 240 + (i // 2) * 270
    s.rect(x, y, 700, 230, fill=LIGHT, stroke=NAVY, sw=3)
    s.line([(x + 28, y + 40), (x + 30, y + 120), (x + 27, y + 190)], stroke=ACC, sw=6)
    s.text(x + 50, y + 55, a, 50, NAVY)
    s.text(x + 50, y + 130, b, 32, SLATE)

# 18 Takeaways
new_frame("Three takeaways")
title("Three takeaways")
for i, t in enumerate(["The running system\nis the spec", "Trust the harness,\nnot the model", "Models draft,\ntests judge"]):
    x = 100 + i * 490
    s.ellipse(x + 150, 250, 120, 120, fill=ACC_L, stroke=ACC, sw=4)
    s.label(x + 210, 312, str(i + 1), 72, ACC)
    s.rect(x, 420, 420, 260, fill=LIGHT, stroke=NAVY, sw=3)
    s.label(x + 210, 550, t, 38, NAVY)

# 19 Try it yourself
new_frame("Try it yourself")
title("Try it yourself")
s.text(100, 250, REPO, 44, ACC)
s.text(100, 315, "→ " + TOPIC + "/", 40, NAVY)
for i, t in enumerate(["Run the workshop", "Try the diamond", "Compare the vendors", "Read the sources"]):
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
s.label(800, 600, "AI and legacy code", 40, SLATE)

out = s.to_json()
probs = validate(out)
if probs:
    print("PROBLEMS:", *probs[:20], sep="\n"); sys.exit(1)
json.dump(out, open(os.path.join(ROOT, "presentation.excalidraw"), "w"))
print("presentation.excalidraw:", count[0], "frames,", len(out["elements"]), "elements")
