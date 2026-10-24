# System One: the serious variant (30 min, technical audience)

Second variant of the light talk in [`../`](../README.md): same content base, **sober look** (navy + one orange accent, white background, no characters, no jokes), still hand-drawn Excalidraw style (Excalifont, roughness 1, sketchy arrows and doodle icons drawn from Excalidraw primitives). 19 slides, one idea each, a title and a few words; everything else is in the speaker notes, which are written as a word-for-word read-aloud script.

| What | File |
|---|---|
| Deck (Excalidraw, 19 frames) | [`presentation.excalidraw`](presentation.excalidraw) |
| PDF / PNG / SVG per slide / overview | [`presentation.pdf`](presentation.pdf), [`export/`](export/), [`contact-sheet.png`](contact-sheet.png) |
| Read-aloud script (full sentences, about 130 words per minute, 30 min) with slide times, stage directions in italic brackets, and 10 spoken Q&As at the end | [`speaker-notes.md`](speaker-notes.md) |
| Live demo code (request → response) | [`../workshop-lite/`](../workshop-lite/README.md) |
| Generator and export tooling | [`tools/`](tools/) (reuses [`../tools/`](../tools/README.md) for `excal.py`, the Excalidraw bundle and `node_modules`) |

Slides: 1 Title · 2 Two kinds of models · 3 Fast and slow · 4 What is Jev · 5 One call, one decision · 6 Three kinds of questions · 7 Not only Jev · 8 Where it fits · 9 Routing · 10 Moderation · 11 Fraud triage · 12 Fast first · 13 Live demo: request · 14 Live demo: response · 15 Use it / skip it · 16 Honest limits · 17 Takeaways · 18 Try it yourself (repo link + QR) · 19 Questions.

## Open the deck
Go to <https://excalidraw.com> → ☰ **Open** → `presentation.excalidraw`. Each slide is a frame named `Slide NN …`, 4 per row. To present: click a frame, <kbd>Shift</kbd>+<kbd>2</kbd>, then the next one. Easy fallback: `presentation.pdf` full-screen.

## Rebuild
Prerequisites: the `../tools/` setup (`npm install`, esbuild bundle, `pip install pillow fonttools brotli`), Google Chrome, and `pip install segno` for the QR.
```bash
cd system-one-models/presentation/serious/tools
python3 make_qr.py          # ../qr.png (QR of https://github.com/vusatui/rnd-research)
python3 build_deck.py       # ../presentation.excalidraw
node export_frames.mjs      # ../export/*.svg|png  (real Excalidraw renderer)
python3 contact_sheet.py && python3 make_pdf.py
```

## Honesty notes
- Facts as in [`../../research.md`](../../research.md); no Jev launch dates, funding or latency numbers; no model versions on slides.
- Slides 5, 9, 10, 11 are **illustrative**; slide 14 shows a saved run of the **local emulator** (not Jev). No real Jev answer was obtained (no key available); nothing is fabricated.
