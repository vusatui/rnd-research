# 24 hours to report, ten years to migrate (CRA reporting, SBOM, post-quantum plan): the 35-minute talk as an Excalidraw deck

> General information, not legal advice. See [`../research.md`](../research.md).

Serious, sober deck in the same format as [`ai-act-art50-transparency/presentation/`](../../ai-act-art50-transparency/presentation/README.md): hand-drawn Excalidraw look (Excalifont, roughness 1, sketchy arrows and doodle icons drawn from Excalidraw primitives), navy + one orange accent on white, no characters, no jokes. 25 slides, one idea each, a title and a few words; everything else is in the speaker notes, which are a word-for-word read-aloud script. Audience: engineers, architects, security and delivery leads.

| What | File |
|---|---|
| Deck (Excalidraw, 25 frames) | [`presentation.excalidraw`](presentation.excalidraw) |
| PDF / PNG / SVG per slide / overview | [`presentation.pdf`](presentation.pdf), [`export/`](export/), [`contact-sheet.png`](contact-sheet.png) |
| Read-aloud script (full sentences, about 130 words per minute, 35 min) with slide times, a few italic stage directions and 10 spoken Q&As at the end | [`speaker-notes.md`](speaker-notes.md) (same text as [`../talk-script.md`](../talk-script.md)) |
| QR code of this topic folder (slide 24) | [`qr.png`](qr.png) |
| Demo material (recorded runs, shortened) | [`../workshop/`](../workshop/README.md): committed outputs in `results/`; every command on slides 3, 8 and 17 runs offline apart from the scanners' databases |
| Generator and export tooling | [`tools/`](tools/) (reuses [`../../system-one-models/presentation/tools/`](../../system-one-models/presentation/tools/README.md) for the Excalidraw bundle and `node_modules`) |

Slides: 1 Title · 2 Read this first (not legal advice) · 3 Monday, 09:00 · 4 The dates · 5 What triggers a report · 6 The clock · 7 One submission · 8 Rehearse it · 9 SBOM: the legal minimum · 10 Our SBOM scored · 11 What no tool can invent · 12 Two scanners · 13 VEX · 14 Let a model draft the advisory? · 15 The quantum dates · 16 Harvest now, decrypt later · 17 Find your crypto · 18 Rank by lifetime · 19 The hybrid handshake · 20 What breaks in practice · 21 Post-quantum signatures are heavy · 22 Ninety days · 23 Honest limits · 24 Try it yourself (repo link + QR) · 25 Questions.

## Open the deck
Go to <https://excalidraw.com> → ☰ **Open** → `presentation.excalidraw`. Each slide is a frame named `Slide NN …`, 4 per row. To present: click a frame, <kbd>Shift</kbd>+<kbd>2</kbd>, then the next one. Easy fallback: `presentation.pdf` full-screen.

## Rebuild
Prerequisites: the first deck's tooling set up once (`cd ../../system-one-models/presentation/tools && npm install` plus the esbuild bundle, see its README), `pip install pillow fonttools brotli segno`, and Google Chrome. Nothing is installed in this folder.
```bash
cd cra-sbom-pqc/presentation/tools
python3 make_qr.py          # ../qr.png (QR of https://github.com/vusatui/rnd-research/tree/main/cra-sbom-pqc/)
python3 build_deck.py       # ../presentation.excalidraw (validates structure, text margins and text overlaps)
node export_frames.mjs      # ../export/*.svg|png  (real Excalidraw renderer)
python3 contact_sheet.py && python3 make_pdf.py
```

## Honesty notes
- Facts as in [`../research.md`](../research.md) and [`../comparison.md`](../comparison.md) (as of 2026-11-16), with their markers. Items the research marks 🟠 (the delegated act on delaying dissemination is known only from the Commission page; the harmonised-standards status from a tracker; FIPS 206 status from NIST IR 8547 plus trackers; the Mosca inequality as a common heuristic) or ❌ (SRP form fields, Commission guidance in full, Digital Omnibus effect) are said as secondary or open in the notes, never as verified facts.
- Numbers marked "our measurement" come from [`../workshop/results/`](../workshop/results/): one fictional, deliberately outdated sample product, one Linux machine, scanner databases of 15 Nov 2026, OpenSSL 3.5.7 on localhost, 30 handshakes per configuration. They show mechanisms and failure modes, not the performance of any vendor product. Vulnerability counts change daily.
- Slide 3 shows the grype summary lines of that run (156 findings, 16 critical, 79 high, one KEV match). Slide 8 is the real output of `cra_clock.py`. Slide 17 is the real output of `scan_crypto.py` (shortened to counts).
- Slide 14 is 4 runs of one free model; the guard is a keyword check, not a proof. Slide 18's lifetimes are fictional; Z is a forecast parameter, not a fact. Slide 19 timings are dominated by process start and are not latency claims.
- The EU roadmap dates (slide 15) are addressed to Member States; the NIST dates apply to NIST standards (US federal context). The CRA itself says "state of the art".
