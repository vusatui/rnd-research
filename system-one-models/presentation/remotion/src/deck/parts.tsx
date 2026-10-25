// Composite doodles, 1:1 with the helpers in ../../serious/tools/build_deck.py, plus build animations.
import React from "react";
import { lerp, seg, useT } from "./anim";
import { measure } from "./fonts";
import { Arrow, Ellipse, Line, Rect, Txt } from "./shapes";
import { ACC, ACC_L, CODE_TEXT, LIGHT, MID, NAVY, SLATE, WHITE } from "./theme";

type Pt = [number, number];

/** Slide title + orange underline (step 0). */
export const Title: React.FC<{ text: string; sub?: string; subSize?: number }> = ({ text, sub, subSize = 36 }) => {
  const t = useT();
  const w = measure(text, 64);
  return (
    <>
      <Txt x={100} y={64} text={text} size={64} color={NAVY} p={t.p(0, 4, 24)} anim="wipe" />
      <Line pts={[[100, 140], [100 + w * 0.6, 142], [100 + w, 139]]} stroke={ACC} sw={5} p={t.p(0, 16, 20)} />
      {sub && <Txt x={100} y={165} text={sub} size={subSize} color={SLATE} p={t.p(0, 24, 16)} />}
    </>
  );
};

export const PageNum: React.FC<{ n: number }> = ({ n }) => {
  const t = useT();
  return <Txt x={1530} y={842} text={`${n}`} size={28} color={MID} align="right" p={t.p(0, 10, 14)} anim="fade" />;
};

export const Caption: React.FC<{ text: string; y?: number; color?: string; size?: number; x?: number; p: number }> = ({
  text, y = 800, color = SLATE, size = 38, x = 800, p,
}) => <Txt x={x} y={y} text={text} size={size} color={color} anchor="center" align="center" p={p} />;

export const Tag: React.FC<{ x: number; y: number; text: string; color?: string; size?: number; p: number }> = ({
  x, y, text, color = ACC, size = 28, p,
}) => {
  const w = measure(text, size);
  const h = size * 1.25;
  return (
    <>
      <Rect x={x} y={y} w={w + 36} h={h + 14} fill={WHITE} stroke={color} sw={2} dashed p={p} />
      <Txt x={x + 18} y={y + 7} text={text} size={size} color={color} p={seg(p, 0.3, 1)} anim="fade" />
    </>
  );
};

export const Box: React.FC<{
  x: number; y: number; w: number; h: number; text: string; size?: number;
  fill?: string; stroke?: string; color?: string; p: number;
}> = ({ x, y, w, h, text, size = 40, fill = LIGHT, stroke = NAVY, color = NAVY, p }) => (
  <>
    <Rect x={x} y={y} w={w} h={h} fill={fill} stroke={stroke} sw={3} p={p} />
    <Txt x={x + w / 2} y={y + h / 2} text={text} size={size} color={color} anchor="center" align="center" p={seg(p, 0.4, 1)} />
  </>
);

export const Arr: React.FC<{ pts: Pt[]; color?: string; sw?: number; p: number; dashed?: boolean; curved?: boolean; tail?: boolean; pulse?: number }> = ({
  pts, color = NAVY, sw = 4, ...rest
}) => <Arrow pts={pts} stroke={color} sw={sw} {...rest} />;

// ---------- doodle icons ----------
export const Doc: React.FC<{ x: number; y: number; w?: number; h?: number; lines?: number; color?: string; fill?: string; p: number }> = ({
  x, y, w = 100, h = 130, lines = 4, color = NAVY, fill = WHITE, p,
}) => (
  <>
    <Rect x={x} y={y} w={w} h={h} fill={fill} stroke={color} sw={3} round={false} p={seg(p, 0, 0.6)} />
    {Array.from({ length: lines }, (_, i) => {
      const ln = i < lines - 1 ? w - 36 : (w - 36) * 0.6;
      const a = 0.35 + (i * 0.55) / lines;
      return <Line key={i} pts={[[x + 18, y + 28 + i * 24], [x + 18 + ln, y + 28 + i * 24]]} stroke={SLATE} sw={3} p={seg(p, a, a + 0.3)} />;
    })}
  </>
);

export const Person: React.FC<{ cx: number; y: number; k?: number; color?: string; p: number }> = ({ cx, y, k = 1, color = NAVY, p }) => (
  <>
    <Ellipse x={cx - 20 * k} y={y} w={40 * k} h={40 * k} stroke={color} sw={3} p={seg(p, 0, 0.5)} />
    <Line
      pts={[[cx - 36 * k, y + 110 * k], [cx - 36 * k, y + 70 * k], [cx, y + 55 * k], [cx + 36 * k, y + 70 * k], [cx + 36 * k, y + 110 * k]]}
      stroke={color} sw={3} p={seg(p, 0.35, 1)}
    />
  </>
);

export const Chip: React.FC<{ x: number; y: number; w: number; h: number; p: number }> = ({ x, y, w, h, p }) => {
  const pins: Pt[][] = [];
  for (let i = 1; i < 4; i++) {
    const px = x + (w * i) / 4;
    const py = y + (h * i) / 4;
    pins.push([[px, y - 16], [px, y]], [[px, y + h], [px, y + h + 16]], [[x - 16, py], [x, py]], [[x + w, py], [x + w + 16, py]]);
  }
  return (
    <>
      {pins.map((pt, i) => (
        <Line key={i} pts={pt} stroke={NAVY} sw={3} p={seg(p, 0.4 + i * 0.04, 0.6 + i * 0.04)} />
      ))}
      <Rect x={x} y={y} w={w} h={h} fill={LIGHT} stroke={NAVY} sw={3} p={seg(p, 0, 0.6)} />
    </>
  );
};

/** Bar chart; bars grow from the baseline. */
export const Bars: React.FC<{ x: number; y: number; vals: number[]; bw?: number; hmax?: number; hi?: number; p: number }> = ({
  x, y, vals, bw = 34, hmax = 100, hi = 0, p,
}) => (
  <>
    <Line pts={[[x - 8, y + hmax], [x + vals.length * (bw + 12), y + hmax]]} stroke={NAVY} sw={3} p={seg(p, 0, 0.3)} />
    {vals.map((v, i) => {
      const bh = Math.max(6, hmax * v);
      const g = seg(p, 0.2 + i * 0.12, 0.65 + i * 0.12);
      if (g <= 0) return null;
      const c = i === hi ? ACC : NAVY;
      // grow: reveal from the baseline up (the hand-drawn bar itself is drawn once at full size)
      const bx = x + i * (bw + 12);
      return (
        <g key={i}>
          <clipPath id={`b${x}_${y}_${i}`} clipPathUnits="userSpaceOnUse">
            <rect x={bx - 10} y={y + hmax + 6 - (bh + 16) * g} width={bw + 20} height={(bh + 16) * g} />
          </clipPath>
          <g clipPath={`url(#b${x}_${y}_${i})`}>
            <Rect x={bx} y={y + hmax - bh} w={bw} h={bh} fill={i === hi ? ACC_L : MID} stroke={c} sw={3} fillStyle="hachure" round={false} p={1} />
          </g>
        </g>
      );
    })}
  </>
);

export const Check: React.FC<{ x: number; y: number; k?: number; color?: string; sw?: number; p: number }> = ({ x, y, k = 1, color = ACC, sw = 7, p }) => (
  <Line pts={[[x, y + 28 * k], [x + 22 * k, y + 52 * k], [x + 62 * k, y]]} stroke={color} sw={sw} p={p} />
);

export const Cross: React.FC<{ x: number; y: number; k?: number; color?: string; sw?: number; p: number }> = ({ x, y, k = 1, color = SLATE, sw = 7, p }) => (
  <>
    <Line pts={[[x, y], [x + 50 * k, y + 50 * k]]} stroke={color} sw={sw} p={seg(p, 0, 0.55)} />
    <Line pts={[[x + 50 * k, y], [x, y + 50 * k]]} stroke={color} sw={sw} p={seg(p, 0.45, 1)} />
  </>
);

export const Bolt: React.FC<{ x: number; y: number; k?: number; p: number }> = ({ x, y, k = 1, p }) => {
  const pts: Pt[] = [[0, 0], [60, 0], [35, 55], [80, 55], [10, 150], [28, 75], [-10, 75]];
  return <Line pts={pts.map(([px, py]) => [x + px * k, y + py * k] as Pt)} closed stroke={ACC} fill={ACC_L} fillStyle="hachure" sw={3} p={p} />;
};

export const Magnifier: React.FC<{ x: number; y: number; k?: number; color?: string; p: number }> = ({ x, y, k = 1, color = NAVY, p }) => (
  <>
    <Ellipse x={x} y={y} w={56 * k} h={56 * k} stroke={color} sw={4} p={seg(p, 0, 0.65)} />
    <Line pts={[[x + 50 * k, y + 50 * k], [x + 84 * k, y + 84 * k]]} stroke={color} sw={7} p={seg(p, 0.6, 1)} />
  </>
);

export const Shield: React.FC<{ x: number; y: number; k?: number; p: number }> = ({ x, y, k = 1, p }) => (
  <>
    <Line
      pts={[[x, y], [x + 70 * k, y + 14 * k], [x + 140 * k, y], [x + 136 * k, y + 70 * k], [x + 70 * k, y + 130 * k], [x + 4 * k, y + 70 * k]]}
      closed stroke={NAVY} fill={LIGHT} sw={4} p={seg(p, 0, 0.7)}
    />
    <Check x={x + 40 * k} y={y + 40 * k} k={0.9 * k} color={ACC} sw={6} p={seg(p, 0.6, 1)} />
  </>
);

export const Fork: React.FC<{ x: number; y: number; p: number }> = ({ x, y, p }) => (
  <>
    <Arr pts={[[x, y + 40], [x + 40, y + 40], [x + 40, y + 8], [x + 90, y + 8]]} p={seg(p, 0, 0.7)} />
    <Arr pts={[[x + 40, y + 40], [x + 90, y + 40]]} p={seg(p, 0.15, 0.85)} />
    <Arr pts={[[x + 40, y + 40], [x + 40, y + 72], [x + 90, y + 72]]} color={ACC} p={seg(p, 0.3, 1)} />
  </>
);

/** Horizontal gauge; the fill grows to `level`, optional dashed threshold. */
export const Gauge: React.FC<{ x: number; y: number; w?: number; level?: number; thr?: number; p: number }> = ({ x, y, w = 240, level = 0.7, thr, p }) => {
  const g = seg(p, 0.3, 1);
  const fw = (w - 6) * level;
  return (
    <>
      <Rect x={x} y={y} w={w} h={26} fill={WHITE} stroke={NAVY} sw={3} p={seg(p, 0, 0.35)} />
      {g > 0 && (
        <g>
          <clipPath id={`g${x}_${y}`} clipPathUnits="userSpaceOnUse">
            <rect x={x} y={y - 5} width={3 + fw * g + 4} height={40} />
          </clipPath>
          <g clipPath={`url(#g${x}_${y})`}>
            <Rect x={x + 3} y={y + 3} w={fw} h={20} fill={ACC_L} stroke={ACC} sw={2} fillStyle="hachure" round={false} p={1} />
          </g>
        </g>
      )}
      {thr !== undefined && <Line pts={[[x + w * thr, y - 18], [x + w * thr, y + 44]]} stroke={NAVY} sw={4} dashed p={seg(p, 0.15, 0.5)} />}
    </>
  );
};

/** Dark code panel; lines appear one after another while p goes 0..1. hl = {line: colour};
 *  marks = line ranges outlined in orange (progress m: 0..1) to point at a part of the code. */
export const CodePanel: React.FC<{
  x: number; y: number; w: number; lines: string[]; size?: number; pad?: number; hl?: Record<number, string>; p: number;
  marks?: { from: number; to: number; m: number }[];
}> = ({ x, y, w, lines, size = 30, pad = 28, hl = {}, p, marks = [] }) => {
  const lh = size * 1.3;
  const h = lines.length * lh + pad * 2;
  const n = lines.length;
  return (
    <>
      <Rect x={x} y={y} w={w} h={h} fill={NAVY} stroke={NAVY} sw={3} p={seg(p, 0, 0.3)} fillFrom={0} />
      {marks.map(({ from, to, m }, i) =>
        m > 0 ? (
          <Rect key={`m${i}`} x={x + pad - 12} y={y + pad + from * lh + 3} w={w - 2 * pad + 24} h={(to - from + 1) * lh - 4}
            stroke={ACC} sw={2.5} p={m} roughness={0.4} />
        ) : null,
      )}
      {lines.map((ln, i) => {
        const a = 0.2 + (0.75 * i) / n;
        const lp = seg(p, a, a + 0.12);
        return ln ? <Txt key={i} x={x + pad} y={y + pad + i * lh} text={ln} size={size} mono color={hl[i] ?? CODE_TEXT} p={lp} anim="fade" /> : null;
      })}
    </>
  );
};

export const codePanelHeight = (n: number, size = 30, pad = 28) => n * size * 1.3 + pad * 2;
export { lerp };
