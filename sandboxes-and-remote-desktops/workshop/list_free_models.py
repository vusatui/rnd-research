"""List current OpenRouter ':free' models with tool calling (and vision). The free list changes often."""
import json, urllib.request
data = json.load(urllib.request.urlopen("https://openrouter.ai/api/v1/models"))["data"]
for m in sorted(data, key=lambda m: m["id"]):
    if m["id"].endswith(":free") and "tools" in m.get("supported_parameters", []):
        vision = "image" in m["architecture"].get("input_modalities", [])
        print(f'{m["id"]:55} ctx={m.get("context_length")} {"vision+tools" if vision else "tools"}')
