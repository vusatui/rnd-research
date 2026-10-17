"""Raw tools of the workshop agent. They do exactly what they are asked - no authorization, no limits -
like most internal APIs that a pilot agent gets wired to. Guardrails live in agent/guards.py."""
from __future__ import annotations

import itertools
import re

from .data import KB, ORDERS

_ticket = itertools.count(1)

TOOL_SPECS = [
    {"type": "function", "function": {
        "name": "search_kb", "description": "Search the help-center knowledge base (policies, shipping, warranty, community tips).",
        "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}},
    {"type": "function", "function": {
        "name": "get_order", "description": "Get an order by id (e.g. A-1001): item, total, status, delivery date.",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}}},
    {"type": "function", "function": {
        "name": "issue_refund", "description": "Refund an order to the original payment method.",
        "parameters": {"type": "object", "properties": {
            "order_id": {"type": "string"}, "amount": {"type": "number"}, "reason": {"type": "string"}},
            "required": ["order_id", "amount", "reason"]}}},
    {"type": "function", "function": {
        "name": "escalate_to_human", "description": "Hand the conversation to a human support agent (creates a ticket).",
        "parameters": {"type": "object", "properties": {
            "reason": {"type": "string"}, "order_id": {"type": "string"}}, "required": ["reason"]}}},
]

# Which documents a query can reach. The community page is only hit by community/forum/late-parcel queries.
_KB_KEYWORDS = {
    "refund_policy": {"refund", "return", "money", "back", "window", "days", "policy", "damaged", "broken"},
    "shipping": {"ship", "shipping", "deliver", "delivery", "canada", "usa", "uk", "eu", "tracking", "country"},
    "warranty": {"warranty", "guarantee", "defect", "damaged", "broken", "repair"},
    "community_tips": {"community", "tip", "tips", "forum", "late", "parcel", "advice"},
}


class FlakyBackend(Exception):
    pass


def search_kb(query: str) -> dict:
    words = set(re.findall(r"[a-z]+", query.lower()))
    words |= {w.rstrip("s") for w in words}
    scored = sorted(((len(words & kw), name) for name, kw in _KB_KEYWORDS.items()), reverse=True)
    hits = [name for score, name in scored if score > 0][:2]
    return {"results": [{"doc": n, "text": KB[n]} for n in hits] or [{"doc": None, "text": "No matching article."}]}


def get_order(order_id: str) -> dict:
    o = ORDERS.get(order_id.strip().upper())
    if not o:
        return {"error": f"order {order_id} not found"}
    if o.get("flaky"):
        raise FlakyBackend("order service timeout (HTTP 504) - please retry")
    return {"order_id": order_id.strip().upper(), **{k: v for k, v in o.items() if k != "flaky"}}


def issue_refund(order_id: str, amount: float, reason: str, ledger: list) -> dict:
    ledger.append({"order_id": order_id, "amount": float(amount), "reason": reason})
    return {"status": "refunded", "order_id": order_id, "amount": float(amount)}


def escalate_to_human(reason: str, order_id: str | None = None) -> dict:
    return {"status": "escalated", "ticket": f"T-{next(_ticket):04d}", "order_id": order_id}
