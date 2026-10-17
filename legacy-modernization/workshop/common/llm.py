"""Minimal OpenRouter client (OpenAI-compatible) with free-model fallback and JSON extraction."""
from __future__ import annotations

import json
import os
import re
import time

from dotenv import load_dotenv

from .paths import WORKSHOP

load_dotenv(WORKSHOP / ".env")

# Free models change often: run `python list_free_models.py` and set OPENROUTER_MODEL.
DEFAULT_MODELS = [
    "nvidia/nemotron-3-super-120b-a12b:free",
    "google/gemma-4-31b-it:free",
    "poolside/laguna-s-2.1:free",
    "cohere/north-mini-code:free",
]


def models() -> list[str]:
    m = os.environ.get("OPENROUTER_MODEL")
    return [m] + [x for x in DEFAULT_MODELS if x != m] if m else DEFAULT_MODELS


def client():
    from openai import OpenAI
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise SystemExit("Set OPENROUTER_API_KEY (free key: https://openrouter.ai/keys) in env or workshop/.env")
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key, timeout=300)


def chat(messages: list[dict], temperature: float = 0.0, max_tokens: int = 8000,
         validate=None) -> tuple[str, str]:
    """Returns (text, model_used). Falls through the free-model list on errors, rate limits,
    truncated replies, or replies that fail `validate(text)` (e.g. broken JSON)."""
    c, last_err = client(), None
    for model in models():
        for attempt in range(2):
            try:
                t0 = time.time()
                r = c.chat.completions.create(model=model, messages=messages,
                                              temperature=temperature, max_tokens=max_tokens)
                text = (r.choices[0].message.content or "").strip()
                finish = r.choices[0].finish_reason
                (WORKSHOP / "out").mkdir(exist_ok=True)
                (WORKSHOP / "out" / "last_llm_reply.txt").write_text(text)
                if os.environ.get("LLM_DEBUG"):
                    print(f"  [{model}] {time.time() - t0:.0f}s finish={finish} chars={len(text)}")
                if not text:
                    raise RuntimeError(f"{model}: empty response (finish={finish})")
                if validate:
                    validate(text)
                return text, model
            except Exception as e:  # noqa: BLE001 - free tier fails in many ways
                last_err = e
                time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"all free models failed, last error: {last_err}")


def extract_json(text: str):
    """Pull the first JSON object/array out of a model reply (handles ```json fences and prose)."""
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if fence:
        text = fence.group(1)
    start = min([i for i in (text.find("{"), text.find("[")) if i >= 0], default=-1)
    if start < 0:
        raise ValueError("no JSON in model reply")
    return json.JSONDecoder().raw_decode(text[start:])[0]


def extract_code(text: str, lang: str = "python") -> str:
    m = re.search(rf"```(?:{lang}|py)?\s*\n(.*?)```", text, re.S)
    return (m.group(1) if m else text).strip() + "\n"
