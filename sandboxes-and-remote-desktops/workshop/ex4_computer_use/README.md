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
- Model: `EX4_MODEL` (default `google/gemma-4-31b-it:free`); see `../../workshop-plan.md` for alternatives.
- Screenshots are sent as user messages (many OpenAI-compatible models reject images in `tool` messages); only the last 3 are kept.
- Desktop resolution is 1280x800 for both backends; coordinates are screenshot pixels.
- Native alternatives (docs only): Anthropic computer-use tool, OpenAI computer-use in the Responses API.
