"""Offline MOCK answers for the Jev emulator: deterministic keyword rules, no LLM, no network.

This is NOT Jev and NOT a model. It exists so the demo and CI still run when there is no key,
no network, or the free OpenRouter tier is rate-limited. Every response produced with these rules
is labelled MOCK by jev_emulator.py.

How it works: each option (and each yes/no question) is matched against a small keyword lexicon;
the keyword hits are turned into fake "vote shares out of 5", so the output has the same shape and
the same 0.2 granularity as the real emulator. Ties produce split votes (borderline answers).
"""
import json, re

K = 5
LEX = {
    "billing": "charged charge refund invoice invoices billed billing payment subscription money vat price receipt declined cancelled",
    "technical": "error errors 500 429 bug crash crashes api integration webhook fails broken down sync export timeout requests",
    "sales": "pricing price quote demo discount plan plans enterprise seats buying contract",
    "account": "account password login log 2fa email profile workspace teammate ownership access merge delete",
    "urgent": "urgent asap immediately now today 500 down outage can't cannot nobody every minutes blocked tomorrow",
    "toxic": "idiot idiots stupid garbage trash hate shut moron dumb",
    "angry": "twice wrong never nobody angry unacceptable worst garbage idiots",
    "excited": "love awesome great amazing thanks excited",
}
# options/questions that are the opposite of a lexicon entry
NEGATES = {"allow": "toxic", "calm": "angry", "reject": "policy_ok", "low": "urgent"}
ALIASES = {"block": "toxic", "insult": "toxic", "insults": "toxic", "attack": "toxic", "attacks": "toxic",
           "abusive": "toxic", "toxic": "toxic",
           "urgency": "urgent", "time-sensitivity": "urgent", "high": "urgent",
           "approve": "policy_ok", "within_policy": "policy_ok", "policy": "policy_ok"}


def _words(text):
    return re.findall(r"[a-z0-9']+", text.lower())


def _policy_ok(state):
    """Structured expense check: per-person amount vs the first $ limit in the policy text."""
    try:
        s = json.loads(state)
    except Exception:
        return 0
    if not isinstance(s, dict) or "amount_usd" not in s:
        return 0
    m = re.search(r"\$(\d+(?:\.\d+)?)", str(s.get("policy", "")))
    if not m:
        return 0
    per_person = float(s["amount_usd"]) / max(int(s.get("people", 1) or 1), 1)
    return 2 if per_person <= float(m.group(1)) else -2


def _hits(topic, state, words):
    if topic == "policy_ok":
        return _policy_ok(state)
    if topic not in LEX:
        return 0
    lex = set(LEX[topic].split())
    return sum(w in lex for w in words)


def _topic_of(name, text=""):
    for w in [name.lower()] + _words(text):
        if w in LEX:
            return w
        if w in ALIASES:
            return ALIASES[w]
    return None


def _score_option(opt, desc, state, words):
    o = opt.lower()
    if o in NEGATES:
        return max(0, 1 - _hits(NEGATES[o], state, words))
    topic = o if o in LEX else ALIASES.get(o) or _topic_of(o, desc)
    if o == "review":  # borderline bucket: wins only when nothing else is clear
        return 0.5
    if o == "escalate":
        return 0.5 if _policy_ok(state) == 0 else 0
    return _hits(topic, state, words) if topic else 0


def _votes(scores):
    """Turn keyword scores into deterministic 'votes out of 5'."""
    order = sorted(scores, key=lambda o: (-scores[o], list(scores).index(o)))
    top = order[0]
    second = order[1] if len(order) > 1 else None
    margin = scores[top] - (scores[second] if second else 0)
    votes = {o: 0 for o in scores}
    if second is None or margin >= 2:
        votes[top] = 5
    elif margin >= 1:
        votes[top], votes[second] = 4, 1
    else:
        votes[top], votes[second] = 3, 2
    return {o: round(v / K, 2) for o, v in votes.items()}


def _score_conf(probs):
    p = [probs[str(i)] for i in range(len(probs))]
    n, m = len(p), max(range(len(p)), key=lambda i: p[i])
    mad = sum(abs(i - (n - 1) / 2) for i in range(n)) / n
    return max(0.0, 1 - sum(pi * abs(i - m) for i, pi in enumerate(p)) / mad)


def answer(q, state):
    words = _words(state)
    typ, crit = q["type"], q.get("criteria") or {}
    if typ == "noul":
        topic = _topic_of("", q.get("instructions", ""))
        h = _hits(topic, state, words) if topic else 0
        yes = 1.0 if h >= 2 else 0.6 if h == 1 else 0.0
        return {"type": "noul", "noul": yes}
    if typ == "choice":
        probs = _votes({o: _score_option(o, d, state, words) for o, d in crit.items()})
        top = max(probs, key=probs.get)
        n = len(probs)  # Jev's documented Choice confidence formula
        return {"type": "choice", "choice": top, "confidence": round((probs[top] - 1 / n) / (1 - 1 / n), 2), "probabilities": probs}
    # score: ordered levels; pick the level whose description matches best, default the middle
    levels = list(crit)
    scores = {str(i): _hits(_topic_of("", lvl), state, words) for i, lvl in enumerate(levels)}
    if not any(scores.values()):
        scores[str(len(levels) // 2)] = 1
    probs = _votes(scores)
    top = max(probs, key=probs.get)
    return {"type": "score", "score": round(sum(int(i) * p for i, p in probs.items()), 2),
            "confidence": round(_score_conf(probs), 2), "legend": {str(i): v for i, v in enumerate(levels)}, "probabilities": probs}
