"""Exercise 1: trace a few agent runs and read them back.

    ./observability/up.sh                     # optional: Phoenix UI on http://127.0.0.1:6006
    python ex1_tracing/demo.py                # 3 runs -> out/traces.jsonl (+ Phoenix if OTLP endpoint is set)
    python ex1_tracing/summarize.py --last 3  # span trees, tokens, latency, shadow cost from the JSONL
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from agent.core import run_agent  # noqa: E402

QUESTIONS = [
    ("C1", "Where is my order A-1001?"),
    ("C1", "My headphones from order A-1001 stopped turning on after a week. Please refund the full $89 to my card."),
    ("C1", "Is my desk lamp order A-1004 delivered?"),   # flaky backend -> retries, circuit breaker
]
for cust, q in QUESTIONS:
    r = run_agent(q, cust, guards=True, tags={"exercise": "ex1"})
    print(f"{r.trace_id}  [{r.stopped}] {r.latency_s:.1f}s steps={r.steps} tools={[t['name'] for t in r.tool_calls]}")
    print(f"   ShopBot: {r.answer[:160]}")
