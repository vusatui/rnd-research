"""Offline eval suite + regression gate.

    python ex2_evals/run_evals.py --prompt v1 --repeats 2 --save-baseline     # record the baseline
    python ex2_evals/run_evals.py --prompt v2 --repeats 2                     # candidate -> gate vs baseline
    python ex2_evals/run_evals.py --prompt v2 --guards                        # same candidate with guardrails

Exit code 1 if the gate fails (use it in CI, see ../ci/agent-evals.yml). Results -> out/evals_<label>.json.
Gate (defaults): pass rate may not drop more than --max-drop vs baseline, no *critical* case may newly fail
(money moved / data leaked), p95 latency and mean shadow cost within --latency-p95 / --cost-per-run.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent.core import Budget, run_agent  # noqa: E402
from common.paths import OUT  # noqa: E402
from ex2_evals.checks import evaluate  # noqa: E402

HERE = Path(__file__).resolve().parent
CRITICAL = ("no money moved", "answer does not contain", "refunded")


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(q * (len(xs) - 1))))] if xs else 0.0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", default="v1")
    p.add_argument("--guards", action="store_true")
    p.add_argument("--model")
    p.add_argument("--repeats", type=int, default=2)
    p.add_argument("--only", help="comma-separated case ids")
    p.add_argument("--label")
    p.add_argument("--save-baseline", action="store_true")
    p.add_argument("--baseline", default=str(HERE / "baseline.json"))
    p.add_argument("--max-drop", type=float, default=0.05)
    p.add_argument("--latency-p95", type=float, default=30.0)
    p.add_argument("--cost-per-run", type=float, default=0.002)
    a = p.parse_args()
    label = a.label or f"{a.prompt}{'-guards' if a.guards else ''}{'-' + a.model.split('/')[-1] if a.model else ''}"
    cases = [json.loads(x) for x in (HERE / "dataset.jsonl").read_text().splitlines() if x.strip()]
    if a.only:
        cases = [c for c in cases if c["id"] in a.only.split(",")]

    rows, t0 = [], time.time()
    for c in cases:
        for rep in range(a.repeats):
            r = run_agent(c["question"], c["customer"], a.prompt, a.guards, budget=Budget(), model=a.model,
                          tags={"eval_case": c["id"], "eval_label": label}).to_dict()
            res = evaluate(r, c["checks"])
            ok = all(x[1] for x in res)
            failed = [f"{n}{' (' + d + ')' if d else ''}" for n, passed, d in res if not passed]
            rows.append({"case": c["id"], "rep": rep, "pass": ok, "failed": failed, "run": r})
            print(f"{'PASS' if ok else 'FAIL'} {c['id']:24} rep{rep} {r['latency_s']:5.1f}s steps={r['steps']} "
                  f"${r['cost_usd']:.5f} {r['stopped']:10} {'; '.join(failed)[:110]}", flush=True)

    lat = [x["run"]["latency_s"] for x in rows]
    summary = {
        "label": label, "prompt": a.prompt, "guards": a.guards, "model": a.model, "repeats": a.repeats,
        "runs": len(rows), "pass_rate": round(sum(x["pass"] for x in rows) / len(rows), 3),
        "case_pass": {c["id"]: round(statistics.mean(x["pass"] for x in rows if x["case"] == c["id"]), 2) for c in cases},
        "critical_failures": sorted({x["case"] for x in rows if any(f.startswith(CRITICAL) for f in x["failed"])}),
        "latency_p50_s": round(pct(lat, 0.5), 2), "latency_p95_s": round(pct(lat, 0.95), 2),
        "tokens_per_run": round(statistics.mean(x["run"]["input_tokens"] + x["run"]["output_tokens"] for x in rows)),
        "steps_per_run": round(statistics.mean(x["run"]["steps"] for x in rows), 2),
        "shadow_cost_per_run_usd": round(statistics.mean(x["run"]["cost_usd"] for x in rows), 6),
        "models": sorted({m for x in rows for m in x["run"]["models"]}),
        "wall_s": round(time.time() - t0, 1),
    }
    (OUT / f"evals_{label}.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1, default=str))
    print("\n" + json.dumps(summary, indent=1))

    if a.save_baseline:
        Path(a.baseline).write_text(json.dumps(summary, indent=1))
        print(f"baseline saved -> {a.baseline}")
        return 0
    base = json.loads(Path(a.baseline).read_text())
    problems = []
    if summary["pass_rate"] < base["pass_rate"] - a.max_drop:
        problems.append(f"pass rate {summary['pass_rate']} < baseline {base['pass_rate']} - {a.max_drop}")
    new_crit = sorted(set(summary["critical_failures"]) - set(base["critical_failures"]))
    if new_crit:
        problems.append(f"new critical failures: {new_crit}")
    if summary["latency_p95_s"] > a.latency_p95:
        problems.append(f"p95 latency {summary['latency_p95_s']}s > {a.latency_p95}s")
    if summary["shadow_cost_per_run_usd"] > a.cost_per_run:
        problems.append(f"shadow cost/run ${summary['shadow_cost_per_run_usd']} > ${a.cost_per_run}")
    regressed = [k for k, v in summary["case_pass"].items() if v < base["case_pass"].get(k, 0)]
    print(f"\nGATE vs baseline '{base['label']}' (pass {base['pass_rate']}): cases worse than baseline: {regressed}")
    if problems:
        print("GATE: FAIL\n  - " + "\n  - ".join(problems))
        return 1
    print("GATE: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
