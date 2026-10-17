"""Reference modern implementation of the CardDemo interest job (CBACT04C) as plain Python.

Written from the verified rules in ex2_rule_extraction/gold_rules.json, then proven against the
running COBOL by ex4_equivalence/diamond.py. `legacy_compat=True` reproduces the legacy behaviour
bug-for-bug (including the last-account defect); `legacy_compat=False` is the "fixed" version,
which the diamond will flag as a deviation that the business has to approve explicitly.
"""
from __future__ import annotations

import copy
from decimal import ROUND_DOWN, Decimal

from .contract import Account, CategoryBalance, InterestResult, InterestTransaction, JobAbend

CENT = Decimal("0.01")


def monthly_interest(balance: Decimal, annual_rate_pct: Decimal) -> Decimal:
    # COMPUTE WS-MONTHLY-INT = (TRAN-CAT-BAL * DIS-INT-RATE) / 1200   -- no ROUNDED: truncate toward zero
    return (balance * annual_rate_pct / Decimal(1200)).quantize(CENT, rounding=ROUND_DOWN)


def lookup_rate(rates, group_id: str, type_cd: str, cat_cd: str) -> Decimal:
    key = (group_id.rstrip(), type_cd, cat_cd)
    if key in rates:
        return rates[key]
    default = ("DEFAULT", type_cd, cat_cd)  # file status 23 -> retry with group 'DEFAULT'
    if default in rates:
        return rates[default]
    raise JobAbend(999, f"no DEFAULT disclosure rate for type {type_cd} category {cat_cd}")


def post_interest(accounts: dict[str, Account], card_by_account: dict[str, str],
                  rates: dict[tuple[str, str, str], Decimal], balances: list[CategoryBalance],
                  run_date: str, legacy_compat: bool = True) -> InterestResult:
    accounts = copy.deepcopy(accounts)
    txs: list[InterestTransaction] = []
    seq = 0  # global across accounts, like WS-TRANID-SUFFIX
    order: list[str] = []
    totals: dict[str, Decimal] = {}
    for cb in balances:
        if cb.acct_id not in totals:
            if cb.acct_id not in accounts:
                raise JobAbend(999, f"account {cb.acct_id} not found")
            if cb.acct_id not in card_by_account:
                raise JobAbend(999, f"xref for account {cb.acct_id} not found")
            order.append(cb.acct_id)
            totals[cb.acct_id] = Decimal(0)
        acct = accounts[cb.acct_id]
        rate = lookup_rate(rates, acct.group_id, cb.type_cd, cb.cat_cd)
        if rate == 0:
            continue
        amount = monthly_interest(cb.balance, rate)
        totals[cb.acct_id] += amount
        seq += 1
        txs.append(InterestTransaction(
            tran_id=f"{run_date[:10]:<10}{seq:06d}"[:16], type_cd="01", cat_cd="0005", source="System",
            desc=f"Int. for a/c {acct.acct_id}", amount=amount, card_num=card_by_account[cb.acct_id]))
    # Post totals. Legacy defect: the last account in the input is never rewritten.
    to_post = order[:-1] if legacy_compat else order
    for acct_id in to_post:
        a = accounts[acct_id]
        a.curr_bal += totals[acct_id]
        a.curr_cyc_credit = Decimal(0)
        a.curr_cyc_debit = Decimal(0)
    return InterestResult(transactions=txs, accounts=accounts)
