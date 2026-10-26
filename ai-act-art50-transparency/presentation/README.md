# Telling people it's AI (EU AI Act Art. 50 transparency): the 30-minute talk as an Excalidraw deck

> General information, not legal advice. See [`../research.md`](../research.md).

Serious, sober deck in the same format as [`ai-finops/presentation/`](../../ai-finops/presentation/README.md) and [`system-one-models/presentation/serious/`](../../system-one-models/presentation/serious/README.md): hand-drawn Excalidraw look (Excalifont, roughness 1, sketchy arrows and doodle icons drawn from Excalidraw primitives), navy + one orange accent on white, no characters, no jokes. 20 slides, one idea each, a title and a few words; everything else is in the speaker notes, which are a word-for-word read-aloud script. Audience: a general internal audience (average developer or user).

| What | File |
|---|---|
| Deck (Excalidraw, 20 frames) | [`presentation.excalidraw`](presentation.excalidraw) |
| PDF / PNG / SVG per slide / overview | [`presentation.pdf`](presentation.pdf), [`export/`](export/), [`contact-sheet.png`](contact-sheet.png) |
| Read-aloud script (full sentences, about 130 words per minute, 30 min) with slide times, a few italic stage directions, and 10 spoken Q&As at the end | [`speaker-notes.md`](speaker-notes.md) (same text as [`../talk-script.md`](../talk-script.md)) |
| QR code of this topic folder (used on slide 19) | [`qr.png`](qr.png) |
| Demo material (recorded runs, shortened) | [`../workshop/`](../workshop/README.md): `ex1_disclosure/audit.py` (offline, reads the committed run), `ex2_c2pa/survival.py` (offline, ~10 s), committed runs in `results/` |
| Generator and export tooling | [`tools/`](tools/) (reuses [`../../system-one-models/presentation/tools/`](../../system-one-models/presentation/tools/README.md) for the Excalidraw bundle and `node_modules`) |

Slides: 1 Title · 2 Read this first (not legal advice) · 3 "Are you a real person?" · 4 Four duties · 5 Provider builds, deployer uses · 6 The dates · 7 Too vague to count · 8 Disclosure belongs to the system · 9 Two layers is the baseline · 10 The marking toolbox · 11 C2PA: signed, then lost · 12 Where the watermark breaks · 13 Fingerprint: a lookup · 14 Four of eleven beat all three · 15 Text is the hard one · 16 Recorded run: the chatbot · 17 Recorded run: the survival table · 18 Honest limits · 19 Try it yourself (repo link + QR) · 20 Questions.

## Open the deck
Go to <https://excalidraw.com> → ☰ **Open** → `presentation.excalidraw`. Each slide is a frame named `Slide NN …`, 4 per row. To present: click a frame, <kbd>Shift</kbd>+<kbd>2</kbd>, then the next one. Easy fallback: `presentation.pdf` full-screen.

## Rebuild
Prerequisites: the first deck's tooling set up once (`cd ../../system-one-models/presentation/tools && npm install` plus the esbuild bundle, see its README), `pip install pillow fonttools brotli segno`, and Google Chrome. Nothing is installed in this folder.
```bash
cd ai-act-art50-transparency/presentation/tools
python3 make_qr.py          # ../qr.png (QR of https://github.com/vusatui/rnd-research/tree/main/ai-act-art50-transparency/)
python3 build_deck.py       # ../presentation.excalidraw (validates structure, text margins and text overlaps)
node export_frames.mjs      # ../export/*.svg|png  (real Excalidraw renderer)
python3 contact_sheet.py && python3 make_pdf.py
```
`kit.py` holds the shared colours, frame helpers and doodle icons; `excal.py` is the scene builder copied from the first deck; `build_deck.py` has the slides and a few local doodles (chat bubble, scales, registry cylinder).

## Honesty notes
- Facts as in [`../research.md`](../research.md) and [`../comparison.md`](../comparison.md) (as of 2026-10-26), with their markers: items the research marks 🟠 (Commission/AI Board adequacy dates, the law-firm memo about 2 Feb 2027, the OpenAI help page) or ❌ (new versions of legacy systems, the official Code PDF) are said as secondary or open in the notes, never as verified facts.
- Numbers marked "our measurement" or "recorded run" come from [`../workshop/results/`](../workshop/results/): 3 procedurally generated images with open stand-ins (DWT-DCT-SVD watermark, 256-bit dHash, a throw-away test CA), 12 texts on a 360M local model, and 20 identity questions to one free chat model (`nvidia/nemotron-3.5-lightning:free`), all read by hand for slide 16. They show mechanisms and failure modes, not the performance of any vendor product.
- Slide 16 is the manual-label audit of the committed run (`ex1_audit.json`); the "20/20*" row is in-sample, and the fresh-probe figure (7 of 13) is the research's. Slide 17 is a shortened excerpt of `ex2_survival_2026-10-26.md` (6 of its 15 rows). Slide 14 combines the 11 non-C2PA transformations of that table.
- Slide 8's "0 of 10 / 10 of 10" compares honest-prompt first replies with the app-owned notice, which is 10/10 by construction, not an empirical result.
- The two layers, the 200-token text rule, the 2 Dec 2026 grace period and the 2 Feb 2027 Code date are stated as in the research; the 2 Feb 2027 date is the Code's voluntary Measure 3.4(c), not an Omnibus date.
