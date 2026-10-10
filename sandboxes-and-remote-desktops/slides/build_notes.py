#!/usr/bin/env python3
"""Copy speaker notes (and sources) from ../talk-script.md into the <aside class="notes"> blocks of index.html.
Run after editing the script: python3 build_notes.py"""
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

notes = []
for block in re.split(r"^## Slide \d+ — ", script, flags=re.M)[1:]:
    timing = re.search(r"\*\*Timing:\*\* (.+)", block).group(1).strip()
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
out, last = [], 0
for m, n in zip(asides, notes):
    out += [deck[last:m.start()], f'<aside class="notes">{n}</aside>']
    last = m.end()
out.append(deck[last:])
deck_path.write_text("".join(out))
print(f"notes written for {len(notes)} slides")
