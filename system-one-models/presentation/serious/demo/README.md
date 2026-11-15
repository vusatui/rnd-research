# Recorded demo for the serious deck (slides 17–19)

> **Status (2026-11-15):** the clips are being **re-recorded**. The new plan is in [`STORYBOARD.md`](STORYBOARD.md) (3 clips: one call with real Jev, same tickets comparison, the threshold); nothing is rendered yet, so slides 17–19 show a placeholder. The real runs behind them are already saved: [`runs/ex1-real-jev.txt`](runs/ex1-real-jev.txt) and [`runs/ex2-ex3-results.txt`](runs/ex2-ex3-results.txt).
>
> The four old clips in `videos/` (`demo-1-files` … `demo-4-threshold`, emulator-based) are obsolete and no longer used by `present.html`.

| New clip (planned) | Shows |
|---|---|
| `videos/demo-1-one-call.mp4` | `jev_client.py`: one request with several questions to real Jev via OpenRouter, the code thresholds, `make lite-jev` |
| `videos/demo-2-same-tickets.mp4` | `ex2_confidence/methods.py` + `eval.py`: written vs computed confidence on the same 150 tickets, `make workshop` |
| `videos/demo-3-threshold.mp4` | `ex3_fast_first/economics.py`: threshold sweep with error/review prices, `make ex3` |

## What is real, and how it is made
The clips are **not screen captures**. They are rendered with a local video tool (not included in this repo) from:
- the **real files** of this repo, read at build time and syntax-highlighted (`capture/build_data.py`);
- **real runs** of the demo commands, recorded line by line with timestamps by `capture/capture.py` into [`runs/`](runs/) (Docker + make). The replay types the command and prints the recorded lines at their recorded times. The only change is that the absolute repo path is shown as `~/rnd-research`. A run that used the offline MOCK fallback is rejected and re-recorded, and the capture aborts if a secret ever appears in the output.
- Captions and comparison cards that quote numbers read them from `runs/*.json`; nothing is typed in by hand.

Demo 1 calls real Jev (`make lite-jev`, needs `OPENROUTER_API_KEY`; about $0.00005 per run). A new capture can give slightly different probabilities; if you re-record, re-read the speaker notes for slide 17. The emulator (`make lite`) is **not Jev** and is not used in the new clips.

## Re-recording the runs
```bash
cd system-one-models/presentation/serious/demo
python3 capture/capture.py   # real runs -> runs/*.json (needs Docker, make, OPENROUTER_API_KEY in system-one-models/.env); capture targets get updated to the STORYBOARD before re-recording
```
Only the rendered mp4 files in `videos/` are needed to present: open `../present.html` in Chrome.
