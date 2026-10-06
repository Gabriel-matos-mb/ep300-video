import React from 'react';
import {Img, staticFile, useCurrentFrame, useVideoConfig, delayRender, continueRender, AbsoluteFill, getInputProps} from 'remotion';
import {AnimKind, ExitKind, enter, leave, prog, easeOut, easeMid, popStrong, counterText} from './anim';
import {COL, SORA, INTER, EMOJI} from './tokens';

// ---------------------------------------------------------------- fontes locais (assets/fonts)
export const Fonts: React.FC = () => {
  const [h] = React.useState(() => delayRender('fonts'));
  React.useEffect(() => {
    const load = async () => {
      const faces = [
        new FontFace('EP300 Sora', `url(${staticFile('fonts/Sora.ttf')})`, {weight: '100 800'}),
        new FontFace('EP300 Inter', `url(${staticFile('fonts/Inter.ttf')})`, {weight: '100 900'}),
      ];
      await Promise.all(faces.map((f) => f.load()));
      faces.forEach((f) => (document.fonts as unknown as {add: (f: FontFace) => void}).add(f));
      continueRender(h);
    };
    load().catch(() => continueRender(h));
  }, [h]);
  return null;
};

export const useQa = () => Boolean((getInputProps() as {qaTransparent?: boolean}).qaTransparent);

export const useT = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return f / fps;
};

// ---------------------------------------------------------------- fundo: SOLIDO e opaco do primeiro ao ultimo quadro
export const Bg: React.FC<{variant: 'ink' | 'cream'}> = ({variant}) => {
  if ((getInputProps() as {qaTransparent?: boolean}).qaTransparent) return null; // so para STICKER_BOUNDS_CHECK
  const ink = variant === 'ink';
  return (
    <AbsoluteFill
      style={{
        backgroundColor: ink ? COL.ink : COL.cream,
        backgroundImage: `radial-gradient(circle at 10px 10px, ${ink ? COL.dotOnInk : COL.dotOnCream} 1.5px, transparent 2px)`,
        backgroundSize: '20px 20px',
      }}
    />
  );
};

// rotacoes do conjunto fixo do handoff (-8, 5, -4, 7, -6, 3) + -3 (texto-adesivo)
const ROTS = [-8, -6, -4, -3, 3, 5, 7];
export const snapRot = (r: number) => (Math.abs(r) < 1 ? 0 : ROTS.reduce((b, c) => (Math.abs(c - r) < Math.abs(b - r) ? c : b), ROTS[0]));

// ---------------------------------------------------------------- Fx: posiciona e anima um elemento (centro em x,y)
type FxProps = {
  at: number;
  out?: number;
  anim?: AnimKind;
  exit?: ExitKind;
  x: number;
  y: number;
  rot?: number;
  sway?: number;
  scale?: number;
  children: React.ReactNode;
};

export const Fx: React.FC<FxProps> = ({at, out, anim = 'pop', exit = 'none', x, y, rot = 0, sway = 0, scale = 1, children}) => {
  const t = useT();
  if (t < at) return null;
  const e = enter(anim, t - at);
  const l = leave(exit, t - (out ?? 1e9));
  const a = e.a * l.a;
  if (a <= 0.003) return null;
  const swayDeg = sway ? sway * Math.sin((2 * Math.PI * (t - at)) / 2.6) : 0;
  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        transform: `translate(-50%, -50%) translateY(${e.dy + l.dy}px) rotate(${snapRot(rot) + e.dr + swayDeg}deg) scale(${e.s * l.s * scale})`,
        opacity: a,
        transformOrigin: 'center center',
        whiteSpace: 'nowrap',
      }}
    >
      {children}
    </div>
  );
};

// ---------------------------------------------------------------- componentes visuais
export const Overline: React.FC<{at: number; text: string; x: number; y: number; color?: string; size?: number; out?: number}> = ({
  at, text, x, y, color = COL.orange, size = 30, out,
}) => (
  <Fx at={at} out={out} anim="rise" x={x} y={y}>
    <div style={{fontFamily: INTER, fontWeight: 500, fontSize: size, letterSpacing: '0.2em', color, lineHeight: 1}}>{text}</div>
  </Fx>
);

type PillVariant = 'w' | 'o';
export const PillBody: React.FC<{text: string; size?: number; variant?: PillVariant; emoji?: string}> = ({text, size = 34, variant = 'w', emoji}) => {
  const bg = variant === 'o' ? COL.orange : COL.white;
  const fg = variant === 'o' ? COL.white : COL.ink2;
  return (
    <div
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: size / 3,
        padding: `${size * 0.45}px ${size * 0.7}px`,
        borderRadius: 9999,
        background: bg,
        border: `3px solid ${COL.ink2}`,
        boxShadow: `${size * 0.15}px ${size * 0.2}px 0 rgba(2,2,2,0.9)`,
        fontFamily: SORA,
        fontWeight: 700,
        fontSize: size,
        color: fg,
        lineHeight: 1,
      }}
    >
      {emoji ? <span style={{fontFamily: EMOJI, fontSize: size * 1.05}}>{emoji}</span> : null}
      <span>{text}</span>
    </div>
  );
};

export const Pill: React.FC<{at: number; x: number; y: number; rot?: number; text: string; size?: number; variant?: PillVariant; emoji?: string; anim?: AnimKind; out?: number; exit?: ExitKind}> = ({
  at, x, y, rot = 0, text, size = 34, variant = 'w', emoji, anim = 'pop', out, exit,
}) => (
  <Fx at={at} x={x} y={y} rot={rot} anim={anim} out={out} exit={exit}>
    <PillBody text={text} size={size} variant={variant} emoji={emoji} />
  </Fx>
);

export const Label: React.FC<{at: number; x: number; y: number; rot?: number; lines: string[]; size?: number; anim?: AnimKind}> = ({at, x, y, rot = 0, lines, size = 34, anim = 'pop'}) => (
  <Fx at={at} x={x} y={y} rot={rot} anim={anim}>
    <div
      style={{
        padding: `${size * 0.45}px ${size * 0.6}px`,
        borderRadius: 22,
        background: COL.white,
        border: `4px solid ${COL.ink2}`,
        boxShadow: '6px 8px 0 rgba(0,0,0,0.85)',
        fontFamily: SORA,
        fontWeight: 700,
        fontSize: size,
        lineHeight: 1.22,
        color: COL.ink2,
        textAlign: 'left',
      }}
    >
      {lines.map((l, i) => (
        <div key={i}>{l}</div>
      ))}
    </div>
  </Fx>
);

export const Stamp: React.FC<{at: number; x: number; y: number; rot?: number; lines: string[]; size?: number; fill?: string}> = ({at, x, y, rot = 0, lines, size = 60, fill}) => {
  const col = COL.orange;
  const txt = fill ? COL.white : col;
  const bw = Math.max(5, size * 0.09);
  return (
    <Fx at={at} x={x} y={y} rot={rot} anim="stamp">
      <div style={{filter: 'drop-shadow(6px 8px 0 rgba(0,0,0,0.35))'}}>
        <div
          style={{
            position: 'relative',
            padding: `${size * 0.35}px ${size * 0.5}px`,
            borderRadius: size * 0.25,
            background: fill ?? 'transparent',
            textAlign: 'center',
          }}
        >
          <div style={{position: 'absolute', inset: 6, borderRadius: size * 0.2, border: `${bw}px solid ${txt}`}} />
          {lines.map((l, i) => (
            <div key={i} style={{position: 'relative', fontFamily: SORA, fontWeight: 800, fontSize: size, letterSpacing: '-0.01em', lineHeight: 1.12, color: txt}}>
              {l}
            </div>
          ))}
        </div>
      </div>
    </Fx>
  );
};

export const Sticker: React.FC<{at: number; x: number; y: number; src: string; size?: number; rot?: number; anim?: AnimKind; sway?: number; breath?: boolean}> = ({
  at, x, y, src, size = 240, rot = 0, anim = 'pop', sway = 0,
}) => (
  <Fx at={at} x={x} y={y} rot={rot} anim={anim} sway={sway}>
    <Img src={staticFile(src)} style={{height: size, width: 'auto', filter: 'drop-shadow(0 8px 12px rgba(0,0,0,0.35))'}} />
  </Fx>
);

export const Emoji: React.FC<{at: number; x: number; y: number; ch: string; size?: number; anim?: AnimKind; out?: number}> = ({at, x, y, ch, size = 100, anim = 'burst', out}) => (
  <Fx at={at} x={x} y={y} anim={anim} out={out} exit={out === undefined ? 'none' : 'cut'}>
    <div style={{fontFamily: EMOJI, fontSize: size, lineHeight: 1, padding: 8, filter: 'drop-shadow(5px 0 0 #fff) drop-shadow(-5px 0 0 #fff) drop-shadow(0 5px 0 #fff) drop-shadow(0 -5px 0 #fff) drop-shadow(4px 4px 0 #fff) drop-shadow(-4px -4px 0 #fff) drop-shadow(4px -4px 0 #fff) drop-shadow(-4px 4px 0 #fff) drop-shadow(0 8px 10px rgba(0,0,0,0.4))'}}>{ch}</div>
  </Fx>
);

// texto em estilo sticker: contorno branco die-cut + sombra
export const StickerText: React.FC<{at: number; x: number; y: number; rot?: number; text: string; size?: number; color?: string; anim?: AnimKind}> = ({at, x, y, rot = 0, text, size = 110, color = COL.orange, anim = 'slap'}) => (
  <Fx at={at} x={x} y={y} rot={rot} anim={anim}>
    <div style={{fontFamily: SORA, fontWeight: 800, fontSize: size, letterSpacing: '-0.02em', color, lineHeight: 1, padding: 10, WebkitTextStroke: '16px #fff', paintOrder: 'stroke fill', strokeLinejoin: 'round', filter: 'drop-shadow(0 8px 10px rgba(0,0,0,0.4))'} as React.CSSProperties}>{text}</div>
  </Fx>
);

export const Slap: React.FC<{at: number; x: number; y: number; rot?: number; text: string; size?: number; color?: string; anim?: AnimKind}> = ({at, x, y, rot = 0, text, size = 110, color = COL.orange, anim = 'slap'}) => (
  <Fx at={at} x={x} y={y} rot={rot} anim={anim}>
    <div style={{fontFamily: SORA, fontWeight: 800, fontSize: size, letterSpacing: '-0.02em', color, lineHeight: 1, textShadow: `${size * 0.03}px ${size * 0.04}px 0 rgba(0,0,0,0.15)`}}>{text}</div>
  </Fx>
);

export const Counter: React.FC<{at: number; to: number; x: number; y: number; size: number; color?: string; fmt?: string; cdur?: number; from?: number}> = ({
  at, to, x, y, size, color = COL.white, fmt = '{}', cdur = 1.1, from = 0,
}) => {
  const t = useT();
  if (t < at) return null;
  const p = prog(t, at, cdur);
  const n = from + (to - from) * easeMid(p);
  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        transform: 'translate(-50%, -50%)',
        fontFamily: SORA,
        fontWeight: 800,
        fontSize: size,
        letterSpacing: '-0.04em',
        lineHeight: 1,
        color,
        whiteSpace: 'nowrap',
        textShadow: `${size * 0.03}px ${size * 0.04}px 0 rgba(0,0,0,0.15)`,
      }}
    >
      {fmt.replace('{}', counterText(n))}
    </div>
  );
};

export type AxisNode = {x: number; label: string; at: number};
export const TLAxis: React.FC<{x0: number; x1: number; y: number; nodes: AxisNode[]; at?: number; draw?: number; width?: number; labSize?: number; color?: string}> = ({
  x0, x1, y, nodes, at = 0, draw = 1.0, width = 8, labSize = 30, color = COL.ink2,
}) => {
  const t = useT();
  if (t < at) return null;
  const p = easeOut(prog(t, at, draw));
  return (
    <>
      <div style={{position: 'absolute', left: x0, top: y - width / 2, width: (x1 - x0) * p, height: width, background: color, borderRadius: width}} />
      {nodes.map((n, i) => {
        const ln = t - n.at;
        if (ln < 0) return null;
        const s = popStrong(prog(ln, 0, 0.35));
        const r = 18 * s;
        return (
          <React.Fragment key={i}>
            <div style={{position: 'absolute', left: n.x - r, top: y - r, width: r * 2, height: r * 2, borderRadius: '50%', background: COL.orange, border: `5px solid ${COL.ink2}`, boxSizing: 'border-box'}} />
            {n.label ? (
              <div style={{position: 'absolute', left: n.x, top: y + 52, transform: 'translate(-50%, -50%)', fontFamily: INTER, fontWeight: 500, fontSize: labSize, letterSpacing: '0.1em', color: COL.ink2, opacity: Math.min(1, ln * 4), whiteSpace: 'nowrap', lineHeight: 1}}>
                {n.label}
              </div>
            ) : null}
          </React.Fragment>
        );
      })}
    </>
  );
};

// grade de circulos: n total, fill preenchidos em laranja (como "4 em cada 10")
export const DotGrid: React.FC<{at: number; n: number; fill: number; x: number; y: number; r?: number; gap?: number; cols?: number; fillAt?: number}> = ({
  at, n, fill, x, y, r = 34, gap = 22, cols, fillAt = 0.3,
}) => {
  const t = useT();
  const c = cols ?? n;
  const lt = t - at;
  if (lt < 0) return null;
  return (
    <>
      {Array.from({length: n}).map((_, i) => {
        const li = lt - i * 0.06;
        if (li < 0) return null;
        const e = enter('pop', li);
        const on = i < fill && lt > fillAt + i * 0.12;
        const px = x + ((i % c) - (c - 1) / 2) * (2 * r + gap);
        const py = y + Math.floor(i / c) * (2 * r + gap);
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: px - r,
              top: py - r,
              width: 2 * r,
              height: 2 * r,
              borderRadius: '50%',
              boxSizing: 'border-box',
              background: on ? COL.orange : COL.white,
              border: `4px solid ${COL.ink2}`,
              boxShadow: '0 6px 0 rgba(0,0,0,0.35)',
              transform: `scale(${e.s})`,
              opacity: e.a,
            }}
          />
        );
      })}
    </>
  );
};

export const Polaroid: React.FC<{at: number; x: number; y: number; rot?: number; src: string; w?: number; ratio?: number; caption?: string; cap?: number; anim?: AnimKind}> = ({
  at, x, y, rot = 0, src, w = 400, ratio = 9 / 16, caption, cap = 26, anim = 'slap',
}) => {
  const pad = w * 0.045;
  const bot = caption ? w * 0.16 : pad;
  return (
    <Fx at={at} x={x} y={y} rot={rot} anim={anim}>
      <div style={{width: w + 2 * pad, background: COL.white, padding: `${pad}px ${pad}px 0`, boxSizing: 'border-box', boxShadow: '0 14px 22px rgba(0,0,0,0.42)'}}>
        <Img src={staticFile(src)} style={{display: 'block', width: w, height: w * ratio, objectFit: 'cover'}} />
        <div style={{height: bot, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: SORA, fontWeight: 700, fontSize: cap, color: COL.ink2}}>{caption}</div>
      </div>
    </Fx>
  );
};

// ---------------------------------------------------------------- ficha de presenca (card branco com linhas)
export type FichaRow = {name: string; n: number; at: number; extra?: {at: number; text: string; emoji: string}; done?: boolean};
export const Ficha: React.FC<{at: number; rows: FichaRow[]; x?: number; y?: number; rot?: number}> = ({at, rows, x = 448, y = 520, rot = -3}) => {
  const t = useT();
  return (
    <Fx at={at} x={x} y={y} rot={rot} anim="up" scale={0.94}>
      <div style={{position: 'relative', width: 700, height: 520, background: COL.white, border: `4px solid ${COL.ink2}`, borderRadius: 18, boxShadow: '8px 10px 0 rgba(0,0,0,0.85)', boxSizing: 'border-box'}}>
        <div style={{position: 'absolute', left: 40, top: 36, fontFamily: SORA, fontWeight: 800, fontSize: 34, letterSpacing: '0.04em', color: COL.ink2, lineHeight: 1}}>FICHA DE PRESENÇA</div>
        {[150, 268, 386].map((yy) => (
          <div key={yy} style={{position: 'absolute', left: 30, right: 30, top: yy, height: 3, background: '#D2D2D2'}} />
        ))}
        <div style={{position: 'absolute', left: 110, top: 110, bottom: 20, width: 3, background: 'rgba(244,115,64,0.5)'}} />
        {rows.map((r, i) => {
          const lt = r.done ? 99 : t - r.at;
          if (lt < 0) return null;
          const p = prog(lt, 0, 0.8);
          const n = Math.floor(1 + (r.n - 1) * easeMid(p));
          const top = 90 + i * 118;
          const small = r.name.length >= 12;
          return (
            <React.Fragment key={i}>
              <svg style={{position: 'absolute', left: 40, top: top + 14}} width="60" height="44" viewBox="0 0 60 44">
                <polyline points="2,18 16,34 40,2" fill="none" stroke={COL.orange} strokeWidth="9" strokeLinejoin="round" strokeLinecap="round" />
              </svg>
              <div style={{position: 'absolute', left: 130, top: top + 4, fontFamily: SORA, fontWeight: 700, fontSize: small ? 28 : 34, color: COL.ink2, lineHeight: 1}}>{r.name}</div>
              <div style={{position: 'absolute', right: 40, top: top - 8, fontFamily: SORA, fontWeight: 800, fontSize: 52, letterSpacing: '-0.03em', color: COL.orange, lineHeight: 1}}>{n}×</div>
              {r.extra && (r.done || t >= r.extra.at) ? (
                <div style={{position: 'absolute', left: 130, top: top + 50}}>
                  <PillBody text={r.extra.text} size={22} variant="o" emoji={r.extra.emoji} />
                </div>
              ) : null}
            </React.Fragment>
          );
        })}
      </div>
    </Fx>
  );
};
