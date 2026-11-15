# System One: the serious variant (30 min, technical audience)

Second variant of the light talk in [`../`](../README.md): same content base, **sober look** (navy + one orange accent, white background, no characters, no jokes), still hand-drawn Excalidraw style (Excalifont, roughness 1, sketchy arrows and doodle icons drawn from Excalidraw primitives). 22 slides, one idea each, a title and a few words; everything else is in the speaker notes, which are written as a word-for-word read-aloud script.

| What | File |
|---|---|
| **Presenter with the recorded demo (open this to present)** | [`present.html`](present.html) |
| Deck (Excalidraw, 22 frames) | [`presentation.excalidraw`](presentation.excalidraw) |
| Recorded demo clips (4 × mp4, no audio) and their reproducible source | [`demo/`](demo/README.md) |
| PDF / PNG / SVG per slide / overview | [`presentation.pdf`](presentation.pdf), [`export/`](export/), [`contact-sheet.png`](contact-sheet.png) |
| Read-aloud script (full sentences, about 130 words per minute, 30 min) with slide times, stage directions in italic brackets, and 10 spoken Q&As at the end | [`speaker-notes.md`](speaker-notes.md) |
| Demo code (request → response) | [`../workshop-lite/`](../workshop-lite/README.md) |
| Generator and export tooling | [`tools/`](tools/) (reuses [`../tools/`](../tools/README.md) for `excal.py`, the Excalidraw bundle and `node_modules`) |

Slides: 1 Title · 2 Two kinds of models · 3 Fast and slow · 4 What is Jev · 5 One call, one decision · 6 Three kinds of questions · 7 Not only Jev · 8 Where it fits · 9 Routing · 10 Moderation · 11 Fraud triage · 12 Fast first · 13 Demo: the request · 14–17 Recorded demo (1 The files · 2 The code · 3 Run it · 4 The threshold) · 18 Use it / skip it · 19 Honest limits · 20 Takeaways · 21 Try it yourself (repo link + QR) · 22 Questions.

## Present (nothing runs live)
Open [`present.html`](present.html) in Chrome (double-click, works offline from `file://`). It shows the exported slides and plays the recorded demo clips inside slides 14–17, so you only talk over them.

| Key | Action |
|---|---|
| → / Space / PageDown, ← / PageUp | next / previous slide (clickers work) |
| K, Enter, `.`, B, or click the video | pause / play the clip |
| R · `[` `]` | restart the clip · slower / faster (0.75×, 1×, 1.25×) |
| N · F | speaker notes panel · fullscreen |

The clips start by themselves when you reach the slide and rewind when you leave it. Keep the folder structure (`export/`, `demo/videos/`) next to `present.html`.

## Open the deck in Excalidraw
Go to <https://excalidraw.com> → ☰ **Open** → `presentation.excalidraw`. Each slide is a frame named `Slide NN …`, 4 per row. To present: click a frame, <kbd>Shift</kbd>+<kbd>2</kbd>, then the next one. Easy fallback: `presentation.pdf` full-screen.

## Rebuild
Prerequisites: the `../tools/` setup (`npm install`, esbuild bundle, `pip install pillow fonttools brotli`), Google Chrome, and `pip install segno` for the QR.
```bash
cd system-one-models/presentation/serious/tools
python3 make_qr.py          # ../qr.png (QR of https://github.com/vusatui/rnd-research)
python3 build_deck.py       # ../presentation.excalidraw
node export_frames.mjs      # ../export/*.svg|png  (real Excalidraw renderer)
python3 contact_sheet.py && python3 make_pdf.py
python3 make_presenter.py   # ../present.html (slides + demo clips + notes)
```
The demo clips have their own pipeline (real runs → Remotion → mp4), see [`demo/README.md`](demo/README.md). Render them before `build_deck.py` so the demo slides get their posters and lengths.

## Honesty notes
- Facts as in [`../../research.md`](../../research.md); no Jev launch dates, funding or latency numbers; no model versions on slides.
- Slides 5, 9, 10, 11 are **illustrative**; the demo clips (slides 14–17) replay a recorded run of the **local emulator** (not Jev). No real Jev answer was obtained (no key available); nothing is fabricated.
