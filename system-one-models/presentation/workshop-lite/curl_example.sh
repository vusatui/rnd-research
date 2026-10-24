#!/usr/bin/env bash
# The same request as example 1, with plain curl. Works against the emulator and real Jev.
set -euo pipefail
BASE="${JEV_BASE_URL:-http://127.0.0.1:8787}"
curl --silent --show-error --fail-with-body "$BASE/v1/systemone" \
  -H "Authorization: Bearer ${JEV_API_KEY:-anything}" \
  -H "Content-Type: application/json" \
  --data-binary @- <<'JSON'
{
  "model": "jev-latest",
  "state": "I was charged twice for my subscription this month. Please refund the extra charge.",
  "questions": {
    "billing": { "type": "noul", "instructions": "Is this message about billing?" },
    "tone": { "type": "choice", "instructions": "What is the tone of this message?",
              "criteria": { "angry": "An upset or hostile message",
                            "calm": "A neutral or polite message",
                            "excited": "An enthusiastic or eager message" } }
  }
}
JSON
echo
