"""Export the cost ledger as FOCUS-shaped rows and build a chargeback report (offline).

FOCUS (FinOps Open Cost and Usage Specification) is the common billing-data schema the FinOps Foundation maintains.
Published version: 1.4 (June 2026). We use a subset of Cost and Usage columns, plus three properties from the
FOCUS 1.5 *working draft* (ratification planned 3 Dec 2026, so names may still change):
  SkuPriceDetails.ModelId / TokenDirection (Input|Output) / TokenCacheAction (Uncached|Read|Write|Other)
  PrincipalId (who made the call) - here the team's gateway key alias, never the key itself.
This is an illustration of the shape, NOT validated with the FOCUS validator.

    python ex4_gateway/to_focus.py                  # from out/ledger.jsonl (all workshop calls)
    python ex4_gateway/to_focus.py --run levers-<stamp>
    python ex4_gateway/to_focus.py --gateway        # from the LiteLLM gateway's spend logs (per team / key)
Sources: https://focus.finops.org/ , https://focus.finops.org/focus-1-5-release-scope/
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common.ledger import load  # noqa: E402
from common.paths import OUT  # noqa: E402
from common.pricing import twin_price  # noqa: E402

COLS = ["ChargePeriodStart", "ChargePeriodEnd", "ChargeCategory", "ServiceCategory", "ServiceName",
        "ServiceProviderName", "SkuId", "ConsumedQuantity", "ConsumedUnit", "PricingQuantity", "PricingUnit",
        "ListUnitPrice", "ListCost", "BilledCost", "BillingCurrency", "PrincipalId", "SkuPriceDetails", "Tags"]


def rows_for(call: dict):
    p = twin_price(call["model"])
    base = call["model"].removesuffix(":free")
    uncached = max(call["input_tokens"] - call["cached_tokens"] - call["cache_write_tokens"], 0)
    parts = [("Input", "Uncached", uncached, p["in"]),
             ("Input", "Read", call["cached_tokens"], p["cached"] if p.get("cached") is not None else p["in"]),
             ("Output", "Uncached", call["output_tokens"], p["out"])]
    for direction, cache, qty, price in parts:
        if not qty:
            continue
        yield {
            "ChargePeriodStart": call["ts"][:13] + ":00:00", "ChargePeriodEnd": call["ts"][:13] + ":59:59",
            "ChargeCategory": "Usage", "ServiceCategory": "AI and Machine Learning",
            "ServiceName": "OpenRouter Chat Completions", "ServiceProviderName": "OpenRouter", "SkuId": base,
            "ConsumedQuantity": qty, "ConsumedUnit": "Tokens", "PricingQuantity": qty, "PricingUnit": "Tokens",
            "ListUnitPrice": price / 1e6, "ListCost": round(qty * price / 1e6, 10),
            "BilledCost": 0.0,   # free endpoint: nothing is billed; ListCost is the shadow (paid-twin) cost
            "BillingCurrency": "USD", "PrincipalId": call.get("principal", f"{call['team']}-bot"),
            "SkuPriceDetails": json.dumps({"ModelId": base, "ModelDeveloper": base.split("/")[0],
                                           "TokenDirection": direction, "TokenCacheAction": cache}),
            "Tags": json.dumps({"team": call["team"], "feature": call["feature"], "config": call["config"]}),
        }


def from_gateway(path: Path) -> list[dict]:
    """Turn LiteLLM spend logs into ledger-like calls (team = gateway team alias, principal = key alias)."""
    calls = []
    for r in json.loads(path.read_text()):
        md = r.get("metadata") or {}
        if r.get("status") != "success":
            continue
        model = (r.get("model") or "").split("/", 1)[-1]
        calls.append({"ts": str(r.get("startTime"))[:19].replace(" ", "T"), "model": model,
                      "input_tokens": r.get("prompt_tokens") or 0, "cached_tokens": 0, "cache_write_tokens": 0,
                      "output_tokens": r.get("completion_tokens") or 0,
                      "team": md.get("user_api_key_team_alias") or r.get("team_alias") or "unknown",
                      "principal": md.get("user_api_key_alias") or r.get("key_alias") or "unknown",
                      "feature": next((t for t in (r.get("request_tags") or []) if not t.startswith(("T", "User-"))),
                                      "untagged"),
                      "config": f"gateway:{r.get('model_group')}", "gateway_spend": r.get("spend")})
    return calls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run")
    ap.add_argument("--gateway", nargs="?", const=str(OUT / "gateway_spend_logs.json"),
                    help="use LiteLLM spend logs (from run_teams.py --report) instead of the workshop ledger")
    a = ap.parse_args()
    if a.gateway and not Path(a.gateway).exists():
        raise SystemExit(f"{a.gateway} not found: run `python ex4_gateway/run_teams.py --report` first, or use the "
                         "committed logs: python ex4_gateway/to_focus.py --gateway results/gateway_spend_logs_reduced.json")
    calls = from_gateway(Path(a.gateway)) if a.gateway else load(run=a.run)
    if not calls:
        raise SystemExit("ledger is empty (out/ledger.jsonl is written by live runs): run ex2_levers/run_levers.py "
                         "or cache_probe.py first")
    out = OUT / ("focus_gateway.csv" if a.gateway else "focus_cost_usage.csv")
    agg = defaultdict(lambda: [0, 0.0])
    n = 0
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, COLS)
        w.writeheader()
        for c in calls:
            for r in rows_for(c):
                w.writerow(r)
                n += 1
                tags = json.loads(r["Tags"])
                d = json.loads(r["SkuPriceDetails"])
                k = (tags["team"], tags["config"], r["SkuId"].split("/")[-1], d["TokenDirection"], d["TokenCacheAction"])
                agg[k][0] += r["ConsumedQuantity"]
                agg[k][1] += r["ListCost"]
    print(f"{n} FOCUS-shaped rows from {len(calls)} calls -> {out}\n")
    print("Chargeback (shadow ListCost, paid-twin prices):")
    print("| team | config | model | direction | cache | tokens | ListCost $ |\n|---|---|---|---|---|---|---|")
    for k, (q, usd) in sorted(agg.items()):
        print(f"| {' | '.join(k)} | {q:,} | {usd:.6f} |")


if __name__ == "__main__":
    main()
