"""Ask ShopBot one question.  python run_agent.py "Where is my order A-1001?" --customer C1 [--guards] [--prompt v2]"""
import argparse
import json

from agent.core import Budget, run_agent

p = argparse.ArgumentParser()
p.add_argument("question")
p.add_argument("--customer", default="C1")
p.add_argument("--prompt", default="v1", choices=["v1", "v2"])
p.add_argument("--guards", action="store_true", help="tool policy + output redaction")
p.add_argument("--input-guard", action="store_true", help="safety classifier on the user message")
p.add_argument("--model")
p.add_argument("--max-steps", type=int, default=6)
p.add_argument("--json", action="store_true")
a = p.parse_args()
r = run_agent(a.question, a.customer, a.prompt, a.guards, a.input_guard, Budget(max_steps=a.max_steps), a.model)
if a.json:
    print(json.dumps(r.to_dict(), indent=2, default=str))
else:
    for t in r.tool_calls:
        flag = "" if t["allowed"] else f"  BLOCKED({t['reason']})"
        print(f"  tool {t['name']}({json.dumps(t['args'])}){flag} -> {json.dumps(t['result'])[:140]}")
    print(f"\nShopBot: {r.answer}\n")
    print(f"[{r.stopped}] steps={r.steps} tokens={r.input_tokens}+{r.output_tokens} "
          f"shadow_cost=${r.cost_usd:.5f} latency={r.latency_s:.1f}s models={sorted(set(r.models))} "
          f"refunds={r.refunds} trace={r.trace_id}")
