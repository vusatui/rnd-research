"""Guardrails, in the order they fire:

1. input guard   - a small safety classifier (nvidia/nemotron-3.5-content-safety:free) on the user message;
2. tool policy   - deterministic checks at the tool boundary (authorization, business limits, intent binding,
                   human approval). This is the layer that still works when the model is fooled;
3. output guard  - redacts card numbers (Luhn-checked) and e-mail addresses before the reply leaves.

Only (2) gives hard guarantees. (1) and (3) are probabilistic / pattern based.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date

from .data import APPROVAL_THRESHOLD_USD, CUSTOMERS, ORDERS, REFUND_WINDOW_DAYS, TODAY


@dataclass
class Decision:
    allowed: bool
    reason: str = ""
    replacement: dict | None = None   # result to return to the model instead of running the tool


@dataclass
class Session:
    customer_id: str
    user_messages: list = field(default_factory=list)


def _norm(oid: str) -> str:
    return (oid or "").strip().upper()


def tool_policy(name: str, args: dict, s: Session) -> Decision:
    if name in ("get_order", "issue_refund"):
        oid = _norm(args.get("order_id"))
        o = ORDERS.get(oid)
        if o and o["customer"] != s.customer_id:
            # Do not confirm that someone else's order exists.
            return Decision(False, "authz:not_owner", {"error": f"order {oid} not found"})
    if name == "issue_refund":
        oid = _norm(args.get("order_id"))
        o = ORDERS.get(oid)
        if not o:
            return Decision(False, "refund:unknown_order", {"error": f"order {oid} not found"})
        # Intent binding: the *user* must have mentioned this order in this conversation. Instructions that only
        # appear in tool output (retrieved documents, e-mails, web pages) cannot trigger a money movement.
        if not any(oid in _norm(m) for m in s.user_messages):
            return Decision(False, "refund:intent_not_bound_to_user",
                            {"error": "refund blocked: the customer did not request a refund for this order"})
        if o["status"] != "delivered":
            return Decision(False, "refund:not_delivered", {"error": "refund not allowed: order not delivered yet"})
        age = (TODAY - date.fromisoformat(o["delivered_on"])).days
        if age > REFUND_WINDOW_DAYS:
            return Decision(False, "refund:outside_window",
                            {"error": f"refund not allowed: delivered {age} days ago (window {REFUND_WINDOW_DAYS})"})
        amount = float(args.get("amount") or 0)
        if amount <= 0 or amount > o["total"]:
            return Decision(False, "refund:bad_amount", {"error": f"refund amount must be in (0, {o['total']}]"})
        if amount > APPROVAL_THRESHOLD_USD:
            return Decision(False, "refund:needs_human_approval",
                            {"status": "pending_human_approval",
                             "message": f"Refunds above ${APPROVAL_THRESHOLD_USD:.0f} need a human agent. "
                                        "A ticket was created; tell the customer a human will confirm."})
    return Decision(True)


_PAN = re.compile(r"\b(?:\d[ -]?){12,18}\d\b")
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")


def _luhn(digits: str) -> bool:
    total, alt = 0, False
    for d in reversed(digits):
        n = int(d)
        if alt:
            n = n * 2 - 9 if n > 4 else n * 2
        total, alt = total + n, not alt
    return total % 10 == 0


def redact_output(text: str, s: Session) -> tuple[str, list[str]]:
    hits = []

    def pan(m):
        digits = re.sub(r"\D", "", m.group(0))
        if _luhn(digits):
            hits.append("pan")
            return f"[card ending {digits[-4:]}]"
        return m.group(0)

    def email(m):
        own = CUSTOMERS.get(s.customer_id, {}).get("email")
        if m.group(0).lower() == (own or "").lower():
            return m.group(0)
        hits.append("email")
        return "[redacted e-mail]"

    return _EMAIL.sub(email, _PAN.sub(pan, text or "")), hits


SAFETY_MODEL = "nvidia/nemotron-3.5-content-safety:free"


def input_guard(text: str) -> tuple[bool, str, float]:
    """Returns (safe, raw_verdict, latency_s). Fails open on errors (logged) - a deliberate, visible choice."""
    from common.llm import chat
    try:
        r = chat([{"role": "user", "content": text}], model=SAFETY_MODEL, fallback=False, max_tokens=60)
        verdict = (r.message.content or "").strip()
        return ("unsafe" not in verdict.lower().split("\n")[0]), verdict, r.latency_s
    except Exception as e:  # noqa: BLE001
        return True, f"guard_error: {e}"[:200], 0.0
