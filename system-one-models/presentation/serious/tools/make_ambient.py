#!/usr/bin/env python3
"""Generate ../audio/ambient.ogg: a soft, seamlessly looping ambient pad (60 s), made from scratch here, so no licensing
questions. Every partial and every LFO completes a whole number of cycles in 60 s, so the end joins the start exactly.
   python3 make_ambient.py   (needs numpy and ffmpeg with libvorbis)"""
import os, subprocess, numpy as np
SR, DUR = 44100, 60
t = np.arange(SR * DUR) / SR
q = lambda f: round(f * DUR) / DUR          # snap a frequency to whole cycles per loop
chords = [[110.0, 164.81, 220.0, 277.18], [98.0, 146.83, 196.0, 246.94]]   # A (add) and G (add): calm, open voicings
x = np.zeros_like(t)
for k, ch in enumerate(chords):
    w = 0.5 - 0.5 * np.cos(2 * np.pi * q(1 / 30) * t + k * np.pi)          # the two chords swap every 30 s, smoothly
    for f in ch:
        for det in (-0.6, 0.6):                                                # slight detune = soft chorus
            ph = np.random.default_rng(int(f * 10 + det * 7)).uniform(0, 2 * np.pi)
            x += w * (np.sin(2 * np.pi * q(f + det) * t + ph) + 0.25 * np.sin(2 * np.pi * q(2 * (f + det)) * t + ph))
x *= 0.75 + 0.25 * np.sin(2 * np.pi * q(1 / 12) * t)                         # slow breathing
x = x / np.abs(x).max() * 0.6
st = np.stack([x, np.roll(x, int(0.012 * SR))], 1)                           # tiny stereo offset (still periodic)
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.makedirs(os.path.join(root, "audio"), exist_ok=True)
raw = (st * 32767).astype("<i2").tobytes()
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "libvorbis", "-q:a", "2",
                os.path.join(root, "audio", "ambient.ogg")], input=raw, check=True)
print("audio/ambient.ogg", os.path.getsize(os.path.join(root, "audio", "ambient.ogg")) // 1024, "KB")
