# System One: the serious variant (30 min, technical audience)

Second variant of the light talk in [`../`](../README.md): same content base, **sober look** (navy + one orange accent, white background, no characters, no jokes), still hand-drawn Excalidraw style (Excalifont, roughness 1, sketchy arrows and doodle icons drawn from Excalidraw primitives). 24 slides, one idea each, a title and a few words; everything else is in the speaker notes, which are written as a word-for-word read-aloud script.

| What | File |
|---|---|
| **Presenter with the recorded demo (open this to present)** | [`present.html`](present.html) |
| Deck (Excalidraw, 24 frames) | [`presentation.excalidraw`](presentation.excalidraw) |
| Recorded demo clips (3 × mp4, 2560×1440, no audio; plan in [`demo/STORYBOARD.md`](demo/STORYBOARD.md)) and their reproducible source | [`demo/`](demo/README.md) |
| PDF / PNG / SVG per slide / overview | [`presentation.pdf`](presentation.pdf), [`export/`](export/), [`contact-sheet.png`](contact-sheet.png) |
| Read-aloud script (full sentences, about 130 words per minute, ~32 min incl. 2 min questions) with slide times, stage directions in italic brackets, and 11 spoken Q&As with our measured numbers | [`speaker-notes.md`](speaker-notes.md) |
| Demo code (request → response) | [`../workshop-lite/`](../workshop-lite/README.md) |
| Generator and export tooling | [`tools/`](tools/) (reuses [`../tools/`](../tools/README.md) for `excal.py`, the Excalidraw bundle and `node_modules`) |

Slides: 1 Title · 2 Two kinds of models · 3 Fast and slow · 4 What is Jev · 5 One call, one decision · 6 Three kinds of questions · 7 Not only Jev · 8 Where it fits · 9 Routing · 10 Fast first · **11-15 Why not structured output + confidence?** (11 The real alternative · 12 Where the number comes from · 13 How we tested · 14 Same 150 tickets · 15 What the numbers say) · 16 Demo: the request · 17-19 Recorded demo (1 One call · 2 Same tickets · 3 The threshold) · 20 Use it / skip it · 21 Honest limits · 22 Takeaways · 23 Try it yourself (repo link + QR) · 24 Questions.

## Present (nothing runs live)
Open [`present.html`](present.html) in Chrome (double-click, works offline from `file://`). It shows the exported slides and plays the recorded demo clips inside slides 17–19 (autoplay; K pauses, R restarts), so you only talk over them.

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
- Facts as in [`../../research.md`](../../research.md); no Jev launch dates, funding or vendor latency numbers. Model names on slides 14-15 are the ones we measured.
- Slides 5 and 9 are **illustrative**. Slides 13-15 and the demo clips use **our own measurement**: 150 held-out synthetic tickets, labels from two blind LLM annotators, method and caveats in [`../../workshop/METHODOLOGY.md`](../../workshop/METHODOLOGY.md); results in [`demo/runs/ex2-ex3-results.txt`](demo/runs/ex2-ex3-results.txt).
- Framing agreed for the talk: choose a decision model for price, speed and format plus decent probabilities, not for superior accuracy; measure confidence of any method on your own data.
- Demo 1 calls **real Jev via OpenRouter** ([recorded run](demo/runs/ex1-real-jev.txt)); nothing is fabricated.
