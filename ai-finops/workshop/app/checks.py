"""Deterministic quality checks for a ticket reply (no LLM judge: cheap, repeatable, and free of judge bias)."""
from __future__ import annotations

import json
import re


def parse(raw: str) -> dict | None:
    s = raw.strip()
    m = re.search(r"\{.*\}", s, re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    return d if isinstance(d, dict) and isinstance(d.get("reply"), str) else None


def score(ticket: dict, raw: str) -> dict:
    d = parse(raw)
    if d is None:
        return {"json_ok": False, "category_ok": False, "facts_ok": False, "pass": False, "missing": ["<json>"]}
    allowed = ticket["category"].split("|")
    cat_ok = str(d.get("category", "")).strip().lower() in allowed
    reply = d["reply"]
    missing = [p for p in ticket.get("must", []) if not re.search(p, reply, re.I)]
    forbidden = [p for p in ticket.get("must_not", []) if re.search(p, reply, re.I)]
    facts_ok = not missing and not forbidden
    return {"json_ok": True, "category_ok": cat_ok, "facts_ok": facts_ok, "pass": cat_ok and facts_ok,
            "missing": missing + [f"forbidden:{p}" for p in forbidden], "words": len(reply.split()),
            "confidence": d.get("confidence"), "sources": d.get("sources")}
