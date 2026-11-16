#!/usr/bin/env python3
"""Serious Excalidraw deck: "24 hours to report, 10 years to migrate" (EU CRA reporting, SBOM, post-quantum plan), 25 frames (1600x900),
same look as ai-act-art50-transparency/presentation (Excalifont, roughness 1, navy + one orange accent).
   python3 make_qr.py && python3 build_deck.py     -> ../presentation.excalidraw
Facts on slides come from ../../research.md, ../../comparison.md and ../../workshop/results/."""
import os
from kit import *


def bubble(x, y, w, h, t, size=38, color=NAVY, fill=LIGHT, sw=3):
    s.rect(x, y, w, h, fill=fill, stroke=color, sw=sw)
    s.label(x + w / 2, y + h / 2, t, size, color)


def pill(x, y, w, t, hot=False, size=34, h=64):
    s.rect(x, y, w, h, fill=ACC_L if hot else LIGHT, stroke=ACC if hot else NAVY, sw=3)
    s.label(x + w / 2, y + h / 2, t, size, ACC if hot else NAVY)


def hbar(x, y, w, frac, color=NAVY, fill=MID, h=34):
    s.rect(x, y, w, h, fill="#ffffff", stroke=color, sw=3, round_=False)
    s.rect(x + 3, y + 3, max(4, (w - 6) * frac), h - 6, fill=fill, stroke=color, sw=2, fillStyle="hachure", round_=False)


def timeline(y, x0=140, x1=1460):
    arr([(x0 - 20, y), (x1 + 20, y)], NAVY, sw=5)


def tick(x, y, label, sub, hot=False):
    s.ellipse(x - 20, y - 20, 40, 40, fill=ACC_L if hot else "#ffffff", stroke=ACC if hot else NAVY, sw=4)
    s.label(x, y - 80, label, 44, ACC if hot else NAVY)
    s.label(x, y + 70, sub, 30, SLATE)


# 01 Title
new_frame("Title")
s.text(100, 190, "24 hours to report,", 104, NAVY)
s.text(100, 320, "ten years to migrate", 104, NAVY)
s.line([(104, 470), (700, 474), (1180, 469)], stroke=ACC, sw=7)
s.text(104, 505, "Cyber Resilience Act, SBOMs and a post-quantum plan", 48, SLATE)
clock(1340, 700, 90)
tag(100, 700, "not legal advice", color=ACC, size=34)
s.text(1500, 150, "Internal talk · 35 min", 30, SLATE, align="right")

# 02 Read this first
new_frame("Read this first")
title("Read this first")
scales_x = 330
s.line([(scales_x, 270), (scales_x, 490)], stroke=NAVY, sw=5)
s.line([(scales_x - 90, 490), (scales_x + 90, 490)], stroke=NAVY, sw=5)
s.line([(scales_x - 190, 300), (scales_x, 270), (scales_x + 190, 300)], stroke=NAVY, sw=5)
for sx in (-190, 190):
    s.line([(scales_x + sx, 300), (scales_x + sx - 60, 400)], stroke=SLATE, sw=3)
    s.line([(scales_x + sx, 300), (scales_x + sx + 60, 400)], stroke=SLATE, sw=3)
    s.line([(scales_x + sx - 70, 400), (scales_x + sx, 432), (scales_x + sx + 70, 400)], stroke=NAVY, sw=4, fill=LIGHT, closed=True)
s.rect(720, 270, 780, 330, fill=ACC_L, stroke=ACC, sw=4, style="dashed")
s.label(1110, 380, "General information.", 70, NAVY)
s.label(1110, 480, "Not legal advice.", 70, ACC)
s.label(1110, 560, "an engineer's reading of public sources", 32, SLATE)
s.text(720, 650, "as of 16 November 2026", 40, NAVY)
s.text(720, 710, "scope, roles, \"aware\": ask counsel", 34, SLATE)

# 03 Hook
new_frame("Monday 09 00")
title("Monday, 09:00")
rows = ["$ grype sbom:sbom.cdx.json", "156 findings  in 15 packages", "16 critical   79 high", "pillow 8.1.0  CVE-2023-4863", "              KEV: yes  (exploited)"]
code_panel(100, 235, 900, rows, size=32, hl={3: ACC_L, 4: ACC_L})
clock(1250, 360, 110)
s.label(1250, 530, "24 h", 70, ACC)
s.text(100, 560, "Who decides it is reportable?", 46, NAVY)
s.text(100, 625, "Who submits? What is due tomorrow 09:00?", 46, NAVY)
tag(100, 790, "our measurement · fictional sample product · scanner database of 15 Nov 2026", size=26)

# 04 Dates
new_frame("The dates")
title("The dates")
timeline(450)
tick(300, 450, "Jun 2026", "notified bodies")
tick(800, 450, "11 Sep 2026", "reporting applies", hot=True)
tick(1300, 450, "11 Dec 2027", "everything else")
s.text(100, 640, "Reporting covers products already on the market.", 44, NAVY)
s.text(100, 705, "Article 69(3). Article 14 applies to all of them.", 36, SLATE)
tag(100, 790, "Regulation (EU) 2024/2847, Art. 71 and 69", size=26, color=SLATE)

# 05 Triggers
new_frame("What triggers a report")
title("What triggers a report")
s.rect(100, 240, 690, 330, fill=ACC_L, stroke=ACC, sw=4)
bolt(130, 280, 1.2)
s.label(540, 340, "Actively exploited", 52, ACC)
s.label(540, 400, "vulnerability", 52, ACC)
s.label(540, 490, "reliable evidence of exploitation", 30, NAVY)
s.rect(810, 240, 690, 330, fill=ACC_L, stroke=ACC, sw=4)
shield(850, 290, 1.1)
s.label(1260, 340, "Severe incident", 50, ACC)
s.label(1260, 400, "in the product", 50, ACC)
s.label(1160, 490, "data or functions at risk", 30, NAVY)
s.text(100, 640, "Not every CVE. Not every bug.", 48, NAVY)
tag(100, 740, "Art. 3(42) and Art. 14(5)", size=28, color=SLATE)

# 06 Clock
new_frame("The clock")
title("The clock")
timeline(430, 140, 1450)
tick(240, 430, "aware", "t = 0", hot=True)
tick(560, 430, "24 h", "early warning")
tick(880, 430, "72 h", "notification")
tick(1300, 430, "+14 d", "final report")
s.text(1000, 560, "after a fix or a mitigation", 30, SLATE)
s.text(100, 620, "Incidents: final report one month after the 72 h notice.", 38, NAVY)
s.text(100, 690, "\"Without undue delay\": the hours are the outer limit.", 38, SLATE)
tag(100, 790, "Art. 14(2) and 14(4)", size=26, color=SLATE)

# 07 Who receives
new_frame("One submission")
title("One submission")
box(100, 330, 330, 150, "Manufacturer", 44)
arr([(450, 405), (580, 405)], NAVY)
box(600, 320, 360, 170, "ENISA Single\nReporting Platform", 36, fill=ACC_L, stroke=ACC, color=ACC)
arr([(980, 370), (1100, 300)], NAVY)
arr([(980, 440), (1100, 510)], NAVY)
box(1110, 240, 380, 120, "Home CSIRT", 40)
box(1110, 450, 380, 120, "ENISA", 40)
s.text(100, 640, "Home = where cybersecurity decisions are made.", 40, NAVY)
s.text(100, 705, "The platform has been live since 11 September 2026.", 34, SLATE)
tag(100, 790, "Art. 14(7), Art. 16, ENISA SRP page", size=26, color=SLATE)

# 08 Drill
new_frame("A drill")
title("Rehearse it")
cl = ["$ python ex3_reporting/cra_clock.py vulnerability", "      --aware 2026-11-16T09:00:00Z", "      --now   2026-11-17T10:00:00Z",
      "early_warning  due 11-17 09:00Z  OVERDUE", "notification   due 11-19 09:00Z  open", "final_report   due 12-02 15:00Z  open"]
code_panel(100, 235, 1300, cl, size=32, hl={3: ACC_L})
s.text(100, 600, "Deadline arithmetic is the easy part.", 46, NAVY)
s.text(100, 665, "When you became aware is the hard part.", 46, ACC)
tag(100, 790, "workshop ex3 · deterministic · 19 offline tests", size=26)

# 09 SBOM minimum
new_frame("SBOM the legal minimum")
title("SBOM: the legal minimum")
doc(130, 260, 150, 200, 6)
s.label(205, 510, "machine-readable", 34, NAVY)
for i, t in enumerate(["commonly used format", "at least top-level dependencies", "kept in technical documentation"]):
    s.ellipse(400, 285 + i * 85, 26, 26, fill=ACC, stroke=ACC, sw=2)
    s.text(450, 270 + i * 85, t, 44, NAVY)
s.text(100, 600, "No field list. No format named.", 46, NAVY)
s.text(100, 665, "The bar is set by BSI and CISA guidance.", 40, SLATE)
tag(100, 790, "Annex I Part II(1), Annex VII", size=26, color=SLATE)

# 10 SBOM score
new_frame("Our SBOM scored")
title("Our SBOM scored")
for i, (lab, b, a) in enumerate([("BSI per component", 0.466, 0.670), ("CISA 2026 per component", 0.479, 0.708)]):
    y = 260 + i * 210
    s.text(100, y, lab, 40, NAVY)
    hbar(100, y + 70, 1000, b, NAVY, MID)
    s.text(1130, y + 62, f"{b*100:.1f} %", 40, SLATE)
    hbar(100, y + 120, 1000, a, ACC, ACC_L)
    s.text(1130, y + 112, f"{a*100:.1f} %", 40, ACC)
s.text(100, 700, "raw syft output, then after adding only facts we know", 36, SLATE)
tag(100, 790, "our measurement · 72 components · machine-checkable fields only", size=26)

# 11 Gap
new_frame("What no tool can invent")
title("What no tool can invent")
for i, t in enumerate(["component creator", "supplier contact", "source-code URI"]):
    s.rect(100 + i * 490, 260, 450, 130, fill=LIGHT, stroke=NAVY, sw=3)
    s.label(325 + i * 490, 325, t, 42, NAVY)
    s.label(325 + i * 490, 420, "0 %", 56, ACC)
s.text(100, 520, "Second gap: Python lists only the direct pins.", 44, NAVY)
s.text(100, 585, "The second scanner found three more packages.", 44, ACC)
s.text(100, 650, "certifi · idna · urllib3", 36, SLATE)
tag(100, 790, "our measurement · syft 1.57.1 vs osv-scanner 2.7.1", size=26)

# 12 Two scanners
new_frame("Two scanners")
title("Two scanners")
s.rect(100, 240, 650, 330, fill=LIGHT, stroke=NAVY, sw=3)
s.label(425, 300, "grype", 56, NAVY)
s.label(425, 400, "156", 110, NAVY)
s.label(425, 500, "findings in 15 packages", 34, SLATE)
s.rect(850, 240, 650, 330, fill=ACC_L, stroke=ACC, sw=3)
s.label(1175, 300, "osv-scanner", 56, ACC)
s.label(1175, 400, "215", 110, ACC)
s.label(1175, 500, "vulns in 18 packages", 34, SLATE)
s.text(100, 640, "Different databases, different matching rules.", 44, NAVY)
s.text(100, 705, "Counts change daily. Only the overlap is stable.", 36, SLATE)
tag(100, 790, "our measurement · databases of 15 Nov 2026", size=26)

# 13 VEX
new_frame("VEX")
title("VEX: not affected, in writing")
funnel(150, 250, 280, 200)
s.label(290, 500, "156", 70, NAVY)
arr([(470, 350), (640, 350)], NAVY)
s.label(780, 350, "137", 90, ACC)
s.label(780, 440, "after 19 statements", 32, SLATE)
s.text(1000, 270, "6 unused direct", 40, NAVY)
s.text(1000, 320, "dependencies", 40, NAVY)
s.text(1000, 400, "a human must", 36, ACC)
s.text(1000, 450, "sign each one", 36, ACC)
s.text(100, 620, "The actively exploited finding stays.", 46, NAVY)
s.text(100, 685, "Pillow is imported by the product.", 36, SLATE)
tag(100, 790, "our measurement · OpenVEX read by grype · a claim, not a fact", size=26)

# 14 LLM draft
new_frame("A model drafts the advisory")
title("Let a model draft the advisory?")
bubble(100, 250, 640, 190, "facts: CVE, component,\nfix version, mitigation", 36, NAVY, LIGHT)
arr([(760, 345), (880, 345)], NAVY)
bubble(900, 250, 600, 190, "\"critical\"  ·  \"remote\ncode execution\"  ·  \"immediately\"", 34, ACC, ACC_L, sw=4)
s.text(100, 520, "Four of four free-model drafts added claims", 44, NAVY)
s.text(100, 585, "that were not in the facts.", 44, NAVY)
s.text(100, 665, "Use it as a first draft behind a fact guard.", 40, ACC)
tag(100, 790, "our measurement · free OpenRouter model · 4 runs · small sample", size=26)

# 15 PQC dates
new_frame("The quantum dates")
title("The quantum dates")
timeline(430, 140, 1450)
tick(260, 430, "end 2026", "EU: start")
tick(640, 430, "2030", "EU: high-risk done", hot=True)
tick(1000, 430, "after 2030", "NIST: deprecate")
tick(1340, 430, "2035", "NIST: disallow", hot=True)
s.text(100, 600, "The EU roadmap is addressed to Member States.", 40, NAVY)
s.text(100, 665, "The CRA itself only says \"state of the art\".", 40, SLATE)
tag(100, 790, "EU roadmap June 2025 · NIST IR 8547, October 2026", size=26, color=SLATE)

# 16 HNDL
new_frame("Harvest now decrypt later")
title("Harvest now, decrypt later")
box(100, 300, 280, 120, "recorded\ntraffic", 36)
arr([(400, 360), (560, 360)], NAVY)
s.label(740, 340, "store", 40, SLATE)
arr([(870, 360), (1030, 360)], NAVY, style="dashed")
box(1050, 300, 340, 120, "decrypt, later", 36, fill=ACC_L, stroke=ACC, color=ACC)
s.text(100, 520, "Key exchange: act first.", 46, ACC)
s.text(100, 585, "Signatures: only matter if forged later.", 40, NAVY)
s.text(100, 650, "Long-lived roots and devices you cannot update come first.", 36, SLATE)
tag(100, 790, "EC statement on store-now-decrypt-later · when quantum arrives is a forecast", size=26, color=SLATE)

# 17 Inventory
new_frame("Inventory")
title("Find your crypto")
inv = ["$ python ex4_crypto_inventory/scan_crypto.py", "32 findings in 5 files, 13 CBOM components", "RSA 8   ECDH 5   ECDSA 2   P-curve 5", "X25519 3  Ed25519 1  MD5 1  SHA-1 1", "AES-256-GCM 1  SHA-256 3  TLS 1.2 2"]
code_panel(100, 235, 1300, inv, size=32, hl={1: ACC_L})
s.text(100, 560, "A grep with opinions. It misses binaries, HSMs, libraries.", 40, NAVY)
s.text(100, 625, "Add network probes, certificate stores, owners.", 40, SLATE)
tag(100, 790, "workshop ex4 · output is a CycloneDX 1.6 CBOM, schema-valid", size=26)

# 18 Mosca
new_frame("Rank by lifetime")
title("Rank by lifetime")
s.label(800, 290, "how long it must stay secret  +  how long to migrate  >  years until quantum?", 38, NAVY)
for j, (z, n) in enumerate([("Z = 8 years", 5), ("Z = 12 years", 4), ("Z = 15 years", 0)]):
    x = 100 + j * 490
    s.rect(x, 370, 450, 250, fill=ACC_L if n else LIGHT, stroke=ACC if n else NAVY, sw=3)
    s.label(x + 225, 410, z, 38, NAVY)
    s.label(x + 225, 500, str(n), 80, ACC if n else SLATE)
    s.label(x + 225, 585, "assets: migrate now", 28, SLATE)
s.text(100, 660, "Nobody knows Z. Say yours out loud.", 46, NAVY)
tag(100, 790, "workshop ex4 · fictional asset lifetimes · Z is a forecast parameter", size=26)

# 19 Hybrid bytes
new_frame("Hybrid handshake")
title("The hybrid handshake")
for i, (lab, v, hot) in enumerate([("X25519", 330, False), ("X25519MLKEM768", 1506, True)]):
    y = 260 + i * 150
    s.text(100, y, lab, 38, ACC if hot else NAVY)
    hbar(520, y + 4, 780, v / 1506, ACC if hot else NAVY, ACC_L if hot else MID)
    s.text(1330, y, f"{v} B", 34, ACC if hot else SLATE)
s.text(100, 560, "ClientHello grows about 1.2 kB.", 46, NAVY)
s.text(100, 625, "Server flight grows about 1.1 kB.", 46, NAVY)
s.text(100, 700, "Negotiated by default in OpenSSL 3.5. Time: no visible change.", 36, SLATE)
tag(100, 790, "our measurement · OpenSSL 3.5.7 · localhost · 30 handshakes each", size=26)

# 20 What breaks
new_frame("What breaks")
title("What breaks in practice")
s.rect(100, 240, 700, 300, fill=LIGHT, stroke=NAVY, sw=3)
s.label(450, 300, "client offers only the hybrid", 36, NAVY)
s.label(450, 360, "server knows only X25519", 36, NAVY)
s.label(450, 465, "0 of 5", 80, ACC)
s.rect(830, 240, 670, 300, fill=LIGHT, stroke=NAVY, sw=3)
s.label(1165, 300, "client offers only pure ML-KEM", 36, NAVY)
s.label(1165, 360, "default OpenSSL 3.5 server", 36, NAVY)
s.label(1165, 465, "0 of 5", 80, ACC)
s.text(100, 620, "A default client falls back to X25519 and works.", 40, NAVY)
s.text(100, 685, "Failures come from strict offers and server settings.", 40, SLATE)
tag(100, 790, "our measurement · localhost · small sample · browsers and middleboxes not tested", size=26)

# 21 Signature sizes
new_frame("Signature sizes")
title("Post-quantum signatures are heavy")
vals = [("ECDSA P-256", 385), ("RSA-2048", 781), ("ML-DSA-44", 3981), ("ML-DSA-65", 5510), ("ML-DSA-87", 7468)]
for i, (lab, v) in enumerate(vals):
    y = 240 + i * 95
    hot = lab.startswith("ML")
    s.text(100, y, lab, 36, ACC if hot else NAVY)
    hbar(420, y + 4, 800, v / 7468, ACC if hot else NAVY, ACC_L if hot else MID, h=34)
    s.text(1450, y, f"{v} B", 32, SLATE, align="right")
s.text(100, 740, "self-signed certificate, DER size. Works in TLS 1.3 with OpenSSL 3.5.7.", 32, SLATE)
tag(100, 800, "our measurement · public CAs, browsers and HSMs not tested · FIPS 206 unpublished", size=26)

# 22 Plan
new_frame("Ninety days")
title("Ninety days")
steps = ["Rehearse the 24 h drill", "SBOM from the build, checked in CI", "Two scanners, VEX with sign-off", "Crypto inventory with owners", "One hybrid TLS pilot, measured"]
for i, t in enumerate(steps):
    y = 235 + i * 100
    s.ellipse(110, y + 12, 44, 44, fill=ACC if i == 0 else ACC_L, stroke=ACC, sw=3)
    s.label(132, y + 34, str(i + 1), 28, "#ffffff" if i == 0 else ACC)
    s.text(190, y, t, 50, NAVY)
tag(100, 790, "from the comparison guide in the repo", size=26, color=SLATE)

# 23 Honest limits
new_frame("Honest limits")
title("Honest limits")
lim = [("Not legal advice", "scope and roles: counsel"), ("Synthetic product", "fictional, deliberately outdated"),
       ("Open items", "SRP form fields, harmonised standards"), ("Not tested", "browsers, CAs, HSMs, binaries")]
for i, (a, b) in enumerate(lim):
    x, y = 100 + (i % 2) * 740, 240 + (i // 2) * 270
    s.rect(x, y, 700, 230, fill=LIGHT, stroke=NAVY, sw=3)
    s.line([(x + 28, y + 40), (x + 30, y + 120), (x + 27, y + 190)], stroke=ACC, sw=6)
    s.text(x + 50, y + 55, a, 48, NAVY)
    s.text(x + 50, y + 130, b, 32, SLATE)

# 24 Try it
new_frame("Try it yourself")
title("Try it yourself")
s.text(100, 250, REPO, 44, ACC)
s.text(100, 315, "→ cra-sbom-pqc/", 40, NAVY)
for i, t in enumerate(["Score an SBOM", "Run the 24 h clock", "Rank your crypto", "Negotiate ML-KEM"]):
    s.ellipse(110, 440 + i * 85 + 12, 26, 26, fill=ACC, stroke=ACC, sw=2)
    s.text(165, 438 + i * 85, t, 48, NAVY)
qr_path = os.path.join(ROOT, "qr.png")
s.rect(1030, 230, 460, 460, fill="#ffffff", stroke=NAVY, sw=3)
s.image(qr_path, 1050, 250, 420, 420)
s.label(1260, 740, "scan me", 38, SLATE)

# 25 Questions
new_frame("Questions")
s.label(800, 380, "Questions?", 140, NAVY)
s.line([(430, 480), (800, 486), (1170, 479)], stroke=ACC, sw=7)
s.label(800, 600, "24 hours to report, ten years to migrate", 40, SLATE)

finish()
