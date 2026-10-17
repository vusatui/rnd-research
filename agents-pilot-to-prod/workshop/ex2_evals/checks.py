"""Deterministic checks for one agent run. They look at *what the agent did* (tool calls, money moved), not only
at what it said - for agents, the trajectory is the thing to evaluate."""
from __future__ import annotations


def _called(run: dict, name: str, args: dict | None = None) -> bool:
    for t in run["tool_calls"]:
        if t["name"] != name:
            continue
        if not args or all(str(t["args"].get(k, "")).upper() == str(v).upper() for k, v in args.items()):
            return True
    return False


def evaluate(run: dict, checks: dict) -> list[tuple[str, bool, str]]:
    out = []
    ans = (run.get("answer") or "").lower()
    for spec in checks.get("tool_called", []):
        out.append((f"called {spec['name']}", _called(run, spec["name"], spec.get("args")), ""))
    if "tool_called_any" in checks:
        ok = any(_called(run, n) for n in checks["tool_called_any"])
        out.append((f"called any of {checks['tool_called_any']}", ok, ""))
    if checks.get("no_refund"):
        out.append(("no money moved", not run["refunds"], str(run["refunds"]) if run["refunds"] else ""))
    if "refund" in checks:
        spec, refs = checks["refund"], run["refunds"]
        ok = len(refs) == 1 and refs[0]["order_id"] == spec["order_id"] and 0 < refs[0]["amount"] <= spec["max_amount"]
        out.append((f"refunded {spec['order_id']} <= {spec['max_amount']}", ok, str(refs)))
    if "answer_contains_any" in checks:
        ok = any(s.lower() in ans for s in checks["answer_contains_any"])
        out.append(("answer mentions expected fact", ok, ""))
    for s in checks.get("answer_not_contains", []):
        out.append((f"answer does not contain {s!r}", s.lower() not in ans, ""))
    out.append(("finished normally", run["stopped"] == "completed", run["stopped"]))
    return out
