import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Player, type PlayerRef } from "@remotion/player";
import { Deck } from "../deck/Deck";
import { loadFonts } from "../deck/fonts";
import { SLIDES } from "../deck/slides";
import { FPS, VIDEO_H, VIDEO_W } from "../deck/theme";
import { computeTimeline } from "../deck/timeline";
import { Md, NOTES } from "./notes";

type Pos = { s: number; k: number };
const TL = computeTimeline(undefined, 0);
const target = ({ s, k }: Pos) => TL.slides[s].start + TL.slides[s].stepEnds[k];
const lastStep = (s: number) => SLIDES[s].steps.length - 1;
const clampPos = (s: number, k: number): Pos => {
  const ss = Math.max(0, Math.min(SLIDES.length - 1, s));
  return { s: ss, k: Math.max(0, Math.min(lastStep(ss), k)) };
};

function parseHash(): Pos | null {
  const m = location.hash.match(/^#(\d+)(?:\.(\d+))?/);
  return m ? clampPos(Number(m[1]) - 1, m[2] ? Number(m[2]) : 0) : null;
}

const inputProps = { hold: 0 };

declare global {
  interface Window {
    __deck?: {
      goto: (slide: number, step?: number) => void;
      next: () => void;
      prev: () => void;
      state: () => Pos & { frame: number; target: number; playing: boolean };
      steps: number[];
    };
  }
}

export const Presenter: React.FC = () => {
  const player = useRef<PlayerRef>(null);
  const [fontsReady, setFontsReady] = useState(false);
  const [pos, setPos] = useState<Pos>(() => parseHash() ?? { s: 0, k: 0 });
  const posRef = useRef(pos);
  const pending = useRef<number | null>(null);
  const [notesOpen, setNotesOpen] = useState(() => new URLSearchParams(location.search).has("notes"));
  const [hud, setHud] = useState(true);
  const [help, setHelp] = useState(false);
  const [fontScale, setFontScale] = useState(1);
  const [startedAt, setStartedAt] = useState<number | null>(null);
  const [now, setNow] = useState(Date.now());
  const typed = useRef("");
  const hudTimer = useRef<number>(0);
  const playing = useRef(false);

  useEffect(() => {
    loadFonts().then(() => setFontsReady(true));
  }, []);

  const showHud = useCallback(() => {
    setHud(true);
    window.clearTimeout(hudTimer.current);
    hudTimer.current = window.setTimeout(() => setHud(false), 3500);
  }, []);

  /** go to a position: animate when it is the very next step, jump otherwise */
  const go = useCallback((next: Pos, animate: boolean) => {
    const p = player.current;
    if (!p) return;
    const from = posRef.current;
    posRef.current = next;
    setPos(next);
    history.replaceState(null, "", `#${next.s + 1}.${next.k}`);
    const to = target(next);
    if (animate && to > target(from)) {
      p.seekTo(target(from));
      pending.current = to;
      playing.current = true;
      p.play();
    } else {
      pending.current = null;
      playing.current = false;
      p.pause();
      p.seekTo(to);
    }
  }, []);

  const finishPending = useCallback(() => {
    const p = player.current;
    if (p && pending.current !== null) {
      const to = pending.current;
      pending.current = null;
      playing.current = false;
      p.pause();
      p.seekTo(to);
      return true;
    }
    return false;
  }, []);

  const next = useCallback(() => {
    if (finishPending()) return; // a click during an animation completes it
    setStartedAt((t) => t ?? Date.now());
    const { s, k } = posRef.current;
    if (k < lastStep(s)) go({ s, k: k + 1 }, true);
    else if (s < SLIDES.length - 1) go({ s: s + 1, k: 0 }, true);
  }, [go, finishPending]);

  const prev = useCallback(() => {
    finishPending();
    const { s, k } = posRef.current;
    if (k > 0) go({ s, k: k - 1 }, false);
    else if (s > 0) go({ s: s - 1, k: lastStep(s - 1) }, false);
  }, [go, finishPending]);

  // stop exactly at the end of the step
  useEffect(() => {
    const p = player.current;
    if (!p) return;
    const onFrame = (e: { detail: { frame: number } }) => {
      if (pending.current !== null && e.detail.frame >= pending.current) finishPending();
    };
    const onEnded = () => finishPending();
    p.addEventListener("frameupdate", onFrame);
    p.addEventListener("ended", onEnded);
    return () => {
      p.removeEventListener("frameupdate", onFrame);
      p.removeEventListener("ended", onEnded);
    };
  }, [fontsReady, finishPending]);

  // initial position
  useEffect(() => {
    if (fontsReady) {
      const id = requestAnimationFrame(() => go(posRef.current, false));
      return () => cancelAnimationFrame(id);
    }
  }, [fontsReady, go]);

  useEffect(() => {
    window.__deck = {
      goto: (s, k = 0) => go(clampPos(s - 1, k < 0 ? 99 : k), false),
      next,
      prev,
      state: () => ({ ...posRef.current, frame: player.current?.getCurrentFrame() ?? -1, target: target(posRef.current), playing: playing.current }),
      steps: SLIDES.map((d) => d.steps.length),
    };
  }, [go, next, prev]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const key = e.key;
      if (/^\d$/.test(key)) {
        typed.current = (typed.current + key).slice(-2);
        return;
      }
      let handled = true;
      switch (key) {
        case "ArrowRight": case "ArrowDown": case "PageDown": case " ": case "l": case "j":
          if (key === " " && e.shiftKey) prev();
          else next();
          break;
        case "Enter":
          if (typed.current) {
            go(clampPos(Number(typed.current) - 1, 0), false);
            typed.current = "";
          } else next();
          break;
        case "ArrowLeft": case "ArrowUp": case "PageUp": case "Backspace": case "h": case "k":
          prev();
          break;
        case "Home":
          go({ s: 0, k: 0 }, false);
          break;
        case "End":
          go({ s: SLIDES.length - 1, k: lastStep(SLIDES.length - 1) }, false);
          break;
        case "f": case "F":
          if (document.fullscreenElement) document.exitFullscreen();
          else document.documentElement.requestFullscreen().catch(() => {});
          break;
        case "n": case "N":
          setNotesOpen((v) => !v);
          break;
        case "?":
          setHelp((v) => !v);
          break;
        case "+": case "=":
          setFontScale((v) => Math.min(2, v + 0.1));
          break;
        case "-":
          setFontScale((v) => Math.max(0.6, v - 0.1));
          break;
        case "t": case "T":
          setStartedAt(Date.now());
          break;
        case "Escape":
          setHelp(false);
          break;
        default:
          handled = false;
      }
      if (key !== "Enter") typed.current = "";
      if (handled) {
        e.preventDefault();
        showHud();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [next, prev, go, showHud]);

  useEffect(() => {
    const onHash = () => {
      const p = parseHash();
      if (p && (p.s !== posRef.current.s || p.k !== posRef.current.k)) go(p, false);
    };
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, [go]);

  useEffect(() => {
    showHud();
    const id = window.setInterval(() => setNow(Date.now()), 1000);
    return () => window.clearInterval(id);
  }, [showHud]);

  const def = SLIDES[pos.s];
  const note = NOTES.slides[pos.s];
  const nSteps = def.steps.length;
  const elapsed = startedAt ? Math.floor((now - startedAt) / 1000) : 0;
  const clock = `${Math.floor(elapsed / 60)}:${String(elapsed % 60).padStart(2, "0")}`;

  const player_ = useMemo(
    () =>
      fontsReady ? (
        <Player
          ref={player}
          component={Deck}
          inputProps={inputProps}
          durationInFrames={TL.total}
          fps={FPS}
          compositionWidth={VIDEO_W}
          compositionHeight={VIDEO_H}
          controls={false}
          clickToPlay={false}
          doubleClickToFullscreen={false}
          spaceKeyToPlayOrPause={false}
          moveToBeginningWhenEnded={false}
          initialFrame={target(posRef.current)}
          acknowledgeRemotionLicense
          style={{ width: "100%", height: "100%" }}
        />
      ) : null,
    [fontsReady],
  );

  return (
    <div className={`app ${notesOpen ? "with-notes" : ""}`} onMouseMove={showHud}>
      <div
        className="stage-wrap"
        onClick={(e) => (e.shiftKey ? prev() : next())}
        onContextMenu={(e) => {
          e.preventDefault();
          prev();
        }}
      >
        <div className="stage">{player_}</div>
      </div>

      <div className={`counter ${hud ? "" : "dim"}`}>
        {pos.s + 1} / {SLIDES.length}
        {nSteps > 1 && (
          <span className="dots">
            {Array.from({ length: nSteps - 1 }, (_, i) => (
              <i key={i} className={i < pos.k ? "on" : ""} />
            ))}
          </span>
        )}
      </div>
      <div className={`hint ${hud ? "" : "hidden"}`}>
        → / space / click: next · ←: back · f: fullscreen · n: notes · ?: help
      </div>

      {help && (
        <div className="help" onClick={() => setHelp(false)}>
          <h2>Keys</h2>
          <table>
            <tbody>
              <tr><td>→ ↓ Space PageDown, click</td><td>next build step, then next slide</td></tr>
              <tr><td>← ↑ Backspace PageUp, right-click</td><td>back one step</td></tr>
              <tr><td>Home / End</td><td>first / last slide</td></tr>
              <tr><td>number + Enter</td><td>jump to slide</td></tr>
              <tr><td>f</td><td>fullscreen</td></tr>
              <tr><td>n</td><td>speaker notes (+ / − text size, t restart timer)</td></tr>
              <tr><td>?</td><td>this help</td></tr>
            </tbody>
          </table>
        </div>
      )}

      {notesOpen && (
        <aside className="notes" style={{ fontSize: `${18 * fontScale}px` }}>
          <header>
            <div>
              <b>Slide {note.n} · {note.title}</b> · {note.time}
            </div>
            <div className="meta">
              step {pos.k}/{nSteps - 1} · ⏱ {clock}
              {pos.s < SLIDES.length - 1 && <> · next: {SLIDES[pos.s + 1].title}</>}
            </div>
          </header>
          <div className="body">
            {note.paragraphs.map((p, i) => (
              <p key={i} className={/^\*\[.*\]\*$/.test(p) ? "stage-dir" : ""}>
                <Md text={p} />
              </p>
            ))}
            {pos.s === SLIDES.length - 1 && (
              <>
                <h3>Easy questions you may get</h3>
                {NOTES.qa.map((q, i) => (
                  <p key={i}>
                    <b>{i + 1}. {q.q}</b> {q.a}
                  </p>
                ))}
              </>
            )}
          </div>
        </aside>
      )}
    </div>
  );
};
