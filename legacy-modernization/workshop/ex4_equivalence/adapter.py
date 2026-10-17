"""Byte-level adapter: legacy fixed-width records <-> domain objects of ex3_new_service.contract.

Both sides of the diamond see identical input bytes and are compared as identical output bytes,
so encoding mistakes (sign overpunch, truncation, padding) count as real differences.
"""
from __future__ import annotations

from decimal import Decimal

from common.records import ACCOUNT, DISCGRP, TCATBAL, TRAN, XREF, parse, render
from ex3_new_service.contract import Account, CategoryBalance, InterestResult, JobAbend

# Comparison schema (per-field rules), like a characterization-test spec:
TS_FIELDS = ("orig_ts", "proc_ts")   # current-time stamps: masked
IGNORED = ("filler",)                # FILLER bytes: never read by consumers (verify per program!)
# Alphanumeric fields built with STRING ... INTO are not space-padded: the rest of the field keeps
# whatever was in uninitialized WORKING-STORAGE (LOW-VALUES under GnuCOBOL -std=ibm; on z/OS it
# depends on compiler/LE options). Lenient mode treats trailing NULs as spaces; --strict does not.


def to_domain(inputs: dict):
    accounts = {}
    for line in inputs["accounts"]:
        p = parse(line, ACCOUNT)
        other = {k: v for k, v in p.items() if k not in {"acct_id", "curr_bal", "curr_cyc_credit", "curr_cyc_debit", "group_id"}}
        accounts[p["acct_id"]] = Account(p["acct_id"], p["curr_bal"], p["curr_cyc_credit"], p["curr_cyc_debit"],
                                         p["group_id"], other)
    card_by_account = {}
    for line in inputs["xrefs"]:
        p = parse(line, XREF)
        card_by_account.setdefault(p["acct_id"], p["card_num"])
    rates = {}
    for line in inputs["discgrps"]:
        p = parse(line, DISCGRP)
        rates[(p["group_id"], line[10:12], p["cat_cd"])] = p["int_rate"]
    bals = []
    for line in sorted(inputs["tcatbals"], key=lambda r: r[:17]):
        p = parse(line, TCATBAL)
        bals.append(CategoryBalance(p["acct_id"], line[11:13], p["cat_cd"], p["balance"]))
    return accounts, card_by_account, rates, bals


def account_line(a: Account) -> str:
    return render({"acct_id": a.acct_id, "curr_bal": a.curr_bal, "curr_cyc_credit": a.curr_cyc_credit,
                   "curr_cyc_debit": a.curr_cyc_debit, "group_id": a.group_id, **a.other}, ACCOUNT)


def tran_line(t) -> str:
    return render({"tran_id": t.tran_id, "type_cd": t.type_cd, "cat_cd": t.cat_cd, "source": t.source,
                   "desc": t.desc, "amount": Decimal(t.amount), "merchant_id": 0, "card_num": t.card_num,
                   "orig_ts": "", "proc_ts": ""}, TRAN)


def run_modern(post_interest, inputs: dict, parm: str, **kw) -> dict:
    accounts, cards, rates, bals = to_domain(inputs)
    try:
        res: InterestResult = post_interest(accounts, cards, rates, bals, parm, **kw)
    except JobAbend as e:
        return {"abend": e.code, "transactions": [], "accounts": []}
    accts = [account_line(res.accounts[k]) for k in sorted(res.accounts)]
    return {"abend": None, "transactions": [tran_line(t) for t in res.transactions], "accounts": accts}


def mask(tran: str, strict: bool = False) -> str:
    if strict:
        return tran[:-72] + " " * 72  # only the two timestamps (and trailing filler) are masked
    p = parse(tran.replace("\x00", " "), TRAN)
    for f in TS_FIELDS + IGNORED:
        p[f] = ""
    return render(p, TRAN)
