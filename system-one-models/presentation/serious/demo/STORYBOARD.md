# Demo storyboard v5: two clips, one per exercise (approved 2026-11-15, rendered; slowed to 0.5× and clip 3 dropped 2026-11-16)

Deck slots: slides 17-18 of the serious deck (`present.html`). Narration = the read-aloud notes of those slides in [`../speaker-notes.md`](../speaker-notes.md) (single source). The timings below are those of the original render; the clips in `videos/` play at half speed, so every time doubles (clip 1 4:04, clip 2 2:22), and the timestamps in the notes are already doubled. All numbers are from real recorded runs on 2026-11-15 (UTC+3):
[`runs/ex1-real-jev.txt`](runs/ex1-real-jev.txt) (real Jev via OpenRouter) and [`runs/ex2-ex3-results.txt`](runs/ex2-ex3-results.txt) (`eval.py --ci --reliability`, `economics.py`). Method: [`../../../workshop/METHODOLOGY.md`](../../../workshop/METHODOLOGY.md).

Every clip follows the same arc:
**1 Problem → 2 Solution design (architecture card) → 3 Why this design → 4 Key code (zooms) → 5 Run → result → 6 Alternatives: where it wins, where it loses.**

Visual language (unchanged from v3): editor + terminal replay of the real files and real recorded output (Remotion, eased zooms/pans, typed commands zoomed on the prompt); white hand-drawn concept cards in the deck style (Excalifont, navy/slate + one orange accent). The architecture card has five boxes: **request → prompt / options → scoring → decision (thresholds) → next action**, each with one line on what it is responsible for; the box under discussion turns orange during the code walk.

| Clip | Slide | Exercise | Code | Run | Length |
|---|---|---|---|---|---|
| 1 One call | 17 | Ex1: one request, several questions, code decides | `presentation/workshop-lite/jev_client.py` | `make lite-jev` (real Jev) | 2:02 |
| 2 Same tickets | 18 | Ex2: written vs computed confidence | `workshop/ex2_confidence/methods.py` | `make -s eval \| grep -E '^(Question\|method\|E jev\|A verbal)'` (re-score saved results, offline) | 1:11 (2:22 at half speed) |

Total 3:49 as rendered, 7:38 at half speed. No emulator on screen except as a one-line mention: the runs are real Jev and saved real results.

---

## Clip 1 · One call (Ex1) · 2:02

| # | sec | On screen | Camera / card |
|---|---|---|---|
| 1 Problem | 0-10 | Card: "API failing for 20 min. Which team? Wake someone up?" + a comment and an expense below, greyed | static card |
| 2 Design | 10-30 | Architecture card: request (`ask()`: state + 2 questions, ONE call) → options (`criteria` in plain words) → scoring (Jev: a probability for every option) → decision (thresholds per action) → next action (route / page / review / escalate) | boxes light up left to right |
| 3 Why | 30-38 | Card: "One call, all questions · every option scored · code owns the thresholds" | — |
| 4 Code | 38-75 | `jev_client.py`: l.26-29 `ask()` one POST to `/v1/systemone` → l.65-69 questions (choice with criteria + noul) → l.51-58 `p_of()` and `noul_band()` (0.7 / 0.3, band = own outcome) → l.71-72 route/page → l.85-86 `block ≥ 0.9` → l.99 approve needs ≥ 0.9 and within policy | eased zoom per block; matching architecture box orange in a corner inset |
| 5 Run | 75-105 | type `make -s lite-jev` (zoom on prompt) → ticket: `technical` p=1, urgent 0.99, 255 ms, $0.000016 → comment: `block` 0.92 → BLOCK → expense: `approve` 0.67 → ESCALATE | zoom on each `CODE decides` line; side-by-side card "same thresholds, three outcomes" |
| 6 Alternatives | 105-120 | Card, two columns. **Structured output from a chat LLM:** works, one generated answer per call, one written number, output tokens billed. **Keyword rules:** free, instant, brittle, no uncertainty. **Jev wins:** one call for all questions, distribution, ~150 ms, input-only price. **Loses:** no text, no explanations; probabilities still need checking (the expense case: 0.67 for an obvious approve) | static |

Numbers: from the re-recorded real runs `runs/jev-ticket.json`, `jev-comment.json`, `jev-approval.json` (2026-11-15 21:20 UTC+3): ticket 255 ms, comment block p=0.92, expense approve p=0.67 (earlier runs: 0.91-0.93 and 0.68-0.70, see `runs/ex1-real-jev.txt`). The three runs cost ~$0.00005.

## Clip 2 · Same tickets (Ex2) · 1:11 (v5, re-rendered 2026-11-16)

Simplified to the talk's core story: Jev (computed probability) vs chat LLMs asked for a written confidence in structured output. Token logprobs, 5 votes and the TF-IDF classifier are no longer on screen (they are in the Q&A of the speaker notes, with their numbers). Times below are at 1×; the delivered clip is slowed to 0.5×.

| # | sec | On screen | Camera / card |
|---|---|---|---|
| 1 Problem | 0-6 | Card: "Why not structured output + a confidence field? Is a decision model any better? Measure it on the same tickets." | — |
| 2 Design | 6-18 | Architecture card: 150 tickets (held out, blind labels) → 2 kinds (written: chat LLM, structured output · computed: Jev) → `eval.py` (accuracy · latency · $ per 1,000) → compare | boxes light up |
| 4 Code | 18-40 | `methods.py`: l.43-48 `VERBAL_SCHEMA` (label + `*_confidence`) → l.52-56 the prompt → l.160-168 Jev (one `systemone` call, both questions) | zoom per block |
| 5 Run | 40-58 | type `make -s eval \| grep -E '^(Question\|method\|E jev\|A verbal)'` (real run, `runs/eval-written.json`, 2026-11-16 20:59 UTC+3; same numbers as `runs/eval.json`) → Jev row: 93% · 161 ms · $0.025/1k → the four written rows: 92–95% · 540 ms–2.1 s · $0.046–$2.00/1k | zoom on the Jev row, then the four written rows |
| 6 Summary | 58-71 | Table card, same as slide 14: Jev computed 93% · 0.16 s · $0.025; GPT-6 Sol written 93% · 2.1 s · $1.34; Claude Sonnet 94% · 1.0 s · $2.00; Claude Haiku 92% · 0.8 s · $0.10; DeepSeek Flash 95% · 0.5 s · $0.046. Foot: ~54–80× cheaper, 6–13× faster than the strong LLMs, same accuracy within the noise; urgency Jev 78% vs 82–86%; not more accurate | static |

Rendered: Remotion at 2880×1620 (CRF 16) → ffmpeg `setpts=2.0*PTS`, lanczos to 2560×1440, CRF 18, 30 fps → `videos/demo-2-same-tickets.mp4` (2:22); poster at 2:12 (the table card).

## Claims checklist (all on screen numbers)

- ✅ request shape, `criteria`, noul 0.7/0.3 band, probability-routing, confidence formulas: docs.typesafe.ai (confidence, probability-routing, API reference), checked 2026-11-15.
- ✅ price $0.042 / 1M input tokens, output free: docs Models page; matches OpenRouter `usage.cost` in our runs.
- ✅ all ex2 numbers (and the ex3 numbers quoted on slide 10): `runs/ex2-ex3-results.txt` (bootstrap CIs inside).
- ⚠ synthetic data, LLM-consensus labels, n=150; one run per method; latency through OpenRouter from one place.
- 🟡 "trained for calibration" is the vendor's claim; our measurement shows comparable, not superior, calibration.

## How it was rendered (2026-11-15)

1. Runs re-recorded with `capture/capture.py` → `runs/jev-ticket|jev-comment|jev-approval|eval|eval-urgency|ex3.json` (only the three `lite-jev` runs called a paid API; eval/ex3 re-score the committed results).
2. `capture/build_data.py` packs the real files (`jev_client.py`, `methods.py`, `eval.py`, `economics.py`) and the runs; waits longer than 1 s between output lines (Docker start-up) are shortened, the programs' own latency numbers are untouched.
3. The local Remotion project (not in the repo) renders the 1920×1080 stage at 4K and downsamples to 2560×1440 H.264 → `videos/demo-1-one-call.mp4`, `demo-2-same-tickets.mp4` + posters (a third clip, `demo-3-threshold`, was rendered and later dropped from the deck); every number on a card or caption is parsed from the runs.
4. `tools/build_deck.py && node tools/export_frames.mjs && python3 tools/make_presenter.py` put the posters into slides 17-18 and the clips into `present.html` (native player).
5. 2026-11-16: both clips slowed to 0.5× with ffmpeg (`setpts=2.0*PTS`, 30 fps, CRF 18, 2560×1440 kept, posters unchanged).
6. 2026-11-16: clip 2 re-rendered (v5, simplified to Jev vs written confidence) from a new real run `runs/eval-written.json`, then slowed to 0.5×.
