# Comparison

Checked 2026-10-10. ✅ primary source, 🟡 vendor-only claim, 🟠 secondary only, ❌ conflicting/unknown. See `research.md`.

## Decision-model APIs

| | TypeSafe Jev 1.13 | OpenAI Decisions | Cloudflare Clef / Clef-flash | Laya | Liquid d1 |
|---|---|---|---|---|---|
| Access | Hosted API ✅ | Hosted API, public beta ✅ | Workers AI + open weights ✅ | Open weights 🟠 | ❌ conflicting |
| Endpoint | `POST /v1/systemone` ✅ | `POST /v1/decisions` ✅ | Workers AI; "Jev-compatible" 🟡 | Jev-compatible via Unsloth 🟡 | `/v1/systemone` shape 🟠 |
| Question types | noul / choice / score ✅ | predicate / choice / score ✅ | same as Jev 🟡 | same 🟠 | same 🟠 |
| Input | text only ✅ | text + images ✅ | text, images, video 🟠 | text 🟠 | ? |
| Price (input / 1M tok) | $0.042, output free ✅ | $0.10, output free ✅ | $0.24 / $0.09 🟠 | free (self-host) | ❌ |
| Size | not published ✅ | not published | 27B / 9B ✅ | ~0.4B 🟠 | 3B (d1-3B) 🟠 |
| Median latency | 524 ms (Cloudflare's test) 🟡 | "~10x faster than Responses" 🟡 | 209 / 39 ms 🟡 | ~6-40 ms 🟡 | ? |
| Context | 64k ✅ | ? | 64k ✅ | ? | 32k 🟠 |
| Customization | none (prompt/state only) ✅ | none | open weights; RL fine-tuning platform 🟡 | fine-tune required 🟠 | ? |

## Broader class: ways to make a "System 1" decision

| Approach | Latency | Calibrated probs | Needs labeled data | Zero-shot new labels | Example |
|---|---|---|---|---|---|
| Rules / regex | µs | no | no | no | keyword routing |
| Classic classifier (TF-IDF + LR) | µs-ms | roughly, can be recalibrated | yes | no | workshop ex1 |
| Fine-tuned encoder (BERT/ModernBERT) | ms | after calibration | yes | no | Laya-style |
| Embeddings + kNN / similarity | ms | weak | few examples | partly | semantic routing |
| Cross-encoder reranker / reward model | 10-100 ms | partly | yes | partly | rerankers, RLHF reward models |
| **General decision model** | 10-500 ms | **trained for it** | no | **yes** | Jev, Clef, OpenAI Decisions |
| LLM + constrained output / logprobs | 0.3-3 s | poor (needs sampling or logprobs) | no | yes | workshop ex2 |
| Reasoning LLM (System 2) | seconds-minutes | poor | no | yes | escalation path in ex3 |
