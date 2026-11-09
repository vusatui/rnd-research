#!/usr/bin/env bash
# Smoke tests for both workshops, offline (MOCK mode): no key, no network needed.
# Runs inside the image: docker run --rm --network none system-one-workshops /app/bin/smoke.sh
set -euo pipefail
export EMULATOR_MOCK=1 DECIDER_MOCK=1
unset OPENROUTER_API_KEY || true
pass() { echo "PASS  $1"; }
fail() { echo "FAIL  $1"; echo "$2" | tail -20; exit 1; }

cd /app
python -m py_compile workshop/*.py workshop/ex*/*.py workshop-lite/*.py && pass "all Python files compile"

out=$(/app/bin/lite.sh 2>&1) || fail "workshop-lite demo (mock)" "$out"
for want in 'MOCK-EMULATOR' "send to 'technical'" 'CODE decides: BLOCK' 'CODE decides: APPROVE'; do
  grep -qF "$want" <<<"$out" || fail "workshop-lite output contains: $want" "$out"
done
pass "workshop-lite: 3 examples, labelled MOCK, expected decisions"

cd /app/workshop
out=$(python ex1_classic_baseline/baseline.py 2>&1) || fail "ex1 baseline" "$out"
grep -q 'department accuracy (LOO)' <<<"$out" && grep -q 'ECE' <<<"$out" || fail "ex1 output" "$out"
pass "ex1 classic baseline (no LLM): $(grep accuracy <<<"$out")"

out=$(python ex2_llm_as_decider/run.py --limit 5 --k 3 2>&1) || fail "ex2 (mock)" "$out"
grep -q 'BACKEND: MOCK' <<<"$out" && grep -q '^accuracy' <<<"$out" || fail "ex2 output" "$out"
pass "ex2 LLM-as-decider (MOCK backend) runs end to end"

for t in 0.3 0.6 0.9; do
  out=$(python ex3_cascade/cascade.py --no-llm --threshold $t 2>&1) || fail "ex3 --no-llm $t" "$out"
  grep -q "^threshold $t" <<<"$out" || fail "ex3 output $t" "$out"
done
pass "ex3 cascade --no-llm, thresholds 0.3/0.6/0.9"
out=$(python ex3_cascade/cascade.py --threshold 0.6 2>&1) || fail "ex3 with S2 (mock)" "$out"
grep -q 'S2 BACKEND: MOCK' <<<"$out" || fail "ex3 S2 mock label" "$out"
pass "ex3 cascade with MOCK System 2"

out=$(python ex4_decision_apis/compare.py 2>&1) || fail "ex4 without keys" "$out"
[ "$(grep -c '^\[skip\]' <<<"$out")" = 3 ] || fail "ex4 should skip all 3 providers without keys" "$out"
pass "ex4 skips every provider when no keys are set"

out=$(python decider.py 2>&1) || fail "decider.py demo (mock)" "$out"
grep -q '"_backend": "MOCK' <<<"$out" || fail "decider mock label" "$out"
pass "decider.py (MOCK) returns choice/noul/score"
echo "ALL SMOKE TESTS PASSED (MOCK mode: no LLM, no network)"
