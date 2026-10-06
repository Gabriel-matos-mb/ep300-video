import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {z} from 'zod';
import {Bg, Emoji, Fonts, Fx, Overline, PillBody, Sticker, useQa, useT} from '../lib/primitives';
import {COL, EMOJI, INTER, SORA} from '../lib/tokens';
import {easeIO, easeOut, prog} from '../lib/anim';

const OUTLINE =
  'drop-shadow(5px 0 0 #fff) drop-shadow(-5px 0 0 #fff) drop-shadow(0 5px 0 #fff) drop-shadow(0 -5px 0 #fff) drop-shadow(4px 4px 0 #fff) drop-shadow(-4px -4px 0 #fff) drop-shadow(4px -4px 0 #fff) drop-shadow(-4px 4px 0 #fff)';

const Frame: React.FC<{variant: 'ink' | 'cream'; children: React.ReactNode}> = ({variant, children}) => (
  <AbsoluteFill>
    <Fonts />
    <Bg variant={variant} />
    {children}
  </AbsoluteFill>
);

// ===================================================================== P01 — contagem 3..2..1 (pre-sessao)
export const p01Schema = z.object({title: z.string(), footer: z.string(), beat: z.number()});
export const P01: React.FC<z.infer<typeof p01Schema>> = ({title, footer, beat}) => {
  const t = useT();
  const idx = Math.min(2, Math.floor(t / beat));
  const n = 3 - idx;
  const f = Math.min(1, (t - idx * beat) / beat);
  const slap = prog(t - idx * beat, 0, 0.32);
  const sc = 1.28 - 0.28 * easeOut(slap);
  const rot = -7 * (1 - easeOut(slap));
  const pulse = 1 + 0.035 * (1 - easeOut(prog(t - idx * beat, 0, 0.4)));
  const R = 340;
  const C = 2 * Math.PI * R;
  const ticks = Array.from({length: 60});
  const qa = useQa();
  return (
    <Frame variant="cream">
      {qa ? null : <div style={{position: 'absolute', left: 0, right: 0, top: 539, height: 3, background: 'rgba(18,18,19,0.16)'}} />}
      {qa ? null : <div style={{position: 'absolute', top: 0, bottom: 0, left: 959, width: 3, background: 'rgba(18,18,19,0.16)'}} />}
      <svg width="1920" height="1080" style={{position: 'absolute', inset: 0, transform: `scale(${pulse})`, transformOrigin: '960px 540px'}}>
        {ticks.map((_, i) => {
          const a = (i / 60) * 2 * Math.PI - Math.PI / 2;
          const major = i % 5 === 0;
          const r0 = 412;
          const r1 = major ? 446 : 430;
          return <line key={i} x1={960 + r0 * Math.cos(a)} y1={540 + r0 * Math.sin(a)} x2={960 + r1 * Math.cos(a)} y2={540 + r1 * Math.sin(a)} stroke={COL.ink2} strokeOpacity={major ? 0.7 : 0.28} strokeWidth={major ? 5 : 3} strokeLinecap="round" />;
        })}
        <circle cx="960" cy="540" r="388" fill="none" stroke={COL.ink2} strokeWidth="6" />
        <circle cx="960" cy="540" r={R} fill="none" stroke="#EFE9DC" strokeWidth="78" />
        <circle cx="960" cy="540" r={R} fill="none" stroke={COL.orange} strokeWidth="78" strokeDasharray={`${C * f} ${C}`} transform="rotate(-90 960 540)" />
        <circle cx="960" cy="540" r="301" fill={COL.cream} stroke={COL.ink2} strokeWidth="6" />
      </svg>
      <div style={{position: 'absolute', left: 960, top: 548, transform: `translate(-50%, -50%) rotate(${rot}deg) scale(${sc})`, filter: `${OUTLINE} drop-shadow(12px 16px 0 rgba(2,2,2,0.9))`}}>
        <div style={{fontFamily: SORA, fontWeight: 800, fontSize: 440, lineHeight: 1, letterSpacing: '-0.04em', color: COL.orange, padding: 12}}>{n}</div>
      </div>
      <Overline at={0} text={title} x={960} y={90} size={30} />
      <div style={{position: 'absolute', left: 960, top: 1000, transform: 'translate(-50%, -50%)', fontFamily: INTER, fontWeight: 700, fontSize: 26, letterSpacing: '0.15em', color: '#787878', whiteSpace: 'nowrap'}}>{footer}</div>
    </Frame>
  );
};
export const p01Default = {title: 'PRÉ-SESSÃO', footer: 'ANALYTICS TALKS · EP 300', beat: 0.97};

// ===================================================================== P02 — aviso antes da sessao (5 paginas)
const PG = [0, 7.7, 12.9, 18.1, 23.7];
const AVISO_END = 31.0;
const Page: React.FC<{i: number; children: React.ReactNode}> = ({i, children}) => {
  const t = useT();
  const s = PG[i];
  const e = i < PG.length - 1 ? PG[i + 1] : AVISO_END + 1;
  if (t < s || t >= e + 0.55) return null;
  const dxIn = i === 0 ? 0 : 1920 * (1 - easeIO(prog(t, s, 0.5)));
  const dxOut = i < PG.length - 1 ? -1920 * easeIO(prog(t, e, 0.5)) : 0;
  return <div style={{position: 'absolute', inset: 0, transform: `translateX(${dxIn + dxOut}px)`}}>{children}</div>;
};

const Txt: React.FC<{at: number; y: number; x?: number; size: number; text: string; color?: string; anim?: 'rise' | 'pop'}> = ({at, y, x = 960, size, text, color = COL.ink2, anim = 'rise'}) => (
  <Fx at={at} x={x} y={y} anim={anim}>
    <div style={{fontFamily: SORA, fontWeight: 800, fontSize: size, color, lineHeight: 1.05, letterSpacing: '-0.02em'}}>{text}</div>
  </Fx>
);

// linha estilo sticker (contorno branco die-cut) + emoji em selo circular
const SlapLine: React.FC<{at: number; x: number; y: number; rot?: number; text: string; size: number; color: string; emoji?: string}> = ({at, x, y, rot = 0, text, size, color, emoji}) => (
  <Fx at={at} x={x} y={y} rot={rot} anim="slap">
    <div style={{display: 'flex', alignItems: 'center', gap: size * 0.12, filter: 'drop-shadow(0 6px 8px rgba(0,0,0,0.25))'}}>
      <div style={{fontFamily: SORA, fontWeight: 800, fontSize: size, color, lineHeight: 1, letterSpacing: '-0.02em', padding: 8, filter: OUTLINE}}>{text}</div>
      {emoji ? (
        <div style={{width: size * 0.78, height: size * 0.78, borderRadius: '50%', background: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: EMOJI, fontSize: size * 0.5, lineHeight: 1}}>{emoji}</div>
      ) : null}
    </div>
  </Fx>
);

// placa SAIDA: a seta e o corredor apontam para o lado da saida (esquerda: ← SAÍDA 🏃 · direita: 🏃 SAÍDA →)
const ExitSign: React.FC<{at: number; x: number; y: number; rot: number; dir: 'left' | 'right'; text: string}> = ({at, x, y, rot, dir, text}) => {
  const t = useT();
  const glow = 0.75 + 0.25 * Math.sin((t - at) * 9);
  const arrow = <span style={{fontFamily: INTER, fontWeight: 800, fontSize: 85, lineHeight: 1}}>{dir === 'left' ? '←' : '→'}</span>;
  const runner = <span style={{fontFamily: EMOJI, fontSize: 88, lineHeight: 1, display: 'inline-block', transform: dir === 'left' ? 'scaleX(1)' : 'scaleX(-1)'}}>🏃</span>;
  const label = <span style={{fontFamily: SORA, fontWeight: 800, fontSize: 71, letterSpacing: '0.04em', lineHeight: 1}}>{text}</span>;
  return (
    <Fx at={at} x={x} y={y} rot={rot} anim="slap" scale={0.98 + 0.02 * glow}>
      <div style={{display: 'flex', alignItems: 'center', gap: 27, padding: '0 37px', height: 170, borderRadius: 22, background: '#188C4C', border: '7px solid #fff', color: '#fff', boxShadow: '6px 8px 0 rgba(0,0,0,0.45)', boxSizing: 'border-box'}}>
        {dir === 'left' ? <>{arrow}{label}{runner}</> : <>{runner}{label}{arrow}</>}
      </div>
    </Fx>
  );
};


// BALDE + PIPOCAS como sistema: balde inteiro + pipocas soltas independentes (assets individuais ainda a chegar).
// Profundidade: a pipoca aparece acima da borda frontal (clip por `rimY`) e some "para dentro" ao descer.
export const PopcornBucket: React.FC<{at: number; x: number; y: number; rot?: number; h?: number; bucket: string; popcorns: string[]; rimY?: number; ratio?: number}> = ({at, x, y, rot = 0, h = 640, bucket, popcorns, rimY = 0.27, ratio = 1143 / 1376}) => {
  const t = useT();
  const w = h * ratio;
  return (
    <Fx at={at} x={x} y={y} rot={rot} anim="up" sway={3}>
      <div style={{position: 'relative', width: w, height: h}}>
        <Img src={staticFile(bucket)} style={{position: 'absolute', inset: 0, height: h, width: 'auto', filter: 'drop-shadow(0 12px 16px rgba(0,0,0,0.35))'}} />
        <div style={{position: 'absolute', left: -w * 0.6, right: -w * 0.6, top: -h * 0.9, height: h * (0.9 + rimY), overflow: 'hidden', pointerEvents: 'none'}}>
          {popcorns.map((src, i) => {
            const ph = (((t - at) * (0.55 + 0.13 * (i % 3)) + i * 0.37) % 1 + 1) % 1; // fases diferentes: nada mecanico
            const up = Math.sin(Math.PI * ph);
            const px = w * (0.18 + 0.64 * ((i * 0.381) % 1)) + w * 0.6;
            const py = h * 0.9 + h * rimY - up * h * (0.22 + 0.12 * (i % 3));
            return <Img key={i} src={staticFile(src)} style={{position: 'absolute', left: px, top: py, height: h * 0.11, width: 'auto', transform: `translate(-50%, -100%) rotate(${ph * 360 * (i % 2 ? 1 : -1)}deg)`}} />;
          })}
        </div>
      </div>
    </Fx>
  );
};

export const p02Schema = z.object({bucketSrc: z.string(), phoneFace: z.string(), popcorns: z.array(z.string())});
export const P02: React.FC<z.infer<typeof p02Schema>> = ({bucketSrc, phoneFace, popcorns}) => {
  const [a1, a2, a3, a4, a5] = PG;
  return (
    <Frame variant="cream">
      <Overline at={0.1} text="ANTES DA SESSÃO COMEÇAR" x={960} y={95} size={32} />
      <Fx at={0.3} x={960} y={145} anim="rise"><div style={{fontFamily: INTER, fontWeight: 700, fontSize: 28, color: '#787878', lineHeight: 1}}>um aviso do Analytics Talks</div></Fx>

      <Page i={0}>
        <ExitSign at={0.7} x={400} y={580} rot={-4} dir="left" text="SAÍDA" />
        <ExitSign at={0.85} x={1520} y={580} rot={4} dir="right" text="SAÍDA" />
        <Txt at={1.1} y={300} size={64} text="As saídas de emergência" />
        <Txt at={1.3} y={385} size={64} text="ficam nas laterais." />
        <SlapLine at={2.9} x={960} y={760} rot={-2} text="Se você falar “eu acho”," size={70} color={COL.ink2} />
        <SlapLine at={4.4} x={1000} y={900} rot={2} text="sugerimos que use-as." size={70} color={COL.orange} emoji="🏃" />
        <Sticker at={1.9} x={960} y={575} src="stickers/extintor.png" size={290} rot={4} anim="slap" />
        <Sticker at={3.6} x={260} y={880} src="personagens/lucian-still.webp" size={240} rot={-8} />
      </Page>

      <Page i={1}>
        <Emoji at={a2} x={960} y={330} ch="🙋" size={170} out={a2 + 3.2} />
        <Emoji at={a2 + 3.2} x={960} y={330} ch="😅" size={170} />
        <Txt at={a2 + 0.1} y={520} size={60} text="Levanta a mão quem já disse" />
        <SlapLine at={a2 + 1.0} x={960} y={690} rot={-3} text="“eu acho”" size={130} color={COL.orange} />
        <Txt at={a2 + 2.0} y={860} size={54} text="numa reunião de resultado." />
      </Page>

      <Page i={2}>
        <Emoji at={a3} x={960} y={330} ch="👀" size={170} />
        <Txt at={a3 + 0.1} y={520} size={72} text="Agora olha pro lado." />
        <Txt at={a3 + 1.1} y={650} size={56} text="A pessoa também levantou." />
        <SlapLine at={a3 + 2.1} x={960} y={820} rot={2} text="Você não está sozinho." size={66} color={COL.orange} emoji="🤝" />
        <Sticker at={a3 + 2.4} x={300} y={860} src="personagens/gustavo-hover-final.webp" size={210} rot={-6} />
      </Page>

      <Page i={3}>
        <Emoji at={a4} x={960} y={330} ch="📱" size={170} />
        <Txt at={a4 + 0.1} y={520} size={72} text="Celular liberado." />
        <SlapLine at={a4 + 1.0} x={960} y={680} rot={-2} text="Só vamos reclamar" size={70} color={COL.ink2} />
        <SlapLine at={a4 + 1.9} x={960} y={830} rot={2} text="se você não marcar a gente." size={70} color={COL.orange} emoji="📸" />
        <Sticker at={a4 + 2.3} x={1680} y={820} src={phoneFace} size={250} rot={7} />
      </Page>

      <Page i={4}>
        {bucketSrc ? (
          <PopcornBucket at={a5} x={1400} y={560} rot={5} h={640} bucket={bucketSrc} popcorns={popcorns} />
        ) : (
          <Fx at={a5} x={1400} y={560} rot={0} anim="up">
            <div style={{width: 520, height: 600, border: '5px dashed #B9B2A3', borderRadius: 28, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', fontFamily: SORA, fontWeight: 800, fontSize: 34, color: '#8A8372', lineHeight: 1.3}}>BALDE_NEEDS_NEW_IMAGE<br />(substituir)</div>
          </Fx>
        )}
        <Txt at={a5 + 0.1} x={640} y={400} size={76} text="Podem pegar a pipoca." />
        <SlapLine at={a5 + 1.6} x={640} y={570} rot={-2} text="Vocês vieram ao cinema" size={66} color={COL.ink2} />
        <SlapLine at={a5 + 2.8} x={660} y={700} rot={2} text="assistir a um podcast." size={66} color={COL.orange} emoji="🍿" />
        <Sticker at={a5 + 4.0} x={300} y={880} src="personagens/lucian-still.webp" size={210} rot={-6} />
        <Sticker at={a5 + 4.2} x={980} y={890} src="personagens/gustavo-still.webp" size={210} rot={6} />
      </Page>
    </Frame>
  );
};
export const p02Default = {bucketSrc: 'stickers/balde_pipoca_a_episodio300.png', phoneFace: 'personagens/gustavo-hover-transicao.webp', popcorns: [] as string[]};

// ===================================================================== P03 — tela do EP 300 (pre-sessao), estrutura da tela final
export const Logo: React.FC<{src: string; h: number}> = ({src, h}) => <Img src={staticFile(src)} style={{height: h, width: 'auto', display: 'block'}} />;
export const Group: React.FC<{at: number; label: string; children: React.ReactNode}> = ({at, label, children}) => {
  const t = useT();
  if (t < at) return null;
  const a = Math.min(1, (t - at) * 3);
  return (
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 22, opacity: a, transform: `translateY(${(1 - a) * 14}px)`}}>
      <div style={{fontFamily: INTER, fontWeight: 500, fontSize: 24, letterSpacing: '0.22em', color: '#9A9A9A', whiteSpace: 'nowrap', lineHeight: 1}}>{label}</div>
      <div style={{display: 'flex', alignItems: 'center', gap: 36, height: 96}}>{children}</div>
    </div>
  );
};
export const Sep: React.FC<{at?: number}> = ({at = 0}) => {
  const t = useT();
  return <div style={{width: 3, height: 90, background: 'rgba(255,255,255,0.28)', alignSelf: 'flex-end', opacity: t >= at ? Math.min(1, (t - at) * 3) : 0}} />;
};

export const p03Schema = z.object({pill: z.string(), kinoplexSrc: z.string()});
export const P03: React.FC<z.infer<typeof p03Schema>> = ({pill, kinoplexSrc}) => (
  <Frame variant="ink">
    <Fx at={0.1} x={960} y={400} rot={-3} anim="slap">
      <Img src={staticFile('brand/selo_episodio_300.png')} style={{height: 560, width: 'auto', filter: 'drop-shadow(0 10px 18px rgba(0,0,0,0.5))'}} />
    </Fx>
    <Fx at={1.4} x={960} y={745} anim="pop" exit="shrink" out={5.4}>
      <PillBody text={pill} emoji="🍿" size={44} variant="o" />
    </Fx>
    <div style={{position: 'absolute', left: 0, right: 0, top: 880, display: 'flex', justifyContent: 'center', alignItems: 'flex-end', gap: 56}}>
      <Group at={1.0} label="REALIZAÇÃO"><Logo src="brand/logo-metricas-boss-branca.png" h={74} /></Group>
      <Sep at={1.15} />
      <Group at={1.15} label="PATROCÍNIO">
        <Logo src="sponsors/purple-metrics.webp" h={92} />
        <Logo src="sponsors/onfly.webp" h={66} />
      </Group>
      <Sep at={1.3} />
      <Group at={1.3} label="CAFÉ OFICIAL"><Logo src="sponsors/coffee-plusplus.webp" h={92} /></Group>
      <Sep at={1.45} />
      <Group at={1.45} label="APOIADOR">
        {kinoplexSrc ? (
          <Logo src={kinoplexSrc} h={80} />
        ) : (
          <div style={{width: 200, height: 78, border: '3px dashed #777', borderRadius: 14, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: INTER, fontWeight: 500, fontSize: 15, letterSpacing: '0.08em', color: '#9A9A9A', textAlign: 'center', lineHeight: 1.25}}>KINOPLEX_WAITING_DESIGN</div>
        )}
      </Group>
    </div>
  </Frame>
);
export const p03Default = {pill: 'A sessão vai começar', kinoplexSrc: 'brand/logo_kinoplex_original.png'};
