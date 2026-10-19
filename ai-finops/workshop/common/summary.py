"""Aggregate per-task results into the numbers a FinOps review asks for."""
from __future__ import annotations

import statistics


def summarize(rows: list[dict], monthly_tasks: int = 100_000) -> dict:
    n = len(rows)
    passed = sum(r["score"]["pass"] for r in rows)
    usd = sum(r["usd_twin"] for r in rows)
    usd_f = sum(r["usd_frontier"] for r in rows)
    inp = sum(r["input_tokens"] for r in rows)
    cached = sum(r["cached_tokens"] for r in rows)
    return {
        "tasks": n, "passed": passed, "pass_rate": round(passed / n, 3) if n else 0,
        "errors": sum(1 for r in rows if r.get("error")),
        "calls": sum(r.get("calls", 1) for r in rows),
        "escalated": sum(1 for r in rows if r.get("escalated")),
        "avg_input_tokens": round(inp / n) if n else 0,
        "cache_hit_rate": round(cached / inp, 3) if inp else 0,
        "avg_output_tokens": round(sum(r["output_tokens"] for r in rows) / n) if n else 0,
        "usd_per_task_twin": usd / n if n else 0,
        "usd_per_task_frontier": usd_f / n if n else 0,
        "usd_per_success_twin": usd / passed if passed else None,
        "usd_per_success_frontier": usd_f / passed if passed else None,
        "usd_month_twin": usd / n * monthly_tasks if n else 0,
        "usd_month_frontier": usd_f / n * monthly_tasks if n else 0,
        "p50_latency_s": round(statistics.median(r["latency_s"] for r in rows), 2) if n else 0,
    }


def table(summaries: dict[str, dict], base: str | None = None) -> str:
    base = base or next(iter(summaries))
    b = summaries[base]
    lines = ["| config | pass | avg in tok | cache hit | avg out tok | $/task (twin) | $/task (frontier) | "
             "$/success (frontier) | vs base (frontier) | p50 s | calls |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for name, s in summaries.items():
        rel = (s["usd_per_task_frontier"] / b["usd_per_task_frontier"] - 1) if b["usd_per_task_frontier"] else 0
        ps = s["usd_per_success_frontier"]
        lines.append(f"| {name} | {s['passed']}/{s['tasks']} | {s['avg_input_tokens']:,} | {s['cache_hit_rate']:.0%} | "
                     f"{s['avg_output_tokens']} | ${s['usd_per_task_twin']:.6f} | ${s['usd_per_task_frontier']:.5f} | "
                     f"{'$%.5f' % ps if ps else 'n/a'} | {rel:+.0%} | {s['p50_latency_s']} | {s['calls']} |")
    return "\n".join(lines)
