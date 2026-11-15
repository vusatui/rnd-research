#!/usr/bin/env python3
"""Shared evaluation harness: every method writes results/<name>.jsonl, this file scores them all the same way.

Per method it reports
  accuracy        on all test tickets, and on the clear ones (two blind labellers agreed)
  ECE             expected calibration error, 10 equal-width bins: |accuracy - confidence| averaged by bin weight
  reliability     confidence bins -> how often the answer in that bin was actually right
  auto@95/@98     coverage vs risk: the largest share of tickets you can automate (highest confidence first)
                  while the automated ones stay >= 95% correct. The rest goes to a human / a bigger model.
  distinct        how many different confidence values the method produced (verbalized numbers cluster)
  tokens, latency, cost   from real usage of each call; cost is $ per 1,000 tickets

Usage:  python eval.py                      # every results/ex2_*.jsonl
        python eval.py results/ex2_jev.jsonl --reliability
"""
import argparse, glob, json, pathlib, statistics, sys

ROOT = pathlib.Path(__file__).parent
RELIABILITY_BINS = [(0.0, 0.5), (0.5, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 0.95), (0.95, 0.99), (0.99, 1.0001)]


def load(path):
    return [json.loads(l) for l in open(path) if l.strip()]


def ece(conf, correct, bins=10):
    n, total = len(conf), 0.0
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        idx = [i for i, c in enumerate(conf) if (lo < c <= hi) or (b == 0 and c <= 0)]
        if idx:
            acc = sum(correct[i] for i in idx) / len(idx)
            avg = sum(conf[i] for i in idx) / len(idx)
            total += len(idx) / n * abs(acc - avg)
    return total


def reliability(conf, correct):
    out = []
    for lo, hi in RELIABILITY_BINS:
        idx = [i for i, c in enumerate(conf) if lo <= c < hi]
        if idx:
            out.append({"bin": f"{lo:.2f}-{min(hi, 1):.2f}", "n": len(idx),
                        "avg_conf": sum(conf[i] for i in idx) / len(idx),
                        "accuracy": sum(correct[i] for i in idx) / len(idx)})
    return out


def coverage_at(conf, correct, target=0.95):
    """Largest share automated (confidence >= t) with accuracy >= target; ties at a threshold go together."""
    order = sorted(range(len(conf)), key=lambda i: -conf[i])
    best, best_t, ok = 0.0, None, 0
    for k, i in enumerate(order, 1):
        ok += correct[i]
        if k < len(order) and conf[order[k]] == conf[i]:
            continue  # a threshold cannot split equal confidences
        if ok / k >= target:
            best, best_t = k / len(conf), conf[i]
    return best, best_t


def score(rows, q="department"):
    conf = [r[f"{q}_p"] for r in rows]
    correct = [int(r[q] == r[f"gold_{q}"]) for r in rows]
    clear = [c for r, c in zip(rows, correct) if not r.get("ambiguous")]
    cov95, t95 = coverage_at(conf, correct, 0.95)
    cov90, t90 = coverage_at(conf, correct, 0.90)
    cov98, t98 = coverage_at(conf, correct, 0.98)
    return {"n": len(rows), "accuracy": sum(correct) / len(rows), "accuracy_clear": sum(clear) / max(1, len(clear)),
            "mean_conf": sum(conf) / len(conf), "ece": ece(conf, correct),
            "auto95": cov95, "auto95_threshold": t95, "auto90": cov90, "auto90_threshold": t90, "auto98": cov98, "auto98_threshold": t98,
            "distinct_conf": len({round(c, 4) for c in conf}), "reliability": reliability(conf, correct)}


def usage(rows):
    ms = sorted(r["ms"] for r in rows)
    return {"in_tok": statistics.mean(r["in_tok"] for r in rows), "out_tok": statistics.mean(r["out_tok"] for r in rows),
            "calls": statistics.mean(r.get("calls", 1) for r in rows),
            "p50_ms": ms[len(ms) // 2], "p90_ms": ms[int(len(ms) * 0.9) - 1],
            "usd_per_1k": 1000 * sum(r["cost"] for r in rows) / len(rows)}


def bootstrap(rows, q="department", n=2000, seed=7):
    """95% percentile bootstrap CIs (resampling tickets with replacement) for accuracy and ECE. Offline, no API calls."""
    import random
    rnd = random.Random(seed)
    conf = [r[f"{q}_p"] for r in rows]
    correct = [int(r[q] == r[f"gold_{q}"]) for r in rows]
    accs, eces = [], []
    for _ in range(n):
        idx = [rnd.randrange(len(rows)) for _ in rows]
        c = [conf[i] for i in idx]; k = [correct[i] for i in idx]
        accs.append(sum(k) / len(k)); eces.append(ece(c, k))
    accs.sort(); eces.sort()
    lo, hi = int(0.025 * n), int(0.975 * n) - 1
    return {"acc_ci": (accs[lo], accs[hi]), "ece_ci": (eces[lo], eces[hi])}


def paired_diff(rows_a, rows_b, q="department", n=2000, seed=7):
    """95% CI of accuracy(a) - accuracy(b) on the same tickets (paired bootstrap)."""
    import random
    rnd = random.Random(seed)
    b = {r["id"]: r for r in rows_b}
    pairs = [(int(r[q] == r[f"gold_{q}"]), int(b[r["id"]][q] == r[f"gold_{q}"])) for r in rows_a if r["id"] in b]
    d = []
    for _ in range(n):
        idx = [rnd.randrange(len(pairs)) for _ in pairs]
        d.append(sum(pairs[i][0] - pairs[i][1] for i in idx) / len(idx))
    d.sort()
    return sum(x - y for x, y in pairs) / len(pairs), (d[int(0.025 * n)], d[int(0.975 * n) - 1])


def name_of(path):
    return pathlib.Path(path).stem.replace("ex2_", "")


def report(paths, show_reliability=False, q="department", ci=False):
    res, data = {}, {}
    for p in paths:
        rows = load(p)
        data[name_of(p)] = rows
        res[name_of(p)] = {**score(rows, q), **usage(rows), "label": rows[0].get("method_label", name_of(p))}
        if ci:
            res[name_of(p)].update(bootstrap(rows, q))
    print(f"\nQuestion: {q}   (same {next(iter(res.values()))['n']} test tickets for every method)\n")
    hdr = f"{'method':34} {'acc':>5} {'clear':>5} {'conf':>5} {'ECE':>5} {'auto@95':>8} {'auto@98':>8} {'distinct':>8} {'tok in/out':>11} {'p50 ms':>7} {'$/1k':>7}"
    print(hdr); print("-" * len(hdr))
    for k, m in res.items():
        print(f"{m['label'][:34]:34} {m['accuracy']:5.0%} {m['accuracy_clear']:5.0%} {m['mean_conf']:5.2f} {m['ece']:5.3f} "
              f"{m['auto95']:8.0%} {m['auto98']:8.0%} {m['distinct_conf']:8d} {m['in_tok']:5.0f}/{m['out_tok']:<5.0f} {m['p50_ms']:7.0f} {m['usd_per_1k']:7.3f}")
    if ci:
        print(f"\n95% bootstrap confidence intervals (2,000 resamples of the {next(iter(res.values()))['n']} tickets)")
        ref = "jev" if "jev" in data else None
        for k, m in res.items():
            line = f"  {m['label'][:34]:34} accuracy {m['accuracy']:4.0%} [{m['acc_ci'][0]:4.0%}-{m['acc_ci'][1]:4.0%}]   ECE {m['ece']:.3f} [{m['ece_ci'][0]:.3f}-{m['ece_ci'][1]:.3f}]"
            if ref and k != ref:
                d, (lo, hi) = paired_diff(data[ref], data[k], q)
                m["jev_minus_this"] = (d, lo, hi)
                line += f"   jev minus this: {d:+.1%} [{lo:+.1%} to {hi:+.1%}]"
            print(line)
    if show_reliability:
        for k, m in res.items():
            print(f"\nReliability - {m['label']}: confidence bin -> how often it was right")
            for b in m["reliability"]:
                bar = "#" * round(b["accuracy"] * 20)
                print(f"  {b['bin']:10} n={b['n']:3}  said {b['avg_conf']:.2f}  was right {b['accuracy']:4.0%}  {bar}")
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--reliability", action="store_true")
    ap.add_argument("--question", default="department", choices=["department", "urgency"])
    ap.add_argument("--ci", action="store_true", help="bootstrap 95%% CIs for accuracy/ECE + paired difference vs jev")
    ap.add_argument("--json", help="also write the summary here")
    a = ap.parse_args()
    paths = a.paths or sorted(glob.glob(str(ROOT / "results" / "ex2_*.jsonl")))
    if not paths:
        sys.exit("no results yet: run ex2 first (or MOCK=1 to replay the committed ones)")
    out = report(paths, a.reliability, a.question, a.ci)
    if a.json:
        json.dump(out, open(a.json, "w"), indent=1)
