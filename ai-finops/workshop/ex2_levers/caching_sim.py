"""Prompt-caching economics, provider by provider (offline; uses token counts from a saved levers run).

Free endpoints rarely reveal a provider's real cache behaviour, so this applies each provider's PUBLISHED caching
rules to our measured prompt shape (stable prefix tokens vs per-ticket tokens). Rules as documented on 2026-10-19:

  OpenAI GPT-5.6+   write 1.25x input, read 0.10x (0.05x on gpt-6.1-sol), min 1,024 tok, TTL >= 30 min
                    https://platform.openai.com/docs/guides/prompt-caching
  Anthropic (5 min) write 1.25x input, read 0.10x (0.05x Opus/Sonnet 5.5), min 512-4,096 tok by model; 1 h TTL: write 2x
                    https://platform.claude.com/docs/en/build-with-claude/prompt-caching
  Gemini (implicit) no write fee, read $0.10 vs $2.00 input on Gemini 4 Argon (0.05x), min 4,096 tok, best effort
                    https://ai.google.dev/gemini-api/docs/caching , https://ai.google.dev/gemini-api/docs/pricing

    python ex2_levers/caching_sim.py out/levers_<stamp>.json --config C_stable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.pipeline import load_tickets  # noqa: E402

RULES = {
    "no caching":                 dict(write=1.00, read=1.00, min_tokens=0),
    "OpenAI GPT-5.6+ (0.10x)":    dict(write=1.25, read=0.10, min_tokens=1024),
    "OpenAI gpt-6.1-sol (0.05x)": dict(write=1.25, read=0.05, min_tokens=1024),
    "Anthropic 5-min (0.10x)":    dict(write=1.25, read=0.10, min_tokens=1024),
    "Anthropic 1-hour (0.10x)":   dict(write=2.00, read=0.10, min_tokens=1024),
    "Gemini implicit (0.05x)":    dict(write=1.00, read=0.05, min_tokens=4096),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--config", default="C_stable")
    a = ap.parse_args()
    data = json.loads(Path(a.run).read_text())
    rows = [r for r in data["rows"][a.config] if r["input_tokens"]]
    tickets = {t["id"]: t for t in load_tickets()}
    # per-ticket part ~ user turn (dynamic header + ticket text); ~4 chars per token is an approximation
    dyn = sum((len(tickets[r["ticket"]]["text"]) + 90) / 4 for r in rows) / len(rows)
    avg_in = sum(r["input_tokens"] for r in rows) / len(rows)
    prefix = avg_in - dyn
    print(f"{a.config}: avg input {avg_in:,.0f} tok = stable prefix ~{prefix:,.0f} + per-ticket ~{dyn:,.0f}\n")
    print("Input-token cost multiplier vs no caching, by requests sharing the prefix within one TTL window:")
    ns = [1, 2, 5, 20, 100]
    print("| provider rule | " + " | ".join(f"N={n}" for n in ns) + " |\n|---|" + "---|" * len(ns))
    out = {}
    for name, r in RULES.items():
        cells = []
        for n in ns:
            if prefix < r["min_tokens"]:
                mult = 1.0
            else:
                pref_cost = (r["write"] + (n - 1) * r["read"]) / n   # per request, in units of uncached prefix
                mult = (prefix * pref_cost + dyn) / avg_in
            cells.append(mult)
        out[name] = cells
        print(f"| {name} | " + " | ".join(f"{m:.2f}x" for m in cells) + " |")
    print("\nN=1 means a cache write that is never read: caching with a write premium then costs MORE than no "
          "caching. A dynamic value at the top of the prompt (config A/B/E: timestamp + ticket id) makes every "
          "request N=1.")
    measured = sum(r["cached_tokens"] for r in rows) / sum(r["input_tokens"] for r in rows)
    print(f"Measured on the free endpoint in this run: cache hit rate {measured:.0%} of input tokens.")
    Path(a.run).with_name(Path(a.run).stem + f"_cachesim_{a.config}.json").write_text(
        json.dumps({"prefix": prefix, "per_ticket": dyn, "N": ns, "multipliers": out}, indent=1))


if __name__ == "__main__":
    main()
