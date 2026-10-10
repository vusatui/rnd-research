"""Shared helpers: dataset loading, metrics (accuracy + Expected Calibration Error), OpenRouter client."""
import json, os, pathlib
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).parent
load_dotenv(ROOT / ".env")
DEPARTMENTS = ["billing", "technical", "account", "sales", "other"]
URGENCY = ["low", "medium", "high"]


def load_tickets():
    return [json.loads(l) for l in open(ROOT / "data" / "tickets.jsonl")]


def ece(confidences, correct, bins=5):
    """Expected Calibration Error: |accuracy - confidence| averaged over confidence bins."""
    n, total = len(confidences), 0.0
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        idx = [i for i, c in enumerate(confidences) if lo < c <= hi or (b == 0 and c == 0)]
        if idx:
            acc = sum(correct[i] for i in idx) / len(idx)
            conf = sum(confidences[i] for i in idx) / len(idx)
            total += len(idx) / n * abs(acc - conf)
    return total


def openrouter():
    from openai import OpenAI
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise SystemExit("Set OPENROUTER_API_KEY in workshop/.env (free key: https://openrouter.ai/keys)")
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)


def model_name():
    return os.environ.get("OPENROUTER_MODEL", "nvidia/nemotron-3-super-120b-a12b:free")
