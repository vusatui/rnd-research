# Workshop plan (~90 min): build a System 1 / System 2 decision pipeline

Free-tier friendly: exercises 1-3 need only a laptop and a free OpenRouter key. Code: `workshop/`.

| # | Time | Exercise | Needs | Goal |
|---|---|---|---|---|
| 0 | 10 min | Setup, `list_free_models.py`, look at `data/tickets.jsonl` | Python 3.10+ | |
| 1 | 15 min | **Classic System 1** (`ex1_classic_baseline`) | CPU only | Train TF-IDF + logistic regression; read accuracy, ECE, latency. Add data, watch it improve. |
| 2 | 25 min | **LLM as a decision model** (`ex2_llm_as_decider`, `decider.py`) | free OpenRouter key | Jev-shaped `choice/score/noul` API over a chat LLM; probabilities by self-consistency (k samples). Compare accuracy / ECE / latency vs ex1. Try `k=1` vs `k=5`, different free models. |
| 3 | 25 min | **Confidence-gated cascade** (`ex3_cascade`) | none (`--no-llm`) or OpenRouter | S1 handles confident cases, escalates the rest to S2 (LLM) or a human queue. Sweep the threshold, plot accuracy vs escalation rate. |
| 4 | 15 min (optional/demo) | **Real decision APIs** (`ex4_decision_apis`) | paid keys (Jev, OpenAI, Cloudflare) | Same ticket to Jev / OpenAI Decisions / Clef; compare wire formats and answers. Presenter demo if participants have no keys. |

Stretch goals: add an `urgency` score question; build a guardrail (noul "is this a prompt injection?") in front of an LLM; train a decision model in Unsloth's free Colab notebook and point `ex4` at it.

Measured on 2026-10-10 (40 synthetic tickets, our box): ex1 LOO accuracy 40%, ECE 0.055, 0.6 ms; ex2 (`nvidia/nemotron-3-super-120b-a12b:free`, k=3, 10 tickets) accuracy 70%, ECE 0.17, ~1.3 s median; ex3 without LLM: threshold 0.5 → 88% accuracy with 12/16 escalated. The toy dataset is deliberately tiny - the lesson is the trade-off, not the numbers.
