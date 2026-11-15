# Recorded demo for the serious deck (slides 14–17)

Four short, silent clips that the speaker talks over, in a Screen Studio style: the whole editor first, then eased zooms into the code being discussed, the command typed at the prompt, the output, and side-by-side comparisons.

| Clip | Shows |
|---|---|
| [`videos/demo-1-files.mp4`](videos/demo-1-files.mp4) | the `workshop-lite/` folder: emulator, client, mock rules, Makefile |
| [`videos/demo-2-code.mp4`](videos/demo-2-code.mp4) | `jev_client.py`: the one HTTP call, state, questions, the 0.7 threshold; how the emulator turns votes into "probabilities" |
| [`videos/demo-3-run.mp4`](videos/demo-3-run.mp4) | `make help`, then `make -s lite EX=ticket|comment|approval` with the real output, and a ticket-vs-comment comparison |
| [`videos/demo-4-threshold.mp4`](videos/demo-4-threshold.mp4) | deep-dive exercise 3: the confidence gate in `cascade.py` and `make -s ex3-sweep` across four thresholds |

## What is real, and how it is made
The clips are **not screen captures**. They are rendered with a local video tool (not included in this repo) from:
- the **real files** of this repo, read at build time and syntax-highlighted (`capture/build_data.py`);
- **real runs** of the demo commands, recorded line by line with timestamps by `capture/capture.py` into [`runs/`](runs/) (Docker + make, the free OpenRouter model behind the emulator). The replay types the command and prints the recorded lines at their recorded times. The only change is that the absolute repo path is shown as `~/rnd-research`. A run that used the offline MOCK fallback is rejected and re-recorded, and the capture aborts if a secret ever appears in the output.
- Captions and comparison cards that quote numbers read them from `runs/*.json`; nothing is typed in by hand.

The emulator is **not Jev**: its "probabilities" are vote shares of 5 calls to a free model, and every response says `EMULATOR`. A new capture can give different numbers (a borderline comment can flip between `review` and `block`); if you re-record, re-read the speaker notes for slides 16 and 17.

## Re-recording the runs
```bash
cd system-one-models/presentation/serious/demo
python3 capture/capture.py   # real runs -> runs/*.json (needs Docker, make, a free OPENROUTER_API_KEY in system-one-models/.env)
```
Only the rendered mp4 files in `videos/` are needed to present: open `../present.html` in Chrome.
