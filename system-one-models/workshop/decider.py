"""A "poor man's System One model" on top of any free chat LLM (OpenRouter).

Same request shape as Jev / OpenAI Decisions: state + typed questions -> typed answers
with probabilities. The LLM is NOT a calibrated decision model, so probabilities are
estimated by self-consistency: sample k answers constrained to the allowed options and
count votes. Real decision models (Jev, Clef, Laya, OpenAI Decisions) instead score every
option in a single forward pass and are trained for calibration - that is the point of
the comparison in the workshop.
"""
import json, re, time
from collections import Counter
from common import openrouter, model_name

PROMPT = """You are a decision function. Read the STATE and answer the QUESTION.
Reply with JSON only: {{"answer": <one of {options}>}}. No explanation.

QUESTION: {instructions}
{criteria}
STATE:
{state}"""


def _options(q):
    if q["type"] == "choice":
        return q["options"]
    if q["type"] == "score":
        return list(range(len(q["levels"])))
    return ["yes", "no"]  # noul / predicate


def _ask_once(client, q, state, temperature):
    opts = _options(q)
    crit = f"CRITERIA: {q['criteria']}" if q.get("criteria") else ""
    if q["type"] == "score":
        crit += "\nLEVELS (answer with the index): " + "; ".join(f"{i}={l}" for i, l in enumerate(q["levels"]))
    r = client.chat.completions.create(
        model=model_name(), temperature=temperature, max_tokens=400,
        # free models are often reasoning models; ask OpenRouter to skip/limit thinking
        extra_body={"reasoning": {"enabled": False}},
        messages=[{"role": "user", "content": PROMPT.format(
            options=json.dumps(opts), instructions=q["instructions"], criteria=crit,
            state=json.dumps(state) if not isinstance(state, str) else state)}])
    text = r.choices[0].message.content or ""
    m = re.search(r'"answer"\s*:\s*("?)([^"}]+)\1', text)
    val = m.group(2).strip() if m else text.strip()
    for o in opts:
        if str(o).lower() == val.lower():
            return o
    return None  # invalid answer: counted as abstention, like a refusal


def decide(state, questions, k=5, temperature=0.8):
    """questions: {name: {"type": "choice"|"score"|"noul", "instructions": ..., ...}}"""
    client, out = openrouter(), {}
    t0 = time.perf_counter()
    for name, q in questions.items():
        votes = Counter(_ask_once(client, q, state, temperature) for _ in range(k))
        valid = {o: votes.get(o, 0) / k for o in _options(q)}
        if q["type"] == "noul":
            out[name] = {"noul": valid["yes"] / max(valid["yes"] + valid["no"], 1e-9)}
        elif q["type"] == "score":
            s = sum(valid.values()) or 1
            out[name] = {"score": sum(i * p for i, p in valid.items()) / s,
                         "probabilities": valid, "confidence": max(valid.values())}
        else:
            best = max(valid, key=valid.get)
            if valid[best] == 0:
                best = None  # every sample was invalid -> abstain
            out[name] = {"choice": best, "probabilities": valid, "confidence": valid.get(best, 0.0),
                         "invalid": votes.get(None, 0)}
    out["_latency_ms"] = round((time.perf_counter() - t0) * 1000)
    return out


if __name__ == "__main__":
    print(json.dumps(decide("I was charged twice for my order, refund please!", {
        "route": {"type": "choice", "instructions": "Which team should own this ticket?",
                  "options": ["billing", "technical", "account", "sales", "other"]},
        "urgent": {"type": "noul", "instructions": "Is this urgent?"},
        "frustration": {"type": "score", "instructions": "How frustrated is the customer?",
                        "levels": ["calm", "annoyed", "angry"]},
    }, k=3), indent=2))
