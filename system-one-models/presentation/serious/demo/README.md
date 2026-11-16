# Recorded demo for the serious deck (slides 17–18)

Two short, silent clips (2560×1440, H.264, no audio, slowed to half speed so the screen text can be read) that the speaker talks over, one per exercise, each in the same arc: problem → design → why → key code (eased zooms) → run & result → alternatives. Plan and timing: [`STORYBOARD.md`](STORYBOARD.md); narration: slides 17–18 in [`../speaker-notes.md`](../speaker-notes.md).

| Clip | Length | Shows |
|---|---|---|
| [`videos/demo-1-one-call.mp4`](videos/demo-1-one-call.mp4) | 4:04 | `jev_client.py`: one request with several questions to **real Jev via OpenRouter**, thresholds per action in code; `make -s lite-jev` for a ticket, a comment and an expense |
| [`videos/demo-2-same-tickets.mp4`](videos/demo-2-same-tickets.mp4) | 3:34 | `ex2_confidence/methods.py`: written confidence, token logprobs, votes, Jev; `make -s eval` (and `QUESTION=urgency`) re-scoring the saved results: table, reliability |

## What is real, and how it is made
The clips are **not screen captures**. They are rendered with a local video tool (not included in this repo) from:
- the **real files** of this repo, read at build time and syntax-highlighted (`capture/build_data.py`);
- **real runs** of the demo commands, recorded line by line with timestamps by `capture/capture.py` into [`runs/`](runs/) (Docker + make). The replay types the command and prints the recorded lines at their recorded times; waits over 1 s between lines (Docker start-up) are shortened, and the absolute repo path is shown as `~/rnd-research`. A real-Jev run whose answers did not all come from `typesafe/jev-*` is rejected and re-recorded, and the capture aborts if a secret ever appears in the output.
- Captions, concept cards and comparison cards that quote numbers read them from `runs/*.json`; nothing is typed in by hand.

Demo 1 calls real Jev (`make lite-jev`, needs `OPENROUTER_API_KEY`; about $0.00005 per run). A new capture can give slightly different probabilities; if you re-record, re-read the speaker notes for slide 17. The emulator (`make lite`) is **not Jev** and is not used in the new clips.

## Re-recording the runs
```bash
cd system-one-models/presentation/serious/demo
python3 capture/capture.py   # real runs -> runs/*.json (needs Docker, make; OPENROUTER_API_KEY in system-one-models/.env for the 3 real-Jev runs, ~$0.00005)
```
The clips were rendered at normal speed and then slowed to 0.5× with `ffmpeg -i in.mp4 -an -vf "setpts=2.0*PTS" -r 30 -c:v libx264 -crf 18 -preset slow out.mp4` (2026-11-16). Only the rendered mp4 files in `videos/` are needed to present: open `../present.html` in Chrome.
