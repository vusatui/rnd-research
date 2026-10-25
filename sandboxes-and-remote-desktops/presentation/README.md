# Sandboxes for AI agents: serious Excalidraw deck (30 min, general internal audience)

Same format and look as [`system-one-models/presentation/serious/`](../../system-one-models/presentation/serious/README.md): **hand-drawn Excalidraw style** (Excalifont, roughness 1, sketchy arrows and doodle icons drawn from Excalidraw primitives), navy + one orange accent on white, no characters, no jokes. 20 slides, one idea each, a title and a few words; everything else is in the speaker notes, written as a word-for-word read-aloud script.

| What | File |
|---|---|
| Deck (Excalidraw, 20 frames) | [`presentation.excalidraw`](presentation.excalidraw) |
| PDF / PNG / SVG per slide / overview | [`presentation.pdf`](presentation.pdf), [`export/`](export/), [`contact-sheet.png`](contact-sheet.png) |
| Read-aloud script (full sentences, about 130 words per minute, 30 min) with slide times, stage directions in italic brackets, and 10 spoken Q&As at the end | [`speaker-notes.md`](speaker-notes.md) |
| Live demo code (ex2 locked-down Docker sandbox, ex4 desktop agent) | [`../workshop/`](../workshop/ex2_llm_loop/agent.py), screenshots in [`../assets/`](../assets/) |
| QR code of the topic folder | [`qr.png`](qr.png) |
| Generator and export tooling | [`tools/`](tools/) (reuses `node_modules` and the Excalidraw bundle of [`../../system-one-models/presentation/tools/`](../../system-one-models/presentation/tools/README.md)) |

Slides: 1 Title · 2 Agents do not only talk · 3 When an agent gets it wrong (Replit) · 4 Hidden instructions · 5 Three ingredients of a leak · 6 What is a sandbox · 7 The isolation ladder · 8 Pick by trust · 9 A screen for the agent · 10 See, think, act · 11 Same job, different walls · 12 Measure the cold start · 13 Live demo: the setup · 14 Live demo: the result · 15 Live demo: a desktop agent · 16 Honest limits · 17 Production checklist · 18 Three takeaways · 19 Try it yourself (repo link + QR) · 20 Questions.

## Open the deck
Go to <https://excalidraw.com> → ☰ **Open** → `presentation.excalidraw`. Each slide is a frame named `Slide NN …`, 4 per row. To present: click a frame, <kbd>Shift</kbd>+<kbd>2</kbd>, then the next one. Easy fallback: `presentation.pdf` full-screen.

## Rebuild
Prerequisites: the setup of `system-one-models/presentation/tools/` (`npm install`, esbuild bundle, `pip install pillow fonttools brotli`), Google Chrome, and `pip install segno` for the QR. Override the shared tools location with `EXCAL_TOOLS=/path/to/tools`.
```bash
cd sandboxes-and-remote-desktops/presentation/tools
python3 make_qr.py          # ../qr.png (QR of https://github.com/vusatui/rnd-research/tree/main/sandboxes-and-remote-desktops/)
python3 build_deck.py       # ../presentation.excalidraw (validates the JSON structure)
node export_frames.mjs      # ../export/*.svg|png  (real Excalidraw renderer)
python3 contact_sheet.py && python3 make_pdf.py
```
`kit.py` holds the palette, frame/title helpers and the doodle icons (copied unchanged from the first deck); `excal.py` is the scene builder and validator.

## Honesty notes
- Facts as in [`../research.md`](../research.md), [`../comparison.md`](../comparison.md) and [`../verification-notes.md`](../verification-notes.md) (the latter wins over older text). Vendor cold-start numbers and the unverified items (E2B fork "20 copies", isolation of Cursor/Devin/Copilot agents, Runloop/Morph/Kasm details, generic gVisor/Kata descriptions) are called out as claims or unverified in the notes.
- Slide 12 shows **our own measurement** ([`../benchmarks.md`](../benchmarks.md), 5 runs, median until the first command, 2026-10-10). Slides 14 and 15 show **recorded runs** from 2026-10-10 with free OpenRouter models on the local Docker backend (not E2B); the screenshots are the real ones from `../assets/`.
- Slides 5, 8 and 11 are simplified diagrams, not measurements.
