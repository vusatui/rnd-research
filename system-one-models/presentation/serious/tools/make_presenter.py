#!/usr/bin/env python3
"""Write ../present.html: an offline presenter for the exported slides that plays the recorded demo
clips inside the demo slides. Open it in Chrome (double-click; works from file://, no server, no network).

Keys: → / Space / PageDown next · ← / PageUp previous · Home/End · F fullscreen · N speaker notes
Slides build in (elements fade in top to bottom, from the inline SVG export). Demo slides have a native
<video controls> player (no autoplay): click it to focus, then Space / ← → work on the video; Esc gives the keys back
to the slides. Without focus: K / Enter = play/pause, R = restart, [ ] = speed. Notes (N) show timestamped comments
for the demos; the current one is highlighted while the clip plays, click one to seek.
   python3 make_presenter.py   (after node export_frames.mjs)"""
import glob, html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
VIDEO_BOX = (176, 150, 1248, 702)            # same box as build_deck.py
DEMOS = {"demo-1": "demo-1-one-call", "demo-2": "demo-2-same-tickets"}  # same names as build_deck.py

pngs = sorted(glob.glob(os.path.join(ROOT, "export", "slide-*.png")))
notes_md = open(os.path.join(ROOT, "speaker-notes.md")).read()
notes = {}
for m in re.finditer(r"^## Slide (\d+) · (.+?)\n(.*?)(?=^## |^---|\Z)", notes_md, re.S | re.M):
    body = html.escape(m.group(3).strip())
    body = re.sub(r"\*\[(.+?)\]\*", r"<em>[\1]</em>", body)
    parts = []
    for p in body.split("\n\n"):
        items = re.findall(r"^- \*\*(\d+):(\d+)\*\* — (.+)$", p, re.M)
        if items:  # timestamped demo comments: highlighted while the clip plays, click = seek
            parts.append("<ol class=ts>" + "".join(f'<li data-t="{int(a) * 60 + int(b)}"><b>{a}:{b}</b> {t}</li>' for a, b, t in items) + "</ol>")
        else:
            parts.append(f"<p>{p}</p>")
    notes[int(m.group(1))] = f"<h3>Slide {m.group(1)} · {html.escape(m.group(2))}</h3>" + "".join(parts)

slides = []
for p in pngs:
    name = os.path.basename(p)
    n = int(name.split("-")[1])
    vid = next((v for k, v in DEMOS.items() if f"-{k}-" in name), None)
    if vid and not os.path.exists(os.path.join(ROOT, "demo", "videos", f"{vid}.mp4")):
        vid = None  # clip not rendered yet: the slide shows its placeholder
    svg = open(p[:-4] + ".svg").read() if os.path.exists(p[:-4] + ".svg") else ""
    slides.append({"svg": svg, "img": f"export/{name}", "video": f"demo/videos/{vid}.mp4" if vid else None,
                   "poster": f"demo/videos/{vid}.poster.jpg" if vid else None, "notes": notes.get(n, "")})

x, y, w, h = VIDEO_BOX
page = """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>System One models · presenter</title>
<style>
html,body{margin:0;height:100%;background:#0e1628;overflow:hidden;font-family:system-ui,sans-serif}
#stage{position:absolute;left:50%;top:50%;width:1600px;height:900px;transform-origin:0 0;background:#fff}
#stage img.slide{position:absolute;inset:0;width:1600px;height:900px}
#stage video{position:absolute;left:XPX;top:YPX;width:WPX;height:HPX;background:#000;display:none}
#svg{position:absolute;inset:0;width:1600px;height:900px;background:#fff}#svg svg{width:1600px;height:900px;display:block}
@keyframes bi{from{opacity:0}to{opacity:1}}
.bi{opacity:0;animation:bi .5s ease-out forwards}
#notes ol.ts{list-style:none;padding:0;margin:6px 0}#notes ol.ts li{padding:4px 10px;border-left:4px solid transparent;cursor:pointer;opacity:.75}
#notes ol.ts li b{font:600 15px monospace;color:#e8590c;margin-right:8px}#notes ol.ts li.cur{opacity:1;background:rgba(232,89,12,.18);border-left-color:#e8590c}
#hud{position:fixed;right:14px;bottom:10px;color:#8b9cb5;font:13px monospace;opacity:.0;transition:opacity .3s}
body:hover #hud{opacity:.8}
#notes{position:fixed;left:0;right:0;bottom:0;max-height:38vh;overflow:auto;background:rgba(14,22,40,.96);color:#e8edf4;
  font:20px/1.5 Georgia,serif;padding:12px 28px;display:none;border-top:3px solid #e8590c}
#notes h3{font:600 15px system-ui;color:#e8590c;margin:6px 0}
#bar{position:absolute;left:XPX;top:BARPX;width:WPX;height:5px;background:#e8edf4;display:none}
#bar div{height:5px;background:#e8590c;width:0}
</style></head><body>
<div id="stage"><img class="slide" id="img" alt=""><div id="svg"></div><video id="vid" controls playsinline preload="auto"></video><div id="bar"><div id="prog"></div></div></div>
<div id="notes"></div><div id="hud"></div>
<script>
const S = SLIDES;
let i = 0, rates = [0.75, 1, 1.25], ri = 1;
const img = document.getElementById("img"), vid = document.getElementById("vid"), notes = document.getElementById("notes"),
      hud = document.getElementById("hud"), stage = document.getElementById("stage"), bar = document.getElementById("bar"), prog = document.getElementById("prog");
S.forEach(s => { const p = new Image(); p.src = s.img; });
function fit() { const k = Math.min(innerWidth / 1600, innerHeight / 900); stage.style.transform = `scale(${k}) translate(-50%,-50%)`; }
function show(n) {
  i = Math.max(0, Math.min(S.length - 1, n)); const s = S[i];
  img.src = s.img; notes.innerHTML = s.notes; vid.pause(); vid.blur(); build(s);
  notes.querySelectorAll("li[data-t]").forEach(li => li.onclick = () => { vid.currentTime = +li.dataset.t; vid.play(); });
  if (s.video) { vid.src = s.video; vid.poster = s.poster; vid.playbackRate = rates[ri]; vid.style.display = "block"; vid.currentTime = 0; }  // no autoplay: native controls
  else { vid.removeAttribute("src"); vid.load(); vid.style.display = "none"; }
  location.hash = i + 1; status();
}
const svgBox = document.getElementById("svg");
function build(s) {  // build-in: the slide's elements fade/slide in, top to bottom
  if (!s.svg) { svgBox.innerHTML = ""; return; }
  svgBox.innerHTML = s.svg; const root = svgBox.querySelector("svg"); if (!root) return;
  const els = [...root.children].filter(e => e.tagName !== "defs" && e.tagName !== "metadata" && e.tagName !== "style");
  const ys = els.map(e => { try { const b = e.getBoundingClientRect(); return b.top * 3 + b.left * 0.2; } catch (_) { return 0; } });
  const order = els.map((e, k) => k).sort((a, b) => ys[a] - ys[b]); const step = Math.min(60, 1100 / Math.max(1, els.length));
  order.forEach((k, r) => { const e = els[k]; e.classList.remove("bi"); e.style.animationDelay = (r * step) + "ms"; void e.getBBox; e.classList.add("bi"); });
}
function status() { hud.textContent = `${i + 1}/${S.length}` + (S[i].video ? `  ·  ${vid.paused ? "paused" : "playing"} ${rates[ri]}x  ·  K pause  R restart  [ ] speed` : "") + "  ·  N notes  F fullscreen"; }
function toggle() { if (!S[i].video) return; vid.paused ? vid.play() : vid.pause(); status(); }
vid.addEventListener("timeupdate", () => {  // highlight the current timestamped comment
  const li = [...notes.querySelectorAll("li[data-t]")]; let cur = null; li.forEach(x => { if (+x.dataset.t <= vid.currentTime + 0.2) cur = x; });
  li.forEach(x => x.classList.toggle("cur", x === cur)); if (cur && notes.style.display === "block") cur.scrollIntoView({ block: "nearest" });
});
["play", "pause", "ended"].forEach(ev => vid.addEventListener(ev, status));
addEventListener("keydown", e => {
  const k = e.key;
  // video focused (clicked): Space / arrows / K control the player natively; Esc returns keys to the slides
  if (document.activeElement === vid) { if (k === "Escape") vid.blur(); else if ([" ", "ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "k", "K"].includes(k)) { if (k === "k" || k === "K") { e.preventDefault(); toggle(); } return; } }
  if (["ArrowRight", "PageDown", " "].includes(k)) { e.preventDefault(); show(i + 1); }
  else if (["ArrowLeft", "PageUp", "Backspace"].includes(k)) { e.preventDefault(); show(i - 1); }
  else if (k === "Home") show(0); else if (k === "End") show(S.length - 1);
  else if (["k", "K", "Enter", ".", "b", "B"].includes(k)) { e.preventDefault(); toggle(); }
  else if (k === "r" || k === "R") { vid.currentTime = 0; vid.play(); }
  else if (k === "[" || k === "]") { ri = Math.max(0, Math.min(2, ri + (k === "]" ? 1 : -1))); vid.playbackRate = rates[ri]; status(); }
  else if (k === "n" || k === "N") notes.style.display = notes.style.display === "block" ? "none" : "block";
  else if (k === "f" || k === "F") document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
});
addEventListener("resize", fit); fit();
show((parseInt(location.hash.slice(1)) || 1) - 1);
</script></body></html>"""
page = (page.replace("SLIDES", json.dumps(slides)).replace("XPX", f"{x}px").replace("YPX", f"{y}px").replace("WPX", f"{w}px")
        .replace("HPX", f"{h}px").replace("BARPX", f"{y + h + 8}px"))
open(os.path.join(ROOT, "present.html"), "w").write(page)
print("present.html:", len(slides), "slides,", sum(1 for s in slides if s["video"]), "with video")
