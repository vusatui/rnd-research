"""List current OpenRouter ':free' models. Marks which ones advertise logprobs and structured outputs.
The free list changes often, so run this before the workshop."""
import json, urllib.request
data = json.load(urllib.request.urlopen("https://openrouter.ai/api/v1/models"))["data"]
for m in sorted(data, key=lambda m: m["id"]):
    if m["id"].endswith(":free"):
        p = set(m.get("supported_parameters", []))
        flags = [f for f in ("logprobs", "structured_outputs", "response_format") if f in p]
        print(f'{m["id"]:60} ctx={m.get("context_length")} {",".join(flags)}')
