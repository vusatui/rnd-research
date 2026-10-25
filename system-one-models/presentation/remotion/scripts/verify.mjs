// Headless check of the presenter: screenshots every build step of every slide, checks that clicking through
// (animated playback) lands exactly on the same frames, and builds contact-sheet.png from the final states.
//   npm run dev  (or npm run preview)  then  npm run verify [-- http://localhost:5173/]
// Chrome: CHROME_PATH=/path/to/chrome (default /usr/bin/google-chrome)
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import puppeteer from "puppeteer-core";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const url = process.argv[2] ?? "http://localhost:5173/";
const shots = path.join(root, "verify", "shots");
fs.mkdirSync(shots, { recursive: true });

const browser = await puppeteer.launch({
  executablePath: process.env.CHROME_PATH ?? "/usr/bin/google-chrome",
  headless: true,
  args: ["--no-sandbox", "--hide-scrollbars", "--force-device-scale-factor=1"],
  defaultViewport: { width: 1920, height: 1080 },
});
const page = await browser.newPage();
const errors = [];
page.on("console", (m) => (m.type() === "error" || m.type() === "warning") && errors.push(m.text()));
page.on("pageerror", (e) => errors.push(String(e)));
await page.goto(url, { waitUntil: "networkidle0" });
await page.waitForFunction(() => window.__deck, { timeout: 20000 });
await new Promise((r) => setTimeout(r, 800));
const steps = await page.evaluate(() => window.__deck.steps);
// hide the HUD for clean screenshots
await page.addStyleTag({ content: ".counter,.hint{display:none!important}" });

const settle = () => page.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(() => setTimeout(r, 120)))));
const stage = await page.$(".stage");
const finals = [];
for (let s = 1; s <= steps.length; s++) {
  for (let k = 0; k < steps[s - 1]; k++) {
    await page.evaluate((s, k) => window.__deck.goto(s, k), s, k);
    await settle();
    const file = path.join(shots, `s${String(s).padStart(2, "0")}-k${k}.png`);
    await stage.screenshot({ path: file });
    if (k === steps[s - 1] - 1) finals.push(file);
  }
}

// click-through: animated playback must stop on the step targets
await page.evaluate(() => window.__deck.goto(1, 0));
await settle();
const bad = [];
let mid = 0;
for (let i = 0; i < 12; i++) {
  await page.evaluate(() => window.__deck.next());
  await new Promise((r) => setTimeout(r, 450));
  if (mid < 3) {
    await stage.screenshot({ path: path.join(shots, `mid-animation-${++mid}.png`) });
  }
  await page.waitForFunction(() => !window.__deck.state().playing, { timeout: 15000 });
  await settle();
  const st = await page.evaluate(() => window.__deck.state());
  if (st.frame !== st.target) bad.push(st);
}
const endState = await page.evaluate(() => window.__deck.state());

// contact sheet of the final states (HTML grid -> screenshot)
const cols = 4, tw = 480, th = 270, gap = 16;
const rows = Math.ceil(finals.length / cols);
const imgs = finals
  .map((f, i) => `<figure><img src="data:image/png;base64,${fs.readFileSync(f).toString("base64")}"><figcaption>${i + 1}</figcaption></figure>`)
  .join("");
const sheet = await browser.newPage();
const W = cols * tw + (cols + 1) * gap, H = rows * (th + 24) + (rows + 1) * gap;
await sheet.setViewport({ width: W, height: H });
await sheet.setContent(`<style>body{margin:0;background:#dde2ea;display:grid;grid-template-columns:repeat(${cols},${tw}px);gap:${gap}px;padding:${gap}px;font:13px system-ui;color:#5b6b82}
figure{margin:0}img{width:${tw}px;height:${th}px;display:block;box-shadow:0 1px 4px rgba(0,0,0,.15)}figcaption{text-align:center;padding-top:4px}</style>${imgs}`);
await sheet.screenshot({ path: path.join(root, "contact-sheet.png"), fullPage: true });

await browser.close();
console.log(`screenshots: ${fs.readdirSync(shots).length} in verify/shots, contact-sheet.png written`);
console.log("after 12 clicks:", endState, bad.length ? "" : "(every click stopped exactly on its step frame)");
if (bad.length) console.log("BAD", bad);
if (errors.length) console.log("console:", [...new Set(errors)].slice(0, 20).join("\n"));
