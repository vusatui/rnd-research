import { SLIDES } from "./slides";
import { TRANSITION } from "./theme";

export type SlideTiming = {
  index: number; // index into SLIDES
  start: number; // global frame where the slide's sequence starts
  duration: number; // length of the slide's sequence (incl. the outgoing transition)
  stepEnds: number[]; // local frame at which each build step is complete (step 0 = entry)
};

export type Timeline = { slides: SlideTiming[]; total: number; hold: number };

/** Step k of a slide runs for steps[k] frames (+ hold frames in video mode, where nobody clicks). */
export function computeTimeline(indices: number[] = SLIDES.map((_, i) => i), hold = 0, tail = 30): Timeline {
  let start = 0;
  const slides = indices.map((index, i) => {
    const steps = SLIDES[index].steps;
    const stepEnds: number[] = [];
    let acc = 0;
    steps.forEach((d, k) => {
      acc += d;
      stepEnds.push(acc);
      if (k < steps.length - 1) acc += hold;
    });
    const last = i === indices.length - 1;
    const body = acc + hold;
    const duration = body + (last ? tail : TRANSITION);
    const t: SlideTiming = { index, start, duration, stepEnds };
    start += body;
    return t;
  });
  const lastT = slides[slides.length - 1];
  return { slides, total: lastT.start + lastT.duration, hold };
}
