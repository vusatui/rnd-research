# Workshop: decision models vs structured output + confidence

Three exercises and a homework, all on **one dataset** (250 synthetic support tickets, `data/`) and **one evaluation harness** (`eval.py`). Every number quoted in the talk comes from here; how it was measured is in [`METHODOLOGY.md`](METHODOLOGY.md).

## Quick start (Docker + make only)

Run from `system-one-models/`:

```bash
cp .env.example .env        # OPENROUTER_API_KEY (needed only for live runs)
make workshop               # ex2 + ex3 from the committed results: no key, no network
make ex1                    # Exercise 1 on the local emulator (free model)
make lite-jev               # Exercise 1 against REAL Jev via OpenRouter (~$0.00002 per request)
make ex2-estimate           # $ estimate before a paid run
make ex2 METHOD=jev         # re-run one method live (METHOD=all|jev|verbal|logprobs|votes|classic, MODEL=, LIMIT=)
make eval                   # accuracy, ECE, reliability tables, auto@95/98, latency, $/1k for every result
make ex3 ERROR_COST=20 REVIEW=1   # fast-first economics with your own costs
make homework               # the same ticket to every decision API you have a key for
make test                   # offline smoke tests (what CI runs)
```

`MOCK=1` never calls a model: ex2 re-scores the committed `results/`, the emulator answers with keyword rules (labelled MOCK). Paid runs stop at `MAX_SPEND_USD` (default $0.05).

## The exercises

| # | Folder | Problem | What you build and measure |
|---|---|---|---|
| 1 | [`../presentation/workshop-lite/`](../presentation/workshop-lite/README.md) | One decision, several questions, code decides | One request = several typed questions; per-action thresholds in code (noul 0.7 / 0.3 band, block ≥ 0.9, approve ≥ 0.9). Same client against the local emulator and real Jev. |
| 2 | [`ex2_confidence/`](ex2_confidence/) | Why not structured output + a confidence number? | The same 150 tickets through 5 methods: A verbalized confidence (structured output; gpt-6-sol, claude-sonnet-5.5, haiku, deepseek), B token logprobs, C self-consistency k=5, D classic classifier, E Jev. Reliability tables, ECE, auto@95/98, latency, $. |
| 3 | [`ex3_fast_first/`](ex3_fast_first/) | Where to put the threshold? | Price errors and reviews, sweep the threshold, find the cheapest; compare every S1 method from ex2. |
| HW | [`homework/`](homework/) | Your provider, your data | Plug a TypeSafe / OpenAI Decisions / Clef key, add it as a method in `ex2_confidence/methods.py`, run it on the same tickets. |

## Results in one table (department, 150 test tickets)

| Method | Accuracy | ECE | distinct conf. values | p50 latency | $ / 1k tickets |
|---|---|---|---|---|---|
| Jev 1.14 (1 call, both questions) | 93% | 0.042 | 35 | **161 ms** | **$0.025** |
| gpt-6-sol, verbalized (structured output) | 93% | 0.039 | 19 | 2,108 ms | $1.34 |
| claude-sonnet-5.5, verbalized | 94% | 0.113 | 17 | 1,020 ms | $2.00 |
| claude-haiku-5.5, verbalized | 92% | 0.069 | 14 | 815 ms | $0.100 |
| deepseek-v4.1-flash, verbalized | 95% | 0.067 | 12 | 540 ms | $0.046 |
| deepseek, logprobs | 95% | 0.032 | 31 | 433 ms | $0.037 |
| deepseek, 5 votes | 97% | 0.024 | 3 | 756 ms | $0.153 |
| TF-IDF + logreg (100 train) | 72% | 0.329 | 146 | 1 ms | $0 |

Department differences between the model-based methods are within the bootstrap noise; on the subjective urgency question Jev trails by 4 points (strong models, not significant) to 9 points (deepseek methods). Honest summary: **choose a decision model for price, speed and format plus decent probabilities, not for superior accuracy, and measure the confidence of any method on your own data.**

## Files

| File | What |
|---|---|
| `common.py` | label set and descriptions (identical for all methods), dataset loader |
| `llm.py` | OpenRouter chat client and System One client; real usage, $ and latency per call; budget guard |
| `eval.py` | the shared harness; `--reliability`, `--ci` (bootstrap), `--question urgency` |
| `data/` | `tickets.jsonl`, `make_dataset.py`, [`DATASET.md`](data/DATASET.md), `generation_log.json`, raw model outputs |
| `results/` | one JSONL per method with per-ticket answers, probabilities, tokens, latency, $ |
| `list_free_models.py` | current free OpenRouter models (for the emulator) |
