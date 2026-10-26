"""Experiment 3: SynthID-Text on a small local model - detect, then attack.

  python ex3_text_watermark/run_lab.py                 # offline: generation + truncation/edit attacks (CPU, ~10 min first run)
  python ex3_text_watermark/run_lab.py --llm-attacks   # + paraphrase and EN->DE->EN translation via OpenRouter free model (<=24 calls)

Outputs results/ex3_text_<date>.json and .md. Generated texts are cached in results/ex3_texts.json (delete to regenerate).
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.paths import DATA, RESULTS  # noqa: E402
from ex3_text_watermark import lab  # noqa: E402

PROMPTS = [
    "Write a short news-style paragraph about a city council approving a new bicycle lane network.",
    "Explain in one paragraph why the sky is blue, for a curious teenager.",
    "Write a short product description for a reusable stainless-steel water bottle.",
    "Write a paragraph from a travel blog about a rainy day in Lisbon.",
    "Describe in one paragraph how a bill becomes a law in a parliamentary system.",
    "Write a short paragraph welcoming new employees to a software company.",
    "Write a paragraph about the benefits of regular sleep.",
    "Write a short story opening about a lighthouse keeper who finds a message in a bottle.",
    "Summarise in one paragraph what a database index is and why it speeds up queries.",
    "Write a paragraph for a local newsletter about a community garden opening this weekend.",
    "Describe in one paragraph how to brew a good cup of tea.",
    "Write a short paragraph about why museums matter in the digital age.",
]
N_TOK = 150


def load_texts(n):
    cache = RESULTS / "ex3_texts.json"
    if cache.exists():
        d = json.loads(cache.read_text())
        if len(d["wm"]) >= n:
            return d
    d = {"model": lab.MODEL, "wm": [], "plain": []}
    for i, p in enumerate(PROMPTS[:n]):
        for kind, flag in (("wm", True), ("plain", False)):
            t = lab.generate(p, flag, N_TOK, seed=i)
            d[kind].append({"prompt": p, "text": t}); print(f"  generated {kind} {i + 1}/{n}: {lab.n_tokens(t)} tokens", flush=True)
    RESULTS.mkdir(exist_ok=True); cache.write_text(json.dumps(d, indent=1, ensure_ascii=False))
    return d


def summarise(scores, thr):
    s = [x for x in scores if x is not None]
    return {"n": len(s), "mean_g": round(float(np.mean(s)), 4) if s else None,
            "detected": f"{sum(x > thr for x in s)}/{len(s)}"}


def overlap(orig: str, new: str, n: int = 4) -> float:
    """Share of the attacked text's word n-grams that also occur in the original (1.0 = copy, ~0 = fully reworded)."""
    g = lambda t: {tuple(w) for w in zip(*[t.lower().split()[i:] for i in range(n)])}  # noqa: E731
    a, b = g(orig), g(new)
    return len(a & b) / len(b) if b else 0.0


def llm_attacks(wm_texts, k):
    from common.llm import chat
    cache = RESULTS / "ex3_attack_texts.json"
    if cache.exists():
        c = json.loads(cache.read_text())
        if len(c["paraphrase (LLM)"]) >= k:
            return {n: v[:k] for n, v in c.items()}
    out = {"paraphrase (LLM)": [], "translate EN->DE->EN (LLM)": []}
    for t in wm_texts[:k]:
        out["paraphrase (LLM)"].append(chat([{"role": "user", "content": "Paraphrase the following text. Keep the meaning, change the wording "
                                              "and sentence structure. Output only the paraphrase.\n\n" + t}], max_tokens=500, temperature=0.7))
        de = chat([{"role": "user", "content": "Translate to German. Output only the translation.\n\n" + t}], max_tokens=700, temperature=0.2)
        out["translate EN->DE->EN (LLM)"].append(chat([{"role": "user", "content": "Translate to English. Output only the translation.\n\n" + de}],
                                                      max_tokens=700, temperature=0.2))
    RESULTS.mkdir(exist_ok=True); cache.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=12, help="prompts (each gives one watermarked + one plain text)")
    ap.add_argument("--llm-attacks", action="store_true")
    ap.add_argument("--llm-n", type=int, default=6, help="texts sent to the LLM attacks (3 calls each)")
    a = ap.parse_args()

    d = load_texts(a.n)
    wm = [x["text"] for x in d["wm"]][:a.n]; plain = [x["text"] for x in d["plain"]][:a.n]
    human = [json.loads(l)["text"] for l in (DATA / "human_texts.jsonl").read_text().splitlines()]

    null = [lab.mean_g(t) for t in plain + human]
    thr = max(x for x in null if x is not None)       # strict: above every non-watermarked text we have (small sample!)
    rows = {"watermarked (as generated)": summarise([lab.mean_g(t) for t in wm], thr),
            "NULL: unwatermarked LLM text": summarise([lab.mean_g(t) for t in plain], thr),
            "NULL: human text (public domain)": summarise([lab.mean_g(t) for t in human], thr)}
    # length dependence
    length = {}
    for L in (20, 40, 80, 150):
        length[L] = {"wm_mean_g": round(float(np.mean([x for x in (lab.mean_g(t, L) for t in wm) if x is not None] or [np.nan])), 4),
                     "null_mean_g": round(float(np.mean([x for x in (lab.mean_g(t, L) for t in plain + human) if x is not None] or [np.nan])), 4),
                     "wm_detected_at_fixed_thr": f"{sum((lab.mean_g(t, L) or 0) > thr for t in wm)}/{len(wm)}",
                     "null_above_thr": f"{sum((lab.mean_g(t, L) or 0) > thr for t in plain + human)}/{len(plain + human)}"}
    attacks = {}
    for name, fn in [("drop 10% of words", lambda t: lab.drop_words(t, .10)), ("drop 30% of words", lambda t: lab.drop_words(t, .30)),
                     ("swap 20% adjacent words", lambda t: lab.swap_words(t, .20)), ("hyphen typos in 30% of words", lambda t: lab.typo_insert(t, .30)),
                     ("first half only", lambda t: t[: len(t) // 2])]:
        attacks[name] = summarise([lab.mean_g(fn(t)) for t in wm], thr)
    if a.llm_attacks:
        for name, texts in llm_attacks(wm, a.llm_n).items():
            attacks[name] = summarise([lab.mean_g(t) for t in texts], thr)
            attacks[name]["per_text_mean_g"] = [round(lab.mean_g(t) or 0, 3) for t in texts]
            attacks[name]["word_4gram_overlap_with_original"] = round(float(np.mean([overlap(o, t) for o, t in zip(wm, texts)])), 3)
            attacks[name]["sample"] = texts[0][:300]

    res = {"date": datetime.datetime.now().isoformat(timespec="seconds"), "model": lab.MODEL, "tokens_per_text": N_TOK,
           "ngram_len": lab.NGRAM, "detector": "mean g-value (30 layers), threshold = max over all null texts",
           "threshold": round(thr, 4), "n_null": len(null), "baseline": rows, "length": length, "attacks": attacks}
    RESULTS.mkdir(exist_ok=True)
    day = datetime.date.today()
    (RESULTS / f"ex3_text_{day}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    md = [f"Detection threshold (max mean-g over {len(null)} non-watermarked texts): {thr:.4f}", "",
          "| condition | texts | mean g | detected |", "|---|---|---|---|"]
    for k, v in {**rows, **attacks}.items():
        extra = f" (4-gram overlap with original {v['word_4gram_overlap_with_original']})" if "word_4gram_overlap_with_original" in v else ""
        md.append(f"| {k}{extra} | {v['n']} | {v['mean_g']} | {v['detected']} |")
    md += ["", "| tokens scored | watermarked mean g | non-watermarked mean g | watermarked above fixed threshold | NON-watermarked above it (false alarms) |", "|---|---|---|---|---|"]
    for L, v in length.items():
        md.append(f"| first {L} | {v['wm_mean_g']} | {v['null_mean_g']} | {v['wm_detected_at_fixed_thr']} | {v['null_above_thr']} |")
    (RESULTS / f"ex3_text_{day}.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
