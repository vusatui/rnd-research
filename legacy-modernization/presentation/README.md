# AI and legacy code: serious Excalidraw deck (30 min, general internal audience)

Same format and look as [`system-one-models/presentation/serious/`](../../system-one-models/presentation/serious/README.md): **hand-drawn Excalidraw style** (Excalifont, roughness 1, sketchy arrows and doodle icons drawn from Excalidraw primitives), navy + one orange accent on white, no characters, no jokes. 20 slides, one idea each, a title and a few words; everything else is in the speaker notes, written as a word-for-word read-aloud script.

| What | File |
|---|---|
| Deck (Excalidraw, 20 frames) | [`presentation.excalidraw`](presentation.excalidraw) |
| PDF / PNG / SVG per slide / overview | [`presentation.pdf`](presentation.pdf), [`export/`](export/), [`contact-sheet.png`](contact-sheet.png) |
| Read-aloud script (full sentences, about 130 words per minute, 30 min) with slide times, stage directions in italic brackets, and 10 spoken Q&As at the end | [`speaker-notes.md`](speaker-notes.md) |
| Live demo code (ex4 diamond equivalence on AWS CardDemo CBACT04C) | [`../workshop/`](../workshop/PARTICIPANTS.md) |
| QR code of the topic folder | [`qr.png`](qr.png) |
| Generator and export tooling | [`tools/`](tools/) (reuses `node_modules` and the Excalidraw bundle of [`../../system-one-models/presentation/tools/`](../../system-one-models/presentation/tools/README.md)) |

Slides: 1 Title · 2 Translation is getting cheap · 3 A program is not the system · 4 Few know the dependencies · 5 Two schools · 6 Better readers than writers · 7 Where it breaks · 8 One missing word · 9 The forgotten last account · 10 The diamond · 11 Live demo: the reference · 12 Live demo: a wrong candidate · 13 Reading rules with a model · 14 Cited, and still wrong · 15 Three ways to generate · 16 Who sells what · 17 Honest limits · 18 Three takeaways · 19 Try it yourself (repo link + QR) · 20 Questions.

## Open the deck
Go to <https://excalidraw.com> → ☰ **Open** → `presentation.excalidraw`. Each slide is a frame named `Slide NN …`, 4 per row. To present: click a frame, <kbd>Shift</kbd>+<kbd>2</kbd>, then the next one. Easy fallback: `presentation.pdf` full-screen.

## Rebuild
Prerequisites: the setup of `system-one-models/presentation/tools/` (`npm install`, esbuild bundle, `pip install pillow fonttools brotli`), Google Chrome, and `pip install segno` for the QR. Override the shared tools location with `EXCAL_TOOLS=/path/to/tools`.
```bash
cd legacy-modernization/presentation/tools
python3 make_qr.py          # ../qr.png (QR of https://github.com/vusatui/rnd-research/tree/main/legacy-modernization/)
python3 build_deck.py       # ../presentation.excalidraw (validates the JSON structure)
node export_frames.mjs      # ../export/*.svg|png  (real Excalidraw renderer)
python3 contact_sheet.py && python3 make_pdf.py
```
`kit.py` holds the palette, frame/title helpers and the doodle icons (copied unchanged from the first deck); `excal.py` is the scene builder and validator.

## Honesty notes
- Facts as in [`../research.md`](../research.md), [`../comparison.md`](../comparison.md) and [`../workshop-plan.md`](../workshop-plan.md) (sources checked 2026-10-17). Vendor statements, productivity numbers and secondary-only items (IBM share drop, GAO) are called out as claims or secondary in the notes; we did not run any vendor product.
- Slides 8, 9, 13, 14, 15 show **our own measurements** (GnuCOBOL 3.2, CardDemo, free OpenRouter models with reasoning off, few runs). Slide 15 also states the later clean-clone re-run that scored 2/25 (one wrong character).
- Slides 11 and 12 show **recorded, shortened/simplified** output of `ex4_equivalence/diamond.py` (copied from the participant guide and the talk script), not a fresh run: GnuCOBOL is not installed on the build machine.
