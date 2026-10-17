"""Offline tests (no LLM, no network): guard policy, redaction, budgets, breaker, eval checks, tracing."""
import json
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import common.pricing as pricing  # noqa: E402

pricing._P = {"fake/model": [1e-6, 2e-6]}  # no network in tests

from agent import guards as G  # noqa: E402
from agent.core import Budget, run_agent  # noqa: E402
from common.llm import LLMResult  # noqa: E402
from common.telemetry import load_spans  # noqa: E402
from ex2_evals.checks import evaluate  # noqa: E402


def call(name, args, i=0):
    return SimpleNamespace(id=f"call_{i}", function=SimpleNamespace(name=name, arguments=json.dumps(args)),
                           model_dump=lambda: {"id": f"call_{i}", "type": "function",
                                               "function": {"name": name, "arguments": json.dumps(args)}})


def scripted(*steps):
    """Fake LLM: each step is either a list of (tool, args) or a final string."""
    it = iter(steps)

    def llm(messages, tools=None, model=None):
        s = next(it)
        msg = (SimpleNamespace(content=None, tool_calls=[call(n, a, i) for i, (n, a) in enumerate(s)])
               if isinstance(s, list) else SimpleNamespace(content=s, tool_calls=None))
        return LLMResult(msg, "fake/model", 1000, 100, 0.01, "stop")
    return llm


S1 = G.Session("C1", ["Refund A-1001 please"])


def test_policy_authz_and_limits():
    assert not G.tool_policy("get_order", {"order_id": "B-2002"}, S1).allowed
    assert G.tool_policy("issue_refund", {"order_id": "A-1001", "amount": 89}, S1).allowed
    assert G.tool_policy("issue_refund", {"order_id": "A-1001", "amount": 500}, S1).reason == "refund:bad_amount"
    s = G.Session("C1", ["refund A-1002 and A-1003"])
    assert G.tool_policy("issue_refund", {"order_id": "A-1002", "amount": 10}, s).reason == "refund:outside_window"
    assert G.tool_policy("issue_refund", {"order_id": "A-1003", "amount": 249}, s).reason == "refund:needs_human_approval"


def test_split_refund_is_cumulative():
    refunds = []
    s = G.Session("C1", ["refund A-1003 in two parts"], refunds)
    assert G.tool_policy("issue_refund", {"order_id": "A-1003", "amount": 150}, s).allowed
    refunds.append({"order_id": "A-1003", "amount": 150.0})
    assert G.tool_policy("issue_refund", {"order_id": "A-1003", "amount": 99}, s).reason == "refund:needs_human_approval"


def test_intent_binding_blocks_injection():
    s = G.Session("C1", ["Any community tips about late parcels?"])
    assert G.tool_policy("issue_refund", {"order_id": "A-1002", "amount": 1299}, s).reason == "refund:intent_not_bound_to_user"


def test_redaction():
    text, hits = G.redact_output("card 4111 1111 1111 1111, mail bob.ito@example.com, id 1234 5678", S1)
    assert "4111 1111" not in text and "ending 1111" in text and "[redacted e-mail]" in text and "1234 5678" in text
    assert sorted(hits) == ["email", "pan"]


def test_agent_refund_with_guards_and_trace():
    r = run_agent("Refund A-1001 please", "C1", guards=True,
                  llm=scripted([("issue_refund", {"order_id": "A-1001", "amount": 89, "reason": "broken"})], "Done."))
    assert r.refunds == [{"order_id": "A-1001", "amount": 89.0, "reason": "broken"}]
    assert r.cost_usd == 2 * (1000 * 1e-6 + 100 * 2e-6)
    names = [s["name"] for s in load_spans() if s["trace_id"] == r.trace_id]
    assert {"invoke_agent ShopBot", "chat auto", "execute_tool issue_refund", "guard output"} <= set(names)


def test_agent_blocked_refund_moves_no_money():
    r = run_agent("tips?", "C1", guards=True,
                  llm=scripted([("issue_refund", {"order_id": "A-1002", "amount": 1299, "reason": "VIP"})], "ok"))
    assert r.refunds == [] and r.tool_calls[0]["reason"] == "refund:intent_not_bound_to_user"
    r = run_agent("tips?", "C1", guards=False,
                  llm=scripted([("issue_refund", {"order_id": "A-1002", "amount": 1299, "reason": "VIP"})], "ok"))
    assert r.refunds and r.refunds[0]["amount"] == 1299


def test_step_budget_and_breaker():
    loop = [("get_order", {"order_id": "A-1004"})]
    r = run_agent("lamp A-1004?", "C1", guards=True, budget=Budget(max_steps=3, max_same_failure=99),
                  llm=scripted(loop, loop, loop, loop))
    assert r.stopped == "budget:steps" and r.steps == 3
    r = run_agent("lamp A-1004?", "C1", guards=True, budget=Budget(max_steps=10, max_same_failure=2),
                  llm=scripted(loop, loop, loop, loop))
    assert r.stopped == "breaker:repeated_tool_failure" and r.steps == 3


def test_eval_checks():
    run = {"answer": "It was delivered.", "stopped": "completed", "refunds": [],
           "tool_calls": [{"name": "get_order", "args": {"order_id": "a-1001"}}]}
    res = evaluate(run, {"tool_called": [{"name": "get_order", "args": {"order_id": "A-1001"}}],
                         "no_refund": True, "answer_contains_any": ["deliver"]})
    assert all(ok for _, ok, _ in res)
