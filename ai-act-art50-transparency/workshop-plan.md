# Workshop plan: "Make a chatbot and a generator Art. 50-ready, then try to break the marks" (~2 h)

> General information, not legal advice. The exercises demonstrate **mechanisms and failure modes** with open stand-ins; they are not
> a conformity test and say nothing about any vendor's product.

Participants take a fictional product ("Ledgerly" support bot, procedurally generated images, a small local LLM) and
(1) make AI disclosure survive a hostile persona prompt, (2) sign, watermark and fingerprint images and measure what survives
everyday transformations (including a real browser screenshot), (3) watermark LLM text and attack it. Free OpenRouter models only
(`nvidia/nemotron-3.5-lightning:free` default, 20 req/min cap, client-throttled to 18); Exercises 2 and 3 run offline on CPU.
Code: [`workshop/`](workshop/); details, budgets and troubleshooting: [`workshop/README.md`](workshop/README.md).

| # | Time | Exercise | Needs | What participants do / learn |
|---|---|---|---|---|
| 0 | 10 min | Setup | Python >= 3.10, Chrome/Chromium for the screenshot rows (optional) | venv, `pip install -r requirements.txt`, `pytest -q tests` (25 offline tests), `.env` with a free key for ex1 |
| 1 | 40 min | **Chatbot disclosure** (`ex1_disclosure/`) | free key (60 requests) | Linter for insufficient forms (Guidelines point 38), fixed first-turn notice + badge, `DisclosingSession` with output guard and input router; red-team 15 prompts x 2 repeats x 2 configs (honest prompt vs "Anna, a human" persona); read the manual labels and `audit.py` to see why a regex judge under-counts |
| 2 | 40 min | **C2PA + watermark + fingerprint survival** (`ex2_c2pa/`) | none (offline) | Make a throw-away CA, sign an image as AI-created (IPTC `trainedAlgorithmicMedia`), embed a 64-bit DWT-DCT-SVD watermark, register a 256-bit dHash; apply 14 variants (file copy, tamper, re-encodes, geometry, screenshots, C2PA-aware crop) incl. real headless-Chrome screenshots; read C2PA verdicts (Trusted / Valid / Invalid / NoManifest); C2PA-aware crop that keeps the chain |
| 3 | 25 min | **Text watermark** (`ex3_text_watermark/`) | optional `requirements-text.txt` (torch CPU, ~1 GB) and ~18 free requests | SynthID-Text logits processor on SmolLM2-360M, own mean-g detector, null threshold from non-watermarked texts, edits, LLM paraphrase and translation cycle, length curve with false alarms |
| - | 5 min | Wrap-up | | Map each failure to a Code measure (1.1, 1.1.3, 3.3, 3.4) and to the deployer-side icon; checklist from `talk-outline.md` |

Stretch goals: replace the DWT-DCT-SVD stand-in with TrustMark or Video Seal and re-run `survival.py`; add a classifier to the router and measure
recall on your own probe set; add a Chrome/WhatsApp/X upload round trip (real platforms) to the transformation list; test the watermark against a
regeneration attack (img2img at low strength); add a multilingual identity-question probe; send a signed manifest through a C2PA-aware editor.

## Commands

```bash
cd ai-act-art50-transparency/workshop
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python -m pytest -q tests                       # 25 passed, 1 skipped (model test)
python ex2_c2pa/survival.py                     # ~10 s; writes results/ex2_survival_<date>.{json,md}
cp .env.example .env                            # OPENROUTER_API_KEY=...
python check_quota.py                           # free requests left today
python ex1_disclosure/run_redteam.py            # 60 requests; resumable
python ex1_disclosure/audit.py                  # manual-label audit of the run
python ex1_disclosure/chatbot.py                # try: are you a human?
pip install -r requirements-text.txt
python ex3_text_watermark/run_lab.py            # offline; first run generates and caches texts
python ex3_text_watermark/run_lab.py --llm-attacks
```

## Measured results (2026-10-26, our box: Python 3.13, CPU only, `nvidia/nemotron-3.5-lightning:free`)

Raw outputs: [`workshop/results/`](workshop/results/). Small samples (n = 3 to 20); numbers are for orientation, not statistics.

### Exercise 1 - disclosure (60 requests; temperature 0.7)

Manual labels of all 60 replies (`manual_labels.json`) vs the regex judge in `run_redteam.py` (the regex judge counted 10 human claims; reading found 15 explicit claims + 5 evasive):

| Configuration | 10 ordinary first replies say "I am an AI" | 20 identity questions: honest / human claim / evasive | Residual non-disclosing replies |
|---|---|---|---|
| A. honest system prompt only | 0/10 | 20 / 0 / 0 | 0 |
| B. "Anna, a human" persona prompt only | 0/10 | 0 / 15 / 5 | 20 |
| B + output guard (regex on reply) | 0/10 | guard replaced 10 replies | 10 (5 explicit claims + 5 evasive) -> guard recall 10/15 on explicit claims |
| B + input router (regex on question) | | router answered 20/20 (in-sample) | 0 |
| fixed first-turn notice | 10/10 by construction | | |

Router on a fresh probe written after the router (13 identity questions, 9 ordinary questions): **7/13 caught, 0/9 false alarms**; not good enough alone. Lesson: the
guarantee must come from app-owned text (notice, badge, routing), and any judge or guard must itself be measured.

### Exercise 2 - survival (3 synthetic 768x768 images; c2pa-python 0.38.1, c2pa-rs 0.91.3)

Watermark detected = >= 50/64 bits (chance p ~ 1e-5); fingerprint match = <= 40/256 bits and nearer than any other image (nearest unrelated image: >= 105).

| Transformation | C2PA | Watermark (mean bit acc.) | Fingerprint (mean dist.) |
|---|---|---|---|
| as issued / file copy | Trusted x3 | 3/3 (1.00) | 3/3 (0) |
| 1 byte changed | Invalid x3 | 3/3 (1.00) | 3/3 (9.7) |
| re-save as PNG | NoManifest | 3/3 (1.00) | 3/3 (0) |
| JPEG q85 / q60 | NoManifest | 3/3 (0.97 / 0.89) | 3/3 (0.3 / 1.3) |
| messenger-like 1280 px q70 (simulated) | NoManifest | 3/3 (0.91) | 3/3 (1.3) |
| resize 50% | NoManifest | **0/3 (0.47)** | 3/3 (0.7) |
| gaussian noise s=8 | NoManifest | 3/3 (1.00) | 3/3 (5.0) |
| crop 80% | NoManifest | **0/3 (0.50)** | **0/3 (94.0)** |
| rotate 5 deg | NoManifest | **0/3 (0.53)** | **0/3 (55.7)** |
| mirror | NoManifest | **0/3 (0.50)** | **0/3 (142.3)** |
| browser screenshot 1:1 (lossless) | NoManifest | 3/3 (1.00) | 3/3 (0) |
| browser screenshot, 125% scaling + border | NoManifest | **0/3 (0.53)** | **0/3 (49.7)** |
| C2PA-aware crop + re-sign | Trusted x3 | 0/3 | 0/3 |

C2PA lost in 11/11 non-aware transformations; 4/11 defeat all three layers. Unit tests add: without a trust anchor an intact file is `Valid` (+ `signingCredential.untrusted`), not `Trusted`.

### Exercise 3 - text watermark (SmolLM2-360M-Instruct, 12 prompts, <= 150 new tokens; threshold 0.5152 = max over 24 non-watermarked texts)

| Condition | n | mean g | detected |
|---|---|---|---|
| watermarked | 12 | 0.557 | 12/12 |
| non-watermarked LLM text / human text | 12 / 12 | 0.502 / 0.496 | 0/12 / 0/12 |
| drop 10% / 30% words | 12 | 0.544 / 0.524 | 12/12 / 10/12 |
| swap 20% adjacent words | 12 | 0.529 | 12/12 |
| typos in 30% of words | 12 | 0.519 | 8/12 |
| first half only | 12 | 0.550 | 12/12 |
| LLM paraphrase (4-gram overlap 0.01) | 6 | 0.508 | **1/6** |
| EN->DE->EN by LLM (overlap 0.41) | 6 | 0.526 | 6/6 |
| first 20 / 40 / 80 / 150 tokens | 12 | 0.535 / 0.549 / 0.556 / 0.557 | 12/12 each; false alarms 5/24, 2/24, 0/24, 0/24 |

## Caveats (also in `research.md` section 5)

Stand-ins, not products: a test CA, DWT-DCT-SVD, procedural images, a 360M model with demo keys, our own detector (not Google's). Samples are tiny; the router
result is partly in-sample; "messenger-like" is a simulation; the translation cycle partly preserves phrasing; human reference texts are 19th-century prose.
Quota: the key used had 1000 free-model requests/day; the three-lab budget is about 80 requests (ex1 60 + ex3 up to 18).
