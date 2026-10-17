#!/usr/bin/env python3
"""Copy speaker notes (and sources) from ../talk-script.md into the <aside class="notes"> blocks of index.html.
Run after editing the script: python3 build_notes.py
Same tool as ../../system-one-models/slides/build_notes.py, plus: only "## Slide N — ..." sections are used (the
"Likely audience questions" section at the end of the script is ignored), and each slide's data-time is checked
against the script's timing."""
import html, pathlib, re

here = pathlib.Path(__file__).resolve().parent
script = (here.parent / "talk-script.md").read_text()
deck_path = here / "index.html"
deck = deck_path.read_text()

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    def link(m):
        url = m.group(2)
        if not re.match(r"https?://", url):
            url = "../" + url  # repo-relative paths from the script are relative to the deck's parent folder
        return f'<a href="{url}">{m.group(1)}</a>'
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, t)

notes, times = [], []
for block in re.split(r"^## ", script, flags=re.M)[1:]:
    if not re.match(r"Slide \d+ — ", block):
        continue  # e.g. "Likely audience questions & answers"
    block = block.split("\n---", 1)[0]
    timing = re.search(r"\*\*Timing:\*\* (.+)", block).group(1).strip()
    times.append(timing.split()[0])
    body = block.split("**Speaker notes:**", 1)[1]
    src = ""
    if "**Sources:**" in body:
        body, src = body.split("**Sources:**", 1)
    paras = [p.strip().replace("\n", " ") for p in body.strip().split("\n\n") if p.strip()]
    h = f"<p><i>Timing: {html.escape(timing)}</i></p>" + "".join(f"<p>{inline(p)}</p>" for p in paras)
    if src.strip():
        h += f"<p><b>Sources:</b> {inline(src.strip())}</p>"
    notes.append(h)

asides = list(re.finditer(r'<aside class="notes">.*?</aside>', deck, flags=re.S))
assert len(asides) == len(notes), (len(asides), len(notes))
deck_times = re.findall(r'<section class="slide[^"]*" data-time="([^"]+)"', deck)
for i, (a, b) in enumerate(zip(deck_times, times), 1):
    if a != b:
        print(f"warning: slide {i} data-time {a} != script timing {b}")
out, last = [], 0
for m, n in zip(asides, notes):
    out += [deck[last:m.start()], f'<aside class="notes">{n}</aside>']
    last = m.end()
out.append(deck[last:])
deck_path.write_text("".join(out))
print(f"notes written for {len(notes)} slides")
