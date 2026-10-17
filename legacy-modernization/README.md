# AI-assisted legacy modernization (COBOL, mainframe, old Java/.NET)

Why clients (banks, insurers, government, retail) are asking for AI-led modernization now, what AWS / IBM / Google /
Microsoft / specialists actually offer, where LLMs help and where they silently break behaviour, and a runnable workshop
that modernizes a real mainframe batch job (AWS CardDemo `CBACT04C`) and **proves** equivalence against the running COBOL.

- [`research.md`](research.md) - sources (checked 2026-10-17) with ✅/🟡/🟠/❌/🧪 markers, key findings, open items
- [`comparison.md`](comparison.md) - AWS Transform, IBM Bob for Z / watsonx Code Assistant for Z, Google MAT + Dual Run,
  Microsoft agents, Mechanical Orchard, deterministic converters, OpenRewrite/Moderne; pricing, languages, self-hosting
- [`talk-outline.md`](talk-outline.md) - ~35 min talk
- [`talk-script.md`](talk-script.md) - full English talk script (~35 min, 24 slides): on-slide content, speaker notes, timing, sources, plus likely audience questions & answers
- [`slides/index.html`](slides/index.html) - self-contained HTML deck (no external dependencies, 1920x1080, autoscale). Open it locally in a browser. Keys: →/Space next, ← back, `N` notes, `S` speaker window with timer, `O` overview, `F` fullscreen. Preview of all slides: [`slides/contact-sheet.png`](slides/contact-sheet.png). Speaker notes are generated from talk-script.md: `python3 slides/build_notes.py`; open with `?check` for an overflow report
- [`workshop-plan.md`](workshop-plan.md) + [`workshop/`](workshop/) - 4 exercises, all free (GnuCOBOL + free OpenRouter models), with real run results
- [`workshop/PARTICIPANTS.md`](workshop/PARTICIPANTS.md) - participant guide: prerequisites, setup, per-exercise commands, expected output, troubleshooting, stretch tasks (verified from a clean clone)

Quick start:

```bash
cd workshop
./setup.sh                      # fetches AWS CardDemo (Apache-2.0) at a pinned commit, checks GnuCOBOL
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
./legacy/build.sh               # compiles the untouched COBOL with GnuCOBOL
python -m pytest -q tests       # offline checks, no LLM
python ex4_equivalence/diamond.py   # reference implementation vs running COBOL: 25/25 equivalent
export OPENROUTER_API_KEY=...   # free key, then ex2/ex3 (see workshop-plan.md)
```

Status: Done (2026-10-17). Research, comparison, talk outline, workshop, participant guide, talk script and HTML slides done (same style and tooling as `../system-one-models/slides/` and `../sandboxes-and-remote-desktops/slides/`).
