# Workshop: make an LLM feature's bill visible, attributable and smaller

A small support-reply feature for a fictional SaaS (**Ledgerly**: 10-section knowledge base, 16 customer tickets with
deterministic checks) is used to measure what each cost lever really does to **$ per task** and **quality**, to put a
self-hosted gateway with per-team budgets in front of it, and to produce a FOCUS-shaped chargeback file.
Everything runs on **free OpenRouter models** (reasoning, retries and provider fallbacks disabled) plus open-source
LiteLLM + Postgres in Docker. Measured results: [`../workshop-plan.md`](../workshop-plan.md).

**Shadow cost.** Free calls cost $0, which hides the problem. Every call is priced twice from published list prices:
- *twin*: the paid OpenRouter endpoint of the same model (fetched live from `/api/v1/models`, snapshot in
  `results/prices_snapshot.json`);
- *frontier*: a paid frontier price card - large = gpt-6.1-sol $2.00 in / $0.10 cached / $2.50 cache write / $10.00
  out per 1M tokens, small = gpt-6-luna $0.10 / $0.01 / $0.125 / $0.50 (platform.openai.com/docs/pricing, read
  2026-10-19). Change them in `common/pricing.py`.

```
app/            kb/ (10 markdown sections), tickets.jsonl (16 tickets + checks), retrieval.py (BM25), checks.py, pipeline.py (configs A-I)
common/         llm.py (OpenRouter client, no fallback/retries, reasoning off, 18 rpm throttle), pricing.py, ledger.py, summary.py
ex2_levers/     run_levers.py (configs x tickets -> pass rate, tokens, $/task, $/success, monthly), cache_probe.py, caching_sim.py
ex3_semantic_cache/ pairs.jsonl (12 paraphrases + 12 near-misses), semantic_cache.py (embeddings or --lexical)
ex4_gateway/    up.sh / down.sh (LiteLLM v1.106.0 + Postgres), litellm_config.yaml, run_teams.py (team budgets), to_focus.py (FOCUS-shaped export)
ex5_breakeven/  breakeven.py (self-host vs API, all assumptions as flags)
results/        committed outputs of the runs described in workshop-plan.md
tests/          offline tests (no network)
```

## Setup

```bash
cd ai-finops/workshop
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
pip install fastembed            # optional, for ex3 with embeddings (~70 MB model download)
cp .env.example .env             # put your free OpenRouter key in .env (https://openrouter.ai/keys); never commit it
python -m pytest -q tests        # offline
python list_free_models.py       # free models + paid-twin prices
python check_quota.py            # free requests left today
```

Models (override with `LARGE_MODEL` / `SMALL_MODEL` in `.env`): large = `nvidia/nemotron-3-ultra-550b-a55b:free`,
small = `nvidia/nemotron-3.5-lightning:free`. Free-tier limits: 20 requests/min; 50/day (<$10 credits bought) or
1,000/day. The full workshop as run used ~230 requests. On the 50/day tier use `--only T01,T02,T03` and re-score the
committed runs offline (`--rescore`).

## Exercises

```bash
# 1. Lever lab: same 16 tickets, different configurations (each config = 16 calls; cascades 16-32)
python ex2_levers/run_levers.py --configs A_baseline,B_concise,D_trim,F_small_full,I_cascade_grounded
python ex2_levers/run_levers.py --rescore results/levers_A-H_2026-10-19.json     # offline, no quota
#   A_baseline   large model, whole KB, dynamic header first, verbose, max_tokens 1500
#   B_concise    + short JSON answer, max_tokens 350          C_stable  + dynamic header moved into the user turn
#   D_trim       + BM25 top-3 sections instead of the whole KB
#   E/F/G_small  small model (dynamic / stable / trimmed)    H_cascade small -> large if JSON invalid or confidence < 0.75
#   I_cascade_grounded  H + escalate if the reply contains $ / % / numbers not present in the KB or ticket

# 2. Prompt caching: does a stable prefix get cached? (sequential, small model)
python ex2_levers/cache_probe.py --n 4 --pad 1 --prefixes dynamic,stable   # ~8k-token prompt, 8 calls
python ex2_levers/caching_sim.py results/levers_A-H_2026-10-19.json --config C_stable   # provider rules, offline

# 3. Semantic cache: would a similarity threshold serve wrong answers? (offline, no LLM calls)
python ex3_semantic_cache/semantic_cache.py            # bge-small-en-v1.5 via fastembed
python ex3_semantic_cache/semantic_cache.py --lexical  # no download: char-3gram TF-IDF

# 4. Gateway: per-team budgets, model allow-lists, spend logs, FOCUS-shaped chargeback (needs Docker)
./ex4_gateway/up.sh                                   # LiteLLM on 127.0.0.1:4000, Postgres on 127.0.0.1:55432
python ex4_gateway/run_teams.py --setup               # team "support" $0.05 (large+small), "growth" $0.01 (small only)
python ex4_gateway/run_teams.py --traffic --support-max 10 --growth 2   # ~13 calls; support gets blocked
python ex4_gateway/run_teams.py --report
python ex4_gateway/to_focus.py --gateway              # FOCUS-shaped CSV + chargeback table from gateway spend logs
python ex4_gateway/to_focus.py                        # same from the local ledger (out/ledger.jsonl)
./ex4_gateway/down.sh

# 5. Self-host break-even (offline arithmetic; every assumption is a flag)
python ex5_breakeven/breakeven.py
python ex5_breakeven/breakeven.py --gpu-hour 10       # hyperscaler-like GPU price
```

## Notes
- The gateway master key in `up.sh` is a workshop placeholder; generated team keys go to `out/gateway_keys.json`
  (git-ignored). Everything listens on 127.0.0.1 only.
- In LiteLLM v1.106.0 the `openrouter/` provider prefix logged $0 for `:free` models even with custom prices, so the
  budget never tripped; the config uses the `openai/` provider with `api_base: https://openrouter.ai/api/v1` instead.
- `to_focus.py` writes FOCUS 1.4 column names plus FOCUS 1.5 *draft* properties (ModelId, TokenDirection,
  TokenCacheAction) in `SkuPriceDetails`; BilledCost is 0 (free tier) and ListCost is the shadow cost. It is not
  validated against the FOCUS validator.
