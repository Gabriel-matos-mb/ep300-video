// Render das camadas V4 para a REVIEW_01: 1280x720 (scale 2/3) @ 23.976, ProRes. Rode DENTRO de remotion/:
//   node tools/render_layers.mjs <outDir> [ID,ID,...]
import path from 'node:path';
import fs from 'node:fs';
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';

const root = process.cwd();
const serveUrl = await bundle({entryPoint: path.resolve(root, 'src/index.ts'), publicDir: path.resolve(root, '../assets')});
const out = path.resolve(root, process.argv[2]);
fs.mkdirSync(out, {recursive: true});

// layer id -> [composition, kind]
const MAP = {
  P01: ['P01-CONTAGEM', 'opaque'], P02: ['P02-AVISO', 'opaque'], P03: ['P03-TELA-300', 'opaque'],
  S01: ['S01-A-VOLTA', 'opaque'], S02S03: ['S02S03-GA4-CHAIN', 'opaque'], S04: ['S04-ATRIB-INCREM', 'opaque'],
  S05: ['S05-BOTAO-MODELO', 'opaque'], S06: ['S06-SETORES', 'opaque'], S07: ['S07-FICHA-PHILL-MAFE', 'opaque'],
  S08: ['S08-FICHA-BONEL', 'opaque'], S09: ['S09-FEV22-27DIAS', 'opaque'], S10: ['S10-MERIDIAN-MCP', 'opaque'],
  S11: ['S11-700-MIL', 'opaque'], F01: ['F01-FINAL-300', 'opaque'],
  O01: ['O01-VOLTANDO-NO-TEMPO', 'alpha'], O02: ['O02-2038-VIAGEM', 'opaque'],
  IA_METADE: ['IA-METADE', 'alpha'], BQ_MARKETING: ['BQ-MARKETING', 'alpha'], CEM_MIL_HORAS: ['CEM-MIL-HORAS', 'alpha'],
};
const only = process.argv[3] ? process.argv[3].split(',') : Object.keys(MAP);
for (const id of only) {
  const [cid, kind] = MAP[id];
  const composition = await selectComposition({serveUrl, id: cid});
  const opts = kind === 'alpha'
    ? {codec: 'prores', proResProfile: '4444', imageFormat: 'png', pixelFormat: 'yuva444p10le'}
    : {codec: 'prores', proResProfile: 'hq', imageFormat: 'png', pixelFormat: 'yuv422p10le'};
  await renderMedia({composition, serveUrl, scale: Number(process.env.RSCALE || 2 / 3), outputLocation: path.join(out, `${id}.mov`), ...opts});
  console.log('layer', id, composition.durationInFrames);
}
