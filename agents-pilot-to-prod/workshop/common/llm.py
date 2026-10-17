"""Minimal OpenRouter client (OpenAI-compatible): free-model fallback, retries, reasoning off, usage capture.

Every call returns an LLMResult with the model actually used, token usage and wall-clock latency, so the agent
can put them on OpenTelemetry spans and enforce budgets.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field

from dotenv import load_dotenv

from .paths import WORKSHOP

load_dotenv(WORKSHOP / ".env")

# Free models change often: run `python list_free_models.py` and set OPENROUTER_MODEL.
DEFAULT_MODELS = [
    "nvidia/nemotron-3-super-120b-a12b:free",
    "google/gemma-4-31b-it:free",
    "nvidia/nemotron-3.5-lightning:free",
    "poolside/laguna-s-2.1:free",
    "google/gemma-4-26b-a4b-it:free",
]


@dataclass
class LLMResult:
    message: object            # openai ChatCompletionMessage (content, tool_calls)
    model: str
    input_tokens: int
    output_tokens: int
    latency_s: float
    finish_reason: str | None
    attempts: list = field(default_factory=list)   # [(model, error)] for failed attempts
    response_id: str | None = None


def models(preferred: str | None = None) -> list[str]:
    m = preferred or os.environ.get("OPENROUTER_MODEL")
    return [m] + [x for x in DEFAULT_MODELS if x != m] if m else list(DEFAULT_MODELS)


_client = None
_recent: list[float] = []
# OpenRouter free tier: 20 requests/min per account (and 50/day without credits, 1000/day with >= $10 credits).
RPM = int(os.environ.get("OPENROUTER_RPM", "18"))


def _throttle():
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


def chat(messages: list[dict], tools: list[dict] | None = None, model: str | None = None,
         temperature: float = 0.0, max_tokens: int = 1500, fallback: bool = True) -> LLMResult:
    """One chat completion. Falls through the free-model list on errors / rate limits / empty replies."""
    c, attempts = client(), []
    mode = os.environ.get("OPENROUTER_REASONING", "off")
    # Free "thinking" models can burn max_tokens on hidden reasoning and return nothing. Default: reasoning off.
    extra = ({"reasoning": {"enabled": False}} if mode == "off" else
             {} if mode == "default" else {"reasoning": {"effort": mode}})
    candidates = models(model) if fallback else [model or models()[0]]
    for m in candidates:
        attempt = 0
        while attempt < 2:
            _throttle()
            t0 = time.time()
            try:
                kw = dict(model=m, messages=messages, temperature=temperature, max_tokens=max_tokens,
                          extra_body=extra)
                if tools:
                    kw["tools"] = tools
                r = c.chat.completions.create(**kw)
                if not r.choices:
                    raise RuntimeError(f"no choices: {getattr(r, 'error', None)}")
                msg = r.choices[0].message
                if not (msg.content or msg.tool_calls):
                    raise RuntimeError(f"empty response (finish={r.choices[0].finish_reason})")
                u = r.usage
                return LLMResult(msg, m, getattr(u, "prompt_tokens", 0) or 0, getattr(u, "completion_tokens", 0) or 0,
                                 time.time() - t0, r.choices[0].finish_reason, attempts, getattr(r, "id", None))
            except Exception as e:  # noqa: BLE001 - the free tier fails in many ways
                attempts.append((m, f"{type(e).__name__}: {str(e)[:160]}"))
                if os.environ.get("LLM_DEBUG"):
                    print(f"  [{m}] failed: {attempts[-1][1]}", flush=True)
                if "free-models-per-min" in str(e) and len(attempts) < 8:
                    time.sleep(15)          # account-wide limit: switching models does not help, wait instead
                    continue
                if "free-models-per-day" in str(e):
                    raise RuntimeError("OpenRouter daily free-model quota exhausted") from e
                attempt += 1
                time.sleep(2 * attempt)
    raise RuntimeError(f"all free models failed: {attempts[-3:]}")
