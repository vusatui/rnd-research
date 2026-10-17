"""Exercise 4b: cost/latency report from eval results (out/evals_*.json): pass rate vs p50/p95 latency vs tokens vs
shadow cost, and the projected monthly bill at a given volume if you were paying list price for the same model.

    python ex4_budget/report.py --conversations-per-month 100000
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.paths import OUT  # noqa: E402

p = argparse.ArgumentParser()
p.add_argument("--conversations-per-month", type=int, default=100_000)
a = p.parse_args()
print(f"{'label':26} {'runs':>4} {'pass':>5} {'p50 s':>6} {'p95 s':>6} {'steps':>5} {'tok/run':>7} {'$/run':>9} {'$/month':>9}")
for f in sorted(OUT.glob("evals_*.json")):
    s = json.loads(f.read_text())["summary"]
    month = s["shadow_cost_per_run_usd"] * a.conversations_per_month
    print(f"{s['label']:26} {s['runs']:>4} {s['pass_rate']:>5.2f} {s['latency_p50_s']:>6.1f} {s['latency_p95_s']:>6.1f} "
          f"{s['steps_per_run']:>5.1f} {s['tokens_per_run']:>7} {s['shadow_cost_per_run_usd']:>9.6f} {month:>9.0f}")
print(f"\n$/month = shadow cost per conversation x {a.conversations_per_month:,} (paid-twin list price on OpenRouter; "
      "excludes retries on 429s, guard-model calls, infra and people).")
