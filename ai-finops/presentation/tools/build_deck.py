#!/usr/bin/env python3
"""Serious Excalidraw deck: "Taming the AI bill" (AI cost control / FinOps for AI), 20 frames (1600x900),
same look as system-one-models/presentation/serious (Excalifont, roughness 1, navy + one orange accent, no characters).
   python3 make_qr.py && python3 build_deck.py     -> ../presentation.excalidraw
Numbers on slides come from ../../research.md and ../../workshop/ (results/, PARTICIPANTS.md)."""
import os
from kit import *

# =====================================================================
# 01 Title
new_frame("Title")
s.text(100, 235, "Taming the AI bill", 118, NAVY)
s.line([(104, 395), (700, 399), (1050, 394)], stroke=ACC, sw=7)
s.text(104, 425, "Cost control for AI features", 52, SLATE)
coin(180, 690, 62, "$", ACC, ACC_L)
arr([(280, 690), (440, 690)], NAVY)
funnel(470, 625, 190, 130)
arr([(700, 690), (860, 690)], ACC)
coin(930, 700, 36, "$", ACC, ACC_L)
s.text(1500, 150, "Internal talk · 30 min", 30, SLATE, align="right")

# 02 Cheaper tokens, bigger bills
new_frame("Cheaper tokens, bigger bills")
title("Cheaper tokens, bigger bills")
arr([(160, 700), (160, 250)], NAVY, sw=3)
arr([(160, 700), (920, 700)], NAVY, sw=3)
s.text(940, 680, "time", 34, SLATE)
s.line([(190, 330), (380, 440), (600, 540), (880, 610)], stroke=NAVY, sw=6)
s.line([(190, 620), (380, 560), (600, 440), (880, 300)], stroke=ACC, sw=6)
s.text(210, 262, "price of a fixed capability", 34, NAVY)
s.text(540, 330, "total bill", 40, ACC)
tag(990, 580, "Epoch AI: ~13× cheaper a year", color=NAVY, size=28)
tag(990, 290, "Gartner forecast", size=28)
tag(990, 440, "schematic sketch, not data", color=SLATE, size=28)
caption("Unit price falls. Spend rises.", 800, SLATE, 42)

# 03 Every step re-sends everything
new_frame("Every step re-sends everything")
title("Every step re-sends everything")
blocks = ["instructions", "tools", "history", "results"]
for c in range(3):
    x = 100 + c * 330
    n = 2 + c
    s.label(x + 130, 270, f"step {c + 1}", 36, SLATE)
    for i in range(n):
        y = 690 - (i + 1) * 80
        last = i == n - 1 and c > 0
        s.rect(x, y, 260, 70, fill=ACC_L if last else LIGHT, stroke=ACC if last else NAVY, sw=3)
        s.label(x + 130, y + 35, blocks[i], 32, ACC if last else NAVY)
arr([(1090, 450), (1170, 450)], SLATE, sw=3)
s.rect(1190, 330, 310, 120, fill=LIGHT, stroke=NAVY, sw=3)
s.label(1345, 390, "input  1×", 44, NAVY)
s.rect(1190, 480, 310, 120, fill=ACC_L, stroke=ACC, sw=3)
s.label(1345, 540, "output  5×", 44, ACC)
tag(1190, 630, "flagship price cards", size=26)
caption("cost grows with steps × context", 800, NAVY, 40)

# 04 Price multipliers
new_frame("Easy-to-miss multipliers")
title("Easy-to-miss multipliers")
cards = [("×2–5", "Long prompts", "above a size tier"), ("×2–6", "Fast tier", "pay for speed"),
         ("+10%", "Data region", "residency pricing"), ("×2", "Promo ends", "one model, 1 Dec")]
for i, (big, a, b) in enumerate(cards):
    x = 100 + i * 355
    s.rect(x, 250, 335, 400, fill=LIGHT, stroke=NAVY, sw=3)
    s.label(x + 167, 360, big, 100, ACC)
    s.label(x + 167, 500, a, 44, NAVY)
    s.label(x + 167, 565, b, 32, SLATE)
tag(100, 700, "as read on 19 Oct 2026 · check before quoting", size=28)
s.text(1500, 705, "Batch and Flex tiers: −50%", 34, NAVY, align="right")

# 05 Cost per task
new_frame("Cost per task, not per token")
title("Cost per task, not per token")
for i, (a, b, ex, x) in enumerate([("$ per task", "", "$0.0125", 100), ("$ per successful task", "÷ pass rate", "$0.0143", 570), ("$ per month", "× volume", "$1,250", 1040)]):
    s.rect(x, 300, 400, 300, fill=ACC_L if i == 1 else LIGHT, stroke=ACC if i == 1 else NAVY, sw=3)
    s.label(x + 200, 365, a, 32 if i == 1 else 40, ACC if i == 1 else NAVY)
    s.label(x + 200, 480, ex, 72, NAVY)
    if b:
        s.label(x + 200, 555, b, 32, SLATE)
arr([(510, 450), (560, 450)], SLATE, sw=3)
arr([(980, 450), (1030, 450)], SLATE, sw=3)
s.text(100, 640, "example: 14 of 16 tickets pass, 100k tickets a month", 32, SLATE)
tag(100, 710, "our measurement · frontier price card", size=28)
caption("a cheap wrong answer is not cheap", 810, NAVY, 38)

# 06 Three verbs
new_frame("Measure allocate limit")
title("FinOps for AI in three verbs")
for i, (a, b) in enumerate([("Measure", "per use case"), ("Allocate", "per team and feature"), ("Limit", "budgets and alerts")]):
    x = 100 + i * 490
    s.rect(x, 250, 420, 360, fill=LIGHT, stroke=NAVY, sw=3)
    if i == 0:
        magnifier(x + 150, 290, 1.4)
    elif i == 1:
        s.rect(x + 130, 300, 160, 100, fill="#ffffff", stroke=NAVY, sw=3)
        s.label(x + 210, 350, "team", 40, ACC)
    else:
        gauge(x + 70, 340, 280, 0.65, 0.8)
    s.label(x + 210, 470, a, 60, ACC)
    s.label(x + 210, 545, b, 34, SLATE)
s.text(100, 680, "98%", 90, ACC)
s.text(380, 695, "of teams now manage AI spend", 40, NAVY)
s.text(380, 750, "31% two years ago · State of FinOps 2026", 30, SLATE)

# 07 Our test
new_frame("Our test")
title("Our test bench")
doc(110, 300, 100, 130, 4)
s.label(160, 465, "16 tickets", 36, NAVY)
doc(110, 540, 100, 130, 3)
s.label(160, 705, "knowledge base", 32, NAVY)
arr([(240, 365), (420, 450)])
arr([(240, 600), (420, 500)])
box(440, 395, 260, 140, "Model", 54, fill=ACC_L, stroke=ACC, color=ACC)
arr([(720, 465), (880, 465)])
s.rect(900, 330, 400, 270, fill=LIGHT, stroke=NAVY, sw=3)
s.text(930, 350, "checks (code)", 36, NAVY)
for i, t in enumerate(["right facts?", "no invented numbers?"]):
    s.ellipse(935, 425 + i * 62, 28, 28, stroke=NAVY, sw=3)
    s.text(985, 419 + i * 62, t, 29, NAVY)
arr([(1320, 465), (1380, 465)], ACC)
s.label(1445, 420, "pass?", 44, ACC)
coin(1445, 510, 38, "$", ACC, ACC_L)
tag(900, 650, "free models, priced at list price", size=28)
caption("same tickets, one lever at a time", 800, SLATE, 40)

# 08 Say less, send less
new_frame("Say less send less")
title("Say less, send less")
base_y, hmax = 690, 340
for i, (lab, v, delta, ps) in enumerate([("baseline", 1.0, "", "14/16"), ("short answers", 0.74, "−26%", "15/16"), ("+ less context", 0.32, "−68%", "15/16")]):
    x = 140 + i * 400
    h = hmax * v
    hot = i > 0
    s.rect(x, base_y - h, 280, h, fill=ACC_L if hot else MID, stroke=ACC if hot else NAVY, sw=3, fillStyle="hachure", round_=False)
    s.label(x + 140, base_y - h - 42, delta if delta else "100%", 56, ACC if hot else NAVY)
    s.label(x + 140, base_y + 40, lab, 36, NAVY)
    s.label(x + 140, base_y + 95, ps + " pass", 32, SLATE)
s.line([(100, base_y), (1500, base_y)], stroke=NAVY, sw=3)
s.text(110, 190, "cost per ticket", 34, SLATE)
tag(1180, 175, "our measurement", size=26)

# 09 Smaller model
new_frame("Smaller model")
title("A smaller model")
for i, (lab, d, ok, hot) in enumerate([("big model", "100%", 14, False), ("small model", "−96%", 14, False), ("small + less context", "−98%", 9, True)]):
    x = 100 + i * 490
    s.rect(x, 240, 420, 470, fill=ACC_L if hot else LIGHT, stroke=ACC if hot else NAVY, sw=3)
    s.label(x + 210, 300, lab, 38, ACC if hot else NAVY)
    s.label(x + 210, 395, d, 84, ACC if hot else NAVY)
    s.label(x + 210, 470, "cost", 30, SLATE)
    for k in range(16):
        cx, cy = x + 62 + (k % 8) * 42, 540 + (k // 8) * 48
        good = k < ok
        s.ellipse(cx - 15, cy - 15, 30, 30, fill=ACC_L if good else "#ffffff", stroke=ACC if good else MID, sw=3)
    s.label(x + 210, 665, f"{ok}/16 pass", 36, ACC if hot else SLATE)
caption("levers interact: re-test after each one", 800, NAVY, 38)
tag(1180, 160, "our measurement", size=26)

# 10 Cascade
new_frame("A cascade needs a checker")
title("A cascade needs a checker")
doc(100, 270, 80, 105, 3)
s.text(95, 390, "ticket", 32, SLATE)
arr([(200, 322), (300, 322)])
box(320, 270, 240, 100, "Small model", 38, fill=ACC_L, stroke=ACC, color=ACC)
arr([(580, 320), (680, 320)])
s.diamond(700, 245, 250, 150, fill=LIGHT, stroke=NAVY, sw=3)
s.label(825, 320, "check", 40, NAVY)
arr([(970, 320), (1090, 320)], ACC)
s.label(1030, 285, "ok", 30, ACC)
s.rect(1110, 270, 290, 100, fill=LIGHT, stroke=NAVY, sw=3)
s.label(1255, 320, "answered", 38, NAVY)
arr([(825, 405), (825, 470), (1000, 470)], SLATE, style="dashed", roundness=None)
s.text(850, 420, "not ok", 30, SLATE)
box(1010, 430, 290, 90, "Big model", 38)
s.text(100, 450, "check: every $ amount", 32, NAVY)
s.text(100, 495, "must exist in the", 32, NAVY)
s.text(100, 540, "knowledge base", 32, NAVY)
for i, (a, b, ok) in enumerate([("self-reported confidence", "13/16", False), ("number check", "14/16 at −95%", True)]):
    x = 100 + i * 740
    s.rect(x, 640, 700, 130, fill=ACC_L if ok else LIGHT, stroke=ACC if ok else NAVY, sw=3)
    (check if ok else cross)(x + 30, 680, 1.0, ACC if ok else SLATE, 7)
    s.text(x + 120, 655, a, 36, NAVY)
    s.text(x + 120, 705, b, 40, ACC if ok else SLATE)
tag(1180, 160, "our measurement", size=26)

# 11 Prompt caching
new_frame("Prompt caching")
title("Prompt caching: keep the start stable")
for i, (lab, order, cached) in enumerate([("dynamic part first", ["time, id", "long instructions"], "0"), ("dynamic part last", ["long instructions", "time, id"], "6,288")]):
    x = 100 + i * 740
    hot = i == 1
    s.text(x, 230, lab, 42, ACC if hot else SLATE)
    y = 310
    for j, t in enumerate(order):
        h = 70 if t == "time, id" else 200
        dyn = t == "time, id"
        s.rect(x, y, 560, h, fill=ACC_L if (hot and not dyn) else (MID if dyn else LIGHT), stroke=ACC if (hot and not dyn) else NAVY, sw=3,
               fillStyle="hachure" if dyn else "solid")
        s.label(x + 280, y + h / 2, t, 36, NAVY)
        y += h + 14
    s.label(x + 280, 660, cached, 84, ACC if hot else NAVY)
    s.label(x + 280, 735, "cached tokens per request", 30, SLATE)
tag(100, 790, "our measurement · ~8k-token prompt · free endpoint", size=26)
s.text(1500, 795, "paid rules: reads ~0.1×, writes ~1.25×", 30, SLATE, align="right")

# 12 Semantic caching
new_frame("Similar is not the same")
title("Similar is not the same")
s.rect(100, 260, 560, 150, fill="#ffffff", stroke=NAVY, sw=3)
s.label(380, 335, "SAML SSO on the\nBusiness plan?", 38, NAVY)
s.rect(940, 260, 560, 150, fill="#ffffff", stroke=NAVY, sw=3)
s.label(1220, 335, "SAML SSO on the\nEnterprise plan?", 38, NAVY)
s.line([(690, 320), (910, 320)], stroke=ACC, sw=6)
s.line([(690, 350), (910, 350)], stroke=ACC, sw=6)
s.label(800, 230, "0.95 similar", 40, ACC)
arr([(380, 430), (700, 540)], SLATE)
arr([(1220, 430), (900, 540)], SLATE)
s.rect(560, 550, 480, 110, fill=ACC_L, stroke=ACC, sw=3)
s.label(800, 605, "same cached answer", 40, ACC)
cross(1070, 578, 0.9, ACC, 8)
s.text(1140, 580, "wrong for one", 34, ACC)
tag(100, 700, "our stress test · 24 pairs built to be tricky", size=28)
caption("a wrong answer is free and instant", 810, NAVY, 38)

# 13 Gateway
new_frame("One door for every call")
title("One door for every call")
box(100, 270, 300, 100, "support", 42)
box(100, 480, 300, 100, "growth", 42)
arr([(420, 320), (600, 380)])
arr([(420, 530), (600, 470)])
s.rect(620, 240, 330, 380, fill=ACC_L, stroke=ACC, sw=4)
s.label(785, 300, "Gateway", 52, ACC)
for i, t in enumerate(["budget", "allow-list", "who called"]):
    s.rect(660, 350 + i * 80, 250, 62, fill="#ffffff", stroke=ACC, sw=2)
    s.label(785, 381 + i * 80, t, 34, NAVY)
arr([(970, 360), (1140, 330)], NAVY)
arr([(970, 520), (1140, 520)], NAVY)
box(1160, 280, 300, 100, "large model", 36)
box(1160, 470, 300, 100, "small model", 36)
arr([(970, 440), (1140, 385)], ACC, style="dashed")
cross(1030, 392, 0.5, ACC, 6)
s.text(100, 660, "support: stopped at 112% of budget", 36, NAVY)
s.text(100, 715, "growth: large model refused", 36, NAVY)
tag(1100, 700, "our measurement", size=26)
caption("one request of overshoot is normal", 810, SLATE, 34)

# 14 Demo: the cost table
new_frame("Live demo: the cost table")
title("Live demo: the cost table")
rows = ["config          pass  $/task   vs base", "A_baseline      14/16 $0.01250     +0%", "B_concise       15/16 $0.00928    -26%",
        "D_trim          15/16 $0.00394    -68%", "F_small_full    14/16 $0.00046    -96%", "G_small_trim     9/16 $0.00019    -98%"]
code_panel(100, 215, 900, rows, size=30, hl={0: ACC_L, 5: ACC_L})
s.text(100, 520, "$ python ex2_levers/run_levers.py --rescore results/…", 28, SLATE)
arr([(1040, 420), (1130, 420)], ACC)
s.text(1150, 340, "cheaper", 44, NAVY)
s.text(1150, 395, "is not always", 44, NAVY)
s.text(1150, 450, "better", 44, ACC)
tag(100, 620, "saved run · shortened table · frontier price card", size=28)
s.text(100, 700, "needs no key: it re-scores our committed runs", 36, SLATE)

# 15 Demo: the $0 trap
new_frame("Live demo: the zero dollar trap")
title("Live demo: the $0 trap")
cfg = ["small:", "  model: openai/nvidia/…:free", "", "small-openrouter-prefix:", "  model: openrouter/nvidia/…:free"]
code_panel(100, 215, 760, cfg, size=28, hl={0: ACC_L, 3: ACC_L})
arr([(890, 330), (990, 330)], ACC)
res = ["small", "  cost logged: 2.8e-06", "", "small-openrouter-prefix", "  cost logged: 0.0"]
code_panel(1010, 215, 490, res, size=28, hl={0: ACC_L, 3: ACC_L, 4: ACC_L})
s.text(100, 520, "same model, same custom price", 36, SLATE)
s.text(100, 600, "18 in × $0.10/M  +  2 out × $0.50/M  =  $0.0000028", 40, NAVY)
s.text(100, 665, "check one request against a hand calculation", 36, ACC)
tag(100, 745, "saved run · LiteLLM v1.106.0 · free model, shadow prices", size=28)

# 16 Self-hosting
new_frame("When self-hosting pays")
title("When does self-hosting pay?")
s.rect(150, 400, 1300, 70, fill="#ffffff", stroke=NAVY, sw=3)
s.rect(153, 403, 1294 * 0.64, 64, fill=ACC_L, stroke=ACC, sw=2, fillStyle="hachure", round_=False)
for pct, lab, up, col in [(0.18, "beats a frontier price", False, NAVY), (0.64, "beats an open model via API", True, ACC)]:
    x = 150 + 1300 * pct
    s.line([(x, 370), (x, 500)], stroke=col, sw=5)
    s.label(x, 335, f"{round(pct * 100)}%", 52, col)
    s.label(x - (60 if not up else 0), 545, lab, 32, col)
x30 = 150 + 1300 * 0.30
s.arrow([(x30, 640), (x30, 505)], stroke=SLATE, sw=3, style="dashed", roundness=None)
s.label(x30, 680, "business hours only: ~30% ceiling", 32, SLATE)
s.text(150, 250, "average utilization of a rented GPU server", 36, SLATE)
tag(100, 760, "our arithmetic · throughput is an assumption", size=28)

# 17 Honest limits
new_frame("Honest limits")
title("Honest limits")
lim = [("16 tickets, one run", "1–2 tickets is noise"), ("Free models, list prices", "shadow cost, nothing charged"),
       ("Caching: partly simulated", "paid rules applied by math"), ("Survey numbers", "reported by their publishers")]
for i, (a, b) in enumerate(lim):
    x, y = 100 + (i % 2) * 740, 240 + (i // 2) * 270
    s.rect(x, y, 700, 230, fill=LIGHT, stroke=NAVY, sw=3)
    s.line([(x + 28, y + 40), (x + 30, y + 120), (x + 27, y + 190)], stroke=ACC, sw=6)
    s.text(x + 50, y + 55, a, 48, NAVY)
    s.text(x + 50, y + 130, b, 38, SLATE)

# 18 Takeaways
new_frame("Three takeaways")
title("Three takeaways")
for i, t in enumerate(["Count cost per\nsuccessful task", "One lever at a time,\nre-test quality", "One gateway door,\ncheck its numbers"]):
    x = 100 + i * 490
    s.ellipse(x + 150, 250, 120, 120, fill=ACC_L, stroke=ACC, sw=4)
    s.label(x + 210, 312, str(i + 1), 72, ACC)
    s.rect(x, 420, 420, 260, fill=LIGHT, stroke=NAVY, sw=3)
    s.label(x + 210, 550, t, 38, NAVY)

# 19 Try it yourself
new_frame("Try it yourself")
title("Try it yourself")
s.text(100, 250, REPO, 44, ACC)
s.text(100, 315, "→ ai-finops/", 40, NAVY)
for i, t in enumerate(["Run the workshop", "Re-score our runs", "Read the research", "Compare the gateways"]):
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
s.label(800, 600, "Taming the AI bill", 40, SLATE)

finish()
