"""Shared bits for every exercise: the dataset, the label set and its descriptions.

Every method in the workshop sees the SAME department descriptions, so the comparison is about
how each method produces an answer and its confidence, not about who got the better prompt.
"""
import json, os, pathlib

ROOT = pathlib.Path(__file__).parent
RESULTS = ROOT / "results"


def _load_env():
    for p in (ROOT / ".env", ROOT.parent / ".env"):
        if p.exists():
            for line in open(p):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if v.strip():
                        os.environ.setdefault(k.strip(), v.strip())


_load_env()

DEPARTMENTS = {
    "billing": "Invoices, charges, refunds, payment methods, VAT, renewals of an existing subscription",
    "technical": "Bugs, errors, outages, API or integration problems, data not syncing, product not working",
    "account": "Login, passwords, 2FA, user seats and roles, workspace ownership, profile or email changes",
    "sales": "Buying more: pricing questions, quotes, upgrades, demos, contracts, procurement for new purchases",
    "other": "Anything else: partnerships, press, job applications, feedback with no request, spam",
}
URGENCY = {
    "low": "Can wait days: questions, nice-to-haves, no business impact",
    "medium": "Should be handled within a day: something is degraded or a deadline is near",
    "high": "Needs attention now: outage, blocked work, money or security at risk",
}


def load_tickets(split=None):
    """split: None (all), 'train' (for the classic classifier only) or 'test' (what every method is scored on)."""
    rows = [json.loads(l) for l in open(ROOT / "data" / "tickets.jsonl")]
    return [r for r in rows if split is None or r["split"] == split]


def mock_mode():
    return os.environ.get("WORKSHOP_MOCK", "").lower() in ("1", "true", "yes")
