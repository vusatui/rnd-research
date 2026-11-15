# How we tested: methodology of the Exercise 2 / 3 comparison

**Question:** for a typed decision over a closed set of options, how does a decision model's *computed* probability distribution (Jev) compare with the *verbalized* confidence a chat LLM writes into structured output, and with the other ways to get a probability out of a chat LLM, on accuracy, calibration, usefulness for automation, latency and cost?

Everything below can be re-run offline from the saved results (`make workshop`, `python eval.py --ci --reliability`); no number in the talk comes from anywhere else.

## 1. Two layers of models

| Layer | Role | Models | Budget |
|---|---|---|---|
| **Utility layer** (builds the test, is not tested) | generate tickets, annotate them | generator `baidu/ernie-5.5-flash-preview:free`; annotators `particle-ai/particle-1:free`, `openai/gpt-6-luna` | $0.006 |
| **Systems under test** | answer the same 150 test tickets | Jev 1.14 (`jev-latest` via OpenRouter); strong chat models `openai/gpt-6-sol`, `anthropic/claude-sonnet-5.5`; small chat models `anthropic/claude-haiku-5.5`, `deepseek/deepseek-v4.1-flash-1017`; a TF-IDF + logistic regression baseline | $0.56 for all methods ($0.50 of it the two strong models) |

No model of the utility layer is a system under test, so no evaluated model graded its own output.
*Lesson learned:* the first dataset attempt used paid frontier models for generation and annotation and burned most of the budget before producing anything. Dataset generation should use free models; the paid budget belongs to the models under test.

## 2. Dataset

- **Synthetic generation** (`data/make_dataset.py`): 250 support tickets for a fictitious B2B analytics SaaS, 10 batches of 25. Each batch has a fixed quota (5 per department, an urgency mix, 6-7 deliberately *borderline* tickets that mix two departments) and a different writing persona (terse admin, upset owner, non-native speaker, developer, procurement, phone typing, ...). The generator records its intended labels.
- **Blind, independent double annotation:** two annotators from different vendors label every ticket without seeing the intended label or each other's answer, with the same label definitions the systems under test get (`common.py`).
- **Inter-annotator agreement:** raw agreement 97.6% on department, 90.0% on urgency (two annotators, 250 tickets).
- **Adjudication:** gold = majority vote of (generator intent, annotator 1, annotator 2). Tickets on which the two blind annotators disagree on department are flagged `ambiguous` (6 of 250, 4 in the test set); accuracy is reported on all tickets and on the clear ones.
- **Split:** fixed random split, **100 train / 150 held-out test**. Only the classic baseline learns from the train split; every method is scored on the same 150 test tickets. No prompt was tuned on the test set.

## 3. Protocol: what each method does

Same task text and the same option descriptions for every method (5 departments, 3 urgency levels). Two questions per ticket: `department` (main metric) and `urgency` (harder, subjective).

| Method | How the answer and its confidence are produced | Calls per ticket |
|---|---|---|
| **A verbalized** (gpt-6-sol, claude-sonnet-5.5, claude-haiku-5.5, deepseek) | structured output (JSON schema, enum labels) with a `*_confidence` number the model writes; the prompt asks for a calibrated probability; temperature 0; minimal reasoning effort (gpt-6-sol, sonnet), reasoning off (haiku, deepseek); one retry with a larger token limit if the JSON comes back empty | 1 (both questions) |
| **B logprobs** (deepseek) | one answer token, `top_logprobs=20`; probability mass of tokens that uniquely prefix an option, renormalized over the options; temperature 0 | 1 per question (2) |
| **C self-consistency** (deepseek) | k = 5 samples at temperature 1, structured output without confidence; probability = vote share | 5 (both questions per call) |
| **D classic** | TF-IDF (1-2 grams) + logistic regression, `predict_proba`, trained on the 100 train tickets | local |
| **E Jev** | one System One request with two `choice` questions (criteria = the option descriptions); probability = `probabilities[choice]` | 1 (both questions) |

For every method the confidence that is scored is **the probability of the chosen option** (for Jev that is `probabilities[choice]`, not the derived `confidence` field, as the Jev docs recommend for thresholds on a Choice).

## 4. Metrics (`eval.py`)

- **Accuracy** on all 150 test tickets and on the clear ones.
- **ECE (expected calibration error):** 10 equal-width confidence bins; per bin |accuracy − mean confidence|, weighted by the share of tickets in the bin.
- **Reliability table** (the tabular form of a reliability diagram): confidence bins 0-0.5, 0.5-0.7, 0.7-0.8, 0.8-0.9, 0.9-0.95, 0.95-0.99, 0.99-1 → mean stated confidence vs observed accuracy, with counts.
- **Selective prediction / coverage-risk:** sort by confidence, automate the most confident ones; **auto@95 / auto@98** = the largest coverage whose accuracy stays ≥ 95% / 98%. Tickets with equal confidence are kept together (a threshold cannot split them), which is why coarse confidence scales lose coverage.
- **Distinct confidence values**: how fine-grained the knob is.
- **Latency**: wall-clock per ticket from the client (through OpenRouter, 6 tickets in parallel), p50 and p90. For B and C the calls of one ticket run in parallel, so latency is the slowest call.
- **Cost**: $ billed per call as reported by OpenRouter's `usage.cost` (token usage × the provider's price list), summed and scaled to 1,000 tickets. Jev bills input tokens only.
- **Uncertainty:** 95% percentile bootstrap intervals (2,000 resamples of the 150 tickets, seed 7) for accuracy and ECE, and a **paired** bootstrap for accuracy differences against Jev. Computed offline from the saved results.
- **Exercise 3 (economics):** a threshold sweep where the escalated tickets go to a human (assumed correct, $0.50 per review) and every wrong automated answer costs $5 (also shown: $20 / $1); total $ per 1,000 tickets.

## 5. Results (department, 150 test tickets)

| Method | Accuracy [95% CI] | ECE [95% CI] | auto@95 | auto@98 | distinct | p50 ms | $ / 1k |
|---|---|---|---|---|---|---|---|
| **E Jev 1.14** (1 call, both questions) | 93% [89-97] | 0.042 [0.030-0.088] | 87% | 77% | 35 | **161** | **0.025** |
| A verbal **gpt-6-sol** | 93% [89-97] | 0.039 [0.021-0.075] | 97% | 87% | 19 | 2,108 | 1.340 |
| A verbal **claude-sonnet-5.5** | 94% [90-97] | 0.113 [0.087-0.147] | 94% | 83% | 17 | 1,020 | 2.001 |
| A verbal claude-haiku-5.5 | 92% [87-96] | 0.069 [0.068-0.113] | 92% | 73% | 14 | 815 | 0.100 |
| A verbal deepseek-v4.1-flash | 95% [92-99] | 0.067 [0.046-0.099] | 100% | 81% | 12 | 540 | 0.046 |
| B logprobs deepseek | 95% [91-98] | 0.032 [0.015-0.067] | 99% | 93% | 31 | 433 | 0.037 |
| C votes k=5 deepseek | 97% [93-99] | 0.024 [0.009-0.057] | 100% | 0% | 3 | 756 | 0.153 |
| D TF-IDF + logreg | 72% [65-79] | 0.329 [0.262-0.395] | 43% | 39% | 146 | 1 | 0 |

**Urgency** (subjective; annotators agree 90%): Jev 78% [71-85], ECE 0.075; gpt-6-sol 82% [75-88], ECE 0.086; claude-sonnet-5.5 82% [75-88], ECE 0.099; haiku 84%, ECE 0.082; verbal deepseek 86% [80-91], ECE 0.057; logprobs 87%, ECE 0.122 (says ~0.98, right 65% in that bin); votes 84%, ECE 0.113.

**Paired accuracy difference Jev − other:** department within ±3.3 points, no difference significant (every CI crosses 0; Jev vs gpt-6-sol exactly 0.0 [−4.0, +3.3]). Urgency: −4 points vs both strong models (CIs cross 0), −6 to −9 vs the deepseek methods (CIs exclude 0 except haiku).

**Shape of the verbalized numbers:** gpt-6-sol is close to calibrated (said 0.75, right 50%; said 0.99, right 100%); claude-sonnet-5.5 is clearly *under*-confident (said 0.57, right 76%; said 0.84, right 100%); both use 17-19 distinct values against Jev's 35.

**Exercise 3** (error $5, review $0.50, per 1,000 tickets, human as System 2): the best threshold gives $127 for Jev (75% automated, 0 errors on the test set), $127 verbal deepseek, $135 sonnet, $138 gpt-6-sol, $103 logprobs (93% automated but 13 errors), against $333 with no gate and $500 all-human. At this volume the model price is noise next to errors and reviews; it matters at scale and for latency.

Full output: [`../presentation/serious/demo/runs/ex2-ex3-results.txt`](../presentation/serious/demo/runs/ex2-ex3-results.txt); per-ticket results: `results/ex2_*.jsonl`; every raw answer: `results/raw/`.

**Reading:** against strong chat models with structured output, Jev reached the **same accuracy and comparable calibration** on department (gpt-6-sol: 93% / ECE 0.039 vs Jev 93% / 0.042) at **1/54 to 1/80 of the price and 6-13x lower latency**, in one call for both questions with a distribution over every option. It was **not more accurate**, and on the subjective urgency question it trailed (not significantly vs the strong models, significantly vs the deepseek methods). Verbalized confidence was not garbage: gpt-6-sol's was well calibrated, Sonnet's under-confident, the small models' usable but coarse. Token logprobs and vote counting were over-confident on the subjective question. So: choose a decision model for price, speed and format plus decent probabilities, not for superior accuracy, and measure the confidence of any method on your own data.

This matches the literature: verbalized confidence of RLHF chat models is often better calibrated than their token probabilities (Tian et al. 2023, arXiv:2305.14975), and verbalized confidence tends to be over-confident, improving with model capability and with consistency-based methods (Xiong et al. 2024, arXiv:2306.13063). On our data the strong models were not over-confident.

## 6. Limitations

- **Synthetic data**, one fictitious product, English only.
- **Gold labels are an LLM consensus.** Methods that judge like a chat LLM have a home advantage; the decision model may be penalized where its reading is defensible. Human labels on real tickets are the proper next step.
- **Small n:** 150 test tickets, one ticket = 0.7 points; most accuracy differences on department are inside the noise (see CIs). ECE with 10 bins on 150 items is noisy and biased upward; read the reliability tables, not the third decimal.
- **One run per method**, no repeated seeds; Jev's probabilities vary slightly between identical calls (we saw 0.62 vs 0.56 on a toy request).
- **One strong model per vendor** (gpt-6-sol, claude-sonnet-5.5) at minimal reasoning effort; more reasoning might change accuracy and calibration (and cost more). No Gemini run.
- **Latency** is end-to-end through OpenRouter from one location on one evening; provider routing varies (B was restricted to providers that return logprobs).
- **Prompt sensitivity:** one prompt per method, not tuned; other wordings will move the numbers.
