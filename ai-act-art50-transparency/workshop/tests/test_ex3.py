"""Offline tests for ex3. Pure-text helpers always run; the model test needs the 360M model (set RUN_MODEL_TESTS=1)."""
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ex3_text_watermark import lab  # noqa: E402
from ex3_text_watermark.run_lab import overlap  # noqa: E402

T = "the quick brown fox jumps over the lazy dog while the city council approved a new bicycle lane network for everyone"


def test_drop_words_fraction():
    out = lab.drop_words(T, 0.3, seed=1)
    assert 0 < len(out.split()) < len(T.split())
    assert lab.drop_words(T, 0.0) == T


def test_swap_words_keeps_the_words():
    out = lab.swap_words(T, 0.5, seed=1)
    assert sorted(out.split()) == sorted(T.split()) and out != T


def test_typo_insert_changes_long_words_only():
    out = lab.typo_insert(T, 1.0)
    assert "qu-ick" in out and "the" in out.split()


def test_overlap_metric():
    assert overlap(T, T) == 1.0
    assert overlap(T, "completely different sentence about something else entirely here today") == 0.0


@pytest.mark.skipif(not os.environ.get("RUN_MODEL_TESTS"), reason="downloads SmolLM2-360M (~700 MB)")
def test_watermarked_text_scores_higher_than_plain():
    p = "Write a short paragraph about why sleep matters."
    wm = lab.mean_g(lab.generate(p, True, 120, seed=1)); pl = lab.mean_g(lab.generate(p, False, 120, seed=1))
    assert wm > pl and wm > 0.52
