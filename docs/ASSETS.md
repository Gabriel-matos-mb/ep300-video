# ASSETS — biblioteca do EP300

Regra: **asset não é só arquivo** — carrega origem, significado, uso e licença. O registro por asset está em
[`handoff-2026-09-30/manifest/assets.json`](../handoff-2026-09-30/manifest/assets.json) (122 itens: 47 MB OFFICIAL · 36 CREATED FOR EP300 · 26 GENERATED ·
11 MOTION ARRAY (só áudio) · 2 EXTERNAL REFERENCE) com `used_in`, `purpose`, `usage_context`, `reusable`, `license_or_provenance`.
Origens/licenças: [`provenance.md`](../handoff-2026-09-30/manifest/provenance.md). Integridade: [`MANIFEST_SHA256.txt`](../MANIFEST_SHA256.txt).

## Onde está cada grupo
| Grupo | No repo | Original no Drive (sob `01_VIDEO DE ABERTURA/`) |
|---|---|---|
| **Stickers de pessoas** (Gustavo, Lucian oficiais + convidados: Bonel, Guta, Layla, Lucas, Mafê, Phillip, Vitória) | `handoff-2026-09-30/shared-assets/stickers/` | `00_ASSETS E INSERTS/stickers e emojis refeitos/` (fonte do Gabriel) |
| Estados do Gustavo/Lucian (`still`, `hover-transicao` = sorriso, `hover-final` = surpresa, `arraste-final` = olhar de lado) | `opening/EP300_V4_MOTIONS/assets/personagens/`, `loop/assets/stickers/{gustavo,lucian}/` | `00_ASSETS E INSERTS/300-handoff-video/assets/personagens` |
| **Balde EP300** (A "EPISÓDIO 300" = oficial; B "Império" = alternativo) + pipocas soltas | `opening/EP300_V4_MOTIONS/assets/stickers/`, `loop/assets/stickers/{balde_pipoca_a_episodio300.png,pipocas/}` | `stickers e emojis refeitos/` (+ `caixa_de_pipoca_EP300_arquivos/` na raiz do episódio) |
| Outros stickers/gags: DeLorean, Marty+Doc ("Dupla futurista em sintonia"), extintor, microfone, viatura, Toddynho, Pica-Pau (silhueta original) | `opening/EP300_V4_MOTIONS/assets/stickers/`, `…/gags/`, `…/cena-sofa/` | idem |
| **Logos institucionais** (Métricas Boss, Purple Metrics, Onfly, Coffee++, Kinoplex, selo Analytics Talks, selo Episódio 300) | `loop/assets/{brand,sponsors}/`, `handoff-2026-09-30/shared-assets/logos/`, `opening/EP300_V4_MOTIONS/assets/{brand,sponsors}/` | `00_ASSETS E INSERTS/logos/`, `300-handoff-video/` |
| Logos de ferramentas (GA, GTM, BigQuery, Looker, Power BI, Amplitude, Ads, Meta, Hotjar, Search Console, Reportei…) | `handoff-2026-09-30/shared-assets/logos/ferramentas/` | simple-icons@13 (CC0; marcas dos donos) |
| Imagens/gráficos (frames históricos, EP1/EP126, ícones) | `handoff-2026-09-30/shared-assets/{images,graphics}/`, `opening/EP300_V4_MOTIONS/assets/hist/` | `00_ASSETS E INSERTS/V*_GERADOS`, arquivo histórico (ver CLAUDE.md do monorepo: busca dirigida em `00_ARQUIVO_HISTORICO`) |
| **Mosaico do Loop** (92 cartões / 60 imagens: thumbs oficiais EP260–289, prints do estúdio, EP126) | `loop/assets/mosaic/`, `loop/assets/thumbs/` | — (exclusivo do Loop) |
| Fontes | `loop/fonts/`, `opening/v2/fonts/`, `opening/EP300_V4_MOTIONS/assets/fonts/`, `handoff-2026-09-30/shared-assets/fonts_reference/` | Sora (títulos/números/adesivos, 800) + Inter (overlines, 700–800) — Google Fonts, OFL |
| Overlays ProRes 4444 alpha (44 da V2; R03) | **não incluídos** (3,5 GB+) | `V2_GERADOS/OVERLAYS`, `R03_LAYERS`, `R03_COMPONENTES_FINAIS_4K` |
| Câmeras brutas | **não incluídas** | `01_BRUTOS/` |
| Áudio | **não incluído** (licença) — ver [`AUDIO.md`](AUDIO.md) | ver AUDIO.md |

## Regras de uso (resumo)
- Logos institucionais: só os oficiais, proporção e área de segurança preservadas; **nunca viram sticker**; Kinoplex = branco oficial; Onfly = inteira (sem crop).
- Rostos-sticker não podem transmitir "susto" sem intenção; nenhum frame em que alguém esteja em pose ruim (R01/R03).
- Terceiros protegidos (Pica-Pau, GoT, Breaking Bad, De Volta para o Futuro): não usar a imagem — só solução original/indireta (silhueta, objeto, texto). O DeLorean e Marty+Doc são stickers feitos pelo Gabriel.
- Emojis (Segoe UI Emoji) não estão no repo. Bandeiras: 65 `.webp` oficiais vivem no repo privado do site (não acessado); as do vídeo foram desenhadas em `v2/extra.py`.
- Patrocinadores: naming/logos de Purple Metrics e Onfly foram tratados como **provisórios** até confirmação.
- Fonte histórica do podcast (frames/episódios antigos): consultar primeiro `…\Marketing Métricas Boss\00_ARQUIVO_HISTORICO\01_VIDEOS\02_PODCAST` com busca dirigida; EP1 = YouTube `4EPVBU7WgDg`.
