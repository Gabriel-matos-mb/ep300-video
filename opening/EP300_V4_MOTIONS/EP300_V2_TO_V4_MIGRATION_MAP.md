# EP300 — Mapa de migração V2 → V4 (forense da V2)

> 02/10/2026. **Somente análise**: nada foi renderizado, montado ou refeito; nenhum `.prproj` foi aberto para escrita; sem FFmpeg para remontar filme.
> Fontes: `timeline_v2.json` + `v2/plan.py` + `v2/build.py` (a V2 = `EP300_ABERTURA_V2_PROXY`), preflight V3 (`v3-preflight/decision_map.json` e `EP300_V3_PREFLIGHT.md`), sequência atual do Premiere (cópia lida), redlines do Gabriel, motions V4 já feitos.
> TC V2 = `MM:SS:FF` @ 30 fps na timeline do PROXY (370,77 s). TC novo = `HH:MM:SS:FF` @ 23,976 na sequência do Gabriel (5:15:13), estimado pela âncora de fala (±0,3 s).

> **Registro das 26 imagens/redlines do Gabriel: `EP300_CHAT_CLEAR_HANDOFF.md` §4 (cópias em `redlines_source/`).**
> **Atualização 03/10/2026:** decisões do Gabriel registradas em `EP300_DECISIONS_LOG.md` (8 casos resolvidos; H7/GRITEM/institucional/supercut LOCKED). `EXECUTION_READY = NO`.
> **PRE_EDITED_4K_SAFETY_MASTER** (`01_BRUTOS/NOVOS TAKES-REGRAVADO/VIDEO PRE EDITADO CINEMA EP 300 EM QUALIDADE MAXIMA.mp4`): referência consolidada da edição do Gabriel (abaixo do Premiere editável, acima de qualquer reconstrução); exportação em andamento, validação pendente.

## 0. Autoridades (hierarquia de EP300_NON_NEGOTIABLES.md)

| Nível | Autoridade | Fonte | Manda em | Status |
|---|---|---|---|---|
| 1 | **LOCKS / Decisões humanas** | Gabriel (explícitas) | o que não pode ser reinterpretado | LOCKED |
| 2 | **EDITORIAL E TÉCNICA** | Premiere atual do Gabriel (`ep 300 final.prproj`) | câmeras novas, multicam, cortes, enquadramento, timing editorial, cor, áudio, efeitos, trechos removidos, falas da nova gravação | EDITORIAL_TECHNICAL_AUTHORITY |
| 3 | **CRIATIVA** | `EP300_ABERTURA_V2_PROXY` | ritmo, dinâmica, densidade de intervenções, músicas, SFX, brincadeiras, inserts, overlays, telas cheias, textos, timing cômico, transições, variedade visual, sensação geral | CREATIVE_BASELINE_APPROVED |
| 4 | **IDENTIDADE VISUAL** | Handoff oficial EP300/site | paleta, tipografia, stickers, scrapbook, linguagem, comportamento gráfico | handoff visual oficial |
| 5 | **CAPTAÇÃO** | Nova gravação | qualidade, execução, falas atualizadas, brincadeiras regravadas, dados atualizados | source material |
| 6 | **EVOLUÇÃO VISUAL** | V4 motions / redlines aprovadas | melhora V2; **nunca** a substitui por algo mais vazio; só se aprovado | SELECTIVE_IMPROVEMENTS |
| 7 | **MAPA DE RECONCILIAÇÃO** | Este documento | recupera continuidade; não redefine a peça | RECOVERY_RECONCILIATION_MAP |

**Versões:**
- `EP300_V4_ASSEMBLY_REVIEW`: **REJECTED** — DO NOT USE AS BASELINE
- `EP300_V4_MOTIONS` + redlines: apenas 5 aprovadas (C00_01, C00_02, C03_08, C05_05, C06_03); os outros 10 aguardam revisão

**Regra de preservação:** a pergunta não é "existe na timeline nova?" e sim "funcionava na V2?". Se funcionava → PRESERVAR/ADAPTAR. Só sai se (1) a fala nova tornou impossível, (2) o Gabriel rejeitou, (3) há V4 claramente superior, (4) ficou factualmente incorreta.
Os **11 Disabled** continuam sendo só "a câmera some aqui"; **não limitam** overlays, inserts, accents nem stickers. A V2 usava 4 linguagens: **INSERT** (tela cheia), **OVERLAY** (motion sobre câmera), **ACCENT** (sticker/texto/número/linha/reação) e **SLOT** (câmera substituída).

### Premiere do Gabriel — INTOCÁVEL (não reproduzir externamente)

- 101 cortes na V1 · multicam verdadeiro (3 câmeras 4K sincronizadas na sequência aninhada: geral +0,000 s · Lucian +0,125 s · Gustavo −2,544 s) · duração 5:15:13 · 11 clipes desativados · P&B no último corte (`00:05:08:14 → 00:05:15:13`).
- **Enquadramento:** rotação **2,2°** (câmera geral) e escalas **112%** (geral), **107,7%** (Lucian), **122,1%** (Gustavo).
- **Cor (Lumetri por câmera):** temperatura **−8,2** · tonalidade **+1,3** · saturação 101.
- **Áudio:** **88 filtros/processamentos** nos 29 clipes de A1 (ganho, limitador, gate, compressor, expansor…) + reverb do blooper final (não localizado no XML pelo extrator — preservar do mesmo jeito).
- Escolha de câmera por corte, trechos removidos, sync, P&B final, blooper final (intencional, antes do looping), brincadeiras com a plateia mantidas.
- O futuro XML será uma **CAMADA ADICIONAL** (V2+, A2+) para colar na sequência dele — nunca uma reconstrução do Premiere. Quem exporta o filme é o Premiere.

### Casa visual do handoff/site (valendo para V2 e V4)

Fonte: `# Guia visual — EP 300 (handoff pro vídeo).txt` (Cláudio Miranda / página `/300`). Paleta: creme `#F7F4ED`, laranja `#F47340`, tinta `#121213`, branco; fundo pontilhado **3 px a cada 20 px**; **Sora 700–800** (números/títulos) e **Inter 400–500** (apoio); adesivo de texto = anel branco arredondado + sombra suave, rotação **−3°**; pill = borda 3 px de tinta + sombra sólida deslocada (`0.2rem 0.25rem 0`); rotações de adesivo do conjunto `−8°, 5°, −4°, 7°, −6°, 3°`; cena do sofá (6 quadros) e rostos "vivos" (still/hover/arraste).
**Desvios dos motions V4 já feitos em relação a esse guia (a corrigir quando se implementar):** pontilhado do Remotion usa 26 px/2,2 px (guia: 20 px/3 px); overlines em Inter 800 (guia: Inter 400–500 no apoio); sombra de pill/label dura e padronizada (ok para pill; texto-adesivo deve ter sombra suave); rotações fora do conjunto fixo em alguns elementos. **A recuperação da V2 não é voltar visualmente para trás:** V2 = estrutura/ritmo/função; V4 = execução atualizada e mais fiel ao handoff.

## 1. Resumo numérico

| Item | Valor |
|---|---|
| Overlays/inserts/accents da V2 | **44** (32 tela cheia · 12 sobre câmera/accents) |
| Outras intervenções visuais da V2 | 3 estruturais (pausa P_EVOL 2,4 s · congelamento GRITEM 3 s · íris da tela do 300) + 6 punch-ins de câmera (superseded pelo multicam do Gabriel) + 10 cortes editoriais (superseded) + 1 bleep + tratamento P&B/REC do cold open |
| **Total de intervenções visuais mapeadas** | **44 + 3 + 6 + 1 = 54** (+ 10 cortes editoriais registrados como autoridade do Gabriel) |
| Overlays: KEEP EXACTLY / KEEP + RETIME / ADAPT / MOVE / REPLACE_APPROVED / NEEDS_HUMAN_V4_REPLACEMENT / DROP_SCRIPT | **2 / 9 / 14 / 1 / 15 / 0 / 3 = 44** (atualizado 03/10 após decisões do Gabriel; DROP_SCRIPT = C01_02, C01_03, C04_02; C06_02 passou a MOVE por H7) |
| SFX: KEEP / RETIME / REPLACE / DROP | **11 / 58 / 0 / 5 = 74** |
| Trilhas | 3 (aviso · bed · final) |
| No assembly reprovado: presentes / parciais / ausentes (dos 44) | **7 / 9 / 28** (no assembly reprovado os 3 DROP_SCRIPT + C06_02/MOVE entram em ausentes) |

### Densidade (sensação de movimento contínuo)

| | V2 (proxy, 370,8 s) | V4 reprovado (sequência 315,9 s) |
|---|---|---|
| Câmera limpa | **15,7%** (maior trecho seguido 9,3 s; média 2,8 s; 21 trechos) | **~72%** (só 11 slots + 2 overlays = 87,7 s cobertos = 28%) |
| Overlay/accent sobre câmera | 10,5% | ~4% (O01+O02) |
| Tela cheia / insert | 73,8% | ~24% (só slots) |
| Música / SFX | 3 trilhas · 74 SFX · ducking | **nenhum** |
Meta de migração: **igualar ou superar a percepção de dinamismo da V2** (não é preencher 100% dos quadros: é nunca deixar a câmera limpa por mais de ~9 s).

## 2. Os 44 overlays — reconciliação completa

Decisões: **KEEP EXACTLY** (mesmo texto/duração, só muda a âncora) · **KEEP + RETIME** (mesma peça, duração/âncora mudam) · **ADAPT** (texto/dado/asset muda; peça V4 ainda não existe) · **REPLACE_APPROVED** (já existe composição V4 aprovada explicitamente por Gabriel que executa a função da V2) · **NEEDS_HUMAN_V4_REPLACEMENT** (V4 é candidato mas sem aprovação explícita; aguarda revisão) · **DROP_SCRIPT** (fala/beat não existe na nova gravação). "Presença" = estado no assembly reprovado.

| # | Cue · TC V2 · tipo | Fala V2 → fala nova | TC novo (cobertura na sequência) | Asset V2 → V4 | Função | DECISÃO · justificativa | Dependência / falta | Presença |
|---|---|---|---|---|---|---|---|---|
| 1 | **C00_00** · 00:00:00–00:11:23 · INSERT (arquivo REC, P&B) | "Fala aí… sejam bem-vindos" / "Começou mesmo?" / "Começa de novo…" + risada → "Tá no ar, tá valendo" → só "Começou mesmo? Começa de novo aqui." + risada (b0 4,15–6,50 s); SEM "tá no ar, tá valendo" | pré-sessão (fora da sequência) | COLD_B_2023_05_24 + COLD_B_VERDADES (clipes de arquivo) → — (clipe de arquivo existente) | erro → percepção → riso: rompimento curto e engraçado | **ADAPT** · Gabriel (msg 02/10): manter SÓ "começou? começa de novo" + risada; "tá no ar" e 2º erro fora; marcou "tirar esse take" no print (qual take exato = NEEDS_REVIEW) | posição no filme (suposição: depois da tela do 300); take exato do print riscado | parcial |
| 2 | **C00_01** · 00:11:23–00:15:02 · FULL SCREEN INSERT | contagem 3-2-1 de película (payoff do "tá valendo") → — (pré-sessão) | pré-sessão (fora da sequência) | C00_01_CONTAGEM_PRE_SESSAO.mov → P01-CONTAGEM (anel, ticks, numeral sticker) | a sessão vai começar | **REPLACE_APPROVED** · Gabriel: "visualmente amadora"; função e duração (2,9 s) mantidas | beeps de 1 kHz (ver SFX); sem o "tá valendo" como gancho → decidir o gancho | presente |
| 3 | **C00_03** · 00:14:20–00:46:02 · FULL SCREEN INSERT (5 páginas) | aviso de cinema: saídas / "eu acho" / levanta a mão / olha pro lado / celular / pipoca → idem (pré-sessão) | pré-sessão (fora da sequência) | C00_03_AVISO_ANTES_DA_SESSAO.mov → P02-AVISO + extintor.png + balde A + gustavo-hover-transicao | colocar a plateia dentro do cinema; interação com a sala | **REPLACE_APPROVED** · estrutura, ordem e jogo com a plateia da V2 INTEIROS; Gabriel: "vídeo final deve começar por aqui" + redlines (setas, maiúsculas, emoji sticker, Gustavo sorrindo, extintor, balde) | balde oficial (A × B?); pipocas soltas; música do aviso e 11 SFX (hoje ausentes) | presente |
| 4 | **C00_02** · 00:45:20–00:51:11 · FULL SCREEN INSERT + íris | selo EPISÓDIO 300 + patrocinadores → íris revela a câmera → — (pré-sessão) | pré-sessão (fora da sequência) | C00_02_TELA_EPISODIO_300.mov → P03-TELA-300 + logo Kinoplex branca original | virada cinema → Analytics Talks | **REPLACE_APPROVED** · Gabriel redlines: tirar rostos repetidos, centralizar, estrutura da tela final, MB realização + Kino apoiador | íris de 0,8 s para a câmera (V2) ainda não refeita | presente |
| 5 | **C01_01** · 00:56:12–00:58:06 · ACCENT / STICKER (overlay) | "episódio especial de número 300" → adesivo 300 + confete → "Tá no ar, tá valendo o episódio 300 do Analytics Talks" (46,3–50,1) | 00:00:04:03 (100% da fala está na sequência) | C01_01_ADESIVO_300_CONFETE.mov → — | celebrar o 300 logo na abertura | **KEEP + RETIME** · funcionava; só re-ancora em "…episódio 300" | confete exige alfa (existe o .mov V2) | AUSENTE |
| 6 | **C01_02** · 01:06:07–01:16:05 · FULL SCREEN INSERT | "já falamos 11.526 vezes… acho" → — (removido do roteiro e da fala) | — | C01_02_DADOS_11526_TELA_CHEIA.mov → — | dados × "acho" | **DROP_SCRIPT** · fala não existe na nova gravação | — | AUSENTE |
| 7 | **C01_03** · 01:15:23–01:23:15 · FULL SCREEN INSERT | "494 vezes de diferença" (placar dados × acho) → — (removido) | — | C01_03_PLACAR_DADOS_X_ACHO.mov → — | dados × "acho" | **DROP_SCRIPT** · fala não existe na nova gravação (piada do "acho" sobrevive no aviso de cinema) | — | AUSENTE |
| 8 | **C02_01** · 01:26:22–01:38:10 · FULL SCREEN INSERT (linha do tempo) | 2015 → Prime → MB Talks → "a volta do Lucian" → podcast + polaroid EP1 → "Começamos lá em 2015… MB Talks… quando eu voltei a gravar… cenário antigo" (50,2–78,3) | 00:00:08:01 (100% da fala está na sequência) | C02_01_HISTORIA_LINHA_DO_TEMPO.mov → S01-A-VOLTA (proposição não verificada) | origem do programa | **REPLACE_APPROVED · HÍBRIDO V2+V4** · decisão Gabriel 03/10: preservar a construção V2 (2015 → Prime → MB Talks, ~5,6 s) + cauda V4 (volta do Lucian → cenário antigo); polaroid/take EP1 rejeitada NÃO volta | início da história (2015/PRIME/MB TALKS, tl ≈ 0:10–0:26) sem insert; nova imagem de cenário antigo (opcional) | parcial |
| 9 | **C02_02** · 01:40:19–01:43:28 · OVERLAY (chuva de perguntas) | "são mais de 300 perguntas" → "300 episódios são mais de 300 [fucking] perguntas" (78,5–84,8) | 00:00:36:07 (90% da fala está na sequência) | C02_02_CHUVA_DE_PERGUNTAS.mov → — | microgag sobre câmera aberta | **KEEP + RETIME** · funcionava; fala ficou 6 s (V2 3,3 s) | H7 (palavrão no mesmo ponto) | AUSENTE |
| 10 | **C02_03** · 01:44:16–01:50:03 · FULL SCREEN INSERT (evolução) + pausa | "E a pergunta foi mudando" — 6 épocas em polaroids + 2,4 s sem voz → "E a pergunta foi mudando" (84,8–86,9) | 00:00:41:23 (100% da fala está na sequência) | C02_03_EVOLUCAO_DO_PROGRAMA.mov → — | mostrar quanto o programa mudou | **ADAPT** · Gabriel pediu trocar 4 prints (EP1, EP100, EP210, EP153); a pausa de 2,4 s não existe na timeline | 4 frames novos do acervo; decisão: abrir pausa/hold na timeline | AUSENTE |
| 11 | **C03_01** · 01:49:21–02:02:21 · FULL SCREEN INSERT (logos) | "no começo, quase tudo era ferramenta" + 12 logos em tiles → "…quase tudo era sobre ferramenta. Como instalar, taguear, número não bate" (86,9–96,6) | 00:00:44:02 (100% da fala está na sequência) | C03_01_ECOSSISTEMA_DE_FERRAMENTAS.mov → — | ecossistema de ferramentas → "ATÉ HOJE" | **ADAPT** · Gabriel: logo da Reportei fora do padrão dos tiles; fala 9,7 s (V2 12,6 s) | ícone da Reportei (só há wordmark) | AUSENTE |
| 12 | **C03_02** · 02:02:09–02:09:03 · FULL SCREEN INSERT (chave ON/OFF) | "o Google desligou o Universal" → "…chegou o Sunset do Google Analytics Universo" (take 139,1–143,1) | 00:00:55:01 (97% da fala está na sequência) | C03_02_UNIVERSAL_ON_OFF.mov → — | UA desligou | **KEEP + RETIME** · funcionava; 4 s de fala (V2 6,4 s) | — | AUSENTE |
| 13 | **C03_03** · 02:08:21–02:16:19 · FULL SCREEN INSERT | "153 episódios… 4 em cada 10 GA4" → idem (147,6–153,4) | 00:00:58:23 (100% da fala está na sequência) | C03_03_CONTADOR_153_GRADE_4_DE_10.mov → S02 (cadeia S02S03) (proposição não verificada) | escala do GA4 em 2023 | **REPLACE_APPROVED (V4)** · decisão Gabriel 03/10: V4 retimado (mesmo desenho/função) | — | presente |
| 14 | **C03_04** · 02:16:07–02:19:22 · FULL SCREEN INSERT / STICKER | "de nada, Vitória" (corações nos olhos) → "De nada, Vitória" (159,7–161,6) — agora DEPOIS do GA4 | 00:01:11:01 (100% da fala está na sequência) | C03_04_DE_NADA_VITORIA.mov + sticker Vitória → — | piada interna (graça visual) | **KEEP + RETIME** · piada gravada de novo; ordem trocada; fala 1,9 s (V2 3,1 s) | — | AUSENTE |
| 15 | **C03_05** · 02:19:10–02:27:16 · FULL SCREEN INSERT | "GA4 nunca saiu da pauta — 1 a cada 3" → "…até hoje tá em 3 a cada 10" (153,4–159,7) | 00:01:04:18 (100% da fala está na sequência) | C03_05_GA4_1_DE_3.mov → S03 (cadeia S02S03) (proposição não verificada) | GA4 permanece | **REPLACE_APPROVED (V4)** · decisão Gabriel 03/10: V4 com dado atualizado (3 em cada 10); dado antigo não volta | — | presente |
| 16 | **C03_06** · 02:29:10–02:33:04 · OVERLAY | "é um tema que eu gosto pouco" (IA) → "um assunto que eu gosto bastante" (165,6–169,2) | — | C03_06_GOSTA_POUCO_IA.mov → — (asset de referência; linguagem anterior preserva) | humor sobre IA | **ADAPT** · fala mudou de sentido; preservar a função/linguagem anterior como baseline (V2 = estrutura/ritmo/função); nova solução criativa = NEEDS_HUMAN_DECISION | — | AUSENTE |
| 17 | **C03_07** · 02:33:01–02:47:11 · FULL SCREEN INSERT (linha do tempo IA) | IA até 2021 → 1 a cada 4 → atribuição/incrementalidade → BigQuery → marketing → IA metade · atribuição e incrementalidade · 4 em 10 · BigQuery (198,4–226,0) | 00:01:16:08 (96% da fala está na sequência) | C03_07_IA_LINHA_DO_TEMPO.mov → S04-ATRIB-INCREM (proposição não verificada) | o que entrou do lado do GA4 | **REPLACE_APPROVED (V4 + COMPLEMENTO)** · decisão Gabriel 03/10: V4 para atribuição/incrementalidade + preservar/adaptar a função audiovisual de "IA METADE" e "BigQuery → MARKETING" (não precisa copiar a execução antiga) | IA "METADE" e BigQuery→MARKETING em câmera ativa ainda sem insert | parcial |
| 18 | **C03_08** · 02:47:07–02:54:19 · FULL SCREEN INSERT | "taguear um botão → confiar no modelo" → idem (226,0–231,9) | 00:01:42:18 (100% da fala está na sequência) | C03_08_BOTAO_VIRA_MODELO.mov → S05-BOTAO-MODELO | virada: ferramenta → modelo | **REPLACE_APPROVED** · Gabriel redline: "modelo." em sticker; mesmo desenho, retimado (S05) | — | presente |
| 19 | **C04_01** · 03:03:28–03:09:12 · FULL SCREEN INSERT (prints + contador) | "203 vezes… fala aí, analítica" → "Mais de 200 vezes que eu falei [bordão não falado]" (235,7–237,6) | 00:01:52:10 (100% da fala está na sequência) | C04_01_BORDAO_203_PRINTS.mov → (supercut 158 cortes, 16:43, existe — não inspecionado) | bordão repetido | **ADAPT** · DADO MUDOU (+200); Gabriel: mais prints, cenários diferentes, reações boas, evitar EP288 | frames novos do acervo; decisão supercut × prints | AUSENTE |
| 20 | **C04_02** · 03:09:22–03:13:10 · OVERLAY (tarja + punch-in) | "qual foi o episódio que nasceu? — nem eu" → — (não falado) | — | C04_02_EPISODIO_DE_ORIGEM.mov → — | microgag | **DROP_SCRIPT** · fala não existe na nova gravação | — | AUSENTE |
| 21 | **C04_03** · 03:14:16–03:21:19 · FULL SCREEN INSERT | "16 maneiras de me apresentar" (balão, 4 apelidos) → "mais de 60 maneiras diferentes de me apresentar" (253,8–257,5) | 00:01:56:07 (98% da fala está na sequência) | C04_03_APELIDOS_16.mov → — | brincadeira do Lucian | **ADAPT** · DADO MUDOU (60+); Gabriel: trocar o rosto lateral do Lucian se a tela ficar | rosto Lucian sorrindo (existe `still`) | AUSENTE |
| 22 | **C04_04** · 03:21:07–03:23:25 · FULL SCREEN INSERT | "diamante negro é oficial" → idem (258,1–259,5) | 00:01:59:22 (100% da fala está na sequência) | C04_04_DIAMANTE_NEGRO_OFICIAL.mov → — | carinho/brincadeira | **KEEP + RETIME** · funcionava; fala 1,4 s (V2 2,6 s) | — | AUSENTE |
| 23 | **C04_05** · 03:24:07–03:27:11 · OVERLAY + câmera congelada (HOLD 3 s) | "Grita aí se vocês concordam" — 4ª parede, escurece, placa GRITEM → idem + "Pelo amor de Deus" (259,5–263,0) | 00:02:01:08 (106% da fala está na sequência) | C04_05_GRITEM_SE_CONCORDAM.mov + freeze → — | interação direta com a plateia | **KEEP + RETIME** · brincadeira com a plateia: Gabriel mandou MANTER; exige freeze/respiro de 3 s na timeline | decisão do Gabriel: freeze 3 s no Premiere; música +10 dB nesse respiro | AUSENTE |
| 24 | **C04_06** · 03:28:02–03:39:04 · FULL SCREEN INSERT | "24 vezes… se o Pica-Pau tivesse chamado a polícia" → passada LONGA do Gabriel (289,7–304,0): "…e o problema continua… ninguém sabe essa referência" | 00:02:05:08 (99% da fala está na sequência) | C04_06_PICA_PAU_24_TELA_CHEIA.mov → — | frase clássica do Lucian | **ADAPT** · versão longa casa com o pill "tem gente que nem sabe a referência"; Gabriel: novo sticker do Pica-Pau | sticker novo do Pica-Pau (Gabriel fornece) | AUSENTE |
| 25 | **C05_01** · 03:38:22–03:50:27 · FULL SCREEN INSERT (mural) | "191 pessoas… 348 vezes… 140 empresas" → "quase 200 pessoas… quase 350 vezes… mais de 140 empresas" (316,7–322,4) | 00:02:19:13 (99% da fala está na sequência) | C05_01_MESA_191_348_140_MURAL.mov → — | escala de convidados | **ADAPT** · DADOS MUDARAM; Gabriel: mais stickers/prints (sensação de multidão, não ranking); EP187 BANIDO | mais stickers (existem Guta, Lucas, Vitória, Layla…) e frames | AUSENTE |
| 26 | **C05_02** · 03:50:15–03:57:11 · FULL SCREEN INSERT | "banco, varejo, mídia, telecom e até o Google… parceiro do Google?" → idem (335,9–346,0) | 00:02:25:05 (87% da fala está na sequência) | C05_02_SETORES_E_GOOGLE.mov → S06-SETORES (proposição não verificada) | empresas que passaram | **REPLACE_APPROVED (V4 + COMPLEMENTO)** · decisão Gabriel 03/10: V4 para os setores + preservar a punchline "PARCEIRO DO GOOGLE? / AINDA NÃO" com intervenção (não volta seca para câmera) | parte Google + "PARCEIRO DO GOOGLE?/AINDA NÃO" (câmera ativa) | parcial |
| 27 | **C05_03** · 03:56:29–03:59:08 · FULL SCREEN INSERT (stickers chorando) | "Eu queria. / Também queria." → um só "Queria." (344,7–346,0) | 00:02:32:17 (100% da fala está na sequência) | C05_03_EU_QUERIA_CHORANDO.mov → — | piada do Google | **ADAPT** · um só locutor falou; manter 1 sticker (quem falou = NEEDS_REVIEW) | quem falou (diarização falhou) | AUSENTE |
| 28 | **C05_04** · 03:58:26–04:05:14 · FULL SCREEN INSERT (polaroids EP126 + viatura) | "nós chamamos… gravamos com a PM do RJ" → idem (346,0–354,9) | 00:02:34:00 (96% da fala está na sequência) | C05_04_PICA_PAU_PM_RJ_EP126.mov + viatura → — | payoff do Pica-Pau | **ADAPT** · Gabriel: "tentar trocar esse frame dele" (convidado EP126) | frame novo do EP126 | AUSENTE |
| 29 | **C05_05** · 04:07:07–04:28:01 · FULL SCREEN INSERT (ficha de presença) | Phill 29×, Mafê 24× (EP1), Bonel 7× → idem (355,8–376,9) | 00:02:43:10 (100% da fala está na sequência) | C05_05_FICHA_DE_PRESENCA_FOTOS.mov → S07 + S08 | convidados recordistas | **REPLACE_APPROVED** · Gabriel redline: "trocar a frase para já paga até boleto"; S07/S08 aprovados; polaroid EP1 trocada | — | presente |
| 30 | **C06_01** · 04:32:19–04:33:22 · ACCENT (slap sobre câmera aberta) | "de vez em quando você acerta antes" → idem (389,3–393,6) | 00:03:04:12 (100% da fala está na sequência) | C06_01_ACERTA_ANTES.mov → — | tese do bloco | **KEEP EXACTLY** · mesmo texto e duração (1,1 s); só muda a âncora | — | AUSENTE |
| 31 | **C06_02** · 04:34:01–04:35:09 · ACCENT (bleep + 🙊) | bleep do palavrão do Lucian → — (sem palavrão equivalente) | — | C06_02_BLEEP.mov + SFX_BLEEP_1kHz → — (SFX_BLEEP_1kHz.wav mantido) | gag | **MOVE** · H7 LOCKED 03/10: "fucking" será CENSURADO e a censura é a gag da V2 (tom divertido, timing cômico, bleep/SFX, reação 🙊/audiovisual): remapear semanticamente para o "fucking" da nova gravação (80,9 s ≈ 00:00:38:17 est. ±0,3 s, dentro de C02_02); não cortar a fala; não usar beep genérico | H7 | AUSENTE |
| 32 | **C06_03** · 04:35:09–04:50:05 · FULL SCREEN INSERT (linha do tempo) | fev/22 todinho + 27 dias; "desculpa, Vi."; out/24 MMM → idem (393,6–411,9) | 00:03:08:19 (100% da fala está na sequência) | C06_03_DATAS_FEV22_OUT24.mov → S09 + toddynho.png | a gente chegou antes | **REPLACE_APPROVED** · Gabriel redline: "o certo é Toddynho"; S09 aprovado; Toddynho com asset oficial | "desculpa, Vi." (sticker Vitória) e out/24 MMM em câmera ativa | parcial |
| 33 | **C06_04** · 04:50:04–04:53:16 · OVERLAY (stickers Guta/Lucas) | "olha aí, de nada, viu? Purple Metrics do Guta" → "De nada, [por favor/Purple?]. Também prevendo, né?" (412,4–414,2) | 00:03:27:02 (97% da fala está na sequência) | C06_04_DE_NADA_PURPLE.mov + stickers Guta/Lucas → — | agradecer o patrocinador | **ADAPT** · default é preservar: depende de OUVIR 2 s (H3). O Gabriel manteve a linha na timeline | H3 (ouvir 412,3–413,6 s) | AUSENTE |
| 34 | **C06_05** · 04:53:16–05:07:08 · FULL SCREEN INSERT (linha do tempo) | +3 meses Meridian; MCP abr/25 → jul/25; "viu, Layla?"; dez/24 → idem sem Layla (414,2–426,6) | 00:03:28:20 (100% da fala está na sequência) | C06_05_DATAS_MERIDIAN_MCP_DEZ24.mov → S10-MERIDIAN-MCP | a gente chegou antes | **REPLACE_APPROVED** · Gabriel redlines; S10 aprovado; "viu, Layla?" não foi falado (DROP_SCRIPT) | dez/24 em câmera ativa | parcial |
| 35 | **C06_06** · 05:07:14–05:10:14 · ACCENT (pill) | "meia-culpa" → "na verdade eu não disse nada. Quem disse foi o Gustavo, mas…" (443,7–449,0) | 00:03:46:19 (100% da fala está na sequência) | C06_06_MEIA_CULPA.mov → — | brincadeira de autoria | **ADAPT** · a piada mudou de forma (autoria dez/24); quem fala cada frase = NEEDS_REVIEW | H10 (gag opcional) | AUSENTE |
| 36 | **C06_07** · 05:10:19–05:18:19 · FULL SCREEN INSERT | fev/26 IA na home · jun/26 · "impossível" · ACERTOU → "o que eu falei que não dava pra fazer, eu fui lá e fiz" · Copilot em junho (456,6–464,6) | 00:03:59:16 (100% da fala está na sequência) | C06_07_DATAS_FEV26_JUN26_ACERTOU.mov → — | virada: acertou de novo | **ADAPT** · "IMPOSSÍVEL" → "não dava pra fazer"; "IA NA HOME DO GA" não falado (H4) | H4 | AUSENTE |
| 37 | **C07_01** · 05:20:29–05:22:08 · ACCENT (slap "vocês.") | "do outro lado da pergunta: vocês" → idem (491,1–497,9) | 00:04:07:18 (100% da fala está na sequência) | C07_01_VOCES_PLATEIA.mov → — | 4ª parede com a plateia | **KEEP + RETIME** · interação com a plateia (manter); só re-ancora | — | AUSENTE |
| 38 | **C07_02** · 05:22:04–05:28:23 · FULL SCREEN INSERT | "700 mil vezes… 106 mil horas" → "700 mil… mais de 100 mil horas" (494,2–502,8) | 00:04:10:20 (100% da fala está na sequência) | C07_02_OUVIDAS_700_MIL.mov → S11-700-MIL (proposição não verificada) | escala de audiência | **REPLACE_APPROVED (V4 + COMPLEMENTO)** · decisão Gabriel 03/10: V4 para "700 MIL" + intervenção para "100+ MIL HORAS" (segundo número também ganha peso visual) | "100+ mil h" em câmera ativa | parcial |
| 39 | **C07_03** · 05:28:11–05:35:16 · FULL SCREEN INSERT (sofá + ano correndo) | "terminaria em 2038" — cena do sofá, 2026→2038, "de volta para o futuro ⚡ 🚗" → "…tu só vai parar de escutar a Analytics Talks em 2038" (502,7–510,6) | 00:04:19:08 (100% da fala está na sequência) | C07_03_DE_VOLTA_PARA_2038.mov (cena-sofá do site) → O02-2038-VIAGEM + O01 (setup) (proposição não verificada) | escala absurda de tempo | **REPLACE_APPROVED · HÍBRIDO** · decisão Gabriel 03/10: setup ("voltando no tempo") e payoff (2038) do V4 com DeLorean + Marty/Doc + cena do sofá/site recuperada no payoff de 2038; não sobrecarregar os dois momentos | — | parcial |
| 40 | **C07_04** · 05:35:04–05:36:22 · FULL SCREEN INSERT (bandeiras) | "em 110 países" — 16 bandeiras quadradas → "em mais de 100 países" (510,6–512,6) | 00:04:27:05 (100% da fala está na sequência) | C07_04_PAISES_110_BANDEIRAS.mov → — | escala geográfica | **ADAPT** · DADO MUDOU (+100); Gabriel: colocar mais bandeiras | mais bandeiras (só 16 desenhadas) | AUSENTE |
| 41 | **C07_05** · 05:39:29–05:43:27 · FULL SCREEN INSERT | "o episódio mais ouvido é o 197" → idem + "no Spotify" (516,7–527,6) | 00:04:33:07 (100% da fala está na sequência) | C07_05_EP_197.mov → — | surpresa: era sobre gente | **KEEP + RETIME** · funcionava; fala 10,9 s (V2 4 s) | — | AUSENTE |
| 42 | **C07_06** · 05:47:29–05:49:20 · ACCENT (slap "gente.") | "…era sobre gente." → idem (527,6–531,8) | 00:04:44:05 (100% da fala está na sequência) | C07_06_GENTE.mov → — | payoff | **KEEP EXACTLY** · mesmo texto, 1,7 s; só muda a âncora | — | AUSENTE |
| 43 | **C08_01** · 05:58:05–06:02:05 · FULL SCREEN INSERT (título) | título do episódio, depois de um respiro → "Qual o futuro da mensuração?" → "…um episódio pra pôr tudo" (592–607) | depois do fecho (após 00:05:15:13) | C08_01_TITULO_EPISODIO.mov → — | título do episódio | **KEEP + RETIME** · funcionava (aprovado); falta definir onde cai (sequência termina em P&B) | posição do título/transição para o looping | AUSENTE |
| 44 | **C09_01** · 06:01:23–06:10:23 · FULL SCREEN INSERT (300 → loop) | 300 conta, estoura (confete), vocês estão aqui, comemoram, vira o lockup do LOOP → — (depois do fecho / blooper P&B) | depois do fecho (após 00:05:15:13) | C09_01_FINAL_300_E_LOOPING.mov → F01-FINAL-300 (logos + Kinoplex) (proposição não verificada) | celebrar o 300 e entrar no looping | **REPLACE_APPROVED (V4 + AJUSTE)** · decisão Gabriel 03/10: "vocês estão aqui e contando" segue REJEITADA; direção de texto "300 episódios, 300 perguntas… / e a de hoje começa agora."; celebração do 300, sem tom de encerramento corporativo; relação com blooper final → loop validada no Premiere | texto final (3 propostas); transição para o looping (projeto próprio) | parcial |

## 2B. Os 8 casos NEEDS_HUMAN_V4_REPLACEMENT — **RESOLVIDOS em 03/10** (ver `EP300_DECISIONS_LOG.md` §1; texto abaixo = histórico da apresentação V2 × V4)

Estes casos têm proposta V4 mas sem aprovação explícita. Cada um está documentado abaixo. **Nenhuma solução foi implementada**; apenas mapeadas as proposições.

---

### C02_01 — HISTÓRIA E VOLTA DO LUCIAN (slot S01)

| Aspecto | V2 (baseline) | V4 (proposição) |
|---|---|---|
| **Conteúdo** | 2015 → Prime → MB Talks → "a volta do Lucian" → podcast + polaroid EP1 | idem (mesmo arc narrativo) |
| **Duração V2** | 11,8 s | — |
| **Duração nova (est.)** | — | S01 = 6,2 s (slot) |
| **Asset V2** | `C02_01_HISTORIA_LINHA_DO_TEMPO.mov` | — |
| **Função** | origem do programa; contexto da volta | idem |
| **V4 proposto** | S01 com timeline refazida (cadeia de 6,2 s); polaroid EP1 removida | — |
| **O que seria perdido** | duração longa (11,8 s) para contextualizar 2015 e a volta; conteúdo visual da timeline V2 | — |
| **O que V4 acrescenta** | execução atualizada, timing mais curto; possibilidade de redline posterior | — |
| **Conflito com NON_NEGOTIABLES** | Nenhum identificado, mas: a redução de duração de 11,8 s para 6,2 s é material; "a volta do Lucian" é baseline criativa (nível 3) | — |
| **Proposta** | S01 é candidato válido; revisão humana recomendada (timing, cobertura da narrativa no slot vs timeline) | — |

**Falta:** revisão do timing/conteúdo de S01 vs C02_01 original.

---

### C03_07 — IA (LINHA DO TEMPO, slot S04)

| Aspecto | V2 (baseline) | V4 (proposição) |
|---|---|---|
| **Conteúdo** | IA até 2021 → 1 a cada 4 → atribuição/incrementalidade → BigQuery → marketing | idem (estrutura mantida) |
| **Duração V2** | 13,8 s | — |
| **Duração nova (est.)** | — | S04 = 9,7 s (slot) |
| **Asset V2** | `C03_07_IA_LINHA_DO_TEMPO.mov` | — |
| **Função** | mostrar a evolução do GA4 com IA como camada | idem |
| **V4 proposto** | S04 com pills refaitos (1/4 → metade, 4/10); timing mais curto | — |
| **O que seria perdido** | estrutura visual de timeline V2; duração para leitura (13,8 s → 9,7 s) | — |
| **O que V4 acrescenta** | atualizações de dados (1/4 → metade); design refreshed; mas timing reduzido | — |
| **Conflito com NON_NEGOTIABLES** | Sim: dados são autoridade de Gabriel (nível 2), mas timeline é baseline criativa (nível 3); redução de 4 s é material | — |
| **Proposta** | S04 é candidato, mas requer verificação: o timing mais curto preserva leitura/compreensão? | — |

**Falta:** revisão do timing de S04 vs impacto narrativo; "IA METADE" e "BigQuery→MARKETING" já cobertos em câmera ativa (remanesce).

---

### C07_03 — 2038 / DE VOLTA PARA O FUTURO (O01 setup + O02 payoff)

| Aspecto | V2 (baseline) | V4 (proposição) |
|---|---|---|
| **Conteúdo** | "terminaria em 2038"; cena sofá; 2026→2038; "de volta para o futuro ⚡ 🚗" | "tu só vai parar… em 2038"; DeLorean; Marty+Doc; eixo AGORA→2038 |
| **Duração V2** | 7,1 s | — |
| **Duração nova (est.)** | — | O01 (setup) + O02 (payoff) = ?** (não medido) |
| **Asset V2** | `C07_03_DE_VOLTA_PARA_2038.mov` (cena-sofá + ano correndo) | — |
| **Função** | escala absurda de tempo; payoff da referência | idem |
| **V4 proposto** | O01 (setup "voltando no tempo") + O02 (payoff "agora→2038") com stickers oficiais DeLorean + Marty+Doc | — |
| **O que seria perdido** | cena sofá do site (asset oficial); estrutura V2 da timeline 2026→2038 | — |
| **O que V4 acrescenta** | stickers oficiais (DeLorean, Marty+Doc); executada com autoridade visual; separação setup/payoff; camadas separáveis | — |
| **Conflito com NON_NEGOTIABLES** | Nenhum se a cena sofá for recuperada; mas DECIDIR: ela volta como parte do beat? (ainda não respondido) | — |
| **Proposta** | O01+O02 são tecnicamente sólidos; decisão: mantém-se cena-sofá do site como parte da peça? | — |

**Falta:** aprovação do uso da cena sofá; confirmação de timing dos compostos O01/O02.

---

### C09_01 — FINAL 300 (F01-FINAL-300 + transição)

| Aspecto | V2 (baseline) | V4 (proposição) |
|---|---|---|
| **Conteúdo** | 300 conta, confete, plateia comemora, vira lockup do LOOP | 300 sobe, logos + Kinoplex, text temático |
| **Duração V2** | 9,1 s | — |
| **Duração nova (est.)** | — | F01 = ?** (não medido) |
| **Asset V2** | `C09_01_FINAL_300_E_LOOPING.mov` | — |
| **Função** | celebração final; transição para looping | idem |
| **V4 proposto** | F01 com 300 sobe, logos MB realização + Kinoplex apoiador, texto = prop (3 opções) | — |
| **O que seria perdido** | estrutura visual "celebração da plateia"; estética de final V2 | — |
| **O que V4 acrescenta** | separação limpa de funções (celebração → números/logos → abertura do loop); texto temático (flexível via prop) | — |
| **Conflito com NON_NEGOTIABLES** | Sim: Gabriel disse "vocês estão aqui e contando" sem sentido (rejeição); reestrutura F01 precisa de aprovação explícita do texto (3 propostas) | — |
| **Proposta** | F01 é tecnicamente pronto; mas escolher texto final entre 3 opções requer sua revisão | — |

**Falta:** escolha do texto final; posição de F01 na sequência (após blooper? antes do loop?); transição para looping.

---

## 3. Outras intervenções da V2 (não são overlay)

| Intervenção | TC V2 | O que fazia | Decisão | Justificativa / dependência |
|---|---|---|---|---|
| **P_EVOL** pausa sem voz 2,4 s | 01:47:09–01:49:21 | silêncio para a sala ler a evolução do programa | **ADAPT** | não existe pausa na timeline do Gabriel (corte 14 só tem 0,63 s de intervalo). Decisão dele: abrir pausa/hold ou deixar o insert correr sobre a fala |
| **HOLD** congelamento (GRITEM) | 03:24:11–03:27:11 | para a imagem, escurece, placa GRITEM; música +10 dB | **KEEP + RETIME** · **LOCKED 03/10: freeze ~2–3 s** | brincadeira com a plateia; não encurtar por ritmo; freeze no Premiere em `00:02:00:01` aprox. |
| **Íris** da tela do 300 para a câmera | 00:45:20–00:51:11 | revelar a sessão (0,8 s) | **KEEP + RETIME** | transição de pré-sessão → câmera; ainda não refeita no V4 |
| **Punch-ins** WG/WL (6 planos 1,6×) e reenquadramentos | planos da V2 | reação/brincadeira via recorte da geral | **DROP** | autoridade editorial do Gabriel: multicam, escalas 112/107,7/122,1% e escolha de câmera |
| **10 cortes editoriais** da V2 | ver `cortes_editoriais` | tirar travadas/retomadas | **DROP** | nova gravação, nova edição do Gabriel |
| **Bleep** 1 kHz (1,27 s) | 04:34:01 | palavrão do Lucian | **MOVE** (H7 LOCKED 03/10) | censura divertida remapeada para o "fucking" (80,9 s); asset `SFX_BLEEP_1kHz.wav` (GAG_SPECIFIC_SFX / FUCKING_CENSORSHIP, fora dos 74) + 🙊 da V2 como baseline da gag |
| Cold open P&B + grão + REC | 00:00–00:11:23 | arquivo de bastidor | **ADAPT** | ver C00_00; tratamento P&B/REC mantido |

## 4. Os 74 SFX

Biblioteca Motion Array da MB + sintéticos (R$ 0). Mix V2: ganhos por tipo (click −14 · whoosh −21 · impact −24 · tvoff −17 · wrong −15 · ding −21 · tick −21 · woosh_boom −21 · thump −20 · pop −19 · party −17 · tickup −20 · rise −23 dB), low-pass 7 kHz e **ducking −12 dB sob a voz**. **KEEP** = o som mantém o mesmo offset dentro da peça (acompanha a âncora); **RETIME** = a peça mudou e o som precisa seguir o novo momento do elemento; **DROP** = o elemento saiu; **REPLACE** = nenhum (não criei nem troquei samples).

| # | Cue | Arquivo | Existe no Drive | TC V2 | Pontuava | TC novo (est.) | Decisão |
|---|---|---|---|---|---|---|---|
| 1 | C00_01 | `SFX_LEADER_BEEP_1kHz.wav` | sim | 00:11:23 | contagem 3-2-1 | pré-sessão +0.00s | **RETIME** |
| 2 | C00_01 | `SFX_LEADER_BEEP_1kHz.wav` | sim | 00:12:22 | contagem 3-2-1 | pré-sessão +0.95s | **RETIME** |
| 3 | C00_01 | `SFX_LEADER_BEEP_1kHz.wav` | sim | 00:13:20 | contagem 3-2-1 | pré-sessão +1.90s | **RETIME** |
| 4 | C00_03 | `SFX_SYN_thump.wav` | sim | 00:15:11 | selo/carimbo/impacto | pré-sessão +0.70s | **RETIME** |
| 5 | C00_03 | `SFX_SYN_pop.wav` | sim | 00:19:02 | entrada de elemento | pré-sessão +4.40s | **RETIME** |
| 6 | C00_03 | `SFX_SYN_pop.wav` | sim | 00:22:11 | entrada de elemento | pré-sessão +7.70s | **RETIME** |
| 7 | C00_03 | `SFX_SYN_pop.wav` | sim | 00:23:11 | entrada de elemento | pré-sessão +8.70s | **RETIME** |
| 8 | C00_03 | `SFX_SYN_pop.wav` | sim | 00:27:17 | entrada de elemento | pré-sessão +12.90s | **RETIME** |
| 9 | C00_03 | `SFX_SYN_pop.wav` | sim | 00:29:20 | entrada de elemento | pré-sessão +15.00s | **RETIME** |
| 10 | C00_03 | `SFX_SYN_pop.wav` | sim | 00:32:23 | entrada de elemento | pré-sessão +18.10s | **RETIME** |
| 11 | C00_03 | `SFX_SYN_pop.wav` | sim | 00:34:20 | entrada de elemento | pré-sessão +20.00s | **RETIME** |
| 12 | C00_03 | `SFX_SYN_pop.wav` | sim | 00:38:11 | entrada de elemento | pré-sessão +23.70s | **RETIME** |
| 13 | C00_03 | `SFX_SYN_pop.wav` | sim | 00:39:29 | entrada de elemento | pré-sessão +25.30s | **RETIME** |
| 14 | C00_03 | `SFX_SYN_pop.wav` | sim | 00:41:05 | entrada de elemento | pré-sessão +26.50s | **RETIME** |
| 15 | C00_02 | `SFX_SYN_pop.wav` | sim | 00:45:23 | entrada de elemento | pré-sessão +0.10s | **RETIME** |
| 16 | C00_02 | `MA_Amenteramco_Whoosh_Pass-By_1.wav` | sim | 00:50:08 | passagem/entrada de tela | pré-sessão +4.60s | **RETIME** |
| 17 | C01_01 | `SFX_SYN_party.wav` | sim | 00:56:12 | estouro do 300 | 00:00:04:03 | **KEEP** |
| 18 | C01_02 | `SFX_SYN_tickup1.0.wav` | sim | 01:08:01 | contador subindo | — (cue DROP) | **DROP** |
| 19 | C01_03 | `SFX_SYN_tickup1.1.wav` | sim | 01:16:02 | contador subindo | — (cue DROP) | **DROP** |
| 20 | C01_03 | `SFX_SYN_thump.wav` | sim | 01:16:29 | selo/carimbo/impacto | — (cue DROP) | **DROP** |
| 21 | C02_01 | `SFX_SYN_thump.wav` | sim | 01:27:10 | selo/carimbo/impacto | 00:00:08:15 | **RETIME** |
| 22 | C02_01 | `SFX_SYN_pop.wav` | sim | 01:35:28 | entrada de elemento | 00:00:17:05 | **RETIME** |
| 23 | C02_01 | `SFX_SYN_pop.wav` | sim | 01:36:10 | entrada de elemento | 00:00:17:15 | **RETIME** |
| 24 | C02_02 | `MA_Amenteramco_Whoosh_Pass-By_1.wav` | sim | 01:40:19 | passagem/entrada de tela | 00:00:36:07 | **KEEP** |
| 25 | C02_03 | `SFX_SYN_pop.wav` | sim | 01:44:00 | entrada de elemento | 00:00:42:10 | **RETIME** |
| 26 | C02_03 | `SFX_SYN_pop.wav` | sim | 01:45:16 | entrada de elemento | 00:00:42:23 | **RETIME** |
| 27 | C02_03 | `SFX_SYN_pop.wav` | sim | 01:46:02 | entrada de elemento | 00:00:43:12 | **RETIME** |
| 28 | C02_03 | `SFX_SYN_pop.wav` | sim | 01:46:19 | entrada de elemento | 00:00:44:02 | **RETIME** |
| 29 | C02_03 | `SFX_SYN_pop.wav` | sim | 01:47:06 | entrada de elemento | 00:00:44:15 | **RETIME** |
| 30 | C02_03 | `SFX_SYN_thump.wav` | sim | 01:47:22 | selo/carimbo/impacto | 00:00:45:04 | **RETIME** |
| 31 | C03_01 | `SFX_SYN_thump.wav` | sim | 02:00:21 | selo/carimbo/impacto | 00:00:55:01 | **RETIME** |
| 32 | C03_02 | `MA_SergeySopko_MouseClick_1.wav` | sim | 02:04:21 | chave OFF | 00:00:57:11 | **KEEP** |
| 33 | C03_02 | `Turn the TV Off and On 1.wav` | sim | 02:04:25 | TV desligando | 00:00:57:14 | **KEEP** |
| 34 | C03_03 | `SFX_SYN_tickup1.1.wav` | sim | 02:10:03 | contador subindo | 00:01:00:08 | **RETIME** |
| 35 | C03_03 | `SFX_SYN_pop.wav` | sim | 02:12:27 | entrada de elemento | 00:01:03:04 | **RETIME** |
| 36 | C03_04 | `SFX_SYN_pop.wav` | sim | 02:16:07 | entrada de elemento | 00:01:11:01 | **KEEP** |
| 37 | C03_04 | `SFX_SYN_pop.wav` | sim | 02:17:04 | entrada de elemento | 00:01:11:23 | **KEEP** |
| 38 | C03_05 | `SFX_SYN_pop.wav` | sim | 02:21:22 | entrada de elemento | 00:01:07:03 | **RETIME** |
| 39 | C03_07 | `SFX_SYN_pop.wav` | sim | 02:37:04 | entrada de elemento | 00:01:20:10 | **RETIME** |
| 40 | C03_07 | `SFX_SYN_thump.wav` | sim | 02:45:19 | selo/carimbo/impacto | 00:01:28:22 | **RETIME** |
| 41 | C03_08 | `SFX_SYN_pop.wav` | sim | 02:51:04 | entrada de elemento | 00:01:46:15 | **RETIME** |
| 42 | C03_08 | `SFX_SYN_pop.wav` | sim | 02:51:10 | entrada de elemento | 00:01:46:20 | **RETIME** |
| 43 | C04_01 | `MA_Amenteramco_Whoosh_Pass-By_1.wav` | sim | 03:04:01 | passagem/entrada de tela | 00:01:52:13 | **RETIME** |
| 44 | C04_01 | `SFX_SYN_tickup2.6.wav` | sim | 03:04:07 | contador subindo | 00:01:52:17 | **RETIME** |
| 45 | C04_02 | `MA_Amenteramco_Whoosh_Pass-By_1.wav` | sim | 03:09:13 | passagem/entrada de tela | — (cue DROP) | **DROP** |
| 46 | C04_02 | `MA_Amenteramco_Whoosh_Pass-By_1.wav` | sim | 03:11:07 | passagem/entrada de tela | — (cue DROP) | **DROP** |
| 47 | C04_03 | `SFX_SYN_tickup1.0.wav` | sim | 03:14:16 | contador subindo | 00:01:56:07 | **RETIME** |
| 48 | C04_04 | `SFX_SYN_thump.wav` | sim | 03:21:22 | selo/carimbo/impacto | 00:02:00:10 | **KEEP** |
| 49 | C04_05 | `MA_AleXZavesa_WooshAndBoom_1.wav` | sim | 03:24:07 | placa GRITEM | 00:02:01:08 | **KEEP** |
| 50 | C04_06 | `SFX_SYN_thump.wav` | sim | 03:28:12 | selo/carimbo/impacto | 00:02:05:16 | **RETIME** |
| 51 | C04_06 | `MA_Amenteramco_Whoosh_Pass-By_1.wav` | sim | 03:32:14 | passagem/entrada de tela | 00:02:09:18 | **RETIME** |
| 52 | C05_01 | `SFX_SYN_tickup0.95.wav` | sim | 03:38:22 | contador subindo | 00:02:19:13 | **RETIME** |
| 53 | C05_01 | `SFX_SYN_tickup0.95.wav` | sim | 03:45:10 | contador subindo | 00:02:26:03 | **RETIME** |
| 54 | C05_01 | `SFX_SYN_tickup0.95.wav` | sim | 03:48:01 | contador subindo | 00:02:28:20 | **RETIME** |
| 55 | C05_02 | `MA_AppleHillStudios_WrongAnswer_1.wav` | sim | 03:55:06 | resposta errada ("AINDA NÃO") | 00:02:29:21 | **RETIME** |
| 56 | C05_04 | `SFX_SYN_thump.wav` | sim | 04:00:23 | selo/carimbo/impacto | 00:02:35:21 | **RETIME** |
| 57 | C05_04 | `MA_Amenteramco_Whoosh_Pass-By_1.wav` | sim | 04:02:08 | passagem/entrada de tela | 00:02:37:09 | **RETIME** |
| 58 | C05_04 | `MA_Amenteramco_Whoosh_Pass-By_1.wav` | sim | 04:03:11 | passagem/entrada de tela | 00:02:38:12 | **RETIME** |
| 59 | C06_03 | `SFX_SYN_pop.wav` | sim | 04:39:18 | entrada de elemento | 00:03:13:02 | **RETIME** |
| 60 | C06_03 | `SFX_SYN_thump.wav` | sim | 04:42:00 | selo/carimbo/impacto | 00:03:15:12 | **RETIME** |
| 61 | C06_05 | `SFX_SYN_thump.wav` | sim | 04:53:28 | selo/carimbo/impacto | 00:03:29:05 | **RETIME** |
| 62 | C06_05 | `SFX_SYN_thump.wav` | sim | 05:02:04 | selo/carimbo/impacto | 00:03:37:10 | **RETIME** |
| 63 | C06_07 | `SFX_SYN_thump.wav` | sim | 05:10:25 | selo/carimbo/impacto | 00:03:59:21 | **RETIME** |
| 64 | C06_07 | `SFX_SYN_thump.wav` | sim | 05:17:07 | selo/carimbo/impacto | 00:04:06:07 | **RETIME** |
| 65 | C07_01 | `SFX_SYN_pop.wav` | sim | 05:20:29 | entrada de elemento | 00:04:07:18 | **KEEP** |
| 66 | C07_02 | `SFX_SYN_tickup0.9.wav` | sim | 05:22:10 | contador subindo | 00:04:11:01 | **RETIME** |
| 67 | C07_02 | `SFX_SYN_tickup0.8.wav` | sim | 05:25:22 | contador subindo | 00:04:14:10 | **RETIME** |
| 68 | C07_03 | `01 Clock Ticking.wav` | sim | 05:31:08 | relógio | 00:04:22:05 | **RETIME** |
| 69 | C07_03 | `SFX_SYN_rise2.6.wav` | sim | 05:31:08 | ano subindo até 2038 | 00:04:22:05 | **RETIME** |
| 70 | C07_04 | `SFX_SYN_pop.wav` | sim | 05:35:04 | entrada de elemento | 00:04:27:05 | **RETIME** |
| 71 | C07_05 | `SFX_SYN_thump.wav` | sim | 05:39:29 | selo/carimbo/impacto | 00:04:33:07 | **KEEP** |
| 72 | C07_06 | `MA_SoundsByGFXSounds_DingNotification_1.wav` | sim | 05:47:29 | sticker "gente." | 00:04:44:05 | **KEEP** |
| 73 | C09_01 | `SFX_SYN_tickup1.1.wav` | sim | 06:01:29 | contador subindo | final +0.20s | **RETIME** |
| 74 | C09_01 | `SFX_SYN_party.wav` | sim | 06:03:02 | estouro do 300 | final +1.30s | **RETIME** |

Além dos 74: **bleep 1 kHz** (1,27 s) e os **áudios de bastidor** do cold open (`COLD_B_2023_05_24.wav`, `COLD_B_VERDADES.wav`; só o primeiro, 4,15–6,50 s, sobrevive).

## 5. Música e desenho de som (todas as trilhas da V2)

| Trilha | Arquivo (existe em `V2_GERADOS/AUDIO`) | TC V2 IN → OUT | Ganho / tratamento | Função | Viradas / ducking | Migração para a nova edição |
|---|---|---|---|---|---|---|
| **Aviso** | `MA_LEXMusic_BeatTheOdds_30s.wav` | 00:14:20 → 00:52:20 (da página 1 do aviso até 0,6 s após a 1ª palavra) | −13 dB; repete (30 s) com fade 0,5 s; rampa até −30 dB nos últimos 1,6 s | clima de "instrução de cinema", leve e engraçado | cai por baixo da íris de entrada | começa com a página 1 do aviso e sai sob a tela do 300 / entrada da fala (mesma rampa) |
| **Bed** | `Trigubovich_A_Groove_Pool_loop_long.wav` | 00:51:02 (1 s antes da 1ª fala) → 05:57:29 (0,2 s antes do título) | −31 dB; fade-in 2,5 s / fade-out 1,4 s; loop | cama sob todo o diálogo | **+10 dB no respiro do GRITEM** (3 s); ducking das SFX sob a voz | sob a sequência do Gabriel inteira, mesmo −31 dB sem tocar na mixagem dele; +10 dB só se o freeze existir |
| **Final** | `MA_Puremusic_InTheSpotlight_12s.wav` | 05:58:05 → fim (título → 300 → loop) | −9 dB; fade-in 1,2 s (marcador do Gabriel: "não entrar estourando") / fade-out 1,2 s | celebração do 300 | entra com o título e segue sob "300 e contando" | entra com o título/final (posição ainda a definir) |

Outros elementos de som: diálogo da V2 = CAM_GERAL +2 dB (**não migra**: vale o tratamento do Gabriel); alvo de mix −16 LUFS / −1,5 dBTP (referência para o mix final dele); beeps de contagem 1 kHz (3×); bleep 1 kHz; `ORIGEM_MOTION_ARRAY.txt` registra a origem/licença das faixas e SFX. **Não escolher músicas novas.**

## 5B. Reconciliação 39 → 44 cues (proveniência dos 5 adicionais)

A V0 (28/09) documentava **39 overlays** (referência: `LEARNINGS.md`, `v0/README.md`).
A V2 expandiu para **44** (documentado em `v3-preflight/EP300_V3_PREFLIGHT.md` como baseline OLD).

Diferença: **+5 cues**. Origem documental dos 5:

| ID | Descrição | Origem | Data |
|---|---|---|---|
| 1 | **UNKNOWN_PROVENANCE** | — | — |
| 2 | **UNKNOWN_PROVENANCE** | — | — |
| 3 | **UNKNOWN_PROVENANCE** | — | — |
| 4 | **UNKNOWN_PROVENANCE** | — | — |
| 5 | **UNKNOWN_PROVENANCE** | — | — |

**Nota:** a documentação disponível não permite rastrear quando os 5 foram adicionados ou qual é a sua origem criativa. Os nomes/funções dos 44 cues atuais estão todos listados na seção 2 deste documento. Se a proveniência for crítica, será necessário uma busca manual nas pastas V0/V2 ou consulta ao histórico do trabalho anterior.

---

## 6. Reconciliação com o preflight V3 (decisão posterior vence)

| Item | Preflight V3 | Decisão posterior | Vale |
|---|---|---|---|
| Abertura (H1) | duas aberturas possíveis | take 42,5 s (Gabriel usou 42,17 s) | posterior |
| Pica-Pau (H5) | default passada curta | **passada longa** na timeline | posterior |
| Fecho (H6) | default 592–607 | 592,13–609,98 + improviso hard-skill mantido (547–555) | posterior |
| Kinoplex | rótulo "APOIADOR" + gramática PATROCÍNIO, logo faltando | Gabriel: **APOIADOR**, logo `logo_kinoplex2.png` **branca/original, nunca sticker**; posição = linha "REALIZAÇÃO / APOIADOR" | posterior |
| C03_04 / C03_05 | ordem trocada (GA4 antes de "de nada, Vitória") | confirmado pela timeline | igual |
| C06_04 "de nada, Purple" | DROP provisório | **NEEDS HUMAN LISTEN** (H3); Gabriel manteve a linha | posterior (mantém ADAPT) |
| C02_03 pausa 2,4 s | manter pausa | pausa não existe na timeline | decisão pendente do Gabriel |
| 2038 (C07_03) | ADAPT genérico | **O02** com DeLorean + dupla Marty/Doc | posterior |
| Assets "criar 0" | zero asset novo | assets oficiais novos fornecidos (Toddynho, DeLorean, Marty+Doc, extintor, microfone, balde ×2, Kinoplex) | posterior |
| KEEP/ADAPT/DROP do preflight | 21 REUSE · 13 ADAPT · 5 DROP | **Atualizado 03/10:** o preflight previa 5 DROP; hoje são **3 DROP_SCRIPT** (C01_02, C01_03, C04_02) — C03_06 virou ADAPT (a fala mudou de sentido, não sumiu) e C06_02 virou MOVE (H7: censura do "fucking") | substituído por decisão posterior |

## 7. Melhorias V4 que devem sobreviver

| V4 | Substitui/estende | Estado |
|---|---|---|
| P01-CONTAGEM (anel + ticks + numeral sticker) | C00_01 | feita; precisa dos 3 beeps de 1 kHz |
| P02-AVISO (cinema, redlines, extintor, balde, Gustavo sorrindo) | C00_03 | feita; precisa da trilha do aviso + 11 SFX; balde A × B a confirmar |
| P03-TELA-300 (selo central, PATROCÍNIO/CAFÉ/REALIZAÇÃO/APOIADOR) | C00_02 | feita; falta a íris para a câmera |
| S01…S11 + cadeia S02S03 (11 slots) | C02_01, C03_03/05/07/08, C05_02/05, C06_03/05, C07_02 | feitas e revisadas; cada uma tem remanescente em câmera ativa (ver tabela) |
| Toddynho (sticker oficial) em S09 | C06_03 | feito; `toddynhoSrc` substituível |
| O01 (setup) + O02 (payoff 2038) com DeLorean + dupla Marty/Doc | C07_03 | feitos; camadas separáveis; sofá do site a decidir |
| F01-FINAL-300 (300 sobe + logos + texto temático) | C09_01 | proposta; texto = prop (3 opções) |
| PopcornBucket (balde + pipocas animáveis) | abertura e looping | componente pronto; pipocas soltas aguardam assets |
| Extintor, microfone | — | extintor usado; microfone disponível (sem função pedida) |
| Redlines aplicados (maiúsculas, setas, emoji sticker, Layla fora, "já paga até boleto") | vários | valem |
| STICKER_BOUNDS_CHECK (QA permanente) | — | vale |
| Extrator da timeline (`extract_timeline.py`) e Remotion com props editáveis | — | vale (ferramenta, não filme) |

## 8. Assets e decisões que ainda faltam

> **Atualizado 03/10:** itens abaixo marcados ~~assim~~ foram resolvidos/superados; estado detalhado em `EP300_DECISIONS_LOG.md` §4–§5. Pipocas soltas **existem** (`Sete pipocas estouradas em adesivos.png`); Pica-Pau novo, 4 frames da evolução, frame EP126 e bandeiras extras = MISSING_USER_PROVIDED_ASSET; stickers do mural já existem.

- **Pipocas soltas individuais** (Gabriel vai adicionar) — para o balde animável (aviso e looping).
- **Sticker novo do Pica-Pau** (personagem protegido; o Gabriel fornece).
- **Balde oficial:** duas faces na pasta (A "EPISÓDIO 300/Kinoplex", B "Do Império dos Dados…") — confirmar qual (ou alternar).
- **Frames novos do acervo** (busca dirigida): EP1 (melhor), EP100 (luz melhor), EP210 (sem CTA), EP153 (Gustavo em pose boa), frame do convidado do EP126, prints para o bordão 203× (cenários diferentes, reações boas; fora EP288/EP187).
- **Mais bandeiras** (só 16 desenhadas) e **mais stickers/prints** para o mural 191 → "quase 200".
- **Ícone da Reportei** em tile branco (só existe o wordmark).
- **Marty e Doc separados** (só existe a arte combinada) — opcional.
- **Supercut 158 cortes** (16:43): inspecionar e escolher trecho curto para o bordão — decisão H8.
- **H3** (ouvir 412,3–413,6 s) e **H7** ("fucking" 80,9 s: bleep/dip/manter).
- **Decisões de timeline do Gabriel:** freeze GRITEM de 3 s · pausa da evolução de 2,4 s · onde entram título (C08_01) e final (C09_01) · onde fica o blooper inicial (suposição: após a tela do 300) · take exato do cold open que ele riscou.
- **Cena do sofá** (asset oficial do site, 6 quadros): volta como parte do beat 2038?
- **Texto da tela final** (F01): escolher entre "300 episódios, 300 perguntas… / e a de hoje começa agora.", "a pergunta continua.", "300 respostas. Falta a pergunta."

## 9. Regras para a futura implementação (ainda NÃO autorizada)

- Entregar uma **camada adicional**: V2+/A2+ para colar na sequência do Gabriel (overlays com alfa da V2 quando funcionam; V4 onde existe; stickers/accents como clipes separados), trilhas e SFX como trilhas de áudio separadas e ducking por keyframes — **sem** reconstruir câmera, cor, enquadramento ou áudio.
- Overlays que **não** funcionam por mudança de timing interno viram V4 (Remotion com props); os `.mov` da V2 valem quando a fala casa (KEEP).
- Revisão do resultado: **exportando do Premiere**; qualquer preview externo é só auxiliar e nunca "o filme".
