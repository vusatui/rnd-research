"""Thin, dependency-light clients for the two kinds of model in this workshop.

chat()       - any generative LLM through OpenRouter's chat completions (structured output, logprobs, sampling)
systemone()  - a System One decision model (Jev) through the same wire format TypeSafe documents:
               POST {base}/v1/systemone  {model, state, questions} -> {answers, usage}
               Works against OpenRouter (base https://openrouter.ai/api), api.typesafe.ai, or the local emulator.

Every call returns real usage: tokens in/out, $ cost as billed (OpenRouter reports it), wall-clock latency.
A process-wide budget guard (MAX_SPEND_USD, default $0.25) stops a run before it spends more than you meant to.
"""
import json, os, time
import requests

OPENROUTER = "https://openrouter.ai/api/v1"


class BudgetExceeded(RuntimeError):
    pass


class Ledger:
    def __init__(self):
        self.cost, self.calls = 0.0, 0
        self.limit = float(os.environ.get("MAX_SPEND_USD", "0.25"))

    def add(self, cost):
        self.cost += cost or 0.0
        self.calls += 1
        if self.cost > self.limit:
            raise BudgetExceeded(f"spent ${self.cost:.4f} > MAX_SPEND_USD=${self.limit} - stopping")


LEDGER = Ledger()


def _key():
    k = os.environ.get("OPENROUTER_API_KEY")
    if not k:
        raise SystemExit("Set OPENROUTER_API_KEY in system-one-models/.env (or run with MOCK=1 to replay cached results)")
    return k


def _post(url, body, headers, timeout=120):
    for attempt in range(5):
        try:
            r = requests.post(url, json=body, headers=headers, timeout=timeout)
        except requests.RequestException:
            time.sleep(2 * (attempt + 1)); continue
        if r.status_code == 200:
            return r.json()
        if r.status_code in (400, 401, 402, 403, 404):
            raise RuntimeError(f"HTTP {r.status_code}: {r.text[:300]}")
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"gave up after retries: HTTP {r.status_code}: {r.text[:200]}")


def chat(model, messages, *, max_tokens=300, temperature=0.0, schema=None, logprobs=False,
         top_logprobs=None, reasoning="minimal"):
    """One chat completion. Returns {text, logprobs, in_tok, out_tok, cost, ms, model}."""
    body = {"model": model, "messages": messages, "max_tokens": max_tokens,
            "temperature": temperature, "usage": {"include": True}}
    if reasoning == "off":
        body["reasoning"] = {"enabled": False}
    elif reasoning:
        body["reasoning"] = {"effort": reasoning}
    if schema:
        body["response_format"] = {"type": "json_schema",
                                   "json_schema": {"name": "answer", "strict": True, "schema": schema}}
    if logprobs:
        body["logprobs"], body["top_logprobs"] = True, top_logprobs or 20
        body["reasoning"] = {"enabled": False}
        body["provider"] = {"require_parameters": True}  # only route to providers that really return logprobs
    t0 = time.perf_counter()
    j = _post(f"{OPENROUTER}/chat/completions", body, {"Authorization": f"Bearer {_key()}"})
    ms = (time.perf_counter() - t0) * 1000
    u = j.get("usage") or {}
    LEDGER.add(u.get("cost"))
    c = (j.get("choices") or [{}])[0]
    return {"text": (c.get("message") or {}).get("content") or "", "logprobs": c.get("logprobs"),
            "in_tok": u.get("prompt_tokens", 0), "out_tok": u.get("completion_tokens", 0),
            "cost": u.get("cost") or 0.0, "ms": ms, "model": j.get("model", model), "provider": j.get("provider")}


def systemone(state, questions, *, model=None, base=None, key=None):
    """One System One request (any number of questions). Returns {answers, in_tok, out_tok, cost, ms, model}."""
    base = (base or os.environ.get("JEV_BASE_URL") or "https://openrouter.ai/api").rstrip("/")
    key = key or os.environ.get("JEV_API_KEY") or _key()
    body = {"model": model or os.environ.get("JEV_MODEL", "jev-latest"), "state": state, "questions": questions}
    t0 = time.perf_counter()
    j = _post(f"{base}/v1/systemone", body, {"Authorization": f"Bearer {key}"})
    ms = (time.perf_counter() - t0) * 1000
    u = j.get("usage") or {}
    LEDGER.add(u.get("cost"))
    return {"answers": j["answers"], "in_tok": u.get("input_tokens", 0), "out_tok": u.get("output_tokens", 0),
            "cost": u.get("cost") or 0.0, "ms": ms, "model": j.get("model")}


def parse_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`").split("\n", 1)[1] if "\n" in text else text
    s, e = text.find("{"), text.rfind("}")
    return json.loads(text[s:e + 1])
