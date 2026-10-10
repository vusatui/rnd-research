"""Cold-start benchmark: E2B code sandbox, E2B Desktop, local Docker (python + ex3 desktop).
Measures create -> first command finished. Every sandbox/container is killed. Usage: python bench_cold_start.py [N]"""
import statistics as st, subprocess, sys, time, urllib.request
from dotenv import load_dotenv

load_dotenv()
N = int(sys.argv[1]) if len(sys.argv) > 1 else 5

def e2b_code():
    from e2b_code_interpreter import Sandbox
    t = time.perf_counter(); s = Sandbox.create(timeout=60)
    try:
        c = time.perf_counter() - t; s.run_code("1+1"); return c, time.perf_counter() - t
    finally: s.kill()

def e2b_desktop():
    from e2b_desktop import Sandbox
    t = time.perf_counter(); s = Sandbox.create(timeout=60)
    try:
        c = time.perf_counter() - t; s.screenshot(); return c, time.perf_counter() - t
    finally: s.kill()

def docker_python():
    t = time.perf_counter()
    p = subprocess.run(["docker", "run", "-d", "--rm", "--network", "none", "python:3.12-slim", "sleep", "60"],
                       capture_output=True, text=True, check=True); cid = p.stdout.strip()
    try:
        c = time.perf_counter() - t
        subprocess.run(["docker", "exec", cid, "python", "-c", "1+1"], check=True); return c, time.perf_counter() - t
    finally: subprocess.run(["docker", "rm", "-f", cid], capture_output=True)

def docker_desktop():
    t = time.perf_counter()
    p = subprocess.run(["docker", "run", "-d", "--rm", "-p", "127.0.0.1:16080:6080", "agent-desktop"],
                       capture_output=True, text=True, check=True); cid = p.stdout.strip()
    try:
        c = time.perf_counter() - t
        while True:  # ready = noVNC answers
            try: urllib.request.urlopen("http://127.0.0.1:16080/vnc.html", timeout=1); break
            except Exception: time.sleep(0.2)
            if time.perf_counter() - t > 120: raise TimeoutError
        return c, time.perf_counter() - t
    finally: subprocess.run(["docker", "rm", "-f", cid], capture_output=True)

def fmt(xs): return f"{st.median(xs):.2f} | {min(xs):.2f} | {max(xs):.2f}"
print("| target | create median | min | max | ready median | min | max |\n|---|---|---|---|---|---|---|")
for name, fn in [("E2B code sandbox", e2b_code), ("E2B Desktop", e2b_desktop),
                 ("Docker python:3.12-slim", docker_python), ("Docker agent-desktop (ex3)", docker_desktop)]:
    r = [fn() for _ in range(N)]
    print(f"| {name} | {fmt([a for a, _ in r])} | {fmt([b for _, b in r])} |", flush=True)
