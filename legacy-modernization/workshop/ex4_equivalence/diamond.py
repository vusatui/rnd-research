"""Exercise 4: behaviour-equivalence ("diamond") tests.

          same input bytes
          /              \\
  CBACT04C under GnuCOBOL   modern implementation
          \\              /
        byte-level compare (timestamps masked)

Usage:
  python ex4_equivalence/diamond.py                         # reference impl, legacy-compatible
  python ex4_equivalence/diamond.py --fixed                 # reference impl with the last-account bug fixed
  python ex4_equivalence/diamond.py --impl out/candidate_llm.py   # LLM-generated candidate from ex3
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common.paths import OUT  # noqa: E402
from common.records import ACCOUNT, TRAN, parse  # noqa: E402
from ex4_equivalence.adapter import mask, run_modern  # noqa: E402
from ex4_equivalence.scenarios import scenarios  # noqa: E402
from legacy.run_legacy import run_intcalc  # noqa: E402

PARM = "2022071800"


def load_impl(path: str | None):
    if not path:
        from ex3_new_service.interest import post_interest
        return post_interest
    spec = importlib.util.spec_from_file_location("candidate", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.post_interest


def field_diff(a: str, b: str, layout) -> list[str]:
    pa, pb = parse(a, layout), parse(b, layout)
    return [f"{k}: legacy={pa[k]!r} modern={pb[k]!r}" for k in pa if pa[k] != pb[k]]


def compare(legacy, modern: dict, strict: bool = False) -> list[str]:
    diffs = []
    if legacy.abend_code != modern["abend"]:
        diffs.append(f"abend code: legacy={legacy.abend_code} modern={modern['abend']}")
    if legacy.abend_code is not None or modern["abend"] is not None:
        return diffs  # abend: compare the abend code only (legacy leaves partial output; see notes)
    lt = [mask(t, strict) for t in legacy.transactions]
    mt = [mask(t, strict) for t in modern["transactions"]]
    if len(lt) != len(mt):
        diffs.append(f"transaction count: legacy={len(lt)} modern={len(mt)}")
    for i, (a, b) in enumerate(zip(lt, mt)):
        if a != b:
            diffs += [f"tx#{i + 1} {d}" for d in field_diff(a, b, TRAN)]
    la = sorted(legacy.accounts, key=lambda r: r[:11])
    ma = sorted(modern["accounts"], key=lambda r: r[:11])
    if len(la) != len(ma):
        diffs.append(f"account count: legacy={len(la)} modern={len(ma)}")
    for a, b in zip(la, ma):
        if a != b:
            diffs += [f"acct {a[:11]} {d}" for d in field_diff(a, b, ACCOUNT)]
    return diffs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--impl")
    ap.add_argument("--fixed", action="store_true", help="reference impl with legacy_compat=False")
    ap.add_argument("--random", type=int, default=20)
    ap.add_argument("--strict", action="store_true", help="byte-exact: do not normalise LOW-VALUES/FILLER")
    a = ap.parse_args()
    impl = load_impl(a.impl)
    kw = {"legacy_compat": False} if a.fixed else {}
    t0, results = time.time(), {}
    for name, inputs in scenarios(a.random).items():
        legacy = run_intcalc(**inputs, parm=PARM)
        try:
            modern = run_modern(impl, inputs, PARM, **kw)
            diffs = compare(legacy, modern, a.strict)
        except Exception as e:  # noqa: BLE001 - a crashing candidate is a finding, not a harness error
            diffs = [f"modern implementation crashed: {type(e).__name__}: {e}"]
        results[name] = diffs
        status = "EQUIVALENT" if not diffs else f"DIFF ({len(diffs)})"
        ab = f"abend {legacy.abend_code} (exit {legacy.return_code})" if legacy.abend_code else "ok"
        print(f"{name:30} legacy {ab:20} tx={len(legacy.transactions):<3} {status}")
        for d in diffs[:3]:
            print(f"    {d[:160]}")
    passed = sum(1 for d in results.values() if not d)
    print(f"\n{passed}/{len(results)} scenarios equivalent in {time.time() - t0:.1f}s")
    tag = pathlib.Path(a.impl).stem if a.impl else ("reference-fixed" if a.fixed else "reference")
    (OUT / f"diamond_{tag}.json").write_text(json.dumps(results, indent=1))
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
