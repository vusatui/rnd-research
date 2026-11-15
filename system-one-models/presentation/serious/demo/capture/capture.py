#!/usr/bin/env python3
"""Record REAL runs of the demo commands for the demo videos (no screen recording needed).

Runs each command in system-one-models/ exactly as a participant would (Docker + make), and stores
every output line with the time it appeared, the exit code and the wall-clock date in ../runs/<id>.json.
The Remotion composition in ../remotion replays these files verbatim (typing the command, then
printing the lines with the recorded timing, long waits capped). Nothing is edited except:
  * the absolute repo path is shown as ~/rnd-research (privacy, shorter lines),
  * if a secret from the environment ever appears in the output, the capture aborts.
For `make lite` runs the capture is repeated (up to 3x) if any answer came from the MOCK fallback,
so the videos show the free LLM behind the emulator, never the offline keyword rules.

   python3 capture.py            # all runs
   python3 capture.py lite-ticket ex3-sweep
"""
import datetime, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
S1 = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))          # system-one-models/
REPO = os.path.dirname(S1)
OUT = os.path.join(HERE, "..", "runs")

RUNS = {
    "make-help":     "make -s help",
    "lite-ticket":   "make -s lite EX=ticket",
    "lite-comment":  "make -s lite EX=comment",
    "lite-approval": "make -s lite EX=approval",
    "ex3-sweep":     "make -s ex3-sweep",
}
SECRETS = [v for k, v in os.environ.items() if any(s in k for s in ("KEY", "TOKEN", "SECRET")) and len(v) >= 12]


def run(cmd):
    started = datetime.datetime.now().astimezone()
    t0 = time.perf_counter()
    p = subprocess.Popen(cmd, shell=True, cwd=S1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, bufsize=1, env={**os.environ, "PYTHONUNBUFFERED": "1"})
    lines = []
    for ln in p.stdout:
        lines.append({"t": round((time.perf_counter() - t0) * 1000), "text": ln.rstrip("\n").replace(REPO, "~/rnd-research")})
    code = p.wait()
    for ln in lines:
        if any(s in ln["text"] for s in SECRETS):
            sys.exit(f"ABORT: a secret appeared in the output of {cmd!r}; nothing written")
    return {"cmd": cmd, "cwd": "~/rnd-research/system-one-models", "started_at": started.isoformat(timespec="seconds"),
            "duration_ms": round((time.perf_counter() - t0) * 1000), "exit_code": code, "lines": lines}


def main():
    os.makedirs(OUT, exist_ok=True)
    subprocess.run("make -s image", shell=True, cwd=S1, check=True)   # warm image so no build output is captured
    for rid in sys.argv[1:] or RUNS:
        for attempt in range(3):
            r = run(RUNS[rid])
            mock = any("MOCK" in l["text"] for l in r["lines"] if l["text"].startswith("BACKEND"))
            if r["exit_code"] == 0 and not (rid.startswith("lite") and mock):
                break
            print(f"{rid}: attempt {attempt + 1} not usable (exit {r['exit_code']}, mock={mock}); retrying", file=sys.stderr)
            time.sleep(5)
        else:
            sys.exit(f"{rid}: no clean real run after 3 attempts")
        json.dump(r, open(os.path.join(OUT, f"{rid}.json"), "w"), indent=1)
        print(f"{rid}: {len(r['lines'])} lines, {r['duration_ms']} ms, exit {r['exit_code']}")


if __name__ == "__main__":
    main()
