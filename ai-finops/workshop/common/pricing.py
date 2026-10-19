"""Shadow pricing. Free models cost $0, which hides the cost problem, so every call is priced as if it had run on
a paid endpoint. Token counts are the invariant; the price card is a parameter.

Price cards (USD per 1M tokens):
- "twin" (default): the OpenRouter list price of the *paid* variant of the same model, fetched live from
  https://openrouter.ai/api/v1/models (cached in out/prices.json; snapshot in results/prices_snapshot.json).
- "frontier": the same token counts re-priced at a frontier-API price card, large -> gpt-6.1-sol,
  small -> gpt-6-luna, from https://platform.openai.com/docs/pricing (read 2026-10-19). Different models use
  different tokenizers, so this is an order-of-magnitude illustration, not a quote.
"""
from __future__ import annotations

import json
import time
import urllib.request

from .paths import OUT, WORKSHOP

CACHE = OUT / "prices.json"
SNAPSHOT = WORKSHOP / "results" / "prices_snapshot.json"

# Read from https://platform.openai.com/docs/pricing on 2026-10-19 (standard tier, short context <=272K).
FRONTIER = {
    "large": {"label": "gpt-6.1-sol", "in": 2.00, "cached": 0.10, "write": 2.50, "out": 10.00},
    "small": {"label": "gpt-6-luna", "in": 0.10, "cached": 0.01, "write": 0.125, "out": 0.50},
}
BATCH_DISCOUNT = 0.5   # OpenAI, Anthropic and Gemini batch APIs: 50% off input and output (docs read 2026-10-19)


def _load() -> dict:
    if CACHE.exists() and time.time() - CACHE.stat().st_mtime < 86400:
        return json.loads(CACHE.read_text())
    try:
        data = json.load(urllib.request.urlopen("https://openrouter.ai/api/v1/models", timeout=20))["data"]
        prices = {}
        for m in data:
            p = m.get("pricing") or {}
            try:
                prices[m["id"]] = {"in": float(p.get("prompt", 0)) * 1e6, "out": float(p.get("completion", 0)) * 1e6,
                                   "cached": float(p["input_cache_read"]) * 1e6 if p.get("input_cache_read") else None,
                                   "write": float(p["input_cache_write"]) * 1e6 if p.get("input_cache_write") else None}
            except (TypeError, ValueError):
                continue
        CACHE.write_text(json.dumps(prices))
        return prices
    except Exception:  # noqa: BLE001 - offline: fall back to the committed snapshot
        for f in (CACHE, SNAPSHOT):
            if f.exists():
                return json.loads(f.read_text())
        return {}


_P: dict | None = None


def twin_price(model: str) -> dict:
    """USD per 1M tokens for the paid twin of `model` ({} if unknown)."""
    global _P
    if _P is None:
        _P = _load()
    p = _P.get(model.removesuffix(":free"))
    if not p:
        return {"in": 0.0, "out": 0.0, "cached": None, "write": None}
    return p


def price_for(model: str, card: str = "twin", tier: str | None = None) -> dict:
    if card == "twin":
        return twin_price(model)
    if card == "frontier":
        from .llm import LARGE
        return FRONTIER["large" if (tier or ("large" if model == LARGE else "small")) == "large" else "small"]
    raise ValueError(card)


def cost(model: str, input_tokens: int, output_tokens: int, cached_tokens: int = 0, cache_write_tokens: int = 0,
         card: str = "twin", batch: bool = False) -> float:
    """USD for one call. Cached tokens are billed at the cache-read rate when the card has one, otherwise at the
    normal input rate (i.e. no caching discount is assumed that the provider does not publish)."""
    p = price_for(model, card)
    cached_rate = p["cached"] if p.get("cached") is not None else p["in"]
    write_rate = p["write"] if p.get("write") is not None else p["in"]
    uncached = max(input_tokens - cached_tokens - cache_write_tokens, 0)
    usd = (uncached * p["in"] + cached_tokens * cached_rate + cache_write_tokens * write_rate
           + output_tokens * p["out"]) / 1e6
    return usd * (BATCH_DISCOUNT if batch else 1.0)


def snapshot(models: list[str]) -> dict:
    """Write the prices actually used to results/prices_snapshot.json (with the date) for reproducibility."""
    snap = {m.removesuffix(":free"): twin_price(m) for m in models}
    SNAPSHOT.parent.mkdir(exist_ok=True)
    SNAPSHOT.write_text(json.dumps({"fetched": time.strftime("%Y-%m-%d"), "source": "https://openrouter.ai/api/v1/models",
                                    "usd_per_1m_tokens": snap, **snap}, indent=2))
    return snap
