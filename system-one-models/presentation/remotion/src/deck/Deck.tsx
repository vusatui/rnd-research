import React from "react";
import { AbsoluteFill } from "remotion";
import { linearTiming, TransitionSeries } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { easeInOut, StepContext } from "./anim";
import { useFonts } from "./fonts";
import { SLIDES } from "./slides";
import { DESIGN_H, DESIGN_W, TRANSITION, WHITE } from "./theme";
import { computeTimeline } from "./timeline";

export type DeckProps = {
  /** indices into SLIDES (default: all 19) */
  slides?: number[];
  /** extra frames to hold after every build step (0 in the presenter, where the speaker clicks) */
  hold?: number;
};

const SlideFrame: React.FC<{ index: number; stepEnds: number[] }> = ({ index, stepEnds }) => {
  const def = SLIDES[index];
  return (
    <AbsoluteFill style={{ backgroundColor: WHITE }}>
      <StepContext.Provider value={{ stepEnds, steps: def.steps }}>
        <svg viewBox={`0 0 ${DESIGN_W} ${DESIGN_H}`} width="100%" height="100%" style={{ display: "block" }}>
          <def.Component />
        </svg>
      </StepContext.Provider>
    </AbsoluteFill>
  );
};

export const Deck: React.FC<DeckProps> = ({ slides, hold = 0 }) => {
  const ready = useFonts();
  const tl = computeTimeline(slides, hold);
  if (!ready) return <AbsoluteFill style={{ backgroundColor: WHITE }} />;
  const timing = linearTiming({ durationInFrames: TRANSITION, easing: easeInOut });
  return (
    <AbsoluteFill style={{ backgroundColor: WHITE }}>
      <TransitionSeries>
        {tl.slides.flatMap((s, i) => {
          const nodes: React.ReactNode[] = [];
          if (i > 0) {
            const kind = SLIDES[s.index].enter;
            nodes.push(
              <TransitionSeries.Transition
                key={`t${i}`}
                presentation={kind === "slide" ? slide({ direction: "from-right" }) : fade()}
                timing={timing}
              />,
            );
          }
          nodes.push(
            <TransitionSeries.Sequence key={`s${i}`} durationInFrames={s.duration} name={SLIDES[s.index].title}>
              <SlideFrame index={s.index} stepEnds={s.stepEnds} />
            </TransitionSeries.Sequence>,
          );
          return nodes;
        })}
      </TransitionSeries>
    </AbsoluteFill>
  );
};
