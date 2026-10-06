// Ferramenta de preview/QA (bundle uma vez; renders leves). Rode DENTRO de remotion/:
//   node tools/render.mjs stills S01-A-VOLTA:110,S05-BOTAO-MODELO:60 [outDir]
//   node tools/render.mjs video S01-A-VOLTA ../previews/S01.mp4 [scale=0.5]
//   node tools/render.mjs qa [outDir]        -> PNGs com alfa nos quadros-limite e a cada 6 quadros de TODOS os slots
// Escala 0.5 = 960x540 (preview). 4K so com autorizacao explicita do Gabriel (scale=2).
import path from 'node:path';
import fs from 'node:fs';
import {bundle} from '@remotion/bundler';
import {renderStill, renderMedia, selectComposition} from '@remotion/renderer';

const root = process.cwd();
const entry = path.resolve(root, 'src/index.ts');
const publicDir = path.resolve(root, '../assets');
const serveUrl = await bundle({entryPoint: entry, publicDir});
const [mode, a, b, c] = process.argv.slice(2);

const comp = (id) => selectComposition({serveUrl, id});

if (mode === 'stills') {
  const out = path.resolve(root, b ?? '../reports/stills');
  fs.mkdirSync(out, {recursive: true});
  for (const item of a.split(',')) {
    const [id, frame] = item.split(':');
    const composition = await comp(id);
    await renderStill({composition, serveUrl, frame: Number(frame), imageFormat: 'png', scale: 0.5, output: path.join(out, `${id}_f${String(frame).padStart(3, '0')}.png`)});
    console.log('still', id, frame);
  }
} else if (mode === 'video') {
  const composition = await comp(a);
  const scale = Number(c ?? 0.5);
  await renderMedia({composition, serveUrl, codec: 'h264', crf: 22, scale, outputLocation: path.resolve(root, b), onProgress: ({progress}) => process.stdout.write(`\r${a} ${(progress * 100).toFixed(0)}%`)});
  console.log('\nvideo', b);
} else if (mode === 'previews') {
  // previews leves 960x540 H.264 de todos os slots + REVIEW-REEL (nada em 4K, nada com alfa)
  const out = path.resolve(root, a ?? '../previews');
  fs.mkdirSync(out, {recursive: true});
  const ids = ['S01-A-VOLTA', 'S02S03-GA4-CHAIN', 'S04-ATRIB-INCREM', 'S05-BOTAO-MODELO', 'S06-SETORES', 'S07-FICHA-PHILL-MAFE', 'S08-FICHA-BONEL', 'S09-FEV22-27DIAS', 'S10-MERIDIAN-MCP', 'S11-700-MIL'];
  for (const id of [...ids, 'REVIEW-REEL']) {
    const composition = await comp(id);
    const file = id === 'REVIEW-REEL' ? 'EP300_V4_MOTION_REVIEW.mp4' : `${id}.mp4`;
    await renderMedia({composition, serveUrl, codec: 'h264', crf: 22, scale: 0.5, outputLocation: path.join(out, file)});
    console.log('preview', file);
  }
} else if (mode === 'annotated') {
  const out = path.resolve(root, a ?? '../previews');
  for (const id of ['S01-A-VOLTA', 'S05-BOTAO-MODELO', 'S07-FICHA-PHILL-MAFE', 'S08-FICHA-BONEL', 'S09-FEV22-27DIAS', 'S10-MERIDIAN-MCP', 'ANNOTATED-REVIEW']) {
    const composition = await comp(id);
    const file = id === 'ANNOTATED-REVIEW' ? 'EP300_V4_ANNOTATED_REVIEW.mp4' : `${id}.mp4`;
    await renderMedia({composition, serveUrl, codec: 'h264', crf: 22, scale: 0.5, outputLocation: path.join(out, file)});
    console.log('preview', file);
  }
  const st = path.resolve(root, '../reports/stills_rev'); fs.mkdirSync(st, {recursive: true});
  for (const [id, f] of [['S01-A-VOLTA', 140], ['S05-BOTAO-MODELO', 140], ['S07-FICHA-PHILL-MAFE', 184], ['S08-FICHA-BONEL', 190], ['S09-FEV22-27DIAS', 210], ['S10-MERIDIAN-MCP', 250]]) {
    await renderStill({composition: await comp(id), serveUrl, frame: f, imageFormat: 'png', scale: 0.5, output: path.join(st, `${id}_f${f}.png`)});
  }
} else if (mode === 'bounds') {
  // STICKER_BOUNDS_CHECK: renderiza SEM fundo, em estados de leitura, e salva PNG com alfa; analise com reports/sticker_bounds.py
  const out = path.resolve(root, a ?? '../reports/bounds');
  fs.mkdirSync(out, {recursive: true});
  const fps = 24000 / 1001;
  const T = (s) => Math.round(s * fps);
  const plan = {
    'S01-A-VOLTA': [T(5.0), 147], 'S02S03-GA4-CHAIN': [T(4.9), T(5.4), 289], 'S04-ATRIB-INCREM': [T(7.0), 231], 'S05-BOTAO-MODELO': [T(2.4), T(5.7), 141],
    'S06-SETORES': [67], 'S07-FICHA-PHILL-MAFE': [T(7.3), 185], 'S08-FICHA-BONEL': [T(7.5), 192], 'S09-FEV22-27DIAS': [T(8.3), 211], 'S10-MERIDIAN-MCP': [T(10.0), 250], 'S11-700-MIL': [89],
    'P01-CONTAGEM': [T(0.8), T(1.8), T(2.7)], 'P02-AVISO': [T(7.4), T(12.6), T(17.8), T(23.4), T(30.5)], 'P03-TELA-300': [T(5.0), 136], 'F01-FINAL-300': [T(5.0), 167],
    'O01-VOLTANDO-NO-TEMPO': [T(1.2), T(2.0)], 'O02-2038-VIAGEM': [T(7.0), T(7.8)],
  };
  for (const [id, frames] of Object.entries(plan)) {
    const composition = await selectComposition({serveUrl, id, inputProps: {qaTransparent: true}});
    for (const f of frames) {
      await renderStill({composition, serveUrl, inputProps: {qaTransparent: true}, frame: Math.min(f, composition.durationInFrames - 1), imageFormat: 'png', scale: 0.5, output: path.join(out, `${id}_${String(f).padStart(4, '0')}.png`)});
    }
    console.log('bounds', id, frames.length);
  }
} else if (mode === 'parts') {
  // partes do ASSEMBLY REVIEW (540p): telas opacas em H.264; overlays em WebM com alfa
  const out = path.resolve(root, a ?? '../previews/parts'); fs.mkdirSync(out, {recursive: true});
  for (const id of ['P01-CONTAGEM', 'P02-AVISO', 'P03-TELA-300', 'F01-FINAL-300', 'S07-FICHA-PHILL-MAFE', 'S08-FICHA-BONEL', 'S09-FEV22-27DIAS']) {
    await renderMedia({composition: await comp(id), serveUrl, codec: 'h264', crf: 22, scale: 0.5, outputLocation: path.join(out, `${id}.mp4`)});
    console.log('part', id);
  }
  for (const id of ['O01-VOLTANDO-NO-TEMPO', 'O02-2038-VIAGEM']) {
    await renderMedia({composition: await comp(id), serveUrl, codec: 'vp8', imageFormat: 'png', pixelFormat: 'yuva420p', scale: 0.5, outputLocation: path.join(out, `${id}.webm`)});
    console.log('part', id);
  }
} else if (mode === 'qa') {
  const out = path.resolve(root, a ?? '../reports/qa_alpha');
  fs.mkdirSync(out, {recursive: true});
  const ids = ['S01-A-VOLTA', 'S02S03-GA4-CHAIN', 'S04-ATRIB-INCREM', 'S05-BOTAO-MODELO', 'S06-SETORES', 'S07-FICHA-PHILL-MAFE', 'S08-FICHA-BONEL', 'S09-FEV22-27DIAS', 'S10-MERIDIAN-MCP', 'S11-700-MIL'];
  for (const id of ids) {
    const composition = await comp(id);
    const n = composition.durationInFrames;
    const frames = new Set([0, 1, 2, n - 3, n - 2, n - 1]);
    for (let f = 0; f < n; f += 6) frames.add(f);
    if (id === 'S02S03-GA4-CHAIN') for (let f = 125; f <= 150; f++) frames.add(f); // janela do empurrao insert->insert, quadro a quadro
    for (const f of [...frames].sort((x, y) => x - y)) {
      await renderStill({composition, serveUrl, frame: f, imageFormat: 'png', scale: 0.25, output: path.join(out, `${id}_${String(f).padStart(4, '0')}.png`)});
    }
    console.log('qa', id, frames.size, 'quadros');
  }
}
