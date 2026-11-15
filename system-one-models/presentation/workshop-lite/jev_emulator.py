#!/usr/bin/env python3
"""Local STAND-IN for the Jev API (NOT Jev).

It speaks the same wire format as POST https://api.typesafe.ai/v1/systemone
(state + typed questions -> typed answers with probabilities), but the "model" behind it is
a chat LLM on OpenRouter. Each vote is ONE call that answers ALL questions of the request; we ask
EMULATOR_SAMPLES times and count votes, then compute `confidence` with Jev's documented formulas.
Real Jev instead computes the distribution over every option in one pass and is trained for
calibration; you pay only for input tokens.

Use it to learn the API shape for free. Point the client at real Jev by changing JEV_BASE_URL.
Run:  python jev_emulator.py      (listens on 127.0.0.1:8787)

Offline modes (no network, no key), both clearly labelled MOCK in every response:
  EMULATOR_MOCK=1            always answer with deterministic keyword rules (mock_rules.py)
  EMULATOR_FALLBACK=mock     use the free LLM, but if it fails for a question, answer that
                             question with the mock rules and say so in "model" and "_note"
"""
import json, os, re, sys, time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import requests
import mock_rules

K = int(os.environ.get("EMULATOR_SAMPLES", "5"))
MODEL = os.environ.get("OPENROUTER_MODEL", "nvidia/nemotron-3.5-lightning:free")
PORT = int(os.environ.get("EMULATOR_PORT", "8787"))
HOST = os.environ.get("EMULATOR_HOST", "127.0.0.1")  # the Docker image sets 0.0.0.0

PROMPT = """You are a decision function. Read the STATE and answer EVERY question below.
Reply with JSON only, one key per question, each value one of that question's options. No explanation.

{questions}

STATE:
{state}

JSON with keys {keys}:"""


def _load_env():
    p = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(p):
        for line in open(p):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def _llm(prompt, temperature):
    """One chat completion. Returns (text, input_tokens, output_tokens)."""
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("Set OPENROUTER_API_KEY (free key: https://openrouter.ai/keys)")
    for attempt in range(4):
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", timeout=60,
            headers={"Authorization": f"Bearer {key}"},
            json={"model": os.environ.get("OPENROUTER_MODEL", MODEL), "temperature": temperature,
                  "max_tokens": 400, "reasoning": {"enabled": False},
                  "messages": [{"role": "user", "content": prompt}]})
        if r.status_code == 200:
            j = r.json()
            u = j.get("usage") or {}
            return (j["choices"][0]["message"].get("content") or ""), u.get("prompt_tokens", 0), u.get("completion_tokens", 0)
        if r.status_code in (400, 401, 402, 403, 404):  # bad key/model: retrying will not help
            raise RuntimeError(f"OpenRouter HTTP {r.status_code}: {r.text[:200]}")
        time.sleep(1.5 * (attempt + 1))
    return "", 0, 0


def _options(q):
    """(options, text shown to the LLM) for one question."""
    typ, crit = q["type"], q.get("criteria")
    if typ == "choice":
        return list(crit), "\n".join(f"  - {k}: {v}" for k, v in crit.items())
    if typ == "score":
        return [str(i) for i in range(len(crit))], "\n".join(f"  - {i}: {v}" for i, v in enumerate(crit)) + "\n  (answer with the level number)"
    return ["yes", "no"], "  - yes\n  - no" + (f"\n  (criteria: {crit})" if crit else "")


def _mock_on():
    return os.environ.get("EMULATOR_MOCK", "").lower() in ("1", "true", "yes")


def choice_confidence(probs):
    """Jev's documented Choice formula: how far the top probability is above an even split (0 = even, 1 = certain)."""
    n = len(probs)
    return (max(probs.values()) - 1 / n) / (1 - 1 / n)


def score_confidence(probs):
    """Jev's documented Score formula: 1 - (expected distance from the peak level) / (same for a uniform spread)."""
    p = [probs[str(i)] for i in range(len(probs))]
    n, m = len(p), max(range(len(p)), key=lambda i: p[i])
    mad_unif = sum(abs(i - (n - 1) / 2) for i in range(n)) / n
    return max(0.0, 1 - sum(pi * abs(i - m) for i, pi in enumerate(p)) / mad_unif)


def _vote(questions, state):
    """ONE LLM call answering ALL questions. Returns ({name: option or None}, in_tok, out_tok)."""
    blocks, opts = [], {}
    for name, q in questions.items():
        opts[name], described = _options(q)
        blocks.append(f"{name}: {q.get('instructions', '')}\n{described}")
    text, tin, tout = _llm(PROMPT.format(questions="\n\n".join(blocks), state=state, keys=json.dumps(list(questions))), 0.8)
    try:
        raw = json.loads(text[text.find("{"): text.rfind("}") + 1])
    except ValueError:
        raw = {}
    picks = {}
    for name, options in opts.items():
        val = str(raw.get(name, "")).strip().lower()
        picks[name] = next((o for o in options if str(o).lower() == val), None)
    return picks, tin, tout


def _answers_from_votes(questions, votes):
    answers = {}
    for name, q in questions.items():
        options, _ = _options(q)
        c = Counter(v[name] for v in votes if v[name] is not None)
        valid = sum(c.values())
        if not valid:
            raise RuntimeError(f"the LLM returned no usable answer for '{name}' (rate limit or bad model?)")
        probs = {o: round(c.get(o, 0) / valid, 2) for o in options}
        if q["type"] == "noul":
            answers[name] = {"type": "noul", "noul": probs["yes"]}
            continue
        top = max(probs, key=probs.get)
        if q["type"] == "choice":
            answers[name] = {"type": "choice", "choice": top, "probabilities": probs,
                             "confidence": round(choice_confidence(probs), 2)}
        else:
            answers[name] = {"type": "score", "score": round(sum(int(i) * p for i, p in probs.items()), 2),
                             "probabilities": probs, "confidence": round(score_confidence(probs), 2),
                             "legend": {str(i): v for i, v in enumerate(q["criteria"])}}
    return answers


def handle(body):
    state = body["state"] if isinstance(body["state"], str) else json.dumps(body["state"], ensure_ascii=False)
    questions = body["questions"]
    if _mock_on():
        answers = {n: mock_rules.answer(q, state) for n, q in questions.items()}
        return {"model": "MOCK-EMULATOR(offline keyword rules)", "answers": answers,
                "usage": {"input_tokens": None, "output_tokens": None},
                "_note": "NOT Jev and NOT an LLM: deterministic keyword rules, same wire format"}
    try:
        with ThreadPoolExecutor(K) as ex:  # K votes in parallel, each vote is ONE call for ALL questions
            votes = list(ex.map(lambda _: _vote(questions, state), range(K)))
        answers = _answers_from_votes(questions, [v[0] for v in votes])
    except Exception:
        if os.environ.get("EMULATOR_FALLBACK", "").lower() != "mock":
            raise
        answers = {n: mock_rules.answer(q, state) for n, q in questions.items()}
        return {"model": f"EMULATOR({MODEL})+MOCK-FALLBACK", "answers": answers,
                "usage": {"input_tokens": None, "output_tokens": None},
                "_note": "NOT Jev: the LLM failed, every question answered by offline keyword rules (MOCK)"}
    return {"model": f"EMULATOR({MODEL}, {K} votes)", "answers": answers,
            "usage": {"input_tokens": sum(v[1] for v in votes), "output_tokens": sum(v[2] for v in votes), "llm_calls": K},
            "_note": f"NOT Jev: {K} calls to a chat LLM (each answers all {len(questions)} questions), votes counted. "
                     "Real Jev: 1 call, a computed distribution, input-only pricing."}


class H(BaseHTTPRequestHandler):
    def do_GET(self):  # health check for scripts: GET /health
        if self.path.rstrip("/") != "/health":
            self.send_error(404); return
        data = json.dumps({"ok": True, "mock": _mock_on()}).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

    def do_POST(self):
        if self.path.rstrip("/") != "/v1/systemone":
            self.send_error(404); return
        try:
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            out, code = handle(body), 200
        except Exception as e:  # keep the demo alive
            out, code = {"detail": {"error_type": "emulator_error", "message": str(e)}}, 500
        data = json.dumps(out).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    _load_env()
    MODEL = os.environ.get("OPENROUTER_MODEL", MODEL)
    if _mock_on():
        print(f"Jev MOCK EMULATOR (offline keyword rules, no LLM, no key) on http://{HOST}:{PORT}  - this is NOT Jev", file=sys.stderr)
    else:
        fb = ", falls back to MOCK rules if the LLM fails" if os.environ.get("EMULATOR_FALLBACK", "").lower() == "mock" else ""
        print(f"Jev EMULATOR (free LLM {MODEL}, {K} votes/question{fb}) on http://{HOST}:{PORT}  - this is NOT Jev", file=sys.stderr)
    ThreadingHTTPServer((HOST, PORT), H).serve_forever()
