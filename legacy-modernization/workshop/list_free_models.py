"""List current OpenRouter ':free' models. The free list changes often; pick one and set OPENROUTER_MODEL."""
import json
import urllib.request

data = json.load(urllib.request.urlopen("https://openrouter.ai/api/v1/models"))["data"]
for m in sorted(data, key=lambda m: m["id"]):
    if m["id"].endswith(":free"):
        print(f"{m['id']:60} ctx={m.get('context_length')}")
