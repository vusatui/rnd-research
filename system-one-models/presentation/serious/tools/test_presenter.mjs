// Headless end-to-end check of ../present.html: slides load, demo clips play, keys navigate and pause.
//   node test_presenter.mjs [outDir]   (screenshots of each demo slide while playing)
import path from "path"; import fs from "fs"; import { createRequire } from "module";
const here = path.dirname(new URL(import.meta.url).pathname);
const require = createRequire(path.resolve(here, "../../tools") + "/");
const puppeteer = require("puppeteer-core");
const out = process.argv[2] || "/tmp/presenter-test"; fs.mkdirSync(out, { recursive: true });
const browser = await puppeteer.launch({ executablePath: "/usr/bin/google-chrome", headless: "new",
  args: ["--no-sandbox", "--autoplay-policy=no-user-gesture-required", "--allow-file-access-from-files", "--disable-background-timer-throttling", "--disable-renderer-backgrounding", "--disable-backgrounding-occluded-windows"] });
const page = await browser.newPage(); await page.setViewport({ width: 1600, height: 900 });
const errors = []; page.on("pageerror", (e) => errors.push(e.message)); page.on("requestfailed", (r) => { if (r.failure()?.errorText !== "net::ERR_ABORTED" && !r.url().startsWith("data:")) errors.push("failed " + r.url() + " " + r.failure()?.errorText); }); // ERR_ABORTED = clip switched away
await page.goto("file://" + path.resolve(here, "../present.html") + "#1");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const st = () => page.evaluate(() => { const v = document.getElementById("vid"); return { slide: location.hash, img: document.getElementById("img").src.split("/").pop(),
  imgOk: document.getElementById("img").naturalWidth, video: v.style.display === "block" ? v.src.split("/").pop() : null, paused: v.paused, t: +v.currentTime.toFixed(2), dur: +(v.duration || 0).toFixed(1), ready: v.readyState }; });
let ok = true; const check = (c, msg) => { console.log((c ? "PASS " : "FAIL ") + msg); ok &&= c; };
await sleep(800);
let s = await st(); check(s.imgOk === 1600 && !s.video, `slide 1 shows an image, no video (${s.img})`);
const vids = await page.evaluate("S.map(s => !!s.video)"); const total = vids.length;
const demo = [17, 18];  // demo slides in build_deck.py
for (let k = 1; k < demo[0]; k++) await page.keyboard.press("ArrowRight");
for (const n of demo) {
  await sleep(900); s = await st();
  if (vids[n - 1]) {
    check(s.slide === `#${n}` && s.video && s.paused && await page.evaluate(() => document.getElementById("vid").controls), `slide ${n}: native player with controls, no autoplay (${s.video})`);
    await page.evaluate(() => document.getElementById("vid").play()); await sleep(2500); s = await st();
    const cur = await page.evaluate(() => document.querySelector("#notes li.cur")?.dataset.t);
    check(!s.paused && s.t > 1 && cur === "0", `slide ${n} plays on demand (t=${s.t}s of ${s.dur}s), notes highlight comment at ${cur}s`);
  } else {
    check(s.slide === `#${n}` && !s.video && s.imgOk === 1600, `slide ${n}: clip not rendered yet, placeholder image shown (${s.img})`);
  }
  await page.screenshot({ path: `${out}/slide-${n}.png` });
  await page.keyboard.press("ArrowRight");
}
await sleep(500); s = await st(); check(s.slide === "#19" && !s.video, `slide 19 has no video (${s.img})`);
await page.keyboard.press("End"); await sleep(300); s = await st(); check(s.slide === `#${total}`, `End goes to the last slide ${total} (${s.img})`);
// ---- presenter + audience sync (two pages, same browser) and ambient sound ----
await page.goto("about:blank");
const P = await browser.newPage(); await P.setViewport({ width: 1600, height: 900 });
const A = await browser.newPage(); await A.setViewport({ width: 1600, height: 900 });
[P, A].forEach((pg) => pg.on("pageerror", (e) => errors.push(e.message)));
const url = "file://" + path.resolve(here, "../present.html");
await P.goto(url + "#1"); await sleep(600); await A.goto(url + "?view=audience#1"); await sleep(900);
const hash = (pg) => pg.evaluate(() => location.hash);
const vs = (pg) => pg.evaluate(() => { const v = document.getElementById("vid"); return { t: +v.currentTime.toFixed(1), paused: v.paused, muted: v.muted }; });
const ui = await A.evaluate(() => ({ notes: getComputedStyle(document.getElementById("notes")).display, hud: getComputedStyle(document.getElementById("hud")).display,
  aud: getComputedStyle(document.getElementById("aud")).display, amb: getComputedStyle(document.getElementById("amb")).display, controls: document.getElementById("vid").controls }));
check(ui.notes === "none" && ui.hud === "none" && ui.aud === "none" && ui.amb === "none" && !ui.controls, `audience view hides notes, HUD, buttons and player controls (${JSON.stringify(ui)})`);
await A.keyboard.press("n"); await sleep(200);
check(await A.evaluate(() => getComputedStyle(document.getElementById("notes")).display) === "none", "N does not open notes in the audience view");
await P.bringToFront(); await P.keyboard.press("ArrowRight"); await P.keyboard.press("ArrowRight"); await sleep(600);
check(await hash(A) === "#3", `presenter → audience slide sync (${await hash(P)} → ${await hash(A)})`);
await A.bringToFront(); await A.keyboard.press("ArrowLeft"); await sleep(600);
check(await hash(P) === "#2", `audience → presenter slide sync, no loop (${await hash(A)} → ${await hash(P)})`);
await P.bringToFront(); await P.evaluate(() => show(16)); await sleep(1200);
check(await hash(A) === "#17" && await A.evaluate(() => document.getElementById("vid").style.display === "block"), "demo slide 17 shows the clip in both windows");
await P.evaluate(() => document.getElementById("notes").style.display = "block");
await P.click('#notes li[data-t="60"]'); await sleep(1800);
let a1 = await vs(A), p1 = await vs(P);
check(!a1.paused && a1.t >= 60 && a1.t < 64 && p1.muted, `note click (1:00) seeks + plays the audience clip (audience t=${a1.t}s playing=${!a1.paused}; presenter muted mirror t=${p1.t}s)`);
await P.keyboard.press("k"); await sleep(700); a1 = await vs(A); p1 = await vs(P);
check(a1.paused && p1.paused && Math.abs(a1.t - p1.t) < 0.6, `K pauses both (audience t=${a1.t}, presenter t=${p1.t})`);
await P.evaluate(() => { const v = document.getElementById("vid"); v.currentTime = 120; }); await sleep(800); a1 = await vs(A);
check(Math.abs(a1.t - 120) < 0.6 && a1.paused, `seek with the presenter's player syncs (audience t=${a1.t})`);
// ambient
let amA = await A.evaluate(() => window.__amb()), amP = await P.evaluate(() => window.__amb());
check(!amA.on && !amP.on && amA.gain === 0, "ambient sound is off by default");
await P.keyboard.press("a"); await sleep(1800); amA = await A.evaluate(() => window.__amb()); amP = await P.evaluate(() => window.__amb());
check(amA.on && amA.audible && amA.target === 0.15 && amP.on && !amP.audible, `A in presenter turns it on in the audience window (audience ${JSON.stringify(amA)}; presenter stays silent: ${JSON.stringify(amP)})`);
await P.keyboard.press("k"); await sleep(1500); amA = await A.evaluate(() => window.__amb());
check(amA.target === 0.04, `ambient ducks while the demo clip plays (${JSON.stringify(amA)})`);
await P.keyboard.press("k"); await sleep(400); await P.keyboard.press("a"); await sleep(1500); amA = await A.evaluate(() => window.__amb());
check(!amA.on && amA.target === 0, `A again turns it off in both (${JSON.stringify(amA)})`);
const shot = (pg, f) => Promise.race([pg.bringToFront().then(() => sleep(300)).then(() => pg.screenshot({ path: `${out}/${f}` })), sleep(20000).then(() => console.log("WARN screenshot timeout " + f))]);
await shot(P, "sync-presenter.png"); await shot(A, "sync-audience.png");
check(errors.length === 0, "no page errors / failed requests" + (errors.length ? ": " + errors.join("; ") : ""));
await browser.close(); process.exit(ok ? 0 : 1);
