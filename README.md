# EP300 · Analytics Talks — Abertura + Loop do telão

Repositório de **handoff e trilha completa** do vídeo do Episódio 300 (Kinoplex, São Paulo, 08/10/2026), para o
**Lucian** continuar o trabalho em cima do que já foi feito. Autor da produção: Gabriel (direção/edição) com Claude (execução).

> **Leia nesta ordem:** este README → [`docs/TRILHA.md`](docs/TRILHA.md) (o que aconteceu, versão a versão) →
> [`opening/EP300_NON_NEGOTIABLES.md`](opening/EP300_NON_NEGOTIABLES.md) (regras que não se reabrem) →
> [`docs/ASSETS.md`](docs/ASSETS.md), [`docs/AUDIO.md`](docs/AUDIO.md), [`docs/REMOTION.md`](docs/REMOTION.md).

## São duas peças separadas

| Peça | O que é | Estado | Código / fonte |
|---|---|---|---|
| **Abertura** | Vídeo narrativo (Gustavo + Lucian em câmera, ~5 min) exibido para a plateia **antes** da gravação. Câmera real + motions/inserts/SFX/trilha por cima. | **Finalizada** (Full HD + 4K, projeto Premiere do Gabriel é a autoridade) | [`opening/`](opening) |
| **Loop** | 120 s em loop exato, **sem áudio**, no telão **durante** a gravação: mosaico de 92 capas de episódios + "EPISÓDIO 300" + créditos + 4 microgags. | **Aprovada** (1080p + 4K, 03/10) | [`loop/`](loop) |

A Abertura termina no mesmo quadro em que o Loop começa. O Loop **não** herda narrativa nem timing de fala da Abertura — só identidade visual, assets e animações aprovadas.

## Onde estão os arquivos pesados (Drive = casa do projeto)

Raiz: `I:\Drives compartilhados\Educação\Marketing Métricas Boss\01_CANAIS_ATIVOS\02_PODCAST\2026\300_[Kinoplex] DO IMPÉRIO DOS DADOS AO FUTURO DA MENSURAÇÃO\01_VIDEO DE ABERTURA\`

| Pasta no Drive | O que tem |
|---|---|
| `03_EDITADOS/VERSÃO FINAL/` | **Masters entregues:** `ABERTURA-EP300 - VF EM 4Q.mp4` (1,9 GB), `…VF EM FULL HD.mp4` (950 MB), `EP300_LOOP_FINAL_1080p.mp4`, `EP300_LOOP_FINAL_4K.mp4` |
| `02_PROJETOS/` | **`ep 300 final.prproj`** (Premiere final do Gabriel — picture lock), projetos V0/V1/V2/R03, XMLs, backups, `EP300_SYNC_3CAM` |
| `00_ASSETS E INSERTS/` | `R03_COMPONENTES_FINAIS_4K` (S05_FIX_TACI, S10, O01, O02, C02_03), `R03_LAYERS`, `V0/V1/V2_GERADOS` (44 overlays ProRes 4444 alpha em `V2_GERADOS/OVERLAYS`, `V2_GERADOS/AUDIO`), `stickers e emojis refeitos`, `logos`, `300-handoff-video`, guia visual e guia de animação |
| `01_BRUTOS/` | `CAM_GERAL.mp4`, câmeras Gustavo/Lucian, `NOVOS TAKES-REGRAVADO` |
| `EP300_HANDOFF_LUCIAN/` | Pacote anterior (30/09, estado V2) com música, SFX, stems — ver [`docs/AUDIO.md`](docs/AUDIO.md) |

**O que está neste repo:** código (motor V2 em Python, Remotion, scripts de mix/XML/QA), docs, manifests, JSONs de timing/cues, XML de revisão,
stickers/logos/fontes/gráficos e as imagens do mosaico do Loop (Git LFS), mais os dois renders finais do Loop em [`loop/renders/`](loop/renders).
**O que NÃO está (de propósito):** masters da Abertura (2,8 GB — estouram a cota do LFS), overlays ProRes, brutos de câmera, projetos Premiere e
**áudio licenciado** (Motion Array: licença da conta MB, redistribuição não verificada; ver AUDIO.md).

## Mapa do repositório

```
README.md
docs/            TRILHA, ASSETS, AUDIO, REMOTION, DRIVE_MAP + wiki/ (router, roteiro, princípios, fechamento)
opening/         Abertura: planos V0→V2, v0/v1/v2 (motor Python), review01 (R01→R03), EP300_V4_MOTIONS (Remotion + assets + redlines), handoff
loop/            Loop: scene.json (manifesto), build.py (renderizador), assets/, versions/, renders/ (finais), tools/export_final.py
handoff-2026-09-30/  pacote do Drive (manifest.json de assets, timeline-notes, edit plan V2, XML V2, biblioteca de stickers/logos/gráficos)
```

## Princípios (resumo — texto completo em `opening/EP300_NON_NEGOTIABLES.md` e `docs/wiki/`)
1. **Premiere do Gabriel é a autoridade editorial** (cortes, multicam, cor, áudio). Não reconstruir câmera com FFmpeg.
2. **KEEP BY DEFAULT, DROP BY EXCEPTION.** A V2 aprovada é o DNA criativo; correção = re-renderizar **uma camada**, não remontar.
3. **Cinema ≠ interface:** nada de "clique/toque/play/cursor" no telão; safe area ≥ 90 px laterais / ≥ 54 px verticais; SFX nunca compete com voz.
4. Grafia **LAYLA** (com Y); é "a **volta do Lucian**". Kinoplex = logo branco oficial; Onfly = logo inteira; logos institucionais nunca viram sticker.
5. Asset ausente = placeholder/flag, nunca invenção; sticker aprovado não se regenera.

## Rodar o Loop (reprodutível)
```bash
cd loop
pip install pillow numpy          # + ffmpeg no PATH
python build.py --frame 47        # um quadro -> out/frame_47.00.png
BUILD_WORKERS=8 python build.py   # render completo (~15 min) -> out/EP300_LOOP_V3_REVIEW.mp4
python tools/export_final.py      # 1080p + 4K (4K = ampliação Lanczos do quadro 1080p)
```
Tudo que é editável está em `loop/scene.json` (troque arquivos em `assets/` mantendo o nome, ou ajuste timelines).

## Rodar os motions Remotion
Ver [`docs/REMOTION.md`](docs/REMOTION.md).
