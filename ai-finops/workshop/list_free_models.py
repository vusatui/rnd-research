"""List current OpenRouter ':free' models that support tool calling, with the list price of their paid twin
(used for shadow cost). The free list changes often; pick one and set OPENROUTER_MODEL."""
import json
import urllib.request

data = json.load(urllib.request.urlopen("https://openrouter.ai/api/v1/models"))["data"]
paid = {m["id"]: m["pricing"] for m in data}
for m in sorted(data, key=lambda m: m["id"]):
    if m["id"].endswith(":free"):
        tools = "tools" if "tools" in (m.get("supported_parameters") or []) else "     "
        p = paid.get(m["id"].removesuffix(":free"))
        price = f"paid twin ${float(p['prompt'])*1e6:.2f}/${float(p['completion'])*1e6:.2f} per 1M in/out" if p else "no paid twin"
        print(f"{m['id']:55} {tools} ctx={m.get('context_length'):>8}  {price}")
