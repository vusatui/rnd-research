"""How many free-model requests are left today on your OpenRouter key (GET /api/v1/key -> free_model_daily_requests).
The daily counter resets at 00:00 UTC. The per-minute limit (20 rpm) is not reported here.

    python check_quota.py
"""
import json
import os
import urllib.request

from dotenv import load_dotenv

from common.paths import WORKSHOP

load_dotenv(WORKSHOP / ".env")
key = os.environ.get("OPENROUTER_API_KEY")
if not key:
    raise SystemExit("Set OPENROUTER_API_KEY (free key: https://openrouter.ai/keys) in env or workshop/.env")
req = urllib.request.Request("https://openrouter.ai/api/v1/key", headers={"Authorization": f"Bearer {key}"})
d = json.load(urllib.request.urlopen(req, timeout=20))["data"]
q = d.get("free_model_daily_requests") or {}
print(f"free-model requests today (UTC day): used {q.get('used', '?')} / limit {q.get('limit', '?')} "
      f"-> remaining {q.get('remaining', '?')}")
print("the full workshop needs ~500 requests; with a 50/day limit use --repeats 1 and --only (see PARTICIPANTS.md)")
