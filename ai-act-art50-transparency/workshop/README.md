# Workshop: marking and disclosing AI content in code (EU AI Act Art. 50)

Three hands-on labs. **General information, not legal advice**; nothing here is a compliance certificate. The
signing certificates are a throw-away test CA, the image watermark is an open 2008-era algorithm, the "AI image" is
procedural, and the text watermark runs on a 360M-parameter local model - they illustrate mechanisms, they are not what
a production generator ships.

| Lab | What you do | Needs |
|---|---|---|
| `ex1_disclosure/` | Chatbot disclosure (Art. 50(1)+(5)) at **system level**: fixed first-turn notice, badge, input router, output guard; red-team it against a "pose as a human" system prompt | free OpenRouter key |
| `ex2_c2pa/` | Sign an "AI image" with **C2PA** Content Credentials, add an invisible watermark and a perceptual fingerprint, then push it through 11 everyday transformations and see which layer survives | nothing (offline); Chrome/Chromium optional (real screenshot) |
| `ex3_text_watermark/` | **SynthID-Text** (HF `transformers`) on a local model: detect, then attack it (word drops, typos, paraphrase, translation cycle) | `requirements-text.txt` (~1 GB incl. model); key only for LLM attacks |

## Quick start

```bash
cd workshop
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python -m pytest -q tests                       # offline, no key: 25 tests
python ex2_c2pa/survival.py                     # ~10 s, offline
cp .env.example .env                            # paste a free key from https://openrouter.ai/keys
python check_quota.py                           # how many free requests are left today
python ex1_disclosure/run_redteam.py            # 60 requests, ~4-8 min (20 requests/min cap, throttled to 18)
python ex1_disclosure/audit.py                  # offline: manual-label audit of the committed run
python ex1_disclosure/chatbot.py                # interactive demo (try: "are you a human?")
pip install -r requirements-text.txt            # optional, torch CPU + transformers
python ex3_text_watermark/run_lab.py            # offline part, ~10 min on CPU the first time (generation is cached)
python ex3_text_watermark/run_lab.py --llm-attacks   # + paraphrase / translation cycle: ~18 requests
RUN_MODEL_TESTS=1 python -m pytest -q tests/test_ex3.py   # loads the model
```

Free-tier budget: ex1 = 60 requests, ex3 `--llm-attacks` = 18, interactive demo = 1 per message. The default model is
`nvidia/nemotron-3.5-lightning:free` (change with `CHAT_MODEL`; `python list_free_models.py`). `common/llm.py` throttles to
18 requests/min, turns reasoning off, and on HTTP 429 waits 65 s and retries (at most 2 retries). The key is read from
`OPENROUTER_API_KEY` (env or `.env`) and never printed or written to results.

## Results committed in `results/` (2026-10-26, our box)

| File | What |
|---|---|
| `ex1_redteam_2026-10-26.json` | all 60 replies (2 configs x 15 prompts x 2 repeats), regex-judged summary |
| `ex1_audit.json` + `ex1_disclosure/manual_labels.json` | my manual reading of every reply and the audit against it |
| `ex2_survival_2026-10-26.{md,json}` | survival matrix, 3 images x 13 transformations, per-image rows |
| `ex3_text_2026-10-26.{md,json}`, `ex3_texts.json`, `ex3_attack_texts.json` | scores, generated and attacked texts |

Free models are non-deterministic and the samples are small (n = 10-20 for ex1, 3 for ex2, 12 for ex3): treat numbers as
illustrations of the mechanism, not benchmarks. Re-running gives different ex1/ex3-attack numbers; ex2 is deterministic
except for the signing time.

## Ex1 - what to look at

1. `ex1_disclosure/disclosure.py`: the notice, `lint_disclosure` (the "insufficient alone" forms from Guidelines point 38),
   `DisclosingSession` (notice before the first user message, router, guard), `agent_message_header` (Guidelines point 31).
2. `run_redteam.py`: config A (honest prompt), config B (a deployer prompt telling the bot to be "Anna, a human"). Read the
   replies yourself - the regex judge in the run is a heuristic and misses cases; `audit.py` shows by how much.
3. `chatbot.py --no-guard --no-router` vs. default.

## Ex2 - what to look at

`lab.py` (signing, reading, watermark, fingerprint) and `survival.py` (the matrix). Add your own image with
`--image path.png`. Try: sign a PNG, upload it to a platform you use, download it again, and run
`python -c "from ex2_c2pa import lab; from pathlib import Path; print(lab.read_credentials(Path('x.png')))"`.
The test CA is trusted only inside this lab; without it a verifier reports `Valid` + `signingCredential.untrusted`
(that is test `test_without_trust_anchor_it_is_only_valid`).

## Ex3 - what to look at

`lab.py` (generation with `SynthIDTextWatermarkingConfig`, mean-g detector, offline attacks) and `run_lab.py`
(null set = unwatermarked LLM text + public-domain human text; threshold = max over the null set; length curve; attacks).
The demo keys are in the source - in production they are secret, and anyone holding them can detect (and forge/scrub).

## Troubleshooting

- `ManifestNotFound` / `NoManifest`: the file was re-encoded by something that is not C2PA-aware. That is the point of ex2.
- `429` from OpenRouter: the client waits and retries; if the daily cap is gone, wait for 00:00 UTC or change key.
- `c2pa-python` wheels need Python >= 3.10. `opencv-python-headless` is used so no GUI libraries are needed.
- No Chrome? The two screenshot rows are skipped and marked "tool missing".
