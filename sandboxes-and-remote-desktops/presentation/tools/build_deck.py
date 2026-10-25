#!/usr/bin/env python3
"""Sandboxes and remote desktops for AI agents: 20 Excalidraw frames (1600x900), same hand-drawn serious style
as system-one-models/presentation/serious (Excalifont, roughness 1, navy + one orange accent, no characters).
   python3 build_deck.py     -> ../presentation.excalidraw   (needs ../qr.png from make_qr.py)"""
from kit import *

ASSETS = os.path.abspath(os.path.join(ROOT, "..", "assets"))
TOPIC = "sandboxes-and-remote-desktops"


# ---------- extra doodles for this topic ----------
def terminal(x, y, w=110, h=80, color=NAVY):
    s.rect(x, y, w, h, fill="#ffffff", stroke=color, sw=3)
    s.line([(x + 16, y + 22), (x + 34, y + 36), (x + 16, y + 50)], stroke=ACC, sw=4)
    s.line([(x + 46, y + 54), (x + 74, y + 54)], stroke=color, sw=4)


def folder(x, y, w=110, h=80, color=NAVY):
    s.line([(x, y + 16), (x, y + h), (x + w, y + h), (x + w, y + 16), (x + w * 0.45, y + 16), (x + w * 0.38, y), (x, y)],
           stroke=color, closed=True, sw=3, fill=LIGHT)


def tag_r(t, y, size=26, color=ACC):
    """tag whose right edge sits at x=1500"""
    w, _ = measure(t, size)
    tag(1500 - (w + 36), y, t, color, size)


def globe(x, y, d=84, color=NAVY):
    s.ellipse(x, y, d, d, fill="#ffffff", stroke=color, sw=3)
    s.ellipse(x + d * 0.3, y, d * 0.4, d, stroke=color, sw=2)
    s.line([(x, y + d / 2), (x + d, y + d / 2)], stroke=color, sw=2)


def key(x, y, k=1.0, color=ACC):
    s.ellipse(x, y, 40 * k, 40 * k, stroke=color, sw=4)
    s.line([(x + 40 * k, y + 20 * k), (x + 110 * k, y + 20 * k)], stroke=color, sw=4)
    s.line([(x + 90 * k, y + 20 * k), (x + 90 * k, y + 40 * k)], stroke=color, sw=4)
    s.line([(x + 106 * k, y + 20 * k), (x + 106 * k, y + 36 * k)], stroke=color, sw=4)


def monitor(x, y, w=160, h=110, color=NAVY):
    s.rect(x, y, w, h, fill="#ffffff", stroke=color, sw=3)
    s.line([(x + w / 2, y + h), (x + w / 2, y + h + 22)], stroke=color, sw=4)
    s.line([(x + w / 2 - 36, y + h + 24), (x + w / 2 + 36, y + h + 24)], stroke=color, sw=4)


def cursor_arrow(x, y, k=1.0, color=ACC):
    s.line([(x, y), (x, y + 70 * k), (x + 18 * k, y + 54 * k), (x + 34 * k, y + 88 * k), (x + 46 * k, y + 82 * k), (x + 30 * k, y + 50 * k), (x + 54 * k, y + 48 * k)],
           stroke=color, closed=True, fill=ACC_L, sw=3)


def cloud(x, y, k=1.0, color=NAVY):
    s.ellipse(x, y + 24 * k, 70 * k, 56 * k, stroke=color, sw=3, fill="#ffffff")
    s.ellipse(x + 40 * k, y, 80 * k, 70 * k, stroke=color, sw=3, fill="#ffffff")
    s.ellipse(x + 90 * k, y + 28 * k, 70 * k, 52 * k, stroke=color, sw=3, fill="#ffffff")
    s.rect(x + 28 * k, y + 50 * k, 110 * k, 34 * k, stroke="#ffffff", fill="#ffffff", sw=1, rough=0, round_=False)


def padlock(x, y, k=1.0, color=NAVY):
    s.rect(x, y + 34 * k, 70 * k, 56 * k, fill=LIGHT, stroke=color, sw=3)
    s.line([(x + 14 * k, y + 34 * k), (x + 14 * k, y + 14 * k), (x + 35 * k, y), (x + 56 * k, y + 14 * k), (x + 56 * k, y + 34 * k)], stroke=color, sw=3)


# =====================================================================
# 01 Title
new_frame("Title")
s.text(100, 235, "Sandboxes for AI agents", 112, NAVY)
s.line([(104, 385), (700, 389), (1240, 384)], stroke=ACC, sw=7)
s.text(104, 420, "Safe places to run code and use a screen", 52, SLATE)
# doodle: agent inside a dashed wall
s.rect(150, 600, 520, 190, fill="#ffffff", stroke=ACC, sw=4, style="dashed")
s.rect(200, 650, 150, 90, fill=LIGHT, stroke=NAVY, sw=3)
s.label(275, 695, "agent", 36, NAVY)
terminal(430, 655, 100, 80)
s.rect(570, 655, 60, 80, fill="#ffffff", stroke=NAVY, sw=3, round_=False)
arr([(720, 695), (850, 695)], SLATE, style="dashed", sw=3)
cross(870, 670, 1.0, ACC, 7)
s.text(960, 668, "your machine", 42, SLATE)
s.text(1500, 150, "Internal talk · 30 min", 30, SLATE, align="right")

# 02 Agents act
new_frame("Agents act")
title("Agents do not only talk")
box(100, 400, 260, 120, "Model", 52, fill=ACC_L, stroke=ACC, color=ACC)
tools = [("Run commands", terminal), ("Edit files", folder), ("Browse the web", globe), ("Call services", cloud)]
for i, (t, fn) in enumerate(tools):
    y = 235 + i * 130
    s.rect(520, y, 470, 110, fill=LIGHT, stroke=NAVY, sw=3)
    if fn is terminal: terminal(545, y + 20, 80, 62)
    elif fn is folder: folder(545, y + 22, 80, 60)
    elif fn is globe: globe(550, y + 14, 80)
    else: cloud(540, y + 18, 0.55)
    s.text(660, y + 32, t, 38, NAVY)
    arr([(360, 460), (505, y + 55)], SLATE, sw=3)
    arr([(1000, y + 55), (1085, 460)], SLATE, sw=3)
s.rect(1100, 380, 400, 160, fill="#ffffff", stroke=ACC, sw=4)
s.label(1300, 440, "A real machine", 44, ACC)
s.label(1300, 495, "files · keys · network", 32, SLATE)
caption("Every tool call has real effects", 810, NAVY, 42)

# 03 Replit
new_frame("When an agent gets it wrong")
title("When an agent gets it wrong")
s.text(100, 165, "Replit · July 2025", 36, SLATE)
s.line([(130, 440), (1470, 440)], stroke=NAVY, sw=4)
steps = [(210, "Code freeze", "no changes allowed", NAVY), (570, "Live database\ndeleted", "by the agent", ACC),
         (930, "“Rollback is\nimpossible”", "the agent said", SLATE), (1290, "Rollback\nworked", "data restored", NAVY)]
for i, (x, a, b, c) in enumerate(steps):
    s.ellipse(x - 26, 414, 52, 52, fill=ACC_L if c == ACC else "#ffffff", stroke=c, sw=4)
    s.label(x, 560, a, 44, c)
    s.label(x, 668, b, 32, SLATE)
cross(906, 300, 1.0, SLATE, 8)
check(1262, 300, 1.0, ACC, 8)
s.label(210, 340, "!", 70, NAVY)
s.label(570, 340, "×", 80, ACC)
caption("Infrastructure saved the data, not the prompt", 790, ACC, 40)
tag_r("reported by The Register, Business Insider", 190)

# 04 Hidden instructions
new_frame("Hidden instructions")
title("Hidden instructions")
doc(110, 290, 150, 200, 5)
s.rect(128, 392, 114, 22, fill=ACC_L, stroke=ACC, sw=2, style="dashed", round_=False)
s.label(185, 530, "a README", 38, NAVY)
tag(110, 580, "one hidden line", size=28)
arr([(300, 390), (470, 390)], ACC)
box(490, 330, 300, 120, "Coding agent", 44)
arr([(810, 390), (980, 390)], ACC)
key(1010, 355, 1.0, ACC)
s.label(1070, 440, "your keys", 38, NAVY)
s.line([(1210, 280), (1210, 500)], stroke=ACC, sw=5, style="dashed")
arr([(1100, 395), (1380, 395)], ACC, sw=4)
s.label(1380, 345, "sent out", 38, ACC)
s.text(100, 665, "Research study", 36, NAVY)
s.text(100, 715, "attack success on coding assistants", 30, SLATE)
s.line([(760, 720), (1480, 720)], stroke=NAVY, sw=4)
for v in (0, 50, 100):
    s.line([(760 + 7.2 * v, 706), (760 + 7.2 * v, 734)], stroke=NAVY, sw=3)
s.rect(760 + 7.2 * 41, 698, 7.2 * 43, 44, fill=ACC_L, stroke=ACC, sw=3, fillStyle="hachure", round_=False)
s.label(760 + 7.2 * 62.5, 670, "41–84 %", 38, ACC)
s.text(760, 748, "0", 28, SLATE)
s.text(1480, 748, "100 %", 28, SLATE, align="right")
tag_r("HiddenLayer 2025 · arXiv 2509.22040", 190)

# 05 Three ingredients
new_frame("Three ingredients of a leak")
title("Three ingredients of a leak")
R = 175
circ = [(440, 390, ""), (720, 390, ""), (580, 575, "")]
for i, (cx, cy, t) in enumerate(circ):
    s.ellipse(cx - R, cy - R, 2 * R, 2 * R, stroke=NAVY if i < 2 else ACC, fill="transparent", sw=4)
s.label(388, 365, "private\ndata", 34, NAVY)
s.label(772, 365, "untrusted\ncontent", 32, NAVY)
s.label(580, 675, "a way out", 38, ACC)
s.rect(530, 430, 100, 56, fill="#ffffff", stroke="#ffffff", sw=1, rough=0, round_=False)
s.label(580, 458, "leak", 48, ACC)
s.text(1000, 250, "A sandbox cuts the legs", 44, NAVY)
for i, (a, b) in enumerate([("No real secrets inside", "cuts the data"), ("Network off or allowlisted", "cuts the way out")]):
    y = 340 + i * 190
    s.rect(1000, y, 500, 150, fill=LIGHT, stroke=NAVY, sw=3)
    s.text(1030, y + 28, a, 34, NAVY)
    s.text(1030, y + 88, b, 34, ACC)
caption("Take one away and an attack becomes an annoyance", 810, SLATE, 36)

# 06 What is a sandbox
new_frame("What is a sandbox")
title("What is a sandbox?")
s.text(100, 165, "A disposable, walled-off computer for the agent", 38, SLATE)
s.rect(100, 250, 860, 520, fill="#ffffff", stroke=ACC, sw=5, style="dashed")
s.text(130, 268, "Sandbox", 44, ACC)
box(150, 380, 230, 110, "Agent", 44)
arr([(390, 435), (470, 435)], SLATE, sw=3)
terminal(490, 395, 110, 80)
folder(640, 398, 110, 78)
s.label(545, 520, "run", 32, SLATE)
s.label(695, 520, "files", 32, SLATE)
for i, t in enumerate(["own files", "network rules", "CPU · RAM · time"]):
    x = 130 + i * 275
    s.rect(x, 640, 260, 80, fill=ACC_L, stroke=ACC, sw=2)
    s.label(x + 130, 680, t, 28, NAVY)
arr([(975, 500), (1090, 500)], SLATE, style="dashed", sw=3)
cross(1100, 475, 1.0, ACC, 7)
s.rect(1180, 340, 320, 320, fill=LIGHT, stroke=NAVY, sw=3)
s.label(1340, 400, "Your machine", 40, NAVY)
key(1275, 450, 0.9, SLATE)
padlock(1325, 540, 0.9)
s.label(1340, 705, "stays untouched", 34, SLATE)
tag(620, 262, "thrown away afterwards", size=26)

# 07 Isolation ladder
new_frame("The isolation ladder")
title("The isolation ladder")
rungs = [("Process", "shared kernel"), ("Container", "shared kernel"), ("gVisor", "kernel in user space"),
         ("microVM", "own kernel"), ("Full VM", "own kernel, any OS")]
for i, (a, b) in enumerate(rungs):
    x = 100 + i * 285
    hh = 120 + i * 62
    top = 760 - hh
    hot = (i == 3)
    s.rect(x, top, 270, hh, fill=ACC_L if hot else LIGHT, stroke=ACC if hot else NAVY, sw=3)
    s.label(x + 135, top + 48, a, 44, ACC if hot else NAVY)
    s.label(x + 135, top + 100, b, 26, SLATE)
arr([(120, 215), (1480, 215)], SLATE, sw=3)
s.text(100, 165, "weaker wall", 32, SLATE)
s.text(1500, 165, "stronger wall", 32, SLATE, align="right")
tag(1090 - measure("Firecracker: E2B, Vercel, Fly", 26)[0] / 2 - 18, 785, "Firecracker: E2B, Vercel, Fly", size=26)
s.text(100, 270, "WASM and V8 isolates are a different,\nlighter kind of sandbox", 30, SLATE)

# 08 Pick by trust
new_frame("Pick by trust")
title("Pick by trust")
rows = [("Your own code", "Container", False), ("Code from an LLM, many tenants", "gVisor or microVM", True), ("Needs a screen or Windows", "Full VM", False)]
for i, (a, b, hot) in enumerate(rows):
    y = 250 + i * 190
    s.rect(100, y, 700, 140, fill=LIGHT, stroke=NAVY, sw=3)
    s.label(450, y + 70, a, 40 if len(a) < 20 else 36, NAVY)
    arr([(830, y + 70), (1000, y + 70)], ACC if hot else NAVY)
    s.rect(1030, y, 470, 140, fill=ACC_L if hot else "#ffffff", stroke=ACC if hot else NAVY, sw=3)
    s.label(1265, y + 70, b, 44, ACC if hot else NAVY)
tag(100, 205 + 0, "rule of thumb", size=26)

# 09 A screen for the agent
new_frame("A screen for the agent")
title("A screen for the agent")
box(100, 400, 230, 110, "Agent", 44)
s.rect(620, 230, 500, 520, fill="#ffffff", stroke=ACC, sw=4, style="dashed")
s.text(645, 245, "Container", 36, ACC)
for i, t in enumerate(["Browser", "Window manager", "Virtual screen"]):
    box(660, 310 + i * 130, 420, 100, t, 40, fill=ACC_L if i == 2 else LIGHT, stroke=ACC if i == 2 else NAVY)
arr([(610, 400), (345, 425)], ACC, sw=4)
s.label(478, 360, "screenshot", 32, ACC)
arr([(345, 490), (610, 520)], NAVY, sw=4)
s.label(478, 565, "click · type", 32, NAVY)
arr([(1140, 490), (1240, 490)], SLATE, sw=4)
s.label(1190, 445, "VNC", 30, SLATE)
monitor(1270, 420, 200, 140)
s.label(1370, 640, "you watch in a\nbrowser tab", 32, NAVY)

# 10 See think act
new_frame("See, think, act")
title("See, think, act")
nodes = [(300, 300, "Screenshot"), (1000, 300, "Vision model"), (650, 600, "Click · type")]
for x, y, t in nodes:
    box(x, y, 300, 110, t, 42, fill=ACC_L if t.startswith("Vision") else LIGHT, stroke=ACC if t.startswith("Vision") else NAVY,
        color=ACC if t.startswith("Vision") else NAVY)
arr([(610, 355), (990, 355)], NAVY)
arr([(1120, 420), (960, 590)], NAVY)
arr([(640, 640), (400, 420)], NAVY)
s.label(800, 295, "what is on screen?", 30, SLATE)
cursor_arrow(1400, 620, 1.2)
s.text(100, 780, "repeat until the model says “done”", 38, ACC)
tag_r("our workshop: ex4", 190)

# 11 Who sells this
new_frame("Same job, different walls")
title("Same job, different walls")
prov = [("E2B", "microVM"), ("Vercel Sandbox", "microVM"), ("Fly.io Sprites", "microVM"),
        ("Cloudflare", "microVM per container"), ("Modal", "gVisor, VMs since Oct 2026"), ("Daytona", "containers + a VM class")]
for i, (a, b) in enumerate(prov):
    x, y = 100 + (i % 3) * 480, 240 + (i // 3) * 270
    s.rect(x, y, 440, 230, fill=ACC_L if i == 0 and False else LIGHT, stroke=NAVY, sw=3)
    s.label(x + 220, y + 85, a, 50, NAVY)
    s.label(x + 220, y + 160, b, 28, SLATE)
caption("Also: browser clouds, and your own Docker", 805, SLATE, 36)
tag_r("checked 10 Oct 2026", 190)

# 12 Cold start
new_frame("Measure the cold start")
title("Measure the cold start")
s.text(100, 165, "seconds until the sandbox ran its first command", 34, SLATE)
data = [("E2B code sandbox", 1.30, False), ("Local Docker, Python", 1.16, False), ("E2B Desktop", 5.98, True), ("Own Docker desktop", 7.22, True)]
x0, sc = 560, 120
for i, (t, v, d) in enumerate(data):
    y = 270 + i * 120
    s.text(100, y + 14, t, 38, NAVY)
    s.rect(x0, y, v * sc, 70, fill=ACC_L if d else MID, stroke=ACC if d else NAVY, sw=3, fillStyle="hachure", round_=False)
    s.text(x0 + v * sc + 20, y + 10, f"{v:.1f} s", 42, ACC if d else NAVY)
s.line([(x0 - 6, 255), (x0 - 6, 740)], stroke=NAVY, sw=3)
caption("Vendors quote about 150 ms. Boot time is not first command.", 805, SLATE, 36)
tag_r("our measurement · 5 runs · median", 190)

# 13 Demo setup
new_frame("Live demo: the setup")
title("Live demo: the setup")
cmd = ['docker run -d --rm \\', '  --network none \\', '  --memory 512m --cpus 1 \\', '  --pids-limit 128 \\', '  --read-only --tmpfs /tmp \\',
       '  --user 65534:65534 \\', '  python:3.12-slim sleep 600']
code_panel(100, 215, 780, cmd, size=30, hl={1: ACC_L})
for i, (a, yy) in enumerate([("no network", 255), ("capped memory, CPU", 340), ("read-only, not root", 425)]):
    arr([(910, yy + 28), (1000, yy + 28)], ACC, sw=3)
    s.text(1020, yy, a, 42, ACC)
s.text(100, 745, "python ex2_llm_loop/agent.py \"30th Fibonacci number and the sum of primes below 10000\"", 26, NAVY)
tag(100, 800, "shortened from ex2_llm_loop/agent.py", size=28)

# 14 Demo result
new_frame("Live demo: the result")
title("Live demo: the result")
s.rect(100, 250, 380, 300, fill="#ffffff", stroke=NAVY, sw=3)
s.label(290, 300, "Task", 40, NAVY)
s.label(290, 420, "30th Fibonacci\nsum of primes\nbelow 10000", 34, SLATE)
arr([(500, 400), (590, 400)], NAVY)
box(610, 340, 220, 120, "Model", 44, fill=ACC_L, stroke=ACC, color=ACC)
arr([(850, 400), (940, 400)], ACC)
s.rect(960, 250, 330, 300, fill=LIGHT, stroke=ACC, sw=4, style="dashed")
s.label(1125, 300, "Sandbox", 40, ACC)
terminal(1070, 360, 110, 80)
s.label(1125, 490, "runs the code", 30, SLATE)
arr([(1310, 400), (1380, 400)], ACC)
s.rect(1390, 330, 130, 140, fill="#ffffff", stroke=ACC, sw=3)
check(1415, 365, 1.0, ACC, 8)
s.text(100, 610, "832040", 80, NAVY)
s.text(560, 610, "5736396", 80, NAVY)
s.text(100, 715, "both correct · one tool call · about 12 s", 40, SLATE)
tag(100, 790, "recorded run · free model · local Docker, not E2B", size=28)

# 15 Demo desktop
new_frame("Live demo: a desktop agent")
title("Live demo: a desktop agent")
for x, p, lab in [(100, "ex3-desktop.png", "start: example.com"), (860, "ex4-run.png", "agent ended on iana.org")]:
    s.rect(x - 10, 230, 660, 420, fill="#ffffff", stroke=NAVY, sw=3, round_=False)
    s.image(os.path.join(ASSETS, p), x, 240, 640, 400)
    s.label(x + 320, 690, lab, 36, NAVY)
arr([(765, 440), (845, 440)], ACC, sw=5)
s.text(100, 750, "read the page: 4 steps, about 20 s", 38, NAVY)
s.text(860, 750, "click a link: 24 steps, about 6 min", 38, ACC)
tag(100, 810, "recorded run · free vision model · our own Docker desktop", size=26)

# 16 Honest limits
new_frame("Honest limits")
title("Honest limits")
lim = [("Free models are flaky", "1 of 5 usable on the desktop"), ("Vendor numbers", "are claims, not proof"),
       ("Some details unverified", "e.g. isolation of Devin, Cursor agents"), ("Providers move fast", "Daytona open source archived")]
for i, (a, b) in enumerate(lim):
    x, y = 100 + (i % 2) * 740, 240 + (i // 2) * 270
    s.rect(x, y, 700, 230, fill=LIGHT, stroke=NAVY, sw=3)
    s.line([(x + 28, y + 40), (x + 30, y + 120), (x + 27, y + 190)], stroke=ACC, sw=6)
    s.text(x + 50, y + 55, a, 46, NAVY)
    s.text(x + 50, y + 130, b, 34, SLATE)

# 17 Checklist
new_frame("Production checklist")
title("Production checklist")
items = ["Network off or allowlisted", "No production secrets", "CPU, memory and time limits", "Log every command",
         "Human OK for destructive steps", "Backups out of its reach"]
for i, t in enumerate(items):
    x, y = 100 + (i % 2) * 740, 240 + (i // 2) * 175
    s.rect(x, y, 700, 145, fill=LIGHT, stroke=NAVY, sw=3)
    check(x + 35, y + 42, 0.9, ACC, 7)
    s.text(x + 125, y + 48, t, 38 if len(t) < 28 else 34, NAVY)

# 18 Takeaways
new_frame("Three takeaways")
title("Three takeaways")
for i, t in enumerate(["The prompt is\nnot a wall", "Match the wall\nto the trust", "Measure it,\nnot the brochure"]):
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
for i, t in enumerate(["Run the workshop", "Benchmark a cold start", "Compare the providers", "Read the sources"]):
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
s.label(800, 600, "Sandboxes for AI agents", 40, SLATE)

out = s.to_json()
probs = validate(out)
if probs:
    print("PROBLEMS:", *probs[:20], sep="\n"); sys.exit(1)
json.dump(out, open(os.path.join(ROOT, "presentation.excalidraw"), "w"))
print("presentation.excalidraw:", count[0], "frames,", len(out["elements"]), "elements")
