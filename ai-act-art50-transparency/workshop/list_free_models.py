"""List current OpenRouter ':free' models. The free list changes often; if the default vanished, pick another one
and set CHAT_MODEL in .env."""
import json
import urllib.request

data = json.load(urllib.request.urlopen("https://openrouter.ai/api/v1/models"))["data"]
for m in sorted(data, key=lambda m: m["id"]):
    if m["id"].endswith(":free"):
        print(f"{m['id']:60} ctx={m.get('context_length'):>8}")
