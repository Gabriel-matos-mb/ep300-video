# EP300 — HANDOFF VISUAL
Analytics Talks — Episódio 300

> Este pacote representa o estado atual do EP300 no momento do handoff e pode receber refinamentos posteriores decorrentes da validação final de Gustavo/Lucian.
> Preparado em 2026-09-30. É uma CÓPIA/derivação da produção — nada da pasta oficial foi movido, reorganizado ou sobrescrito.

## O que tem aqui
| Pasta | Conteúdo |
|---|---|
| `01_OPENING/` | **Abertura V2** (vídeo narrativo antes da gravação, 6:10). `MASTER_REFERENCE` = proxy 720p (master de cinema 1920x1080 **ainda não renderizado**); `XML` = Premiere (2 sequências, 42 marcadores); `EDITABLE` = manifesto, edit plan, código-fonte (`plan.py` decide tudo), stems de áudio; `ASSETS` = miniaturas dos overlays + bastidores do cold open. |
| `02_LOADING_LOOP/` | **Loop do telão V2** (120 s, 1920x1080, 30 fps, sem áudio, loop exato) — **outra peça**, exibida durante a gravação. Editável = `scene.json` + `build.py` (não há XML). `ASSETS` = mosaico de acervo (exclusivo do loop). |
| `03_SHARED_ASSETS/` | Assets usados pelas duas peças: `stickers` (pessoas), `logos`, `graphics`, `images`, `audio`/`sfx`, `fonts_reference`. |
| `04_MANIFEST/` | `assets.json` (um registro por asset), `timeline-notes.md` (cena → tempo → intenção), `provenance.md`. |

## Como ler `assets.json`
Cada item: `id`, `name`, `type`, `file` (caminho dentro do pacote), `source` (MB OFFICIAL / MOTION ARRAY / GENERATED / CREATED FOR EP300 / EXTERNAL REFERENCE / UNKNOWN),
`used_in` (cenas em que aparece — varredura estática, aproximada), `purpose`, `visual_meaning`, **`usage_context`** (o porquê, extraído da intenção da cena), `reusable`, `license_or_provenance`, `notes`.

## Linguagem visual da Abertura (resumo útil para reuso)
- **Paleta:** off‑white (#F7F3EA) · laranja MB (#F47340) · tinta (#121213). Fundo **pontilhado** (bolinhas 3 px a cada 20–26 px), creme nas cenas “de papel” e preto nas “de noite”.
- **Tipografia:** Sora 800 (números, títulos, adesivos) + Inter 700–800 tracking aberto (overlines em caixa alta).
- **Colagem/sticker:** tudo tem rotação do conjunto {−8, 5, −4, 7, −6, 3}°, contorno branco e **sombra sólida deslocada** (tipo adesivo colado); rostos = adesivos com estados (sorriso/surpresa/pensando).
- **Motion:** entradas “tapa do adesivo” (125%→100%), “pop”, “carimbo”; telas cheias encadeadas por **empurrão** (a seguinte desliza e empurra a anterior — sem câmera aparecendo); números contam; linhas do tempo desenham.
- **Ritmo/música:** câmera geral como base (fechadas só em reação); telas cheias quando a fala vira voz‑off; trilha baixa (−31 dB) sob o diálogo; SFX macios e sempre abaixo da voz (ducking −12 dB); 300 = confete + língua de sogra.
- **Regras de cinema:** sem linguagem de interface (clique/toque/play/cursor), safe area 90×54 px, tempo de leitura em telas sem voz, LAYLA com Y, “a volta do Lucian”.

## Loop (separado)
Composição: fundo pontilhado + mosaico de acervo (parallax lento) + “EPISÓDIO 300” + selo Analytics Talks + patrocinadores (Patrocínio oficial / Café oficial / Realização) + 3–4 microgags espaçados (Gustavo espia, pipoca, empurrão). Compartilha com a abertura: paleta, tipografia, patrocinadores, stickers Gustavo/Lucian, balde; é **exclusivo do loop**: o mosaico. Os últimos 1,5 s da abertura são os quadros finais do loop.

## Mais reutilizáveis
Stickers de pessoas (3–4 estados cada), logos de ferramentas em tile, gags originais, estrutura `plan.py` (cena = lista de elementos com tempo relativo), `sfx_v2.py` (SFX sintéticos), `qa_leak.py` / `qa_cues_v2.py --safe` / `qa_reading.py` (QAs determinísticos).

## Restrições / licença
- **Motion Array:** só 11 arquivos de áudio (música + SFX), licença da conta MB — ver `04_MANIFEST/provenance.md`. Não redistribuir fora da MB.
- **Logos de parceiros e de ferramentas:** marcas dos respectivos donos; patrocinadores ainda **provisórios**.
- **Emojis** (Segoe UI Emoji) não incluídos.

## Só referência (não editáveis)
Proxies MP4 (`MASTER_REFERENCE`), `caixa_pipoca_frente/verso` (versão superada), `overlays_ref/*.png`. Os 44 overlays ProRes (3,5 GB) **não foram duplicados**: estão em `00_ASSETS E INSERTS/V2_GERADOS/OVERLAYS` (ver `01_OPENING/ASSETS/OVERLAYS_LOCALIZACAO.txt`).

## Contexto do estado
Cor: o XML não leva o Lumetri do Gabriel (colar atributos no Premiere). Pendências abertas: master 1920x1080, logo MB Prime, naming dos patrocinadores, números falados × site (191/196, 140/146, 106/107 mil), SFX ainda não auditionados na sala.
