# Exercise 4: computer-use agent (generic, any vision + tool-calling model)

Loop: screenshot → vision LLM (OpenRouter, OpenAI-compatible) → function tool call (`click`, `type`, `key`, `scroll`, `screenshot`, `wait`, `done`) → executed on the desktop backend → new screenshot.

```bash
pip install -r ../requirements.txt
export OPENROUTER_API_KEY=...            # https://openrouter.ai/keys (free models need no credits)
# backend A: your own desktop from ex3
docker run --rm -d --name desk -p 127.0.0.1:6080:6080 --shm-size=1g agent-desktop
DESKTOP_BACKEND=docker python agent.py "Open https://news.ycombinator.com and tell me the top story"
# backend B: E2B Desktop (cloud)
DESKTOP_BACKEND=e2b E2B_API_KEY=... python agent.py
# smoke test without an LLM
DESKTOP_BACKEND=docker python test_backend.py
```

- `backends.py` — `DockerBackend` (wraps `ex3_docker_desktop/desktop_tools.py`, xdotool via `docker exec`) and `E2BBackend` (`e2b_desktop`), same interface.
- Model: `EX4_MODEL` (default `dots-studio/dots-3-note-preview:free`); optional `EX4_FALLBACK_MODELS` (comma list, OpenRouter tries them when the main model fails). See `../../workshop-plan.md` for test results and alternatives.
- Free models are rate-limited often: the agent retries 429/5xx and empty responses with backoff.
- The agent accepts pixel ints, numeric strings, or 0..1 normalized coordinates, and key names like `enter` or `["ctrl","l"]`.
- Screenshots are sent as user messages (many OpenAI-compatible models reject images in `tool` messages); only the last 3 are kept.
- Desktop resolution is read from the first screenshot (1280x800 by default); coordinates are screenshot pixels.
- Native alternatives (docs only): Anthropic computer-use tool, OpenAI computer-use in the Responses API.
