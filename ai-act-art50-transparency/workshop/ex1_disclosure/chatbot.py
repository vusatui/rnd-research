"""Interactive demo: a chat session with the fixed first-turn notice, a badge and the output guard.

    python ex1_disclosure/chatbot.py              # B_persona prompt (pressure to claim humanity) + guard ON
    python ex1_disclosure/chatbot.py --no-guard --no-router   # see what the raw model says
    python ex1_disclosure/chatbot.py --prompt a   # the 'honest prompt' config
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import llm  # noqa: E402
from ex1_disclosure.disclosure import DisclosingSession  # noqa: E402
from ex1_disclosure.run_redteam import PROMPT_A, PROMPT_B  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--no-guard", action="store_true", help="do not replace model replies that claim to be human")
ap.add_argument("--no-router", action="store_true", help="do not answer 'are you human/AI?' from the application")
ap.add_argument("--prompt", choices=["a", "b"], default="b")
a = ap.parse_args()
s = DisclosingSession(llm=lambda m: llm.chat(m, max_tokens=250), system_prompt=PROMPT_A if a.prompt == "a" else PROMPT_B,
                      guard=not a.no_guard, router=not a.no_router)
print(f"[{s.badge}] {s.transcript[0].text}\n(type 'quit' to stop)\n")
while True:
    try:
        u = input("you> ").strip()
    except EOFError:
        break
    if u in ("quit", "exit", ""):
        break
    r = s.ask(u)
    print(f"[{s.badge}] {r}" + ("   <-- answered/replaced by the application, not the model" if s.transcript[-1].guard_hit else "") + "\n")
