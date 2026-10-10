"""Exercise 4 (optional, needs provider keys) - same question to real decision APIs.

Sends one ticket to every provider whose key is set and prints the raw typed answers.
Request shapes follow the public docs checked on 2026-10-10:
  - TypeSafe Jev:   POST https://api.typesafe.ai/v1/systemone  (state + questions map; noul/choice/score)
  - OpenAI:         POST https://api.openai.com/v1/decisions    (input + questions array; predicate/choice/score)
  - Cloudflare Clef: Workers AI, '@cf/cloudflare/clef-flash' - described as Jev-API compatible
    (exact Workers AI request body NOT verified by us; see research.md).
Providers without keys are skipped. No free tier is confirmed for any of them.
"""
import os, sys, json, pathlib, requests
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import common  # noqa: F401  (loads .env)

TICKET = "I was charged twice for my March invoice and nobody answers. Refund today please."
OPTS = ["billing", "technical", "account", "sales", "other"]


def jev():
    return requests.post("https://api.typesafe.ai/v1/systemone", timeout=30,
        headers={"Authorization": f"Bearer {os.environ['TYPESAFE_API_KEY']}"},
        json={"model": "jev-latest", "state": TICKET, "questions": {
            "route": {"type": "choice", "instructions": "Which team should own this ticket?", "options": OPTS},
            "urgent": {"type": "noul", "instructions": "Is this ticket urgent?"}}}).json()


def openai_decisions():
    return requests.post("https://api.openai.com/v1/decisions", timeout=30,
        headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
        json={"model": "gpt-6-luna", "input": TICKET, "questions": [
            {"type": "choice", "name": "route", "instructions": "Which team should own this ticket?",
             "choices": [{"value": o} for o in OPTS]},
            {"type": "predicate", "name": "urgent", "instructions": "Is this ticket urgent?"}]}).json()


def clef():
    acc = os.environ["CLOUDFLARE_ACCOUNT_ID"]
    # UNVERIFIED body shape: assumed Jev-compatible per Cloudflare's changelog. Check the model page first.
    return requests.post(f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/run/@cf/cloudflare/clef-flash",
        timeout=30, headers={"Authorization": f"Bearer {os.environ['CLOUDFLARE_API_TOKEN']}"},
        json={"state": TICKET, "questions": {
            "route": {"type": "choice", "instructions": "Which team should own this ticket?", "options": OPTS}}}).json()


for name, fn, key in [("jev", jev, "TYPESAFE_API_KEY"), ("openai", openai_decisions, "OPENAI_API_KEY"),
                      ("clef", clef, "CLOUDFLARE_API_TOKEN")]:
    if not os.environ.get(key):
        print(f"[skip] {name}: {key} not set"); continue
    try:
        print(f"== {name}\n" + json.dumps(fn(), indent=2)[:2000])
    except Exception as e:  # keep the workshop going if one provider fails
        print(f"[error] {name}: {e}")
