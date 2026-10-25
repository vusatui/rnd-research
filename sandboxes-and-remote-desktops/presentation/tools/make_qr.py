#!/usr/bin/env python3
"""QR code of the topic folder URL -> ../qr.png   (pip install segno)"""
import os, segno
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
segno.make("https://github.com/vusatui/rnd-research/tree/main/sandboxes-and-remote-desktops/", error="m").save(
    os.path.join(ROOT, "qr.png"), scale=14, border=1, dark="#1c2b4a", light="#ffffff")
