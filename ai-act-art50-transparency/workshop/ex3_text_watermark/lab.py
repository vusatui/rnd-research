"""SynthID-Text lab: watermark LLM output at generation time, detect with a keyed statistic, then try to break it.

SynthID-Text (Dathathri et al., Nature 2024, doi:10.1038/s41586-024-08025-4) is implemented in Hugging Face
`transformers` (SynthIDTextWatermarkLogitsProcessor). What we use here is a small LOCAL model (SmolLM2-360M-Instruct, CPU)
and a SIMPLE mean-g-value detector (HF documents that its own detector is not the one used for Gemini - texts from the Gemini
app are NOT detectable with this code). Everything here is a teaching-scale reproduction, not a measurement of Google's product.

How detection works: every token is chosen by 'tournament sampling' among candidates scored by pseudo-random g-values in {0,1}
(30 layers, seeded by the secret keys and the previous 4 tokens). Unwatermarked text has mean g ~= 0.5; watermarked text is
pushed above 0.5. No key -> no detection (the Code of Practice allows restricted access to text-watermark detectors for this
reason, Measure 3.x).
"""
from __future__ import annotations

import random
import re

import numpy as np

MODEL = "HuggingFaceTB/SmolLM2-360M-Instruct"
# DEMO keys. In production they are secret; anyone holding them can detect, anyone who learns them can forge/scrub.
KEYS = [654, 400, 836, 123, 340, 443, 597, 160, 57, 29, 590, 639, 13, 715, 468, 990, 966, 226, 324, 585,
        118, 504, 421, 521, 129, 669, 732, 225, 90, 960]
NGRAM = 5

_state: dict = {}


def load():
    if _state:
        return _state
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, SynthIDTextWatermarkingConfig
    from transformers.generation.logits_process import SynthIDTextWatermarkLogitsProcessor
    torch.manual_seed(0)
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.float32)
    cfg = SynthIDTextWatermarkingConfig(keys=KEYS, ngram_len=NGRAM)
    proc = SynthIDTextWatermarkLogitsProcessor(ngram_len=cfg.ngram_len, keys=cfg.keys, sampling_table_size=cfg.sampling_table_size,
                                               sampling_table_seed=cfg.sampling_table_seed,
                                               context_history_size=cfg.context_history_size, device="cpu")
    _state.update(tok=tok, model=model, cfg=cfg, proc=proc, torch=torch)
    return _state


def generate(prompt: str, watermark: bool, max_new_tokens: int = 150, seed: int = 0) -> str:
    s = load(); torch = s["torch"]
    torch.manual_seed(seed)
    ids = s["tok"].apply_chat_template([{"role": "user", "content": prompt}], add_generation_prompt=True,
                                       return_tensors="pt", return_dict=True)
    kw = dict(watermarking_config=s["cfg"]) if watermark else {}
    out = s["model"].generate(**ids, do_sample=True, temperature=0.8, top_k=40, max_new_tokens=max_new_tokens,
                              pad_token_id=s["tok"].eos_token_id, **kw)
    return s["tok"].decode(out[0, ids["input_ids"].shape[1]:], skip_special_tokens=True).strip()


def mean_g(text: str, max_tokens: int | None = None) -> float | None:
    """Detection score = mean g-value over all (n-gram, layer) pairs. ~0.5 if unmarked. None if text too short (<= ngram)."""
    s = load(); torch = s["torch"]
    ids = s["tok"].encode(text, add_special_tokens=False)
    if max_tokens:
        ids = ids[:max_tokens]
    if len(ids) <= NGRAM + 2:
        return None
    g = s["proc"].compute_g_values(torch.tensor([ids]))            # (1, L-4, depth)
    return float(g.float().mean())


def n_tokens(text: str) -> int:
    return len(load()["tok"].encode(text, add_special_tokens=False))


# ---------------------------------------------------------------- offline attacks (no LLM) ---------------------------
def drop_words(text: str, frac: float, seed: int = 0) -> str:
    rng = random.Random(seed); w = text.split()
    return " ".join(x for x in w if rng.random() > frac)


def swap_words(text: str, frac: float, seed: int = 0) -> str:
    """Swap adjacent word pairs with probability `frac` per position (reordering, meaning mostly kept)."""
    rng = random.Random(seed); w = text.split(); i = 0
    while i < len(w) - 1:
        if rng.random() < frac:
            w[i], w[i + 1] = w[i + 1], w[i]; i += 2
        else:
            i += 1
    return " ".join(w)


def typo_insert(text: str, frac: float, seed: int = 0) -> str:
    """Insert a harmless character into `frac` of the words (changes tokenisation, so n-gram hashes change)."""
    rng = random.Random(seed)
    return " ".join((x[: len(x) // 2] + "-" + x[len(x) // 2:]) if len(x) > 3 and rng.random() < frac else x for x in text.split())


def sentences(text: str) -> list[str]:
    return [x for x in re.split(r"(?<=[.!?])\s+", text) if x]
