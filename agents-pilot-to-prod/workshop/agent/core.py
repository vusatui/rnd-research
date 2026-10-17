"""ShopBot: a deliberately small tool-calling agent loop with tracing, guardrails and budgets.

    run_agent("Refund A-1001 please", customer_id="C1", prompt="v1", guards=True, budget=Budget())

Every run is one trace:  invoke_agent ShopBot
                           ├─ guard input            (optional)
                           ├─ chat <model>           (one per LLM step; tokens, latency, shadow cost)
                           ├─ execute_tool <name>    (args/result, policy decision)
                           └─ guard output
"""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field

from opentelemetry.trace import Status, StatusCode

from common import telemetry
from common.llm import chat as default_chat
from common.pricing import shadow_cost

from . import guards as G
from . import tools as T
from .data import CUSTOMERS, TODAY
from .prompts import PROMPTS

AGENT_NAME = "ShopBot"
AGENT_VERSION = "1.0.0"


@dataclass
class Budget:
    max_steps: int = 6            # LLM calls per run
    max_tokens: int = 30_000      # input + output tokens per run
    max_seconds: float = 90.0     # wall clock per run
    max_cost_usd: float = 0.01    # shadow cost per run (paid-twin list price)
    max_same_failure: int = 2     # circuit breaker: identical failing tool call


@dataclass
class RunResult:
    run_id: str
    trace_id: str
    customer_id: str
    question: str
    prompt: str
    guards: bool
    answer: str = ""
    stopped: str = "completed"             # completed | budget:* | breaker:* | input_guard | error
    steps: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    latency_s: float = 0.0
    models: list = field(default_factory=list)
    tool_calls: list = field(default_factory=list)   # {name,args,result,allowed,reason,error}
    refunds: list = field(default_factory=list)      # money that actually moved
    guard_events: list = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


def _exec_tool(name: str, args: dict, ledger: list):
    if name == "search_kb":
        return T.search_kb(str(args.get("query", "")))
    if name == "get_order":
        return T.get_order(str(args.get("order_id", "")))
    if name == "issue_refund":
        return T.issue_refund(str(args.get("order_id", "")).upper(), args.get("amount", 0), str(args.get("reason", "")), ledger)
    if name == "escalate_to_human":
        return T.escalate_to_human(str(args.get("reason", "")), args.get("order_id"))
    return {"error": f"unknown tool {name}"}


def run_agent(question: str, customer_id: str = "C1", prompt: str = "v1", guards: bool = False,
              input_guard: bool = False, budget: Budget | None = None, model: str | None = None,
              llm=default_chat, tags: dict | None = None) -> RunResult:
    budget = budget or Budget()
    tracer = telemetry.setup()
    cust = CUSTOMERS[customer_id]
    session = G.Session(customer_id, [question])
    res = RunResult(uuid.uuid4().hex[:12], "", customer_id, question, prompt, guards)
    t0 = time.time()
    system = PROMPTS[prompt].format(customer_id=customer_id, customer_name=cust["name"], today=TODAY.isoformat())
    messages = [{"role": "system", "content": system}, {"role": "user", "content": question}]
    failures: dict[str, int] = {}

    with tracer.start_as_current_span(f"invoke_agent {AGENT_NAME}") as root:
        res.trace_id = f"{root.get_span_context().trace_id:032x}"
        telemetry.set_attrs(root, {
            "gen_ai.operation.name": "invoke_agent", "gen_ai.provider.name": "openrouter",
            "gen_ai.agent.name": AGENT_NAME, "gen_ai.agent.version": AGENT_VERSION,
            "gen_ai.conversation.id": res.run_id, "openinference.span.kind": "AGENT",
            "input.value": telemetry.content(question), "session.id": res.run_id, "user.id": customer_id,
            "app.prompt.version": prompt, "app.guards.enabled": guards,
            **{f"app.tag.{k}": str(v) for k, v in (tags or {}).items()}})

        if input_guard:
            with tracer.start_as_current_span("guard input") as gs:
                safe, verdict, lat = G.input_guard(question)
                telemetry.set_attrs(gs, {"openinference.span.kind": "GUARDRAIL", "app.guard.verdict": verdict,
                                         "app.guard.safe": safe})
            if not safe:
                res.guard_events.append({"guard": "input", "verdict": verdict})
                res.stopped = "input_guard"
                res.answer = "Sorry, I can't help with that request. I can connect you with a human agent."

        while res.stopped == "completed" and not res.answer:
            # ---- budgets are checked *before* spending more ----
            if res.steps >= budget.max_steps:
                res.stopped = "budget:steps"
            elif res.input_tokens + res.output_tokens >= budget.max_tokens:
                res.stopped = "budget:tokens"
            elif time.time() - t0 >= budget.max_seconds:
                res.stopped = "budget:time"
            elif res.cost_usd >= budget.max_cost_usd:
                res.stopped = "budget:cost"
            if res.stopped != "completed":
                root.add_event("budget_exceeded", {"app.budget.reason": res.stopped})
                res.answer = "I'm sorry, this is taking longer than expected. I've passed your request to a human agent."
                break

            req_model = model or "auto"
            with tracer.start_as_current_span(f"chat {req_model}") as span:
                try:
                    r = llm(messages, tools=T.TOOL_SPECS, model=model)
                except Exception as e:  # noqa: BLE001
                    span.set_status(Status(StatusCode.ERROR, str(e)[:200]))
                    res.stopped, res.answer = "error", "Sorry, something went wrong. A human agent will follow up."
                    break
                res.steps += 1
                cost = shadow_cost(r.model, r.input_tokens, r.output_tokens)
                res.input_tokens += r.input_tokens
                res.output_tokens += r.output_tokens
                res.cost_usd += cost
                res.models.append(r.model)
                calls = r.message.tool_calls or []
                telemetry.set_attrs(span, {
                    "gen_ai.operation.name": "chat", "gen_ai.provider.name": "openrouter",
                    "gen_ai.request.model": req_model, "gen_ai.response.model": r.model,
                    "gen_ai.response.id": r.response_id,
                    "gen_ai.response.finish_reasons": [r.finish_reason or "unknown"],
                    "gen_ai.usage.input_tokens": r.input_tokens, "gen_ai.usage.output_tokens": r.output_tokens,
                    "gen_ai.request.temperature": 0.0,
                    # OpenInference twins for the Phoenix UI
                    "openinference.span.kind": "LLM", "llm.model_name": r.model,
                    "llm.token_count.prompt": r.input_tokens, "llm.token_count.completion": r.output_tokens,
                    "llm.token_count.total": r.input_tokens + r.output_tokens,
                    "input.value": telemetry.content(messages[-1]),
                    "output.value": telemetry.content(r.message.content or [c.function.name for c in calls]),
                    # no cost attribute in the GenAI semconv (yet) -> app namespace
                    "app.cost.shadow_usd": round(cost, 8), "app.llm.failed_attempts": len(r.attempts),
                })
            messages.append({"role": "assistant", "content": r.message.content or "",
                             **({"tool_calls": [c.model_dump() for c in calls]} if calls else {})})
            if not calls:
                res.answer = (r.message.content or "").strip()
                break

            for c in calls:
                name = c.function.name
                try:
                    args = json.loads(c.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}
                rec = {"name": name, "args": args, "allowed": True, "reason": "", "error": None}
                with tracer.start_as_current_span(f"execute_tool {name}") as ts:
                    decision = G.tool_policy(name, args, session) if guards else G.Decision(True)
                    if not decision.allowed:
                        result = decision.replacement
                        rec.update(allowed=False, reason=decision.reason)
                        res.guard_events.append({"guard": "tool_policy", "tool": name, "reason": decision.reason})
                        ts.add_event("guardrail_blocked", {"app.guard.reason": decision.reason})
                        if decision.reason == "refund:needs_human_approval":
                            T.escalate_to_human("refund above threshold", args.get("order_id"))
                    else:
                        try:
                            result = _exec_tool(name, args, res.refunds)
                        except Exception as e:  # noqa: BLE001
                            result = {"error": str(e)}
                            rec["error"] = str(e)
                            ts.set_status(Status(StatusCode.ERROR, str(e)[:200]))
                    key = f"{name}:{json.dumps(args, sort_keys=True)}"
                    if isinstance(result, dict) and result.get("error"):
                        failures[key] = failures.get(key, 0) + 1
                    rec["result"] = result
                    telemetry.set_attrs(ts, {
                        "gen_ai.operation.name": "execute_tool", "gen_ai.tool.name": name,
                        "gen_ai.tool.type": "function", "gen_ai.tool.call.id": c.id,
                        "gen_ai.tool.call.arguments": telemetry.content(args),
                        "gen_ai.tool.call.result": telemetry.content(result),
                        "openinference.span.kind": "TOOL", "tool.name": name,
                        "input.value": telemetry.content(args), "output.value": telemetry.content(result),
                        "app.guard.allowed": rec["allowed"], "app.guard.reason": rec["reason"] or None})
                res.tool_calls.append(rec)
                messages.append({"role": "tool", "tool_call_id": c.id, "content": json.dumps(result)})
            if any(v > budget.max_same_failure for v in failures.values()):
                res.stopped = "breaker:repeated_tool_failure"
                root.add_event("circuit_breaker", {"app.breaker.key": max(failures, key=failures.get)})
                res.answer = "Our order system is having trouble right now. I've created a ticket for a human agent."

        if guards:
            with tracer.start_as_current_span("guard output") as gs:
                res.answer, hits = G.redact_output(res.answer, session)
                telemetry.set_attrs(gs, {"openinference.span.kind": "GUARDRAIL", "app.guard.redactions": len(hits)})
                if hits:
                    res.guard_events.append({"guard": "output", "redacted": hits})
        res.latency_s = round(time.time() - t0, 3)
        telemetry.set_attrs(root, {
            "output.value": telemetry.content(res.answer), "app.stopped": res.stopped, "app.steps": res.steps,
            "gen_ai.usage.input_tokens": res.input_tokens, "gen_ai.usage.output_tokens": res.output_tokens,
            "app.cost.shadow_usd": round(res.cost_usd, 8), "app.refunds.count": len(res.refunds),
            "app.refunds.usd": sum(x["amount"] for x in res.refunds)})
        if res.stopped not in ("completed", "input_guard"):
            root.set_status(Status(StatusCode.ERROR, res.stopped))
    telemetry.flush()
    return res
