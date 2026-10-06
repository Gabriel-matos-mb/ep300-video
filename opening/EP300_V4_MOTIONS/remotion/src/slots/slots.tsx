import React from 'react';
import {AbsoluteFill} from 'remotion';
import {z} from 'zod';
import {Bg, Counter, DotGrid, Emoji, Ficha, Fonts, Fx, Label, Overline, Pill, PillBody, Polaroid, Slap, StickerText, Stamp, Sticker, TLAxis, useT} from '../lib/primitives';
import {COL, SORA} from '../lib/tokens';
import {easeIO, prog} from '../lib/anim';

// Todas as composicoes sao 1920x1080 @ 23.976 e cobrem o quadro INTEIRO (fundo opaco do 1o ao ultimo quadro).
// Tempos de cada elemento (`at`) = segundos desde o inicio do slot, ancorados nas palavras da fala (MVI_9939).
const Frame: React.FC<{variant: 'ink' | 'cream'; children: React.ReactNode}> = ({variant, children}) => (
  <AbsoluteFill>
    <Fonts />
    <Bg variant={variant} />
    {children}
  </AbsoluteFill>
);

// ===================================================================== S01 — cauda: "a volta do Lucian" -> "cenario antigo" (HIBRIDO: 2015/PRIME/MB TALKS ja estao na V2)
export const s01Schema = z.object({
  title: z.string(),
  pill: z.string(),
  polaroidCaption: z.string(),
  pill2: z.string(),
});
export const S01: React.FC<z.infer<typeof s01Schema>> = ({title, pill, pill2}) => (
  <Frame variant="cream">
    <Overline at={0} text={title} x={960} y={130} size={30} />
    <Pill at={0.9} x={960} y={400} rot={-3} text={pill} emoji="🎙️" size={72} />
    <Sticker at={1.2} x={640} y={680} src="personagens/gustavo-still.webp" size={300} rot={7} />
    <Sticker at={1.35} x={1280} y={680} src="personagens/lucian-still.webp" size={300} rot={-8} />
    <Pill at={3.5} x={960} y={900} rot={-4} text={pill2} size={56} variant="o" />
    {/* R03: polaroid do EP1 (Gustavo + Mafe, print corrigido) entra em "deve estar aparecendo ai pra galera" (rel 4,6 s) */}
    <Polaroid at={4.6} x={1625} y={650} rot={4} src="hist/EP001_2021_b.png" w={370} caption="EP 1 · 2021" cap={24} />
  </Frame>
);
export const s01Default = {title: 'DE ONDE VEM', pill: 'a volta do Lucian', polaroidCaption: '', pill2: 'no escritório antigo'};

// ===================================================================== S02+S03 — 153 / GA4 3 em 10 (cadeia: insert -> insert sem camera entre eles)
const PUSH_AT = 5.5; // empurrao S02 -> S03 (fundo continuo; so o conteudo desliza)
const PUSH_DUR = 0.5;
export const chainSchema = z.object({
  episodes: z.number(),
  gridTotal: z.number(),
  gridFill: z.number(),
  ga4Fill: z.number(),
  ga4Label: z.string(),
});
const S2_LEN = 5.839;
export const Chain: React.FC<z.infer<typeof chainSchema>> = ({episodes, gridTotal, gridFill, ga4Fill, ga4Label}) => {
  const t = useT();
  const p = easeIO(prog(t, PUSH_AT, PUSH_DUR));
  const dx2 = -1920 * p;
  const dx3 = 1920 * (1 - p);
  const dt = S2_LEN; // S03 comeca no instante S2_LEN da cadeia
  const Shift: React.FC<{dx: number; children: React.ReactNode}> = ({dx, children}) => (
    <div style={{position: 'absolute', inset: 0, transform: `translateX(${dx}px)`}}>{children}</div>
  );
  // S03: relogio proprio (t3 = t - dt); implementado deslocando o tempo dos filhos via wrapper de Sequence-like
  return (
    <Frame variant="ink">
      <Shift dx={dx2}>
        <Counter at={0.6} to={episodes} x={960} y={330} size={260} cdur={0.5} />
        <Overline at={1.4} text="EPISÓDIOS EM 2023" x={960} y={490} color={COL.white} size={32} />
        <DotGrid at={2.7} n={gridTotal} fill={gridFill} x={960} y={680} r={42} gap={26} fillAt={0.35} />
        <Pill at={5.0} x={960} y={860} text="4 em cada 10 = GA4" size={44} variant="o" />
      </Shift>
      {t >= PUSH_AT - 0.01 ? (
        <Shift dx={dx3}>
          <GA4Block dt={dt} fill={ga4Fill} label={ga4Label} />
        </Shift>
      ) : null}
    </Frame>
  );
};
export const chainDefault = {episodes: 153, gridTotal: 10, gridFill: 4, ga4Fill: 3, ga4Label: '3 A CADA 10 EPISÓDIOS'};

// bloco S03 com tempo proprio: re-escala `at` somando dt (os primitives leem useT global)
const GA4Block: React.FC<{dt: number; fill: number; label: string}> = ({dt, fill, label}) => (
  <>
    <Sticker at={dt - 0.15} x={640} y={430} src="stickers/googleanalytics.png" size={330} rot={-6} anim="slap" sway={3} />
    <Slap at={dt + 0.24} x={1180} y={330} rot={-6} text="GA4" size={170} />
    <Overline at={dt + 0.8} text="NUNCA SAIU DA PAUTA" x={1180} y={480} color={COL.white} size={28} />
    <DotGrid at={dt + 3.9} n={10} cols={5} fill={fill} x={1180} y={610} r={40} gap={24} fillAt={0.4} />
    <Overline at={dt + 4.7} text={label} x={1180} y={820} color={COL.white} size={30} />
  </>
);

// ===================================================================== S04 — atribuicao + incrementalidade + 4 em 10
export const s04Schema = z.object({title: z.string(), pillA: z.string(), pillB: z.string(), caption: z.string(), total: z.number(), fill: z.number()});
export const S04: React.FC<z.infer<typeof s04Schema>> = ({title, pillA, pillB, caption, total, fill}) => (
  <Frame variant="cream">
    {/* R03: composicao reequilibrada — sticker aprovado (Gustavo sorrindo) a esquerda; bloco de texto centrado no eixo 975 */}
    <Overline at={0} text={title} x={975} y={110} size={28} />
    <Sticker at={0.5} x={400} y={560} src="personagens/gustavo-hover-transicao.webp" size={330} rot={-6} anim="pop" />
    <Pill at={0.2} x={930} y={300} rot={-3} text={pillA} size={70} />
    <Pill at={1.3} x={1180} y={440} rot={3} text={pillB} size={70} />
    {/* "4 EM 10" colado SO na incrementalidade (H9): selo na ponta da pill + grade logo abaixo dela */}
    <Pill at={4.4} x={1600} y={390} rot={5} text="4 EM 10" size={48} variant="o" anim="slap" />
    <DotGrid at={4.4} n={total} fill={fill} x={1180} y={640} r={34} gap={20} fillAt={0.4} />
    <Overline at={5.4} text={caption} x={1180} y={745} color={COL.ink2} size={28} />
    <Pill at={7.5} x={1180} y={440} rot={3} text={pillB} size={70} variant="o" anim="slap" />
  </Frame>
);
export const s04Default = {title: 'O QUE ENTROU DO LADO DO GA4', pillA: 'atribuição', pillB: 'incrementalidade', caption: '4 EM CADA 10 EPISÓDIOS DESTE ANO', total: 10, fill: 4};

// ===================================================================== S05 — botao -> modelo
export const s05Schema = z.object({title: z.string(), before: z.string(), after: z.string(), tag: z.string()});
export const S05: React.FC<z.infer<typeof s05Schema>> = ({title, before, after, tag}) => (
  <Frame variant="ink">
    <Overline at={0} text={title} x={960} y={150} color={COL.white} size={30} />
    <Pill at={0.9} x={960} y={480} rot={-2} text={before} size={64} variant="o" out={2.7} exit="shrink" />
    <Pill at={3.9} x={960} y={480} rot={3} text={after} emoji="🤖" size={64} anim="slap" />
    <StickerText at={5.2} x={1300} y={780} rot={6} text={tag} size={120} />
  </Frame>
);
export const s05Default = {title: 'A PERGUNTA MUDOU', before: 'como taguear um botão?', after: 'dá pra confiar em...', tag: 'modelo.'};

// ===================================================================== S06 — setores (banco, varejo, midia, telecom)
export const s06Schema = z.object({title: z.string(), a: z.string(), b: z.string(), c: z.string(), d: z.string()});
export const S06: React.FC<z.infer<typeof s06Schema>> = ({title, a, b, c, d}) => (
  <Frame variant="cream">
    <Overline at={0} text={title} x={960} y={150} size={28} />
    <Pill at={0.28} x={420} y={420} rot={-3} text={a} emoji="🏦" size={54} />
    <Pill at={0.68} x={780} y={620} rot={3} text={b} emoji="🛒" size={54} />
    <Pill at={1.34} x={1150} y={420} rot={2} text={c} emoji="📺" size={54} />
    <Pill at={2.04} x={1510} y={620} rot={-4} text={d} emoji="📡" size={54} />
  </Frame>
);
export const s06Default = {title: 'EMPRESAS QUE PASSARAM AQUI', a: 'banco', b: 'varejo', c: 'mídia', d: 'telecom'};

// ===================================================================== S07 — ficha de presenca: Phill + Mafe
export const s07Schema = z.object({phillN: z.number(), mafeN: z.number(), badge: z.string(), polaroidCaption: z.string()});
export const S07: React.FC<z.infer<typeof s07Schema>> = ({phillN, mafeN, badge, polaroidCaption}) => (
  <Frame variant="ink">
    <Ficha at={0} rows={[
      {name: 'Phill', n: phillN, at: 1.9},
      {name: 'Mafê', n: mafeN, at: 3.6, extra: {at: 5.4, text: badge, emoji: '⭐'}},
    ]} />
    <Sticker at={0.9} x={1230} y={340} src="stickers/phill.png" size={300} rot={-6} anim="slap" />
    <Fx at={0.9} x={1230} y={540} rot={3} anim="slap"><PillBody text="Phill" size={28} /></Fx>
    <Sticker at={3.8} x={1590} y={640} src="stickers/mafe.png" size={290} rot={6} anim="slap" />
    <Fx at={3.8} x={1590} y={830} rot={-3} anim="slap"><PillBody text="Mafê" size={28} /></Fx>
    <Polaroid at={5.9} x={1610} y={250} rot={4} src="hist/EP001_2021_b.png" w={300} caption={polaroidCaption} cap={22} />
  </Frame>
);
export const s07Default = {phillN: 29, mafeN: 24, badge: 'convidada do EP 1', polaroidCaption: 'EP 1 · 2021'};

// ===================================================================== S08 — ficha de presenca: Bonel
export const s08Schema = z.object({bonelN: z.number(), extras: z.boolean()});
export const S08: React.FC<z.infer<typeof s08Schema>> = ({bonelN, extras}) => (
  <Frame variant="ink">
    <Ficha at={-1} rows={[
      {name: 'Phill', n: 29, at: 0, done: true},
      {name: 'Mafê', n: 24, at: 0, done: true, extra: {at: 0, text: 'convidada do EP 1', emoji: '⭐'}},
      {name: 'Cláudio “Coisa Rica” Bonel', n: bonelN, at: 0.2},
    ]} />
    <Sticker at={0.05} x={1250} y={470} src="stickers/bonel.png" size={420} rot={-4} anim="slap" />
    <Fx at={0.05} x={1250} y={730} rot={2} anim="slap"><PillBody text="Cláudio Bonel" size={30} /></Fx>
    {extras ? (
      <>
        <Pill at={3.7} x={1420} y={190} rot={-3} text="veio responder uma pergunta" size={34} />
        <Pill at={5.9} x={1480} y={880} rot={3} text="e ficou por anos" size={34} />
        <Pill at={7.1} x={1000} y={960} rot={-2} text="já paga até boleto" emoji="💸" size={34} variant="o" />
      </>
    ) : null}
    <Fx at={1.2} x={1250} y={800} rot={0} anim="pop"><PillBody text="recordista de fora" emoji="🏆" size={26} variant="o" /></Fx>
  </Frame>
);
export const s08Default = {bonelN: 7, extras: true};

// ===================================================================== S09 — fev/2022 + 27 dias
export const s09Schema = z.object({title: z.string(), quote1: z.string(), quote2: z.string(), toddynhoSrc: z.string(), stamp1: z.string(), stamp2: z.string()});
export const S09: React.FC<z.infer<typeof s09Schema>> = ({title, quote1, quote2, toddynhoSrc, stamp1, stamp2}) => (
  <Frame variant="cream">
    <Overline at={0} text={title} x={960} y={90} size={28} />
    <TLAxis x0={140} x1={1780} y={520} at={-1} draw={0.01} nodes={[{x: 380, label: 'FEV 2022', at: -1}]} />
    <Label at={1.4} x={400} y={330} rot={2} lines={[quote1, quote2]} size={42} />
    {toddynhoSrc ? <Sticker at={3.3} x={760} y={790} src={toddynhoSrc} size={310} rot={-5} anim="drop" sway={3} /> : null}
    <Stamp at={4.8} x={1230} y={700} rot={6} lines={[stamp1, stamp2]} size={52} fill={COL.orange} />
  </Frame>
);
export const s09Default = {title: 'A GENTE CHEGOU ANTES', quote1: '“o GA4 era esse', quote2: 'toddynho todo?”', toddynhoSrc: 'stickers/toddynho.png', stamp1: '+27 DIAS', stamp2: 'GOOGLE: FIM DO UA'};

// ===================================================================== S10 — Meridian + MCP
export const s10Schema = z.object({title: z.string(), stampA1: z.string(), stampA2: z.string(), mcp1: z.string(), mcp2: z.string(), stampB1: z.string(), stampB2: z.string()});
export const S10: React.FC<z.infer<typeof s10Schema>> = ({title, stampA1, stampA2, mcp1, mcp2, stampB1, stampB2}) => (
  <Frame variant="cream">
    <Overline at={0} text={title} x={960} y={90} size={28} />
    <TLAxis x0={140} x1={1780} y={520} at={-1} draw={0.01} nodes={[
      {x: 380, label: 'OUT 2024', at: -1},
      {x: 900, label: 'ABR 2025', at: 2.8},
      {x: 1460, label: 'JUL 2026', at: 9.2},
    ]} />
    <Stamp at={0.15} x={400} y={340} rot={-6} lines={[stampA1, stampA2]} size={46} fill={COL.orange} />
    <Label at={4.0} x={1090} y={330} rot={2} lines={[mcp1, mcp2]} size={40} />
    <Emoji at={5.6} x={1440} y={230} ch="🌍" size={96} />
    <Stamp at={9.2} x={1330} y={760} rot={6} lines={[stampB1, stampB2]} size={48} fill={COL.orange} />
  </Frame>
);
export const s10Default = {title: 'A GENTE CHEGOU ANTES', stampA1: '+3 MESES', stampA2: 'GOOGLE: MERIDIAN', mcp1: '1º MCP do mundo', mcp2: 'pro Google Analytics', stampB1: 'JULHO DE 2026', stampB2: 'O DO GOOGLE'};

// ===================================================================== S11 — 700 mil
export const s11Schema = z.object({value: z.number(), caption: z.string()});
export const S11: React.FC<z.infer<typeof s11Schema>> = ({value, caption}) => (
  <Frame variant="ink">
    <Counter at={0} to={value} x={960} y={430} size={340} fmt="{} mil" cdur={0.8} />
    <Overline at={1.4} text={caption} x={960} y={660} color={COL.white} size={32} />
  </Frame>
);
export const s11Default = {value: 700, caption: 'VEZES ALGUÉM APERTOU O PLAY'};
