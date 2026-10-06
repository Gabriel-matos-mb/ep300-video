# EP300_V4_MOTIONS

Motions dos **slots** (trechos de câmera desativados) da sequência real do Premiere `MVI_9939` (5:15). PREMIERE = montagem; REMOTION = motions editáveis; RENDER = ponte.

| Pasta | O que é |
|---|---|
| `remotion/` | projeto Remotion (1920×1080 @ 23,976; escala 2 = 4K). `remotion/studio.cmd` abre o Studio. 1 composição por slot + `REVIEW-REEL`. Textos/números editáveis no painel de props. |
| `assets/` | fontes (Sora/Inter), stickers, polaroid, logo GA, gag Toddynho — copiados da V2 (pequenos). **Nenhuma câmera copiada.** |
| `previews/` | previews 960×540 H.264 por slot + `EP300_V4_MOTION_REVIEW.mp4` |
| `premiere/` | `EP300_V4_SLOTS.csv` (TC in/out dos slots) |
| `reports/` | `timeline_dump.json`, QA de cobertura, scripts de extração |
| `EP300_V4_TIMELINE_MAP.md` | timeline real (101 cortes, câmera, slots, pontos a conferir) |
| `EP300_V4_MOTION_MAP.md` | slot a slot: motion, REUSE/ADAPT/NEW, composition, transições, track |

## Reextrair depois que o Gabriel salvar o Premiere
```
cd reports
python extract_timeline.py "<caminho do .prproj>" .   # só lê (trabalha numa cópia)
python gen_slots_ts.py && python gen_maps.py
```
## Previews
```
cd remotion
node tools/render.mjs video S05-BOTAO-MODELO ../previews/S05.mp4      # 960x540
node tools/render.mjs stills S01-A-VOLTA:110                         # PNG 960x540
```
Render 4K / alpha / master: **não feito** (só com autorização).
