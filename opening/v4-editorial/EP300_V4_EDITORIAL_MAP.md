# EP300 V4 — Mapa Editorial (conform sobre a gravação 4K de 30/09)

> ⚠️ **SUPERADO em 02/10/2026 (noite) pela sequência real do Gabriel no Premiere (5:15, multicam, 11 slots).** Este mapa fica só como referência de motions/assets/KEEP-ADAPT-DROP-NEW. Onde divergir, vale a timeline: ver `../EP300_V4_MOTIONS/EP300_V4_TIMELINE_MAP.md` (ex.: H5 → passada **longa** do Pica-Pau; improviso hard/soft skill mantido).

> Gerado em 2026-10-02. **Somente leitura**: nenhum `.prproj` tocado, nada renderizado, nenhum asset criado. V0–V3 intactas.
> Tempos = segundos no áudio da **CAM_GERAL 4K nova** (`MVI_9939.MP4`). ±0,3 s (ASR). Vídeo **não foi visto**: coluna CÂMERA aplica a *regra* da V2 (geral frontal por padrão; fechadas só em reação/brincadeira), não inspeção.
> Autoridade editorial = **a fala gravada**. Roteiro Notion e V3 preflight são referência. Diarização falhou (câmeras laterais captam os dois): **não atribuo falas a Gustavo/Lucian** além do que o roteiro indica; onde importa, marcado NEEDS_REVIEW.
> "V3" aqui = o remapeamento V2→nova gravação do preflight (`v3-preflight/`), **não existe V3 renderizada**. Assets vivos são os da V2.

## 1. Master e fontes

| Item | Resultado |
|---|---|
| **Master de câmera (geral)** | `01_BRUTOS/NOVOS TAKES-REGRAVADO/03_CAMERA_GERAL/MVI_9939.MP4` — 3840×2160, 23,976 fps, h264, AAC 48 kHz estéreo, **612,445 s**, mod. 30/09 18:27. Único candidato 4K de geral; a antiga (`CAM_GERAL.mp4`: 1920×1080, 30 fps, 1047 s, 28/09) **não é mais autoridade**. |
| Laterais (mesmo lote) | `MVI_9947.MP4` (Gustavo, 609,234 s) · `MVI_9967.MP4` (Lucian, 613,947 s) — 4K, 23,976 fps. |
| **Transcrição correspondente** | `v3-preflight/transcript_new.txt` + `transcript_new_geral.json` (Whisper large-v3-turbo sobre a 9939; palavras com timestamp). **ASR ≠ verdade.** Transcrição antiga (`transcript_old_v2_507-951.txt`) usada só para comparar. |
| Projeto Premiere | Drive `02_PROJETOS/ep 300 final.prproj` (14,9 KB, 02/10 19:28). Inspecionada **cópia** (scratchpad): é projeto *stub* — importa as 3 câmeras 4K novas e tem 1 sequência 4K com os 3 clipes **empilhados em t=0 (sem sync, sem corte)**; Premiere deixou transcrição "InFlight" da 9939. **Nenhuma edição perdida.** O arquivo "EP 300 - VIDEO FINAL - SYNC 4K.prproj" (atalho Recentes de 02/10 19:26) **não existe em disco** (nem no Drive nem local) — foi o save que falhou. Trabalhar em cópia **local**. |
| Roteiro | Notion "novo roteiro:" (30/09). Não bloqueia: a fala gravada manda. |
| Supercut | `BORDAO_SUPERCUT_158_cortes.mp4`: 1920×1080, 30 fps, **1002,8 s (16:43)**, 385 MB, com áudio. É compilação bruta, **não é insert pronto**. |
| Fps/resolução | Master 23,976 fps 4K; overlays V2 foram 30 fps 1080p. Ver BLOCKERS B1. |

## 2. Fala útil — EDL de diálogo V4 (passadas limpas, tempos na 9939)

A gravação é contínua com muitas retomadas. Escolha = passada limpa mais provável (texto), **última tentativa vence** quando houve "volta/de novo". Duração de fala ≈ **5:00** (V2 ≈ 7:24 de fala) + pausas P_EVOL 2,4 s e GRITEM 3 s.

| EDL | In–Out | Conteúdo | Obs. |
|---|---|---|---|
| E01 | 42.5–96.6 | "Fala aí…" · "Tá no ar, tá valendo o episódio 300" · origem 2015/Prime/MB Talks/volta/cenário antigo · "300 perguntas" · "a pergunta foi mudando" · ferramentas · "o que segue sendo realidade. Infelizmente" | Corrida contínua de ~54 s; corta em "Infelizmente" (96.5). Contém "fucking" (80.9, **passada única**). |
| E02 | 118.5–124.0 | "Aí, em 2023, o Google desligou, fez o Sunset do Universal Analytics" | Passada limpa; 100–114 travadas. |
| E03 | ≈148.0–165.0 | "Naquele ano … 153 episódios. 4 em cada 10 … GA4" · "GA4 … hoje 3 a cada 10" · "De nada, Vitória" · "Mas o que mudou … foi que entrou do lado do GA4, né?" | Início ≈148,0 (depois de "Vamos voltar de novo"). **161.5–165.0 é a ponte do roteiro ("o que mudou foi o que entrou do lado dele") — não estava mapeada no preflight.** |
| E04 | 197.7–234.0 | IA até 2021 · "antes do hype" · metade dos episódios · atribuição e incrementalidade · 4 em 10 · BigQuery · "taguear o botão" → "confiar no modelo" · "o assunto mudou, outras coisas ficaram igualzinhas" | Passada limpa de ~36 s. 165.6–169.2 ("gosto bastante") **não usar**. |
| E05 | 235.7–237.6 + 253.7–263.0 | "Mais de 200 vezes que eu falei [bordão **não falado**]" + "mais de 60 maneiras diferentes de me apresentar" · "diamante negro é um oficial, né, galera? Grita aí… Pelo amor de Deus" | **Lacuna do bordão em 237.6** — o supercut é o candidato natural para preenchê-la (H8). |
| E06 | 263.0–279.0 | Pica-Pau (curta) · "Só que as respostas quase nunca foram nossas" · "Quase 200 pessoas sentaram nessa mesa. Quase 350 vezes." | Alternativa longa em H5. Corta antes de "Mais de 140 em…" (truncado). |
| E07 | 334.8–376.6 | "De mais de 140 empresas. Banco, varejo, mídia, telecom, até o Google veio aqui… ainda não é parceiro do Google, tu acredita? Queria." · PM do RJ · ficha de presença (Phill 29, Mafê 24, Bonel 7) | **Refinamento vs. preflight** (que usava 316.5–326.5, com gagueira "de mais de 40, de mais de 140"): E06→E07 emenda limpo. |
| E08 | 390.2–426.1 | "300 vezes, de vez em quando você acerta antes" · fev/22 todinho + 27 dias · "Desculpa, Vitória…" · out/24 MMM · "De nada, [?]. Também prevendo, né?" · Meridian · MCP abr/25 → julho | 412.3–413.6 = H3 (ouvir 2 s). |
| E09 | 438.3–464.1 | dez/2024 "a gente disse que ia dar pra conversar" + piada de autoria · "Exatamente" · fev/2026 "o que eu falei que não dava pra fazer, eu mesmo fui lá e fiz" · "Analytics Copilot em junho" | 464–470 (700 mil/100 mil h) existe mas **foi dito "muito rápido" e refeito** → não usar. |
| E10 | ≈490.4–513.9 | "E do outro lado da pergunta, vocês" · 700 mil · 100 mil horas · 2038 · "mais de 100 países" | Passada refeita (mais lenta). Cortar o "você" tropeçado (~497). 514.0 ("Já ouviram o episódio…") **cortar**. |
| E11 | 516.7–534.0 | Spotify/EP 197 · "era sobre gente" · "Acredita? / Acredito, cara." | Beat de reação 532.4–534.0. |
| E12 | 592.1–607.0 *(ou 555.5–567.0)* | fecho: "300 episódios… 700 mil plays… [110 países]… pergunta pra fazer. Qual o futuro da mensuração?" · "Mas isso eu espero que a gente resolva agora. Um episódio pra pôr tudo." | H6. Precedido opcionalmente por N10 (580.9–591.0). |

Ruído de set a cortar sempre: 0–42, 111–116, 133–138, 170–175, 191–197, 433–438, 473–479, 538–546, 567–569, 576–579, 610.3 ("Foi.").

## 3. Mapa de beats (cronológico)

Legenda STATUS: **KEEP** · **ADAPT** · **DROP** (`*` = provisório, reversível) · **NEW**. Exec: PREMIERE · REMOTION · ASSET EXISTENTE · ASSET NOVO · MANUAL · BLOCKED.
V2/V3 = identificador do cue em `v2/plan.py`. Assets "existentes" = `…/00_ASSETS E INSERTS/V2_GERADOS` e repo `v2/`.

### A — CINEMA / ORIENTAÇÕES (pré-sessão, fora da 9939)

| ID | TIME | FALA / CONTEÚDO | CÂMERA | V3 (existia) | STATUS | V4 | TELA | ASSET | EXEC | OBS. |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 | pré-sessão | cold open de arquivo (bastidor 2023: "Começou mesmo?" → "Tá no ar, tá valendo") | — (arquivo) | C00_00 · SAME | KEEP | manter | FULL SCREEN | existente | PREMIERE/ASSET EXISTENTE | Não depende da nova gravação. Eco com E01 ("Tá no ar, tá valendo" falado de novo em 46.3) — ver H1. |
| A2 | pré-sessão | contagem | — | C00_01 · SAME | KEEP | manter | FULL SCREEN | existente | ASSET EXISTENTE | |
| A3 | pré-sessão | aviso para a sala (5 páginas; sem CTA digital) | — | C00_03 · SAME | KEEP | manter | FULL SCREEN+TEXT | existente | ASSET EXISTENTE | Regras cinema≠interface já aplicadas na V2. |
| A4 | pré-sessão | tela EP 300 (selo 300 + patrocinadores) | — | C00_02 · SAME | KEEP | manter estrutura V2; **sem Kinoplex** até K1 | FULL SCREEN | existente | ASSET EXISTENTE | Slot de Kinoplex: ver K1 (BLOCKED). |

### B — APRESENTAÇÃO

| ID | TIME | FALA / CONTEÚDO | CÂMERA | V3 | STATUS | V4 | TELA | ASSET | EXEC | OBS. |
|---|---|---|---|---|---|---|---|---|---|---|
| B1 | 46.3–50.1 | "Tá no ar, tá valendo o episódio 300 do Analytics Talks" | geral 4K | C01_01 adesivo 300 + confete (MEDIUM, NEEDS_HUMAN) | ADAPT | âncora do confete em "…episódio 300" (≈47.4–50.1); abertura = take **42.5** | CAMERA+MOTION (sticker) | existente C01_01 | REMOTION (re-âncora) | Take 16.6 morre em 29 ("2025", comentário de set) → **H1 resolvido pela fala**. |
| B2 | — | dados 11.526 × "acho" | — | C01_02 | DROP | — | — | — | — | Removido do roteiro e não falado. |
| B3 | — | "494 vezes de diferença" | — | C01_03 | DROP | — | — | — | — | Idem. |
| B4 | 50.2–78.3 | 2015 → Prime → MB Talks → "a volta" → podcast | geral 4K | C02_01 linha do tempo + polaroid EP1 | ADAPT | respaçar nós (~28 s de fala vs 11,6 s); polaroid EP1 mantém | INSERT (full) | existente | REMOTION (re-timing) | "a volta **do Lucian**" (regra permanente). |
| B5 | 70.9–74.8 | "voltou naquele cenário no escritório antigo… MesaCast" | geral/fechada | — | NEW | gancho opcional: frame histórico do cenário antigo | INSERT (frame) | **localizar** no arquivo oficial (busca dirigida) | MANUAL (localizar) | Opcional; sem ele, segue câmera. |

### C — O QUE MUDOU NA PAUTA

| ID | TIME | FALA / CONTEÚDO | CÂMERA | V3 | STATUS | V4 | TELA | ASSET | EXEC | OBS. |
|---|---|---|---|---|---|---|---|---|---|---|
| C1 | 78.5–84.8 | "300 episódios são mais de 300 [fucking] perguntas" | geral 4K | C02_02 chuva de perguntas | KEEP | manter | CAMERA+MOTION | existente | ASSET EXISTENTE | Palavrão: H7 (passada única). |
| C2 | 84.8–86.9 | "E a pergunta foi mudando" | geral | C02_03 | ADAPT | inserir **pausa sem voz 2,4 s** (leitura) | INSERT | existente | PREMIERE (pausa) + ASSET EXISTENTE | Mesma regra V2. |
| C3 | 86.9–96.6 | ferramentas: instalar/taguear/número não bate… "o que segue sendo realidade. Infelizmente" | geral | C03_01 logos + carimbo ATÉ HOJE | KEEP | carimbo ATÉ HOJE cai em ≈93.1 | INSERT (logos) + TEXT | existente | ASSET EXISTENTE | Improviso reforça o carimbo. |
| C4 | 118.5–124.0 | "o Google … fez o Sunset do Universal Analytics" | geral | C03_02 chave UA | KEEP | manter | INSERT | existente | ASSET EXISTENTE | "2023" falado em 118.5. |
| C5 | ≈148.0–153.0 | "153 episódios… 4 em cada 10 falavam sobre o GA4" | geral | C03_03 contador 153 | KEEP | manter | INSERT | existente | ASSET EXISTENTE | Números idênticos. |
| C6 | 153.2–159.3 | "GA4 nunca saiu da pauta… até hoje 3 a cada 10" | geral | C03_05 (1 a cada 3) | ADAPT | grade 1/3 → **3/10**; texto "3 A CADA 10" | INSERT | adaptar | REMOTION (re-render) | **Dado mudou** (F2). |
| C7 | 159.8–165.0 | "De nada, Vitória" · "Mas o que mudou… do lado do GA4, né?" | geral/fechada (reação) | C03_04 (vinha **antes** do GA4) | KEEP | **reordenar** depois de C6; ponte 161.5–165.0 sem insert | STICKER + CAMERA | existente | PREMIERE (ordem) + ASSET EXISTENTE | Única troca de ordem narrativa. |
| C8 | 165.6–169.2 | "um assunto que eu gosto **bastante**" | — | C03_06 ("gosto pouco") | DROP | descartar insert (sentido invertido); trecho fora da EDL | — | — | — | Manter contradiria a fala. |
| C9 | 197.7–225.8 | IA até 2021; "antes do hype"; metade dos episódios; atribuição e incrementalidade; **4 em 10 deste ano (incrementalidade)**; BigQuery → marketing | geral | C03_07 IA timeline (1 a cada 4) | ADAPT | "IA: **METADE**"; grade 5/10; pills **ATRIBUIÇÃO** e **INCREMENTALIDADE** (as duas são faladas em 208.9–212.2); contador **4 EM 10 (2026)** só na incrementalidade; BigQuery/MARKETING mantém | INSERT | adaptar | REMOTION (re-render) | F3/F4. **H9 resolvido pela fala.** |
| C10 | 225.9–234.0 | "taguear o botão" → "confiar no modelo" · "o assunto mudou…" | geral | C03_08 | KEEP | manter | INSERT | existente | ASSET EXISTENTE | Idêntico. |

### D — O QUE NÃO MUDOU / BRINCADEIRAS

| ID | TIME | FALA / CONTEÚDO | CÂMERA | V3 | STATUS | V4 | TELA | ASSET | EXEC | OBS. |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 | 235.7–237.6 (+ lacuna) | "Mais de 200 vezes que eu falei [bordão não falado]" | geral | C04_01 contador 203 + prints | ADAPT | contador **+200**; lacuna do bordão preenchida por trecho curto do supercut **ou** pelos prints V2 | SUPER CUT *ou* PRINT | supercut (inspecionar) / existente | REMOTION + MANUAL (seleção do trecho) | H8. "158 cortes" ≠ "+200": o contador não pode dizer 158. |
| D2 | — | "episódio de origem? — nem eu" | — | C04_02 | DROP | — | — | — | — | Não falado. |
| D3 | 253.7–257.3 | "mais de 60 maneiras diferentes de me apresentar" | geral | C04_03 (16) | ADAPT | 16 → **60+**; 4 apelidos (EP205/256/270/69) seguem como exemplos | INSERT | adaptar | REMOTION (re-render) | F6. |
| D4 | 258.1–259.5 | "diamante negro é um oficial, né, galera?" | geral | C04_04 | KEEP | manter | STICKER | existente | ASSET EXISTENTE | |
| D5 | 259.5–263.0 | "Grita aí se vocês concordam. Pelo amor de Deus." | geral | C04_05 gritem | KEEP | respiro de 3 s após a fala | INSERT/CAMERA | existente | PREMIERE (respiro) + ASSET EXISTENTE | |
| D6 | 263.0–273.6 | "24 vezes… Pica-Pau…" + "Só que as respostas quase nunca foram nossas" | geral/fechada | C04_06 silhueta + viatura | KEEP | passada curta (default) | INSERT | existente | ASSET EXISTENTE | H5: versão longa (289.3–302.3) = alternativa; **não tem a ponte**. |
| D7 | 273.8–279.0 + 334.8–337.1 | "Quase 200 pessoas… Quase 350 vezes… de mais de 140 empresas" | geral | C05_01 mural (191/348/140) | ADAPT | **quase 200 / quase 350 / 140+** (3 contadores) | INSERT | adaptar | REMOTION (re-render) | F7. Emenda 279.0→334.8 é refinamento V4. |
| D8 | 337.1–345.0 | "Banco, varejo, mídia, telecom, até o Google veio aqui… não é parceiro do Google" | geral | C05_02 setores/Google | KEEP | manter | INSERT | existente | ASSET EXISTENTE | "Meta" do roteiro não é falada (nem na V2): nada a fazer. |
| D9 | 345.0–346.5 | "…tu acredita? **Queria.**" | fechada (ver vídeo) | C05_03 chorando "Eu queria / Também queria" | ADAPT | **um** sticker só; quem falou: NEEDS_REVIEW (diarização falhou) | STICKER | existente | ASSET EXISTENTE | |
| D10 | 346.7–354.4 | "O Pica-Pau não chamou a polícia, mas nós chamamos… PM do RJ" | geral | C05_04 | KEEP | manter | INSERT | existente | ASSET EXISTENTE | |
| D11 | 354.6–376.6 | ficha de presença: Phill 29, Mafê 24 (ep. 1), Bonel 7 · "enchendo o nosso saco… até pra dar boleto" | geral/fechada | C05_05 ficha | KEEP | manter | INSERT | existente | ASSET EXISTENTE | Números iguais. |

### E — "A GENTE ACERTA ANTES"

| ID | TIME | FALA / CONTEÚDO | CÂMERA | V3 | STATUS | V4 | TELA | ASSET | EXEC | OBS. |
|---|---|---|---|---|---|---|---|---|---|---|
| E1 | 390.2–393.5 | "quando você pergunta algo 300 vezes, de vez em quando você acerta antes" | geral | C06_01 | KEEP | manter | INSERT | existente | ASSET EXISTENTE | |
| E2 | — | bleep do palavrão do Lucian | — | C06_02 | DROP | — | — | — | — | Sem palavrão equivalente neste ponto. |
| E3 | 393.5–411.8 | fev/2022 todinho + 27 dias · "Desculpa, Vitória…" · out/2024 MMM | geral/fechada | C06_03 toddynho + pills | KEEP | manter | INSERT + STICKER | existente | ASSET EXISTENTE | |
| E4 | 412.3–413.6 | "De nada, [?]. Também prevendo, né?" | — | C06_04 "de nada, Purple" + Guta/Lucas | DROP* | provisório: sem stickers Guta/Lucas | — | — | — | **NEEDS_LISTEN 2 s.** Re-ASR direcionada: "De nada, por favor. Também… prevendo, né?" (antes: "Purple Match do Guta"). Se for "Purple", vira ADAPT. |
| E5 | 414.3–426.1 | Meridian +3 meses · MCP abr/25 → julho · "do outro ano, tá?" | geral | C06_05 | ADAPT | **remover** pill/sticker Layla ("viu, Layla?" não falado); manter MCP/jul | INSERT | adaptar | REMOTION (re-render) | |
| E6 | 438.3–448.9 | dez/2024 "a gente disse que ia dar pra conversar" + piada de autoria ("na verdade eu não disse nada. Quem disse foi o Gustavo, mas aí ele pensou, e eu fiz também") | geral/fechada | C06_06 "meia-culpa" | ADAPT | a "meia-culpa" **é a piada** (não é beat separado); rótulo dez/24 revisado; gag gráfica opcional | INSERT + TEXT | adaptar | REMOTION | H10. Quem diz cada frase: NEEDS_REVIEW. |
| E7 | 456.6–464.1 | fev/2026 "o que eu falei que não dava pra fazer, eu mesmo fui lá e fiz" · Copilot em junho | geral | C06_07 fev26 IA na home + jun26 | ADAPT | "IMPOSSÍVEL" → **"não dava pra fazer"**; **sem** carimbo "IA NA HOME DO GA" (não falado) salvo confirmação | INSERT + TEXT | adaptar | REMOTION | H4. Fev/26 na fala = o que *ele fez*, não "GA colocou IA na home". |

### F — VOCÊS (audiência)

| ID | TIME | FALA / CONTEÚDO | CÂMERA | V3 | STATUS | V4 | TELA | ASSET | EXEC | OBS. |
|---|---|---|---|---|---|---|---|---|---|---|
| F1 | ≈490.4–497.5 | "E do outro lado da pergunta, vocês" | geral | C07_01 | KEEP | manter | INSERT | existente | ASSET EXISTENTE | |
| F2 | 497.5–502.4 | "700 mil" · "mais de 100 mil horas ouvidas" | geral | C07_02 (106 mil h) | ADAPT | 106 → **100+ mil h** | INSERT | adaptar | REMOTION (re-render) | F8. |
| F3 | 502.7–510.2 | "terminaria em 2038" | geral | C07_03 | KEEP | manter | INSERT | existente | ASSET EXISTENTE | |
| F4 | 510.4–513.9 | "em mais de 100 países" | geral | C07_04 (110) | ADAPT | **+100** (verdadeiro nos dois casos) | INSERT | adaptar | REMOTION (re-render) | H2 dissolve: gráfico "+100" é seguro; ver H2/H6. |
| F5 | 516.7–527.3 | episódio mais ouvido no Spotify: 197 | geral | C07_05 | KEEP | manter; "NO SPOTIFY" opcional | INSERT | existente | ASSET EXISTENTE | |
| F6 | 527.5–531.8 | "era sobre gente" | geral | C07_06 | KEEP | manter | INSERT | existente | ASSET EXISTENTE | |
| F7 | 532.4–534.0 | "Acredita? / Acredito, cara." | **lateral/aberta** (reação) | — | NEW | beat de reação **sem insert** | CAMERA | — | PREMIERE | Corte de câmera apenas. |

### G — FECHAMENTO

| ID | TIME | FALA / CONTEÚDO | CÂMERA | V3 | STATUS | V4 | TELA | ASSET | EXEC | OBS. |
|---|---|---|---|---|---|---|---|---|---|---|
| G1 | 580.9–591.0 *(ou 547.1–555.0)* | "a galera ainda acha que isso é hard/soft skill… as empresas são feitas de pessoas" | geral/fechada | — | NEW | opcional (~8–10 s); sem insert; corte editorial | CAMERA | — | PREMIERE | Forte editorialmente; ASR ambíguo (hard × soft) → **ouvir antes de decidir**. H6. |
| G2 | 592.1–603.6 | "300 episódios… mais de 700 mil plays… [110 países]… Qual o futuro da mensuração?" | geral | C08_01 título (preflight: ADAPT) | ADAPT | título entra **após "…futuro da mensuração"** (casa com o título do episódio); tempo recalculado | FULL SCREEN (título) | existente | REMOTION (re-âncora) | H6. Passada 555.5 aborta em 567 ("tá") — a de 592 é a última. |
| G3 | 603.6–607.0 | "Mas isso eu espero que a gente resolva agora. Um episódio pra pôr tudo." | geral | — | NEW | ponte para o episódio, antes do título | CAMERA | — | PREMIERE | Fora do roteiro. |
| G4 | pós-fala | 300 comemorado → vira lockup do loop | — | C09_01 | KEEP | recalcular início (após G3) | FULL SCREEN | existente (`final_v2`) | REMOTION (re-âncora) | Slot de Kinoplex: K1 (BLOCKED). |

### K — Kinoplex (sem posição)

| ID | TIME | FALA / CONTEÚDO | CÂMERA | V3 | STATUS | V4 | TELA | ASSET | EXEC | OBS. |
|---|---|---|---|---|---|---|---|---|---|---|
| K1 | **indefinido** | — | — | exploração V3 (histórica) | NEW | **não presumir** posição, rótulo, tratamento nem agrupamento | ? | **oficial pendente** (Cláudio Miranda / site-handoff) | BLOCKED | FATO: apoiador oficial do EP300. Sem logo em sticker, sem redesenho/estilização, sem rótulo até receber o design. |

## 4. H1–H10 reavaliados contra a gravação nova

Vocabulário: **RESOLVIDO PELA FALA** (a gravação decide) · **ESTREITADO** (a pergunta mudou/ficou menor) · **OUVIR** (checagem de poucos segundos) · **ESCOLHA HUMANA**.

| H | Antes | Agora | Evidência (9939) | Ação |
|---|---|---|---|---|
| H1 abertura | NEEDS_RECHECK | **RESOLVIDO PELA FALA** (confirmar) | Take 16.6 morre em 29 s (diz "2025", comentário de set). Só o take 42.5 corre contínuo até "300 episódios" (76.9). Sobra micro-escolha: eco "Tá no ar, tá valendo" com o cold open (A1). | Usar 42.5. Não bloqueia. |
| H2 países | STILL_RELEVANT | **ESTREITADO** | Falado 100 (510.4, 512.0) e 110 (485.6, 596.0). Gráfico "+100" é verdadeiro nos dois casos; o fecho de 592 diz "110" (se usado). | "+100" no corpo; decidir G2 (H6). Checar o número real só se quiserem "110". |
| H3 Purple/Guta/Lucas | STILL_RELEVANT | **OUVIR** | Re-ASR direcionada de 404–416: "De nada, por favor. Também… prevendo, né?" (V2: "de nada, viu? Purple Match do Guta"). Pode ser "Purple" abreviado. | Ouvir 412.3–413.6. DROP* até lá. |
| H4 IA-home/fev26 | STILL_RELEVANT | **ESTREITADO** | Fala liga fev/2026 a "o que eu falei que não dava pra fazer, eu fui lá e fiz" — não a "GA colocou IA na home". | Sem carimbo "IA NA HOME DO GA" salvo confirmação de fato. |
| H5 Pica-Pau | NEEDS_RECHECK | **ESCOLHA HUMANA** (concreta) | Curta 263.0–273.6 traz a ponte "Só que as respostas quase nunca foram nossas". Longa 289.3–302.3 tem a piada ("ninguém sabe essa referência") mas **não tem a ponte** → exigiria splice com 270.9–273.8. | Default curta. |
| H6 fecho | NEEDS_RECHECK | **ESCOLHA HUMANA** | 555.5 aborta em 567 ("tá") e reinicia; 592.1 é a última tentativa e traz "resolva agora / pra pôr tudo" **e** "110 países". "hard/soft skill" ocorre duas vezes (547 e 581), ASR contraditório. | Default 592–607; ouvir G1 antes de manter/cortar. |
| H7 palavrão | STILL_RELEVANT | **ESTREITADO** | "fucking" (80.9) tem **passada única** — não há "outra passada". Outros palavrões (29.5, 475.5) estão fora da EDL. | Bleep × deixar × dip de áudio. |
| H8 supercut | STILL_RELEVANT | **ESTREITADO** | Supercut = 16:43, 1080p30 — compilação, não insert. A fala "Mais de 200 vezes que eu falei…" deixa **lacuna do bordão** (237.6) que ele pode preencher. | Escolher trecho curto (≈3–4 s) ou manter prints. Ver o arquivo (não inspecionado visualmente). |
| H9 atribuição/increm. | STILL_RELEVANT | **RESOLVIDO PELA FALA** | Falado: "E atribuição e incrementalidade viraram um assunto" (208.9–212.2) e "4 em cada 10 … falamos sobre incrementalidade" (214–216). | Duas pills; contador 4/10 só na incrementalidade. |
| H10 dez/24 | STILL_RELEVANT | **ESTREITADO** | A "meia-culpa" separada acabou: a piada de autoria é o beat. Estrutura falada: dez/24 → piada → "Exatamente" → fev/26 "eu fui lá e fiz" → Copilot jun. | Gag gráfica opcional; sem atribuição por nome na tela sem confirmar quem fala. |

Resultado: **2 resolvidos pela fala (H1, H9) · 5 estreitados (H2, H4, H7, H8, H10) · 1 ouvir (H3) · 2 escolha humana (H5, H6)**. Nenhum bloqueia.

## 5. Contagem de beats

49 beats: **KEEP 23 · ADAPT 15 · DROP 6 · NEW 5** (detalhe em `EP300_V3_TO_V4_DELTA.md`).

## 6. Limites desta análise

- Vídeo novo não foi visto: nada sobre enquadramento, leitura de teleprompter, foco ou exposição; câmeras = regra, não decisão.
- Passadas escolhidas por texto (ASR com erros: "Luciano", "Popilot", "Pobarino", "a 4"). Tempos ±0,3 s; refinar no Premiere.
- Diarização falhou; atribuição de falas = ordem do roteiro, não verificada.
- Sync entre câmeras não medido (stub do Premiere está empilhado em 0).
- Thumb (feedback Lucian) e Kinoplex: ver BLOCKERS.
