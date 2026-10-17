"""The "new service": the same logic behind a small REST API (FastAPI).

  uvicorn ex3_new_service.api:app --reload      # then POST /interest-runs
"""
from __future__ import annotations

from decimal import Decimal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .contract import Account, CategoryBalance, JobAbend
from .interest import post_interest

app = FastAPI(title="Card interest service (modernized CBACT04C)")


class AccountIn(BaseModel):
    acct_id: str
    curr_bal: Decimal
    curr_cyc_credit: Decimal = Decimal(0)
    curr_cyc_debit: Decimal = Decimal(0)
    group_id: str = ""


class RateIn(BaseModel):
    group_id: str
    type_cd: str
    cat_cd: str
    rate: Decimal


class BalanceIn(BaseModel):
    acct_id: str
    type_cd: str
    cat_cd: str
    balance: Decimal


class RunIn(BaseModel):
    run_date: str
    accounts: list[AccountIn]
    card_by_account: dict[str, str]
    rates: list[RateIn]
    balances: list[BalanceIn]
    legacy_compat: bool = True


@app.post("/interest-runs")
def interest_run(req: RunIn):
    accounts = {a.acct_id: Account(a.acct_id, a.curr_bal, a.curr_cyc_credit, a.curr_cyc_debit, a.group_id)
                for a in req.accounts}
    rates = {(r.group_id, r.type_cd, r.cat_cd): r.rate for r in req.rates}
    bals = sorted((CategoryBalance(b.acct_id, b.type_cd, b.cat_cd, b.balance) for b in req.balances),
                  key=lambda b: (b.acct_id, b.type_cd, b.cat_cd))
    try:
        res = post_interest(accounts, req.card_by_account, rates, bals, req.run_date, req.legacy_compat)
    except JobAbend as e:
        raise HTTPException(status_code=422, detail={"abend": e.code, "reason": e.reason}) from e
    return {"transactions": [t.__dict__ for t in res.transactions],
            "accounts": [{"acct_id": a.acct_id, "curr_bal": a.curr_bal, "curr_cyc_credit": a.curr_cyc_credit,
                          "curr_cyc_debit": a.curr_cyc_debit} for a in res.accounts.values()]}
