"""Exercise 1 - the classic "System 1": a tiny trained classifier.

TF-IDF + logistic regression, trained in milliseconds, answers in microseconds, and returns
probabilities. We measure accuracy, calibration (ECE) and latency with leave-one-out CV,
because the toy dataset is small. This is the baseline every decision model must beat.
"""
import sys, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from common import load_tickets, ece

rows = load_tickets()
X, y = [r["text"] for r in rows], [r["department"] for r in rows]
confs, correct, lat = [], [], []
for i in range(len(rows)):
    clf = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True),
                        LogisticRegression(max_iter=2000, C=10))
    clf.fit(X[:i] + X[i + 1:], y[:i] + y[i + 1:])
    t = time.perf_counter()
    proba = clf.predict_proba([X[i]])[0]
    lat.append((time.perf_counter() - t) * 1000)
    best = proba.argmax()
    confs.append(float(proba[best]))
    correct.append(clf.classes_[best] == y[i])

print(f"department accuracy (LOO): {sum(correct)/len(rows):.2%}")
print(f"mean confidence:           {sum(confs)/len(confs):.2f}")
print(f"ECE:                       {ece(confs, correct):.3f}")
print(f"median latency:            {sorted(lat)[len(lat)//2]:.2f} ms")
print("\nTry: python baseline.py | then add 20 more rows to data/tickets.jsonl and re-run.")
