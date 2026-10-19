"""Run the ticket set through several lever configurations and report quality vs cost.

    python ex2_levers/run_levers.py --configs A_baseline,B_concise,C_stable,D_trim,E_small_dyn,F_small_full,G_small_trim,H_cascade
    python ex2_levers/run_levers.py --configs A_baseline --only T01,T02      # small, cheap run
    python ex2_levers/run_levers.py --rescore results/levers_<stamp>.json   # offline, no LLM calls

Writes out/levers_<stamp>.json (all raw answers + scores) and prints a markdown table.
Free-quota cost: one request per ticket per config (+1 per escalation in H_cascade).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.checks import score  # noqa: E402
from app.pipeline import CONFIGS, answer, load_tickets  # noqa: E402
from common import llm  # noqa: E402
from common.paths import OUT  # noqa: E402
from common.pricing import snapshot  # noqa: E402
from common.summary import summarize, table  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--configs", default="A_baseline")
    ap.add_argument("--only", help="comma-separated ticket ids")
    ap.add_argument("--monthly", type=int, default=100_000, help="tasks per month for the projection")
    ap.add_argument("--workers", type=int, default=4, help="parallel requests (free tier is slow; the rpm throttle is shared)")
    ap.add_argument("--rescore", help="re-score a saved run offline")
    a = ap.parse_args()

    if a.rescore:
        data = json.loads(Path(a.rescore).read_text())
        tickets = {t["id"]: t for t in load_tickets()}
        for cfg, rows in data["rows"].items():
            for r in rows:
                r["score"] = score(tickets[r["ticket"]], r.get("raw", ""))
        sums = {c: summarize(rs, a.monthly) for c, rs in data["rows"].items()}
        print(table(sums))
        return

    tickets = load_tickets(a.only.split(",") if a.only else None)
    configs = a.configs.split(",")
    for c in configs:
        if c not in CONFIGS:
            raise SystemExit(f"unknown config {c}; choose from {list(CONFIGS)}")
    stamp = time.strftime("%Y%m%d-%H%M%S")
    run = f"levers-{stamp}"
    snapshot([llm.LARGE, llm.SMALL])
    rows: dict[str, list] = {}
    for c in configs:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(a.workers) as pool:
            results = list(pool.map(lambda t: answer(t, c, run), tickets))
        rows[c] = results
        for t, r in zip(tickets, results):
            s = r["score"]
            flag = "PASS" if s["pass"] else "fail"
            extra = f" esc({r.get('why')})" if r.get("escalated") else ""
            err = f" ERROR {r['error'][:80]}" if r.get("error") else ""
            print(f"{c:13} {t['id']} {flag} in={r['input_tokens']:>5} cached={r['cached_tokens']:>5} "
                  f"out={r['output_tokens']:>4} ${r['usd_frontier']:.5f}{extra}{err} {s.get('missing') or ''}",
                  flush=True)
    sums = {c: summarize(rs, a.monthly) for c, rs in rows.items()}
    out = OUT / f"levers_{stamp}.json"
    out.write_text(json.dumps({"run": run, "models": {"large": llm.LARGE, "small": llm.SMALL},
                               "llm_calls": llm.CALLS["n"], "summary": sums, "rows": rows}, indent=1))
    print()
    print(table(sums))
    print(f"\nLLM calls: {llm.CALLS['n']}  saved: {out}")


if __name__ == "__main__":
    main()
