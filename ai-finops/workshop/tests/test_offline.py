"""Offline tests: no network, no key. A scripted fake LLM stands in for OpenRouter."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import pipeline  # noqa: E402
from app.checks import score  # noqa: E402
from app.retrieval import sections, top_k  # noqa: E402
from common import llm, pricing  # noqa: E402

PRICES = {"large/model": {"in": 2.0, "out": 10.0, "cached": 0.1, "write": 2.5},
          "small/model": {"in": 0.1, "out": 0.5, "cached": 0.01, "write": None}}


@pytest.fixture(autouse=True)
def fake_world(monkeypatch, tmp_path):
    monkeypatch.setattr(pricing, "_P", PRICES)
    monkeypatch.setattr(llm, "LARGE", "large/model:free")
    monkeypatch.setattr(llm, "SMALL", "small/model:free")
    monkeypatch.setattr("common.ledger.LEDGER", tmp_path / "ledger.jsonl")


def fake_chat(replies):
    calls = []

    def chat(messages, model, max_tokens=1500, temperature=0.0, extra=None):
        calls.append(model)
        text = replies[model] if isinstance(replies, dict) else replies.pop(0)
        return text, llm.Usage(model, 1000, 200, 0, 50, 0, 0.1, "stop")
    return chat, calls


def test_kb_and_retrieval():
    assert len(sections()) == 10
    assert top_k("refund for my annual plan", 1) == ["billing"]
    assert "api" in top_k("API 429 rate limit", 3)


def test_cost_math():
    # 800 uncached * 2 + 200 cached * 0.1 + 50 out * 10 = 1600 + 20 + 500 = 2120 per 1M
    assert pricing.cost("large/model:free", 1000, 50, cached_tokens=200) == pytest.approx(2120 / 1e6)
    assert pricing.cost("large/model:free", 1000, 50, batch=True) == pytest.approx((2000 + 500) / 1e6 * 0.5)
    # no published cache-write price -> billed at the normal input rate
    assert pricing.cost("small/model:free", 1000, 0, cache_write_tokens=1000) == pytest.approx(100 / 1e6)


def test_checks():
    t = {"category": "billing|sales", "must": ["30%"], "must_not": ["guarantee"]}
    ok = json.dumps({"category": "sales", "reply": "Non-profits get 30% off.", "sources": ["plans"], "confidence": 0.9})
    assert score(t, ok)["pass"]
    assert not score(t, ok.replace("30%", "20%"))["pass"]
    assert not score(t, "not json")["json_ok"]
    bad = json.dumps({"category": "sales", "reply": "30% off, we guarantee it", "sources": [], "confidence": 1})
    assert not score(t, bad)["pass"]


def test_cascade_escalates_only_on_validator_failure(monkeypatch):
    t = pipeline.load_tickets(["T14"])[0]
    good = json.dumps({"category": "billing", "reply": "Registered charities get 30% off Team and Business.",
                       "sources": ["plans"], "confidence": 0.9})
    low = json.loads(good) | {"confidence": 0.4}
    chat, calls = fake_chat({"small/model:free": good, "large/model:free": good})
    monkeypatch.setattr(llm, "chat", chat)
    r = pipeline.answer(t, "H_cascade", "test")
    assert not r["escalated"] and calls == ["small/model:free"] and r["score"]["pass"]

    chat, calls = fake_chat({"small/model:free": json.dumps(low), "large/model:free": good})
    monkeypatch.setattr(llm, "chat", chat)
    r = pipeline.answer(t, "H_cascade", "test")
    assert r["escalated"] and r["why"] == "low confidence" and calls == ["small/model:free", "large/model:free"]
    assert r["calls"] == 2 and r["usd_twin"] > 0


def test_stable_prefix_is_byte_identical():
    t1, t2 = pipeline.load_tickets(["T01", "T02"])
    s = pipeline.CONFIGS["C_stable"]
    d = pipeline.CONFIGS["B_concise"]
    assert pipeline.build_messages(t1, s)[0] == pipeline.build_messages(t2, s)[0]
    assert pipeline.build_messages(t1, d)[0] != pipeline.build_messages(t2, d)[0]


def test_offline_scripts_run():
    for args in (["ex5_breakeven/breakeven.py"], ["ex3_semantic_cache/semantic_cache.py", "--lexical"]):
        out = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True, timeout=60)
        assert out.returncode == 0, out.stderr
    assert "break-even utilization" in subprocess.run([sys.executable, "ex5_breakeven/breakeven.py"], cwd=ROOT,
                                                      capture_output=True, text=True).stdout


def test_grounded_numbers():
    t = {"text": "We have 120 people and need SSO."}
    assert pipeline.ungrounded_numbers("Enterprise starts at $5,000 per year, minimum 50 seats.", t["text"]) == {"$5000"}
    assert pipeline.ungrounded_numbers("Minimum 50 seats; for 120 people choose Enterprise.", t["text"]) == set()
    assert pipeline.ungrounded_numbers("Non-profits get 30 % off.", "") == set()
