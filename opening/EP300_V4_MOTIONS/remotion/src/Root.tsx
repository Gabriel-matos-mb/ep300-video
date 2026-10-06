import React from 'react';
import {AbsoluteFill, Composition, Series} from 'remotion';
import {SLOT_META, SlotMeta, SEQ} from './data/slots';
import {H, W, FPS, COL, SORA, INTER} from './lib/tokens';
import {Fonts} from './lib/primitives';
import {
  Chain, S01, S04, S05, S06, S07, S08, S09, S10, S11,
  chainDefault, chainSchema, s01Default, s01Schema, s04Default, s04Schema, s05Default, s05Schema, s06Default, s06Schema,
  s07Default, s07Schema, s08Default, s08Schema, s09Default, s09Schema, s10Default, s10Schema, s11Default, s11Schema,
} from './slots/slots';
import {P01, P02, P03, p01Default, p01Schema, p02Default, p02Schema, p03Default, p03Schema} from './slots/presession';
import {F01, O01, O02, f01Default, f01Schema, o01Default, o01Schema, o02Default, o02Schema, IAMetade, iaDefault, iaSchema, BQMarketing, bqDefault, bqSchema, CemMilHoras, cemDefault, cemSchema} from './slots/finale';

const frames = (...ids: string[]) => ids.reduce((n, id) => n + SLOT_META[id].frames, 0);
const common = {fps: FPS, width: W, height: H};

type Entry = {id: string; slots: string[]; cls: string; v2: string; note: string; node: React.ReactNode};
// classe = REUSE/ADAPT/NEW em relacao ao motion V2 (ver EP300_V4_MOTION_MAP.md). Timing de todos os slots mudou -> ADAPT.
export const ENTRIES: Entry[] = [
  {id: 'S01-A-VOLTA', slots: ['S01'], cls: 'ADAPT', v2: 'C02_01 HISTORIA_LINHA_DO_TEMPO', note: 'a volta · cenário antigo', node: <S01 {...s01Default} />},
  {id: 'S02S03-GA4-CHAIN', slots: ['S02', 'S03'], cls: 'ADAPT', v2: 'C03_03 + C03_05', note: '153 · 4 em 10 → GA4 3 em 10 (dado mudou)', node: <Chain {...chainDefault} />},
  {id: 'S04-ATRIB-INCREM', slots: ['S04'], cls: 'ADAPT', v2: 'C03_07 (trecho das pills)', note: 'atribuição · incrementalidade · 4 em 10', node: <S04 {...s04Default} />},
  {id: 'S05-BOTAO-MODELO', slots: ['S05'], cls: 'ADAPT', v2: 'C03_08 BOTAO_VIRA_MODELO', note: 'taguear botão → confiar no modelo', node: <S05 {...s05Default} />},
  {id: 'S06-SETORES', slots: ['S06'], cls: 'ADAPT', v2: 'C05_02 (só os setores)', note: 'banco · varejo · mídia · telecom', node: <S06 {...s06Default} />},
  {id: 'S07-FICHA-PHILL-MAFE', slots: ['S07'], cls: 'ADAPT', v2: 'C05_05 FICHA (1ª metade)', note: 'Phill 29× · Mafê 24×', node: <S07 {...s07Default} />},
  {id: 'S08-FICHA-BONEL', slots: ['S08'], cls: 'ADAPT', v2: 'C05_05 FICHA (2ª metade)', note: 'Bonel 7× · "até pra dar boleto"', node: <S08 {...s08Default} />},
  {id: 'S09-FEV22-27DIAS', slots: ['S09'], cls: 'ADAPT', v2: 'C06_03 (só fev/22 + 27 dias)', note: 'todinho · +27 dias', node: <S09 {...s09Default} />},
  {id: 'S10-MERIDIAN-MCP', slots: ['S10'], cls: 'ADAPT', v2: 'C06_05 (sem Layla, sem dez/24)', note: 'Meridian · 1º MCP · julho', node: <S10 {...s10Default} />},
  {id: 'S11-700-MIL', slots: ['S11'], cls: 'ADAPT', v2: 'C07_02 (só 700 mil)', note: '700 mil vezes alguém apertou o play', node: <S11 {...s11Default} />},
];

const SLATE = 22; // ~0,9 s

const Slate: React.FC<{e: Entry}> = ({e}) => {
  const a: SlotMeta = SLOT_META[e.slots[0]];
  const b: SlotMeta = SLOT_META[e.slots[e.slots.length - 1]];
  const dur = (e.slots.reduce((n, id) => n + SLOT_META[id].frames, 0) / FPS).toFixed(2);
  return (
    <AbsoluteFill style={{background: '#000', color: COL.white, fontFamily: SORA, padding: 120, justifyContent: 'center'}}>
      <Fonts />
      <div style={{fontFamily: INTER, fontWeight: 800, letterSpacing: '0.2em', color: COL.orange, fontSize: 30}}>{e.slots.join(' + ')} · {e.cls}</div>
      <div style={{fontWeight: 800, fontSize: 84, marginTop: 24}}>{e.note}</div>
      <div style={{fontWeight: 600, fontSize: 40, marginTop: 36, opacity: 0.85}}>Premiere V1: {a.tcIn} → {b.tcOut} · {dur} s · câmera DESATIVADA</div>
      <div style={{fontWeight: 600, fontSize: 32, marginTop: 20, opacity: 0.6}}>V2 de origem: {e.v2}</div>
    </AbsoluteFill>
  );
};

const Reel: React.FC = () => (
  <Series>
    {ENTRIES.map((e) => (
      <React.Fragment key={e.id}>
        <Series.Sequence durationInFrames={SLATE}>
          <Slate e={e} />
        </Series.Sequence>
        <Series.Sequence durationInFrames={e.slots.reduce((n, id) => n + SLOT_META[id].frames, 0)}>{e.node}</Series.Sequence>
      </React.Fragment>
    ))}
  </Series>
);

const REVISED = ['S01-A-VOLTA', 'S05-BOTAO-MODELO', 'S07-FICHA-PHILL-MAFE', 'S08-FICHA-BONEL', 'S09-FEV22-27DIAS', 'S10-MERIDIAN-MCP'];
const revEntries = ENTRIES.filter((e) => REVISED.includes(e.id));
const ReelRev: React.FC = () => (
  <Series>
    {revEntries.map((e) => (
      <React.Fragment key={e.id}>
        <Series.Sequence durationInFrames={SLATE}><Slate e={e} /></Series.Sequence>
        <Series.Sequence durationInFrames={e.slots.reduce((n, id) => n + SLOT_META[id].frames, 0)}>{e.node}</Series.Sequence>
      </React.Fragment>
    ))}
  </Series>
);
const revFrames = revEntries.reduce((n, e) => n + SLATE + e.slots.reduce((m, id) => m + SLOT_META[id].frames, 0), 0);

export const reelFrames = ENTRIES.reduce((n, e) => n + SLATE + e.slots.reduce((m, id) => m + SLOT_META[id].frames, 0), 0);

export const Root: React.FC = () => (
  <>
    <Composition id="S01-A-VOLTA" component={S01} schema={s01Schema} defaultProps={s01Default} durationInFrames={frames('S01')} {...common} />
    <Composition id="S02S03-GA4-CHAIN" component={Chain} schema={chainSchema} defaultProps={chainDefault} durationInFrames={frames('S02', 'S03')} {...common} />
    <Composition id="S04-ATRIB-INCREM" component={S04} schema={s04Schema} defaultProps={s04Default} durationInFrames={frames('S04')} {...common} />
    <Composition id="S05-BOTAO-MODELO" component={S05} schema={s05Schema} defaultProps={s05Default} durationInFrames={frames('S05')} {...common} />
    <Composition id="S06-SETORES" component={S06} schema={s06Schema} defaultProps={s06Default} durationInFrames={frames('S06')} {...common} />
    <Composition id="S07-FICHA-PHILL-MAFE" component={S07} schema={s07Schema} defaultProps={s07Default} durationInFrames={frames('S07')} {...common} />
    <Composition id="S08-FICHA-BONEL" component={S08} schema={s08Schema} defaultProps={s08Default} durationInFrames={frames('S08')} {...common} />
    <Composition id="S09-FEV22-27DIAS" component={S09} schema={s09Schema} defaultProps={s09Default} durationInFrames={frames('S09')} {...common} />
    <Composition id="S10-MERIDIAN-MCP" component={S10} schema={s10Schema} defaultProps={s10Default} durationInFrames={frames('S10')} {...common} />
    <Composition id="S11-700-MIL" component={S11} schema={s11Schema} defaultProps={s11Default} durationInFrames={frames('S11')} {...common} />
    <Composition id="P01-CONTAGEM" component={P01} schema={p01Schema} defaultProps={p01Default} durationInFrames={71} {...common} />
    <Composition id="P02-AVISO" component={P02} schema={p02Schema} defaultProps={p02Default} durationInFrames={744} {...common} />
    <Composition id="P03-TELA-300" component={P03} schema={p03Schema} defaultProps={p03Default} durationInFrames={138} {...common} />
    <Composition id="F01-FINAL-300" component={F01} schema={f01Schema} defaultProps={f01Default} durationInFrames={169} {...common} />
    <Composition id="O01-VOLTANDO-NO-TEMPO" component={O01} schema={o01Schema} defaultProps={o01Default} durationInFrames={86} {...common} />
    <Composition id="IA-METADE" component={IAMetade} schema={iaSchema} defaultProps={iaDefault} durationInFrames={60} {...common} />
    <Composition id="BQ-MARKETING" component={BQMarketing} schema={bqSchema} defaultProps={bqDefault} durationInFrames={139} {...common} />
    <Composition id="CEM-MIL-HORAS" component={CemMilHoras} schema={cemSchema} defaultProps={cemDefault} durationInFrames={72} {...common} />
    <Composition id="O02-2038-VIAGEM" component={O02} schema={o02Schema} defaultProps={o02Default} durationInFrames={182} {...common} />
    <Composition id="ANNOTATED-REVIEW" component={ReelRev} durationInFrames={revFrames} {...common} />
    <Composition id="REVIEW-REEL" component={Reel} durationInFrames={reelFrames} {...common} />
  </>
);
export const _seq = SEQ;
