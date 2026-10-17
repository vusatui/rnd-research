"""Exercise 2: business-rule extraction with an LLM, then *check* it.

1. Send CBACT04C (with line numbers) + its copybooks to a free OpenRouter model.
2. Ask for structured rules, each citing source line ranges and COBOL symbols.
3. Grounding check (deterministic): do the cited lines exist and mention the cited symbols?
4. Score against a hand-verified answer key (gold_rules.json): recall + which rules were missed.
5. Optional --runs N: repeat and measure drift (same prompt, different answers?).

Usage: python ex2_rule_extraction/extract.py [--runs 2]
Writes out/rules.json (last run) and out/rules_report.json.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common.llm import chat, extract_json  # noqa: E402
from common.paths import APP, CBACT04C, OUT  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
SRC_LINES = CBACT04C.read_text(encoding="latin-1").splitlines()

PROMPT = """You are a senior mainframe analyst doing business-rule extraction for a modernization program.
Extract EVERY business rule and behaviour of the COBOL batch program below that a re-implementation must preserve:
calculations (including precision/rounding), lookups and fallbacks, control flow (loops, control breaks, end-of-file
handling), outputs written, error handling, and anything that looks like a defect or unfinished code.

Return ONLY JSON of the form:
{"rules": [{"id": "R1", "title": "...", "description": "precise, testable statement",
            "category": "calculation|lookup|control-flow|output|error-handling|defect",
            "source_lines": [[start, end]], "symbols": ["COBOL-NAME", ...], "confidence": 0.0-1.0}]}
Line numbers refer to the numbered program listing. Cite the narrowest ranges that prove each rule.

PROGRAM CBACT04C (numbered):
{program}

COPYBOOKS:
{copybooks}
"""


def numbered() -> str:
    return "\n".join(f"{i:4d} {line.rstrip()}" for i, line in enumerate(SRC_LINES, 1))


def copybooks() -> str:
    out = []
    for name in re.findall(r"COPY\s+([A-Z0-9]+)", CBACT04C.read_text()):
        p = APP / "cpy" / f"{name}.cpy"
        out.append(f"--- {name} ---\n{p.read_text(encoding='latin-1')}")
    return "\n".join(out)


def norm_ranges(rule: dict) -> list:
    """Accept [[a, b]], [a, b], [[a]] and [a] (models are sloppy about the shape); keep invalid ones for reporting."""
    raw = rule.get("source_lines") or []
    if raw and all(isinstance(x, int) for x in raw):
        raw = [raw] if len(raw) == 2 else [[x, x] for x in raw]
    return [[r[0], r[0]] if isinstance(r, list) and len(r) == 1 else r for r in raw]


def grounded(rule: dict) -> tuple[bool, str]:
    ranges = norm_ranges(rule)
    if not ranges:
        return False, "no source lines"
    text = ""
    for r in ranges:
        if not (isinstance(r, list) and len(r) == 2 and 1 <= int(r[0]) <= int(r[1]) <= len(SRC_LINES)):
            return False, f"bad range {r}"
        text += "\n".join(SRC_LINES[int(r[0]) - 1:int(r[1])]).upper()
    syms = [s.upper() for s in rule.get("symbols") or []]
    if syms and not any(s in text for s in syms):
        return False, f"none of {syms[:4]} appear in cited lines"
    return True, "ok"


def overlaps(a, b) -> bool:
    return int(a[0]) <= b[1] and b[0] <= int(a[1])


def score(rules: list[dict], gold: list[dict]) -> dict:
    covered = {}
    for g in gold:
        for r in rules:
            blob = f"{r.get('title', '')} {r.get('description', '')}".lower()
            ranges = [x for x in norm_ranges(r) if isinstance(x, list) and len(x) == 2]
            polarity_ok = not g.get("require_any") or any(k in blob for k in g["require_any"])
            if (any(overlaps(x, a) for x in ranges for a in g["anchor"]) and polarity_ok
                    and any(k.lower() in blob for k in g["keywords"])):
                covered[g["id"]] = r.get("id")
                break
    return {"recall": round(len(covered) / len(gold), 2), "covered": covered,
            "missed": [g["id"] for g in gold if g["id"] not in covered]}


def run_once() -> dict:
    t0 = time.time()
    prompt = PROMPT.replace("{program}", numbered()).replace("{copybooks}", copybooks())
    text, model = chat([{"role": "user", "content": prompt}], max_tokens=16000,
                       validate=lambda t: extract_json(t)["rules"])
    rules = extract_json(text).get("rules", [])
    checks = [(r.get("id"), *grounded(r)) for r in rules]
    gold = json.loads((HERE / "gold_rules.json").read_text())["rules"]
    return {"model": model, "seconds": round(time.time() - t0, 1), "n_rules": len(rules),
            "ungrounded": [{"id": i, "why": why} for i, ok, why in checks if not ok],
            "score": score(rules, gold), "rules": rules}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--rescore", action="store_true", help="re-score out/rules.json against the answer key, no LLM call")
    a = ap.parse_args()
    if a.rescore:
        rules = json.loads((OUT / "rules.json").read_text())["rules"]
        gold = json.loads((HERE / "gold_rules.json").read_text())["rules"]
        s = score(rules, gold)
        print(f"{len(rules)} rules | ungrounded {sum(1 for r in rules if not grounded(r)[0])} | "
              f"recall {s['recall']} | missed: {', '.join(s['missed']) or '-'}")
        return
    runs = []
    for i in range(a.runs):
        r = run_once()
        runs.append(r)
        s = r["score"]
        print(f"run {i + 1}: {r['model']} | {r['seconds']}s | {r['n_rules']} rules | "
              f"ungrounded {len(r['ungrounded'])} | recall vs answer key {s['recall']} | missed: {', '.join(s['missed']) or '-'}")
        for u in r["ungrounded"]:
            print(f"   ungrounded {u['id']}: {u['why']}")
    (OUT / "rules.json").write_text(json.dumps({"program": "CBACT04C", "rules": runs[-1]["rules"]}, indent=1))
    report = [{k: v for k, v in r.items() if k != "rules"} for r in runs]
    if len(runs) > 1:
        sets = [set(r["score"]["covered"]) for r in runs]
        inter, union = set.intersection(*sets), set.union(*sets)
        drift = round(1 - len(inter) / max(1, len(union)), 2)
        print(f"drift across {len(runs)} runs (1 - Jaccard of covered gold rules): {drift}; "
              f"unstable: {', '.join(sorted(union - inter)) or '-'}")
        report.append({"drift": drift, "unstable": sorted(union - inter)})
    (OUT / "rules_report.json").write_text(json.dumps(report, indent=1))
    print("wrote out/rules.json and out/rules_report.json")


if __name__ == "__main__":
    main()
