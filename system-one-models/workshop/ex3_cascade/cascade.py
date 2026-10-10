"""Exercise 3 - System 1 / System 2 cascade with a confidence gate.

Fast path: the Exercise-1 classifier (System 1). If its confidence is below THRESHOLD,
escalate to the LLM decider (System 2 stand-in). Reports accuracy, share of escalations
and total LLM calls - the core trade-off every decision-model architecture is about.
Usage: python cascade.py --threshold 0.6 [--no-llm]
"""
import sys, pathlib, argparse
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from common import load_tickets, DEPARTMENTS

ap = argparse.ArgumentParser()
ap.add_argument("--threshold", type=float, default=0.6)
ap.add_argument("--no-llm", action="store_true", help="escalations go to a 'human' queue instead")
a = ap.parse_args()
rows = load_tickets()
train, test = rows[:24], rows[24:]
clf = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True), LogisticRegression(max_iter=2000, C=10))
clf.fit([r["text"] for r in train], [r["department"] for r in train])

ok = esc = 0
for r in test:
    p = clf.predict_proba([r["text"]])[0]
    label, conf, path = clf.classes_[p.argmax()], p.max(), "S1"
    if conf < a.threshold:
        esc += 1
        if a.no_llm:
            label, path = r["department"], "HUMAN"  # assume the human is right
        else:
            from decider import decide
            label = decide(r["text"], {"route": {"type": "choice", "options": DEPARTMENTS,
                           "instructions": "Which team should own this support ticket?"}}, k=1)["route"]["choice"]
            path = "S2"
    ok += label == r["department"]
    print(f"{path:5} conf={conf:.2f} -> {label:9} (gold {r['department']})")
print(f"\nthreshold {a.threshold}: accuracy {ok/len(test):.2%}, escalated {esc}/{len(test)}")
print("Sweep it: for t in 0.3 0.5 0.7 0.9; do python cascade.py --no-llm --threshold $t | tail -1; done")
