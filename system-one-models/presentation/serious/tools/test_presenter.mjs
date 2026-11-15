// Headless end-to-end check of ../present.html: slides load, demo clips play, keys navigate and pause.
//   node test_presenter.mjs [outDir]   (screenshots of each demo slide while playing)
import path from "path"; import fs from "fs"; import { createRequire } from "module";
const here = path.dirname(new URL(import.meta.url).pathname);
const require = createRequire(path.resolve(here, "../../tools") + "/");
const puppeteer = require("puppeteer-core");
const out = process.argv[2] || "/tmp/presenter-test"; fs.mkdirSync(out, { recursive: true });
const browser = await puppeteer.launch({ executablePath: "/usr/bin/google-chrome", headless: "new",
  args: ["--no-sandbox", "--autoplay-policy=no-user-gesture-required", "--allow-file-access-from-files"] });
const page = await browser.newPage(); await page.setViewport({ width: 1600, height: 900 });
const errors = []; page.on("pageerror", (e) => errors.push(e.message)); page.on("requestfailed", (r) => { if (r.failure()?.errorText !== "net::ERR_ABORTED") errors.push("failed " + r.url() + " " + r.failure()?.errorText); }); // ERR_ABORTED = clip switched away
await page.goto("file://" + path.resolve(here, "../present.html") + "#1");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const st = () => page.evaluate(() => { const v = document.getElementById("vid"); return { slide: location.hash, img: document.getElementById("img").src.split("/").pop(),
  imgOk: document.getElementById("img").naturalWidth, video: v.style.display === "block" ? v.src.split("/").pop() : null, paused: v.paused, t: +v.currentTime.toFixed(2), dur: +(v.duration || 0).toFixed(1), ready: v.readyState }; });
let ok = true; const check = (c, msg) => { console.log((c ? "PASS " : "FAIL ") + msg); ok &&= c; };
await sleep(800);
let s = await st(); check(s.imgOk === 1600 && !s.video, `slide 1 shows an image, no video (${s.img})`);
const vids = await page.evaluate("S.map(s => !!s.video)"); const total = vids.length;
const demo = [17, 18, 19];  // demo slides in build_deck.py
for (let k = 1; k < demo[0]; k++) await page.keyboard.press("ArrowRight");
for (const n of demo) {
  await sleep(vids[n - 1] ? 3000 : 600); s = await st();
  if (vids[n - 1]) {
    check(s.slide === `#${n}` && s.video && !s.paused && s.t > 1 && s.ready >= 2, `slide ${n} plays ${s.video} (t=${s.t}s of ${s.dur}s)`);
  } else {
    check(s.slide === `#${n}` && !s.video && s.imgOk === 1600, `slide ${n}: clip not rendered yet, placeholder image shown (${s.img})`);
  }
  await page.screenshot({ path: `${out}/slide-${n}.png` });
  await page.keyboard.press("ArrowRight");
}
await sleep(500); s = await st(); check(s.slide === "#20" && !s.video, `slide 20 has no video (${s.img})`);
await page.keyboard.press("End"); await sleep(300); s = await st(); check(s.slide === `#${total}`, `End goes to the last slide ${total} (${s.img})`);
check(errors.length === 0, "no page errors / failed requests" + (errors.length ? ": " + errors.join("; ") : ""));
await browser.close(); process.exit(ok ? 0 : 1);
