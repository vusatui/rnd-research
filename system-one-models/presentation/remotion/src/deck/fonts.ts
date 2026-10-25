import { useEffect, useState } from "react";
import { continueRender, delayRender } from "remotion";
import excalifont from "../assets/fonts/Excalifont.woff2";
import cascadia from "../assets/fonts/CascadiaCode-Regular.woff2";
import arrows from "../assets/fonts/LiberationSans-Arrows.woff2";

// Fonts are bundled with the app (no network at runtime).
let loaded = false;
let promise: Promise<void> | null = null;

export function loadFonts(): Promise<void> {
  if (!promise) {
    const faces = [new FontFace("Excalifont", `url(${excalifont})`), new FontFace("Cascadia Code", `url(${cascadia})`), new FontFace("Deck Arrows", `url(${arrows})`)];
    promise = Promise.all(
      faces.map((f) =>
        f.load().then((ff) => {
          document.fonts.add(ff);
        }),
      ),
    ).then(() => {
      loaded = true;
    });
  }
  return promise;
}

/** true once the fonts are ready; blocks Remotion rendering until then. */
export function useFonts(): boolean {
  const [ready, setReady] = useState(loaded);
  const [handle] = useState(() => (loaded ? null : delayRender("Loading fonts")));
  useEffect(() => {
    loadFonts().then(() => {
      setReady(true);
      if (handle !== null) continueRender(handle);
    });
  }, [handle]);
  return ready;
}

const cache = new Map<string, number>();
let ctx: CanvasRenderingContext2D | null = null;

/** Width of a (possibly multi-line) string in design px, like excal.measure(). */
export function measure(text: string, size: number, family = "Excalifont, 'Deck Arrows', 'Cascadia Code'"): number {
  const key = `${size}|${family}|${text}`;
  const hit = cache.get(key);
  if (hit !== undefined) return hit;
  ctx ??= document.createElement("canvas").getContext("2d")!;
  ctx.font = `${size}px ${family}`;
  const w = Math.max(...text.split("\n").map((l) => ctx!.measureText(l).width));
  if (loaded) cache.set(key, w);
  return w;
}
