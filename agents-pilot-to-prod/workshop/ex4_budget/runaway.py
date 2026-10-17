"""Exercise 4a: a runaway run. The order service for A-1004 always times out. Without limits an agent retries
until something else stops it; with a step budget + circuit breaker it stops early and hands off.

    python ex4_budget/runaway.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from agent.core import Budget, run_agent  # noqa: E402

Q = "Is my desk lamp order A-1004 delivered? Keep trying until you get an answer, it's important."
for label, b in [("loose  (20 steps, no breaker)", Budget(max_steps=20, max_same_failure=99, max_seconds=300, max_cost_usd=1)),
                 ("strict (6 steps, breaker after 2 identical failures)", Budget())]:
    r = run_agent(Q, "C1", guards=True, budget=b, tags={"exercise": "ex4-runaway"})
    print(f"{label}: stopped={r.stopped} steps={r.steps} tool_calls={len(r.tool_calls)} "
          f"tokens={r.input_tokens + r.output_tokens} shadow=${r.cost_usd:.5f} latency={r.latency_s:.1f}s")
    print(f"   ShopBot: {r.answer[:150]}")
