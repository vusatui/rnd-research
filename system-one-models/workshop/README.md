# Workshop code: System One / decision models

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
