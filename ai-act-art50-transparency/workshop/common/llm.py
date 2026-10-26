"""Minimal OpenRouter client (OpenAI-compatible) for the Art. 50 workshop.

One attempt per call (the only exception: a 429 "per-minute limit" answer is waited out and repeated, up to 2 times),
NO other retries and NO provider fallbacks: an experiment must know exactly which model answered and
how many calls were made (free tier: 20 requests/min, 50/day without credits, 1,000/day with >= $10 of credits).
Reasoning is disabled by default (free models are slow and noisy with it on).
"""
from __future__ import annotations

import os
import threading
import time

from dotenv import load_dotenv

from .paths import WORKSHOP

load_dotenv(WORKSHOP / ".env")

MODEL = os.environ.get("CHAT_MODEL", "nvidia/nemotron-3.5-lightning:free")
RPM = int(os.environ.get("OPENROUTER_RPM", "18"))
_recent: list[float] = []
_lock = threading.Lock()
_client = None
CALLS = {"n": 0}


def _throttle():
    with _lock:
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
        _client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key, timeout=120, max_retries=0)
    return _client


def chat(messages: list[dict], model: str | None = None, max_tokens: int = 400, temperature: float = 0.7) -> str:
    """One chat completion, one attempt. Raises on any error (the caller decides what a failure means)."""
    from openai import RateLimitError
    for attempt in range(3):
        _throttle()
        try:
            r = client().chat.completions.create(model=model or MODEL, messages=messages, max_tokens=max_tokens,
                                                 temperature=temperature, extra_body={"reasoning": {"enabled": False}})
            break
        except RateLimitError:      # 429 = per-minute window used up (also by other apps on your key): wait, then retry
            if attempt == 2:
                raise
            time.sleep(65)
    with _lock:
        CALLS["n"] += 1
    if not r.choices:
        raise RuntimeError(f"no choices: {getattr(r, 'error', None)}")
    return r.choices[0].message.content or ""
