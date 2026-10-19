"""Exact vs semantic caching on 24 labelled query pairs (offline, no LLM calls).

A semantic cache returns a stored answer when a new query's embedding is "similar enough" to a cached one.
That saves a model call, but a near-miss with a different meaning (upgrade vs downgrade, annual vs monthly)
returns a WRONG answer at zero marginal cost. This script sweeps the similarity threshold and shows hit rate on
true paraphrases vs false-hit rate on near-misses.

    python ex3_semantic_cache/semantic_cache.py              # local embeddings (fastembed, BAAI/bge-small-en-v1.5)
    python ex3_semantic_cache/semantic_cache.py --lexical    # no download: character 3-gram TF-IDF cosine
"""
from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path

PAIRS = [json.loads(line) for line in (Path(__file__).parent / "pairs.jsonl").read_text().splitlines() if line.strip()]


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", "", s.lower())).strip()


def lexical_sims(pairs):
    def grams(s):
        s = f"  {norm(s)}  "
        return Counter(s[i:i + 3] for i in range(len(s) - 2))
    docs = [grams(p["cached"]) for p in pairs] + [grams(p["new"]) for p in pairs]
    df = Counter(g for d in docs for g in d)
    n = len(docs)

    def vec(d):
        return {g: c * math.log(n / df[g]) for g, c in d.items()}

    def cos(a, b):
        dot = sum(v * b.get(k, 0) for k, v in a.items())
        return dot / (math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values())) or 1)
    return [cos(vec(grams(p["cached"])), vec(grams(p["new"]))) for p in pairs]


def embedding_sims(pairs, model="BAAI/bge-small-en-v1.5"):
    import numpy as np
    from fastembed import TextEmbedding
    m = TextEmbedding(model)
    a = np.array(list(m.embed([p["cached"] for p in pairs])))
    b = np.array(list(m.embed([p["new"] for p in pairs])))
    a /= np.linalg.norm(a, axis=1, keepdims=True)
    b /= np.linalg.norm(b, axis=1, keepdims=True)
    return [float(x) for x in (a * b).sum(1)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lexical", action="store_true")
    a = ap.parse_args()
    sims = lexical_sims(PAIRS) if a.lexical else embedding_sims(PAIRS)
    kind = "char-3gram TF-IDF" if a.lexical else "bge-small-en-v1.5 embeddings"
    same = [s for s, p in zip(sims, PAIRS) if p["same"]]
    diff = [s for s, p in zip(sims, PAIRS) if not p["same"]]
    exact_hits = sum(norm(p["cached"]) == norm(p["new"]) for p in PAIRS if p["same"])
    print(f"similarity ({kind}): paraphrases mean {sum(same)/len(same):.3f} [min {min(same):.3f}, max {max(same):.3f}]"
          f" | near-misses mean {sum(diff)/len(diff):.3f} [min {min(diff):.3f}, max {max(diff):.3f}]")
    print(f"exact-match cache: {exact_hits}/{len(same)} paraphrase hits, 0/{len(diff)} false hits\n")
    print("| threshold | paraphrase hits (saved calls) | near-miss hits (WRONG answers served) |\n|---|---|---|")
    rows = []
    for th in [0.70, 0.75, 0.80, 0.85, 0.90, 0.95]:
        h = sum(s >= th for s in same)
        f = sum(s >= th for s in diff)
        rows.append({"threshold": th, "hits": h, "false_hits": f})
        print(f"| {th:.2f} | {h}/{len(same)} | {f}/{len(diff)} |")
    print("\nWorst near-misses (highest similarity, different answer):")
    for s, p in sorted(((s, p) for s, p in zip(sims, PAIRS) if not p["same"]), key=lambda x: -x[0])[:4]:
        print(f"  {s:.3f}  '{p['cached']}'  vs  '{p['new']}'")
    out = Path(__file__).resolve().parent.parent / "out" / f"semantic_cache_{'lexical' if a.lexical else 'embed'}.json"
    out.write_text(json.dumps({"kind": kind, "sims": sims, "sweep": rows}, indent=1))


if __name__ == "__main__":
    main()
