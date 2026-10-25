// Hand-drawn primitives: roughjs (the renderer Excalidraw uses) -> SVG paths, animated by progress p (0..1).
import React, { useId, useMemo } from "react";
import rough from "roughjs";
import type { Drawable, Options } from "roughjs/bin/core";
import { clamp01, seg } from "./anim";
import { measure } from "./fonts";
import { HAND, LINE_H, MONO, NAVY } from "./theme";

const gen = rough.generator();
type Pt = [number, number];

function hash(s: string): number {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619);
  return (h >>> 0) % 2147483647 || 1;
}

type Style = {
  stroke?: string;
  sw?: number;
  fill?: string;
  fillStyle?: "solid" | "hachure";
  dashed?: boolean;
  roughness?: number;
};

function options(key: string, st: Style): Options {
  const sw = st.sw ?? 3;
  return {
    seed: hash(key),
    roughness: st.roughness ?? 1,
    bowing: 1,
    stroke: st.stroke ?? NAVY,
    strokeWidth: sw,
    fill: st.fill && st.fill !== "transparent" ? st.fill : undefined,
    fillStyle: st.fillStyle ?? "solid",
    fillWeight: sw / 2,
    hachureGap: sw * 4,
    hachureAngle: -41,
    disableMultiStroke: !!st.dashed,
    preserveVertices: true,
    curveFitting: 1,
  };
}

const memo = new Map<string, Drawable>();
function draw(key: string, make: () => Drawable): Drawable {
  let d = memo.get(key);
  if (!d) {
    d = make();
    memo.set(key, d);
  }
  return d;
}

/** Renders a rough drawable: outline strokes "draw on", fills fade in. */
export const Rough: React.FC<{ d: Drawable; p: number; dashed?: boolean; opacity?: number; fillFrom?: number }> = ({
  d,
  p,
  dashed,
  opacity = 1,
  fillFrom = 0.35,
}) => {
  const id = useId().replace(/:/g, "");
  if (p <= 0) return null;
  const o = d.options;
  const po = clamp01(p / 0.85);
  const pf = seg(p, fillFrom, 1);
  const fills: React.ReactNode[] = [];
  const outlines: string[] = [];
  d.sets.forEach((set) => {
    const path = gen.opsToPath(set, 2);
    if (set.type === "fillPath") fills.push(<path key={fills.length} d={path} fill={o.fill} stroke="none" opacity={pf} />);
    else if (set.type === "fillSketch")
      fills.push(
        <path key={fills.length} d={path} fill="none" stroke={o.fill} strokeWidth={o.fillWeight} strokeLinecap="round" opacity={pf} />,
      );
    else outlines.push(...path.split(/(?=M)/).filter((x) => x.trim()));
  });
  const common = { fill: "none", stroke: o.stroke, strokeWidth: o.strokeWidth, strokeLinecap: "round" as const, strokeLinejoin: "round" as const };
  let lines: React.ReactNode;
  if (dashed) {
    const dash = `8 ${8 + o.strokeWidth}`;
    lines = (
      <>
        {po < 1 && (
          <mask id={`m${id}`} maskUnits="userSpaceOnUse" x={-200} y={-200} width={2000} height={1300}>
            {outlines.map((s, i) => (
              <path key={i} d={s} fill="none" stroke="#fff" strokeWidth={o.strokeWidth * 4} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - po} />
            ))}
          </mask>
        )}
        <g mask={po < 1 ? `url(#m${id})` : undefined}>
          {outlines.map((s, i) => (
            <path key={i} d={s} {...common} strokeDasharray={dash} />
          ))}
        </g>
      </>
    );
  } else {
    lines = outlines.map((s, i) =>
      po >= 1 ? (
        <path key={i} d={s} {...common} />
      ) : (
        <path key={i} d={s} {...common} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - po} />
      ),
    );
  }
  return (
    <g opacity={opacity}>
      {fills}
      {lines}
    </g>
  );
};

type ShapeProps = Style & { p: number; opacity?: number; fillFrom?: number };

/** Excalidraw rectangle; round = adaptive radius like Excalidraw's roundness type 3. */
export const Rect: React.FC<ShapeProps & { x: number; y: number; w: number; h: number; round?: boolean }> = ({
  x, y, w, h, round = true, p, opacity, fillFrom, ...st
}) => {
  const key = `rect|${x}|${y}|${w}|${h}|${round}|${JSON.stringify(st)}`;
  const d = draw(key, () => {
    const o = options(key, st);
    if (!round) return gen.rectangle(x, y, w, h, o);
    const m = Math.min(w, h);
    const r = m <= 128 ? m * 0.25 : 32;
    const path = `M ${x + r} ${y} L ${x + w - r} ${y} Q ${x + w} ${y}, ${x + w} ${y + r} L ${x + w} ${y + h - r} Q ${x + w} ${y + h}, ${x + w - r} ${y + h} L ${x + r} ${y + h} Q ${x} ${y + h}, ${x} ${y + h - r} L ${x} ${y + r} Q ${x} ${y}, ${x + r} ${y}`;
    return gen.path(path, o);
  });
  return <Rough d={d} p={p} dashed={st.dashed} opacity={opacity} fillFrom={fillFrom} />;
};

export const Ellipse: React.FC<ShapeProps & { x: number; y: number; w: number; h: number }> = ({ x, y, w, h, p, opacity, fillFrom, ...st }) => {
  const key = `ell|${x}|${y}|${w}|${h}|${JSON.stringify(st)}`;
  const d = draw(key, () => gen.ellipse(x + w / 2, y + h / 2, w, h, options(key, st)));
  return <Rough d={d} p={p} dashed={st.dashed} opacity={opacity} fillFrom={fillFrom} />;
};

/** Polyline; curved (Excalidraw roundness 2) when it has more than 2 points, closed -> polygon. */
export const Line: React.FC<ShapeProps & { pts: Pt[]; curved?: boolean; closed?: boolean }> = ({
  pts, curved = true, closed = false, p, opacity, fillFrom, ...st
}) => {
  const key = `line|${JSON.stringify(pts)}|${curved}|${closed}|${JSON.stringify(st)}`;
  const d = draw(key, () => {
    const o = options(key, st);
    if (closed) return gen.polygon(pts, o);
    if (pts.length === 2) return gen.line(pts[0][0], pts[0][1], pts[1][0], pts[1][1], o);
    return curved ? gen.curve(pts, o) : gen.linearPath(pts, o);
  });
  return <Rough d={d} p={p} dashed={st.dashed} opacity={opacity} fillFrom={fillFrom} />;
};

function headPts(tip: Pt, from: Pt, sw: number): [Pt, Pt] {
  const ang = Math.atan2(tip[1] - from[1], tip[0] - from[0]);
  const len = Math.hypot(tip[0] - from[0], tip[1] - from[1]);
  const L = Math.min(22 + sw * 1.5, len * 0.5);
  const a = (25 * Math.PI) / 180;
  return [
    [tip[0] - L * Math.cos(ang - a), tip[1] - L * Math.sin(ang - a)],
    [tip[0] - L * Math.cos(ang + a), tip[1] - L * Math.sin(ang + a)],
  ];
}

/** point at fraction f along a polyline */
export function along(pts: Pt[], f: number): Pt {
  const segs = pts.slice(1).map((q, i) => Math.hypot(q[0] - pts[i][0], q[1] - pts[i][1]));
  let d = clamp01(f) * segs.reduce((a, b) => a + b, 0);
  for (let i = 0; i < segs.length; i++) {
    if (d <= segs[i] || i === segs.length - 1) {
      const k = segs[i] ? Math.min(1, d / segs[i]) : 0;
      return [pts[i][0] + (pts[i + 1][0] - pts[i][0]) * k, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * k];
    }
    d -= segs[i];
  }
  return pts[pts.length - 1];
}

/** Arrow: the shaft draws on, then the head(s). `pulse` (0..1) sends a small dot along it (gone at 0 and 1). */
export const Arrow: React.FC<
  Omit<ShapeProps, "fill" | "fillStyle"> & { pts: Pt[]; curved?: boolean; head?: boolean; tail?: boolean; pulse?: number; pulseColor?: string }
> = ({ pts, curved = true, head = true, tail = false, p, pulse = 0, pulseColor, opacity, ...st }) => {
  const sw = st.sw ?? 4;
  const s2 = { ...st, sw, dashed: false };
  const n = pts.length;
  const [h1, h2] = headPts(pts[n - 1], pts[n - 2], sw);
  const [t1, t2] = headPts(pts[0], pts[1], sw);
  const pd = seg(p, 0.75, 1);
  const dot = pulse > 0 && pulse < 1 ? along(pts, pulse) : null;
  return (
    <g opacity={opacity}>
      <Line pts={pts} curved={curved} p={seg(p, 0, 0.8)} {...st} sw={sw} />
      {head && <Line pts={[h1, pts[n - 1], h2]} curved={false} p={pd} {...s2} />}
      {tail && <Line pts={[t1, pts[0], t2]} curved={false} p={pd} {...s2} />}
      {dot && <circle cx={dot[0]} cy={dot[1]} r={9} fill={pulseColor ?? st.stroke ?? NAVY} opacity={Math.sin(Math.PI * pulse)} />}
    </g>
  );
};

type TxtProps = {
  x: number;
  y: number;
  text: string;
  size?: number;
  color?: string;
  align?: "left" | "center" | "right";
  /** "top": y is the top of the text box (Excalidraw s.text); "center": y is its centre (s.label) */
  anchor?: "top" | "center";
  mono?: boolean;
  p: number;
  anim?: "fade" | "wipe" | "rise";
  weight?: number;
};

/** Text placed like Excalidraw text elements (line height 1.25). */
export const Txt: React.FC<TxtProps> = ({ x, y, text, size = 48, color = NAVY, align = "left", anchor = "top", mono, p, anim = "rise" }) => {
  const id = useId().replace(/:/g, "");
  if (p <= 0) return null;
  const lines = text.split("\n");
  const lh = size * LINE_H;
  const top = anchor === "top" ? y : y - (lines.length * lh) / 2;
  const family = mono ? MONO : HAND;
  const anchorAttr = align === "left" ? "start" : align === "center" ? "middle" : "end";
  const content = lines.map((l, i) => (
    <text
      key={i}
      x={x}
      y={top + (i + 0.5) * lh + size * 0.02}
      fontFamily={family}
      fontSize={size}
      fill={color}
      textAnchor={anchorAttr}
      dominantBaseline="central"
      style={{ whiteSpace: "pre" }}
    >
      {l}
    </text>
  ));
  if (anim === "wipe" && p < 1) {
    const w = measure(text, size, mono ? MONO : undefined) + size;
    const left = align === "left" ? x : align === "center" ? x - w / 2 : x - w;
    return (
      <g>
        <clipPath id={`c${id}`} clipPathUnits="userSpaceOnUse">
          <rect x={left - size * 0.5} y={top - size} width={(w + size) * p} height={lines.length * lh + size * 2} />
        </clipPath>
        <g clipPath={`url(#c${id})`}>{content}</g>
      </g>
    );
  }
  const dy = anim === "rise" ? (1 - p) * 14 : 0;
  return (
    <g opacity={p} transform={dy ? `translate(0 ${dy})` : undefined}>
      {content}
    </g>
  );
};
