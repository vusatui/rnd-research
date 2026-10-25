import { createContext, useContext } from "react";
import { Easing, useCurrentFrame } from "remotion";

export const StepContext = createContext<{ stepEnds: number[]; steps: number[] }>({ stepEnds: [0], steps: [0] });

export const easeOut = Easing.bezier(0.22, 1, 0.36, 1);
export const easeInOut = Easing.bezier(0.65, 0, 0.35, 1);

export const clamp01 = (v: number) => (v < 0 ? 0 : v > 1 ? 1 : v);
/** sub-progress of p between a and b */
export const seg = (p: number, a: number, b: number) => clamp01((p - a) / (b - a));
export const lerp = (a: number, b: number, p: number) => a + (b - a) * p;

export type T = {
  /** eased progress (0..1) of an animation that starts `delay` frames into build step `step` and lasts `dur` frames */
  p: (step: number, delay?: number, dur?: number, ease?: (x: number) => number) => number;
  frame: number;
};

export function useT(): T {
  const frame = useCurrentFrame();
  const { stepEnds, steps } = useContext(StepContext);
  return {
    frame,
    p: (step, delay = 0, dur = 18, ease = easeOut) => {
      const start = stepEnds[step] - steps[step] + delay;
      return ease(clamp01((frame - start) / dur));
    },
  };
}

export const linearEase = (x: number) => x;
