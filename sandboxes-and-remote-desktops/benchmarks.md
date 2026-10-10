# Cold-start benchmarks

Measured 2026-10-10 from the same Linux box (Istanbul region, home-grade network to E2B's cloud),
5 runs each, with `workshop/bench_cold_start.py`. Times in seconds.

- **create**: API call / `docker run -d` returns.
- **ready**: the sandbox did real work: `run_code("1+1")` (E2B code), first screenshot (E2B Desktop),
  `docker exec python -c 1+1` (Docker), noVNC answering HTTP (ex3 desktop).

| target | create median | min | max | ready median | min | max |
|---|---|---|---|---|---|---|
| E2B code sandbox (Firecracker microVM, cloud) | 0.49 | 0.43 | 0.98 | 1.30 | 0.86 | 1.64 |
| E2B Desktop (microVM + Xfce + VNC, cloud) | 4.99 | 4.89 | 19.04 | 5.98 | 5.92 | 20.19 |
| Docker `python:3.12-slim` (local, `--network none`) | 1.08 | 0.89 | 3.37 | 1.16 | 0.97 | 3.47 |
| Docker `agent-desktop` from ex3 (local, Xvfb + noVNC + Chromium) | 6.80 | 6.05 | 12.57 | 7.22 | 6.46 | 12.99 |

## Takeaways

- A remote E2B microVM including the network round trip is **as fast as or faster than a local Docker container** on
  this box: snapshot-restored microVMs beat container setup (overlayfs, network namespace, cgroups).
- Desktops cost ~5-7 s either way; the first run in each series was the slow outlier (cold template cache / image
  layers), so pre-warm before a live demo.
- Ready != usable for a browser agent: launching Firefox inside a fresh E2B Desktop took another ~10-20 s
  (the smoke test waits 20 s before its screenshot).
- Vendor claims (~150-200 ms boot) measure the VM restore only; what your agent feels is create + API + first command.

## Other runs on the same day

| run | result |
|---|---|
| ex1 (`ex1_e2b_code/main.py`, real E2B) | OK, ~6 s end to end |
| ex2 (`ex2_llm_loop/agent.py`, E2B backend, `nvidia/nemotron-3-super-120b-a12b:free`) | correct t-test answer, ~11.5 s |
| E2B Desktop smoke test (`ex4_computer_use/e2b_desktop_smoke.py`) | desktop ready in ~8 s, screenshot `assets/e2b-desktop.png` |
| ex4 (`DESKTOP_BACKEND=e2b`, task: "open example.com, read the heading") | correct ("Example Domain") in 13 steps, ~2 min (free model is the bottleneck) |
