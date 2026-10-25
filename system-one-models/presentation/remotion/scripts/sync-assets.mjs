// Copies the QR code and converts the speaker notes of the serious deck (the source of truth)
// into src/assets/qr.png and src/notes.json.   npm run sync
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const serious = path.resolve(here, "../../serious");
const out = path.resolve(here, "../src");

fs.copyFileSync(path.join(serious, "qr.png"), path.join(out, "assets/qr.png"));

const md = fs.readFileSync(path.join(serious, "speaker-notes.md"), "utf8");
const [body, qaPart = ""] = md.split(/^## Easy questions you may get\s*$/m);

const paras = (txt) =>
  txt
    .split(/\n\s*\n/)
    .map((p) => p.replace(/\s*\n\s*/g, " ").trim())
    .filter((p) => p && p !== "---" && !p.startsWith("Sources for the facts"));

const slides = [];
const re = /^## Slide (\d+) · (.+?) · ([\d.]+ min)\s*$/gm;
const heads = [...body.matchAll(re)];
heads.forEach((m, i) => {
  const end = i + 1 < heads.length ? heads[i + 1].index : body.length;
  slides.push({
    n: Number(m[1]),
    title: m[2],
    time: m[3],
    paragraphs: paras(body.slice(m.index + m[0].length, end)),
  });
});

const qa = [];
for (const m of qaPart.matchAll(/\*\*(\d+)\. (.+?)\*\*\n([^]*?)(?=\n\*\*\d+\.|\n---|$)/g)) {
  qa.push({ q: m[2].trim(), a: m[3].replace(/\s*\n\s*/g, " ").trim() });
}

if (slides.length !== 19) throw new Error(`expected 19 slides in speaker-notes.md, got ${slides.length}`);
fs.writeFileSync(path.join(out, "notes.json"), JSON.stringify({ slides, qa }, null, 2) + "\n");
console.log(`notes.json: ${slides.length} slides, ${qa.length} Q&As; qr.png copied`);
