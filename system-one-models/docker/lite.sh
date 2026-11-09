#!/usr/bin/env bash
# Runs the workshop-lite demo inside the container: start the Jev emulator, wait until it is up,
# run the client examples (all three, or the ones passed as arguments).
#   lite.sh                  -> ticket comment approval
#   lite.sh ticket           -> one example
# (The plain-curl example runs from a curl container: `make emulator` + `make curl`.)
# Env: EMULATOR_MOCK=1 (offline rules), EMULATOR_FALLBACK=mock (LLM, mock on failure),
#      JEV_BASE_URL (if it points elsewhere, e.g. real Jev, no emulator is started).
set -euo pipefail
cd /app/workshop-lite

PORT="${EMULATOR_PORT:-8787}"
export JEV_BASE_URL="${JEV_BASE_URL:-http://127.0.0.1:${PORT}}"
LOCAL=0
case "$JEV_BASE_URL" in http://127.0.0.1:*|http://localhost:*) LOCAL=1 ;; esac

if [ "$LOCAL" = 1 ]; then
  if [ "${EMULATOR_MOCK:-}" != "1" ] && [ -z "${OPENROUTER_API_KEY:-}" ]; then
    echo "!! OPENROUTER_API_KEY is not set: switching to MOCK mode (offline keyword rules, NOT an LLM, NOT Jev)." >&2
    echo "!! Put a free key in system-one-models/.env to use the LLM emulator." >&2
    export EMULATOR_MOCK=1
  fi
  EMULATOR_HOST=127.0.0.1 python jev_emulator.py &
  EMU_PID=$!
  trap 'kill $EMU_PID 2>/dev/null || true' EXIT
  python - "$PORT" <<'PY' || { echo "emulator did not start" >&2; exit 1; }
import sys, time, urllib.request
for _ in range(50):
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{sys.argv[1]}/health", timeout=1); sys.exit(0)
    except Exception:
        time.sleep(0.2)
sys.exit(1)
PY
fi

python jev_client.py "$@"
