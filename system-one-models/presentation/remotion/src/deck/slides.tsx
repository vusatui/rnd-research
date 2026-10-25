// The 19 slides of the serious deck (same order, wording and layout as ../../serious/tools/build_deck.py),
// each split into build steps. Step 0 is the entry (plays with the transition); every click plays the next step.
// steps[k] = length of step k in frames (30 fps). All animations of a step must finish inside it.
import React from "react";
import { Img } from "remotion";
import qr from "../assets/qr.png";
import { linearEase, seg, useT } from "./anim";
import {
  Arr, Bars, Bolt, Box, Caption, Check, Chip, CodePanel, Cross, Doc, Fork, Gauge, Magnifier, PageNum, Person, Shield, Tag, Title,
} from "./parts";
import { Ellipse, Line, Rect, Txt } from "./shapes";
import { ACC, ACC_L, LIGHT, MID, NAVY, REPO, SLATE, WHITE } from "./theme";

export type SlideDef = {
  id: string;
  title: string;
  steps: number[];
  /** transition used when entering this slide */
  enter: "fade" | "slide";
  Component: React.FC;
};

// 01 ------------------------------------------------------------------
const S01: React.FC = () => {
  const t = useT();
  return (
    <>
      <Txt x={100} y={250} text="System One models" size={120} color={NAVY} p={t.p(0, 4, 30)} anim="wipe" />
      <Line pts={[[104, 400], [700, 404], [1180, 399]]} stroke={ACC} sw={7} p={t.p(0, 22, 22)} />
      <Txt x={104} y={430} text="AI that decides, instead of writes" size={52} color={SLATE} p={t.p(0, 34, 18)} />
      <Txt x={1500} y={150} text="Internal talk · 30 min" size={30} color={SLATE} align="right" p={t.p(0, 40, 16)} />
      <Doc x={130} y={640} w={90} h={118} p={t.p(0, 50, 20)} />
      <Arr pts={[[250, 700], [400, 700]]} p={t.p(0, 62, 14)} />
      <Chip x={450} y={650} w={120} h={100} p={t.p(0, 68, 18)} />
      <Arr pts={[[640, 700], [790, 700]]} color={ACC} p={t.p(0, 78, 12)} />
      <Bars x={840} y={640} vals={[0.25, 0.9, 0.35]} bw={36} hmax={120} hi={1} p={t.p(0, 82, 18)} />
    </>
  );
};

// 02 ------------------------------------------------------------------
const S02: React.FC = () => {
  const t = useT();
  return (
    <>
      <Title text="Two kinds of AI models" />
      <Txt x={100} y={250} text="Generator" size={44} color={SLATE} p={t.p(1, 0, 14)} />
      <Doc x={100} y={320} w={90} h={115} lines={3} p={t.p(1, 4, 18)} />
      <Arr pts={[[220, 378], [450, 378]]} p={t.p(1, 14, 14)} />
      <Box x={470} y={330} w={340} h={96} text="Text generator" p={t.p(1, 22, 18)} />
      <Arr pts={[[830, 378], [1060, 378]]} p={t.p(1, 34, 12)} />
      <Doc x={1090} y={316} w={110} h={130} lines={5} p={t.p(1, 40, 14)} />
      <Doc x={1220} y={316} w={110} h={130} lines={5} p={t.p(1, 44, 14)} />
      <Txt x={1360} y={350} text="…" size={70} color={SLATE} p={t.p(1, 48, 10)} />

      <Txt x={100} y={520} text="Decider" size={44} color={ACC} p={t.p(2, 0, 14)} />
      <Doc x={100} y={590} w={90} h={115} lines={3} p={t.p(2, 4, 18)} />
      <Arr pts={[[220, 648], [450, 648]]} color={ACC} p={t.p(2, 14, 14)} />
      <Box x={470} y={600} w={340} h={96} text="Decision model" fill={ACC_L} stroke={ACC} p={t.p(2, 22, 18)} />
      <Arr pts={[[830, 648], [1060, 648]]} color={ACC} p={t.p(2, 34, 12)} />
      <Rect x={1090} y={580} w={330} h={135} fill={WHITE} stroke={ACC} sw={3} p={t.p(2, 38, 10)} />
      <Bars x={1130} y={600} vals={[0.2, 0.85, 0.3]} bw={36} hmax={95} hi={1} p={t.p(2, 40, 14)} />
      <Check x={1290} y={625} k={1} color={ACC} sw={8} p={t.p(2, 48, 10)} />

      <Caption text="Text out   vs   a decision out" y={810} p={t.p(3, 0, 20)} />
      <PageNum n={2} />
    </>
  );
};

// 03 ------------------------------------------------------------------
const S03: React.FC = () => {
  const t = useT();
  return (
    <>
      <Title text="Two ways to think" />
      <Rect x={100} y={240} w={650} h={400} fill={ACC_L} stroke={ACC} sw={3} p={t.p(1, 0, 20)} />
      <Bolt x={380} y={290} p={t.p(1, 10, 22)} />
      <Txt x={425} y={520} text="System 1" size={56} color={ACC} anchor="center" align="center" p={t.p(1, 22, 14)} />
      <Txt x={425} y={590} text="fast · instinct" size={38} color={NAVY} anchor="center" align="center" p={t.p(1, 28, 14)} />

      <Rect x={850} y={240} w={650} h={400} fill={LIGHT} stroke={NAVY} sw={3} p={t.p(2, 0, 20)} />
      <Magnifier x={1090} y={300} k={1.4} p={t.p(2, 10, 22)} />
      <Txt x={1175} y={520} text="System 2" size={56} color={NAVY} anchor="center" align="center" p={t.p(2, 22, 14)} />
      <Txt x={1175} y={590} text="slow · deliberate" size={38} color={SLATE} anchor="center" align="center" p={t.p(2, 28, 14)} />

      <Arr pts={[[425, 665], [425, 735]]} color={ACC} p={t.p(3, 0, 14)} />
      <Caption text="Decision models are built for System 1 jobs" y={780} color={NAVY} size={42} p={t.p(3, 8, 20)} />
      <Txt x={1500} y={660} text="idea from Kahneman" size={28} color={SLATE} align="right" p={t.p(3, 18, 16)} />
      <PageNum n={3} />
    </>
  );
};

// 04 ------------------------------------------------------------------
const S04: React.FC = () => {
  const t = useT();
  const boxes: [number, string][] = [[120, "one HTTP call"], [590, "no generated text"], [1060, "typed answers"]];
  const arrows: [number, number][][] = [
    [[330, 650], [610, 540]],
    [[800, 650], [800, 570]],
    [[1270, 650], [990, 540]],
  ];
  return (
    <>
      <Title text="What is Jev?" sub="A hosted System One model from TypeSafe AI" subSize={38} />
      <Ellipse x={560} y={300} w={480} h={260} fill={ACC_L} stroke={ACC} sw={4} p={t.p(1, 0, 24)} />
      <Txt x={800} y={430} text="Jev" size={110} color={ACC} anchor="center" align="center" p={t.p(1, 14, 18)} />
      {boxes.map(([x, s], i) => (
        <Box key={s} x={x} y={660} w={420} h={100} text={s} p={t.p(2, i * 12, 20)} />
      ))}
      {arrows.map((pts, i) => (
        <Arr key={i} pts={pts} color={SLATE} sw={3} p={t.p(2, 14 + i * 12, 16)} />
      ))}
      <PageNum n={4} />
    </>
  );
};

// 05 ------------------------------------------------------------------
const S05: React.FC = () => {
  const t = useT();
  return (
    <>
      <Title text="One call, one decision" />
      <Tag x={1180} y={740} text="illustrative" p={t.p(0, 26, 14)} />
      <Doc x={110} y={280} w={100} h={130} lines={4} p={t.p(1, 0, 20)} />
      <Txt x={160} y={445} text="state" size={40} anchor="center" align="center" p={t.p(1, 10, 12)} />
      <Txt x={110} y={480} text="(the text)" size={30} color={SLATE} p={t.p(1, 14, 12)} />
      <Rect x={110} y={570} w={140} h={130} fill={WHITE} stroke={NAVY} sw={3} p={t.p(1, 10, 18)} />
      {[0, 1, 0].map((r, i) => (
        <React.Fragment key={i}>
          <Ellipse x={135} y={592 + i * 34} w={20} h={20} stroke={NAVY} sw={2} fill={r ? ACC_L : WHITE} p={t.p(1, 18 + i * 4, 10)} />
          <Line pts={[[172, 602 + i * 34], [225, 602 + i * 34]]} stroke={SLATE} sw={3} p={t.p(1, 20 + i * 4, 10)} />
        </React.Fragment>
      ))}
      <Txt x={180} y={735} text="questions" size={40} anchor="center" align="center" p={t.p(1, 26, 12)} />

      <Arr pts={[[270, 345], [470, 450]]} p={t.p(2, 0, 16)} pulse={t.p(2, 16, 24, linearEase)} />
      <Arr pts={[[270, 635], [470, 520]]} p={t.p(2, 4, 16)} pulse={t.p(2, 18, 24, linearEase)} />
      <Box x={480} y={400} w={340} h={150} text="Jev" size={80} fill={ACC_L} stroke={ACC} color={ACC} p={t.p(2, 12, 20)} />

      <Arr pts={[[840, 475], [1010, 475]]} color={ACC} p={t.p(3, 0, 14)} pulse={t.p(3, 4, 18, linearEase)} />
      <Rect x={1030} y={300} w={470} h={340} fill={WHITE} stroke={ACC} sw={3} p={t.p(3, 8, 18)} />
      <Txt x={1060} y={325} text="department" size={36} p={t.p(3, 18, 12)} />
      <Bars x={1070} y={375} vals={[0.12, 0.88, 0.1]} bw={40} hmax={100} hi={1} p={t.p(3, 22, 22)} />
      <Txt x={1260} y={400} text="technical" size={40} color={ACC} p={t.p(3, 38, 12)} />
      <Txt x={1060} y={520} text="urgent?" size={36} p={t.p(3, 30, 12)} />
      <Gauge x={1230} y={525} w={230} level={0.9} p={t.p(3, 34, 24)} />
      <Txt x={1265} y={695} text="numbers, not sentences" size={38} color={SLATE} anchor="center" align="center" p={t.p(3, 50, 16)} />
      <PageNum n={5} />
    </>
  );
};

// 06 ------------------------------------------------------------------
const S06: React.FC = () => {
  const t = useT();
  const cards: [string, string, number][] = [["Choice", "pick one", 100], ["Score", "rate on a scale", 580], ["Yes / no", "probability of yes", 1060]];
  const sel = t.p(1, 38, 14);
  const knob = t.p(2, 30, 16);
  return (
    <>
      <Title text="Three kinds of questions" />
      {cards.map(([name, sub, x], i) => (
        <React.Fragment key={name}>
          <Rect x={x} y={250} w={440} h={480} fill={LIGHT} stroke={NAVY} sw={3} p={t.p(i + 1, 0, 18)} />
          <Txt x={x + 220} y={320} text={name} size={56} color={ACC} anchor="center" align="center" p={t.p(i + 1, 8, 14)} />
          <Txt x={x + 220} y={385} text={sub} size={36} color={SLATE} anchor="center" align="center" p={t.p(i + 1, 12, 14)} />
        </React.Fragment>
      ))}
      {/* choice: three options, one gets picked */}
      {["billing", "technical", "sales"].map((s, i) => {
        const yy = 460 + i * 70;
        const op = t.p(1, 18 + i * 5, 12);
        return (
          <React.Fragment key={s}>
            <Ellipse x={150} y={yy} w={34} h={34} stroke={NAVY} sw={3} fill={WHITE} p={op} />
            {i === 1 && <Ellipse x={150} y={yy} w={34} h={34} stroke={NAVY} sw={3} fill={ACC_L} p={sel > 0 ? 1 : 0} opacity={sel} fillFrom={0} />}
            <Txt x={205} y={yy - 4} text={s} size={38} color={NAVY} p={i === 1 ? op * (1 - sel) : op} />
            {i === 1 && <Txt x={205} y={yy - 4} text={s} size={38} color={ACC} p={sel} anim="fade" />}
          </React.Fragment>
        );
      })}
      {/* score: scale + knob */}
      <Line pts={[[630, 560], [980, 560]]} stroke={NAVY} sw={4} p={t.p(2, 14, 14)} />
      {[0, 1, 2, 3, 4].map((i) => (
        <Line key={i} pts={[[630 + i * 87.5, 540], [630 + i * 87.5, 580]]} stroke={NAVY} sw={3} p={t.p(2, 18 + i * 3, 8)} />
      ))}
      <g transform={`translate(${(1 - knob) * -151} 0)`}>
        <Ellipse x={759} y={538} w={44} h={44} fill={ACC_L} stroke={ACC} sw={4} p={knob > 0 ? 1 : 0} opacity={knob} fillFrom={0} />
      </g>
      <Txt x={630} y={620} text="calm" size={34} color={SLATE} p={t.p(2, 24, 12)} />
      <Txt x={980} y={620} text="angry" size={34} color={SLATE} align="right" p={t.p(2, 24, 12)} />
      {/* yes / no: gauge */}
      <Gauge x={1110} y={545} w={340} level={0.82} thr={0.5} p={t.p(3, 18, 26)} />
      <Txt x={1110} y={600} text="no" size={34} color={SLATE} p={t.p(3, 26, 12)} />
      <Txt x={1450} y={600} text="yes" size={34} color={ACC} align="right" p={t.p(3, 26, 12)} />
      <Txt x={1280} y={480} text="urgent?" size={40} anchor="center" align="center" p={t.p(3, 14, 12)} />
      <PageNum n={6} />
    </>
  );
};

// 07 ------------------------------------------------------------------
const S07: React.FC = () => {
  const t = useT();
  const cards: [number, string, string][] = [[100, "OpenAI", "Decisions API (beta)"], [580, "Cloudflare", "Clef, open weights"], [1060, "Unsloth", "recipe to train your own"]];
  return (
    <>
      <Title text="Not only Jev" />
      <Txt x={800} y={330} text="Same shape" size={60} color={ACC} anchor="center" align="center" p={t.p(1, 0, 18)} />
      <Txt x={800} y={400} text="text + questions  →  typed answers" size={38} color={SLATE} anchor="center" align="center" p={t.p(1, 10, 18)} />
      {cards.map(([x, name, sub], i) => (
        <React.Fragment key={name}>
          <Rect x={x} y={540} w={440} h={200} fill={LIGHT} stroke={NAVY} sw={3} p={t.p(2, i * 10, 18)} />
          <Txt x={x + 220} y={600} text={name} size={52} anchor="center" align="center" p={t.p(2, i * 10 + 8, 14)} />
          <Txt x={x + 220} y={675} text={sub} size={34} color={SLATE} anchor="center" align="center" p={t.p(2, i * 10 + 12, 14)} />
          <Arr pts={[[x + 220, 535], [800 + (x + 220 - 800) * 0.3, 450]]} color={SLATE} sw={3} p={t.p(2, i * 10 + 20, 16)} />
        </React.Fragment>
      ))}
      <PageNum n={7} />
    </>
  );
};

// 08 ------------------------------------------------------------------
const Icon: React.FC<{ i: number; cx: number; cy: number; p: number }> = ({ i, cx, cy, p }) => {
  switch (i) {
    case 0:
      return <Fork x={cx - 45} y={cy - 40} p={p} />;
    case 1:
      return <Shield x={cx - 45} y={cy - 55} k={0.65} p={p} />;
    case 2:
      return <Magnifier x={cx - 40} y={cy - 45} k={0.9} p={p} />;
    case 3:
      return (
        <>
          <Rect x={cx - 40} y={cy - 40} w={80} h={80} fill={WHITE} stroke={NAVY} sw={3} round={false} p={seg(p, 0, 0.6)} />
          <Check x={cx - 25} y={cy - 28} k={0.8} color={ACC} sw={6} p={seg(p, 0.5, 1)} />
        </>
      );
    case 4:
      return (
        <>
          <Rect x={cx - 55} y={cy - 40} w={110} h={70} fill={WHITE} stroke={NAVY} sw={3} p={seg(p, 0, 0.6)} />
          <Line pts={[[cx - 20, cy + 30], [cx - 30, cy + 55], [cx + 5, cy + 30]]} stroke={NAVY} sw={3} p={seg(p, 0.4, 0.8)} />
          <Txt x={cx} y={cy - 5} text="?" size={56} color={ACC} anchor="center" align="center" p={seg(p, 0.5, 1)} />
        </>
      );
    default:
      return (
        <>
          <Ellipse x={cx - 45} y={cy - 45} w={90} h={90} fill={ACC_L} stroke={ACC} sw={3} fillStyle="hachure" p={seg(p, 0, 0.6)} />
          <Check x={cx - 28} y={cy - 25} k={0.9} color={NAVY} sw={6} p={seg(p, 0.5, 1)} />
        </>
      );
  }
};

const S08: React.FC = () => {
  const t = useT();
  const items = ["Routing", "Moderation", "Fraud triage", "Form checks", "Intent detection", "Approvals"];
  return (
    <>
      <Title text="Where it fits" />
      {items.map((s, i) => {
        const x = 100 + (i % 3) * 480;
        const y = 240 + Math.floor(i / 3) * 290;
        return (
          <React.Fragment key={s}>
            <Rect x={x} y={y} w={440} h={250} fill={LIGHT} stroke={NAVY} sw={3} p={t.p(1, i * 8, 18)} />
            <Icon i={i} cx={x + 220} cy={y + 95} p={t.p(1, i * 8 + 10, 20)} />
            <Txt x={x + 220} y={y + 200} text={s} size={44} anchor="center" align="center" p={t.p(1, i * 8 + 14, 14)} />
          </React.Fragment>
        );
      })}
      <PageNum n={8} />
    </>
  );
};

// 09 ------------------------------------------------------------------
const S09: React.FC = () => {
  const t = useT();
  const outs: { pts: [number, number][]; color: string }[] = [
    { pts: [[680, 425], [950, 280]], color: SLATE },
    { pts: [[680, 445], [950, 445]], color: ACC },
    { pts: [[680, 465], [950, 610]], color: SLATE },
  ];
  return (
    <>
      <Title text="Routing" />
      <Tag x={1290} y={235} text="illustrative" size={26} p={t.p(0, 26, 14)} />
      <Doc x={100} y={380} w={100} h={130} lines={3} p={t.p(1, 0, 18)} />
      <Txt x={90} y={530} text="ticket" size={36} color={SLATE} p={t.p(1, 8, 12)} />
      <Arr pts={[[230, 445], [400, 445]]} p={t.p(1, 12, 14)} pulse={t.p(1, 20, 18, linearEase)} />
      <Box x={420} y={395} w={240} h={100} text="Jev" size={56} fill={ACC_L} stroke={ACC} color={ACC} p={t.p(1, 18, 18)} />

      {outs.map((o, i) => (
        <Arr key={i} pts={o.pts} color={o.color} p={t.p(2, i * 6, 16)} pulse={i === 1 ? t.p(2, 22, 22, linearEase) : 0} />
      ))}
      <Box x={960} y={220} w={300} h={100} text="Billing" size={42} p={t.p(2, 10, 18)} />
      <Box x={960} y={395} w={300} h={100} text="Technical" size={42} fill={ACC_L} stroke={ACC} color={ACC} p={t.p(2, 16, 18)} />
      <Box x={960} y={570} w={300} h={100} text="Sales" size={42} p={t.p(2, 22, 18)} />

      <Arr pts={[[540, 510], [540, 690]]} color={SLATE} dashed sw={3} p={t.p(3, 0, 16)} />
      <Txt x={565} y={570} text="unsure" size={36} color={SLATE} p={t.p(3, 8, 12)} />
      <Person cx={540} y={700} k={0.6} color={SLATE} p={t.p(3, 14, 18)} />
      <Txt x={590} y={730} text="human" size={36} color={SLATE} p={t.p(3, 22, 14)} />
      <PageNum n={9} />
    </>
  );
};

// 10 ------------------------------------------------------------------
const S10: React.FC = () => {
  const t = useT();
  const lanes: [string, number, number, string, string][] = [
    ["Allow", 900, 180, LIGHT, NAVY],
    ["Human review", 1090, 290, ACC_L, ACC],
    ["Block", 1390, 130, LIGHT, NAVY],
  ];
  return (
    <>
      <Title text="Moderation" />
      <Tag x={100} y={240} text="illustrative" size={26} p={t.p(0, 26, 14)} />
      <Rect x={100} y={300} w={330} h={150} fill={WHITE} stroke={NAVY} sw={3} p={t.p(1, 0, 18)} />
      <Txt x={265} y={345} text="comment" size={40} anchor="center" align="center" p={t.p(1, 8, 12)} />
      {[0, 1].map((i) => (
        <Line key={i} pts={[[135, 395 + i * 28], [395 - i * 60, 395 + i * 28]]} stroke={SLATE} sw={3} p={t.p(1, 12 + i * 4, 12)} />
      ))}
      <Arr pts={[[450, 375], [570, 375]]} p={t.p(1, 16, 12)} />
      <Box x={590} y={325} w={200} h={100} text="Jev" size={56} fill={ACC_L} stroke={ACC} color={ACC} p={t.p(1, 24, 18)} />

      <Arr pts={[[810, 375], [880, 375]]} color={ACC} p={t.p(2, 0, 12)} />
      {lanes.map(([s, x, w, f, c], i) => (
        <React.Fragment key={s}>
          <Rect x={x} y={330} w={w - 10} h={90} fill={f} stroke={c} sw={3} p={t.p(2, 6 + i * 8, 16)} />
          <Txt x={x + (w - 10) / 2} y={375} text={s} size={32} color={c} anchor="center" align="center" p={t.p(2, 12 + i * 8, 12)} />
        </React.Fragment>
      ))}
      <Check x={960} y={470} k={0.9} color={NAVY} sw={6} p={t.p(2, 30, 14)} />
      <Person cx={1225} y={450} k={0.55} color={ACC} p={t.p(2, 34, 16)} />
      <Cross x={1430} y={470} k={0.9} color={NAVY} sw={6} p={t.p(2, 38, 14)} />

      <Arr pts={[[900, 590], [1510, 590]]} color={SLATE} tail sw={3} p={t.p(3, 0, 18)} />
      <Txt x={900} y={610} text="sure it's fine" size={30} color={SLATE} p={t.p(3, 12, 12)} />
      <Txt x={1510} y={610} text="sure it's not" size={30} color={SLATE} align="right" p={t.p(3, 14, 12)} />
      <Caption text="unsure → ask a person" y={760} color={ACC} size={42} p={t.p(3, 26, 18)} />
      <PageNum n={10} />
    </>
  );
};

// 11 ------------------------------------------------------------------
const S11: React.FC = () => {
  const t = useT();
  return (
    <>
      <Title text="Fraud triage" />
      <Tag x={100} y={240} text="illustrative" size={26} p={t.p(0, 26, 14)} />
      <Rect x={100} y={330} w={330} h={190} fill={WHITE} stroke={NAVY} sw={3} p={t.p(1, 0, 18)} />
      <Txt x={265} y={380} text="payment" size={42} anchor="center" align="center" p={t.p(1, 8, 12)} />
      <Txt x={265} y={445} text="unusual?" size={42} color={SLATE} anchor="center" align="center" p={t.p(1, 12, 12)} />
      <Arr pts={[[450, 425], [580, 425]]} p={t.p(1, 16, 12)} />
      <Box x={600} y={375} w={200} h={100} text="Jev" size={56} fill={ACC_L} stroke={ACC} color={ACC} p={t.p(1, 22, 16)} />
      <Arr pts={[[820, 425], [940, 425]]} color={ACC} p={t.p(1, 34, 12)} />
      <Txt x={960} y={285} text="risk" size={40} p={t.p(1, 36, 12)} />
      <Gauge x={960} y={340} w={480} level={0.8} thr={0.6} p={t.p(1, 38, 22)} />
      <Txt x={960} y={395} text="low" size={30} color={SLATE} p={t.p(1, 44, 12)} />
      <Txt x={1440} y={395} text="high" size={30} color={SLATE} align="right" p={t.p(1, 44, 12)} />

      <Arr pts={[[1010, 450], [1010, 560]]} color={SLATE} p={t.p(2, 0, 14)} />
      <Check x={980} y={580} k={1} color={NAVY} sw={7} p={t.p(2, 10, 14)} />
      <Txt x={1010} y={730} text="fast path" size={40} anchor="center" align="center" p={t.p(2, 16, 14)} />

      <Arr pts={[[1300, 450], [1300, 560]]} color={ACC} p={t.p(3, 0, 14)} />
      <Magnifier x={1260} y={580} k={1} color={ACC} p={t.p(3, 8, 18)} />
      <Txt x={1300} y={730} text="closer look" size={40} color={ACC} anchor="center" align="center" p={t.p(3, 16, 14)} />
      <Caption text="a first look, not a verdict" y={835} size={36} p={t.p(3, 26, 18)} />
      <PageNum n={11} />
    </>
  );
};

// 12 ------------------------------------------------------------------
const S12: React.FC = () => {
  const t = useT();
  return (
    <>
      <Title text="Fast first" />
      {Array.from({ length: 8 }, (_, i) => (
        <Ellipse key={i} x={100 + (i % 2) * 50} y={300 + Math.floor(i / 2) * 60} w={32} h={32} fill={MID} stroke={NAVY} sw={2} p={t.p(1, i * 3, 10)} />
      ))}
      <Txt x={100} y={550} text="all requests" size={34} color={SLATE} p={t.p(1, 18, 12)} />
      <Arr pts={[[230, 400], [420, 400]]} p={t.p(1, 22, 14)} pulse={t.p(1, 30, 18, linearEase)} />
      <Box x={440} y={340} w={300} h={120} text="Fast model" size={46} fill={ACC_L} stroke={ACC} color={ACC} p={t.p(1, 28, 18)} />

      <Arr pts={[[760, 370], [1060, 370]]} color={ACC} p={t.p(2, 0, 16)} pulse={t.p(2, 12, 22, linearEase)} />
      <Txt x={910} y={335} text="most" size={36} color={ACC} anchor="center" align="center" p={t.p(2, 8, 12)} />
      <Rect x={1080} y={330} w={380} h={90} fill={LIGHT} stroke={NAVY} sw={3} p={t.p(2, 12, 16)} />
      <Txt x={1270} y={375} text="answered" size={40} anchor="center" align="center" p={t.p(2, 20, 14)} />

      <Arr pts={[[590, 480], [590, 640], [1060, 640]]} curved={false} color={SLATE} dashed p={t.p(3, 0, 20)} />
      <Txt x={610} y={540} text="unsure" size={36} color={SLATE} p={t.p(3, 8, 12)} />
      <Box x={1080} y={590} w={380} h={100} text="Big LLM" size={46} p={t.p(3, 16, 18)} />
      <Arr pts={[[1270, 700], [1270, 770]]} color={SLATE} p={t.p(3, 30, 12)} />
      <Txt x={1270} y={810} text="answered" size={36} color={SLATE} anchor="center" align="center" p={t.p(3, 38, 14)} />
      <PageNum n={12} />
    </>
  );
};

// 13 ------------------------------------------------------------------
const REQ = [
  "POST /v1/systemone", "{", '  "model": "jev-latest",', '  "state": "API returns 500 on every', '            request for 20 minutes…",',
  '  "questions": {', '    "department": {', '      "type": "choice",', '      "criteria": { "billing": …,', '                    "technical": …,',
  '                    "sales": … }', "    },", '    "urgent": { "type": "noul" }', "  }", "}",
];
const S13: React.FC = () => {
  const t = useT();
  const marks = [
    { from: 3, to: 4, m: t.p(2, 2, 16) },
    { from: 5, to: 13, m: t.p(3, 2, 18) },
  ];
  return (
    <>
      <Title text="Live demo: request" />
      <Txt x={100} y={835} text="workshop-lite/jev_client.py · local emulator unless a Jev key is set" size={30} color={SLATE} p={t.p(0, 26, 14)} />
      <CodePanel x={100} y={215} w={820} lines={REQ} size={28} hl={{ 0: ACC_L }} p={t.p(1, 0, 66, linearEase)} marks={marks} />
      <Tag x={1070} y={660} text="shortened" size={28} p={t.p(1, 50, 14)} />
      <Arr pts={[[950, 372], [1050, 372]]} color={ACC} sw={3} p={t.p(2, 0, 14)} />
      <Txt x={1070} y={340} text="state" size={44} color={ACC} p={t.p(2, 8, 12)} />
      <Txt x={1070} y={390} text="the text" size={30} color={SLATE} p={t.p(2, 12, 12)} />
      <Arr pts={[[950, 470], [1050, 470]]} color={ACC} sw={3} p={t.p(3, 0, 14)} />
      <Txt x={1070} y={440} text="questions" size={44} color={ACC} p={t.p(3, 8, 12)} />
      <Txt x={1070} y={490} text="what we want" size={30} color={SLATE} p={t.p(3, 12, 12)} />
      <PageNum n={13} />
    </>
  );
};

// 14 ------------------------------------------------------------------
const RESP = [
  "{", '  "department": {', '    "type": "choice",', '    "choice": "technical",', '    "confidence": 1.0,', '    "probabilities": {',
  '      "billing": 0.0,', '      "technical": 1.0,', '      "sales": 0.0 }', "  },", '  "urgent": { "type": "noul",', '              "noul": 1.0 }', "}",
];
const CODE = ['d = answers["department"]', "", 'if d["confidence"] >= 0.7:', '    route(d["choice"])', "else:", "    ask_a_human()"];
const S14: React.FC = () => {
  const t = useT();
  return (
    <>
      <Title text="Live demo: response" />
      <Tag x={100} y={745} text="EMULATOR output, not real Jev" size={32} p={t.p(0, 24, 14)} />
      <Txt x={100} y={815} text="A free LLM behind a Jev-shaped endpoint (workshop-lite/sample_output.txt)" size={30} color={SLATE} p={t.p(0, 30, 14)} />
      <CodePanel x={100} y={215} w={720} lines={RESP} size={26} hl={{ 3: ACC_L }} p={t.p(1, 0, 60, linearEase)} marks={[{ from: 3, to: 4, m: t.p(2, 2, 16) }]} />
      <Arr pts={[[850, 450], [960, 450]]} color={ACC} p={t.p(2, 0, 14)} />
      <Rect x={980} y={215} w={520} h={300} fill={WHITE} stroke={ACC} sw={3} p={t.p(2, 8, 18)} />
      {CODE.map((ln, i) =>
        ln ? <Txt key={i} x={1005} y={240 + i * 38} text={ln} size={26} mono color={i === 2 ? ACC : NAVY} p={t.p(2, 16 + i * 5, 10)} anim="fade" /> : null,
      )}
      <Txt x={1240} y={570} text="our code decides" size={42} color={ACC} anchor="center" align="center" p={t.p(2, 46, 16)} />
      <PageNum n={14} />
    </>
  );
};

// 15 ------------------------------------------------------------------
const S15: React.FC = () => {
  const t = useT();
  return (
    <>
      <Title text="Use it. Skip it." />
      <Rect x={100} y={230} w={680} h={520} fill={ACC_L} stroke={ACC} sw={3} p={t.p(1, 0, 18)} />
      <Txt x={140} y={255} text="Use it for" size={50} color={ACC} p={t.p(1, 8, 14)} />
      {["sorting", "yes / no checks", "high volume", "fast answers"].map((s, i) => (
        <React.Fragment key={s}>
          <Check x={150} y={360 + i * 92} k={0.7} color={ACC} sw={6} p={t.p(1, 16 + i * 8, 12)} />
          <Txt x={215} y={352 + i * 92} text={s} size={44} p={t.p(1, 18 + i * 8, 12)} />
        </React.Fragment>
      ))}
      <Rect x={820} y={230} w={680} h={520} fill={LIGHT} stroke={NAVY} sw={3} p={t.p(2, 0, 18)} />
      <Txt x={860} y={255} text="Skip it for" size={50} color={SLATE} p={t.p(2, 8, 14)} />
      {["writing text", "explaining why", "multi-step reasoning", "open chat"].map((s, i) => (
        <React.Fragment key={s}>
          <Cross x={860} y={360 + i * 92} k={0.7} color={SLATE} sw={6} p={t.p(2, 16 + i * 8, 12)} />
          <Txt x={935} y={352 + i * 92} text={s} size={44} p={t.p(2, 18 + i * 8, 12)} />
        </React.Fragment>
      ))}
      <PageNum n={15} />
    </>
  );
};

// 16 ------------------------------------------------------------------
const S16: React.FC = () => {
  const t = useT();
  const lim: [string, string][] = [
    ["Text first", "no audio, no video"], ["English works best", "other languages weaker"],
    ["Test on your data", "check the probabilities"], ["Vendor numbers", "are claims, not proof"],
  ];
  return (
    <>
      <Title text="Honest limits" />
      {lim.map(([a, b], i) => {
        const x = 100 + (i % 2) * 740;
        const y = 240 + Math.floor(i / 2) * 270;
        const k = i + 1;
        return (
          <React.Fragment key={a}>
            <Rect x={x} y={y} w={700} h={230} fill={LIGHT} stroke={NAVY} sw={3} p={t.p(k, 0, 16)} />
            <Line pts={[[x + 28, y + 40], [x + 30, y + 120], [x + 27, y + 190]]} stroke={ACC} sw={6} p={t.p(k, 8, 14)} />
            <Txt x={x + 50} y={y + 55} text={a} size={52} p={t.p(k, 10, 14)} />
            <Txt x={x + 50} y={y + 130} text={b} size={38} color={SLATE} p={t.p(k, 16, 14)} />
          </React.Fragment>
        );
      })}
      <PageNum n={16} />
    </>
  );
};

// 17 ------------------------------------------------------------------
const S17: React.FC = () => {
  const t = useT();
  const items = ["Right model\nfor the job", "The model answers,\nyour code decides", "Fast first,\nbig model if unsure"];
  return (
    <>
      <Title text="Three takeaways" />
      {items.map((s, i) => {
        const x = 100 + i * 490;
        const k = i + 1;
        return (
          <React.Fragment key={s}>
            <Ellipse x={x + 150} y={250} w={120} h={120} fill={ACC_L} stroke={ACC} sw={4} p={t.p(k, 0, 18)} />
            <Txt x={x + 210} y={312} text={`${k}`} size={72} color={ACC} anchor="center" align="center" p={t.p(k, 8, 12)} />
            <Rect x={x} y={420} w={420} h={260} fill={LIGHT} stroke={NAVY} sw={3} p={t.p(k, 10, 18)} />
            <Txt x={x + 210} y={550} text={s} size={38} anchor="center" align="center" p={t.p(k, 20, 14)} />
          </React.Fragment>
        );
      })}
      <PageNum n={17} />
    </>
  );
};

// 18 ------------------------------------------------------------------
const S18: React.FC = () => {
  const t = useT();
  return (
    <>
      <Title text="Try it yourself" />
      <Txt x={100} y={250} text={REPO} size={44} color={ACC} p={t.p(0, 20, 24)} anim="wipe" />
      <Txt x={100} y={315} text="→ system-one-models/" size={40} p={t.p(0, 32, 14)} />
      <Rect x={1030} y={230} w={460} h={460} fill={WHITE} stroke={NAVY} sw={3} p={t.p(0, 24, 20)} />
      <g opacity={t.p(0, 36, 18)}>
        <foreignObject x={1050} y={250} width={420} height={420}>
          <Img src={qr} style={{ width: 420, height: 420, display: "block", imageRendering: "pixelated" }} />
        </foreignObject>
      </g>
      <Txt x={1260} y={740} text="scan me" size={38} color={SLATE} anchor="center" align="center" p={t.p(0, 46, 14)} />
      {["Run the workshop", "Poke the API calls", "Compare the approaches", "Read the sources"].map((s, i) => (
        <React.Fragment key={s}>
          <Ellipse x={110} y={440 + i * 85 + 12} w={26} h={26} fill={ACC} stroke={ACC} sw={2} p={t.p(1, i * 8, 12)} />
          <Txt x={165} y={438 + i * 85} text={s} size={48} p={t.p(1, i * 8 + 4, 14)} />
        </React.Fragment>
      ))}
      <PageNum n={18} />
    </>
  );
};

// 19 ------------------------------------------------------------------
const S19: React.FC = () => {
  const t = useT();
  return (
    <>
      <Txt x={800} y={380} text="Questions?" size={140} anchor="center" align="center" p={t.p(0, 6, 30)} anim="wipe" />
      <Line pts={[[430, 480], [800, 486], [1170, 479]]} stroke={ACC} sw={7} p={t.p(0, 26, 22)} />
      <Txt x={800} y={600} text="System One models · Jev" size={40} color={SLATE} anchor="center" align="center" p={t.p(0, 40, 18)} />
      <PageNum n={19} />
    </>
  );
};

const S01WithNum: React.FC = () => (
  <>
    <S01 />
    <PageNum n={1} />
  </>
);

export const SLIDES: SlideDef[] = [
  { id: "title", title: "Title", steps: [100], enter: "fade", Component: S01WithNum },
  { id: "two-kinds-of-models", title: "Two kinds of AI models", steps: [40, 60, 60, 30], enter: "slide", Component: S02 },
  { id: "fast-and-slow", title: "Two ways to think", steps: [40, 45, 45, 40], enter: "fade", Component: S03 },
  { id: "what-is-jev", title: "What is Jev?", steps: [44, 40, 60], enter: "slide", Component: S04 },
  { id: "one-call-one-decision", title: "One call, one decision", steps: [44, 40, 50, 70], enter: "fade", Component: S05 },
  { id: "three-kinds-of-questions", title: "Three kinds of questions", steps: [40, 55, 50, 50], enter: "fade", Component: S06 },
  { id: "not-only-jev", title: "Not only Jev", steps: [40, 34, 60], enter: "fade", Component: S07 },
  { id: "where-it-fits", title: "Where it fits", steps: [40, 80], enter: "fade", Component: S08 },
  { id: "use-case-routing", title: "Routing", steps: [44, 40, 56, 44], enter: "slide", Component: S09 },
  { id: "use-case-moderation", title: "Moderation", steps: [44, 44, 56, 50], enter: "fade", Component: S10 },
  { id: "use-case-fraud-triage", title: "Fraud triage", steps: [44, 64, 40, 50], enter: "fade", Component: S11 },
  { id: "fast-first", title: "Fast first", steps: [40, 54, 40, 56], enter: "fade", Component: S12 },
  { id: "live-demo-request", title: "Live demo: request", steps: [44, 70, 34, 40], enter: "slide", Component: S13 },
  { id: "live-demo-response", title: "Live demo: response", steps: [44, 64, 70], enter: "fade", Component: S14 },
  { id: "use-it-skip-it", title: "Use it. Skip it.", steps: [40, 56, 56], enter: "slide", Component: S15 },
  { id: "honest-limits", title: "Honest limits", steps: [40, 34, 34, 34, 34], enter: "fade", Component: S16 },
  { id: "three-takeaways", title: "Three takeaways", steps: [40, 40, 40, 40], enter: "slide", Component: S17 },
  { id: "try-it-yourself", title: "Try it yourself", steps: [70, 50], enter: "fade", Component: S18 },
  { id: "questions", title: "Questions?", steps: [70], enter: "fade", Component: S19 },
];
