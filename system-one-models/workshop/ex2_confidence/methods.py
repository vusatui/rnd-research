"""Five ways to get "an answer + how sure" for the same ticket. Each returns one result row.

The two questions asked every time: department (5 options) and urgency (3 options).
All methods see the same option descriptions (common.DEPARTMENTS / common.URGENCY).

A  verbal    structured output: the LLM writes the label AND a confidence number (1 call, both questions)
B  logprobs  the LLM's own token probabilities over the option names (1 call per question, needs logprobs)
C  votes     self-consistency: k samples at temperature 1, count votes (k calls, both questions per call)
D  classic   TF-IDF + logistic regression trained on 100 labelled tickets (local, no LLM)
E  jev       a System One decision model: 1 request, both questions, a distribution over every option
"""
import json, math, sys, pathlib, time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import DEPARTMENTS, URGENCY
import llm

QUESTIONS = {"department": DEPARTMENTS, "urgency": URGENCY}


def _described(d):
    return "\n".join(f"- {k}: {v}" for k, v in d.items())


TASK = f"""You route support tickets for Lumen, a B2B analytics SaaS.
Departments:
{_described(DEPARTMENTS)}
Urgency:
{_described(URGENCY)}
"""


def _row(t, ans, in_tok, out_tok, cost, ms, calls, label):
    r = {"id": t["id"], "gold_department": t["department"], "gold_urgency": t["urgency"], "ambiguous": t["ambiguous"],
         "in_tok": in_tok, "out_tok": out_tok, "cost": cost, "ms": round(ms), "calls": calls, "method_label": label}
    for q, (choice, p, probs) in ans.items():
        r[q], r[f"{q}_p"], r[f"{q}_probs"] = choice, round(p, 4), probs
    return r


# ---------- A: structured output with a verbalized confidence ----------
VERBAL_SCHEMA = {"type": "object", "additionalProperties": False,
    "required": ["department", "department_confidence", "urgency", "urgency_confidence"],
    "properties": {"department": {"type": "string", "enum": list(DEPARTMENTS)},
                   "department_confidence": {"type": "number"},
                   "urgency": {"type": "string", "enum": list(URGENCY)},
                   "urgency_confidence": {"type": "number"}}}


def verbal(t, model):
    prompt = TASK + f"""
For the ticket below give the department and the urgency. For each, also give your confidence: the probability
(0.0-1.0) that your answer is correct. Be calibrated: of the answers you give 0.8, about 80% should be right.

Ticket: {t['text']}"""
    reasoning = "minimal" if ("gpt-6" in model or "sonnet" in model) else "off"
    spent = {"in": 0, "out": 0, "cost": 0.0, "ms": 0.0, "calls": 0}
    for max_tokens in (120, 600):  # a model that spends tokens on hidden reasoning can return empty at 120: retry once
        r = llm.chat(model, [{"role": "user", "content": prompt}], max_tokens=max_tokens, temperature=0.0,
                     schema=VERBAL_SCHEMA, reasoning=reasoning)
        for k, v in (("in", r["in_tok"]), ("out", r["out_tok"]), ("cost", r["cost"]), ("ms", r["ms"]), ("calls", 1)):
            spent[k] += v
        try:
            j = llm.parse_json(r["text"])
            break
        except ValueError:
            j = None
    if j is None:
        raise RuntimeError(f"{model} returned no JSON for ticket {t['id']}")
    ans = {q: (j[q], min(1.0, max(0.0, float(j[f"{q}_confidence"]))), None) for q in QUESTIONS}
    return _row(t, ans, spent["in"], spent["out"], spent["cost"], spent["ms"], spent["calls"], f"A verbal  {model.split('/')[-1]}")


# ---------- B: token logprobs over the option names ----------
def _dist_from_logprobs(top, options):
    mass = {o: 0.0 for o in options}
    for x in top:
        tok = x["token"].strip().lower()
        hits = [o for o in options if tok and o.startswith(tok)]
        if len(hits) == 1:
            mass[hits[0]] += math.exp(x["logprob"])
    s = sum(mass.values()) or 1.0
    return {o: v / s for o, v in mass.items()}


def logprobs(t, model):
    def one(q):
        prompt = TASK + f"\nTicket: {t['text']}\n\nWhich {q}? Answer with exactly one of: {', '.join(QUESTIONS[q])}. Lowercase, nothing else."
        for _ in range(4):  # a few OpenRouter providers occasionally drop logprobs: ask again
            r = llm.chat(model, [{"role": "user", "content": prompt}], max_tokens=1, temperature=0.0,
                         logprobs=True, top_logprobs=20, reasoning=None)
            if r["logprobs"] and r["logprobs"].get("content"):
                return q, r
        raise RuntimeError(f"no logprobs from {model} for ticket {t['id']}")
    t0 = time.perf_counter()
    with ThreadPoolExecutor(2) as ex:
        res = dict(ex.map(one, QUESTIONS))
    ms = (time.perf_counter() - t0) * 1000
    ans = {}
    for q, r in res.items():
        top = r["logprobs"]["content"][0]["top_logprobs"]
        probs = _dist_from_logprobs(top, list(QUESTIONS[q]))
        best = max(probs, key=probs.get)
        ans[q] = (best, probs[best], {k: round(v, 4) for k, v in probs.items()})
    return _row(t, ans, sum(r["in_tok"] for r in res.values()), sum(r["out_tok"] for r in res.values()),
                sum(r["cost"] for r in res.values()), ms, 2, f"B logprobs {model.split('/')[-1]}")


# ---------- C: self-consistency, k votes ----------
VOTE_SCHEMA = {"type": "object", "additionalProperties": False, "required": ["department", "urgency"],
    "properties": {"department": {"type": "string", "enum": list(DEPARTMENTS)},
                   "urgency": {"type": "string", "enum": list(URGENCY)}}}


def votes(t, model, k=5):
    prompt = TASK + f"\nTicket: {t['text']}\n\nGive the department and the urgency."
    t0 = time.perf_counter()
    with ThreadPoolExecutor(k) as ex:
        rs = list(ex.map(lambda _: llm.chat(model, [{"role": "user", "content": prompt}], max_tokens=40,
                                             temperature=1.0, schema=VOTE_SCHEMA, reasoning="off"), range(k)))
    ms = (time.perf_counter() - t0) * 1000
    picks = [llm.parse_json(r["text"]) for r in rs]
    ans = {}
    for q in QUESTIONS:
        c = Counter(p[q] for p in picks)
        probs = {o: c.get(o, 0) / k for o in QUESTIONS[q]}
        best = max(probs, key=probs.get)
        ans[q] = (best, probs[best], probs)
    return _row(t, ans, sum(r["in_tok"] for r in rs), sum(r["out_tok"] for r in rs), sum(r["cost"] for r in rs),
                ms, k, f"C votes k={k} {model.split('/')[-1]}")


# ---------- D: classic classifier ----------
def classic_fit(train):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    clfs = {}
    for q in QUESTIONS:
        clf = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=1),
                            LogisticRegression(max_iter=3000, C=10))
        clf.fit([r["text"] for r in train], [r[q] for r in train])
        clfs[q] = clf
    return clfs


def classic(t, clfs):
    t0 = time.perf_counter()
    ans = {}
    for q, clf in clfs.items():
        p = clf.predict_proba([t["text"]])[0]
        probs = {c: float(v) for c, v in zip(clf.classes_, p)}
        best = max(probs, key=probs.get)
        ans[q] = (best, probs[best], {k: round(v, 4) for k, v in probs.items()})
    return _row(t, ans, 0, 0, 0.0, (time.perf_counter() - t0) * 1000, 0, "D classic TF-IDF+logreg (100 train)")


# ---------- E: System One decision model ----------
def jev(t, model="jev-latest"):
    qs = {"department": {"type": "choice", "instructions": "Which department should own this Lumen support ticket?",
                         "criteria": DEPARTMENTS},
          "urgency": {"type": "choice", "instructions": "How urgent is this ticket?", "criteria": URGENCY}}
    r = llm.systemone(t["text"], qs, model=model)
    ans = {}
    for q in QUESTIONS:
        a = r["answers"][q]
        ans[q] = (a["choice"], a["probabilities"][a["choice"]], a["probabilities"])
    row = _row(t, ans, r["in_tok"], r["out_tok"], r["cost"], r["ms"], 1, f"E jev ({r['model']})")
    row["jev_confidence"] = {q: r["answers"][q].get("confidence") for q in QUESTIONS}
    return row
