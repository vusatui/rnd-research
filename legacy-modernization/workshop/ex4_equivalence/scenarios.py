"""Characterization inputs for the diamond. Real CardDemo reference data + generated balances.

The CardDemo sample TCATBALF has all-zero balances (balances are produced by the POSTTRAN job),
so on its own it proves almost nothing. We keep it, then add generated "posted" balances that
exercise the rules: negatives, sub-cent truncation, several categories per account, group hits
vs DEFAULT fallback, zero-rate groups and two abend paths.
"""
from __future__ import annotations

import random
from decimal import Decimal

from common.records import ACCOUNT, TCATBAL, parse, render
from legacy.run_legacy import carddemo_inputs

DEFAULT_COMBOS = [("01", "0001"), ("01", "0002"), ("01", "0003"), ("01", "0004"), ("02", "0001"),
                  ("02", "0002"), ("02", "0003"), ("03", "0001"), ("03", "0002"), ("03", "0003"),
                  ("04", "0001"), ("04", "0002"), ("04", "0003"), ("05", "0001"), ("06", "0001"),
                  ("06", "0002"), ("07", "0001")]
EDGE_AMOUNTS = ["999.99", "0.01", "-0.01", "-100.07", "79.99", "1234.56", "0.00", "-999999999.99", "999999999.99"]


def _tcat(acct_id: str, type_cd: str, cat_cd: str, bal: Decimal) -> str:
    return render({"acct_id": acct_id, "type_cd": type_cd, "cat_cd": cat_cd, "balance": bal}, TCATBAL)


def _with_group(acct_line: str, group: str) -> str:
    p = parse(acct_line, ACCOUNT)
    p["group_id"] = group
    return render(p, ACCOUNT)


def generated(seed: int, n_accounts: int = 12, groups: bool = True) -> dict:
    rng = random.Random(seed)
    base = carddemo_inputs()
    accts = base["accounts"][:]
    if groups:  # CardDemo accounts have a blank group id; give some a real one to exercise the primary lookup
        for i in range(len(accts)):
            r = rng.random()
            if r < 0.3:
                accts[i] = _with_group(accts[i], "A000000000")
            elif r < 0.4:
                accts[i] = _with_group(accts[i], "ZEROAPR")
    ids = sorted(parse(a, ACCOUNT)["acct_id"] for a in accts)
    tc = []
    for acct_id in rng.sample(ids, n_accounts):
        for type_cd, cat_cd in rng.sample(DEFAULT_COMBOS, rng.randint(1, 4)):
            if rng.random() < 0.25:
                bal = Decimal(rng.choice(EDGE_AMOUNTS))
            else:
                bal = Decimal(rng.randint(-50_000_00, 500_000_00)) / 100
            tc.append(_tcat(acct_id, type_cd, cat_cd, bal))
    return {**base, "accounts": accts, "tcatbals": tc}


def scenarios(n_random: int = 20) -> dict[str, dict]:
    base = carddemo_inputs()
    out = {"carddemo-sample-data": base}
    out["edge-amounts"] = {**base, "tcatbals": [_tcat(f"{i + 1:011d}", "01", "0001", Decimal(a))
                                                for i, a in enumerate(EDGE_AMOUNTS)]}
    out["single-account"] = {**base, "tcatbals": [_tcat("00000000005", "01", "0001", Decimal("1000.00"))]}
    for s in range(n_random):
        out[f"random-seed-{s}"] = generated(s)
    out["abend-missing-default-rate"] = {**base, "tcatbals": [_tcat("00000000001", "01", "0001", Decimal("10.00")),
                                                              _tcat("00000000002", "09", "0001", Decimal("10.00"))]}
    out["abend-unknown-account"] = {**base, "tcatbals": [_tcat("00000000001", "01", "0001", Decimal("10.00")),
                                                         _tcat("00000099999", "01", "0001", Decimal("10.00"))]}
    return out
