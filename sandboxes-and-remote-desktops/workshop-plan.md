# Workshop (2–2.5 h)

**Prerequisites:** Python 3.10+, Docker, an E2B key (Hobby, free), an LLM key (OpenAI or Anthropic; any OpenAI-compatible provider works). `pip install -r workshop/requirements.txt`.

| # | Exercise | Time | Outcome |
|---|---|---|---|
| 1 | `ex1_e2b_code` — create a sandbox, run code, files, limits, kill it | 20 min | understanding of the sandbox lifecycle |
| 2 | `ex2_llm_loop` — `run_python` tool → E2B, the agent solves a data-analysis task | 35 min | an agent loop with isolation |
| 3 | `ex3_docker_desktop` — your own desktop: Docker+Xvfb+noVNC+Chromium, Playwright inside, watch it in the browser on :6080 | 35 min | a self-hosted remote desktop |
| 4 | `ex4_computer_use` — screenshot→LLM→action loop on E2B Desktop (or on the ex3 container) | 40 min | a computer-use agent with live view |

Bonus tasks: run ex3 with `--runtime=runsc` (gVisor); restrict egress (`--network none` / allowlist proxy); prompt-injection demo: a file with an "instruction" inside the sandbox — show that the damage stays contained.
