#!/usr/bin/env python3
"""Local STAND-IN for the Jev API (NOT Jev).

It speaks the same wire format as POST https://api.typesafe.ai/v1/systemone
(state + typed questions -> typed answers with probabilities), but the "model" behind it is
a free chat LLM on OpenRouter. Probabilities are estimated by asking the LLM several times and
counting votes - real Jev instead scores every option in one pass and is trained for calibration.

Use it to learn the API shape for free. Point the client at real Jev by changing JEV_BASE_URL.
Run:  python jev_emulator.py      (listens on 127.0.0.1:8787)
"""
import json, os, re, sys, time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import requests

K = int(os.environ.get("EMULATOR_SAMPLES", "5"))
MODEL = os.environ.get("OPENROUTER_MODEL", "nvidia/nemotron-3.5-lightning:free")
PORT = int(os.environ.get("EMULATOR_PORT", "8787"))

PROMPT = """You are a decision function. Read the STATE and answer the QUESTION.
Reply with JSON only: {{"answer": <one of {options}>}}. No explanation.

QUESTION: {instructions}
OPTIONS:
{described}

STATE:
{state}"""


def _load_env():
    p = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(p):
        for line in open(p):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def _llm(prompt, temperature):
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("Set OPENROUTER_API_KEY (free key: https://openrouter.ai/keys)")
    for attempt in range(4):
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", timeout=60,
            headers={"Authorization": f"Bearer {key}"},
            json={"model": os.environ.get("OPENROUTER_MODEL", MODEL), "temperature": temperature,
                  "max_tokens": 300, "reasoning": {"enabled": False},
                  "messages": [{"role": "user", "content": prompt}]})
        if r.status_code == 200:
            return r.json()["choices"][0]["message"].get("content") or ""
        time.sleep(1.5 * (attempt + 1))
    return ""


def _sample(q, state, options, described):
    text = _llm(PROMPT.format(options=json.dumps(options), instructions=q.get("instructions", ""),
                              described=described, state=state), 0.8)
    m = re.search(r'"answer"\s*:\s*"?([^"}\n]+?)"?\s*[},]', text + "}")
    val = (m.group(1) if m else text).strip().lower()
    for o in options:
        if str(o).lower() == val:
            return o
    return None


def _answer(q, state):
    typ, crit = q["type"], q.get("criteria")
    if typ == "choice":
        options = list(crit)
        described = "\n".join(f"- {k}: {v}" for k, v in crit.items())
    elif typ == "score":
        options = [str(i) for i in range(len(crit))]
        described = "\n".join(f"- {i}: {v}" for i, v in enumerate(crit)) + "\n(answer with the level number)"
    else:  # noul
        options = ["yes", "no"]
        described = "- yes\n- no"
    with ThreadPoolExecutor(K) as ex:
        votes = Counter(ex.map(lambda _: _sample(q, state, options, described), range(K)))
    valid = sum(v for o, v in votes.items() if o is not None)
    if not valid:
        raise RuntimeError("the free LLM returned no usable answers (rate limit or bad model?) - try another OPENROUTER_MODEL")
    probs = {o: round(votes.get(o, 0) / valid, 2) for o in options}
    if typ == "noul":
        return {"type": "noul", "noul": probs["yes"]}
    top = max(probs, key=probs.get)
    if typ == "choice":
        return {"type": "choice", "choice": top, "confidence": probs[top], "probabilities": probs}
    return {"type": "score", "score": round(sum(int(i) * p for i, p in probs.items()), 2),
            "confidence": probs[top], "legend": {str(i): v for i, v in enumerate(crit)}, "probabilities": probs}


def handle(body):
    state = body["state"] if isinstance(body["state"], str) else json.dumps(body["state"], ensure_ascii=False)
    items = list(body["questions"].items())
    with ThreadPoolExecutor(len(items)) as ex:
        answers = dict(zip([n for n, _ in items], ex.map(lambda nq: _answer(nq[1], state), items))) 
    return {"model": f"EMULATOR({MODEL})", "answers": answers,
            "usage": {"input_tokens": None, "output_tokens": None},
            "_note": "NOT Jev: free LLM + vote counting, same wire format"}


class H(BaseHTTPRequestHandler):
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
    print(f"Jev EMULATOR (free LLM {MODEL}, {K} votes/question) on http://127.0.0.1:{PORT}  - this is NOT Jev", file=sys.stderr)
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
