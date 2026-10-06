# REMOTION — motions dos slots (EP300 V4)

Projeto: [`opening/EP300_V4_MOTIONS/remotion/`](../opening/EP300_V4_MOTIONS/remotion). 1920×1080 @ **23,976 fps** (mesma taxa da sequência do Premiere),
fundo **opaco** do primeiro ao último quadro dos slots. **Escala 2 = 4K nativo sem perda** (`scale=2` / `RSCALE=2`).
`publicDir` = `../assets` (fontes, stickers, logos) — troque arquivos lá sem abrir código.

## Rodar
```bash
cd opening/EP300_V4_MOTIONS/remotion
npm install                       # node_modules não está no repo
studio.cmd                        # (Windows) ou: npx remotion studio src/index.ts
node tools/render.mjs stills S01-A-VOLTA:110,S05-BOTAO-MODELO:60     # PNG 960x540
node tools/render.mjs video S01-A-VOLTA ../previews/S01.mp4          # preview 960x540
node tools/render.mjs qa                                             # PNGs com alfa nos quadros-limite
RSCALE=2 node tools/render_layers.mjs ...                            # camadas .mov com alfa; 4K = RSCALE=2
```
`assets/` precisa estar presente (vem do Drive: `02_PROJETOS/EP300_ABERTURA_R03_EDITAVEL/_insumos/EP300_V4_MOTIONS_assets/`; neste repo já está em `EP300_V4_MOTIONS/assets/`).
**4K / alpha / master só com OK explícito do Gabriel.**

## Composições (`src/Root.tsx`)
| Grupo | IDs | Conteúdo |
|---|---|---|
| Slots (câmera desativada na sequência `MVI_9939`) | `S01-A-VOLTA`, `S02S03-GA4-CHAIN`, `S04-ATRIB-INCREM`, `S05-BOTAO-MODELO`, `S06-SETORES`, `S07-FICHA-PHILL-MAFE`, `S08-FICHA-BONEL`, `S09-FEV22-27DIAS`, `S10-MERIDIAN-MCP`, `S11-700-MIL` | linhas do tempo, contadores, grade "4 em 10 / 3 em 10", fichas de presença, etc. (mapa: `EP300_V4_MOTION_MAP.md`) |
| Pré-sessão / final | `P01-CONTAGEM`, `P02-AVISO` (`PopcornBucket`, props `bucketSrc`, `rimY`), `P03-TELA-300`, `F01-FINAL-300` | contagem, aviso para a sala, tela 300, final |
| Overlays/inserts | `O01-VOLTANDO-NO-TEMPO`, `O02-2038-VIAGEM`, `IA-METADE`, `BQ-MARKETING`, `CEM-MIL-HORAS` | DeLorean/Marty+Doc, 2038, "IA metade", BigQuery → marketing, "100+ mil horas" |
| Revisão | `ANNOTATED-REVIEW`, `REVIEW-REEL` | reel de revisão |

Dados editáveis por composição: painel de props do Studio (textos/números); lista de slots em `src/data/slots.ts` (`EP300_V4_SLOTS.csv` em `premiere/`).
Tokens de marca (mesmos do motor V2, `v2/gfx.py`): `src/lib/tokens.ts`; primitivos de animação: `src/lib/anim.ts`, `primitives.tsx`.

## Sistema balde + pipocas (Abertura **e** Loop)
`PopcornBucket`: imagem inteira do balde por baixo; as pipocas são cortadas por `rimY` (fração da altura onde começa a borda frontal) — aparecem acima da
boca e somem "para dentro" ao descer. Balde oficial = **A "EPISÓDIO 300"** (`assets/stickers/balde_pipoca_a_episodio300.png`); o B ("Do Império dos Dados…") existe mas não foi usado.
Pipocas soltas: `Sete pipocas estouradas em adesivos.png` (recortadas em `loop/assets/stickers/pipocas/`).

## Regras de produção nos motions
- Texto fala com a sala (sem "clique/toque/play/cursor"); safe area 90 px laterais / 54 px verticais; tempo real de leitura em tela sem voz.
- Stickers: contorno branco + sombra sólida deslocada; rotações do conjunto {−8, 5, −4, 7, −6, 3}°; Sora 800 + Inter 700–800.
- Slot = momento de **substituição integral da câmera**; overlays/inserts/accents podem existir fora dele. Câmera desativada tem de estar 100% coberta.
- REUSE = 0 nos slots: a fala nova mudou o timing; reaproveitam-se gramática, assets e dados.

## Relação com o motor Python (V2)
`opening/v2/engine.py`/`plan.py` (cena = lista de elementos com tempo relativo) e `review01/b2`, `b3` geram a maioria dos layers da R03 (PIL + ffmpeg, ProRes 4444 alpha).
Remotion cobre os slots V4; o Loop usa um motor Python próprio (`loop/build.py` + `scene.json`). Roteamento de ferramentas: `docs/wiki/audiovisual-execution-router.md`.
