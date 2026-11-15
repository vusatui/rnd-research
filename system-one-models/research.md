# System One models: research notes

Topic: *Jev, a non-text-generating "System One" AI model*, generalized to **decision models**: models that read an input and return typed, probability-bearing decisions instead of generated text.

All sources were checked on **2026-10-10** unless noted; the Jev rows, OpenRouter availability and section 7 were re-checked on **2026-11-15**. Legend:
- ✅ **verified**: read on the primary (vendor/official) page.
- 🟡 **vendor-only**: stated by the vendor about itself (benchmarks, latency, speed claims); not independently reproduced.
- 🟠 **secondary**: only from third-party blogs/aggregators; not confirmed on a primary page.
- ❌ **conflict / unverified**.

> Caution: in the past weeks many unofficial "Jev" sites appeared (jevtypesafeai.com, jevai.guide, jevwiki.ai, madewithjev.com, systemonemodels.ai, modelsystem.one ...). They are **not** TypeSafe and sometimes contradict the official docs (see pricing below). We only treat `docs.typesafe.ai` as primary for Jev.

## 1. Jev (TypeSafe AI)

| Claim | Status | Source |
|---|---|---|
| Jev is TypeSafe's flagship and "first System One model"; returns typed decisions + probabilities, not text; does not write replies, code, or reasoning explanations | ✅ | [docs.typesafe.ai/concepts/system-one](https://docs.typesafe.ai/concepts/system-one) |
| Name "System One" from Kahneman's *Thinking, Fast and Slow* (System 1 fast/intuitive vs System 2 deliberate) | ✅ | same |
| Three primitives: **Choice** (one of N options), **Score** (ordered levels), **Noul** (probability of "yes") | ✅ | same; [llms.txt index](https://docs.typesafe.ai/llms.txt) |
| Answers carry **confidence** separately from probability; designed for "act vs escalate to a human or reasoning model" | ✅ | system-one page; [Confidence](https://docs.typesafe.ai/confidence.md) |
| Trained for calibration ("probabilities optimized against outcomes"); calibration is a group property, not a per-answer guarantee | ✅ (claim) / 🟡 (quality) | system-one page; training method called **RLCD** in [Models](https://docs.typesafe.ai/models.md) - RLCD itself is not explained in detail in what we read |
| API: `POST https://api.typesafe.ai/v1/systemone` with `model`, `state`, `questions` (map); SDK `typesafe-sdk` (Python), `@typesafe-ai/sdk` (JS) | ✅ | [Models](https://docs.typesafe.ai/models.md), API ref |
| Input: text (string, JSON object, array of text) **and PNG/JPEG images** anywhere in the request (state, instructions, criteria); no audio/video yet. `box` question type (locate something in an image) needs Jev 1.14 and the `TypeSafe-Danger-Zone-Images: true` header | ✅ (2026-11-15) | [Models](https://docs.typesafe.ai/models.md), [Images](https://docs.typesafe.ai/images.md), [API reference](https://docs.typesafe.ai/api/system-one.md) |
| Current model **`jev-1.14.0`** (available from 2026-10-14); `jev-1.13.0` still listed; aliases `jev-latest`, `jev-preview` → 1.14.0. Pin a versioned ID in production | ✅ (2026-11-15) | [Models](https://docs.typesafe.ai/models.md) |
| **Available on OpenRouter:** `POST https://openrouter.ai/api/v1/systemone` with `model: jev-latest` (same wire format; response `model: typesafe/jev-1.14-20261014`, `provider: TypeSafe`, `usage.cost` billed input-only). `typesafe/jev-router` on OpenRouter is a different product (a chat router that picks an LLM), not the decision API | ✅ tested 2026-11-15 | our calls, [`presentation/serious/demo/runs/ex1-real-jev.txt`](presentation/serious/demo/runs/ex1-real-jev.txt) |
| `confidence` is derived from `probabilities`: Choice `(p_max − 1/n)/(1 − 1/n)`; Score `max(0, 1 − Σ p_i·|i − m| / MAD_unif)`; Noul has none (use P(yes), start with 0.7 / 0.3 and give the band its own outcome). For thresholds on a Choice the docs recommend the chosen option's probability | ✅ (2026-11-15) | [Confidence](https://docs.typesafe.ai/confidence.md), [Routing by probability](https://docs.typesafe.ai/patterns/probability-routing.md) |
| Price **$0.042 / 1M input tokens** ($42 per billion), output free | ✅ | Models page |
| Rate limits 100K tok/s, 80 req/s, "adjusting dynamically" due to demand | ✅ | Models page |
| Context 64k per request; 32k for state + longest question; opt-in long context (262k) via `TypeSafe-Danger-Zone-Long-Context: true` | ✅ | Models page |
| Not fine-tuned per customer; same weights for every account; not trained on customer data | ✅ | Models page |
| English best; other languages weaker | ✅ | Models page |
| Known weaknesses page ("Jev 1.13 jaggedness") exists | ✅ (exists) | llms.txt |
| Measured by us (150 synthetic tickets, two questions per request, via OpenRouter): p50 161 ms, p90 210 ms; $0.025 per 1,000 tickets (~596 input tokens each) | ✅ own measurement, see section 7 | [`workshop/METHODOLOGY.md`](workshop/METHODOLOGY.md) |
| Parameter count / architecture | ❌ not published | Models page lists none |
| Latency "70-500 ms", "40-200x faster than a frontier LLM" | 🟠 | unofficial jevtypesafeai.com; Cloudflare measured Jev median **524 ms** (🟡 Cloudflare benchmark) |
| Price **$0.42/M** | ❌ **conflicts** with official $0.042/M | unofficial jevtypesafeai.com - ignore |
| Launched 15 Sep 2026; founders Diogo Almeida, Erik Gafni, Sasha Sheng; $40M seed led by DCVC; name nods to Jevons paradox; hosted with waitlist | 🟠 | softwareinsights.dev, jevtypesafeai.com - not found on a TypeSafe page we could read |

## 2. OpenAI Decisions API

| Claim | Status | Source |
|---|---|---|
| Exists; **public beta**, GA "in the coming weeks" | ✅ | [platform.openai.com/docs/guides/decisions](https://platform.openai.com/docs/guides/decisions) |
| `POST /v1/decisions`; fields `model`, `input`, `questions` (array, each with `name`); response `answers` array, possible `refusal` answer type | ✅ | same |
| Only model: `gpt-6-luna` | ✅ | same |
| Question types: `predicate` (probability), `choice` (one value + probabilities + confidence), `score` (probability-weighted average of level indices + confidence) | ✅ | same |
| Text **and images** (base64 data URLs only; no hosted URLs / file_id) | ✅ | same |
| "about 10x faster than the Responses API" | 🟡 | same |
| Price $0.10 / 1M input tokens; no output, cache-read or cache-write charges; regional/long-context multipliers | ✅ | same |
| ZDR + HIPAA for eligible customers; US/EU residency | ✅ | same |
| SDK min versions Python 3.26.0, JS 7.30.0 (`client.decisions.create`) | ✅ | same |
| OpenAI recommends Structured Outputs / function calling when you need generated objects or tool arguments | ✅ | same |
| Public beta announced 6-7 Oct 2026, shown earlier at DevDay | 🟠 | community.openai.com thread (2026-10-07), stackone.com blog |
| Available via Vercel AI Gateway as `openai/gpt-6-luna-decisions`; gateway's `/v1/decisions` also serves Jev, Liquid d1, Laya | 🟡 (Vercel's own changelog) | [vercel.com/changelog](https://vercel.com/changelog/openai-decisions-api-now-available-on-ai-gateway) |
| Request limits: 1-255 choices, 2-10 score levels | 🟡 | Vercel docs (mirrors OpenAI shape); not seen on the OpenAI page we read |

Note: Jev and OpenAI converge on the **same three primitives** (Noul ≈ predicate, Choice, Score) with different wire shapes (map vs array, `state` vs `input`).

## 3. The LinkedIn post (https://lnkd.in/p/e9nNGmzZ)

✅ Short link resolves (HTTP 301) to a post by **Daniel Han (Unsloth)**, published 2026-10-07 16:22 UTC (19:22 Istanbul). Full text only partially visible without login; the public meta description says:

> "You can now train your own Decision model like Jev locally! We increased Qwen3.5 0.8B's accuracy from 20.7% to 74.3% across 3 decision benchmarks - on just 4GB VRAM. Turn any LLM like Qwen3.8, Gemma 4 into decision models with our open-source repo. ... We fine-tuned with a Clef head using Unsloth and LoRA (r=64) for one epoch, increasing downstream accuracy from 30–37% to 78%."

Details from the [Unsloth guide](https://unsloth.ai/docs/basics/train-your-own-decision-model-with-unsloth) (✅ read via search extract): new `FastDecisionModel` / `DecisionTrainer`; the LLM reads input + all questions/options once, a small scoring head ("same design as Cloudflare's Clef") scores every option - no text generation; free Colab/Kaggle notebooks (Qwen3.5-4B); trained models can be served by Unsloth as a **Jev-compatible API** (requests for `jev-latest` routed to your model). Accuracy numbers are 🟡 vendor-only. Unsloth also documents serving **Laya** locally behind a TypeSafe-compatible API ([decision-laya](https://unsloth.ai/docs/models/decision-laya)), with the caveat that Laya's `confidence` formula differs from Jev's.

## 4. The wider ecosystem (generalization)

| Model | Vendor | Open weights | Notes | Status |
|---|---|---|---|---|
| Clef (27B), Clef-flash (9B) | Cloudflare | Yes, Apache 2.0 (HF) | Workers AI `@cf/cloudflare/clef(-flash)`, 64K ctx, "fully Jev-API compatible"; Cloudflare reports it leads 7/10 decision benchmarks, median latency 209 ms / 39 ms vs Jev 524 ms | ✅ existence ([changelog 2026-10-01](https://developers.cloudflare.com/changelog/post/2026-10-01-clef-workers-ai/), [blog](https://blog.cloudflare.com/clef-decision-models/)); 🟡 benchmarks |
| Laya | Convai Innovations | Yes, Apache 2.0 | ModernBERT-large encoder + decision head, ~0.4B, very fast; needs fine-tuning to be useful | 🟠 (third-party sites + Unsloth docs) |
| d1 / d1-3B | Liquid AI | d1-3B under LFM Open License (commercial use restricted above $10M revenue) | Sources **conflict** on whether d1 is hosted-only or self-hostable | ❌ conflict - check Liquid's own page |
| "Kev 9B", "DiffusionGemma Jev", "Decider 35B-A3B", "Jev Decision Index" | various | ? | Only seen in Cloudflare/S5 Labs tables | 🟠 not investigated |

**Older, well-established members of the same class** (not new, but the talk's generalization): text classifiers (logistic regression, fine-tuned BERT/ModernBERT), cross-encoder rerankers, reward models / LLM-as-judge, embedding similarity + kNN, LLM routers (e.g. RouteLLM), guardrail classifiers (Llama Guard-style), learned policies/value networks in RL (AlphaGo's policy net = "intuition", MCTS = "deliberation"). What is new in Sept-Oct 2026 is a **general-purpose, instruction-following, zero-shot** decision model with a standard API.

## 5. Key findings

1. "System One model" is a real, documented product category as of Sept-Oct 2026: TypeSafe Jev (hosted), OpenAI Decisions (beta), Cloudflare Clef (open), plus Laya / Liquid d1 and the Unsloth training recipe.
2. The **API shape is converging**: state/input + typed questions (yes-probability, choice, ordered score) → probabilities + confidence, billed on input tokens only, output free.
3. The value proposition is **latency, cost, and calibrated uncertainty** for narrow decisions consumed by code (routing, triage, guardrails, reranking), with LLMs (System 2) reserved for low-confidence cases.
4. **Jev-compatible API** is becoming a de facto interface (Clef, Unsloth, Vercel gateway), similar to how the OpenAI chat API became the standard for LLMs.
5. Benchmarks are almost all vendor-run; independent evaluation is thin. Calibration claims must be tested on your own labeled data (OpenAI's own guide says the same).

## 6. Unverified / open items

- Jev launch date, founders, funding, parameter count, latency figures (unofficial sources only).
- Exact Workers AI request body for Clef (our `ex4` code assumes the Jev shape - not tested).
- Liquid d1 availability (hosted vs self-host) - conflicting sources.
- Laya's vendor and size - only third-party pages.
- Whether TypeSafe or OpenAI offer any free tier (none found). Real Jev runs through any OpenRouter key with credits; the emulator and the committed results keep the workshop free to follow.
- Independent benchmark of calibration across providers - none found; our own small comparison is in section 7.

## 7. Decision model vs structured output + verbalized confidence (our measurement, 2026-11-15)

The obvious alternative to a decision model is a chat LLM with **structured output** (JSON schema, enum labels) that also writes a **confidence** number. The difference is *how the number is produced*: a chat model **writes** a confidence as tokens (verbalized); a decision model **computes** a probability for every option from one pass and is trained for calibration (vendor claim, Jev docs).

What the literature says (both papers ✅ read on arXiv, 2026-11-15):
- **Tian et al., "Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback"**, [arXiv:2305.14975](https://arxiv.org/abs/2305.14975) (2023): for RLHF chat models (ChatGPT, GPT-4, Claude), verbalized confidences are typically *better* calibrated than the models' conditional token probabilities on TriviaQA, SciQ and TruthfulQA, often cutting ECE by a relative 50%.
- **Xiong et al., "Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs"**, [arXiv:2306.13063](https://arxiv.org/abs/2306.13063) (ICLR 2024): verbalized confidence tends to be *over-confident*; calibration and failure prediction improve with model capability; consistency across multiple samples and better aggregation help; white-box methods are better but the gap is narrow.

Our measurement (method, caveats and CIs: [`workshop/METHODOLOGY.md`](workshop/METHODOLOGY.md)); department question, same 150 held-out synthetic tickets, same option descriptions:

| Method | Accuracy | ECE | distinct values | p50 | $ / 1k |
|---|---|---|---|---|---|
| Jev 1.14 (1 call, 2 questions) | 93% | 0.042 | 35 | 161 ms | $0.025 |
| gpt-6-sol, verbalized | 93% | 0.039 | 19 | 2,108 ms | $1.34 |
| claude-sonnet-5.5, verbalized | 94% | 0.113 (under-confident) | 17 | 1,020 ms | $2.00 |
| claude-haiku-5.5, verbalized | 92% | 0.069 | 14 | 815 ms | $0.10 |
| deepseek-v4.1-flash, verbalized | 95% | 0.067 | 12 | 540 ms | $0.046 |
| deepseek, token logprobs | 95% | 0.032 | 31 | 433 ms | $0.037 |
| deepseek, 5 votes | 97% | 0.024 | 3 | 756 ms | $0.153 |

Findings: (1) verbalized confidence from strong models is **not garbage** (gpt-6-sol well calibrated, Sonnet under-confident rather than over-confident); (2) it is **coarse** (12-19 distinct values) and costs output tokens and latency; (3) logprobs and vote counting were **over-confident on the subjective urgency question** (logprobs said ~0.98, was right 65% in that bin); (4) Jev matched the strong models' accuracy and calibration on department at 1/54-1/80 of the price and 6-13x lower latency, but **was not more accurate**, and trailed on urgency (−4 points vs the strong models, not significant; −6 to −9 vs the deepseek methods). Labels are an LLM consensus on synthetic data, which favours LLM-like judgement.
Conclusion for the talk: **choose a decision model for price, speed and format plus decent probabilities, not for superior accuracy; measure the confidence of any method on your own data.**
