"use client";

import { useEffect, useState } from "react";
import { Jost } from "next/font/google";

const jost = Jost({ subsets: ["latin"], display: "swap" });

const ORANGE = "#FF5A1F";
const DRAW_MS = 3400;
const OPEN_MS = 1100;

// Points the path passes through, in a 600 x 400 drawing space.
const POINTS: [number, number][] = [
  [40, 330],
  [170, 230],
  [320, 270],
  [430, 140],
  [560, 70],
];
const PATH = "M" + POINTS.map(([x, y]) => `${x} ${y}`).join(" L");

// When the pencil reaches each point (seconds). Draw starts at 0.3s and takes 2.4s.
const REACHED = [0.3, 0.92, 1.5, 2.14, 2.7];

const THEMES = {
  light: { bg: "#E5EAF0", plane: "#F8F6F0", ink: "#102B4E", accent: "#1F58B5", grid: "rgba(31,88,181,.22)" },
  dark: { bg: "#081A38", plane: "#102850", ink: "#F2F7FF", accent: "#7FB3ED", grid: "rgba(127,179,237,.2)" },
};

export default function Intro({ onDone }: { onDone: () => void }) {
  const [phase, setPhase] = useState<"draw" | "open">("draw");
  const [mode, setMode] = useState<"light" | "dark">("light");

  useEffect(() => {
    try {
      const t = window.localStorage.getItem("cb-theme");
      if (t === "light" || t === "dark") setMode(t);
    } catch {
      /* storage unavailable */
    }
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      onDone();
      return;
    }
    const a = window.setTimeout(() => setPhase("open"), DRAW_MS);
    const b = window.setTimeout(onDone, DRAW_MS + OPEN_MS);
    return () => {
      window.clearTimeout(a);
      window.clearTimeout(b);
    };
  }, [onDone]);

  const c = THEMES[mode];
  const open = phase === "open";

  const sheet = (side: "top" | "bottom"): React.CSSProperties => ({
    position: "absolute",
    left: 0,
    right: 0,
    [side]: 0,
    height: "50%",
    backgroundColor: c.bg,
    backgroundImage: `linear-gradient(${c.grid} 1px,transparent 1px),linear-gradient(90deg,${c.grid} 1px,transparent 1px)`,
    backgroundSize: "30px 30px",
    backgroundPosition: side === "top" ? "0 0" : "0 100%",
    transform: open ? `translateY(${side === "top" ? "-101%" : "101%"})` : "translateY(0)",
    transition: "transform 800ms cubic-bezier(.65,0,.35,1) 250ms",
  });

  return (
    <div
      aria-hidden
      className={`${jost.className} fixed inset-0 z-[100] overflow-hidden`}
      style={{ pointerEvents: open ? "none" : "auto", color: c.ink }}
    >
      <style>{`
        @keyframes ci-draw{to{stroke-dashoffset:0}}
        @keyframes ci-fade{to{opacity:1}}
        @keyframes ci-pin{from{transform:rotateX(-58deg) scaleY(0)}to{transform:rotateX(-58deg) scaleY(1)}}
        @keyframes ci-rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
        .ci-path{stroke-dasharray:1;stroke-dashoffset:1;animation:ci-draw 2.4s .3s linear forwards}
        .ci-node{opacity:0;animation:ci-fade .3s ease forwards}
        .ci-pin{transform:rotateX(-58deg) scaleY(0);transform-origin:bottom;animation:ci-pin .45s cubic-bezier(.2,1.4,.4,1) forwards}
        .ci-title{opacity:0;animation:ci-rise .7s .15s ease forwards}
        .ci-sub{opacity:0;animation:ci-rise .7s .45s ease forwards}
      `}</style>

      {/* The two sheets of drafting paper that split open at the end */}
      <div style={sheet("top")} />
      <div style={sheet("bottom")} />

      {/* The scene */}
      <div
        className="absolute inset-0 flex flex-col items-center justify-center"
        style={{
          opacity: open ? 0 : 1,
          transform: open ? "scale(1.25)" : "scale(1)",
          transition: "opacity 450ms ease, transform 700ms ease",
        }}
      >
        <div className="mb-6 text-center">
          <p className="ci-sub text-xs font-medium uppercase tracking-[0.2em]" style={{ color: c.accent }}>
            Plotting your path
          </p>
          <h1 className="ci-title mt-1 text-3xl font-bold tracking-tight sm:text-4xl">Career Blueprint</h1>
        </div>

        <div style={{ perspective: "1100px" }} className="w-[88vw] max-w-[760px]">
          <div
            className="relative w-full"
            style={{ aspectRatio: "3 / 2", transformStyle: "preserve-3d", transform: "rotateX(58deg)" }}
          >
            {/* The paper, with a grid that fades out toward the edges */}
            <div
              className="absolute inset-0 rounded-sm"
              style={{
                backgroundColor: c.plane,
                backgroundImage: `linear-gradient(${c.grid} 1px,transparent 1px),linear-gradient(90deg,${c.grid} 1px,transparent 1px)`,
                backgroundSize: "30px 30px",
                border: `1px solid ${c.grid}`,
                boxShadow: `0 30px 60px rgba(0,0,0,.18)`,
                WebkitMaskImage: "radial-gradient(ellipse at center, black 60%, transparent 100%)",
                maskImage: "radial-gradient(ellipse at center, black 60%, transparent 100%)",
              }}
            />

            {/* The path, drawn by the pencil */}
            <svg viewBox="0 0 600 400" className="absolute inset-0 h-full w-full" fill="none">
              <path d={PATH} stroke={c.accent} strokeOpacity=".25" strokeWidth="10" strokeLinecap="round" strokeLinejoin="round" pathLength={1} className="ci-path" />
              <path d={PATH} stroke={c.ink} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" pathLength={1} className="ci-path" />
              {POINTS.map(([x, y], i) => (
                <circle key={i} cx={x} cy={y} r="8" fill={c.plane} stroke={c.ink} strokeWidth="2.5" className="ci-node" style={{ animationDelay: `${REACHED[i]}s` }} />
              ))}
              <circle r="6" fill={ORANGE} opacity="0">
                <set attributeName="opacity" to="1" begin="0.3s" />
                <animateMotion dur="2.4s" begin="0.3s" fill="freeze" path={PATH} />
              </circle>
            </svg>

            {/* Pins that stand up off the paper at each milestone */}
            {POINTS.map(([x, y], i) => (
              <div
                key={i}
                className="absolute"
                style={{ left: `${(x / 600) * 100}%`, top: `${(y / 400) * 100}%`, width: 0, height: 0, transformStyle: "preserve-3d" }}
              >
                <div
                  className="ci-pin absolute"
                  style={{ left: -1, top: -64, width: 2, height: 64, background: c.ink, animationDelay: `${REACHED[i] + 0.1}s` }}
                >
                  <span
                    className="absolute rounded-full"
                    style={{ left: -6, top: -8, width: 14, height: 14, background: ORANGE, border: `2px solid ${c.plane}` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}