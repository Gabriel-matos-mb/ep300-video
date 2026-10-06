# EP300 · Loop do telão · V0 (proxy)

Vídeo que fica em **loop no telão do Kinoplex durante a gravação do podcast** (08/10/2026). **Entregável separado
da Abertura** (`../ep300-cinema-opening/`) — não é uma versão dela. Abertura chama atenção; o Loop cria atmosfera.

- **Formato:** 1920×1080 · 16:9 · 30 fps · H.264 MP4 · **120 s** · sem áudio · loop exato (frame(120 s) ≡ frame(0)).
- **Custo adicional:** R$ 0 (Python + Pillow + numpy + ffmpeg locais, assets já existentes do EP300).
- **Estado:** V0 PROXY (CRF 20, ~40 MB). **Master de cinema não gerado.**

## Conceito
Estado-base **calmo**: fundo escuro pontilhado (bolinhas do site), colagem de prints/thumbs de episódios antigos em
3 profundidades com parallax orbital lentíssimo (6–22 px em 30–60 s) e "respiração" de 1 % em 20 s; grande **EPISÓDIO 300**
em adesivo (balanço de ±0,7° em 12 s, escala ±1,2 % em 10 s); logo Analytics Talks; pílula "Toca pra ver o que rolou até aqui.";
patrocinadores **estáticos** na base. Por cima disso, **3 microinterações em 120 s** (≈ 25 s de "vida", ≈ 95 s de calma).

| Quando | Microinteração |
|---|---|
| 12–20 s | Gustavo aparece à esquerda, fica surpreso, sai. |
| 30–41 s / 70–81 s | "Holofote": um cartão da colagem sobe de brilho +4 % de escala e volta (elemento aparecendo/desaparecendo, sem texto). |
| 50–61 s | Lucian aparece → a pipoca surge e dá um pulinho → Lucian reage (surpresa → sorriso) → pipoca some → Lucian sai. |
| 92–104 s | Os dois aparecem; Gustavo olha de lado pro Lucian; Lucian devolve um sorriso; saem. |

Sem cortes, sem flash, sem texto novo, sem transição grande. Bloco de patrocinadores nunca se move.

## Como editar (nada exige reconstruir a cena)
Tudo está em **`scene.json`** (manifesto) — a animação lê o manifesto e os PNGs; **asset visual ≠ lógica de animação**.

| Quero trocar | Faça |
|---|---|
| Gustavo / Lucian (rosto) | substitua os arquivos em `assets/stickers/<gustavo|lucian>/` **mantendo o nome** (`still`=base, `hover-transicao`=sorriso, `hover-final`=surpresa, `arraste-final`=olhar de lado) ou aponte outro caminho em `actors[].states`. Qualquer tamanho/proporção: o motor recorta o transparente e normaliza pelo maior lado (`size`). Testado com sticker de outra proporção (`out/swap_test_gustavo_bonel.png`). |
| Pipoca | `assets/stickers/pipoca.png` (ou `props[0].file`). |
| Logo Analytics Talks | `title.logo.file`. |
| Patrocinador / Café | `sponsors.patrocinio[]` / `sponsors.cafe[]` (ordem = ordem na tela). |
| Thumbs da colagem | `collage.cards[].file` (posição, ângulo, profundidade, brilho, período por cartão). |
| Quando cada coisa acontece | `actors[].presence` (0→1, keyframes em s), `actors[].state` (troca de expressão com crossfade 0,3 s), `props[].presence/hop`, `collage.spotlights`. |
| Duração | `canvas.duration` — mantenha múltiplo dos períodos (30/60 s dos cartões, 20/12/10/3 s) para o loop continuar exato. |

Regenerar: `python build.py` (≈ 6 min, usa todos os núcleos) → `out/EP300_LOOP_V0_PROXY.mp4`.
Só um quadro: `python build.py --frame 55` · folha de contato: `python build.py --contact` · QA: `python qa.py` (→ `out/qa_report.json`, `out/qa_motion.png`).
Dependências: Python 3.12, Pillow ≥ 11, numpy, ffmpeg no PATH (matplotlib opcional p/ o gráfico do QA).

## Assets usados (origem)
- `assets/thumbs/` — prints de episódios 282–288 e quadros do EP 126 (`…/V1_GERADOS/PRINTS`, `EP126` — os mesmos da Abertura V1).
- `assets/stickers/{gustavo,lucian}/` — adesivos vivos do handoff Claudio/Lucian (`300-handoff-video/assets/personagens`): **só cabeça/rosto, contorno branco, sem recorte novo**.
- `assets/stickers/pipoca.png` — `STICKER PIPOCA.png` (nova referência do Gabriel, `stickers e emojis refeitos/`).
- `assets/sponsors/*.webp`, `assets/brand/selo-analytics-talks.webp` — handoff `/300`.
- Fonte Sora (`fonts/`), paleta creme/laranja/tinta do handoff. "300" e "EPISÓDIO" são **texto real** em estilo adesivo (não o selo com rostos, para não duplicar Gustavo/Lucian).
- `assets/brand/selo_episodio_300.png` está na pasta mas **não é usado** (referência).

## Placeholders / pendências
1. **Stickers Gustavo/Lucian**: são os do site (fotos reais, 4 expressões); Gabriel prepara versões melhores → trocar arquivos.
2. **Mapa de patrocinadores**: "Patrocínio" = Purple Metrics, Eletromidia, Onfly, Reportei, Sinatra; "Café Oficial" = Coffee++ (assumido pelos logos do handoff `/300`; confirmar a lista final).
3. **Layout estático aprovado**: não encontrei o arquivo (PNG/Figma) — montei a composição a partir da descrição do brief e dos assets. Se existir, comparar e ajustar `scene.json`.
4. **Eletromidia** sai pequeno (logo baixo/largo, ~40 px de altura) — pedir versão mais alta se quiser mais presença.
5. **Master**: não gerado (CRF 20 proxy). Antes do master: teste no projetor real (brilho/contraste, safe area do Kinoplex).

## Registro (não implementado)
- 💡 OPORTUNIDADE DE ROTA: o motor `build.py` + `scene.json` (atores com estados, presença por keyframes, loop exato por períodos divisores) serve de base para outros loops de evento/idle (ex.: telão de intervalo). Não generalizado agora.
- Studio: `studio_handoff.py` registra o Loop como output próprio `ep300-loop` (card `ep300-video-looping`, produção `ep300-telao-looping`); a página `#/ep300` ganhou a seção "Looping do telão" separada de "Abertura · versões".

---
## V1 (29/09) — refinamento pós-revisão do V0
Direção aprovada; mudanças: **CTA/pílula removidos** (nada com cara de botão), **mosaico de acervo** (92 cartões / 60 imagens: thumbs oficiais EP260–289, prints do estúdio principal, EP126 e só 6% de azul SP; 33 episódios), **troca lenta** em 16 cartões (dissolve de 10 s, volta ao original — costura circular), **4 microgags** (espiada · pipoca · cursor puxa o Lucian · empurrão) com ≥15 s de calma entre eles, **patrocinadores modulares e PROVISÓRIOS** (Patrocínio Oficial: Purple Metrics/"Corpo" e Onfly a confirmar · Café Oficial: Coffee++ · Realização: logo oficial Métricas Boss, sem rotação). Sem áudio.
Regenerar: `python make_v1_scene.py` (re-sorteia mosaico e reescreve `scene.json`) → `BUILD_WORKERS=8 python build.py` (~15 min) → `python qa.py`. V0: `versions/scene_V0.json` (+ MP4).
Limitação: não há thumbs de episódios anteriores ao 251 (Rio antigo) — colocar em `assets/mosaic` e rodar `make_v1_scene.py`.
