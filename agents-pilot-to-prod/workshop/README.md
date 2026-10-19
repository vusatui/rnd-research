# Workshop: take a pilot agent to production readiness

A deliberately small customer-support agent (**ShopBot**: orders, refunds, help-center search, human hand-off) is
taken through the four things a production-readiness review asks for: **tracing**, an **eval suite with a
regression gate**, **guardrails** and a **cost/latency budget**. Everything runs on free OpenRouter models and
self-hosted open-source tools (Arize Phoenix in Docker). Measured results: [`../workshop-plan.md`](../workshop-plan.md).
**Participants: start with [`PARTICIPANTS.md`](PARTICIPANTS.md)** (step-by-step guide with expected outputs).

```
agent/          ShopBot: core loop (core.py), raw tools (tools.py), guardrails (guards.py), prompts v1/v2, fake back office
common/         OpenRouter client (fallbacks, retries, reasoning off, 20 rpm throttle), OTel setup, shadow pricing
ex1_tracing/    demo.py (3 traced runs), summarize.py (span trees from out/traces.jsonl)
ex2_evals/      dataset.jsonl (12 cases), checks.py, run_evals.py (+ gate), judge_bias.py + judge_pairs.jsonl
ex3_guardrails/ attacks.jsonl (9 attacks), run_redteam.py (ASR per config + input-guard false positives)
ex4_budget/     runaway.py (step budget + circuit breaker), report.py (pass rate vs latency vs $)
observability/  up.sh - Phoenix container (UI + OTLP on 127.0.0.1:6006)
ci/             agent-evals.yml - example GitHub Actions gate (not active)
tests/          offline tests with a scripted fake LLM (no network)
```

## Setup

```bash
cd agents-pilot-to-prod/workshop
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
cp .env.example .env            # put your free OpenRouter key in .env (https://openrouter.ai/keys); never commit it
python -m pytest -q tests       # offline, no key needed
python list_free_models.py      # free models with tool support + paid-twin price (used for shadow cost)
python check_quota.py           # free-model requests left today on your key
./observability/up.sh           # optional: Phoenix UI on http://127.0.0.1:6006 (needs Docker)
```

Free-tier limits (OpenRouter docs): 20 requests/min; 50 requests/day if you bought <10 credits, 1,000/day otherwise.
The full workshop uses ~500 requests; with the 50/day tier run each exercise with `--repeats 1` and `--only`, and
re-score the committed runs offline: `python ex2_evals/run_evals.py --rescore results/evals_v2.json`.

## Exercises

```bash
# 1. Tracing
python run_agent.py "Where is my order A-1001?" --guards
python ex1_tracing/demo.py && python ex1_tracing/summarize.py --last 3

# 2. Evals + regression gate
python ex2_evals/run_evals.py --prompt v1 --repeats 2 --save-baseline   # baseline
python ex2_evals/run_evals.py --prompt v2 --repeats 2                   # "small prompt tweak" -> GATE: FAIL
python ex2_evals/run_evals.py --prompt v2 --guards --repeats 2          # same tweak behind guardrails
python ex2_evals/judge_bias.py --judges nvidia/nemotron-3-super-120b-a12b:free

# 3. Guardrails / red team
python run_agent.py "Any community tips about late parcels?"            # indirect prompt injection, no guards
python run_agent.py "Any community tips about late parcels?" --guards
python ex3_guardrails/run_redteam.py --configs none,policy,policy+in --repeats 2

# 4. Budgets
python ex4_budget/runaway.py
python ex4_budget/report.py --conversations-per-month 100000
```

Notes
- Free models are non-deterministic and rotate; results vary run to run - that is why the evals repeat runs.
- Traces contain prompts, tool arguments and customer data (`CAPTURE_CONTENT=0` drops content); Phoenix is bound to localhost.
- `.env` is git-ignored; `out/` (traces, results) is git-ignored; curated results are copied to `results/`.
