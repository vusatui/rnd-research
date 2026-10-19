# Workshop plan: AI cost control (~2.5-3 h)

Goal: participants leave able to (1) compute **$ per successful task** for an LLM feature, (2) predict and measure the
effect of the main cost levers on cost *and* quality, (3) put a gateway with budgets and attribution in front of a
feature and produce a FOCUS-shaped chargeback, and (4) reason about self-host break-even with explicit assumptions.
Code and commands: [`workshop/README.md`](workshop/README.md). All numbers below were measured on **2026-10-19** with
free OpenRouter models (large = `nvidia/nemotron-3-ultra-550b-a55b:free`, small = `nvidia/nemotron-3.5-lightning:free`),
reasoning/retries/fallbacks off, one run per configuration, n=16 tickets. Costs are **shadow costs** from published
paid prices (twin = paid OpenRouter endpoint of the same model; frontier = gpt-6.1-sol / gpt-6-luna list prices).
Differences of 1-2 tickets are within noise.

## Agenda

| # | Min | Block | What participants do |
|---|---|---|---|
| 0 | 15 | Setup + framing | venv, key, `pytest`, `check_quota.py`; why free models need shadow prices; Price x Quantity |
| 1 | 45 | Lever lab | run A_baseline and 3-4 configs; read the table; predict before running; find the hallucinated price in the cascade |
| 2 | 20 | Prompt caching | cache probe stable vs dynamic; caching simulator; discuss write premium and TTL |
| 3 | 15 | Semantic cache | run the threshold sweep; pick a threshold; see the near-miss failures |
| 4 | 40 | Gateway + chargeback | LiteLLM up; two teams with budgets/allow-lists; trip a budget; FOCUS export; chargeback table |
| 5 | 15 | Self-host break-even | change GPU price, throughput, utilization; find when self-hosting wins |
| 6 | 10 | Wrap-up | checklist: unit metric, attribution, budgets, levers in order of risk |

Quota: ~230 requests for everything as run below; a 50/day key can do blocks 1-2 with `--only` and `--rescore`.

## Block 1 - lever lab (measured)

Frontier price card, 100k tickets/month projection:

| config | pass | avg in tok | avg out tok | $/task | $/success | vs baseline | $/month @100k | p50 s |
|---|---|---|---|---|---|---|---|---|
| A_baseline (large, whole KB, verbose) | 14/16 | 4,231 | 403 | $0.01250 | $0.01428 | - | $1,250 | 8.85 |
| B_concise (short JSON, max_tokens 350) | 15/16 | 4,216 | 85 | $0.00928 | $0.00990 | -26% | $928 | 2.32 |
| C_stable (B + dynamic header moved into the user turn) | 14/16 | 4,218 | 88 | $0.00931 | $0.01064 | -25% | $931 | 2.77 |
| D_trim (C + BM25 top-3 sections) | 15/16 | 1,537 | 86 | $0.00394 | $0.00420 | -68% | $394 | 3.76 |
| E_small_dyn | 14/16 | 4,217 | 79 | $0.00046 | $0.00053 | -96% | $46 | 4.31 |
| F_small_full (stable) | 14/16 | 4,217 | 79 | $0.00046 | $0.00053 | -96% | $46 | 2.64 |
| G_small_trim | 9/16 | 1,537 | 82 | $0.00019 | $0.00035 | -98% | $19 | 1.90 |
| H_cascade (F → D if invalid / confidence < 0.75) | 13/16 | 4,039 | 81 | $0.00065 | $0.00080 | -95% | $65 | 1.83 |
| I_cascade_grounded (H + number grounding) | 14/16 | 4,310 | 87 | $0.00065 | $0.00074 | -95% | $65 | 1.52 |

Source files: `workshop/results/levers_summary_A-H.md`, `levers_summary_I.md` (raw: `levers_*_2026-10-19.json`).

Discussion points (what we actually saw):
- **Concise output was cheaper *and* better.** Output was ~1/3 of the baseline's cost (403 tokens at 5x the input
  price); cutting it to 85 tokens saved 26% and cut p50 latency from 8.9 s to 2.3 s.
- **Trimming context is the biggest lever on the large model** (-68%) without quality loss here - BM25 recall@3 was
  14/16, but the large model compensated on the misses.
- **Small model + trimmed context collapsed** (9/16; mostly wrong categories): levers interact; stacking two "safe"
  levers can break quality. This is why every lever needs the eval set.
- **The cascade is only as good as its escalation signal.** H escalated once (invalid JSON); the small model's
  self-reported confidence was high on its wrong answers. In I, the grounding check escalated T11, where the small
  model had invented an Enterprise price ("$9,900"; in the H run the same invented price came with self-reported
  confidence 0.95, passed H's validator and failed the facts check); the large model then passed. In earlier runs the small model
  also invented "$5,000" - which slipped through a naive grounding check because "5,000" appears in the KB as a file
  count; keeping the `$` marker in the comparison fixed it.
- **Our own checks have the same blind spot.** F_small_full "passed" T11 with an invented "$5,000 per year" base price
  (it also said "contact sales for a custom quote", which satisfied the regex). The quality numbers are only as good as
  the checks - another argument for deterministic grounding checks in both the eval set and the runtime validator.
- The large model sometimes returned a KB section id ("invoicing") as the category (T05).
- Twin vs frontier: B vs E (same prompt, large vs small) differ ~9x on twin prices and ~20x on the frontier card. The *choice of price card*
  changes the business case; always state it.

## Block 2 - prompt caching (measured + simulated)

- Cache probe (sequential, small model): with the ~4.2k-token prompt both stable and dynamic prefixes got **0 cached
  tokens**; with the ~8.1k-token prompt (`--pad 1`) the stable prefix got **6,288 cached tokens** on every request from
  the 2nd on (58% of input, twin cost -24%), the dynamic one 0. In the later I run the free endpoint cached 15% of
  input on ~4.2k prompts - free-endpoint caching is undocumented and opportunistic, so treat these as qualitative.
- Simulation with published rules on the measured shape (stable prefix ~4,173 + ~45 tokens/ticket), input-cost
  multiplier vs no caching by requests per TTL window:

| rule | N=1 | N=2 | N=5 | N=20 | N=100 |
|---|---|---|---|---|---|
| OpenAI GPT-5.6+ / Anthropic 5-min (write 1.25x, read 0.10x) | 1.25x | 0.68x | 0.34x | 0.17x | 0.12x |
| OpenAI gpt-6.1-sol (read 0.05x) | 1.25x | 0.65x | 0.30x | 0.12x | 0.07x |
| Anthropic 1-hour (write 2x) | 1.99x | 1.05x | 0.49x | 0.20x | 0.13x |
| Gemini implicit (no write fee, read 0.05x) | 1.00x | 0.53x | 0.25x | 0.11x | 0.07x |

  Point: a dynamic value at the top makes every request "N=1" - you pay the write premium and never read.

## Block 3 - semantic cache (measured, offline)

bge-small-en-v1.5 on 24 hand-built pairs (12 true paraphrases, 12 near-misses with a different correct answer):
mean similarity paraphrases 0.824 vs near-misses 0.836. At threshold 0.80: 8/12 paraphrases hit (saved), 9/12
near-misses would be served the **wrong** cached answer; at 0.85: 3/12 vs 6/12. Worst: "SSO on the Business plan?" vs
"SSO on the Enterprise plan?" = 0.946. Lexical TF-IDF caught no paraphrases. The pairs are adversarial by design;
the lesson is that no global threshold separates them (consistent with vCache, ICLR 2026).

## Block 4 - gateway, budgets, chargeback (measured)

LiteLLM v1.106.0 (OSS) + Postgres 16, frontier shadow prices in the model config:
- Team **support** ($0.05 budget, large+small): requests 1-6 served; request 7 rejected with HTTP 422 "Budget has
  been exceeded"; final spend $0.05619 = **112%** of budget (check happens before the call; the crossing request is
  served). Team spend shown to the client lags by one request.
- Team **growth** ($0.01, small only): `large` → HTTP 403 (not on allow-list); two small calls $0.00091.
- Gotchas: key-level tags are Enterprise-only (403); per-request `metadata.tags` work. With the `openrouter/`
  provider prefix free models were logged at $0 despite custom prices, so budgets never tripped - verify the gateway's
  cost numbers against a hand calculation before trusting a budget.
- `to_focus.py` turned the spend logs and the local ledger into FOCUS-shaped rows (one row per model x token direction
  x cache action, `PrincipalId` = team key alias, never the key, `Tags` = team/feature/config) and a chargeback table:
  `results/focus_gateway.csv`, `results/chargeback_gateway.md`, `results/focus_cost_usage.csv`,
  `results/chargeback_ledger.md`.

## Block 5 - self-host break-even (arithmetic)

Defaults (all flags): 8xH100 at $3.50/GPU-h (specialist-cloud price, secondary source), always on; $15k/month ops;
**assumed** 5,000 output tok/s per replica; 10 input tokens per output token, prefill 10x cheaper.
Fixed cost $35,440/month; capacity 6.57B output tokens/month at 100%.

| compared with | API $ per 1M output tok (incl. input) | break-even utilization |
|---|---|---|
| open-weights via API ($0.60 / $2.40) | $8.40 | 64% |
| frontier API ($2 / $10) | $30.00 | 18% |

Self-host $ per 1M output tokens: $107.88 at 5% utilization, $21.58 at 25%, $5.39 at 100%. At $10/GPU-h
(`--gpu-hour 10`, hyperscaler-like) the open-weights comparison never breaks even (`results/breakeven_hyperscaler.md`).
Business-hours-only traffic caps an always-on replica at ~30% average utilization.

## Takeaways checklist
1. Pick the unit (ticket, document, conversation) and report $/task and $/success next to quality.
2. Shadow-price free and internal models; state the price card and its date.
3. One path to models (gateway) with team/feature attribution and budgets; test the budget and the price table.
4. Levers in order of risk: output caps → stable prefix/caching → context trimming → batch for async → smaller model
   or cascade with a *deterministic* validator → semantic caching only with validation.
5. Re-run the eval set after every lever; levers interact.
