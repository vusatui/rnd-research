# Workshop-lite: call Jev in 15 minutes

Goal: see with your own eyes what a **System One / decision model** call looks like: *text in, typed answer + probabilities out, no generated text*.

You need Python 3.10+ and (for the free path) a free OpenRouter key. Nothing else.

## Which backend are you talking to? (read this first)

All three options use the **same client code** and the same Jev wire format (`POST /v1/systemone`, see the [official API reference](https://docs.typesafe.ai/api/system-one.md)). Only the URL and key change.

| # | Backend | Cost | `JEV_BASE_URL` | `JEV_API_KEY` | Status for this workshop |
|---|---|---|---|---|---|
| A | **Local emulator** (default): a free chat LLM on OpenRouter behind a Jev-shaped endpoint. **This is NOT Jev.** | free | `http://127.0.0.1:8787` | anything | ✅ tested, outputs below |
| B | **Real Jev** at TypeSafe | paid, [$0.042 / 1M input tokens, output free](https://docs.typesafe.ai/models.md) | `https://api.typesafe.ai` | key from [console.typesafe.ai/keys](https://console.typesafe.ai/keys) | ⛔ not tested: we have no key (see below) |
| C | **Real Jev via OpenRouter** (billed to your OpenRouter account) | paid | `https://openrouter.ai/api` | an OpenRouter key **with credits and no $0 key limit** | ⛔ not tested: our key is capped at $0 (see below) |

What the emulator does (so nobody is misled): it asks a free LLM the same question 5 times, counts the answers and reports the vote shares as "probabilities". Real Jev instead scores every option in a single pass and is trained to give calibrated probabilities. The emulator's `confidence` is just the top vote share. The response says `"model": "EMULATOR(...)"` so it can never be confused with Jev. Numbers like `1.0` or `0.6` in the outputs below are vote shares, **not** Jev probabilities.

## Run it (5 minutes, free path)

```bash
cd system-one-models/presentation/workshop-lite
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then paste your free OPENROUTER_API_KEY (https://openrouter.ai/keys)

python jev_emulator.py &      # terminal 1 (or background): the stand-in "Jev" server on :8787
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

- ✅ Emulator + `jev_client.py` (all 3 examples) + `curl_example.sh`: run for real on 2026-10-24.
- ✅ Client against real Jev **without a key**: `HTTP 401 authentication_error` from `api.typesafe.ai`, so the URL and wire format are right, but **no real Jev answer was obtained**.
- ✅ Client against OpenRouter's Jev endpoint with our key: `HTTP 403 Key limit exceeded ($0.00 of $0.00)`: the key we have is capped at zero spend (set up for free models only). **No real Jev answer was obtained.**
- ⛔ We did **not** fabricate any Jev response. Everything above comes from the emulator.
- Request/response shapes follow the [official API reference](https://docs.typesafe.ai/api/system-one.md) and [quick start](https://docs.typesafe.ai/introduction/quickstart.md). Note: Jev uses `criteria` (not `options`) for choices and score levels; the older `../../workshop/ex4_decision_apis/compare.py` uses `options` and should be fixed before it is used against real Jev.

## Switching to real Jev

1. Get a key: sign up at [console.typesafe.ai](https://console.typesafe.ai) (new accounts currently get no free credits, per TypeSafe's X posts as quoted by third-party trackers, so you need to add a few dollars; this workshop uses fractions of a cent), **or** use an OpenRouter key with credits ([OpenRouter's Jev guide](https://openrouter.ai/docs/guides/community/jev)).
2. Edit `.env`: set `JEV_BASE_URL` and `JEV_API_KEY` (options B / C in `.env.example`). No code changes. You do not need the emulator any more.
3. Optional: the official SDK does the same thing: `pip install typesafe-sdk`, then see the [quick start](https://docs.typesafe.ai/introduction/quickstart.md).
4. For production, pin a version (e.g. `jev-1.14.0`) instead of the `jev-latest` alias, as [the docs recommend](https://docs.typesafe.ai/models.md).
