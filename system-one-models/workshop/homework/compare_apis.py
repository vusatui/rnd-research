"""Homework (optional, needs provider keys) - the same ticket to every decision API you have a key for.

Sends one ticket to every provider whose key is set and prints the raw typed answers.
Jev is also reachable through OpenRouter (Exercises 1 and 2 use that path); this file is for direct keys.
Then the real homework: add your provider as a method in ex2_confidence/methods.py, run it on the same
150 test tickets and compare it with `python eval.py --reliability` and ex3_fast_first/economics.py.
Request shapes follow the public docs checked on 2026-10-10:
  - TypeSafe Jev:   POST https://api.typesafe.ai/v1/systemone  (state + questions map; noul/choice/score)
  - OpenAI:         POST https://api.openai.com/v1/decisions    (input + questions array; predicate/choice/score)
  - Cloudflare Clef: Workers AI, '@cf/cloudflare/clef-flash' - described as Jev-API compatible
    (exact Workers AI request body NOT verified by us; see research.md).
Providers without keys are skipped. No free tier is confirmed for any of them.
"""
import os, sys, json, pathlib, requests
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import DEPARTMENTS  # also loads .env

TICKET = "I was charged twice for my March invoice and nobody answers. Refund today please."
OPTS = ["billing", "technical", "account", "sales", "other"]


def jev():
    return requests.post("https://api.typesafe.ai/v1/systemone", timeout=30,
        headers={"Authorization": f"Bearer {os.environ['TYPESAFE_API_KEY']}"},
        json={"model": "jev-latest", "state": TICKET, "questions": {
            "route": {"type": "choice", "instructions": "Which team should own this ticket?", "criteria": DEPARTMENTS},
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
            "route": {"type": "choice", "instructions": "Which team should own this ticket?", "criteria": DEPARTMENTS}}}).json()


for name, fn, keys in [("jev", jev, ["TYPESAFE_API_KEY"]), ("openai", openai_decisions, ["OPENAI_API_KEY"]),
                       ("clef", clef, ["CLOUDFLARE_ACCOUNT_ID", "CLOUDFLARE_API_TOKEN"])]:
    missing = [k for k in keys if not os.environ.get(k)]
    if missing:
        print(f"[skip] {name}: {', '.join(missing)} not set"); continue
    try:
        print(f"== {name}\n" + json.dumps(fn(), indent=2)[:2000])
    except Exception as e:  # keep the workshop going if one provider fails
        print(f"[error] {name}: {e}")
