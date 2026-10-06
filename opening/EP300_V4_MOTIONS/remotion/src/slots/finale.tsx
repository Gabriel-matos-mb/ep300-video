import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {z} from 'zod';
import {Bg, Fonts, Fx, Overline, PillBody, useT} from '../lib/primitives';
import {COL, SORA} from '../lib/tokens';
import {easeIO, easeMid, easeOut, prog, counterText} from '../lib/anim';
import {Group, Logo, Sep} from './presession';

const OUTLINE =
  'drop-shadow(6px 0 0 #fff) drop-shadow(-6px 0 0 #fff) drop-shadow(0 6px 0 #fff) drop-shadow(0 -6px 0 #fff) drop-shadow(5px 5px 0 #fff) drop-shadow(-5px -5px 0 #fff) drop-shadow(5px -5px 0 #fff) drop-shadow(-5px 5px 0 #fff)';

// quadro transparente (overlay sobre camera ativa): sem Bg
const FrameT: React.FC<{children: React.ReactNode}> = ({children}) => (
  <AbsoluteFill>
    <Fonts />
    {children}
  </AbsoluteFill>
);

// tela cheia (fundo tinta) — O02 vira card, sem camera
const FrameO: React.FC<{children: React.ReactNode}> = ({children}) => (
  <AbsoluteFill>
    <Bg variant="ink" />
    <Fonts />
    {children}
  </AbsoluteFill>
);

const lbl: React.CSSProperties = {fontFamily: SORA, fontWeight: 800, color: '#fff', letterSpacing: '0.08em', filter: 'drop-shadow(3px 4px 0 rgba(0,0,0,0.85))', lineHeight: 1, whiteSpace: 'nowrap'};

// ===================================================================== F01 — final: 300 (substitui "vocês estão aqui e contando")
export const f01Schema = z.object({line1: z.string(), line2: z.string(), kinoplexSrc: z.string()});
export const F01: React.FC<z.infer<typeof f01Schema>> = ({line1, line2, kinoplexSrc}) => {
  const t = useT();
  const p = easeMid(prog(t, 0.2, 1.1));
  const n = Math.floor(300 * p);
  const settle = prog(t, 1.3, 0.25);
  const sc = 1 + (t > 1.3 ? 0.08 * (1 - settle) : 0);
  return (
    <AbsoluteFill>
      <Fonts />
      <Bg variant="ink" />
      <Overline at={0.1} text="EPISÓDIO" x={960} y={170} color={COL.orange} size={44} />
      <div style={{position: 'absolute', left: 960, top: 400, transform: `translate(-50%, -50%) scale(${sc})`, filter: `${OUTLINE} drop-shadow(14px 18px 0 rgba(0,0,0,0.7))`}}>
        <div style={{fontFamily: SORA, fontWeight: 800, fontSize: 430, lineHeight: 1, letterSpacing: '-0.04em', color: COL.orange, padding: 16}}>{counterText(n)}</div>
      </div>
      <Fx at={1.8} x={960} y={655} rot={-2} anim="pop"><PillBody text={line1} size={44} /></Fx>
      <Fx at={2.4} x={960} y={745} rot={1.5} anim="slap"><PillBody text={line2} size={44} variant="o" /></Fx>
      <div style={{position: 'absolute', left: 0, right: 0, top: 880, display: 'flex', justifyContent: 'center', alignItems: 'flex-end', gap: 56}}>
        <Group at={3.0} label="REALIZAÇÃO"><Logo src="brand/logo-metricas-boss-branca.png" h={74} /></Group>
        <Sep at={3.15} />
        <Group at={3.15} label="PATROCÍNIO"><Logo src="sponsors/purple-metrics.webp" h={92} /><Logo src="sponsors/onfly.webp" h={66} /></Group>
        <Sep at={3.3} />
        <Group at={3.3} label="CAFÉ OFICIAL"><Logo src="sponsors/coffee-plusplus.webp" h={92} /></Group>
        <Sep at={3.45} />
        <Group at={3.45} label="APOIADOR"><Logo src={kinoplexSrc} h={80} /></Group>
      </div>
    </AbsoluteFill>
  );
};
export const f01Default = {line1: '300 episódios, 300 perguntas…', line2: 'e a de hoje começa agora.', kinoplexSrc: 'brand/logo_kinoplex_original.png'};

const Layers = z.object({delorean: z.boolean(), dupla: z.boolean(), axis: z.boolean(), markers: z.boolean(), hero: z.boolean(), sofa: z.boolean().optional()});

// ===================================================================== O01 — BEAT A "voltando no tempo" (SETUP, overlay sobre camera)
// camadas separaveis: DELOREAN · DUPLA (Marty+Doc) · TIME_AXIS · TIME_MARKERS (rotulos)
export const o01Schema = z.object({layers: Layers, car: z.string(), dupla: z.string(), left: z.string(), right: z.string()});
export const O01: React.FC<z.infer<typeof o01Schema>> = ({layers, car, dupla, left, right}) => {
  const t = useT();
  const Y = 925;
  const axisP = easeOut(prog(t, 0.05, 0.9)); // eixo cresce da direita (PRESENTE) para a esquerda (PASSADO)
  const axisOut = prog(t, 2.6, 0.4);
  const carX = 2150 - (2150 - 330) * easeIO(prog(t, 0.2, 1.6)); // atravessa da direita para a esquerda e sai
  const dIn = prog(t, 1.0, 0.35);
  const dOut = prog(t, 2.7, 0.25);
  const dS = dIn < 1 ? 0.6 + 0.4 * easeOut(dIn) * 1.1 : 1 - dOut * 0.4;
  return (
    <FrameT>
      {layers.axis ? (
        <div style={{opacity: 1 - axisOut}}>
          <div style={{position: 'absolute', left: 1700 - 1400 * axisP, top: Y - 6, width: 1400 * axisP, height: 12, background: COL.orange, border: '3px solid #020202', borderRadius: 12, boxShadow: '0 4px 0 rgba(0,0,0,0.85)', boxSizing: 'border-box'}} />
        </div>
      ) : null}
      {layers.markers ? (
        <div style={{opacity: (1 - axisOut) * Math.min(1, t * 4)}}>
          <div style={{position: 'absolute', left: 1700, top: Y + 40, transform: 'translateX(-50%)', fontSize: 34, ...lbl}}>{right}</div>
          <div style={{position: 'absolute', left: 300, top: Y + 40, transform: 'translateX(-50%)', fontSize: 34, ...lbl, opacity: prog(t, 1.0, 0.4)}}>{left}</div>
        </div>
      ) : null}
      {layers.delorean ? (
        <div style={{position: 'absolute', left: carX, top: Y - 108, transform: 'translate(-50%, -50%)', opacity: 1 - dOut}}>
          <Img src={staticFile(car)} style={{height: 150, width: 'auto', filter: 'drop-shadow(0 8px 10px rgba(0,0,0,0.45))'}} />
        </div>
      ) : null}
      {layers.dupla && t >= 1.0 && dOut < 1 ? (
        <div style={{position: 'absolute', left: 1600, top: 830, transform: `translate(-50%, -50%) rotate(-3deg) scale(${dS})`, opacity: Math.min(1, dIn * 3) * (1 - dOut)}}>
          <Img src={staticFile(dupla)} style={{height: 210, width: 'auto', filter: 'drop-shadow(0 10px 14px rgba(0,0,0,0.4))'}} />
        </div>
      ) : null}
    </FrameT>
  );
};
export const o01Default = {layers: {delorean: true, dupla: true, axis: false, markers: false, hero: false}, car: 'stickers/delorean.png', dupla: 'stickers/dupla_marty_doc.png', left: 'PASSADO', right: 'PRESENTE'};

// ===================================================================== O02 — BEAT B "2038" (PAYOFF, overlay sobre camera)
// camadas separaveis: DELOREAN · DUPLA · TIME_AXIS · TIME_MARKERS · 2038_HERO · SOFA (cena do site, 6 quadros, espelhada como na V2)
// janela: 259.6-267.2 (7,6 s). "play agora" 1,3 · "aqui agora" 2,1 · "tu so vai parar de escutar" 4,1 · "2038" 6,4
export const o02Schema = z.object({layers: Layers, from: z.string(), to: z.string(), car: z.string(), dupla: z.string(), tAgora: z.number(), tArrive: z.number(), tSofa: z.number(), tEnd: z.number()});
const SOFA_TS = [0, 0.78, 1.41, 2.12, 2.92, 3.64];
export const O02: React.FC<z.infer<typeof o02Schema>> = ({layers, from, to, car, dupla, tAgora, tArrive, tSofa, tEnd}) => {
  const t = useT();
  const X0 = 250;
  const X1 = 1600;
  const Y = 985;
  const p = easeMid(prog(t, tAgora, tArrive - tAgora));
  const tip = X0 + (X1 - X0) * p;
  const carIn = prog(t, tAgora - 0.2, 0.35);
  const fade = 1 - prog(t, tEnd, 0.45);
  const sofaFr = Math.max(...SOFA_TS.map((v, i) => (t - tSofa >= v ? i : 0))) + 1;
  const dot = (x: number, key: string, big = false) => (
    <div key={key} style={{position: 'absolute', left: x - (big ? 17 : 13), top: Y - (big ? 17 : 13), width: big ? 34 : 26, height: big ? 34 : 26, borderRadius: '50%', background: COL.orange, border: '5px solid #020202', boxSizing: 'border-box'}} />
  );
  return (
    <FrameO>
      <div style={{opacity: fade}}>
        {layers.axis && tip - X0 > 6 ? <div style={{position: 'absolute', left: X0, top: Y - 6, width: Math.max(0, tip - X0), height: 12, background: COL.orange, border: '3px solid #020202', borderRadius: 12, boxShadow: '0 4px 0 rgba(0,0,0,0.85)', boxSizing: 'border-box'}} /> : null}
        {layers.markers ? (
          <>
            {t >= tAgora - 0.3 ? dot(X0, 'start', true) : null}
            {[0.25, 0.5, 0.75].map((f) => (tip >= X0 + (X1 - X0) * f ? dot(X0 + (X1 - X0) * f, `m${f}`) : null))}
            {t >= tArrive ? dot(X1, 'end', true) : null}
          </>
        ) : null}
        {layers.markers ? <Fx at={tAgora - 0.3} x={X0} y={Y - 52} anim="rise"><div style={{fontSize: 30, ...lbl}}>{from}</div></Fx> : null}
        {layers.delorean ? (
          <div style={{position: 'absolute', left: tip, top: Y - 108, transform: 'translate(-50%, -50%) scaleX(-1)', opacity: carIn}}>
            <Img src={staticFile(car)} style={{height: 150, width: 'auto', filter: 'drop-shadow(0 8px 10px rgba(0,0,0,0.45))'}} />
          </div>
        ) : null}
        {layers.hero ? (
          <Fx at={tArrive} x={1470} y={620} rot={-3} anim="slap">
            <div style={{fontFamily: SORA, fontWeight: 800, fontSize: 200, lineHeight: 1, letterSpacing: '-0.04em', color: COL.orange, padding: 14, filter: `${OUTLINE} drop-shadow(8px 10px 0 rgba(0,0,0,0.75))`}}>{to}</div>
          </Fx>
        ) : null}
        {layers.dupla ? (
          <Fx at={tArrive + 0.4} x={420} y={760} rot={3} anim="slap">
            <Img src={staticFile(dupla)} style={{height: 270, width: 'auto', filter: 'drop-shadow(0 10px 14px rgba(0,0,0,0.4))'}} />
          </Fx>
        ) : null}
        {layers.sofa ? (
          <Fx at={tSofa} x={925} y={290} rot={2} anim="pop">
            <Img src={staticFile(`cena-sofa/${sofaFr}.webp`)} style={{width: 760, height: 'auto', transform: 'scaleX(-1)', filter: 'drop-shadow(0 10px 14px rgba(0,0,0,0.35))'}} />
          </Fx>
        ) : null}
      </div>
    </FrameO>
  );
};
export const o02Default = {layers: {delorean: true, dupla: true, axis: true, markers: true, hero: true, sofa: true}, from: 'AGORA', to: '2038', car: 'stickers/delorean.png', dupla: 'stickers/dupla_marty_doc.png', tAgora: 3.8, tArrive: 6.4, tSofa: 0.2, tEnd: 7.0};

// ===================================================================== NOVOS COMPLEMENTOS (overlay alfa, sticker/pill/numero-heroi; terco superior livre)
const stk: React.CSSProperties = {fontFamily: SORA, fontWeight: 800, lineHeight: 1, letterSpacing: '-0.02em', padding: 10, filter: 'drop-shadow(5px 0 0 #fff) drop-shadow(-5px 0 0 #fff) drop-shadow(0 5px 0 #fff) drop-shadow(0 -5px 0 #fff) drop-shadow(4px 4px 0 #fff) drop-shadow(-4px -4px 0 #fff) drop-shadow(4px -4px 0 #fff) drop-shadow(-4px 4px 0 #fff) drop-shadow(0 8px 10px rgba(0,0,0,0.4))'};

// IA_METADE — 2,5 s ("metade" 1,0)
export const iaSchema = z.object({a: z.string(), b: z.string(), c: z.string()});
export const IAMetade: React.FC<z.infer<typeof iaSchema>> = ({a, b, c}) => (
  <FrameT>
    <Fx at={0} x={945} y={330} rot={-3} anim="slap" out={2.2} exit="up"><div style={{...stk, fontSize: 150, color: COL.orange}}>{a}</div></Fx>
    <Fx at={0.95} x={945} y={455} rot={5} anim="slap" out={2.2} exit="up"><PillBody text={b} size={64} variant="o" /></Fx>
    <Fx at={1.6} x={945} y={560} rot={-3} anim="pop" out={2.2} exit="up"><PillBody text={c} size={38} /></Fx>
  </FrameT>
);
export const iaDefault = {a: 'IA', b: 'METADE', c: 'dos nossos episódios'};

// BQ_MARKETING — 5,8 s ("engenheiro" 1,0 · "virou" 2,3 · "marketing" 4,9)
export const bqSchema = z.object({a: z.string(), b: z.string(), c: z.string()});
export const BQMarketing: React.FC<z.infer<typeof bqSchema>> = ({a, b, c}) => (
  <FrameT>
    <Fx at={0} x={975} y={320} rot={-3} anim="pop" out={5.4} exit="up"><PillBody text={a} size={52} /></Fx>
    <Fx at={0.8} x={975} y={495} rot={3} anim="pop" out={3.0} exit="shrink"><PillBody text={b} emoji="🛠️" size={30} /></Fx>
    <Fx at={2.2} x={975} y={405} anim="pop" out={5.4} exit="up"><div style={{...stk, fontSize: 70, color: COL.ink2}}>↓</div></Fx>
    <Fx at={3.0} x={975} y={495} rot={3} anim="slap" out={5.4} exit="up"><PillBody text={c} size={52} variant="o" /></Fx>
  </FrameT>
);
export const bqDefault = {a: 'BigQuery', b: 'assunto de engenheiro', c: 'MARKETING'};

// CEM_MIL_HORAS — 3,0 s ("100" 0,5 · "mil horas" 0,9-1,2 · "ouvidas" 1,8)
export const cemSchema = z.object({value: z.number(), caption: z.string()});
export const CemMilHoras: React.FC<z.infer<typeof cemSchema>> = ({value, caption}) => {
  const t = useT();
  const p = easeMid(prog(t, 0.3, 0.8));
  const n = Math.floor(value * p);
  const done = t >= 1.1;
  const settle = prog(t, 1.1, 0.3);
  const sc = done ? 1 + 0.07 * (1 - settle) : 1;
  const out = prog(t, 2.7, 0.3);
  if (t < 0.3 || out >= 1) return <FrameT><span /></FrameT>;
  return (
    <FrameT>
      <div style={{position: 'absolute', left: 960, top: 210 - out * 30, opacity: 1 - out, transform: `translate(-50%, -50%) scale(${sc}) rotate(-3deg)`}}>
        <div style={{...stk, fontSize: 170, color: COL.orange, whiteSpace: 'nowrap'}}>{`${n}${done ? '+' : ''} MIL HORAS`}</div>
      </div>
      <Fx at={1.8} x={960} y={345} rot={3} anim="pop" out={2.7} exit="up"><PillBody text={caption} size={38} /></Fx>
    </FrameT>
  );
};
export const cemDefault = {value: 100, caption: 'ouvidas de conteúdo'};
