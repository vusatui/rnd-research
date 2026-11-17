#!/usr/bin/env python3
"""Write ../present.html: an offline presenter for the exported slides that plays the recorded demo
clips inside the demo slides. Open it in Chrome (double-click; works from file://, no server, no network).

Keys: → / Space / PageDown next · ← / PageUp previous · Home/End · F fullscreen · N speaker notes
Slides build in (elements fade in top to bottom, from the inline SVG export). Demo slides have a native
<video controls> player (no autoplay): click it to focus, then Space / ← → work on the video; Esc gives the keys back
to the slides. Without focus: K / Enter = play/pause, R = restart, [ ] = speed. Notes (N) show timestamped comments
for the demos; the current one is highlighted while the clip plays, click one to seek.
   python3 make_presenter.py   (after node export_frames.mjs)"""
import base64, glob, html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
VIDEO_BOX = (176, 150, 1248, 702)            # same box as build_deck.py
DEMOS = {"demo-1": "demo-1-one-call", "demo-2": "demo-2-same-tickets"}  # same names as build_deck.py

pngs = sorted(glob.glob(os.path.join(ROOT, "export", "slide-*.png")))
notes_md = open(os.path.join(ROOT, "speaker-notes.md")).read()
# sentence end = . ? ! (optionally followed by a closing quote/bracket) + space + a capital, digit, quote or stage direction;
# decimals ("0.16 s") and "e.g." never match because they aren't followed by space + capital
SENT = re.compile(r"(?<=[.?!])(?:(?<=[^A-Z]\.)|(?<=[?!]))\s+(?=[A-Z0-9\"“(&<])|(?<=</em>)\s+")
notes = {}
for m in re.finditer(r"^## Slide (\d+) · (.+?)\n(.*?)(?=^## |^---|\Z)", notes_md, re.S | re.M):
    body = html.escape(m.group(3).strip())
    body = re.sub(r"\*\[(.+?)\]\*", r"<em>[\1]</em>", body)
    parts = []
    for p in body.split("\n\n"):
        items = re.findall(r"^- \*\*(\d+):(\d+)\*\* — (.+)$", p, re.M)
        if items:  # timestamped demo comments: highlighted while the clip plays, click = seek
            parts.append("<ol class=ts>" + "".join(f'<li data-t="{int(a) * 60 + int(b)}"><b>{a}:{b}</b> {t}</li>' for a, b, t in items) + "</ol>")
        else:  # prose: one sentence per line, small gap between lines, bigger gap between paragraphs
            sents = [x.strip() for x in SENT.split(" ".join(p.split())) if x.strip()]
            parts.append("<ul class=ph>" + "".join(f"<li>{x}</li>" for x in sents) + "</ul>")
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

amb_path = os.path.join(ROOT, "audio", "ambient.ogg")   # made by make_ambient.py; embedded so the loop is gapless via Web Audio, also from file://
AMBIENT = "data:audio/ogg;base64," + base64.b64encode(open(amb_path, "rb").read()).decode() if os.path.exists(amb_path) else ""
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
#notes ul.ph{list-style:none;padding:0;margin:0 0 18px}#notes ul.ph li{margin:0 0 8px;padding-left:10px;border-left:3px solid rgba(139,156,181,.35)}
#notes h3{font:600 15px system-ui;color:#e8590c;margin:6px 0}
#aud{position:fixed;right:14px;top:10px;font:13px system-ui;color:#e8edf4;background:#e8590c;border:0;border-radius:6px;padding:6px 10px;cursor:pointer;opacity:.25;transition:opacity .3s}
#aud:hover,#amb:hover{opacity:1}
#amb{position:fixed;right:190px;top:10px;font:13px system-ui;color:#e8edf4;background:#1c2b4a;border:1px solid #5b6b82;border-radius:6px;padding:6px 10px;cursor:pointer;opacity:.25;transition:opacity .3s}
body.audience #notes,body.audience #hud,body.audience #aud,body.audience #amb{display:none!important}
body.audience{cursor:none}
</style></head><body>
<div id="stage"><img class="slide" id="img" alt=""><div id="svg"></div><video id="vid" controls playsinline preload="auto"></video></div>
<div id="notes"></div><div id="hud"></div><button id="aud" title="P: open the audience window">audience window (P)</button><button id="amb" title="A: ambient sound on/off">♪ off (A)</button>
<script>
const S = SLIDES;
const AUDIENCE = new URLSearchParams(location.search).get("view") === "audience";
if (AUDIENCE) { document.body.classList.add("audience"); document.title = "System One models"; }
let i = 0, rates = [0.75, 1, 1.25], ri = 1, peer = false;
const img = document.getElementById("img"), vid = document.getElementById("vid"), notes = document.getElementById("notes"),
      hud = document.getElementById("hud"), stage = document.getElementById("stage");
if (AUDIENCE) vid.removeAttribute("controls");
S.forEach(s => { const p = new Image(); p.src = s.img; });
// ---- sync between the presenter window and the audience window (BroadcastChannel, localStorage fallback) ----
// Every message is applied idempotently (only if the state differs), so echoes die out and nothing loops.
const ME = Math.random().toString(36).slice(2);
let bc = null; try { bc = new BroadcastChannel("system-one-deck"); bc.onmessage = (e) => recv(e.data); } catch (_) {}
addEventListener("storage", (e) => { if (e.key === "system-one-deck" && e.newValue) { try { recv(JSON.parse(e.newValue)); } catch (_) {} } });
function send(m) { m.from = ME; m.n = Date.now() + Math.random(); if (bc) bc.postMessage(m); try { localStorage.setItem("system-one-deck", JSON.stringify(m)); } catch (_) {} }
let seen = new Set();
function recv(m) {
  if (!m || m.from === ME || seen.has(m.n)) return; seen.add(m.n);
  if (m.type === "hello") { peer = true; if (!AUDIENCE) { vid.muted = true; send({ type: "slide", i }); send({ type: "amb", on: ambOn }); if (S[i].video) send({ type: "video", t: vid.currentTime, paused: vid.paused }); } ambApply(); status(); return; }
  if (m.type === "amb") { peer = true; if (m.on !== ambOn) ambSet(m.on, true); else ambApply(); return; }
  if (m.type === "slide") { peer = true; if (m.i !== i) show(m.i, true); return; }
  if (m.type === "video" && S[i].video) {
    if (Math.abs(vid.currentTime - m.t) > 0.4) vid.currentTime = m.t;
    if (m.paused && !vid.paused) vid.pause(); else if (!m.paused && vid.paused) vid.play().catch(() => {});
  }
}
function vstate() { if (S[i].video) send({ type: "video", t: vid.currentTime, paused: vid.paused }); }
["play", "pause", "seeked"].forEach(ev => vid.addEventListener(ev, vstate));
// ---- ambient sound: off by default, quiet, gapless loop; plays in the audience window (or here if none is linked); ducks during demo clips ----
const AMB_SRC = "AMBIENT_DATA", VOL = 0.15, DUCK = 0.04;
let ambOn = false, actx = null, gain = null, srcNode = null, ambBuf = null;
async function ambEnsure() {
  if (!AMB_SRC) return false;
  if (!actx) { actx = new (window.AudioContext || window.webkitAudioContext)(); gain = actx.createGain(); gain.gain.value = 0; gain.connect(actx.destination);
    const b64 = AMB_SRC.split(",")[1], bin = atob(b64), u8 = new Uint8Array(bin.length); for (let k = 0; k < bin.length; k++) u8[k] = bin.charCodeAt(k);
    ambBuf = await actx.decodeAudioData(u8.buffer); }
  if (actx.state === "suspended") { try { await actx.resume(); } catch (_) {} }
  if (!srcNode) { srcNode = actx.createBufferSource(); srcNode.buffer = ambBuf; srcNode.loop = true; srcNode.connect(gain); srcNode.start(); }
  return true;
}
function ambAudible() { return ambOn && (AUDIENCE || !peer); }
async function ambApply() {
  const target = ambAudible() ? (vid.paused ? VOL : DUCK) : 0;
  if (target > 0) await ambEnsure();
  if (gain) gain.gain.setTargetAtTime(target, actx.currentTime, 0.4);
  document.getElementById("amb").textContent = ambOn ? "♪ on (A)" : "♪ off (A)"; status();
}
function ambSet(on, remote) { ambOn = on; ambApply(); if (!remote) send({ type: "amb", on }); }
["play", "pause", "ended"].forEach(ev => vid.addEventListener(ev, ambApply));
["pointerdown", "keydown"].forEach(ev => addEventListener(ev, () => { if (actx && actx.state === "suspended") actx.resume(); if (ambAudible()) ambApply(); }));
document.getElementById("amb").onclick = () => ambSet(!ambOn);
window.__amb = () => ({ on: ambOn, audible: ambAudible(), gain: gain ? +gain.gain.value.toFixed(3) : 0, target: ambAudible() ? (vid.paused ? VOL : DUCK) : 0, ctx: actx ? actx.state : "none" });
function openAudience() { window.open(location.pathname + "?view=audience#" + (i + 1), "system-one-audience", "popup,width=1280,height=720"); }
document.getElementById("aud").onclick = openAudience;
// ---------------------------------------------------------------------------------------------------------
function fit() { const k = Math.min(innerWidth / 1600, innerHeight / 900); stage.style.transform = `scale(${k}) translate(-50%,-50%)`; }
function show(n, remote) {
  n = Math.max(0, Math.min(S.length - 1, n)); const changed = n !== i || !img.src; i = n; const s = S[i];
  img.src = s.img; notes.innerHTML = AUDIENCE ? "" : s.notes; vid.pause(); vid.blur(); build(s);
  notes.querySelectorAll("li[data-t]").forEach(li => li.onclick = () => { vid.currentTime = +li.dataset.t; vid.play().catch(() => {}); });
  if (s.video) { vid.src = s.video; vid.poster = s.poster; vid.playbackRate = rates[ri]; vid.style.display = "block"; vid.currentTime = 0; }  // no autoplay
  else { vid.removeAttribute("src"); vid.load(); vid.style.display = "none"; }
  history.replaceState(null, "", "#" + (i + 1)); status();
  if (!remote) send({ type: "slide", i });
}
const svgBox = document.getElementById("svg");
function build(s) {  // build-in: the slide's elements fade in, top to bottom
  if (!s.svg) { svgBox.innerHTML = ""; return; }
  svgBox.innerHTML = s.svg; const root = svgBox.querySelector("svg"); if (!root) return;
  const els = [...root.children].filter(e => e.tagName !== "defs" && e.tagName !== "metadata" && e.tagName !== "style");
  const ys = els.map(e => { try { const b = e.getBoundingClientRect(); return b.top * 3 + b.left * 0.2; } catch (_) { return 0; } });
  const order = els.map((e, k) => k).sort((a, b) => ys[a] - ys[b]); const step = Math.min(60, 1100 / Math.max(1, els.length));
  order.forEach((k, r) => { const e = els[k]; e.classList.remove("bi"); e.style.animationDelay = (r * step) + "ms"; void e.getBBox; e.classList.add("bi"); });
}
function status() { if (AUDIENCE) return; hud.textContent = `${i + 1}/${S.length}` + (S[i].video ? `  ·  ${vid.paused ? "paused" : "playing"} ${rates[ri]}x  ·  K pause  R restart  [ ] speed` : "") + `  ·  N notes  F fullscreen  P audience window${peer ? " (linked)" : ""}  A ambient ${ambOn ? "on" : "off"}`; }
function toggle() { if (!S[i].video) return; vid.paused ? vid.play().catch(() => {}) : vid.pause(); status(); }
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
  else if (k === "r" || k === "R") { vid.currentTime = 0; vid.play().catch(() => {}); }
  else if (k === "[" || k === "]") { ri = Math.max(0, Math.min(2, ri + (k === "]" ? 1 : -1))); vid.playbackRate = rates[ri]; status(); }
  else if (!AUDIENCE && (k === "n" || k === "N")) notes.style.display = notes.style.display === "block" ? "none" : "block";
  else if (!AUDIENCE && (k === "p" || k === "P")) openAudience();
  else if (k === "a" || k === "A") ambSet(!ambOn);
  else if (k === "f" || k === "F") document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
});
addEventListener("resize", fit); fit();
i = -1; show((parseInt(location.hash.slice(1)) || 1) - 1, AUDIENCE);
send({ type: "hello" });
</script></body></html>"""
# layout placeholders first, data last (base64 payloads must never be touched by a later replace)
page = page.replace("XPX", f"{x}px").replace("YPX", f"{y}px").replace("WPX", f"{w}px").replace("HPX", f"{h}px")
page = page.replace("const S = SLIDES;", "const S = " + json.dumps(slides) + ";", 1).replace('"AMBIENT_DATA"', json.dumps(AMBIENT), 1)
open(os.path.join(ROOT, "present.html"), "w").write(page)
print("present.html:", len(slides), "slides,", sum(1 for s in slides if s["video"]), "with video")
