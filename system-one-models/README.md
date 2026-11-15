# System One models (decision models)

Jev and the new class of non-text-generating "System One" models, generalized to decision models in general (classifiers, rerankers, reward models, routers, guardrails) and the System 1 / System 2 split in AI systems.

- [`research.md`](research.md) - sources, verification status, key findings, open items; section 7 = our decision-model vs structured-output measurement
- [`comparison.md`](comparison.md) - Jev vs OpenAI Decisions vs Clef vs Laya vs d1; broader approaches
- [`talk-outline.md`](talk-outline.md) - ~35 min talk
- [`workshop/`](workshop/README.md) - 3 exercises + homework on one 250-ticket dataset and one eval harness; the measured comparison of Jev vs structured output + verbalized confidence; [`workshop/METHODOLOGY.md`](workshop/METHODOLOGY.md) says how we tested (older plan: [`workshop-plan.md`](workshop-plan.md))
- [`talk-script.md`](talk-script.md) - full English talk script (~35 min, 25 slides): on-slide content, speaker notes, timing, sources
- [`slides/index.html`](slides/index.html) - self-contained HTML deck (no external dependencies, 1920x1080, autoscale). Open it locally in a browser. Keys: →/Space next, ← back, `N` notes, `S` speaker window with timer, `O` overview, `F` fullscreen. Preview of all slides: [`slides/contact-sheet.png`](slides/contact-sheet.png). Speaker notes are generated from talk-script.md: `python3 slides/build_notes.py`
- **Run everything with Docker + make:** `cd system-one-models && make help` (`make ex1` / `make lite-jev` for Exercise 1, `make workshop` to replay Exercises 2-3 offline, `make ex2`/`eval`/`ex3` for live runs, `make test` for the offline smoke tests; see the workshop READMEs)
- [`presentation/`](presentation/) - **light 30-min version for a general audience**: Excalidraw deck (18 mostly-visual slides), speaker notes, image prompts, and a 15-min `workshop-lite` that calls Jev

Status: Draft (2026-10-10). Talk script and HTML slides: done (same style and tooling as `../sandboxes-and-remote-desktops/slides/`).
