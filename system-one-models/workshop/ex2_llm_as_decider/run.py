"""Exercise 2 - an LLM forced into System One shape (free OpenRouter model).

Runs decider.decide() on every ticket and reports accuracy, ECE and latency, so you can
compare with Exercise 1. Expect: higher accuracy on unseen wording, much higher latency,
and confidence that is only as good as k-sample voting allows.
Usage: python run.py [--limit 15] [--k 3]
"""
import sys, pathlib, argparse
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import load_tickets, ece, DEPARTMENTS
from decider import decide

ap = argparse.ArgumentParser()
ap.add_argument("--limit", type=int, default=15)
ap.add_argument("--k", type=int, default=3)
a = ap.parse_args()
rows = load_tickets()[: a.limit]
confs, correct, lat = [], [], []
for r in rows:
    ans = decide(r["text"], {"route": {"type": "choice", "options": DEPARTMENTS,
                 "instructions": "Which team should own this support ticket?"}}, k=a.k)
    c = ans["route"]
    confs.append(c["confidence"]); correct.append(c["choice"] == r["department"]); lat.append(ans["_latency_ms"])
    print(f'{"OK " if correct[-1] else "ERR"} {str(c["choice"]):9} p={c["confidence"]:.2f} {ans["_latency_ms"]:>6} ms  {r["text"][:60]}')
print(f"\naccuracy {sum(correct)/len(rows):.2%} | ECE {ece(confs, correct):.3f} | median latency {sorted(lat)[len(lat)//2]} ms (k={a.k})")
