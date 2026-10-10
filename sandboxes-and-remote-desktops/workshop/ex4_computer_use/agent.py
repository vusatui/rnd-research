"""Exercise 4: generic computer-use loop: screenshot -> vision LLM -> function-tool action.

No vendor computer-use API: plain OpenAI-style function tools, so any vision + tool-calling
model works (OpenRouter free models by default). Anthropic/OpenAI native computer-use tools
are discussed in the docs only.
  OPENROUTER_API_KEY  - required
  EX4_MODEL           - default google/gemma-4-31b-it:free (vision + tools)
  DESKTOP_BACKEND     - docker (ex3 container, default) | e2b (E2B Desktop, needs E2B_API_KEY)
"""
import base64, json, os, sys
from dotenv import load_dotenv
from openai import OpenAI
sys.path.insert(0, os.path.dirname(__file__))
from backends import make_backend, wait

load_dotenv()
MODEL = os.getenv("EX4_MODEL", "google/gemma-4-31b-it:free")

def _fn(name, desc, props=None, req=None):
    return {"type": "function", "function": {"name": name, "description": desc, "parameters": {
        "type": "object", "properties": props or {}, "required": req or []}}}
XY = {"x": {"type": "integer"}, "y": {"type": "integer"}}
TOOLS = [
    _fn("screenshot", "Take a fresh screenshot of the desktop."),
    _fn("click", "Click at pixel coordinates of the latest screenshot.",
        {**XY, "button": {"type": "string", "enum": ["left", "right"]}, "double": {"type": "boolean"}}, ["x", "y"]),
    _fn("type", "Type text at the current focus.", {"text": {"type": "string"}}, ["text"]),
    _fn("key", "Press a key or combo in xdotool syntax, e.g. Return, ctrl+l, ctrl+a.",
        {"keys": {"type": "string"}}, ["keys"]),
    _fn("scroll", "Scroll at a point.", {**XY, "direction": {"type": "string", "enum": ["up", "down"]},
        "amount": {"type": "integer"}}, ["direction"]),
    _fn("wait", "Wait N seconds (max 10) for the page to load.", {"seconds": {"type": "number"}}, ["seconds"]),
    _fn("done", "Finish the task with a final answer.", {"answer": {"type": "string"}}, ["answer"]),
]

def execute(desk, name, a):
    """Run one tool call on the backend; returns a short text result."""
    if name == "screenshot": return "ok"
    if name == "click": desk.click(int(a["x"]), int(a["y"]), a.get("button", "left"), bool(a.get("double")))
    elif name == "type": desk.type(a["text"])
    elif name == "key": desk.key(a["keys"])
    elif name == "scroll":
        if "x" in a and "y" in a: desk.move(int(a["x"]), int(a["y"]))
        desk.scroll(a.get("direction", "down"), int(a.get("amount", 3)))
    elif name == "wait": wait(a.get("seconds", 1))
    else: return f"unknown tool {name}"
    return "ok"

def image_msg(png: bytes, note="Current screen:"):
    # Screenshots go in a user message: many OpenAI-compatible models do not accept images in tool messages.
    return {"role": "user", "content": [{"type": "text", "text": note}, {"type": "image_url",
            "image_url": {"url": "data:image/png;base64," + base64.b64encode(png).decode()}}]}

def main(task, max_steps=25):
    client = OpenAI(base_url=os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1"),
                    api_key=os.environ["OPENROUTER_API_KEY"])
    desk = make_backend()
    print("Live view:", desk.live_url)
    msgs = [{"role": "system", "content": "You control a Linux desktop (1280x800) with a Chromium browser. "
             "Use the tools, one action at a time; coordinates are pixels of the latest screenshot. "
             "Call done(answer) when finished."},
            {"role": "user", "content": task}, image_msg(desk.screenshot())]
    try:
        for step in range(max_steps):
            m = client.chat.completions.create(model=MODEL, messages=msgs, tools=TOOLS).choices[0].message
            msgs.append(m.model_dump(exclude_none=True))
            if m.content: print("🤖", m.content)
            if not m.tool_calls:
                return m.content
            for tc in m.tool_calls:
                try: args = json.loads(tc.function.arguments or "{}")
                except json.JSONDecodeError as e: args, res = {}, f"bad arguments: {e}"
                print(f"[{step}] {tc.function.name} {args}")
                if tc.function.name == "done":
                    return args.get("answer")
                try: res = execute(desk, tc.function.name, args)
                except Exception as e: res = f"error: {e}"
                msgs.append({"role": "tool", "tool_call_id": tc.id, "content": res})
            msgs.append(image_msg(desk.screenshot()))
            # keep context small: drop all but the last 3 screenshots
            imgs = [i for i, x in enumerate(msgs) if x["role"] == "user" and isinstance(x["content"], list)]
            for i in imgs[:-3]: msgs[i] = {"role": "user", "content": "(old screenshot removed)"}
        return "max steps reached"
    finally:
        desk.close()

if __name__ == "__main__":
    print(main(" ".join(sys.argv[1:]) or "Open https://news.ycombinator.com in the browser and tell me the title of the top story."))
