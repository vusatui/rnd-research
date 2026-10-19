"""Self-hosting vs API break-even (offline arithmetic, no LLM calls).

The question clients ask: "at what volume is running an open-weights model on our own GPUs cheaper than paying
per token?" The answer is dominated by UTILIZATION: you pay for GPU-hours whether or not tokens flow.

Inputs (override on the command line). Every default is labelled with where it comes from:
  --gpu-hour    3.50   USD per GPU-hour, H100 on-demand, specialist clouds. SECONDARY SOURCE: GPU price indexes,
                       Oct 2026 (e.g. https://gpueconomy.com/price-index ~ $3.5; hyperscaler list ~ $10). Check yours.
  --gpus        8      GPUs per serving replica (a large MoE model typically needs a full 8-GPU node)
  --tps         5000   ASSUMPTION: aggregate generated tokens/s per replica at good batching. Not measured here;
                       benchmark your model + engine (e.g. vLLM's benchmark tooling) before using this.
  --ops-month   15000  ASSUMPTION: monthly people cost to run it (on-call, upgrades, evals), USD
  --in-out      10     input tokens per output token in the workload (our ticket task: ~40:1; chat ~3-10:1)
  --prefill-x   10     ASSUMPTION: prefill is ~10x cheaper per token than decode on the same GPUs
API prices (USD per 1M tokens, input/output), read 2026-10-19:
  open-weights model via OpenRouter: nvidia/nemotron-3-ultra-550b-a55b 0.60/2.40 (https://openrouter.ai/api/v1/models)
  frontier API: gpt-6.1-sol 2.00/10.00 (https://platform.openai.com/docs/pricing)

    python ex5_breakeven/breakeven.py
    python ex5_breakeven/breakeven.py --gpu-hour 10 --tps 2500
"""
from __future__ import annotations

import argparse

HOURS_MONTH = 730


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gpu-hour", type=float, default=3.50)
    ap.add_argument("--gpus", type=int, default=8)
    ap.add_argument("--tps", type=float, default=5000)
    ap.add_argument("--ops-month", type=float, default=15000)
    ap.add_argument("--in-out", type=float, default=10)
    ap.add_argument("--prefill-x", type=float, default=10)
    a = ap.parse_args()

    apis = {"open-weights via API (0.60/2.40)": (0.60, 2.40), "frontier API (2.00/10.00)": (2.00, 10.00)}
    gpu_month = a.gpu_hour * a.gpus * HOURS_MONTH
    fixed = gpu_month + a.ops_month
    # capacity in "output-token equivalents": each output token also brings in_out input tokens of prefill work
    eq_per_output = 1 + a.in_out / a.prefill_x
    out_capacity = a.tps / eq_per_output * 3600 * HOURS_MONTH   # output tokens/month at 100% utilization
    print(f"Replica: {a.gpus} GPUs x ${a.gpu_hour}/h = ${gpu_month:,.0f}/month always-on, + ops ${a.ops_month:,.0f} "
          f"= ${fixed:,.0f}/month fixed")
    print(f"Capacity at 100% utilization: {out_capacity/1e9:.2f}B output tokens/month "
          f"(+{a.in_out:g}x input tokens each)\n")
    print("| API | API $ per 1M output tok (incl. its input) | self-host break-even volume | "
          "break-even utilization |\n|---|---|---|---|")
    for name, (pin, pout) in apis.items():
        per_out = pout + a.in_out * pin                     # USD per 1M output tokens incl. input tokens
        be_tokens = fixed / per_out * 1e6                  # output tokens/month where costs are equal
        util = be_tokens / out_capacity
        verdict = f"{util:.0%}" + (" (impossible: >100%)" if util > 1 else "")
        print(f"| {name} | ${per_out:.2f} | {be_tokens/1e9:.2f}B out tok/month | {verdict} |")
    print("\nSelf-hosted $ per 1M output tokens (incl. input) by utilization:")
    print("| utilization | " + " | ".join(f"{u:.0%}" for u in (0.05, 0.10, 0.25, 0.50, 0.75, 1.0)) + " |")
    print("|---|" + "---|" * 6)
    cells = []
    for u in (0.05, 0.10, 0.25, 0.50, 0.75, 1.0):
        cells.append(f"${fixed / (out_capacity * u) * 1e6:.2f}")
    print("| self-host | " + " | ".join(cells) + " |")
    print("\nRead it as: below the break-even utilization the API is cheaper. Arithmetic check: traffic only in "
          "business hours (50 of 168 h/week) caps an always-on replica at ~30% average utilization even if it is "
          "saturated during those hours. The frontier row compares different models (quality differs) - it answers "
          "'what if a self-hosted open model is good enough for this task', which your evals must confirm.")


if __name__ == "__main__":
    main()
