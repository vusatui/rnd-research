"""Smoke test for E2B Desktop: boot, open a browser, screenshot, print the live stream URL, kill."""
import sys, time
from dotenv import load_dotenv
from e2b_desktop import Sandbox

load_dotenv()
out = sys.argv[1] if len(sys.argv) > 1 else "e2b-desktop.png"
t0 = time.perf_counter()
desk = Sandbox.create(resolution=(1280, 800), timeout=300)
print(f"desktop ready in {time.perf_counter() - t0:.1f}s, id={desk.sandbox_id}")
try:
    desk.stream.start(require_auth=True)
    key = desk.stream.get_auth_key()
    print("stream URL (view-only):", desk.stream.get_url(auth_key=key, view_only=True))
    desk.open("https://example.com")
    time.sleep(20)  # first browser launch in a fresh VM is slow
    open(out, "wb").write(bytes(desk.screenshot()))
    print("screenshot ->", out)
finally:
    desk.kill()
    print("killed")
