# System One models: research notes

Topic: *Jev, a non-text-generating "System One" AI model*, generalized to **decision models**: models that read an input and return typed, probability-bearing decisions instead of generated text.

All sources were checked on **2026-10-10** unless noted. Legend:
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
| Text-only input (string, JSON object, array of text). No images/audio/video yet | ✅ | system-one + Models pages |
| Current model `jev-1.13.0`; aliases `jev-latest`, `jev-preview` (both → 1.13.0) | ✅ | Models page |
| Price **$0.042 / 1M input tokens** ($42 per billion), output free | ✅ | Models page |
| Rate limits 100K tok/s, 80 req/s, "adjusting dynamically" due to demand | ✅ | Models page |
| Context 64k per request; 32k for state + longest question | ✅ | Models page |
| Not fine-tuned per customer; same weights for every account; not trained on customer data | ✅ | Models page |
| English best; other languages weaker | ✅ | Models page |
| Known weaknesses page ("Jev 1.13 jaggedness") exists | ✅ (exists) | llms.txt |
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
- Whether TypeSafe or OpenAI offer any free tier (none found). Exercise 4 therefore needs paid keys; exercises 1-3 are free.
- Independent benchmark of calibration across providers - none found.
