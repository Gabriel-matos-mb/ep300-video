# EP300 — CHAT CLEAR HANDOFF (03/10/2026)

> Checkpoint obrigatório antes do `/clear`. **Só documentação. Nada foi implementado, renderizado, gerado ou alterado no audiovisual.**
> Ler este arquivo + `EP300_NON_NEGOTIABLES.md` antes de qualquer ação no EP300.
> Escopo: EP300 / Analytics Talks / Kinoplex. Nada do Analytics Summit Manifesto / Manifesto V4 / Summit 2026 entra aqui (NON_NEGOTIABLES §22).
> `MIGRATION_MAP = NORMALIZED` · **`EXECUTION_READY = NO`** · **CUES ACCOUNTED ≠ VISUAL ASSETS APPROVED ≠ EXECUTION READY**

---
## 1. Autoridade e non-negotiables (resumo; texto completo em `EP300_NON_NEGOTIABLES.md`)
1. Decisões humanas explícitas / LOCKED → 2. **Premiere atual do Gabriel** (`EDITORIAL_TECHNICAL_AUTHORITY`) → 3. **`EP300_ABERTURA_V2_PROXY`** (`CREATIVE_BASELINE_APPROVED`) → 4. handoff visual oficial EP300/site → 5. nova gravação → 6. V4 / redlines aprovadas (`SELECTIVE_IMPROVEMENTS`) → 7. Migration Map (`RECOVERY_RECONCILIATION_MAP`, não autoridade criativa).
- `PRE_EDITED_4K_SAFETY_MASTER` fica entre o Premiere editável e qualquer reconstrução (não substitui o Premiere).
- A regravação é nova fonte de imagem/fala, **não** autorização para remontar o vídeo.
- `EP300_V4_ASSEMBLY_REVIEW.mp4` = **REJEITADO** (`DO_NOT_USE_AS_BASELINE`).
- **KEEP BY DEFAULT, DROP BY EXCEPTION** (`DROP_USER` / `DROP_SCRIPT` / `DROP_FACT` / `REPLACE_APPROVED`). Na dúvida: PRESERVAR. Nenhum elemento aprovado some em silêncio.
- Música, SFX e ducking da V2 são baseline. Disabled slots **não** são os únicos lugares de motion. SLOT / OVERLAY / INSERT / ACCENT são categorias distintas.
- Claude **não** reconstrói a montagem via FFmpeg (FFmpeg = utilidade/QA/proxy/transcode). Asset ausente = placeholder ou flag, nunca invenção. Decisão humana aberta não se fecha em silêncio. Documentação não autoriza execução.
- Remapeamento por **fala/beat**, nunca por timecode antigo.

## 2. Estado atual
- Migration Map: 44 overlays = 2 KEEP EXACTLY · 9 KEEP+RETIME · 14 ADAPT · **1 MOVE (C06_02)** · 15 REPLACE_APPROVED · 0 NEEDS_HUMAN · **3 DROP_SCRIPT (C01_02, C01_03, C04_02)**.
- SFX: 74 = 11 KEEP · 58 RETIME · 0 REPLACE · 5 DROP_SCRIPT (`SFX_SYN_tickup1.0` C01_02 · `SFX_SYN_tickup1.1` C01_03 · `SFX_SYN_thump` C01_03 · `MA_Amenteramco_Whoosh_Pass-By_1` ×2 C04_02). **Inalterado.** `SFX_BLEEP_1kHz.wav` **não** está nos 74 (`GAG_SPECIFIC_SFX / FUCKING_CENSORSHIP`).
- 8 casos V2×V4: **RESOLVED** (ver `EP300_DECISIONS_LOG.md` §1).
- Documentos: `EP300_NON_NEGOTIABLES.md` · `EP300_V4_MOTIONS/EP300_V2_TO_V4_MIGRATION_MAP.md` · `EP300_V4_MOTIONS/EP300_DECISIONS_LOG.md` · `EP300_V4_MOTIONS/EP300_V4_REDLINES.md` (transcrição antiga, **superada pelo registro da seção 4**) · `EP300_V4_MOTIONS/EP300_HUMAN_DECISIONS_V2_x_V4.md` (superado).

## 3. Decisões LOCKED
- **FUCKING / H7:** censurar, **com o tom divertido da V2** (timing cômico, bleep/SFX, reação 🙊/audiovisual, intervenção visual associada). Remapear para o "fucking" da nova gravação (~80,9 s, dentro de C02_02). Sem bleep seco/genérico; sem cortar a fala; pode melhorar acabamento/sincronismo, **não** reinventar a gag. C06_02 = MOVE.
- **GRITEM:** freeze de ~2–3 s para a plateia gritar; não comprimir por ritmo.
- **8 casos:** C02_01 híbrido V2+V4 (polaroid EP1 não volta) · C03_03 V4 · C03_05 V4 (3 em cada 10) · C03_07 V4+complemento (IA METADE, BigQuery→MARKETING) · C05_02 V4+complemento (PARCEIRO DO GOOGLE? / AINDA NÃO) · C07_02 V4+complemento (100+ MIL HORAS) · C07_03 híbrido (setup/payoff V4 com DeLorean+Marty/Doc + cena do sofá no payoff 2038) · C09_01 V4+ajuste ("300 episódios, 300 perguntas… / e a de hoje começa agora."; "vocês estão aqui e contando" segue rejeitada).
- **H4:** sem o carimbo "IA NA HOME DO GA" (não falado). **H9:** "4 EM 10" só em INCREMENTALIDADE. **H10:** "meia-culpa" ancorada em 445,1–448,3 s ("Quem disse foi o Gustavo, mas… eu fiz também"). (Detalhe em `EP300_DECISIONS_LOG.md` §11.)
- **SUPERCUT** `BORDAO_SUPERCUT_158_cortes.mp4` = `REFERENCE_ARCHIVE / DO_NOT_INSERT_BY_DEFAULT` (compilado do Lucian com IA dos "Fala aí, analítico e analítica de plantão"; só fonte de frames/prints se um momento específico precisar; não analisar agora).
- **STICKERS:** o Gabriel já fez todos. Antes de marcar qualquer um como MISSING, conferir os assets fornecidos/pasta oficial. Não regenerar os aprovados. (Correção: as pipocas soltas **existem** — `Sete pipocas estouradas em adesivos.png`.)

## 4. REDLINE REGISTER — as 26 imagens enviadas por Gabriel
Fonte: transcrito da sessão; cópias em `EP300_V4_MOTIONS/redlines_source/R01…R26_*`. **26/26 recuperadas.** As marcações vermelhas são **instruções**, nunca elementos de design. Estados: `RESOLVED` (corrigido; manter como anti-regressão) · `STILL_OPEN` (solução/asset ainda por aplicar ou decidir) · `SUPERSEDED` · `REFERENCE_ONLY`. "Aplicado" = presente no V4/preview; **a validação visual final é no Premiere**.

| # | Arquivo | Tela / cena | O que Gabriel marcou (transcrição literal) | Problema | Correção pedida | Status | Intenção humana (anti-regressão) |
|---|---|---|---|---|---|---|---|
| R01 | S01 | "DE ONDE VEM" (2015→PRIME→MB TALKS→A VOLTA) | (a) seta na polaroid EP1·2021: "não usar esse take / gustavo e mafe nem estão em pose boa. Gustavo coçando nariz. tirar!!!!" · (b) seta no sticker do Lucian: "NÃO USAR ESSE EMOJI DE HOVER PRA DAR IDEIA DE SUSTO. TROCAR…" | frame ruim (poses, Gustavo coçando o nariz) + expressão de susto no rosto do Lucian | remover a polaroid; trocar o rosto do Lucian | **RESOLVED** (polaroid removida; Lucian `still`) | nenhum frame em que alguém esteja em pose ruim; rostos-sticker não podem transmitir "susto" sem intenção. C02_01 híbrido: **a polaroid/take EP1 rejeitada NÃO volta** |
| R02 | S05 | "A PERGUNTA MUDOU" · "dá pra confiar no modelo?" | caixa vermelha em **"modelo."**: "deixar estilo sticker." | palavra solta sem linguagem de sticker | aplicar estilo sticker (anel branco) | **RESOLVED** | palavra-destaque = sticker, não texto cru |
| R03 | S07 | FICHA DE PRESENÇA Phill 29× / Mafê 24× | setas na polaroid EP1·2021: "NÃO USAR ESSE PRINT SOBRE ESSE EP. POSE HORRÍVEL. AJUSTAR POR OUTRO." | pose ruim no print do EP1 | trocar por outro frame | **RESOLVED** (outro frame do clipe EP1, ~2,0 s) | print histórico escolhido pela qualidade do momento, não só por ser do episódio certo |
| R04 | S08 | FICHA + Cláudio "Coisa Rica" Bonel 7× | seta na pill "até pra dar boleto": "TROCA A FRASE PARA: JÁ PAGA ATÉ BOLETO." | frase errada | trocar o texto | **RESOLVED** | texto da pill = "já paga até boleto" |
| R05 | S09 | "A GENTE CHEGOU ANTES" · FEV 2022 · +27 DIAS | (a) seta em "todinho todo?": "O CERTO É TODDYNHO" · (b) seta no carton: "NÃO USAR ESSE EMOJI HORRÍVEL. VOU TENTAR GERAR UM STICKER DO TODDYNHO." | grafia + ilustração ruim | grafia **TODDYNHO** e sticker oficial | **RESOLVED** (sticker oficial do Gabriel em `stickers/toddynho.png`) | marca grafada TODDYNHO; usar o sticker oficial feito pelo Gabriel, nunca ilustração improvisada |
| R06 | S10 | linha do tempo OUT 2024 / ABR 2025 · globo 🌎 | seta no globo: "ESTILO STICKER! / EMOJIS SEMPRE ESTILO STICKER" | emoji solto sem contorno sticker | globo em sticker | **RESOLVED** | **regra permanente:** emoji usado como elemento visual independente = estética sticker |
| R07 | cold open (V2 proxy) | take de arquivo REC/BASTIDOR P&B (Coffee++ na mesa) | X vermelho no quadro: "TIRAR ESSE TAKE DO VIDEO FINAL!!!! NÃO USAR ESSE!!" | take indevido no vídeo final | remover | **RESOLVED** (fora do assembly; blooper inicial = só Lucian "começou? começa de novo" + risada; **nunca** "tá no ar, tá valendo"). Posição do blooper na sequência segue decisão editorial no Premiere | esse take **não pode** reaparecer; blooper inicial é o trecho aprovado do Lucian |
| R08 | contagem 3-2-1 (pré-sessão) | tela "1", anel laranja | (texto do chat) "ESSA TELA DE CONTAGEM 3...2....1 PRECISA ficar visualmente melhor. ta meio amadora." | visual amador | redesenhar | **RESOLVED** (P01-CONTAGEM redesenhada) — validação visual pendente | contagem precisa de acabamento de cinema, não de slide |
| R09 | aviso p.1 | "As saídas de emergência ficam nas laterais." + placas SAÍDA | círculo/seta na placa esquerda: "o video final deve começar por aqui… / corrigir a seta q tá invertida. / tem que ser <- saída (emoji) / (emoji) saída ->" | seta invertida; emoji ↔ direção da saída incoerentes | placa esquerda `← SAÍDA 🏃`, placa direita `🏃 SAÍDA →`; o vídeo final começa por esta tela | **RESOLVED** | o vídeo começa aqui (sem cold open antes); seta e personagem coerentes com o sentido da saída |
| R10 | aviso p.2 | "Levanta a mão quem já disse 'eu acho'" · emoji 🙋 | seta no emoji: "emoji cortando, corrigir. transformar em sticker e validar qualidade do emoji, esse parece baixa resolução…" | emoji cortado, baixa resolução | sticker vetorial inteiro | **RESOLVED** | emoji nunca cortado nem pixelado |
| R11 | aviso p.2 | mesma tela · emoji 😅 | seta: "emoji cortado. tranformar em sticker." | emoji cortado | sticker inteiro | **RESOLVED** | idem; 🙋 sai quando 😅 entra |
| R12 | aviso p.1 | "se você falar 'eu acho'," | seta em "se": "Se a palavra anterior terminou com ponto essa deve começar com letra maiuscula." | minúscula após ponto | "Se…" | **RESOLVED** | regra: depois de ponto, maiúscula |
| R13 | aviso | "A pessoa também levantou. / você não está sozinho." | seta: "letra maiuscula." | idem | "Você…" | **RESOLVED** | idem |
| R14 | aviso (celular) | "Celular liberado. só vamos reclamar se você não marcar a gente." + Gustavo de olhar lateral | seta no sticker: "trocar esse sticker / usar o Gustavo sorrindo ou de boca aberta :o" | expressão ruim do Gustavo | Gustavo sorrindo ou boca aberta | **RESOLVED** (`gustavo-hover-transicao`) | rosto-sticker com expressão simpática/engraçada; "Só…" com maiúscula |
| R15 | aviso (pipoca) | "Podem pegar a pipoca." + balde antigo | (a) seta no balde: "a gente trocou esse balde / tentar trocar imagem…" · (b) seta em "vocês vieram": "letra maiuscula." | balde antigo; minúscula após ponto | balde novo EP300; "Vocês…" | **RESOLVED** (balde A "EPISÓDIO 300" aplicado, "Vocês…" corrigido). **Pendência humana à parte:** 2 baldes na pasta (A × B) — escolher A, B ou alternar | usar o balde oficial novo; nunca o antigo |
| R16 | tela do 300 (inicial) | selo EPISÓDIO 300 + faces laterais + pill + PATROCÍNIO | (a) X nas faces laterais: "tirar emojis repetidos do Gustavo e Lucian. deixar apenas o central." · (b) linha de centro: "alinhar ao centro as logos e infos." · (c) seta na pill: "alinhar esse texto e caixa e começar com maiusculo." · (d) "alinhar ao centro as logos e infos. alimentar com métricas boss e kinoplex [leitura incerta da palavra 'alimentar'] / mb como realização e kino como apoiador" | rostos repetidos; desalinhamento; minúscula; falta MB e Kino | só o selo central; tudo centralizado; "A sessão vai começar"; MB = REALIZAÇÃO, Kino = APOIADOR | **RESOLVED** (P03-TELA-300). Categorias agora **LOCKED** (seção 6) | uma só presença de Gustavo/Lucian (a do selo); alinhamento central; institucional na hierarquia correta |
| R17 | C02_03 | "A PERGUNTA FOI MUDANDO" · EP1/EP73/EP100/EP153/EP210/HOJE | 4 marcações: EP1·2021 "TROCAR PRINT POR OUTRO MELHOR" · EP100·2023 "TROCAR PRINT POR OUTRO COM LUZ MELHOR" · EP210·2025 "TROCAR PRINT POR OUTRO MELHOR. (SEM O CTA EMBAIXO)" · EP153·2024 "TROCAR PRINT (GUSTAVO EM POSE RUIM)" | prints ruins (pose, luz, CTA) | 4 frames melhores | **STILL_OPEN** — não aplicado; substitutos **não localizados** (B + C, ver `DECISIONS_LOG` §8). Pausa de 2,4 s também depende da timeline | print histórico = qualidade do momento; sem CTA; sem pose ruim |
| R18 | C03_01 | "NO COMEÇO, QUASE TUDO ERA ferramenta" · tiles de logos | seta na Reportei: "A LOGO DA REPORTEI NÃO SEGUE O MESMO PADRÃO.. AJUSTAR" | logo não está em tile branco e fica cortada | mesmo padrão dos tiles | **STILL_OPEN** (só existe o wordmark `reportei.webp`; ícone no padrão não existe) | todas as logos de ferramenta em tile uniforme |
| R19 | C04_01 | "O BORDÃO DO GUSTAVO" · 203× · EP282/284/286/288 | esq.: "TENTAR COLOCAR MAIS PRINTS PARA DAR SENSAÇÃO DE MUITAS VEZES… PRINTS COM REAÇÕES BOAS." dir.: "USAR PRINTS DE DIFERENTES CENÁRIOS.. eVITAR USAR ESSE [EP288] ESSE É DE OUTRO ESTUDIO EM SP." | 4 prints quase iguais, mesmo estúdio, outro estúdio em SP no EP288 | mais prints, cenários/épocas diferentes, reações boas; **sem EP288** | **STILL_OPEN** (frames não selecionados; supercut = só fonte de frames) | sensação de repetição histórica do bordão |
| R20 | C04_03 | "16 JEITOS DE APRESENTAR O LUCIAN" | seta no Lucian (olhar de lado): "SE ESSA TELA FICAR… TROCAR EMOJI…" | rosto do Lucian com expressão estranha | trocar o sticker | **STILL_OPEN** (a tela fica por KEEP BY DEFAULT — a fala "mais de 60 maneiras" existe; `lucian-still` existe; falta aplicar) | rosto-sticker com expressão simpática |
| R21 | C04_06 | "FRASE CLÁSSICA DO LUCIAN" · 24× · Pica-Pau + viatura | seta no pássaro: "COLOCAR NOVO STICKER DO PICA PAU." | sticker de pica-pau genérico | sticker novo | **STILL_OPEN** — o sticker novo foi **produzido pelo Gabriel** (`USER_CONFIRMED_ASSET_EXISTS / FILE_NOT_LOCATED`); **não gerar outro; não usar a silhueta antiga automaticamente** | preservar a piada; usar o sticker feito pelo Gabriel |
| R22 | C05_01 | "191 PESSOAS SENTARAM NESSA MESA" | "AQUI PRECISAREMOS COLOCAR MAIS STICKER E/OU MAIS PRINTS, QUEREMOS DAR A SENSAÇÃO DE MUITA GENTE. DESSA FORMA PARECE UM RANKING. QUEREMOS DAR A SENSAÇÃO DE QUANTIDADE/VARIEDADE DE PESSOAS." + X no print EP187·convidado remoto: "esse cara tá BANIDO DESSE VÍDEO!!!!" | parece ranking; pouca variedade; print banido | mais stickers/prints; remover o EP187 | **STILL_OPEN** (stickers existem: Guta, Vitória, Lucas, Layla, Phill, Mafê, Bonel; falta compor). **EP187 BANIDO** | multidão/diversidade, nunca ranking |
| R23 | C05_04 | Pica-Pau → "NÓS CHAMAMOS" · EP126 PMERJ | seta no frame do convidado: "TENTAR TROCAR ESSE FRAME DELE" | frame ruim (olhando para baixo) | outro frame | **STILL_OPEN** (substituto não localizado; B + C) | preservar o conceito da piada; frame com boa expressão |
| R24 | C07_04 | "110 países" + bandeiras | "COLOCAR MAIS BANDEIRAS" | poucas bandeiras (16) | mais bandeiras, linguagem de sticker | **STILL_OPEN** (C — bandeiras adicionais não existem). Nota H2: a fala diz "100+" aqui e "110" no fecho | bandeiras quadradas, borda de tinta + sombra sólida (formato do site) |
| R25 | C09_01 | "EPISÓDIO 300 · vocês estão aqui · e contando." | (texto do chat) "ESSE 'vocês estão aqui e contando.' não tá fazendo sentido não, precisamos mudar isso... para dar alguma conexão melhor com a temática do vídeo…" | frase sem sentido | nova copy ligada ao tema | **RESOLVED** (direção de texto LOCKED: "300 episódios, 300 perguntas… / e a de hoje começa agora."; F01 usa essa linha). A frase da V2 fica **REJEITADA** | tela 300 = celebração/abertura do episódio, não encerramento corporativo |
| R26 | C09_01 | tela final V2: EPISÓDIO 300 + PATROCÍNIO OFICIAL (Purple Metrics, Onfly) · CAFÉ OFICIAL (Coffee++) · REALIZAÇÃO (Métricas Boss) | (texto do chat) "essa tela final com as logos/ep 300/patrocinadores/café e realização funciona melhor q a tela inicial, eu digo em questão de estrutura visual…" | — | usar como referência de estrutura | **REFERENCE_ONLY** (já aplicada como estrutura de P03/F01) | referência estrutural de organização institucional |

**Totais:** recuperadas **26/26** · RESOLVED **17** (R01–R16, R25; R07/R08/R15 com nota) · STILL_OPEN **8** (R17–R24) · SUPERSEDED **0** · REFERENCE_ONLY **1** (R26).
Notas: R17 contém 4 marcações; R16 contém 4; R01 contém 2. Esta contagem por **imagem** supera as 25 linhas por cue de `DECISIONS_LOG` §4/§9 (que estão corretas em conteúdo, só agregadas de outro jeito).

## 5. Assets fornecidos pelo usuário (já existem)
Pasta Drive `01_VIDEO DE ABERTURA/00_ASSETS E INSERTS/`: `stickers e emojis refeitos/` (Guta ×3, Vitória ×4, Lucas ×3, Layla, Phill ×2, Mafê ×3, Bonel ×3, viatura, Toddynho, DeLorean, Marty+Doc `Dupla futurista em sintonia`, microfone, extintor, 2 baldes, balde antigo, **Sete pipocas estouradas em adesivos**) · `logos/logo_kinoplex2.png` · `300-handoff-video/` (cena do sofá, patrocinadores `onfly/purple-metrics/coffee-plusplus/reportei/eletromidia/sinatra`, personagens, selo). Cópias de trabalho em `EP300_V4_MOTIONS/assets/`.
**Não localizado (mas informado como existente):** sticker novo do Pica-Pau (`A`). **Realmente faltando (`C`):** frames substitutos da evolução (EP1/EP100/EP210/EP153), frame do EP126, prints do bordão, ícone/tile da Reportei, bandeiras extras.
**Observação técnica:** a cópia de trabalho da logo Kinoplex é **300×75 px** — validar suficiência de resolução na implementação (sem redesenhar/esticar com efeitos).

## 6. Institucional — LOCKED (não reinterpretar)
**REALIZAÇÃO:** Métricas Boss · **PATROCÍNIO:** Purple Metrics + Onfly · **CAFÉ OFICIAL:** Coffee++ · **APOIADOR:** Kinoplex.
- Kinoplex: **logo branca da pasta `logos`**, nunca sticker, nunca redesenhada.
- Onfly: **inteira, sem crop**, dentro da safe area (a V2 tinha corte — em R16 o logo aparece parcialmente coberto pela bandeja do Windows na captura; de qualquer forma o lock vale).
- Nenhuma logo institucional é estilizada como sticker; preservar proporção e integridade dos arquivos oficiais.

## 7. Safety master 4K
`PRE_EDITED_4K_SAFETY_MASTER` = `…/01_VIDEO DE ABERTURA/01_BRUTOS/NOVOS TAKES-REGRAVADO/VIDEO PRE EDITADO CINEMA EP 300 EM QUALIDADE MAXIMA.mp4`. Edição já tratada pelo Gabriel (cortes, multicam, framing, cor, áudio). **Não** substitui o Premiere editável nem autoriza flatten. Preferir este arquivo como base consolidada; nunca reconstruir a partir dos brutos. **Estado: EXPORTING** (última checagem: ~707 MB e crescendo, sem índice `moov`). Validar só depois de estável: FILE_EXISTS · READABLE · RESOLUTION · FPS · DURATION · AUDIO_PRESENT. Não reencodar, transcrever, remontar nem comparar com os brutos.

## 8. Pendências humanas reais
1. **H3:** ouvir 412,3–414,1 s ("De nada, por favor"/"Purple"?) → define C06_04 (stickers Guta/Lucas).
2. **H2:** a edição contém "mais de 100 países" (≈4:27) **e** "mais de 110 países" (≈5:01) — aceitar a contradição ou ajustar.
3. **Balde A × B** (ou alternar).
4. **Cold open:** posição do blooper inicial na sequência.
5. Posição do título (C08_01), do final (C09_01) e a relação final → blooper P&B → loop (validar no Premiere); pausa de 2,4 s da evolução.
6. Entregar/localizar: sticker novo do Pica-Pau; frames da evolução, EP126 e bordão; ícone Reportei; bandeiras extras (ou decidir o que fazer sem eles).

## 9. WORD / PHRASE EMPHASIS PASS
`WORD_PHRASE_PASS = REQUIRED_BEFORE_FINAL_EXECUTION` — **não executada**. Rever a nova fala para achar pontos de ACCENT · HERO WORD · palavra-sticker · TYPO FULLSCREEN · NUMBER HERO · PUNCHLINE · CORRECTION/STRIKE/REPLACE · TEXT+STICKER/PRINT · reação · quebra de quarta parede · microanimação. **Não** é animar toda frase nem virar legenda cinética; a V2 é a referência de densidade/ritmo/humor; objetivo = oportunidades perdidas na montagem atual/regravação, além dos 44 cues.

## 10. Próximos passos (nenhum autorizado ainda)
1. Gabriel resolve H3, H2, balde, posições editoriais e entrega/localiza os assets da seção 8.6.
2. Validar o safety master quando terminar de exportar.
3. WORD / PHRASE EMPHASIS PASS (com o Gabriel).
4. Só então: autorização explícita para implementar a **camada adicional** (XML/overlays/música/SFX) sobre o Premiere — nunca reconstruir câmeras, cor ou áudio.

## 11. DO NOT REOPEN AFTER /clear
- Autoridade/hierarquia (seção 1) e status das versões; V4 assembly = rejeitado.
- Os 8 casos V2×V4; H7 (censura divertida); GRITEM (freeze 2–3 s); H1, H5, H6, H8, H11 e as resoluções de H4, H9, H10.
- Institucional (seção 6); Kinoplex branco sem sticker; Onfly inteira.
- Supercut = só arquivo de referência; stickers = prontos (conferir antes de dizer "missing").
- Os 17 redlines RESOLVED e o R26 — são anti-regressão, **não** pendência.
- 44/44 cues e 74/74 SFX (contagens da seção 2).
- Isolamento EP300 × Manifesto.
- Não refazer discovery do Premiere (5:15, 101 cortes, 11 slots, multicam, P&B final) — já está em `EP300_V4_MOTIONS/reports/timeline_dump.json`.

## 12. Auto-validação (feita antes de parar)
26/26 imagens recuperadas e cada uma com status · corrigidos não reabertos · pendentes não marcados como resolvidos (R17–R24 = STILL_OPEN) · stickers existentes não listados como missing (Pica-Pau = A) · institucional MB / Purple Metrics + Onfly / Coffee++ / Kinoplex · Kinoplex branco sem sticker · Onfly sem crop · censura divertida e freeze 2–3 s preservados · supercut só referência · safety master sem substituir o Premiere · V2 baseline · V4 assembly rejeitado · nada do Manifesto · `EXECUTION_READY = NO`.

---
## FECHAMENTO DA SESSÃO DO OPENING (03/10/2026) — SUPERA O ESTADO "EXECUTION_READY = NO" ACIMA
**STATE: CREATIVE / PICTURE LOCK PROVISÓRIO → finalização no Premiere (Gabriel).** Não iniciar Review 04 automaticamente. MP4 da Review 03 = última referência completa de revisão, **não** é master.
**Autoridade:** correções 4K posteriores > Review 03 (por componente); Premiere final do Gabriel > tudo.
**Componentes atuais (caminhos sob `review01/`):**
- `layers_r03_ep1fix_4k/C02_03.mov` (4K, print novo do EP1; 720p em `layers_r03_ep1fix/`)
- `work/r3/rem4k/S10.mov` (JUL 2026 / JULHO DE 2026) · `work/r3/rem4k/O01.mov` e `O02.mov` (4K, DeLorean de frente; O02 com sofá subido)
- Demais layers R03: `layers_r03/` · pacote editável: `editable_r03/` (XML `EP300_V4_PRESENTABLE_REVIEW_03.xml`, `timing_map_review03.json`, stems/SFX) · MP4: `V4_PRESENTABLE_REVIEW_03.mp4`
- Fontes: `b3/b3.py` (motor V2), `EP300_V4_MOTIONS/remotion` (Remotion; `RSCALE=2` = 4K), `b2/`, `compose_video.py`/`mix_audio.py`/`build_xml.py` (`REV=03`). Review 02 intacta.
**Preservar tudo** (layers, renders 4K, código, XML, timing maps, stems, SFX, assets, checkpoints, R02/R03). Nada apagado/movido/enviado ao Drive.
**Pendente (POST-master):** `EP300_OPENING_STORAGE_RECONCILIATION` — LOCAL SSD ↔ DRIVE (regra Drive First; COPIAR→VALIDAR→APAGAR; classes: master/editável/código/asset/layer final/áudio/doc → preservar+Drive; proxy/cache → regenerável; frames/contact sheets → descartável; intermediário/obsoleto/duplicado → avaliar). Medir: tamanho total, maiores subpastas/arquivos, espaço recuperável, o que já está no Drive, o que existe só no SSD (`layers*` ≈ 2,5 GB cada). Nenhuma exclusão sem aprovação do Gabriel.
**Aprendizado do Premiere final** (comparar XML/.prproj do Gabriel): só após ele fornecer; não agora.
**Próximo projeto:** EP300 CINEMA LOOP — separado; usa o Opening só como biblioteca de assets/identidade/componentes aprovados (sem herdar narrativa, timing de fala, montagem, regras de cue ou elementos dependentes de áudio).
**Backlog POST-EP300:** Usage & Token Observatory, Storage Hygiene, Abandonment Check, MB Studio Consolidation Pass.
