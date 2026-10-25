// preview/sample-transitions.mp4 -> preview/sample-transitions.gif (needs ffmpeg on PATH)
import { execFileSync } from "node:child_process";
const vf = "fps=12,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse=dither=none";
execFileSync("ffmpeg", ["-loglevel", "error", "-y", "-i", "preview/sample-transitions.mp4", "-vf", vf, "preview/sample-transitions.gif"], { stdio: "inherit" });
console.log("preview/sample-transitions.gif");
