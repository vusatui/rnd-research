"""The contract every implementation of the interest job must satisfy (reference or LLM-generated).

Domain objects only: no fixed-width records, no zoned decimals. The byte-level codec lives in
ex4_equivalence/adapter.py so that implementations are compared on the exact same footing.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal


class JobAbend(Exception):
    """Raised where the legacy job would abend (CEE3ABD). `code` mirrors the user abend code."""

    def __init__(self, code: int, reason: str):
        super().__init__(f"abend {code}: {reason}")
        self.code, self.reason = code, reason


@dataclass
class Account:
    acct_id: str                 # 11 digits, e.g. "00000000001"
    curr_bal: Decimal
    curr_cyc_credit: Decimal
    curr_cyc_debit: Decimal
    group_id: str                # disclosure group, may be blank
    other: dict = field(default_factory=dict)  # untouched fields, carried through


@dataclass(frozen=True)
class CategoryBalance:
    acct_id: str
    type_cd: str                 # 2 chars
    cat_cd: str                  # 4 digits
    balance: Decimal


@dataclass
class InterestTransaction:
    tran_id: str                 # 16 chars
    type_cd: str
    cat_cd: str
    source: str
    desc: str
    amount: Decimal
    card_num: str


@dataclass
class InterestResult:
    transactions: list[InterestTransaction]
    accounts: dict[str, Account]  # account state after the run, keyed by acct_id


# Signature every implementation exposes:
# def post_interest(accounts: dict[str, Account], card_by_account: dict[str, str],
#                   rates: dict[tuple[str, str, str], Decimal], balances: list[CategoryBalance],
#                   run_date: str) -> InterestResult
#   rates key = (group_id, type_cd, cat_cd); group_id is the 10-char value stripped of trailing spaces.
#   balances arrive sorted by (acct_id, type_cd, cat_cd).
