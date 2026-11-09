# Workshop code: System One / decision models

## Quick start with Docker

Only Docker and make are needed. Run from `system-one-models/`:

```bash
cd system-one-models
cp .env.example .env     # add a free OPENROUTER_API_KEY for ex2/ex3 (https://openrouter.ai/keys)
make ex1                 # classic classifier baseline, no key
make ex2 LIMIT=15 K=3    # free LLM forced into decision shape
make ex3 THRESHOLD=0.6   # cascade: classifier first, LLM when unsure
make ex3-sweep           # threshold sweep with a "human" queue, no key
make ex4                 # real decision APIs, skips providers without keys
make workshop            # ex1 + ex2 + ex3 in a row
make models              # current free OpenRouter models (the list changes often)
make shell               # a shell in the container
```

`MOCK=1` (for example `make workshop MOCK=1`) swaps the LLM for deterministic keyword rules (`mock_decider.py`), so everything runs offline without a key. Output then says `BACKEND: MOCK`; its accuracy numbers mean nothing. Your edits under `workshop/` (e.g. new rows in `data/tickets.jsonl`) are mounted into the container, no rebuild needed. `make test` runs the offline smoke tests that CI runs.

## Without Docker

```bash
cd system-one-models/workshop
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # add a free OPENROUTER_API_KEY for ex2/ex3
python list_free_models.py    # free models change often; set OPENROUTER_MODEL
```

| # | Folder | Needs | What you learn |
|---|---|---|---|
| 1 | `ex1_classic_baseline/` | nothing (CPU) | A trained classifier is already a System 1: probabilities, microsecond latency, calibration (ECE) |
| 2 | `ex2_llm_as_decider/` | free OpenRouter key | Forcing a generative LLM into the decision shape (`state + typed questions -> probabilities`); cost of self-consistency |
| 3 | `ex3_cascade/` | nothing (`--no-llm`) or OpenRouter key | Confidence-gated System 1 -> System 2 escalation; threshold sweep |
| 4 | `ex4_decision_apis/` | optional paid keys | Same question to Jev, OpenAI Decisions, Cloudflare Clef |

`decider.py` is a small Jev-shaped wrapper (`choice` / `score` / `noul`) over any chat LLM.
Dataset: `data/tickets.jsonl`, 40 synthetic support tickets (department + urgency).
