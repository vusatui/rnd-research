import fs from "fs"; import path from "path"; import http from "http"; import { createRequire } from "module";
const here = path.dirname(new URL(import.meta.url).pathname);          // <topic>/presentation/tools
const light = path.resolve(here, "../../../system-one-models/presentation/tools");  // reuse bundle + node_modules of the first deck
const require = createRequire(light + "/");
const puppeteer = require("puppeteer-core");
const root = path.resolve(here, "..");
const scene = JSON.parse(fs.readFileSync(path.join(root, "presentation.excalidraw"), "utf8"));
const outDir = path.join(root, "export"); fs.mkdirSync(outDir, { recursive: true });
for (const f of fs.readdirSync(outDir)) if (/^slide-.*\.(png|svg)$/.test(f)) fs.unlinkSync(path.join(outDir, f));
const fontsDir = path.join(light, "node_modules/@excalidraw/excalidraw/dist/prod/");
const server = http.createServer((req, res) => {
  const u = decodeURIComponent(req.url.split("?")[0]);
  if (u === "/") { res.setHeader("content-type", "text/html"); res.end(`<!doctype html><html><body><script>window.EXCALIDRAW_ASSET_PATH="/assets/";</script><script src="/bundle.js"></script></body></html>`); return; }
  let p = u === "/bundle.js" ? path.join(light, "dist/export_bundle.js") : u.startsWith("/assets/") ? path.join(fontsDir, u.slice(8)) : null;
  if (p && fs.existsSync(p)) { res.setHeader("content-type", p.endsWith(".js") ? "text/javascript" : p.endsWith(".woff2") ? "font/woff2" : "application/octet-stream"); res.end(fs.readFileSync(p)); } else { res.statusCode = 404; res.end(); }
}).listen(0);
const port = server.address().port;
const browser = await puppeteer.launch({ executablePath: "/usr/bin/google-chrome", headless: "new", args: ["--no-sandbox", "--disable-gpu"] });
const page = await browser.newPage();
await page.setViewport({ width: 1600, height: 900, deviceScaleFactor: 1 });
page.on("pageerror", (e) => console.error("pageerror", e.message));
await page.goto(`http://localhost:${port}/`);
await page.waitForFunction("window.__ready === true", { timeout: 60000 });
const frames = scene.elements.filter((e) => e.type === "frame");
for (const fr of frames) {
  const svg = await page.evaluate((sc, id, files) => window.__exportFrame(sc, id, files), scene, fr.id, scene.files);
  const slug = fr.name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  fs.writeFileSync(path.join(outDir, `${slug}.svg`), svg);
  const p2 = await browser.newPage();
  await p2.setViewport({ width: 1600, height: 900 });
  await p2.setContent(`<html><body style="margin:0;background:#fff">${svg.replace(/<svg /, '<svg style="display:block;width:1600px;height:900px" ')}</body></html>`);
  await new Promise((r) => setTimeout(r, 500));
  await p2.screenshot({ path: path.join(outDir, `${slug}.png`), clip: { x: 0, y: 0, width: 1600, height: 900 } });
  await p2.close();
  console.log("exported", slug);
}
await browser.close(); server.close();
