"""Print span trees from out/traces.jsonl - what you would otherwise look at in Phoenix/Langfuse/Jaeger.

    python ex1_tracing/summarize.py --last 3
    python ex1_tracing/summarize.py --trace <trace_id>
"""
import argparse
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.telemetry import load_spans  # noqa: E402

p = argparse.ArgumentParser()
p.add_argument("--last", type=int, default=3)
p.add_argument("--trace")
a = p.parse_args()
spans = load_spans()
by_trace = defaultdict(list)
for s in spans:
    by_trace[s["trace_id"]].append(s)
roots = sorted((s for s in spans if s["parent_id"] is None), key=lambda s: s["start"])
roots = [r for r in roots if r["trace_id"] == a.trace] if a.trace else roots[-a.last:]


def line(s):
    at = s["attributes"]
    d = f"{(s['end'] - s['start']) * 1000:7.0f} ms"
    extra = []
    if "gen_ai.usage.input_tokens" in at:
        extra.append(f"tok {at['gen_ai.usage.input_tokens']}+{at.get('gen_ai.usage.output_tokens', 0)}")
    if "app.cost.shadow_usd" in at:
        extra.append(f"${at['app.cost.shadow_usd']:.6f}")
    if at.get("gen_ai.response.model"):
        extra.append(at["gen_ai.response.model"])
    if at.get("app.guard.allowed") is False:
        extra.append(f"BLOCKED {at.get('app.guard.reason')}")
    if at.get("app.stopped"):
        extra.append(f"stopped={at['app.stopped']}")
    if s["status"] == "ERROR":
        extra.append("ERROR")
    for e in s["events"]:
        extra.append(f"event:{e['name']}")
    return f"{s['name']:32} {d}  {'  '.join(extra)}"


for r in roots:
    kids = defaultdict(list)
    for s in by_trace[r["trace_id"]]:
        kids[s["parent_id"]].append(s)
    print(f"\ntrace {r['trace_id']}  {r['attributes'].get('input.value', '')[:80]!r}")

    def walk(s, depth):
        print("  " * depth + line(s))
        for k in sorted(kids[s["span_id"]], key=lambda x: x["start"]):
            walk(k, depth + 1)
    walk(r, 1)
