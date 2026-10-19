"""Minimal OpenRouter client (OpenAI-compatible) for cost experiments.

Deliberately NO fallbacks and NO automatic retries: a cost experiment must know exactly which model answered and
how many calls were made (a silent retry is a silent extra charge). Reasoning is disabled by default because hidden
reasoning tokens are billed as output on paid models and make free models slow.

Every call returns a Usage record with input / cached / output tokens as reported by the provider.
"""
from __future__ import annotations

import os
import threading
import time
from dataclasses import dataclass

from dotenv import load_dotenv

from .paths import WORKSHOP

load_dotenv(WORKSHOP / ".env")

# Default model pair (free endpoints). Shadow prices come from their paid twins, see common/pricing.py.
LARGE = os.environ.get("LARGE_MODEL", "nvidia/nemotron-3-ultra-550b-a55b:free")
SMALL = os.environ.get("SMALL_MODEL", "nvidia/nemotron-3.5-lightning:free")

RPM = int(os.environ.get("OPENROUTER_RPM", "18"))   # free tier: 20 requests/min per account
_recent: list[float] = []
_lock = threading.Lock()
_client = None
CALLS = {"n": 0}


@dataclass
class Usage:
    model: str
    input_tokens: int
    cached_tokens: int
    cache_write_tokens: int
    output_tokens: int
    reasoning_tokens: int
    latency_s: float
    finish_reason: str | None
    provider: str | None = None


def _throttle():
    with _lock:   # thread-safe: the free tier limit is per account, not per thread
        now = time.time()
        _recent[:] = [t for t in _recent if now - t < 60]
        if len(_recent) >= RPM:
            time.sleep(60 - (now - _recent[0]) + 0.5)
        _recent.append(time.time())


def client():
    global _client
    if _client is None:
        from openai import OpenAI
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise SystemExit("Set OPENROUTER_API_KEY (free key: https://openrouter.ai/keys) in env or workshop/.env")
        _client = OpenAI(base_url=os.environ.get("OPENAI_BASE_URL_OVERRIDE", "https://openrouter.ai/api/v1"),
                         api_key=key, timeout=120, max_retries=0)
    return _client


def chat(messages: list[dict], model: str, max_tokens: int = 1500, temperature: float = 0.0,
         extra: dict | None = None) -> tuple[str, Usage]:
    """One chat completion, one attempt. Raises on any error (the caller decides what a failure means)."""
    _throttle()
    body = {"reasoning": {"enabled": False}}
    if extra:
        body.update(extra)
    t0 = time.time()
    with _lock:
        CALLS["n"] += 1
    r = client().chat.completions.create(model=model, messages=messages, max_tokens=max_tokens,
                                         temperature=temperature, extra_body=body)
    if not r.choices:
        raise RuntimeError(f"no choices: {getattr(r, 'error', None)}")
    u = r.usage
    ptd = getattr(u, "prompt_tokens_details", None)
    ctd = getattr(u, "completion_tokens_details", None)
    usage = Usage(
        model=model,
        input_tokens=getattr(u, "prompt_tokens", 0) or 0,
        cached_tokens=(getattr(ptd, "cached_tokens", 0) or 0) if ptd else 0,
        cache_write_tokens=(getattr(ptd, "cache_write_tokens", 0) or 0) if ptd else 0,
        output_tokens=getattr(u, "completion_tokens", 0) or 0,
        reasoning_tokens=(getattr(ctd, "reasoning_tokens", 0) or 0) if ctd else 0,
        latency_s=time.time() - t0,
        finish_reason=r.choices[0].finish_reason,
        provider=getattr(r, "provider", None),
    )
    return r.choices[0].message.content or "", usage
