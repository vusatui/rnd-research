"""Support-ticket reply pipeline with switchable cost levers.

One task = one customer ticket -> JSON {category, reply, sources, confidence}. Levers:
- model:   large vs small (routing)
- context: full knowledge base vs top-3 retrieved sections (context trimming)
- prefix:  'dynamic' puts a timestamp + ticket id at the top of the system prompt (a common pattern that defeats
           prefix caching); 'stable' keeps the system prompt byte-identical and moves dynamic data to the user turn
- style:   verbose vs concise instructions + max_tokens (output length control)
- cascade: answer with the small model, escalate to the large model only if a cheap validator rejects the answer
"""
from __future__ import annotations

import json
import re
import time
import uuid
from pathlib import Path

from common import llm
from common.ledger import record

from .checks import parse, score
from .retrieval import full_kb, sections, top_k

TICKETS = Path(__file__).parent / "tickets.jsonl"
CATEGORIES = ["billing", "account", "technical", "data_privacy", "sales"]

INSTRUCTIONS = f"""You are the customer-support assistant of Ledgerly, an invoicing SaaS.
Answer the customer's ticket using ONLY the knowledge base below. Never invent policies, prices, dates or promises.
If the knowledge base says support must not do something (for example disable 2FA on request, promise a release
date, or speculate about an outage), follow it. Mention concrete numbers and steps from the knowledge base.

Return ONLY a JSON object, no markdown fences:
{{"category": one of {CATEGORIES}, "reply": "<the reply to the customer>",
 "sources": [<ids of the knowledge-base sections you used, e.g. "billing">], "confidence": <0.0-1.0>}}
"""
STYLE = {
    "verbose": "Write a thorough, warm reply: restate the customer's problem, explain every relevant policy in detail, "
               "walk through all the steps, and add any helpful extra tips and context you can think of.",
    "concise": "Write a short reply: at most 80 words, only what the customer needs, no greetings or sign-offs.",
}

CONFIGS: dict[str, dict] = {
    "A_baseline":   dict(model="large", context="full", prefix="dynamic", style="verbose", max_tokens=1500),
    "B_concise":    dict(model="large", context="full", prefix="dynamic", style="concise", max_tokens=350),
    "C_stable":     dict(model="large", context="full", prefix="stable", style="concise", max_tokens=350),
    "D_trim":       dict(model="large", context="top3", prefix="stable", style="concise", max_tokens=350),
    "E_small_dyn":  dict(model="small", context="full", prefix="dynamic", style="concise", max_tokens=350),
    "F_small_full": dict(model="small", context="full", prefix="stable", style="concise", max_tokens=350),
    "G_small_trim": dict(model="small", context="top3", prefix="stable", style="concise", max_tokens=350),
    "H_cascade":    dict(cascade=("F_small_full", "D_trim")),                     # validator: format + confidence
    "I_cascade_grounded": dict(cascade=("F_small_full", "D_trim"), grounded=True),  # + numbers must exist in KB
}


def load_tickets(only: list[str] | None = None) -> list[dict]:
    ts = [json.loads(line) for line in TICKETS.read_text().splitlines() if line.strip()]
    return [t for t in ts if not only or t["id"] in only]


def build_messages(ticket: dict, cfg: dict) -> list[dict]:
    if cfg["context"] == "full":
        kb = full_kb()
    else:
        kb = "\n\n".join(sections()[s] for s in top_k(ticket["text"], 3))
    dynamic = f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S')}. Ticket ID: {ticket['id']}. Session: {uuid.uuid4()}."
    body = f"{INSTRUCTIONS}\n{STYLE[cfg['style']]}\n\n# KNOWLEDGE BASE\n\n{kb}"
    if cfg["prefix"] == "dynamic":
        return [{"role": "system", "content": f"{dynamic}\n\n{body}"},
                {"role": "user", "content": ticket["text"]}]
    return [{"role": "system", "content": body},
            {"role": "user", "content": f"[{dynamic}]\n\n{ticket['text']}"}]


def model_id(tier: str) -> str:
    return llm.LARGE if tier == "large" else llm.SMALL


def _nums(text: str) -> set[str]:
    """Numbers with their unit marker kept: '$5,000' -> '$5000', '30 %' -> '30%', '14' -> '14'.
    Keeping '$' matters: the KB mentions '5,000 files' but never '$5,000'."""
    out = set()
    for cur, n, pct in re.findall(r"([$€£]?)\s?(\d[\d,]*(?:\.\d+)?)\s?(%?)", text):
        out.add(f"{cur}{n.replace(',', '').rstrip('.')}{pct}")
    return out


def ungrounded_numbers(reply: str, ticket_text: str) -> set[str]:
    """Numbers in the reply (prices, limits, days) that appear neither in the knowledge base nor in the ticket."""
    return _nums(reply) - _nums(full_kb()) - _nums(ticket_text)


def validate(raw: str, ticket: dict | None = None, grounded: bool = False) -> tuple[bool, str]:
    """Cheap validator used by the cascade (no gold labels, no extra LLM call)."""
    d = parse(raw)
    if d is None:
        return False, "invalid JSON"
    if str(d.get("category", "")).lower() not in CATEGORIES:
        return False, "unknown category"
    src = d.get("sources") or []
    if not src or not set(src) <= set(sections()):
        return False, "no/unknown sources"
    try:
        if float(d.get("confidence", 0)) < 0.75:
            return False, "low confidence"
    except (TypeError, ValueError):
        return False, "bad confidence"
    if grounded and ticket is not None:
        bad = ungrounded_numbers(d["reply"], ticket["text"])
        if bad:
            return False, f"ungrounded numbers {sorted(bad)}"
    return True, "ok"


def cfg_second(parent: str) -> str | None:
    return CONFIGS[parent].get("cascade", (None, None))[1]


def answer(ticket: dict, config: str, run: str, team: str = "support", parent: str | None = None) -> dict:
    cfg = CONFIGS[config]
    if "cascade" in cfg:
        first, second = cfg["cascade"]
        r1 = answer(ticket, first, run, team, parent=config)
        ok, why = validate(r1["raw"], ticket, cfg.get("grounded", False))
        if ok:
            return {**r1, "config": config, "escalated": False, "why": why}
        r2 = answer(ticket, second, run, team, parent=config)
        return {**r2, "config": config, "escalated": True, "why": why,
                "usd_twin": r1["usd_twin"] + r2["usd_twin"], "usd_frontier": r1["usd_frontier"] + r2["usd_frontier"],
                "input_tokens": r1["input_tokens"] + r2["input_tokens"],
                "cached_tokens": r1["cached_tokens"] + r2["cached_tokens"],
                "output_tokens": r1["output_tokens"] + r2["output_tokens"],
                "latency_s": r1["latency_s"] + r2["latency_s"], "calls": 2}
    msgs = build_messages(ticket, cfg)
    try:
        raw, usage = llm.chat(msgs, model_id(cfg["model"]), max_tokens=cfg["max_tokens"])
    except Exception as e:  # noqa: BLE001 - a failed call is a failed task, recorded as such
        return {"ticket": ticket["id"], "config": config, "raw": "", "error": f"{type(e).__name__}: {str(e)[:200]}",
                "usd_twin": 0.0, "usd_frontier": 0.0, "input_tokens": 0, "cached_tokens": 0, "output_tokens": 0,
                "latency_s": 0.0, "calls": 1, "score": score(ticket, "")}
    row = record(usage, run=run, config=f"{parent}>{config}" if parent else config, task_id=ticket["id"], team=team,
                 step="escalation" if parent and config == cfg_second(parent) else "answer")
    return {"ticket": ticket["id"], "config": config, "raw": raw, "model": usage.model,
            "usd_twin": row["usd_twin"], "usd_frontier": row["usd_frontier"], "input_tokens": usage.input_tokens,
            "cached_tokens": usage.cached_tokens, "output_tokens": usage.output_tokens,
            "finish_reason": usage.finish_reason, "latency_s": usage.latency_s, "calls": 1,
            "score": score(ticket, raw)}
