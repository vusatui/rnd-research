import React from "react";
import { Composition } from "remotion";
import { Deck, type DeckProps } from "../deck/Deck";
import { FPS, VIDEO_H, VIDEO_W } from "../deck/theme";
import { computeTimeline } from "../deck/timeline";

const meta = ({ props }: { props: DeckProps }) => ({ durationInFrames: computeTimeline(props.slides, props.hold).total });

export const Root: React.FC = () => (
  <>
    {/* the whole deck, played back automatically: every build step is held for 1.5 s */}
    <Composition id="Deck" component={Deck} width={VIDEO_W} height={VIDEO_H} fps={FPS} durationInFrames={1}
      defaultProps={{ hold: 45 } as DeckProps} calculateMetadata={meta} />
    {/* the exact timeline the presenter uses (no holds; the presenter pauses at the end of each step) */}
    <Composition id="Presenter" component={Deck} width={VIDEO_W} height={VIDEO_H} fps={FPS} durationInFrames={1}
      defaultProps={{ hold: 0 } as DeckProps} calculateMetadata={meta} />
    {/* a short sample of builds and transitions */}
    <Composition id="Sample" component={Deck} width={VIDEO_W} height={VIDEO_H} fps={FPS} durationInFrames={1}
      defaultProps={{ slides: [3, 4, 12, 13], hold: 15 } as DeckProps} calculateMetadata={meta} />
  </>
);
