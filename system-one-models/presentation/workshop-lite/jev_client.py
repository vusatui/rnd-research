#!/usr/bin/env python3
"""Call a Jev-style API with three tiny examples. Same code for the emulator and for real Jev.

   python jev_client.py            # run all three examples
   python jev_client.py ticket     # or: ticket | comment | approval
Config (env or .env): JEV_BASE_URL, JEV_API_KEY, JEV_MODEL  - see .env.example
  local emulator (default)  JEV_BASE_URL=http://127.0.0.1:8787
  real Jev via OpenRouter   JEV_BASE_URL=https://openrouter.ai/api  JEV_API_KEY=<OpenRouter key>  JEV_MODEL=jev-latest
  real Jev direct           JEV_BASE_URL=https://api.typesafe.ai    JEV_API_KEY=<TypeSafe key>
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
    print(f"QUESTIONS in ONE request: {', '.join(questions)}")
    resp, ms, base = ask(state, questions)
    u = resp.get("usage") or {}
    cost = f"  ${u['cost']:.6f}" if u.get("cost") is not None else ""
    print(f"BACKEND: {base}  model={resp['model']}  ({ms} ms, tokens in/out {u.get('input_tokens')}/{u.get('output_tokens')}{cost})")
    if "MOCK" in resp.get("model", "") or "EMULATOR" in resp.get("model", ""):
        print(f"!! {resp.get('_note', 'not Jev')}")
    print(json.dumps(resp["answers"], indent=2))
    return resp["answers"]


def p_of(a):
    """The probability to act on: the chosen option's probability (Choice/Score) or P(yes) (Noul)."""
    return a["noul"] if a["type"] == "noul" else a["probabilities"][str(a.get("choice", max(a["probabilities"], key=a["probabilities"].get)))]


def noul_band(p, yes=0.7, no=0.3):
    """Jev docs: start with 0.7 / 0.3 and give the band in between its own outcome."""
    return "yes" if p >= yes else "no" if p <= no else "unsure"


def ticket():
    a = show("1. Route a support ticket",
        "Our API integration started returning 500 errors on every request 20 minutes ago. "
        "We can't process any customer orders until this is fixed.",
        {"department": {"type": "choice", "instructions": "Which team should handle this?",
                        "criteria": {"billing": "Payment or subscription issues",
                                     "technical": "Bugs or integration problems",
                                     "sales": "Pricing or account questions"}},
         "urgent": {"type": "noul", "instructions": "The message conveys urgency or time-sensitivity"}})
    d, u = a["department"], noul_band(a["urgent"]["noul"])
    route = f"send to '{d['choice']}'" if p_of(d) >= 0.7 else "low probability -> a human picks the team"
    page = {"yes": "page the on-call engineer", "no": "normal queue", "unsure": "flag for a quick human look"}[u]
    print(f"-> CODE decides: {route}; urgency {u} -> {page}")


def comment():
    a = show("2. Moderate a comment",
        "You are all idiots. Go read the docs before posting garbage.",
        {"toxic": {"type": "noul", "instructions": "The comment insults or attacks people"},
         "action": {"type": "choice", "instructions": "What should the moderator do?",
                    "criteria": {"allow": "Fine to publish", "review": "Borderline, a human should look",
                                 "block": "Clearly breaks the rules"}}})
    act, p = a["action"]["choice"], p_of(a["action"])
    # thresholds scale with risk: blocking a user's post needs more certainty than publishing it
    need = {"block": 0.9, "allow": 0.7, "review": 0.0}[act]
    final = act if p >= need else "review"
    print(f"-> CODE decides: {final.upper()}  (model said {act} with p={p:.2f}, '{act}' needs >= {need})")


def approval():
    a = show("3. Approve or reject an expense",
        {"item": "Team lunch", "amount_usd": 42, "policy": "Meals up to $60 per person are fine.", "people": 4},
        {"within_policy": {"type": "noul", "instructions": "The expense is within the stated policy"},
         "decision": {"type": "choice", "instructions": "What should happen to this expense?",
                      "criteria": {"approve": "Within policy", "reject": "Breaks the policy",
                                   "escalate": "Unclear, a manager should decide"}}})
    dec, p, pol = a["decision"]["choice"], p_of(a["decision"]), noul_band(a["within_policy"]["noul"])
    # moving money is the risky action: approve only when both answers agree and are clear
    final = "approve" if dec == "approve" and p >= 0.9 and pol == "yes" else "reject" if dec == "reject" and p >= 0.9 else "escalate"
    print(f"-> CODE decides: {final.upper()}  (decision {dec} p={p:.2f}, within policy: {pol})")


if __name__ == "__main__":
    load_env()
    which = sys.argv[1:] or ["ticket", "comment", "approval"]
    for w in which:
        {"ticket": ticket, "comment": comment, "approval": approval}[w]()
