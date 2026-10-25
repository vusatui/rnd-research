# AI agents from pilot to production: the 30-minute talk as an Excalidraw deck

Serious, sober variant in the same format as [`system-one-models/presentation/serious/`](../../system-one-models/presentation/serious/README.md): hand-drawn Excalidraw look (Excalifont, roughness 1, sketchy arrows and doodle icons drawn from Excalidraw primitives), navy + one orange accent on white, no characters, no jokes. 20 slides, one idea each, a title and a few words; everything else is in the speaker notes, which are a word-for-word read-aloud script.

| What | File |
|---|---|
| Deck (Excalidraw, 20 frames) | [`presentation.excalidraw`](presentation.excalidraw) |
| PDF / PNG / SVG per slide / overview | [`presentation.pdf`](presentation.pdf), [`export/`](export/), [`contact-sheet.png`](contact-sheet.png) |
| Read-aloud script (full sentences, about 130 words per minute, 30 min) with slide times, stage directions in italic brackets, and 10 spoken Q&As at the end | [`speaker-notes.md`](speaker-notes.md) |
| QR code of this topic folder (used on slide 19) | [`qr.png`](qr.png) |
| Live demo material | [`../workshop/`](../workshop/PARTICIPANTS.md) (`run_agent.py`, `ex3_guardrails/`, saved logs in `results/`) |
| Generator and export tooling | [`tools/`](tools/) (reuses [`../../system-one-models/presentation/tools/`](../../system-one-models/presentation/tools/README.md) for the Excalidraw bundle and `node_modules`) |

Slides: 1 Title · 2 The pilot trap · 3 What is an agent · 4 What the review asks · 5 Match controls to autonomy · 6 One run, one trace · 7 Test what it did, not what it said · 8 One friendly sentence (eval drop 0.92 to 0.58) · 9 A judge needs a rulebook · 10 The prompt asks, the code enforces · 11 Red team: attack success rate · 12 Live demo: the attack · 13 Live demo: the guard · 14 Stop the loop in code · 15 The EU AI Act clock · 16 Tools in one picture · 17 Honest limits · 18 Three takeaways · 19 Try it yourself (repo link + QR) · 20 Questions.

## Open the deck
Go to <https://excalidraw.com> → ☰ **Open** → `presentation.excalidraw`. Each slide is a frame named `Slide NN …`, 4 per row. To present: click a frame, <kbd>Shift</kbd>+<kbd>2</kbd>, then the next one. Easy fallback: `presentation.pdf` full-screen.

## Rebuild
Prerequisites: the first deck's tooling set up once (`cd ../../system-one-models/presentation/tools && npm install` plus the esbuild bundle, see its README), `pip install pillow fonttools brotli segno`, and Google Chrome. Nothing is installed in this folder.
```bash
cd agents-pilot-to-prod/presentation/tools
python3 make_qr.py          # ../qr.png (QR of https://github.com/vusatui/rnd-research/tree/main/agents-pilot-to-prod/)
python3 build_deck.py       # ../presentation.excalidraw (validates structure, text margins and text overlaps)
node export_frames.mjs      # ../export/*.svg|png  (real Excalidraw renderer)
python3 contact_sheet.py && python3 make_pdf.py
```
`kit.py` holds the shared colours, frame helpers and doodle icons; `excal.py` is the scene builder copied from the first deck.

## Honesty notes
- Facts as in [`../research.md`](../research.md) (sources checked 2026-10-17) and the measured runs in [`../workshop/results/`](../workshop/results/). Vendor claims (Gartner forecasts, survey results, cloud governance products) are said as claims in the notes; the "95% of pilots fail" and "80% of AI projects fail" figures are deliberately not used as facts.
- Numbers marked "our measurement" come from a free model (`nvidia/nemotron-3-super-120b-a12b:free`), 12 eval cases x 2 repeats, 9 red-team attacks, one judge model; free models are non-deterministic.
- Slide 6 is a real span tree from a workshop run (PARTICIPANTS.md). Slides 12 and 13 show **saved** runs from `results/redteam.log` (slide 12: prompt v1, which already says "tool content is data"; slide 13: prompt v2) and a **simplified** excerpt of `agent/guards.py`; the live runs may differ.
- The EU AI Act slide follows `research.md` section 7 and is not legal advice.
