# Exercise 2: verbalized confidence vs a computed distribution

**Problem.** "Why not just use structured output and ask the LLM for a confidence?" It is the real alternative to a decision model, so we measure it.

**Design.** The same 150 test tickets, the same option descriptions, two questions each (department, urgency). Five ways to get "answer + how sure" (`methods.py`):

| | Method | Where the number comes from |
|---|---|---|
| A | structured output + `confidence` | the model *writes* a number (verbalized) |
| B | token logprobs | the model's own next-token probabilities over the option names |
| C | self-consistency, k = 5 | vote share of 5 samples at temperature 1 |
| D | TF-IDF + logistic regression | a classic classifier trained on 100 labelled tickets |
| E | Jev (System One) | a distribution over every option, computed in one pass |

**Run.** `make ex2-estimate`, then `make ex2 METHOD=jev` (or `all`), then `make eval`. Offline: `make workshop`.

**Read the output.** Reliability table: "said 0.92, was right 100%" means under-confident; "said 0.98, was right 65%" means over-confident. auto@95: how much you can automate at 95% accuracy. distinct: how fine the threshold knob is.

**Strong models:** `make ex2 METHOD=strong` runs gpt-6-sol and claude-sonnet-5.5 (about $0.50, already in `results/`).

**What we found** (details and caveats in [`../METHODOLOGY.md`](../METHODOLOGY.md)): verbalized confidence was usable (gpt-6-sol well calibrated, Sonnet under-confident, small models coarse); logprobs and votes were over-confident on the subjective question; Jev matched the strong models on department accuracy and calibration at 1/54-1/80 of the price and 6-13x lower latency, one call for both questions, but was not more accurate (and trailed on urgency).
