"""Offline checks (no LLM, no network): codec, graph, API, diamond on the reference implementation."""
import pathlib
import subprocess
import sys
from decimal import Decimal

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from common.records import decode_zoned, encode_zoned  # noqa: E402


@pytest.mark.parametrize("text,scale,value", [("0000010{", 2, Decimal("1.00")), ("0000102}", 2, Decimal("-10.20")),
                                              ("0000012J", 2, Decimal("-1.21")), ("00000005", 2, Decimal("0.05"))])
def test_decode_zoned(text, scale, value):
    assert decode_zoned(text, scale) == value


def test_encode_truncates_like_cobol_move():
    assert encode_zoned(Decimal("-0.019"), 9, 2) == "0000000000J"  # -0.01
    assert encode_zoned(Decimal("-0.009"), 9, 2) == "0000000000{"  # truncates to 0 -> positive zero
    assert encode_zoned(Decimal("12.349"), 3, 2) == "0123D"   # truncated, not rounded


def test_dependency_graph():
    from ex1_dependency_graph.graph import build_graph
    g = build_graph()
    edges = {(e["src"], e["dst"], e["rel"]) for e in g["edges"]}
    assert ("JOB:INTCALC", "CBACT04C", "runs") in edges
    assert ("CBACT04C", "ACCTDATA", "updates") in edges


def test_api_matches_reference():
    from fastapi.testclient import TestClient
    from ex3_new_service.api import app
    body = {"run_date": "2022071800",
            "accounts": [{"acct_id": "00000000001", "curr_bal": "100.00"},
                         {"acct_id": "00000000002", "curr_bal": "50.00"}],
            "card_by_account": {"00000000001": "4111111111111111", "00000000002": "4222222222222222"},
            "rates": [{"group_id": "DEFAULT", "type_cd": "01", "cat_cd": "0001", "rate": "15.00"}],
            "balances": [{"acct_id": "00000000001", "type_cd": "01", "cat_cd": "0001", "balance": "1000.00"},
                         {"acct_id": "00000000002", "type_cd": "01", "cat_cd": "0001", "balance": "-0.07"}]}
    r = TestClient(app).post("/interest-runs", json=body).json()
    assert [t["amount"] for t in r["transactions"]] == ["12.50", "0.00"]
    assert r["transactions"][1]["tran_id"] == "2022071800000002"
    bal = {a["acct_id"]: a["curr_bal"] for a in r["accounts"]}
    assert bal == {"00000000001": "112.50", "00000000002": "50.00"}  # last account not posted (legacy defect)


def test_diamond_reference_is_equivalent():
    r = subprocess.run([sys.executable, "ex4_equivalence/diamond.py", "--random", "3"], cwd=ROOT,
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-2000:]


def test_diamond_catches_the_fix():
    r = subprocess.run([sys.executable, "ex4_equivalence/diamond.py", "--random", "3", "--fixed"], cwd=ROOT,
                       capture_output=True, text=True)
    assert r.returncode == 1 and "curr_bal" in r.stdout
