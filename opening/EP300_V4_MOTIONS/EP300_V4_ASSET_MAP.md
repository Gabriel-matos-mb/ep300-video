# EP300 — Mapa de assets oficiais (V4)

> 02/10/2026. **Fonte prioritária dos stickers/emojis refeitos:** `…/01_VIDEO DE ABERTURA/00_ASSETS E INSERTS/stickers e emojis refeitos` (caminho > 260 caracteres: copiar com prefixo `\\?\` no Windows).
> Ordem de decisão: **asset oficial fornecido > asset antigo > emoji genérico > placeholder.** Dúvida entre versões → sinalizar, não escolher em silêncio.
> Cópias de trabalho em `assets/` (a pasta do Drive não foi alterada). Nenhum asset foi gerado, redesenhado ou recortado por mim.

## Assets fornecidos e onde estão sendo usados
| Asset (arquivo no Drive) | Cópia | Uso agora | Camada editável |
|---|---|---|---|
| `Adesivo recortado da caixinha Toddynho.png` | `stickers/toddynho.png` | **S09** (+27 dias) — prop `toddynhoSrc` | sim (prop) |
| `Adesivo do DeLorean com contorno branco.png` | `stickers/delorean.png` | **O01** (setup, PRESENTE ← PASSADO) e **O02** (payoff, AGORA → 2038) | layer `delorean` |
| `Dupla futurista em sintonia.png` (**Marty + Doc numa só arte**) | `stickers/dupla_marty_doc.png` | O01 (reação curta) e O02 (reação na chegada) | layer `dupla`. **Não há arquivos separados de Marty e Doc**; não recortei (cortaria o contorno). Se quiser removê-los individualmente, preciso dos dois arquivos |
| `Adesivo de extintor vermelho-2.png` | `stickers/extintor.png` | **Aviso p.1** (saídas de emergência), entre as placas | sim |
| `Adesivo cartoon de microfone DYLAN-1.png` | `stickers/microfone.png` | **não usado**: nenhum redline pede função de podcast/transição aqui. Disponível; candidato a transição cinema → Analytics Talks |
| `3e2a1087-….png` (balde, face "EPISÓDIO 300 · Analytics Talks · QR · Purple/MB · apoio Kinoplex") | `stickers/balde_pipoca_a_episodio300.png` | **Aviso p.5** — `bucketSrc` (padrão) | `PopcornBucket` |
| `5762c52c-….png` (balde, face "Do Império dos Dados Ao Futuro da Mensuração") | `stickers/balde_pipoca_b_imperio.png` | **não usado** | ver dúvida abaixo |
| `logos/logo_kinoplex2.png` | `brand/logo_kinoplex_original.png` | **P03 e F01** como APOIADOR. **Branca, original, nunca sticker** | `<Logo>` (prop `kinoplexSrc`) |
| pipocas soltas individuais | — | **AINDA NÃO EXISTEM** — nada inventado | `PopcornBucket.popcorns` (lista vazia) |

### Dúvida a sinalizar (balde)
Há **dois baldes** na pasta (duas faces: a do "EPISÓDIO 300 / Kinoplex" e a do "Do Império dos Dados…"). Usei a **A (EPISÓDIO 300)** no aviso por combinar com "vocês vieram ao cinema assistir a um podcast". Troca = prop `bucketSrc`. Confirme qual é a oficial ou se o balde deve girar entre as duas faces.

## Sistema balde + pipocas (abertura **e** looping) — reutilizável
Componente `PopcornBucket` (`remotion/src/slots/presession.tsx`):
- `POPCORN_BUCKET` = `bucket` (imagem inteira do balde) · `POPCORN_01…n` = lista `popcorns` (um arquivo por pipoca) · `POPCORN_GROUP` = o conjunto animado.
- **Profundidade:** a imagem do balde fica por baixo; as pipocas são cortadas por uma linha `rimY` (fração da altura onde começa a borda frontal) — aparecem acima da boca e somem "para dentro" ao descer; nunca ficam coladas por trás.
- **Movimento:** cada pipoca sobe, gira e volta numa fase própria (períodos e alturas diferentes) — sem sincronia mecânica; curto e controlado, sem explosão/confete.
- **Bounds:** pipocas soltas **podem** atravessar o quadro durante a trajetória; as estacionárias não podem ser cortadas. Balde, extintor, microfone, Marty+Doc, DeLorean, Toddynho: inteiros em estado de leitura (STICKER_BOUNDS_CHECK).
- **Pendente (aguarda assets):** ligar `popcorns` aos arquivos individuais quando você os colocar na pasta.

### Registro para o projeto EP300 Cinema Loop Video (não executado)
Lucian com o baldinho: microanimação de pipocas transbordando do balde que ele segura — preservar Lucian e o balde real; adicionar só as pipocas necessárias acima da boca do balde; respeitar perspectiva e oclusão (borda frontal); não cobrir rosto nem informação; loop curto (sobe → gira → desce/some atrás da borda → outra aparece), fases independentes. Reuso: `PopcornBucket` + pipocas soltas.

## Regras visuais permanentes (EP300)
- Emoji **solto** → estética sticker (contorno branco consistente); emoji **inline** em pill/texto pode ficar inline.
- Nenhum sticker/emoji/logo/rosto/número/card/pill/foto cortado em estado de leitura; safe area 90/54 px. Check: `reports/sticker_bounds.py` (`STICKER_BOUNDS_CHECK`).
- Kinoplex: logo **branca e original**, nunca sticker.
- Referência específica > genérica (Toddynho, De Volta para o Futuro).

## Beats de passagem do tempo (De Volta para o Futuro) — overlays sobre câmera ativa
| FALA EXATA (MVI_9939) | TC na timeline | FUNÇÃO | DELOREAN | MARTY+DOC | 2038 | Composição / camadas |
|---|---|---|---|---|---|---|
| "Voltando um pouco no tempo, novamente, em dezembro de 2024" (src 438,28) | 00:03:41:09 (86 q) | **SETUP** rápido | cruza direita→esquerda no eixo PRESENTE ← PASSADO e sai | dupla pequena pontua e sai | — | `O01-VOLTANDO-NO-TEMPO` · layers `delorean` `dupla` `axis` `markers` |
| "Se você apertar o play agora… tu só vai parar de escutar a Analytics Talks em 2038" (src 502,74; "2038" em 509,16) | 00:04:19:15; "2038" ≈ 00:04:26 (203 q) | **PAYOFF** | percorre AGORA → 2038 e estaciona | dupla reage na chegada (canto inferior esquerdo, fora dos rostos) | **HERO** grande (slap) | `O02-2038-VIAGEM` · layers `delorean` `dupla` `axis` `markers` `hero` |
Setup e payoff **não repetem a mesma animação** (direção, eixo e papel diferentes). Camadas separáveis por prop no Remotion Studio (`layers`); render alfa por camada só quando você aprovar.
