"""Shadow pricing: free models cost $0, which hides the cost problem. We price every call at the OpenRouter list
price of the *paid* variant of the same model (e.g. `nvidia/nemotron-3-super-120b-a12b` for the `:free` one),
fetched live from https://openrouter.ai/api/v1/models and cached in out/prices.json."""
from __future__ import annotations

import json
import time
import urllib.request

from .paths import OUT

CACHE = OUT / "prices.json"


def _load() -> dict:
    if CACHE.exists() and time.time() - CACHE.stat().st_mtime < 86400:
        return json.loads(CACHE.read_text())
    try:
        data = json.load(urllib.request.urlopen("https://openrouter.ai/api/v1/models", timeout=20))["data"]
        prices = {m["id"]: [float(m["pricing"]["prompt"]), float(m["pricing"]["completion"])] for m in data
                  if m.get("pricing")}
        CACHE.write_text(json.dumps(prices))
        return prices
    except Exception:  # noqa: BLE001 - offline: no shadow price
        return json.loads(CACHE.read_text()) if CACHE.exists() else {}


_P = None


def price_per_token(model: str) -> tuple[float, float]:
    """USD per input token, per output token, for the paid twin of `model` (0, 0 if unknown)."""
    global _P
    if _P is None:
        _P = _load()
    base = model.removesuffix(":free")
    return tuple(_P.get(base, [0.0, 0.0]))


def shadow_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    pi, po = price_per_token(model)
    return input_tokens * pi + output_tokens * po
