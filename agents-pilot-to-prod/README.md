# AI agents from pilot to production: governance, evals, observability

Why agent pilots stall at the security / legal / risk review, what enterprise clients actually ask for, and the
minimum engineering kit that gets an agent through: proportional governance, OpenTelemetry tracing, evals with a
regression gate, guardrails at the tool boundary, and cost/latency budgets. With a runnable workshop that takes a
small support agent through all of it on free models and self-hosted tools, with measured results.

- [`research.md`](research.md) - sources (checked 2026-10-17) with ✅/🟡/🟠/❌/🧪 markers: demand signals and disputed
  statistics, governance by autonomy level, OTel GenAI semantic conventions, OWASP Agentic Top 10, LLM-as-judge
  pitfalls, cost/latency, EU AI Act timeline after the Digital Omnibus, consensus vs disputed, open items
- [`comparison.md`](comparison.md) - Langfuse, Arize Phoenix, LangSmith, Braintrust, Opik, MLflow, OpenAI tracing/evals,
  Promptfoo, Inspect, DeepEval, NeMo Guardrails, Guardrails AI, LLM Guard, safety classifiers, AWS AgentCore,
  Microsoft Agent 365; licenses, self-hosting, OTel support, ownership changes; decision guide
- [`talk-outline.md`](talk-outline.md) - ~35 min talk, 9 segments with timing
- [`workshop-plan.md`](workshop-plan.md) + [`workshop/`](workshop/) - 4 exercises (tracing, evals + gate, guardrails /
  red team, budgets) with real run results

Quick start:

```bash
cd workshop
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python -m pytest -q tests                  # offline, no key
cp .env.example .env                       # add a free OpenRouter key
./observability/up.sh                      # optional: Phoenix trace UI on http://127.0.0.1:6006
python run_agent.py "Any community tips about late parcels?" --guards
python ex2_evals/run_evals.py --prompt v2 --repeats 2   # regression gate vs the committed baseline
```

Status: In progress (2026-10-17). Research, comparison, talk outline, workshop and workshop plan done; talk script and
HTML slides next.
