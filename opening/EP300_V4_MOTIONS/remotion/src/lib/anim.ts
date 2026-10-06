// Curvas e entradas portadas do motor V2 (v2/gfx.py + v2/engine.py) para manter a mesma sensacao de movimento.
export const clamp = (x: number, a = 0, b = 1) => Math.max(a, Math.min(b, x));

const bezier = (p1x: number, p1y: number, p2x: number, p2y: number) => (x0: number) => {
  const x = clamp(x0);
  let lo = 0;
  let hi = 1;
  for (let i = 0; i < 30; i++) {
    const t = (lo + hi) / 2;
    const bx = 3 * (1 - t) ** 2 * t * p1x + 3 * (1 - t) * t ** 2 * p2x + t ** 3;
    if (bx < x) lo = t;
    else hi = t;
  }
  const t = (lo + hi) / 2;
  return 3 * (1 - t) ** 2 * t * p1y + 3 * (1 - t) * t ** 2 * p2y + t ** 3;
};

export const easeOut = bezier(0.25, 1, 0.5, 1);
export const easeMid = bezier(0.33, 1, 0.68, 1);
export const easeIn = bezier(0.32, 0, 0.67, 0);
export const easeIO = bezier(0.76, 0, 0.24, 1);
export const popSoft = bezier(0.34, 1.56, 0.64, 1);
export const popStrong = (x0: number) => {
  const x = clamp(x0);
  if (x < 0.5) return 1.19 * easeOut(x / 0.5);
  return 1.19 - 0.19 * easeIO((x - 0.5) / 0.5);
};
export const prog = (t: number, t0: number, dur: number) => (dur > 0 ? clamp((t - t0) / dur) : t >= t0 ? 1 : 0);

export type AnimKind = 'pop' | 'slap' | 'rise' | 'up' | 'stamp' | 'burst' | 'drop' | 'none';
export type Enter = {s: number; dy: number; a: number; dr: number};

export const enter = (anim: AnimKind, lt: number): Enter => {
  if (lt < 0) return {s: 0, dy: 0, a: 0, dr: 0};
  switch (anim) {
    case 'pop': {
      const p = prog(lt, 0, 0.5);
      return {s: 0.5 + 0.5 * popSoft(p), dy: 0, a: Math.min(1, p * 3), dr: 0};
    }
    case 'slap': {
      const p = prog(lt, 0, 0.4);
      return {s: p > 0 ? 1.25 - 0.25 * popStrong(p) : 1.25, dy: 0, a: Math.min(1, p * 5), dr: -9 * (1 - easeOut(p))};
    }
    case 'rise': {
      const p = prog(lt, 0, 0.7);
      return {s: 1, dy: 24 * (1 - easeOut(p)), a: easeOut(p), dr: 0};
    }
    case 'up': {
      const p = prog(lt, 0, 0.5);
      return {s: 1, dy: 16 * (1 - easeOut(p)), a: Math.min(1, p * 2), dr: 0};
    }
    case 'stamp': {
      const p = prog(lt, 0, 0.28);
      return {s: p < 1 ? 1.6 - 0.6 * easeIn(p) : 1, dy: 0, a: Math.min(1, p * 4), dr: 0};
    }
    case 'burst': {
      const p = prog(lt, 0, 0.45);
      return {s: popStrong(p), dy: 0, a: Math.min(1, p * 4), dr: -52 * (1 - easeOut(p))};
    }
    case 'drop': {
      const p = prog(lt, 0, 0.55);
      return {s: 1, dy: -700 * (1 - popSoft(p)), a: 1, dr: 0};
    }
    default:
      return {s: 1, dy: 0, a: 1, dr: 0};
  }
};

export type ExitKind = 'none' | 'up' | 'shrink' | 'cut';
export const leave = (kind: ExitKind, lt: number): Enter => {
  if (lt < 0 || kind === 'none') return {s: 1, dy: 0, a: 1, dr: 0};
  if (kind === 'up') {
    const p = prog(lt, 0, 0.3);
    return {s: 1, dy: -40 * easeIn(p), a: 1 - easeIn(p), dr: 0};
  }
  if (kind === 'shrink') {
    const p = prog(lt, 0, 0.3);
    return {s: 1 - easeIn(p), dy: 0, a: 1, dr: 0};
  }
  return {s: 1, dy: 0, a: 0, dr: 0};
};

// "153" -> "153"; 700000 -> "700.000" (separador de milhar brasileiro, como no motor V2)
export const counterText = (n: number) => String(Math.floor(n)).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
