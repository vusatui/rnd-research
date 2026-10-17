"""LLM-as-judge pitfalls, measured on 8 hand-made pairs where the right answer is known (see judge_pairs.jsonl):
the *good* answer is short and policy-compliant, the *bad* one is long, warm and violates the policy.

  1. pairwise accuracy and position bias: ask "A or B?" in both orders; count wrong picks and order flips;
  2. pointwise scores (1-5) for good vs bad: does verbosity/politeness buy points?
  3. the same pairwise test *with the policy in the prompt* - grounding the judge in the rule.

  python ex2_evals/judge_bias.py --judges nvidia/nemotron-3-super-120b-a12b:free,poolside/laguna-s-2.1:free
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.llm import chat  # noqa: E402
from common.paths import OUT  # noqa: E402

HERE = Path(__file__).resolve().parent

PAIR = """You are evaluating two customer-support replies to the same customer message.
{policy}Customer message: {q}

Reply A:
{a}

Reply B:
{b}

Which reply is better overall? Answer with exactly one letter: A or B."""

POINT = """Rate this customer-support reply from 1 (very bad) to 5 (excellent) for overall quality.
{policy}Customer message: {q}

Reply:
{r}

Answer with a single digit 1-5."""


def ask(judge, prompt):
    r = chat([{"role": "user", "content": prompt}], model=judge, fallback=False, max_tokens=10)
    return (r.message.content or "").strip()


def letter(text):
    m = re.search(r"\b([AB])\b", text.upper())
    return m.group(1) if m else "?"


def digit(text):
    m = re.search(r"[1-5]", text)
    return int(m.group(0)) if m else None


def run(judge, pairs, with_policy):
    res = {"correct": 0, "total": 0, "flips": 0, "first_pos": 0, "unparsed": 0, "detail": []}
    for p in pairs:
        pol = f"Store policy: {p['policy']}\n" if with_policy else ""
        x = letter(ask(judge, PAIR.format(policy=pol, q=p["question"], a=p["good"], b=p["bad"])))  # good is A
        y = letter(ask(judge, PAIR.format(policy=pol, q=p["question"], a=p["bad"], b=p["good"])))  # good is B
        res["correct"] += (x == "A") + (y == "B")
        res["total"] += 2
        res["flips"] += (x == y and x != "?")          # same letter both times = followed position, not content
        res["first_pos"] += (x == "A") + (y == "A")
        res["unparsed"] += (x == "?") + (y == "?")
        res["detail"].append({"id": p["id"], "good_first": x, "good_second": y})
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--judges", default="nvidia/nemotron-3-super-120b-a12b:free,poolside/laguna-s-2.1:free")
    a = ap.parse_args()
    pairs = [json.loads(x) for x in (HERE / "judge_pairs.jsonl").read_text().splitlines() if x.strip()]
    path = OUT / "judge_bias.json"
    report = json.loads(path.read_text()) if path.exists() else {}
    for judge in a.judges.split(","):
        try:
            r_np = run(judge, pairs, with_policy=False)
            r_p = run(judge, pairs, with_policy=True)
            good, bad = [], []
            for p in pairs:
                good.append(digit(ask(judge, POINT.format(policy="", q=p["question"], r=p["good"]))))
                bad.append(digit(ask(judge, POINT.format(policy="", q=p["question"], r=p["bad"]))))
        except Exception as e:  # noqa: BLE001
            print(f"{judge}: failed ({e})")
            continue
        g = [x for x in good if x]
        b = [x for x in bad if x]
        report[judge] = {
            "pairwise_no_policy": {k: v for k, v in r_np.items()},
            "pairwise_with_policy": {k: v for k, v in r_p.items()},
            "pointwise_no_policy": {"good_mean": round(statistics.mean(g), 2) if g else None,
                                    "bad_mean": round(statistics.mean(b), 2) if b else None,
                                    "bad_scored_>=_good": sum(1 for x, y in zip(good, bad) if x and y and y >= x),
                                    "good": good, "bad": bad},
        }
        print(f"\n== judge {judge}")
        for name, r in (("no policy", r_np), ("with policy", r_p)):
            print(f"  pairwise {name:11}: correct {r['correct']}/{r['total']}, same-letter-both-orders "
                  f"{r['flips']}/{len(pairs)}, picked first slot {r['first_pos']}/{r['total']}, unparsed {r['unparsed']}")
        pw = report[judge]["pointwise_no_policy"]
        print(f"  pointwise (no policy): good mean {pw['good_mean']}, bad mean {pw['bad_mean']}, "
              f"bad >= good in {pw['bad_scored_>=_good']}/{len(pairs)}  good={good} bad={bad}")
        path.write_text(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
