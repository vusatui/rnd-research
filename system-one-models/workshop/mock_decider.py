"""Offline MOCK for decider.py: deterministic keyword rules instead of an LLM (DECIDER_MOCK=1).

NOT a model and NOT an LLM. It only exists so the exercises run in CI and on stage without a key
or network. Results printed with it are labelled MOCK; do not read anything into its accuracy.
Each sample is a keyword vote with a deterministic tie-break that depends on the sample index,
so k samples can disagree (split votes) on ambiguous text, like a real self-consistency run.
"""
import hashlib, json, re

LEX = {
    "billing": "charged charge refund invoice invoices billed billing payment money vat receipt declined cancelled annual monthly price",
    "technical": "error 500 429 bug crash crashes api webhook fails broken down sync export button typo pdf blank mode safari android startup update",
    "account": "account password login log 2fa email profile workspace teammate ownership access merge delete forgot reset",
    "sales": "pricing quote demo discount plan plans enterprise seats buying contract nonprofit security sso",
    "other": "partner podcast love hiring meaning life",
    "yes": "urgent asap now today down outage nobody declined tomorrow crashes 2fa another",
    "high": "urgent asap now today down outage nobody declined tomorrow crashes 2fa another",
}


def _words(text):
    return re.findall(r"[a-z0-9']+", text.lower())


def answer_once(q, state, options, i):
    text = state if isinstance(state, str) else json.dumps(state)
    words = _words(text)
    scores = {o: sum(w in set(LEX.get(str(o).lower(), "").split()) for w in words) for o in options}
    best = max(scores.values())
    tied = [o for o in options if scores[o] == best]
    if best == 0 and "no" in options:
        return "no"
    # deterministic "sampling": on a tie, different sample indices pick different tied options
    h = int(hashlib.sha1(f"{text}|{i}".encode()).hexdigest(), 16)
    return tied[h % len(tied)] if best > 0 or len(tied) == 1 else options[h % len(options)]
