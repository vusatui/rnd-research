"""Smoke-test a backend without any LLM: drives the same execute() the agent uses."""
import os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from backends import make_backend
from agent import execute

desk = make_backend()
for name, a in [("click", {"x": 600, "y": 60}), ("key", {"keys": "ctrl+l"}),
                ("type", {"text": "https://example.com"}), ("key", {"keys": "Return"}),
                ("wait", {"seconds": 4}), ("scroll", {"x": 640, "y": 400, "direction": "down", "amount": 2})]:
    print(name, a, execute(desk, name, a))
png = desk.screenshot(); open("ex4-smoke.png", "wb").write(png)
print("screenshot bytes:", len(png), "png" if png[:4] == b"\x89PNG" else "NOT PNG")
desk.close()
