"""Does the provider actually cache our prompt? Sequential probe: the same N tickets with a stable prefix and with a
dynamic prefix (timestamp + ticket id at the top of the system prompt), one request at a time.

    python ex2_levers/cache_probe.py --n 6 --model small
    python ex2_levers/cache_probe.py --n 4 --pad 1 --prefixes stable   # ~8k-token prefix
Free-quota cost: 2 x N requests. Reports cached_tokens as returned by the provider (usage.prompt_tokens_details).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.pipeline import CONFIGS, build_messages, load_tickets, model_id  # noqa: E402
from common import llm  # noqa: E402
from common.ledger import record  # noqa: E402
from common.paths import OUT  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--model", default="small", choices=["small", "large"])
    ap.add_argument("--pad", type=int, default=0, help="append the KB N more times (longer prefix, same task)")
    ap.add_argument("--prefixes", default="dynamic,stable")
    a = ap.parse_args()
    tickets = load_tickets()[: a.n]
    run = f"cacheprobe-{time.strftime('%Y%m%d-%H%M%S')}"
    res = {}
    for prefix in a.prefixes.split(","):
        cfg = dict(CONFIGS["F_small_full"], prefix=prefix, model=a.model)
        res[prefix] = []
        for t in tickets:
            msgs = build_messages(t, cfg)
            if a.pad:
                from app.retrieval import full_kb
                msgs[0]["content"] += "".join(f"\n\n# APPENDIX {i + 1}: copy of the knowledge base\n\n{full_kb()}"
                                              for i in range(a.pad))
            try:
                _, u = llm.chat(msgs, model_id(a.model), max_tokens=cfg["max_tokens"])
            except Exception as e:  # noqa: BLE001
                print(f"{prefix:8} {t['id']} ERROR {str(e)[:120]}")
                continue
            row = record(u, run=run, config=f"probe_{prefix}_pad{a.pad}", task_id=t["id"])
            res[prefix].append({"ticket": t["id"], "input": u.input_tokens, "cached": u.cached_tokens,
                                "provider": u.provider, "usd_twin": row["usd_twin"]})
            print(f"{prefix:8} {t['id']} in={u.input_tokens} cached={u.cached_tokens} provider={u.provider} "
                  f"${row['usd_twin']:.6f}", flush=True)
    print()
    for prefix, rows in res.items():
        inp = sum(r["input"] for r in rows) or 1
        print(f"{prefix:8}: cache hit rate {sum(r['cached'] for r in rows)/inp:.0%} of input tokens, "
              f"twin cost ${sum(r['usd_twin'] for r in rows):.6f} for {len(rows)} requests")
    (OUT / f"{run}.json").write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
