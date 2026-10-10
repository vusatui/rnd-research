"""Упр. 4: computer-use цикл screenshot -> Claude -> action на E2B Desktop.
Версию tool/beta сверить с docs.anthropic.com (computer use) — они обновляются."""
import base64, sys
from dotenv import load_dotenv
import anthropic
from e2b_desktop import Sandbox

load_dotenv()
MODEL = "claude-sonnet-4-5"
TOOL_TYPE, BETA = "computer_20250124", "computer-use-2025-01-24"
W, H = 1024, 768
client = anthropic.Anthropic()

def shot(d):
    return {"type": "image", "source": {"type": "base64", "media_type": "image/png",
            "data": base64.b64encode(d.screenshot()).decode()}}

def act(d, a):
    t = a["action"]; xy = a.get("coordinate")
    if t == "screenshot": pass
    elif t == "left_click": d.left_click(*xy)
    elif t == "double_click": d.double_click(*xy)
    elif t == "right_click": d.right_click(*xy)
    elif t == "mouse_move": d.move_mouse(*xy)
    elif t == "type": d.write(a["text"])
    elif t == "middle_click": d.middle_click(*xy)
    elif t == "triple_click":
        for _ in range(3): d.left_click(*xy)
    elif t == "left_click_drag": d.drag(tuple(a["start_coordinate"]), tuple(xy))
    elif t == "key":  # Claude шлёт xdotool-нотацию: "ctrl+l" -> ["ctrl", "l"]
        keys = a["text"].split("+"); d.press(keys if len(keys) > 1 else keys[0])
    elif t == "scroll":
        if xy: d.move_mouse(*xy)
        d.scroll(a.get("scroll_direction", "down"), a.get("scroll_amount", 3))
    elif t == "wait": d.wait(int(a.get("duration", 1) * 1000))
    else: print("неподдержанное действие:", t)
    return shot(d)

def main(task, max_steps=25):
    d = Sandbox.create(resolution=(W, H), timeout=900)
    d.stream.start()
    print("Live view:", d.stream.get_url())
    msgs = [{"role": "user", "content": task}]
    tools = [{"type": TOOL_TYPE, "name": "computer", "display_width_px": W, "display_height_px": H}]
    try:
        for _ in range(max_steps):
            r = client.beta.messages.create(model=MODEL, max_tokens=1024, tools=tools, messages=msgs, betas=[BETA])
            msgs.append({"role": "assistant", "content": r.content})
            uses = [b for b in r.content if b.type == "tool_use"]
            for b in r.content:
                if b.type == "text": print("🤖", b.text)
            if not uses: break
            msgs.append({"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": u.id, "content": [act(d, u.input)]} for u in uses]})
    finally:
        input("Enter чтобы убить песочницу..."); d.kill()

if __name__ == "__main__":
    main(" ".join(sys.argv[1:]) or "Открой Firefox, найди погоду в Стамбуле и скажи температуру.")
