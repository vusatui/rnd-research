#!/usr/bin/env bash
# One real round trip through the LLM emulator (free OpenRouter model). Needs OPENROUTER_API_KEY.
# Fails if the answer came from the mock fallback, so it really tests the free model.
set -euo pipefail
[ -n "${OPENROUTER_API_KEY:-}" ] || { echo "SKIP: OPENROUTER_API_KEY not set"; exit 0; }
unset EMULATOR_MOCK EMULATOR_FALLBACK || true
out=$(/app/bin/lite.sh ticket 2>&1) || { echo "$out"; echo "FAIL: live emulator call"; exit 1; }
echo "$out"
grep -q 'model=EMULATOR(' <<<"$out" && ! grep -q 'MOCK' <<<"$out" || { echo "FAIL: not a real LLM answer"; exit 1; }
echo "LIVE CHECK PASSED (free LLM via OpenRouter, emulator - NOT Jev)"
