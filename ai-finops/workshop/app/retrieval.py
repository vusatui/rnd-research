"""Tiny BM25 retriever over the knowledge-base sections (no dependencies, no embeddings, deterministic).
Context trimming lever: send the top-k relevant sections instead of the whole knowledge base."""
from __future__ import annotations

import math
import re
from functools import lru_cache
from pathlib import Path

KB_DIR = Path(__file__).parent / "kb"
_STOP = set("a an the and or of to in on for is are be can do does i we you our your my it this that with at by from "
            "as how what when will not no if have has was were me us they them their there just any all".split())


def _tok(s: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in _STOP and len(w) > 1]


@lru_cache(maxsize=1)
def sections() -> dict[str, str]:
    out = {}
    for f in sorted(KB_DIR.glob("*.md")):
        text = f.read_text()
        sid = re.search(r"\[(\w+)\]", text).group(1)
        out[sid] = text.strip()
    return out


def full_kb() -> str:
    return "\n\n".join(sections().values())


def top_k(query: str, k: int = 3, k1: float = 1.5, b: float = 0.75) -> list[str]:
    docs = {sid: _tok(t) for sid, t in sections().items()}
    n = len(docs)
    avg = sum(len(d) for d in docs.values()) / n
    df: dict[str, int] = {}
    for d in docs.values():
        for w in set(d):
            df[w] = df.get(w, 0) + 1
    q = _tok(query)
    scores = {}
    for sid, d in docs.items():
        s = 0.0
        for w in q:
            tf = d.count(w)
            if not tf:
                continue
            idf = math.log(1 + (n - df[w] + 0.5) / (df[w] + 0.5))
            s += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(d) / avg))
        scores[sid] = s
    return [sid for sid, _ in sorted(scores.items(), key=lambda x: -x[1])[:k]]
