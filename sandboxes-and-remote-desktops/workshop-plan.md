# Workshop (2–2.5 h)

**Prerequisites:** Python 3.10+, Docker, an E2B key (Hobby, free), a free OpenRouter key (`OPENROUTER_API_KEY`; free `:free` models, any OpenAI-compatible endpoint works via `LLM_BASE_URL`). `pip install -r workshop/requirements.txt`.

| # | Exercise | Time | Outcome |
|---|---|---|---|
| 1 | `ex1_e2b_code` — create a sandbox, run code, files, limits, kill it | 20 min | understanding of the sandbox lifecycle |
| 2 | `ex2_llm_loop` — `run_python` tool → E2B, the agent solves a data-analysis task | 35 min | an agent loop with isolation |
| 3 | `ex3_docker_desktop` — your own desktop: Docker+Xvfb+noVNC+Chromium, Playwright inside, watch it in the browser on :6080 | 35 min | a self-hosted remote desktop |
| 4 | `ex4_computer_use` — generic screenshot→vision LLM→function-tool action loop (click/type/key/scroll/screenshot/wait/done); backend `DESKTOP_BACKEND=docker` (ex3 container) or `e2b` (E2B Desktop) | 40 min | a computer-use agent with live view |

Bonus tasks: run ex3 with `--runtime=runsc` (gVisor); restrict egress (`--network none` / allowlist proxy); prompt-injection demo: a file with an "instruction" inside the sandbox — show that the damage stays contained.

## LLM models (OpenRouter, free tier)

Checked 2026-10-10 via `https://openrouter.ai/api/v1/models` (filter: `:free` + `tools` in `supported_parameters`). The free list changes often: run `python workshop/list_free_models.py` before the workshop. Free models are rate-limited (roughly 20 req/min and a small daily cap without credits) and may log prompts — never send secrets.

| Use | Default (env) | Alternatives |
|---|---|---|
| ex2, tool calling | [`nvidia/nemotron-3-super-120b-a12b:free`](https://openrouter.ai/nvidia/nemotron-3-super-120b-a12b:free) (`EX2_MODEL`) | [`nvidia/nemotron-3-ultra-550b-a55b:free`](https://openrouter.ai/nvidia/nemotron-3-ultra-550b-a55b:free), [`poolside/laguna-s-2.1:free`](https://openrouter.ai/poolside/laguna-s-2.1:free), [`cohere/north-mini-code:free`](https://openrouter.ai/cohere/north-mini-code:free), [`google/gemma-4-31b-it:free`](https://openrouter.ai/google/gemma-4-31b-it:free) |
| ex4, vision + tool calling | [`google/gemma-4-31b-it:free`](https://openrouter.ai/google/gemma-4-31b-it:free) (`EX4_MODEL`) | [`thinkingmachines/inkling:free`](https://openrouter.ai/thinkingmachines/inkling:free), [`thinkingmachines/inkling-small:free`](https://openrouter.ai/thinkingmachines/inkling-small:free), [`google/gemma-4-26b-a4b-it:free`](https://openrouter.ai/google/gemma-4-26b-a4b-it:free), [`nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`](https://openrouter.ai/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free), [`dots-studio/dots-3-note-preview:free`](https://openrouter.ai/dots-studio/dots-3-note-preview:free) |

Generic open models are not trained for pixel-precise clicking the way vendor computer-use models are; expect misclicks — that is a useful discussion point. Vendor-native alternatives (not used in code, mention in the talk): Anthropic's computer-use tool (`computer_toolset_20260801`, Claude) and OpenAI's computer-use tool in the Responses API — they return structured actions in a model-specific schema, while ex4 uses plain function tools so any model fits.

## Testing without an LLM

`DESKTOP_BACKEND=docker python workshop/ex4_computer_use/test_backend.py` (ex3 container named `desk` running) drives the same `execute()` the agent uses and saves `ex4-smoke.png`.
