#!/usr/bin/env python3
"""Call a Jev-style API with three tiny examples. Same code for the emulator and for real Jev.

   python jev_client.py            # run all three examples
   python jev_client.py ticket     # or: ticket | comment | approval
Config (env or .env): JEV_BASE_URL, JEV_API_KEY, JEV_MODEL  - see .env.example
Wire format: https://docs.typesafe.ai/api/system-one.md
"""
import json, os, sys, time
import requests


def load_env():
    p = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(p):
        for line in open(p):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def ask(state, questions):
    base = os.environ.get("JEV_BASE_URL", "http://127.0.0.1:8787").rstrip("/")
    t0 = time.perf_counter()
    r = requests.post(f"{base}/v1/systemone", timeout=120,
        headers={"Authorization": f"Bearer {os.environ.get('JEV_API_KEY', 'anything')}"},
        json={"model": os.environ.get("JEV_MODEL", "jev-latest"), "state": state, "questions": questions})
    ms = round((time.perf_counter() - t0) * 1000)
    if r.status_code != 200:
        sys.exit(f"HTTP {r.status_code} from {base}: {r.text[:300]}")
    return r.json(), ms, base


def show(title, state, questions):
    print(f"\n=== {title} ===\nSTATE: {state if isinstance(state, str) else json.dumps(state)}")
    resp, ms, base = ask(state, questions)
    print(f"BACKEND: {base}  model={resp['model']}  ({ms} ms)")
    print(json.dumps(resp["answers"], indent=2))
    return resp["answers"]


def ticket():
    a = show("1. Route a support ticket",
        "Our API integration started returning 500 errors on every request 20 minutes ago. "
        "We can't process any customer orders until this is fixed.",
        {"department": {"type": "choice", "instructions": "Which team should handle this?",
                        "criteria": {"billing": "Payment or subscription issues",
                                     "technical": "Bugs or integration problems",
                                     "sales": "Pricing or account questions"}},
         "urgent": {"type": "noul", "instructions": "The message conveys urgency or time-sensitivity"}})
    d = a["department"]
    print(f"-> CODE decides: send to '{d['choice']}'" + ("" if d["confidence"] >= 0.7 else "  (low confidence -> ask a human)"))


def comment():
    a = show("2. Moderate a comment",
        "You are all idiots. Go read the docs before posting garbage.",
        {"toxic": {"type": "noul", "instructions": "The comment insults or attacks people"},
         "action": {"type": "choice", "instructions": "What should the moderator do?",
                    "criteria": {"allow": "Fine to publish", "review": "Borderline, a human should look",
                                 "block": "Clearly breaks the rules"}}})
    print(f"-> CODE decides: {a['action']['choice'].upper()}")


def approval():
    a = show("3. Approve or reject an expense",
        {"item": "Team lunch", "amount_usd": 42, "policy": "Meals up to $60 per person are fine.", "people": 4},
        {"within_policy": {"type": "noul", "instructions": "The expense is within the stated policy"},
         "decision": {"type": "choice", "instructions": "What should happen to this expense?",
                      "criteria": {"approve": "Within policy", "reject": "Breaks the policy",
                                   "escalate": "Unclear, a manager should decide"}}})
    print(f"-> CODE decides: {a['decision']['choice'].upper()}")


if __name__ == "__main__":
    load_env()
    which = sys.argv[1:] or ["ticket", "comment", "approval"]
    for w in which:
        {"ticket": ticket, "comment": comment, "approval": approval}[w]()
