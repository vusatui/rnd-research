"""Free local CPU benchmark on our 150 held-out tickets (department question). No API calls.
A) zero-shot NLI: MoritzLaurer/deberta-v3-base-zeroshot-v2.0 (184M, MIT), no training.
B) small encoder + logistic regression: BAAI/bge-small-en-v1.5 embeddings, trained on the 100 train tickets."""
import json, time, statistics, os, platform, torch
from sklearn.linear_model import LogisticRegression
torch.set_num_threads(int(os.environ.get("THREADS", "4")))
rows = [json.loads(l) for l in open("/workspace/rnd-research/system-one-models/workshop/data/tickets.jsonl")]
train = [r for r in rows if r["split"] == "train"]; test = [r for r in rows if r["split"] == "test"]
labels = ["billing", "technical", "account", "sales", "other"]
print("threads", torch.get_num_threads(), "cpu", platform.processor() or platform.machine(), "train", len(train), "test", len(test))
def report(name, preds, lat):
    acc = sum(p == r["department"] for p, r in zip(preds, test)) / len(test)
    lat = sorted(lat); print(f"{name}: accuracy {acc:.1%}, latency p50 {statistics.median(lat)*1000:.0f} ms, p90 {lat[int(.9*len(lat))]*1000:.0f} ms per ticket (1 thread pool, batch 1)")
# B
from sentence_transformers import SentenceTransformer
m = SentenceTransformer("BAAI/bge-small-en-v1.5", device="cpu")
Xtr = m.encode([r["text"] for r in train], normalize_embeddings=True)
clf = LogisticRegression(max_iter=2000, C=10).fit(Xtr, [r["department"] for r in train])
preds, lat = [], []
for r in test:
    t = time.perf_counter(); e = m.encode([r["text"]], normalize_embeddings=True); preds.append(clf.predict(e)[0]); lat.append(time.perf_counter() - t)
report("bge-small (33M) + logistic regression, trained on 100 tickets", preds, lat)
# A
from transformers import pipeline
zs = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0", device=-1)
hyp = {"billing": "This ticket is about billing, invoices, payments or refunds.", "technical": "This ticket is about a technical problem, errors, outages or configuration.",
       "account": "This ticket is about account access, login, users or settings.", "sales": "This ticket is about buying, plans, pricing or upgrades.", "other": "This ticket is about something else."}
inv = {v: k for k, v in hyp.items()}
preds, lat = [], []
for r in test:
    t = time.perf_counter(); o = zs(r["text"], list(hyp.values()), hypothesis_template="{}", multi_label=False); preds.append(inv[o["labels"][0]]); lat.append(time.perf_counter() - t)
report("deberta-v3-base zero-shot NLI (184M), no training", preds, lat)
