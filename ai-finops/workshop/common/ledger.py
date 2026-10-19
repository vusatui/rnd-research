"""Append-only cost ledger: one JSON line per LLM call with who/what/why attribution and shadow cost.
This is the data a chargeback report (and a FOCUS export) is built from."""
from __future__ import annotations

import json
import time
from dataclasses import asdict

from .paths import OUT
from .pricing import cost

LEDGER = OUT / "ledger.jsonl"


def record(usage, *, run: str, config: str, task_id: str, team: str = "support", feature: str = "ticket-reply",
           step: str = "answer", path=None, **extra) -> dict:
    row = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "run": run, "config": config, "task_id": task_id,
           "team": team, "feature": feature, "step": step, **asdict(usage),
           "usd_twin": cost(usage.model, usage.input_tokens, usage.output_tokens, usage.cached_tokens,
                            usage.cache_write_tokens, "twin"),
           "usd_frontier": cost(usage.model, usage.input_tokens, usage.output_tokens, usage.cached_tokens,
                                usage.cache_write_tokens, "frontier"),
           **extra}
    with open(path or LEDGER, "a") as f:
        f.write(json.dumps(row) + "\n")
    return row


def load(path=None, run: str | None = None) -> list[dict]:
    path = path or LEDGER
    if not path.exists():
        return []
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    return [r for r in rows if run is None or r["run"] == run]
