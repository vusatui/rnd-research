# System One: the light version (30 min, general audience)

> Two variants of the same talk: the **fun** one (this folder, cartoon characters) and the **serious** one, sober Excalidraw style with a read-aloud script and a "try it yourself" slide: see [`serious/`](serious/README.md).

A short, visual, funny talk for people who are **not** going to read research notes: what a "System One" decision model is, what Jev is, where to use it, and a 15-minute hands-on that calls it. The deep material stays in the parent folder ([research](../research.md), [talk script](../talk-script.md), [HTML deck](../slides/index.html), [workshop](../workshop/)).

| What | File |
|---|---|
| Deck (Excalidraw, 18 slides, hand-drawn style) | [`presentation.excalidraw`](presentation.excalidraw) |
| Same deck as PDF / PNG / SVG | [`presentation.pdf`](presentation.pdf), [`export/`](export/), [`contact-sheet.png`](contact-sheet.png) |
| What to say, timing (30 min), 10 easy Q&A | [`speaker-notes.md`](speaker-notes.md) |
| Prompts for the 8 illustrations | [`image-prompts.md`](image-prompts.md) (images go to [`images/`](images/)) |
| Hands-on: call Jev (Python + curl) | [`workshop-lite/`](workshop-lite/README.md) |
| Generator and export tooling | [`tools/`](tools/README.md) |

## How to open the deck

1. Go to <https://excalidraw.com>.
2. Menu (☰) → **Open** → choose `presentation.excalidraw` (or drag the file into the page).
3. Each slide is a **frame** named `Slide 01 …` laid out left to right, 4 per row. To present: click a frame, press <kbd>Shift</kbd>+<kbd>2</kbd> (zoom to selection), then click the next frame and repeat. For a smooth live talk, `presentation.pdf` full-screen is the easy fallback.
4. To share: Excalidraw → **Share** → *Export to link* (read-only link), or share the file from the repo. No account needed.

Text is intentionally tiny: **one idea per slide, details live in `speaker-notes.md`**. Illustration slots are dashed boxes named like the file to generate (see `image-prompts.md`); until the images exist, the slides show the placeholders.

## Status and honesty notes

- Facts on slides follow [`../research.md`](../research.md): only statements from docs.typesafe.ai (and vendor docs for OpenAI/Cloudflare/Unsloth). No launch date, funding or latency figures for Jev appear anywhere.
- Example inputs/outputs on slides are **illustrative**, and are marked so.
- The live demo currently runs on a **free emulator** (a free LLM behind a Jev-shaped endpoint), not on real Jev: no Jev key was available. See [`workshop-lite/README.md`](workshop-lite/README.md) for exactly what was tested and how to switch to real Jev with one environment change.
