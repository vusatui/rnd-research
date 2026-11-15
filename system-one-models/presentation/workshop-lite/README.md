# Workshop-lite = Exercise 1: one call, several questions, your code decides

Goal: see with your own eyes what a **System One / decision model** call looks like: *text in, typed answer + probabilities out, no generated text*.

You need **Docker and make** (recommended, nothing else to install) or Python 3.10+. For the free path you also need a free OpenRouter key; without one the demo still runs in a clearly labelled offline MOCK mode.

## Quick start with Docker

Run from `system-one-models/` (two folders up from here):

```bash
cd system-one-models
cp .env.example .env     # paste your free OPENROUTER_API_KEY (https://openrouter.ai/keys)
make lite                # builds the image, starts the emulator, runs all 3 examples
make lite EX=ticket      # just one: ticket | comment | approval
make lite-mock           # fully offline: no key, no network (MOCK keyword rules, NOT an LLM)
```

The plain-curl example: `make emulator` in one terminal, `make curl` in another (curl also runs in Docker). `make help` lists every target.

Which engine answered is always printed in `model=`:

| `model=` says | What answered |
|---|---|
| `EMULATOR(<free model>, 5 votes)` | the free OpenRouter LLM, 5 calls, each answering **all** questions of the request (still **not** Jev) |
| `typesafe/jev-1.14-…` | **real Jev** (`make lite-jev`, via OpenRouter) |
| `EMULATOR(<free model>)+MOCK-FALLBACK` | the free LLM failed (rate limit, no network), so offline keyword rules answered; a `!!` line says which questions |
| `MOCK-EMULATOR(offline keyword rules)` | `make lite-mock` / `MOCK=1`: no LLM at all, deterministic rules for demos and CI |

`make lite` falls back to MOCK on failure so a live demo never dies on stage; use `make lite FALLBACK=` to get the error instead. The mock answers are hand-written keyword rules: they show the wire format and the "code decides" step, nothing about model quality.

## Which backend are you talking to? (read this first)

All three options use the **same client code** and the same Jev wire format (`POST /v1/systemone`, see the [official API reference](https://docs.typesafe.ai/api/system-one.md)). Only the URL and key change.

| # | Backend | Cost | `JEV_BASE_URL` | `JEV_API_KEY` | Status for this workshop |
|---|---|---|---|---|---|
| A | **Local emulator** (default): a free chat LLM on OpenRouter behind a Jev-shaped endpoint. **This is NOT Jev.** | free | `http://127.0.0.1:8787` | anything | ✅ tested, outputs below |
| B | **Real Jev** at TypeSafe | paid, [$0.042 / 1M input tokens, output free](https://docs.typesafe.ai/models.md) | `https://api.typesafe.ai` | key from [console.typesafe.ai/keys](https://console.typesafe.ai/keys) | not tested (no TypeSafe key); same wire format as C |
| C | **Real Jev via OpenRouter** (billed to your OpenRouter account, `model: jev-latest`) | paid, same price | `https://openrouter.ai/api` | an OpenRouter key with credits | ✅ tested 2026-11-15: `make lite-jev`, ~150 ms and ~$0.000016 per request ([recorded run](../serious/demo/runs/ex1-real-jev.txt)) |

What the emulator does (so nobody is misled): it calls a free LLM 5 times; each call answers **all** questions of the request at once (one JSON object), and the vote shares become the "probabilities". `confidence` is then computed with Jev's documented formulas: Choice `(p_max − 1/n) / (1 − 1/n)`, Score `1 − (expected distance from the peak level) / (same for a uniform spread)`; a Noul has no confidence, its value is P(yes). Real Jev computes the distribution over every option in one call, bills input tokens only, and is trained for calibration. The response says `"model": "EMULATOR(...)"` so it can never be confused with Jev, and reports the LLM's real token usage.

**Your code decides, with a threshold per action** (`jev_client.py`, following the Jev docs on [confidence](https://docs.typesafe.ai/confidence.md) and [routing by probability](https://docs.typesafe.ai/patterns/probability-routing.md)): act on the probability of the chosen option; Noul: ≥ 0.7 yes, ≤ 0.3 no, the band between gets its own outcome; risky actions need more (block a comment ≥ 0.9, approve an expense ≥ 0.9 and within policy). With real Jev the expense example ends in ESCALATE: Jev gave "approve" only 0.67-0.70, below the 0.9 bar, which is exactly what the threshold is for.

## Run it without Docker (5 minutes, free path)

```bash
cd system-one-models/presentation/workshop-lite
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then paste your free OPENROUTER_API_KEY (https://openrouter.ai/keys)

python jev_emulator.py &      # terminal 1 (or background): the stand-in "Jev" server on :8787 (EMULATOR_MOCK=1 = offline)
python jev_client.py          # runs all 3 examples; or: python jev_client.py ticket|comment|approval
bash curl_example.sh          # the same idea with plain curl
```

If a free model is rate-limited, set another one in `.env` (`OPENROUTER_MODEL=...`; the list changes often, see `../../workshop/list_free_models.py`).

## The three examples

Every call has the same shape: **`state`** (what to look at) + **`questions`** (what you want to know). Question types:

| Type | Asks | Returns |
|---|---|---|
| `choice` | pick one option | `choice`, `probabilities`, `confidence` |
| `score` | rate on an ordered scale | `score`, `probabilities`, `confidence` |
| `noul` | yes/no | `noul` = probability of yes (0 to 1) |

1. **Route a support ticket**: `department` (choice) + `urgent` (noul). Your *code* then picks the team, and sends low-confidence cases to a human.
2. **Moderate a comment**: `toxic` (noul) + `action` (allow / review / block).
3. **Approve or reject an expense**: `within_policy` (noul) + `decision` (approve / reject / escalate). Structured state (JSON) works too.

The idea to remember: the model **answers a question**, your **code decides what to do**.

## Real output (emulator backend, 2026-10-24, free model `nvidia/nemotron-3.5-lightning:free`)

Full run saved in [`sample_output.txt`](sample_output.txt). Example 1, request and response:

```json
POST http://127.0.0.1:8787/v1/systemone
{
  "model": "jev-latest",
  "state": "Our API integration started returning 500 errors on every request 20 minutes ago. We can't process any customer orders until this is fixed.",
  "questions": {
    "department": {"type": "choice", "instructions": "Which team should handle this?",
                   "criteria": {"billing": "Payment or subscription issues",
                                "technical": "Bugs or integration problems",
                                "sales": "Pricing or account questions"}},
    "urgent": {"type": "noul", "instructions": "The message conveys urgency or time-sensitivity"}
  }
}
```
```json
{"department": {"type": "choice", "choice": "technical", "confidence": 1.0,
                "probabilities": {"billing": 0.0, "technical": 1.0, "sales": 0.0}},
 "urgent": {"type": "noul", "noul": 1.0}}
```

Example 2 (comment moderation) came back `block` with vote shares `allow 0.0 / review 0.4 / block 0.6`, i.e. a borderline answer, which is exactly where a confidence threshold would send it to a human. Example 3 came back `approve`. LLM outputs vary between runs.

## What was tested and what was not

- ✅ Emulator + `jev_client.py` (all 3 examples) + `curl_example.sh`, offline MOCK and with a free model (one call per vote answering all questions): 2026-11-15.
- ✅ **Real Jev via OpenRouter** (`make lite-jev`), all 3 examples: 2026-11-15, [recorded output](../serious/demo/runs/ex1-real-jev.txt). Ticket → technical, P(urgent) 0.99; comment → block 0.91-0.93 (passes the 0.9 bar); expense → approve only 0.67-0.70, so the code escalates. 130-260 ms and about $0.000016 per request; `usage` shows ~55 output tokens that are not billed.
- Not tested: a direct TypeSafe key (`api.typesafe.ai` answered `401` without a key, so URL and wire format are right).
- Older outputs further up in this README come from the emulator and are vote shares, not Jev probabilities.
- Request/response shapes follow the [official API reference](https://docs.typesafe.ai/api/system-one.md). Jev uses `criteria` (not `options`) for choices and score levels.

## Switching to real Jev

1. Get a key: sign up at [console.typesafe.ai](https://console.typesafe.ai) (new accounts currently get no free credits, per TypeSafe's X posts as quoted by third-party trackers, so you need to add a few dollars; this workshop uses fractions of a cent), **or** use an OpenRouter key with credits ([OpenRouter's Jev guide](https://openrouter.ai/docs/guides/community/jev)).
2. Edit `.env`: set `JEV_BASE_URL` and `JEV_API_KEY` (options B / C in `.env.example`). No code changes. You do not need the emulator any more.
3. Optional: the official SDK does the same thing: `pip install typesafe-sdk`, then see the [quick start](https://docs.typesafe.ai/introduction/quickstart.md).
4. For production, pin a version (e.g. `jev-1.14.0`) instead of the `jev-latest` alias, as [the docs recommend](https://docs.typesafe.ai/models.md).
