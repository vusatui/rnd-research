# Taming the AI bill (AI cost control / FinOps for AI): the 30-minute talk as an Excalidraw deck

Serious, sober variant in the same format as [`system-one-models/presentation/serious/`](../../system-one-models/presentation/serious/README.md): hand-drawn Excalidraw look (Excalifont, roughness 1, sketchy arrows and doodle icons drawn from Excalidraw primitives), navy + one orange accent on white, no characters, no jokes. 20 slides, one idea each, a title and a few words; everything else is in the speaker notes, which are a word-for-word read-aloud script.

| What | File |
|---|---|
| Deck (Excalidraw, 20 frames) | [`presentation.excalidraw`](presentation.excalidraw) |
| PDF / PNG / SVG per slide / overview | [`presentation.pdf`](presentation.pdf), [`export/`](export/), [`contact-sheet.png`](contact-sheet.png) |
| Read-aloud script (full sentences, about 130 words per minute, 30 min) with slide times, stage directions in italic brackets, and 10 spoken Q&As at the end | [`speaker-notes.md`](speaker-notes.md) |
| QR code of this topic folder (used on slide 19) | [`qr.png`](qr.png) |
| Live demo material | [`../workshop/`](../workshop/PARTICIPANTS.md) (`ex2_levers/run_levers.py --rescore`, `ex4_gateway/`, committed runs in `results/`) |
| Generator and export tooling | [`tools/`](tools/) (reuses [`../../system-one-models/presentation/tools/`](../../system-one-models/presentation/tools/README.md) for the Excalidraw bundle and `node_modules`) |

Slides: 1 Title · 2 Cheaper tokens, bigger bills · 3 Every step re-sends everything · 4 Easy-to-miss multipliers · 5 Cost per task, not per token · 6 FinOps for AI in three verbs · 7 Our test bench · 8 Say less, send less · 9 A smaller model · 10 A cascade needs a checker · 11 Prompt caching · 12 Similar is not the same · 13 One door for every call · 14 Live demo: the cost table · 15 Live demo: the $0 trap · 16 When does self-hosting pay · 17 Honest limits · 18 Three takeaways · 19 Try it yourself (repo link + QR) · 20 Questions.

## Open the deck
Go to <https://excalidraw.com> → ☰ **Open** → `presentation.excalidraw`. Each slide is a frame named `Slide NN …`, 4 per row. To present: click a frame, <kbd>Shift</kbd>+<kbd>2</kbd>, then the next one. Easy fallback: `presentation.pdf` full-screen.

## Rebuild
Prerequisites: the first deck's tooling set up once (`cd ../../system-one-models/presentation/tools && npm install` plus the esbuild bundle, see its README), `pip install pillow fonttools brotli segno`, and Google Chrome. Nothing is installed in this folder.
```bash
cd ai-finops/presentation/tools
python3 make_qr.py          # ../qr.png (QR of https://github.com/vusatui/rnd-research/tree/main/ai-finops/)
python3 build_deck.py       # ../presentation.excalidraw (validates structure, text margins and text overlaps)
node export_frames.mjs      # ../export/*.svg|png  (real Excalidraw renderer)
python3 contact_sheet.py && python3 make_pdf.py
```
`kit.py` holds the shared colours, frame helpers and doodle icons; `excal.py` is the scene builder copied from the first deck.

## Honesty notes
- Facts as in [`../research.md`](../research.md) (sources checked 2026-10-19) and the measured runs in [`../workshop/results/`](../workshop/results/). Surveys, expert interviews and analyst forecasts (Accenture, McKinsey, Gartner) are said as signals or forecasts in the notes, never as facts. Prices are "as read on 2026-10-19".
- Numbers marked "our measurement" are n=16 tickets, one run per configuration, free OpenRouter models priced at published list prices (shadow cost; the premium price card is $2/$10 per 1M tokens). A difference of 1-2 tickets is noise. Slide 2's curves are a labelled schematic sketch, not data.
- Slide 14 is a shortened excerpt of the committed re-score table; slide 15 shows the committed LiteLLM v1.106.0 result and config contrast from `workshop/PARTICIPANTS.md`. Prompt-cache numbers come from a free endpoint plus a simulation of the published paid rules. Slide 16 is arithmetic on stated assumptions (throughput is an assumption), not a benchmark.
- The cost-per-successful-task figures on slide 5 ($0.0125 / $0.0143 / $1,250) are the baseline row of the workshop tables; the dollars per month figure is cost per task x 100k tickets.
