#!/usr/bin/env python3
"""Exercise 3 - "fast first": the threshold is a business knob, so put a price on it.

System 1  = a cheap decision with a probability (default: Jev results from Exercise 2)
Gate      = if p(answer) >= threshold -> act automatically, else escalate
System 2  = a human queue (always right, costs --review per ticket) or a stronger LLM (--s2 <method>)

For every threshold we count, per 1,000 tickets: automated share, wrong automated actions, human load,
and total cost = S1 cost + S2 cost + errors x --error-cost. Then the optimum, and the same optimum for every
other S1 method from Exercise 2: a better calibrated S1 lets you automate more at the same error rate.

  python ex3_fast_first/economics.py                         # S1=jev, S2=human, error $5, review $0.50
  python ex3_fast_first/economics.py --error-cost 20 --review 1.0
  python ex3_fast_first/economics.py --s1 votes_deepseek-v4.1-flash-1017 --s2 verbal_claude-haiku-5.5
Needs only the results/ files (committed), no key, no network.
"""
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import RESULTS

THRESHOLDS = [0.0, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99, 1.01]


def load(name):
    p = RESULTS / f"ex2_{name}.jsonl"
    if not p.exists():
        sys.exit(f"missing {p.name}: run Exercise 2 first (or use one of: {', '.join(sorted(x.stem[4:] for x in RESULTS.glob('ex2_*.jsonl')))})")
    return {r["id"]: r for r in map(json.loads, open(p))}


def simulate(s1, s2, t, err_cost, review, q="department"):
    n = len(s1)
    auto = esc = wrong_auto = wrong_s2 = 0
    cost = 0.0
    for i, r in s1.items():
        cost += r["cost"]
        if r[f"{q}_p"] >= t:
            auto += 1
            wrong_auto += r[q] != r[f"gold_{q}"]
        else:
            esc += 1
            if s2 is None:
                cost += review
            else:
                cost += s2[i]["cost"]
                wrong_s2 += s2[i][q] != s2[i][f"gold_{q}"]
    errors = wrong_auto + wrong_s2
    total = cost + errors * err_cost
    k = 1000 / n
    return {"t": t, "auto": auto / n, "errors_per_1k": errors * k, "human_per_1k": (esc if s2 is None else 0) * k,
            "s2_calls_per_1k": (esc if s2 is not None else 0) * k, "usd_per_1k": total * k,
            "accuracy": 1 - errors / n}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--s1", default="jev")
    ap.add_argument("--s2", default="human", help="'human' or an ex2 result name, e.g. verbal_claude-haiku-5.5")
    ap.add_argument("--error-cost", type=float, default=5.0, help="$ cost of one wrong automated routing")
    ap.add_argument("--review", type=float, default=0.50, help="$ cost of one human review")
    a = ap.parse_args()
    s1 = load(a.s1)
    s2 = None if a.s2 == "human" else load(a.s2)
    print(f"S1 = {a.s1}   S2 = {a.s2}   error ${a.error_cost:.2f}   review ${a.review:.2f}   ({len(s1)} test tickets, scaled to 1,000)\n")
    print(f"{'threshold':>9} {'automated':>9} {'errors':>7} {'to human':>8} {'to S2 LLM':>9} {'total $':>8}")
    rows = [simulate(s1, s2, t, a.error_cost, a.review) for t in THRESHOLDS]
    best = min(rows, key=lambda r: r["usd_per_1k"])
    for r in rows:
        mark = "  <- cheapest" if r is best else ""
        label = "never" if r["t"] > 1 else f"{r['t']:.2f}"
        print(f"{label:>9} {r['auto']:9.0%} {r['errors_per_1k']:7.0f} {r['human_per_1k']:8.0f} {r['s2_calls_per_1k']:9.0f} {r['usd_per_1k']:8.0f}{mark}")
    print("\n(threshold 0 = automate everything, 'never' = everything goes to S2)")
    print("\nSame economics, best threshold for every S1 method from Exercise 2:")
    print(f"{'S1 method':34} {'best t':>6} {'automated':>9} {'errors':>7} {'total $':>8}")
    for p in sorted(RESULTS.glob("ex2_*.jsonl")):
        name = p.stem[4:]
        other = load(name)
        b = min((simulate(other, s2, t, a.error_cost, a.review) for t in THRESHOLDS), key=lambda r: r["usd_per_1k"])
        label = "never" if b["t"] > 1 else f"{b['t']:.2f}"
        print(f"{name:34} {label:>6} {b['auto']:9.0%} {b['errors_per_1k']:7.0f} {b['usd_per_1k']:8.0f}")


if __name__ == "__main__":
    main()
