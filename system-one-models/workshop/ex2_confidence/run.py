#!/usr/bin/env python3
"""Exercise 2 - verbalized confidence vs a computed distribution, on the same 150 test tickets.

  python ex2_confidence/run.py --method jev                      # E: decision model, 1 request
  python ex2_confidence/run.py --method verbal --model openai/gpt-4o-mini
  python ex2_confidence/run.py --method all                     # every method in the plan below
  python ex2_confidence/run.py --estimate                       # $ estimate, no calls
Results go to results/ex2_<method>_<model>.jsonl, then:  python eval.py --reliability
MOCK=1 / no key: nothing is called, the committed results are scored again (that is what CI does).
"""
import argparse, json, sys, pathlib, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import load_tickets, RESULTS, mock_mode
import llm, methods

CHEAP = "deepseek/deepseek-v4.1-flash-1017"   # one cheap model for A, B and C: same model, three ways to get confidence
PLAN = [("verbal", CHEAP), ("logprobs", CHEAP), ("votes", CHEAP), ("verbal", "anthropic/claude-haiku-5.5"),
        ("classic", None), ("jev", "jev-latest")]
STRONG = [("verbal", "openai/gpt-6-sol"), ("verbal", "anthropic/claude-sonnet-5.5")]  # opt-in: --method strong (~$0.5)
# rough $/ticket from OpenRouter prices (in, out tokens per ticket)
EST = {"anthropic/claude-sonnet-5.5": (2.0, 10.0), "deepseek/deepseek-v4.1-flash-1017": (0.02, 0.108), "openai/gpt-4o-mini": (0.15, 0.6), "openai/gpt-6-sol": (2.0, 10.0), "anthropic/claude-haiku-5.5": (0.1, 0.5), "jev-latest": (0.042, 0)}
TOK = {"verbal": (800, 40), "logprobs": (620, 2), "votes": (5 * 310, 5 * 15), "jev": (420, 0), "classic": (0, 0)}


def out_path(method, model):
    return RESULTS / f"ex2_{method}{'_' + model.split('/')[-1] if model and method != 'jev' else ''}.jsonl"


def estimate(plan, n):
    total = 0
    for m, model in plan:
        if m == "classic":
            continue
        pi, po = EST[model]; ti, to = TOK[m]
        c = n * (ti * pi + to * po) / 1e6
        total += c
        print(f"  {m:9} {model:28} ~${c:.3f}")
    print(f"  total for {n} tickets ~${total:.3f}")
    return total


def run(method, model, tickets, train, workers):
    fn = {"verbal": lambda t: methods.verbal(t, model), "logprobs": lambda t: methods.logprobs(t, model),
          "votes": lambda t: methods.votes(t, model), "jev": lambda t: methods.jev(t, model)}.get(method)
    if method == "classic":
        clfs = methods.classic_fit(train)
        fn, workers = (lambda t: methods.classic(t, clfs)), 1
    # every answer is saved to disk the moment it arrives; a re-run reuses it instead of paying again
    cache = RESULTS / "raw" / out_path(method, model).stem
    cache.mkdir(parents=True, exist_ok=True)

    def cached(t):
        f = cache / f"{t['id']}.json"
        if f.exists():
            return json.load(open(f))
        r = fn(t)
        if method != "classic":
            json.dump(r, open(f, "w"))
        return r
    t0 = time.perf_counter()
    with ThreadPoolExecutor(workers) as ex:
        rows = list(ex.map(cached, tickets))
    p = out_path(method, model)
    with open(p, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print(f"{method:9} {model or '':28} {len(rows)} tickets in {time.perf_counter()-t0:5.1f}s  "
          f"${sum(r['cost'] for r in rows):.4f}  -> {p.relative_to(RESULTS.parent)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", default="all", choices=["all", "strong", "verbal", "logprobs", "votes", "classic", "jev"])
    ap.add_argument("--model")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--estimate", action="store_true")
    a = ap.parse_args()
    RESULTS.mkdir(exist_ok=True)
    test, train = load_tickets("test"), load_tickets("train")
    if a.limit:
        test = test[:a.limit]
    plan = PLAN if a.method == "all" else STRONG if a.method == "strong" else [(a.method, a.model or dict(PLAN).get(a.method))]
    print(f"Exercise 2: {len(test)} test tickets, {len(plan)} method(s)")
    est = estimate(plan, len(test))
    if a.estimate:
        return
    if mock_mode():
        print("\nMOCK=1: no model is called. Re-scoring the committed results in results/ (recorded on a real run).")
    else:
        for m, model in plan:
            run(m, model, test, train, a.workers)
        print(f"spent this run: ${llm.LEDGER.cost:.4f} (estimate was ${est:.3f})")
    import eval as ev
    ev.report(sorted(str(p) for p in RESULTS.glob("ex2_*.jsonl")), show_reliability=False)


if __name__ == "__main__":
    main()
