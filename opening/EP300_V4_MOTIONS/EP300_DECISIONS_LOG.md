# EP300 — Registro de decisões humanas (consolidação 03/10/2026)

> Só documentação. Nada foi implementado, renderizado, editado ou gerado.
> Escopo: EP300 / Analytics Talks / Kinoplex (PROJECT ISOLATION, NON_NEGOTIABLES §22). Nada do Manifesto/Summit foi usado.
> `MIGRATION_MAP = NORMALIZED` · `HUMAN_DECISIONS_8_CASES = RESOLVED` · **`EXECUTION_READY = NO`**
> **44/44 cues contabilizados ≠ 44/44 assets visuais aprovados.**

## 1. Os 8 casos (decisão do Gabriel, 03/10)
| Cue | Decisão | Condição |
|---|---|---|
| C02_01 | **V2 + V4 (híbrido)** | V2 para 2015 → Prime → MB Talks (~5,6 s iniciais) + V4 corrigido para a cauda (volta do Lucian → cenário antigo). Polaroid/take EP1 rejeitada NÃO volta |
| C03_03 | **V4** | retimado; mesmo desenho/função |
| C03_05 | **V4** | dado atualizado "3 em cada 10"; dado antigo não volta |
| C03_07 | **V4 + complemento** | V4 para atribuição/incrementalidade; preservar/adaptar a função audiovisual de "IA METADE" e "BigQuery → MARKETING" (execução antiga não precisa ser copiada) |
| C05_02 | **V4 + complemento** | V4 nos setores; preservar a punchline "PARCEIRO DO GOOGLE? / AINDA NÃO" com intervenção |
| C07_02 | **V4 + complemento** | V4 para "700 MIL"; "100+ MIL HORAS" também ganha peso visual |
| C07_03 | **híbrido** | setup "voltando no tempo" + payoff 2038 do V4 com DeLorean + Marty/Doc; cena do sofá/site recuperada no payoff 2038; sem sobrecarregar os dois momentos |
| C09_01 | **V4 + ajuste** | "vocês estão aqui e contando" segue rejeitada; direção de texto: "300 episódios, 300 perguntas… / e a de hoje começa agora."; celebração do 300; sem tom de encerramento corporativo; ligação com blooper final → loop validada no Premiere |

## 2. Locks
- **FUCKING / H7 — RESOLVED / LOCKED:** censurar, preservando o tom divertido da V2 (timing cômico, bleep/SFX, reação audiovisual, intervenção visual associada). Remapear para o "fucking" da nova gravação (80,9 s). Sem cortar a fala; sem beep genérico; melhora de acabamento permitida, reinvenção da gag não.
  - Consequência no mapa: o bleep **não** caiu por mudar de posição. **C06_02: DROP_SCRIPT → MOVE.** Isso altera a contagem anterior (DROP_SCRIPT de overlays 4 → 3). Os 5 SFX DROP_SCRIPT (C01_02, C01_03, C04_02) não mudam; `SFX_BLEEP_1kHz.wav` não está entre os 74 e segue como asset do bleep.
- **GRITEM — RESOLVED / LOCKED:** freeze de ~2–3 s, para a plateia gritar. Não encurtar por ritmo.
- **Institucional — LOCKED:** PATROCÍNIO Purple Metrics · Onfly · CAFÉ OFICIAL Coffee++ · APOIADOR Kinoplex (logo branca da pasta `logos`, nunca sticker, nunca redesenhada) · REALIZAÇÃO Métricas Boss. **Onfly: logo completa, sem crop, dentro da safe area** (na V2 estava cortada).
- **Supercut `BORDAO_SUPERCUT_158_cortes.mp4` — REFERENCE_ARCHIVE / DO_NOT_INSERT_BY_DEFAULT:** só fonte de frames se necessário; não analisar agora.
- **Stickers — USER_PROVIDED:** Gabriel fez todos. Não gerar, não redesenhar (reconciliação na seção 4).

## 3. Novo: PRE_EDITED_4K_SAFETY_MASTER
- Arquivo: `…/01_VIDEO DE ABERTURA/01_BRUTOS/NOVOS TAKES-REGRAVADO/VIDEO PRE EDITADO CINEMA EP 300 EM QUALIDADE MAXIMA.mp4`
- Função: referência consolidada da edição do Gabriel (cortes, multicam, enquadramento, cor, áudio) e base segura para previews/composições. **Não** substitui o Premiere como autoridade editorial e **não** autoriza flatten da entrega final.
- Hierarquia: Premiere atual (editável) > safety master (consolidado) ; V2_PROXY = baseline criativa.
- Regra: se for preciso base consolidada, **preferir este arquivo**; nunca reconstruir cortes/multicam/cor/áudio/framing a partir dos brutos 4K. Divergência entre reconstrução automática e este arquivo → a reconstrução está errada.
- **Status: EXPORT_IN_PROGRESS.** Em 03/10 o arquivo tinha ~707 MB e crescia (index `moov` ainda ausente → não legível). **Validação pendente:** FILE_EXISTS · VIDEO_READABLE · RESOLUTION · FPS · DURATION · AUDIO_PRESENT. Sem reencodar, alterar ou gerar nova versão.

## 4. Prints/redlines já fornecidos — recuperação (somente o já documentado/entregue)
Fonte: `EP300_V4_REDLINES.md` (transcrição dos prints anotados por você) + pasta do Drive `stickers e emojis refeitos` e `300-handoff-video`. Marcações em vermelho = instruções de correção, nunca elementos de design.
**Limite honesto:** as imagens com marcação vermelha em si foram enviadas no chat; não existem como arquivos no projeto. O que existe é a transcrição de cada marcação nos redlines. Não fiz busca de acervo.

| Cue / tela | Redline | Ajuste | Status do ajuste | Asset corrigido existe? | Pronto? |
|---|---|---|---|---|---|
| C02_01 (S01) polaroid EP1 | "não usar esse take… tirar" | remover | aplicado | n/a (remoção) | SIM |
| C02_01 (S01) emoji hover | "não dar ideia de susto" | Lucian `still` | aplicado | sim (`personagens/lucian-still.webp`) | SIM |
| C03_08 (S05) | "modelo." em sticker | estilo sticker | aplicado | sim | SIM |
| C05_05 (S07) EP1 | "pose horrível" | outro frame do clipe EP1 | aplicado | sim (frame de clipe já existente, 2,0 s) | SIM |
| C05_05 (S08) | "já paga até boleto" | trocar frase | aplicado | n/a (texto) | SIM |
| C06_03 (S09) | "o certo é Toddynho" | sticker oficial | aplicado | sim (`stickers/toddynho.png`) | SIM |
| C06_05 (S10) | emojis sempre sticker | sticker | aplicado | sim | SIM |
| C00_00 cold open | "tirar esse take"; só "começou? começa de novo" + risada | corte 4,15–6,50 s | aplicado no assembly reprovado | n/a | PARCIAL (qual take foi riscado + posição = decisão editorial) |
| C00_01 contagem | "visualmente amadora" | redesenhar | aplicado (P01) | sim | SIM |
| C00_03 aviso p.1 | "vídeo final deve começar por aqui"; setas invertidas | ordem + setas | aplicado | n/a | SIM |
| C00_03 aviso p.2 | emoji cortando → sticker (🙋 😅) | sticker inteiro | aplicado | sim | SIM |
| C00_03 aviso p.1/3/4/5 | "se/você/só/vocês" maiúsculas | texto | aplicado | n/a | SIM |
| C00_03 aviso p.4 | Gustavo sorrindo/boca aberta | troca de sticker | aplicado | sim (`gustavo-hover-transicao`) | SIM |
| C00_03 aviso p.5 | trocar o balde | balde oficial | aplicado (balde A); **2 baldes na pasta (A × B)** | sim | PARCIAL — escolher A, B ou alternar |
| C00_03 pipocas soltas | — | pipocas animáveis | **assets existem:** `Sete pipocas estouradas em adesivos.png` (Drive, 02/10 22:03) — antes eu os dava como inexistentes (correção) | sim | ligar ao `PopcornBucket` (não implementado) |
| C00_02 tela do 300 | rostos repetidos; centralizar; MB realização + Kino apoiador | estrutura | aplicado (P03) | sim | SIM (reconferir Onfly sem crop) |
| C09_01 final | "vocês estão aqui e contando" sem sentido; "tela final funciona melhor" | novo texto | texto definido (§1); F01 existe | sim | texto a aplicar na implementação |
| C02_03 evolução | EP1 "melhor", EP100 "luz melhor", EP210 "sem CTA embaixo", EP153 "Gustavo em pose ruim" | 4 prints trocados | **não aplicado** | **NÃO localizados** nos arquivos entregues (só `hist/EP001_2021*.png`) | NÃO — MISSING_USER_PROVIDED_ASSET (confirmar se você já os enviou em alguma pasta) |
| C03_01 ferramentas | logo da Reportei fora do padrão | tile | não aplicado | `reportei.webp` existe no handoff (wordmark) | NÃO — falta tile/ícone no padrão |
| C04_01 bordão | mais prints, cenários diferentes, reações boas, evitar EP288 | enriquecer | não aplicado | supercut = fonte de frames (REFERENCE_ARCHIVE) | NÃO |
| C04_03 apelidos | trocar emoji lateral do Lucian se a tela ficar | emoji | não aplicado | sim (`lucian-still`) | depende de a tela ficar |
| C04_06 Pica-Pau | "novo sticker do Pica-Pau" | sticker | não aplicado | **NÃO localizado** (só `gag_picapau_silhueta.png` antigo em V2_GERADOS) | NÃO — MISSING_USER_PROVIDED_ASSET |
| C05_01 mural 191 | mais stickers/prints; EP187 banido | enriquecer | não aplicado | **stickers existem** (Guta ×3, Vitória ×3, Lucas ×3, Layla, Phill ×2, Mafê ×3, Bonel ×3) | PARCIAL — montar com o que já existe |
| C05_04 PM-RJ | trocar frame do convidado | frame EP126 | não aplicado | **NÃO localizado** | NÃO — MISSING_USER_PROVIDED_ASSET |
| C07_04 países | mais bandeiras | + bandeiras | não aplicado | só 16 desenhadas | NÃO (confirmar se você fez outras) |

**Contagem:** 25 redlines/itens documentados · **prontos 14** · **parciais 5** (cold open, balde A×B, apelidos, mural, final-texto) · **faltando 6** (evolução — 4 prints tratados como 1 item —, Reportei, bordão, Pica-Pau, PM-RJ, bandeiras). Nada foi buscado/gerado para preencher.

## 5. H1–H10 (+H11) reconciliados
| H | Tema | Estado | Base |
|---|---|---|---|
| H1 | abertura (take 42,5 s) | SUPERSEDED | Gabriel usou 42,17 s na timeline |
| H2 | países 100+ / 110+ | SUPERSEDED | fala gravada na timeline: "em mais de 100 países" |
| H3 | "de nada, Purple/Guta/Lucas" | STILL_OPEN | falta ouvir 412,3–413,6 s; Gabriel manteve a linha |
| H4 | "IA na home (fev/26)" não falado | STILL_OPEN | afeta C06_07 |
| H5 | Pica-Pau passada | SUPERSEDED | passada longa na timeline |
| H6 | fecho / improviso hard-soft skill | SUPERSEDED | 592,13–609,98 + improviso mantido |
| H7 | "fucking" | RESOLVED / LOCKED | censura divertida baseada na V2 |
| H8 | supercut | RESOLVED | REFERENCE_ARCHIVE |
| H9 | atribuição/incrementalidade (rótulo 4 em 10) | STILL_OPEN | decisão não registrada |
| H10 | dez/24 piada de autoria / "meia-culpa" | STILL_OPEN | decisão não registrada |
| H11 | Kinoplex APOIADOR | RESOLVED | logo branca da pasta, sem sticker |
**RESOLVED:** H7, H8 (+H11) · **SUPERSEDED:** H1, H2, H5, H6 · **STILL_OPEN:** H3, H4, H9, H10.
(H2 marcado SUPERSEDED por inferência da fala presente na sua edição; me corrija se a escolha era outra.)

## 6. WORD / PHRASE EMPHASIS PASS — REGISTERED / NOT EXECUTED — `REQUIRED_BEFORE_FINAL_EXECUTION`
Rever a nova fala para achar onde palavra/frase/número/punchline ganha força: ACCENT · HERO WORD · TYPO FULLSCREEN · NUMBER HERO · PUNCHLINE · CORRECTION/STRIKE/REPLACE · TEXT + STICKER · TEXT + PRINT. **Não** é animar toda fala nem virar legenda cinética; preservar ritmo e densidade da V2 e acrescentar oportunidades da nova gravação, além dos 44 cues herdados.

## 7. Por que EXECUTION_READY continua NO
1. reconciliar os redlines/prints faltando (seção 4) e os 4 H abertos (seção 5);
2. executar depois a WORD / PHRASE EMPHASIS PASS;
3. validar o PRE_EDITED_4K_SAFETY_MASTER quando terminar de exportar;
4. validar a integração final no Premiere.

---
# Rodada de fechamento (03/10/2026) — o que realmente continua humano

> Nota: o `SELF_VALIDATION_PROTOCOL` não está definido em nenhum arquivo do projeto. Apliquei o equivalente: para cada H, checar LOCKS → NON_NEGOTIABLES → redlines → baseline V2 → timeline atual → decisão humana posterior, usando só a transcrição da nova gravação (`v3-preflight/transcript_new_geral.json`) e `reports/timeline_dump.json` (nenhuma mídia processada; safety master não tocado).

## 8. Correção de status dos assets (A / B / C)
A = USER_CONFIRMED_ASSET_EXISTS / FILE_NOT_LOCATED · B = REDLINE_RECOVERED / SOURCE_IMAGE_NOT_IN_PROJECT · C = ACTUALLY_MISSING_ASSET
| Item | Status anterior | Status corrigido | Evidência |
|---|---|---|---|
| Pica-Pau novo (C04_06) | MISSING_USER_PROVIDED_ASSET | **A** | Gabriel confirmou que todos os stickers foram feitos; arquivo não localizado; NÃO gerar, NÃO usar a silhueta antiga |
| 4 frames da evolução (EP1/EP100/EP210/EP153) | MISSING | **B** (prints marcados vieram pelo chat) **+ C** (os frames substitutos não foram entregues; o redline pede "outro melhor") | nenhuma frase do Gabriel diz que os substitutos foram fornecidos |
| Frame EP126 (C05_04) | MISSING | **B + C** | idem |
| Bordão 203× (C04_01) | MISSING | **B + C-derivável** | redline recuperado; frames virão do acervo/supercut (REFERENCE_ARCHIVE), extração não feita |
| Reportei em tile (C03_01) | MISSING | **C** (só o wordmark `reportei.webp` existe) — vira A se você já fez o ícone | redline pede ícone no padrão dos tiles |
| Bandeiras extras (C07_04) | MISSING | **C** | as 16 foram desenhadas por código na V2; não há sinal de arquivo seu |
| Cold open — take riscado | — | **B** | print marcado só no chat |
Mudaram de status: Pica-Pau (agora A) e os 4 itens com B. Nenhuma busca ampla no Drive foi feita.

## 9. Redlines — 25 (contagem revisada com evidência)
**READY 16 · PARTIAL 3 · UNRESOLVED 6.** Duas linhas subiram de PARTIAL para READY: **C04_03 apelidos** (a condição "se a tela ficar" é resolvida por KEEP BY DEFAULT: a fala "mais de 60 maneiras" existe, então a tela fica e o redline "trocar emoji" vale — Lucian `still` já existe) e **C09_01 texto final** (texto definido na decisão de 03/10).
| Cue | Estado | O que falta |
|---|---|---|
| C00_00 cold open | PARTIAL | qual take foi riscado no print (imagem só no chat) e a posição no filme |
| C00_03 balde | PARTIAL | escolher qual balde: A (EPISÓDIO 300) ou B (Império), ou alternar; as 2 faces existem |
| C05_01 mural 191 | PARTIAL | só composição: os stickers existem; falta montar "sensação de multidão" (EP187 banido) |
| C02_03 evolução | UNRESOLVED | 4 frames substitutos: EP1, EP100 (luz melhor), EP210 (sem CTA), EP153 (Gustavo em boa pose); posição da pausa de 2,4 s |
| C03_01 ferramentas | UNRESOLVED | ícone/tile da Reportei no padrão dos outros |
| C04_01 bordão | UNRESOLVED | seleção dos frames (cenários diferentes, reações boas, sem EP288); fonte possível: supercut |
| C04_06 Pica-Pau | UNRESOLVED | localizar o sticker novo (A) |
| C05_04 PM-RJ | UNRESOLVED | frame novo do convidado do EP126 |
| C07_04 países | UNRESOLVED | bandeiras além das 16 |

## 10. H2 — revalidação: **STILL_OPEN** (reduzido)
Pergunta original: "100+" (roteiro/passada limpa) ou "110+" (fecho falado)? A fala não torna a questão obsoleta: a edição do Gabriel contém **os dois números falados** — "mais de 100 países" (510,4 e 512,0 s) e "mais de **110** países" (596,0–597,2 s, dentro do corte nº 98, `src 595,929–600,058`, tl ≈ 00:05:01). A parte do **overlay** é objetiva (o texto segue a fala do ponto: "100+" em C07_04), mas a contradição **audível** 100 × 110 no mesmo filme permanece e é decisão editorial/factual sua.

## 11. Os H realmente abertos
**H3 — "de nada, Purple" (C06_04)** · TC novo ≈ 00:03:27:02 · fala ASR: 412,3–414,1 "De nada, por favor. Também prevendo, né?" (antes: 409,8–411,8 "um episódio inteiro sobre o M&M").
- Pergunta original: a menção a Purple/Guta/Lucas sumiu da fala — intencional? · V2: stickers Guta/Lucas + "olha aí, de nada, viu? Purple Metrics do Guta" · V4: nada.
- Já decidido: você manteve a linha na timeline; Purple Metrics é PATROCÍNIO (lock).
- **O que falta:** o ASR escreveu "por favor", não "Purple". Só ouvindo 2 s (412,3–414,1) se resolve: se for "Purple" → ADAPT com os stickers; se não → manter os stickers Guta/Lucas com "DE NADA" sem o nome, ou DROP_SCRIPT. **STILL_OPEN (1 escuta de 2 s).**

**H4 — "IA na home do GA" (C06_07)** · TC ≈ 00:03:59:16 · fala 456,6–464,1.
- **RESOLVED** por NON_NEGOTIABLES §8 (fala sumiu = DROP_SCRIPT do elemento): "IA NA HOME DO GA" não é falado e o "fevereiro de 2026" falado refere-se ao "o que eu falei que não dava pra fazer, eu mesmo fui lá e fiz" (o lançamento do Copilot), então manter o carimbo afirmaria um fato diferente do dito. Fica: fev/26 · jun/26 · "NÃO DAVA PRA FAZER" · ACERTOU (ADAPT). *Se quiser o carimbo mesmo assim, é ordem sua, não pendência.*

**H9 — rótulo do "4 em cada 10" (C03_07)** · TC ≈ 00:01:16:08.
- **RESOLVED** por §8 + DROP_FACT: a fala diz "4 em cada 10 episódios desse ano a gente falou sobre **incrementalidade**" (214,0–218,0). O dado vale só para incrementalidade; rotular "atribuição + incrementalidade" tornaria o dado incorreto. Regra: "ATRIBUIÇÃO e INCREMENTALIDADE" como assunto (210–212) e "4 EM 10 (2026)" colado apenas em INCREMENTALIDADE. Conferir S04 na implementação.

**H10 — "meia-culpa" (C06_06)** · TC ≈ 00:03:46:19 · falas: 443,7–445,0 "na verdade, eu não disse nada." / 445,1–448,3 "Quem disse foi o Gustavo, mas aí ele pensou, e eu fiz também, né?" / 459,2–462,2 "o que eu falei que não dava pra fazer, eu fui lá e fiz".
- **RESOLVED** pelo baseline V2: a "meia-culpa" era o pill de admissão parcial; semanticamente é a frase de 445,1–448,3. A segunda ocorrência (459,2) é o beat ACERTOU de C06_07, que já tem cobertura própria. Âncora = 445,1; texto V2 "MEIA-CULPA".

**Resumo:** só **H3** (escuta de 2 s) e **H2** (100 × 110 audível) continuam com você.

## 12. Bleep
C06_02 = **MOVE** (mantido) → "fucking" ≈ 80,9 s, censura divertida da V2. `SFX_BLEEP_1kHz.wav` = **GAG_SPECIFIC_SFX / FUCKING_CENSORSHIP**, fora do inventário original; **74/74 inalterado**.

## 13. Safety master
PRE_EDITED_4K_SAFETY_MASTER = **EXPORTING** (crescendo, sem índice de leitura na última checagem). Não tocado. Validação futura só: FILE_EXISTS · READABLE · RESOLUTION · FPS · DURATION · AUDIO_PRESENT.
**EXECUTION_READY = NO.**

---
## 14. Reconciliação com o handoff do /clear (03/10/2026)
- As 26 imagens dos redlines **foram recuperadas do transcrito** e estão em `redlines_source/R01…R26`. Isso **corrige** a frase da §4 ("as imagens só existem no chat") e invalida o rótulo "B / SOURCE_IMAGE_NOT_IN_PROJECT" da §8: a fonte agora existe no projeto. Os itens continuam `C` (substitutos faltando) onde aplicável.
- O registro por imagem em `EP300_CHAT_CLEAR_HANDOFF.md` §4 **prevalece** sobre a contagem 25 (14/5/6) das §4/§9: 26 imagens → 17 RESOLVED · 8 STILL_OPEN · 1 REFERENCE_ONLY.
- Correção de rótulo: **C04_03 apelidos** e **C09_01** estavam "READY" na §9 no sentido "pronto para implementar". No registro: C09_01/R25 = RESOLVED (texto definido); C04_03/R20 = **STILL_OPEN** (solução definida, ainda não aplicada).
- C06_02 = MOVE e DROP_SCRIPT de overlays = 3 (já na §2). Os 74 SFX não mudam.
