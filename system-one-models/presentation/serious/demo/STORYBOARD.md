# Demo storyboard v4: three clips, one per exercise (approved 2026-11-15, rendered)

Deck slots: slides 17-19 of the serious deck (`present.html`). Narration = the read-aloud notes of those slides in [`../speaker-notes.md`](../speaker-notes.md) (single source; the clip timing below follows them). All numbers are from real recorded runs on 2026-11-15 (UTC+3):
[`runs/ex1-real-jev.txt`](runs/ex1-real-jev.txt) (real Jev via OpenRouter) and [`runs/ex2-ex3-results.txt`](runs/ex2-ex3-results.txt) (`eval.py --ci --reliability`, `economics.py`). Method: [`../../../workshop/METHODOLOGY.md`](../../../workshop/METHODOLOGY.md).

Every clip follows the same arc:
**1 Problem → 2 Solution design (architecture card) → 3 Why this design → 4 Key code (zooms) → 5 Run → result → 6 Alternatives: where it wins, where it loses.**

Visual language (unchanged from v3): editor + terminal replay of the real files and real recorded output (Remotion, eased zooms/pans, typed commands zoomed on the prompt); white hand-drawn concept cards in the deck style (Excalifont, navy/slate + one orange accent). The architecture card has five boxes: **request → prompt / options → scoring → decision (thresholds) → next action**, each with one line on what it is responsible for; the box under discussion turns orange during the code walk.

| Clip | Slide | Exercise | Code | Run | Length |
|---|---|---|---|---|---|
| 1 One call | 17 | Ex1: one request, several questions, code decides | `presentation/workshop-lite/jev_client.py` | `make lite-jev` (real Jev) | 2:02 |
| 2 Same tickets | 18 | Ex2: verbalized vs computed confidence | `workshop/ex2_confidence/methods.py`, `workshop/eval.py` | `make eval`, `make eval QUESTION=urgency` (re-score saved results, offline) | 1:47 |
| 3 The threshold | 19 | Ex3: fast-first economics | `workshop/ex3_fast_first/economics.py` | `make ex3` | 1:13 |

Total 5:02 (rendered). No emulator on screen except as a one-line mention: the runs are real Jev and saved real results.

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

## Clip 2 · Same tickets (Ex2) · 1:47

| # | sec | On screen | Camera / card |
|---|---|---|---|
| 1 Problem | 0-8 | Card: "Why not structured output + a confidence field?" | — |
| 2 Design | 8-25 | Architecture card: request = 150 held-out tickets, same option text → five scorers (A written confidence · B token logprobs · C 5 votes · D classifier · E Jev) → `eval.py` (accuracy, ECE, reliability, auto@95/98, distinct values, latency, $) → decision = which confidence you may threshold | scorer boxes fan out |
| 3 Why | 25-32 | Card: "Same tickets, same options, same metrics: only the source of the number differs" | — |
| 4 Code | 32-62 | `methods.py`: l.43-51 `VERBAL_SCHEMA` (label + `*_confidence`) → l.87-92 logprobs (`top_logprobs=20`) → l.116-121 votes (k=5, temperature 1) → l.160-164 Jev (one `systemone` call, both questions) → `eval.py` l.26 `ece()` and l.49 `coverage_at()` | zoom per function; label chip A/B/C/E |
| 5 Run | 62-90 | type `make eval` (then `make eval QUESTION=urgency`) → table (department): Jev 93% · ECE 0.042 · 35 values · 161 ms · $0.025/1k; gpt-6-sol 93% · 0.039 · 19 · 2,108 ms · $1.34; sonnet-5.5 94% · 0.113 · 17 · 1,020 ms · $2.00; deepseek verbal 95% · 0.067 · 12 · 540 ms · $0.046; votes 97% · 0.024 · 3 values → reliability (urgency): logprobs "said 0.98, right 65%"; gpt-6-sol "said 0.99, right 100%" (department) | zoom on the Jev row, then the two strong rows, then the logprobs reliability line (orange underline) |
| 6 Alternatives | 90-105 | Card: **Jev wins** on price (50-80× cheaper than strong LLMs), speed (6-13×), format (one call, every option). **Ties** on accuracy and calibration on department (differences within the 95% CIs). **Loses** on the subjective urgency question (−4 vs strong models, n.s.; −6 to −9 vs deepseek). Caveat chip: "synthetic tickets, LLM labels, n=150" | static |

## Clip 3 · The threshold (Ex3) · 1:13

| # | sec | On screen | Camera / card |
|---|---|---|---|
| 1 Problem | 0-8 | Card: "Where do we put the threshold?" | — |
| 2 Design | 8-20 | Architecture card: S1 (Jev results from ex2) → gate `p ≥ t` → automate / human queue; prices: error $5, review $0.50 | gate box orange |
| 3 Why | 20-26 | Card: "A threshold is a business knob: price errors and reviews, then sweep" | — |
| 4 Code | 26-42 | `economics.py`: l.31 `simulate()` (auto vs escalate, cost sum) → l.21 `THRESHOLDS` → l.66-67 sweep + `best` | zoom per block |
| 5 Run | 42-62 | type `make ex3` → sweep: t=0 → 100% automated, 67 errors/1k, $333; t=0.95 → 75% automated, 0 errors on the test set, **$127 ← cheapest**; never → $500 | zoom on the three rows, chart card (cost vs threshold) |
| 6 Alternatives | 62-75 | Bottom table "best threshold per S1": Jev $127 · verbal deepseek $127 · sonnet $135 · gpt-6-sol $138 · logprobs $103 (93% automated, 13 errors) · votes $130. Card: "At this volume errors and reviews dominate; model price and latency matter at scale" | zoom on the bottom table |

## Claims checklist (all on screen numbers)

- ✅ request shape, `criteria`, noul 0.7/0.3 band, probability-routing, confidence formulas: docs.typesafe.ai (confidence, probability-routing, API reference), checked 2026-11-15.
- ✅ price $0.042 / 1M input tokens, output free: docs Models page; matches OpenRouter `usage.cost` in our runs.
- ✅ all ex2/ex3 numbers: `runs/ex2-ex3-results.txt` (bootstrap CIs inside).
- ⚠ synthetic data, LLM-consensus labels, n=150; one run per method; latency through OpenRouter from one place.
- 🟡 "trained for calibration" is the vendor's claim; our measurement shows comparable, not superior, calibration.

## How it was rendered (2026-11-15)

1. Runs re-recorded with `capture/capture.py` → `runs/jev-ticket|jev-comment|jev-approval|eval|eval-urgency|ex3.json` (only the three `lite-jev` runs called a paid API; eval/ex3 re-score the committed results).
2. `capture/build_data.py` packs the real files (`jev_client.py`, `methods.py`, `eval.py`, `economics.py`) and the runs; waits longer than 1 s between output lines (Docker start-up) are shortened, the programs' own latency numbers are untouched.
3. The local Remotion project (not in the repo) renders the 1920×1080 stage at 4K and downsamples to 2560×1440 H.264 → `videos/demo-1-one-call.mp4`, `demo-2-same-tickets.mp4`, `demo-3-threshold.mp4` + posters; every number on a card or caption is parsed from the runs.
4. `tools/build_deck.py && node tools/export_frames.mjs && python3 tools/make_presenter.py` put the posters into slides 17-19 and the clips into `present.html` (autoplay).
