#!/usr/bin/env bash
# Smoke tests for both workshops, offline (MOCK mode): no key, no network needed.
# Runs inside the image: docker run --rm --network none system-one-workshops /app/bin/smoke.sh
set -euo pipefail
export EMULATOR_MOCK=1 WORKSHOP_MOCK=1
unset OPENROUTER_API_KEY || true
pass() { echo "PASS  $1"; }
fail() { echo "FAIL  $1"; echo "$2" | tail -20; exit 1; }

cd /app
python -m py_compile workshop/*.py workshop/ex*/*.py workshop/data/*.py workshop/homework/*.py workshop-lite/*.py || fail "a Python file does not compile" ""
pass "all Python files compile"

out=$(/app/bin/lite.sh 2>&1) || fail "workshop-lite demo (mock)" "$out"
for want in 'MOCK-EMULATOR' "send to 'technical'" 'model said block' 'CODE decides: APPROVE'; do
  grep -qF "$want" <<<"$out" || fail "workshop-lite output contains: $want" "$out"
done
pass "workshop-lite: 3 examples, labelled MOCK, expected decisions"

cd /app/workshop
out=$(python ex2_confidence/run.py 2>&1) || fail "ex2 (MOCK: re-score committed results)" "$out"
grep -q 'MOCK=1: no model is called' <<<"$out" && grep -q 'E jev' <<<"$out" && grep -q 'A verbal' <<<"$out" || fail "ex2 output" "$out"
pass "ex2 re-scores the committed results of all methods offline"

out=$(python eval.py --reliability 2>&1) || fail "eval.py" "$out"
grep -q 'Reliability - ' <<<"$out" && grep -q 'auto@95' <<<"$out" || fail "eval output" "$out"
pass "eval.py: accuracy, ECE, reliability tables, auto@95, cost"

out=$(python ex3_fast_first/economics.py 2>&1) || fail "ex3 economics" "$out"
grep -q 'cheapest' <<<"$out" || fail "ex3 output" "$out"
out=$(python ex3_fast_first/economics.py --error-cost 20 --review 1 2>&1) || fail "ex3 economics params" "$out"
pass "ex3 fast-first economics sweep (two cost settings)"

out=$(python homework/compare_apis.py 2>&1) || fail "homework without keys" "$out"
[ "$(grep -c '^\[skip\]' <<<"$out")" = 3 ] || fail "homework should skip all 3 providers without keys" "$out"
pass "homework skips every provider when no keys are set"
echo "ALL SMOKE TESTS PASSED (MOCK mode: no LLM, no network)"
