# EP300 V3 — Pré-flight (remapeamento da V2 sobre a regravação de 30/09)

> Gerado em 2026-10-01. **Nada foi editado, renderizado ou criado como asset.** V2 intacta. Só leitura de Drive/Notion + transcrição local.
> Tempos "NEW" = segundos no áudio da **CAM_GERAL nova** (`MVI_9939.MP4`, 610 s). Tempos "OLD" = timeline da CAM_GERAL antiga (como em `v2/plan.py`).
> Fontes: transcrição nova `transcript_new.txt` (Whisper large-v3-turbo, **ASR ≠ verdade**), transcrição V2 `transcript_old_v2_507-951.txt`, `v2/plan.py`, roteiro Notion `roteiro_novo_notion_2026-09-30.txt`.

## 1. Fontes (status)

| | Item | Status |
|---|---|---|
| NEW | 3 câmeras: `…/01_BRUTOS/NOVOS TAKES-REGRAVADO/` → `03_CAMERA_GERAL/MVI_9939.MP4` (612,4 s), `01_CAMERA-GUSTAVO/MVI_9947.MP4` (609,2 s), `02_CAMERA-LUCIAN/MVI_9967.MP4` (613,9 s); h264, **23,976 fps**, AAC 48 kHz estéreo, ~9 GB cada | FOUND (vídeo não inspecionado) |
| NEW | Roteiro atualizado: Notion "Texto corrido para teleprompter — EP 300" (editado 30/09 20:56Z); a página guarda 3 versões — a **mais nova** é o bloco "novo roteiro:" no topo | FOUND |
| NEW | Áudio de mesa/lapela separado da regravação | MISSING (só o áudio embutido nas câmeras; a geral foi a fonte de diálogo na V2) |
| OLD | XML/timeline V2, `timeline_v2.json`, `plan.py`, 44 overlays alpha, `V2_GERADOS` (assets, stickers, logos), áudio (trilhas/SFX/stems), proxy 6:10, loop V2 | FOUND (Drive `02_PROJETOS/EP300_ABERTURA_V2`, repo `v2/`) |
| OLD | Handoff Lucian (`EP300_HANDOFF_LUCIAN`) com manifest | FOUND (não aberto — não necessário hoje) |
| NEW? | `BORDAO_SUPERCUT_158_cortes.mp4` (385 MB, 30/09 14:59) na raiz do EP300 — **asset novo, não inspecionado** | FOUND |

## 2. Nova transcrição
Feita: `transcript_new.txt` / `transcript_new_geral.json` (palavras com timestamps), 274 segmentos. **Identificação Gustavo/Lucian: FALHOU** — as câmeras laterais captam os dois; razão de energia não separou. Atribuição abaixo = ordem do roteiro. Mapeamento da fala nova: ~0–42 s chat de operação/slate/erros; takes úteis a partir de ~42 s; **o material é uma gravação contínua com muitas retomadas** ("volta um pouquinho"), então para cada trecho há 1–4 passadas — o mapa aponta a passada **limpa mais provável**, não definitiva.

## 3. Alinhamento semântico OLD ↔ NEW (resumo)
Roteiro: 11 mil/acho/494 **saiu**; nenhum bloco do roteiro novo ficou sem fala, exceto "o GA colocou IA na home" e "Meta". Mudanças de **dado**: 9 (seção 9). Contagem do mapa (40 decisões): **KEEP 19 · ADAPT 15 · REMOVE 6**; classes: SAME 3 · MOVED 16 · MODIFIED 16 · REMOVED 5 · NEW 14 (seção 7).
A ordem narrativa é a mesma da V2, com 2 exceções: (a) "de nada, Vitória" agora vem **depois** do "3 a cada 10" do GA4; (b) abertura e fecho foram reescritos.

## 4–5. Decision Map
Legenda judges: **E**ditorial · **C**ontinuidade · **F**ato · **V**isual (OK/WARN/FAIL). NEEDS_HUMAN onde há conflito. Detalhe estruturado: `decision_map.json`.

| ID | OLD tc | OLD fala/ideia | NEW tc | NEW fala/ideia | STATUS | ASSET | CHANGE | CONF | JUDGES | REASON |
|---|---|---|---|---|---|---|---|---|---|---|
| C00_00-03 | pré-sessão | cold open arquivo + contagem + aviso + tela EP300 | — | — | **KEEP** (SAME) | C00_00/01/03/02 V2 | nenhuma | HIGH | E:OK C:OK F:OK V:OK | Independe da nova gravação. Atenção: cold open termina em 'Tá no ar, tá valendo' e a nova abertura também diz isso (H1). |
| C01_01 | 512.9 | 'episódio especial de número 300' → adesivo 300 + confete | 16.6–21.5 (c/ 'Luciano') ou 42.5–50.1 ('Tá no ar… episódio 300') | abertura reescrita: 1ª passada com erro (12.7); a limpa (42.5) não diz 'Bem-vindos… especial' | **ADAPT** (MODIFIED) | C01_01 | ancorar confete em '…episódio 300' (46.3–50.1) ou 'número 300' (21.0) | MEDIUM | E:WARN C:OK F:OK V:OK · **NEEDS_HUMAN** | Duas aberturas possíveis; escolha editorial (H1). |
| C01_02 | 522.7 | 'dados 11.526 vezes; acho' | — | bloco removido do roteiro e não falado | **REMOVE** (REMOVED) | C01_02 | nenhuma | HIGH | E:OK C:WARN F:OK V:OK | Roteiro novo não tem dados/acho; nada falado. |
| C01_03 | 532.3 | '494 vezes de diferença' | — | removido | **REMOVE** (REMOVED) | C01_03 | nenhuma | HIGH | E:OK C:OK F:OK V:OK | Idem. |
| C02_01 | 544.8 | 2015 → Prime → MB Talks → 'a volta' → podcast | 50.2–78.3 | mesma ideia, mais longa e improvisada (escritório antigo, MesaCast, 'ali da galera') | **ADAPT** (MODIFIED) | C02_01 (nós 2015/PRIME/MB TALKS/A VOLTA/PODCAST) | reespaçar nós (~28 s de fala vs 11.6 s); polaroid EP1 mantém | MEDIUM | E:OK C:OK F:OK V:WARN | Rótulos continuam válidos; só o ritmo muda. 'Cenário antigo' é gancho opcional (N11). |
| C02_02 | 558.7 | '300 episódios são mais de 300 perguntas' | 78.5–84.8 | falado com 'fucking' (improviso) | **KEEP** (MOVED) | C02_02 | — | HIGH | E:OK C:OK F:OK V:OK · **NEEDS_HUMAN** | 'fucking' decide-se em H7. |
| C02_03 | 562.6 | 'E a pergunta foi mudando' | 84.8–86.9 | mesma frase, emendada em 'No começo…' | **ADAPT** (MOVED) | C02_03 | pausa sem voz de 2,4 s precisa ser inserida | HIGH | E:OK C:OK F:OK V:OK | Mesma regra V2: pausa de leitura. |
| C03_01 | 570.75 | 'No começo… ferramenta; instalar/taguear/número não bate' | 86.9–94.5 (+96.2) | acrescentou 'o que segue sendo realidade. Infelizmente' | **KEEP** (MOVED) | C03_01 | carimbo ATÉ HOJE cai em 'o que segue sendo realidade' (~93.1) | HIGH | E:OK C:OK F:OK V:OK | Improviso reforça o carimbo. |
| C03_02 | 583.35 | 'em 2023 o Google desligou o Universal' | 118.5–124.0 | 'fez o Sunset do Universal Analytics' (texto diferente, ideia igual) | **KEEP** (MODIFIED) | C03_02 | — | HIGH | E:OK C:OK F:OK V:OK | Passada limpa; as de 100–114 têm travadas. |
| C03_03 | 589.75 | '153 episódios… 4 em 10 GA4' | 146.9–153.0 (limpa) | 'Naquele ano a gente publicou 153 episódios. 4 em cada 10 falavam sobre o GA4.' | **KEEP** (SAME) | C03_03 | — | HIGH | E:OK C:OK F:OK V:OK | Números idênticos. |
| C03_05 | 623.4 | 'GA4 nunca saiu da pauta — 1 a cada 3' | 153.2–159.3 | 'até hoje tá em 3 a cada 10 episódios' | **ADAPT** (MODIFIED) | C03_05 | grade 1/3 → 3/10; texto '1 A CADA 3 EPISÓDIOS' → '3 A CADA 10' | HIGH | E:OK C:OK F:FAIL V:FAIL | Dado mudou; texto/grade antigos ficam errados. |
| C03_04 | 620.3 | 'de nada, Vitória' | 159.8–161.2 | mesma piada, mas agora DEPOIS do GA4 (ordem trocada) | **KEEP** (MOVED) | C03_04 | reordenar: C03_05 antes de C03_04 | MEDIUM | E:OK C:OK F:OK V:OK | No V2 vinha antes; piada continua legível. |
| C03_06 | 633.4 | 'é um tema que eu gosto pouco' (IA) | 165.6–169.2 / 177.9 | 'um assunto que eu gosto bastante / tenho bastante interesse' | **REMOVE** (MODIFIED) | C03_06 | descartar insert (sentido invertido) | HIGH | E:FAIL C:WARN F:FAIL V:FAIL | Manter contradiria a fala. |
| C03_07 | 637.1 | IA fora da pauta até 2021; 1 a cada 4; atribuição/incrementalidade; BigQuery | 197.7–225.8 (limpa) | IA 'metade dos episódios'; incrementalidade '4 em cada 10 deste ano'; BigQuery → marketing; improviso 'antes do hype' | **ADAPT** (MODIFIED) | C03_07 | 'IA: 1 A CADA 4' → 'METADE'; grade c/ 5/10; pills atribuição/incrementalidade + '4 EM 10 (2026)'; BigQuery/MARKETING mantém | MEDIUM | E:OK C:OK F:FAIL V:WARN · **NEEDS_HUMAN** | Dado mudou; falado só cita 'incrementalidade' nos 4/10 (H9). |
| C03_08 | 652.6 | taguear botão → confiar no modelo | 225.9–231.7 | idêntico | **KEEP** (SAME) | C03_08 | — | HIGH | E:OK C:OK F:OK V:OK | — |
| C04_01 | 669.3 | '203 vezes… fala aí, analítica' | 235.7–237.6 | 'Mais de 200 vezes que eu falei' (bordão não repetido aqui) | **ADAPT** (MODIFIED) | C04_01 (+ BORDAO_SUPERCUT_158_cortes.mp4, novo no Drive, não inspecionado) | contador 203 → '+200' | MEDIUM | E:OK C:OK F:FAIL V:WARN · **NEEDS_HUMAN** | Existe supercut novo de 158 cortes; usar ou não (H8). |
| C04_02 | 675.1 | 'episódio de origem? — nem eu' | — | não falado | **REMOVE** (REMOVED) | C04_02 | nenhuma | HIGH | E:OK C:OK F:OK V:OK | Improviso antigo sem equivalente. |
| C04_03 | 679.9 | '16 maneiras de me apresentar' | 253.7–257.3 (limpa) | 'mais de 60 maneiras diferentes' | **ADAPT** (MODIFIED) | C04_03 | 16 → '60+'; 4 apelidos (EP205/256/270/69) seguem como exemplos | HIGH | E:OK C:OK F:FAIL V:WARN | Dado mudou. |
| C04_04 | 686.6 | 'diamante negro é oficial' | 258.1–259.5 | 'Mas, diamante negro é um oficial, né, galera?' | **KEEP** (MOVED) | C04_04 | — | HIGH | E:OK C:OK F:OK V:OK | — |
| C04_05 | 689.6 | 'Grita aí se vocês concordam' (improviso) | 259.5–262.96 | idêntico, + 'Pelo amor de Deus' | **KEEP** (MOVED) | C04_05 | respiro de 3 s após 'Pelo amor de Deus' | HIGH | E:OK C:OK F:OK V:OK | Improviso se repetiu. |
| C04_06 | 690.45 | '24 vezes… Pica-Pau' | 262.96–270.7 (curta) / 289.3–302.3 (com improviso) | idêntico; retake acrescenta 'ninguém sabe essa referência' | **KEEP** (MOVED) | C04_06 | versão longa casa com o pill 'tem gente que nem sabe a referência' | HIGH | E:OK C:OK F:OK V:OK · **NEEDS_HUMAN** | Qual passada usar (H5). |
| C05_01 | 701.1 | '191 pessoas… 348 vezes… 140 empresas' | 316.5–326.5 (limpa) | 'quase 200 pessoas… quase 350 vezes… mais de 140 empresas' | **ADAPT** (MODIFIED) | C05_01 (counters + n2/n3) | 191 → 'quase 200'; 348 → 'quase 350'; 140+ mantém | HIGH | E:OK C:OK F:FAIL V:FAIL | Dado mudou (arredondado). |
| C05_02 | 756.55 | 'banco, varejo, mídia, telecom, Google; não é parceiro' | 334.8–346.5 | idêntico (improviso 'tu acredita? Queria.') | **KEEP** (MOVED) | C05_02 | — | HIGH | E:OK C:OK F:OK V:OK | Meta está no roteiro mas não foi falada (nem no V2). |
| C05_03 | 763.0 | 'Eu queria. / Também queria.' | 345.7–346.5 | só um 'Queria.' | **ADAPT** (MODIFIED) | C05_03 | um adesivo só (quem falou: conferir no vídeo) | MEDIUM | E:OK C:OK F:OK V:WARN | Locutor não confirmado (diarização falhou). |
| C05_04 | 764.9 | 'nós chamamos… PM do RJ' | 346.7–354.4 | idêntico | **KEEP** (MOVED) | C05_04 | — | HIGH | E:OK C:OK F:OK V:OK | — |
| C05_05 | 773.3 | ficha: Phill 29, Mafê 24, Bonel 7 | 354.6–376.6 | idêntico; improviso 'enchendo o nosso saco… até pra dar boleto' | **KEEP** (MOVED) | C05_05 | — | HIGH | E:OK C:OK F:OK V:OK | Números iguais. |
| C06_01 | 859.75 | 'de vez em quando você acerta antes' | 390.2–393.5 (limpa) | idêntico | **KEEP** (MOVED) | C06_01 | — | HIGH | E:OK C:OK F:OK V:OK | — |
| C06_02 | 861.15 | bleep do palavrão do Lucian | — | sem palavrão equivalente no ponto | **REMOVE** (REMOVED) | C06_02 | nenhuma | HIGH | E:OK C:OK F:OK V:OK | Ver 'fucking' (H7). |
| C06_03 | 862.4 | fev/2022 toddynho + 27 dias; out/2024 MMM | 393.5–411.8 | idêntico; 'todinho gelado'; 'desculpa, Vitória' também falado | **KEEP** (MOVED) | C06_03 | — | HIGH | E:OK C:OK F:OK V:OK | Piada Vitória repetiu. |
| C06_04 | 877.25 | 'de nada, Purple (Guta/Lucas)' | — | não falado | **REMOVE** (REMOVED) | C06_04 | não usar stickers Guta/Lucas | MEDIUM | E:WARN C:OK F:OK V:OK · **NEEDS_HUMAN** | Menção ao patrocinador sumiu — intencional? (H3). |
| C06_05 | 880.65 | Meridian +3 meses 'viu, Laila?'; MCP abr/25 → jul/25; dez/24 | 414.3–426.1 (Meridian/MCP); 438.3–448.3 (dez/24) | sem 'viu, Layla?'; 'do outro ano, tá? Que fique claro'; dez/24 virou piada de atribuição | **ADAPT** (MODIFIED) | C06_05 | remover pill/sticker Layla; manter MCP/jul; revisar rótulo dez/24 | MEDIUM | E:OK C:OK F:OK V:WARN | Layla não é mencionada. |
| C06_06 | 901.2 | 'meia-culpa' | 443.7–448.3 / 459.2–462.2 | 'quem disse foi o Gustavo, mas eu fiz também' e 'o que eu falei que não dava pra fazer, eu fui lá e fiz' | **ADAPT** (MODIFIED) | C06_06 | mover para 459.2 (ou 443.7) | MEDIUM | E:OK C:OK F:OK V:WARN · **NEEDS_HUMAN** | H10. |
| C06_07 | 904.3 | fev/26 IA na home do GA; jun/26 Copilot; 'impossível' | 456.6–464.1 | falado: fev 2026 … 'eu fui lá e fiz' … Copilot em junho; 'IA na home do GA' NÃO falado | **ADAPT** (MODIFIED) | C06_07 | 'IMPOSSÍVEL' → 'não dava pra fazer'; carimbo 'IA NA HOME DO GA' sem respaldo na fala | MEDIUM | E:OK C:OK F:WARN V:WARN · **NEEDS_HUMAN** | H4. |
| C07_01 | 914.7 | 'do outro lado da pergunta: vocês' | 491.5–497.5 (limpa) | idêntico (várias retomadas 464–497) | **KEEP** (MOVED) | C07_01 | — | HIGH | E:OK C:OK F:OK V:OK | — |
| C07_02 | 915.85 | '700 mil… 106 mil horas' | 497.5–502.4 | '700 mil' igual; 'mais de 100 mil horas' | **ADAPT** (MODIFIED) | C07_02 | 106 mil h → '100+ mil h' | HIGH | E:OK C:OK F:FAIL V:FAIL | Dado mudou. |
| C07_03 | 922.1 | 'terminaria em 2038' | 502.7–510.2 | idêntico | **KEEP** (MOVED) | C07_03 | — | HIGH | E:OK C:OK F:OK V:OK | — |
| C07_04 | 928.85 | 'Em 110 países' | 510.4–513.9 ('mais de 100'); 596.0 ('mais de 110') | passada limpa diz 100; fechamento diz 110 | **ADAPT** (MODIFIED) | C07_04 | '110' → '100+' (roteiro) — conflito entre passadas | MEDIUM | E:OK C:OK F:FAIL V:FAIL · **NEEDS_HUMAN** | H2. |
| C07_05 | 933.7 | 'episódio 197 mais ouvido' | 516.7–527.3 | idêntico + 'no Spotify' | **KEEP** (MOVED) | C07_05 | opcional: 'NO SPOTIFY' | HIGH | E:OK C:OK F:OK V:OK | — |
| C07_06 | 941.7 | 'era sobre gente' | 527.5–531.8 | idêntico | **KEEP** (MOVED) | C07_06 | — | HIGH | E:OK C:OK F:OK V:OK | — |
| C08/C09 | 951.9 | fim → título → final 300/loop | 555.5–565.7 (limpa) ou 592.1–602.2 | fecho NOVO: 'Qual o futuro da mensuração?' + improviso 'hard/soft skill… empresas são feitas de pessoas' + 'resolva agora' | **ADAPT** (MODIFIED) | C08_01, C09_01 | título entra após 'futuro da mensuração' (casa com o título do episódio); recalcular tempo | MEDIUM | E:OK C:OK F:OK V:OK · **NEEDS_HUMAN** | H6. |

## 6. Judges — resultado
Conflitos reais (FAIL) concentram-se em **Fato/Visual** — são todos "dado mudou" (seção 9) ou "sentido invertido" (`C03_06`). Nenhum FAIL de Continuidade: a linguagem V2 se aplica sem mudança. WARN editoriais: abertura (H1), patrocinador Purple (H3).

## 7. NEW FREESTYLE MOMENTS
| # | NEW tc | Quem (pelo roteiro) | Fala (ASR) | Diferença vs roteiro | Impacto | Sugestão |
|---|---|---|---|---|---|---|
| N1 | 93.1–96.6 | Gustavo | "o que segue sendo realidade. Infelizmente" | acréscimo | reforça carimbo ATÉ HOJE | KEEP |
| N2 | 202–204 | Lucian | "então a gente começou inclusive a falar antes do hype, tá?" | acréscimo | pode acompanhar C03_07 (nó 'ATÉ 2021') | KEEP |
| N3 | 289–303 | Gustavo/Lucian | "o problema continua… não é que estão chamando a polícia… ninguém sabe essa referência" | retake improvisado | casa com pill existente | REVIEW (H5) |
| N4 | 337–346 | Lucian/Gustavo | "até o Google veio aqui… a gente ainda não é parceiro do Google, tu acredita? Queria." | igual ao V2 | mantém C05_02/03 | KEEP |
| N5 | 370–376 | Gustavo | "enchendo o nosso saco… até pra dar boleto" | acréscimo | sem insert | KEEP |
| N6 | 405.9–409.4 | — | "Desculpa, Vitória, mas a gente continua produzindo conteúdo" | igual ao V2 (pill 'desculpa, Vi.') | mantém | KEEP |
| N7 | 443.7–448.3 | Lucian | "na verdade eu não disse nada. Quem disse foi o Gustavo, mas…" | dez/2024 virou piada de atribuição | ver C06_05/06 | REVIEW (H10) |
| N8 | 513.96 | — | "Já ouviram o episódio nosso da Analytics Talks?" | acréscimo | quebra fluxo | CUT |
| N9 | 532.4–534.0 | Gustavo/Lucian | "Acredita? / Acredito, cara." | acréscimo | beat de reação (câmera lateral/aberta) | KEEP |
| N10 | 547–555 e 580–591 | Lucian/Gustavo | "a galera ainda acha que a hard skill é ferramenta… as empresas são feitas de pessoas" | NOVO (fora do roteiro) | forte editorialmente; ocupa ~8 s antes do fecho | REVIEW (H6) |
| N11 | 70–77 | Lucian | "voltou naquele cenário no escritório antigo… MesaCast" | acréscimo | gancho p/ frames históricos de cenário | REVIEW |
| N12 | 80.9 | Gustavo | "mais de 300 fucking perguntas" | palavrão | bleep ou escolher outra passada | REVIEW (H7) |
| N13 | 603.5–606.9 | Gustavo | "Mas isso eu espero que a gente resolva agora. Um episódio pra por tudo." | NOVO | ponte para o episódio | REVIEW (H6) |
| N14 | 0–42, 111–116, 133–138, 170–175, 191–197, 433–438, 473–479, 538–546, 567–569, 576–579 | — | slate, "volta", "bota aí, Gabriel", comentários de operação | ruído de set | — | CUT |

## 8. INSERT REMAP
| Insert V2 | Função | Novo momento semântico | STATUS |
|---|---|---|---|
| C01_01 adesivo 300 | festejar o 300 | "episódio 300" (46–50 ou 21) | ADAPT |
| C01_02 / C01_03 | dados × acho | — | DROP |
| C02_01 linha do tempo | origem do programa | 50–78 | ADAPT (respacejar) |
| C02_02 chuva de perguntas | "300 perguntas" | 78–85 | REUSE |
| C02_03 evolução | "a pergunta foi mudando" | 85–87 + 2,4 s de pausa | REUSE |
| C03_01 logos | ferramentas | 87–94 | REUSE |
| C03_02 chave UA | UA desligou | 118–124 | REUSE |
| C03_03 contador 153 | 153 / 4 em 10 | 147–153 | REUSE |
| C03_05 GA4 | GA4 1/3 | 153–159 (3 em 10) | ADAPT |
| C03_04 de nada Vitória | piada | 160–161 | REUSE (reordenar) |
| C03_06 gosto pouco | IA | — | DROP (sentido invertido) |
| C03_07 IA timeline | IA/atribuição/BigQuery | 198–226 | ADAPT |
| C03_08 botão→modelo | virada | 226–232 | REUSE |
| C04_01 bordão 203 | 203 vezes | 236–238 (+200) | ADAPT / RETHINK c/ supercut (H8) |
| C04_02 origem | — | — | DROP |
| C04_03 apelidos | 16 → 60+ | 254–257 | ADAPT |
| C04_04 diamante | oficial | 258–260 | REUSE |
| C04_05 gritem | respiro | 260–263 | REUSE |
| C04_06 Pica-Pau | 24× | 263–271 / 289–302 | REUSE |
| C05_01 mural | 191/348/140 | 316–327 (~200/~350/140+) | ADAPT |
| C05_02 setores/Google | — | 335–346 | REUSE |
| C05_03 chorando | "Queria" | 346 | ADAPT |
| C05_04 PM RJ | — | 347–354 | REUSE |
| C05_05 ficha | Phill/Mafê/Bonel | 355–377 | REUSE |
| C06_01 acerta antes | — | 390–394 | REUSE |
| C06_02 bleep | — | — | DROP |
| C06_03 fev22/out24 | toddynho/MMM | 394–412 | REUSE |
| C06_04 Purple/Guta/Lucas | — | — | DROP (H3) |
| C06_05 Meridian/MCP/dez24 | — | 414–448 | ADAPT |
| C06_06 meia-culpa | — | 459–462 | ADAPT |
| C06_07 fev26/jun26 | — | 456–464 | ADAPT (H4) |
| C07_01 vocês | — | 491–498 | REUSE |
| C07_02 700 mil/horas | 106→100+ | 497–502 | ADAPT |
| C07_03 2038 | — | 503–510 | REUSE |
| C07_04 países | 110→100+ | 510–514 | ADAPT (H2) |
| C07_05 EP197 | — | 517–527 | REUSE |
| C07_06 gente | — | 528–532 | REUSE |
| C08_01 / C09_01 título/final/loop | — | 565.7 ou 602.2 | REUSE (recalcular) |
| C00_00–C00_03 | pré-sessão | independentes | REUSE |

Totais: REUSE 21 · ADAPT 13 · DROP 5 (C04_01 pode virar RETHINK em H8). Zero asset novo criado.

## 9. FACT CHANGE MAP
| # | OLD (V2) | NEW (fala/roteiro novo) | Visual afetado | Ação |
|---|---|---|---|---|
| F1 | dados 11.526 × acho 11.032, 494 | removido | C01_02, C01_03 | dropar |
| F2 | GA4 "1 a cada 3" | "3 a cada 10" | C03_05 (texto+grade) | trocar |
| F3 | IA "1 a cada 4" | "metade dos episódios" | C03_07 (rótulo+grade) | trocar |
| F4 | atribuição/increm. "quase o mesmo tanto" | "4 em cada 10 deste ano" (falado: incrementalidade) | C03_07 pills | trocar + confirmar (H9) |
| F5 | 203 vezes | "mais de 200" | C04_01 | trocar p/ "+200" |
| F6 | 16 maneiras | "mais de 60" | C04_03 | trocar p/ "60+" |
| F7 | 191 / 348 / 140 | "quase 200" / "quase 350" / "mais de 140" | C05_01 (3 contadores) | trocar |
| F8 | 106 mil horas | "mais de 100 mil horas" | C07_02 | trocar |
| F9 | 110 países | "mais de 100" (roteiro/passada limpa); "mais de 110" no fecho falado | C07_04 | decidir (H2) |
| F10 | — | "no Spotify" (episódio 197) | C07_05 | opcional |
| F11 | "IA na home do GA em fev/2026" | roteiro tem; **não falado** | C06_07 | confirmar (H4) |
| F12 | Meta (roteiro) | não falado (nem no V2) | — | nada |
| — | **Inalterados**: 153, "4 em cada 10" GA4, 24× Pica-Pau, 27 dias, Phill 29, Mafê 24 (ep. 1), Bonel 7, 700 mil, 2038, EP 197, Copilot jun/26, MCP abr/25→jul, Meridian +3 meses, MB Talks/2015 | | | |

> Observação: "MB Talks" (nome do programa) é o do roteiro novo e foi falado; versões antigas do roteiro diziam "Analytics Talks". Nós V2 já usam MB TALKS.

## 10. Don'ts aplicados
Câmera não escolhida por qualidade técnica nem vídeo inspecionado (leitura de TP é decisão de edição, não de pré-flight); insert com sentido mudado → DROP; dados mudados → trocar; ASR tratado como pista (ex.: "Luciano"/"Lucian", "Popilot", "Pobarino"); nenhum asset oficial substituído; nada movido ou sobrescrito; V2 intacta.

## 11. EP300 V3 EXECUTION PLAN (para depois do reset)

**A. MEDIA REPLACEMENT** — trocar as 3 fontes por `MVI_9939` (geral), `MVI_9947` (Gustavo), `MVI_9967` (Lucian). **Riscos técnicos:** originais ~9 GB e 23,976 fps (V2 usa `FPS=30`; a geral antiga era um transcode de 1,5 GB) → decidir conform (23,976→30 ou timeline 23,976) e fazer proxies só então; offsets entre câmeras (estimativa grosseira por energia: Gustavo ≈ +2,54 s, Lucian ≈ −0,11 s em relação à geral — **não confiável**, rodar `v2/sync_check.py` equivalente) e **re-medir o lead de 5 quadros** da imagem da geral (`W_VIDEO_LEAD_FRAMES`) — pode não valer para o arquivo novo. Cold open, aviso, tela EP300 e loop **não trocam**.

**B. TIMELINE RECONSTRUCTION** — criar `v3/plan.py` derivado de `v2/plan.py` (V2 intacta): `SEGMENTS`/`CUTS` novos a partir das passadas limpas da seção 5 (≈ 11 trechos), `OFFSETS` novos; cada cue herda de V2 com `st` re-ancorado na fala nova (campo `tl`/`st` por fala, não por timecode). Pausa P_EVOL de 2,4 s e respiro GRITEM de 3 s mantidos.

**C. CAMERA** — reaproveitável: *regra* (geral frontal por padrão; fechadas só em reação/brincadeira; punch-ins WG/WL) e os pontos de reação (chorando, "Acredito, cara", gritem). Refazer: **todos os cortes de câmera** (timecodes novos, takes novos). Decidir câmera olhando vídeo — não feito hoje.

**D. INSERTS** — seção 8: REUSE 21 · ADAPT 13 · DROP 5.

**E. TEXT/DATA (obrigatório mudar)** — F2–F8, F9 (após H2); remover pills "viu, Layla?" e "gosto pouco"; rótulo "IMPOSSÍVEL"→"não dava pra fazer"; carimbo "IA NA HOME DO GA" sujeito a H4.

**F. AUDIO** — trilhas e SFX permanecem; recalcular ducking e as âncoras de SFX (todas atreladas a cues); bleep novo só se H7 mandar. `BLEEPS` antigo sai.

**G. NEW MOMENTS** — (opcional, depende de H) fecho com "Qual o futuro da mensuração?" → título; "hard/soft skill… pessoas" (N10) se mantido; beat "Acredito, cara"; supercut bordão (H8). Nenhum asset criado nesta etapa.

**H. HUMAN DECISIONS (11)**
- **H1** Abertura: usar 16.6–21.5 ("Bem-vindos… especial", mas diz "Luciano") ou 42.5–50.1 ("Tá no ar, tá valendo… 300")? E a repetição de "Tá no ar, tá valendo" com o cold open?
- **H2** Países: "100+" (roteiro/passada limpa) ou "110+" (fecho falado)?
- **H3** Menção a Purple/Guta/Lucas ("de nada") sumiu da fala — intencional?
- **H4** "GA colocou IA na home (fev/26)" no roteiro mas não falado — manter carimbo na tela?
- **H5** Pica-Pau: passada curta (263–271) ou longa com "ninguém sabe essa referência" (289–302)?
- **H6** Fecho: qual passada (555–566 ou 592–602) e manter o improviso hard/soft skill + "resolva agora"?
- **H7** Palavrão "fucking" (80.9): manter c/ bleep ou outra passada?
- **H8** Usar `BORDAO_SUPERCUT_158_cortes.mp4` no lugar dos prints (C04_01)?
- **H9** Atribuição/incrementalidade "4 em cada 10": rotular só incrementalidade (como falado) ou ambas (roteiro)?
- **H11** Kinoplex APOIADOR: confirme com Taciana o asset oficial da logo. Escolha gramática (rótulo separado APOIADOR ou integrado em PATROCÍNIO)?
- **H10** Dez/2024 virou piada de atribuição ("quem disse foi o Gustavo"): manter como está e onde cai a "meia-culpa"?

**I. EXECUTION ORDER**
1. Conform/proxy das 3 câmeras novas + sync (offsets, lead) — destrava tudo.
2. Gabriel responde H1–H10 (5 min, só sobre esta página).
3. `v3/plan.py`: SEGMENTS/CUTS a partir da seção 5 + ajuste de cues.
4. Trocar dados/textos (seção 9) e rerenderizar apenas overlays afetados (build com cache por hash).
5. Câmeras (cortes/punch-ins) vendo o vídeo, depois TP-check.
6. Áudio (ducking, SFX), XML editável + proxy, QA (leak, safe area, reading, sync) e handoff no Studio — V3 como **READY_FOR_HUMAN**, nunca master.

## Limites desta análise (honestidade)
- Vídeo novo **não foi visto** (nenhum frame decodificado); nada sobre enquadramento, TP-reading, foco ou exposição.
- Passadas "limpas" são escolhas por texto (ASR com erros; mesmos nomes variam). Timestamps ±0,3 s.
- Diarização falhou; atribuições Gustavo/Lucian vêm do roteiro.
- Roteiro Notion tem 3 versões na mesma página; usei a do topo ("novo roteiro:") — confirmar que é a vigente.

---

## NOVO REQUISITO — Kinoplex (adicionado 01/10)

**Origem:** orientação oficial da Taciana.

**Requisito:** Kinoplex deve aparecer como **APOIADOR** do EP300, seguindo a mesma lógica visual que Purple Metrics (PATROCÍNIO), Onfly (PATROCÍNIO), Coffee++ (CAFÉ OFICIAL) e Reportei (PATROCÍNIO).

**V2 atual:** Kinoplex não aparece (evento foi adicionado após o início da edição).

**Localização da linguagem visual:**

- **Cue C00_02** (`plan.py`, linhas 174–177): rótulo "PATROCÍNIO" em cinza pequeno (22 px, cor 160,160,160), com 3–4 logos 150–170 px lado a lado, sway 2,6–3,4.
- **Final/loop** (`customs_v2.py`, linha 214): "patrocinadores entram" no cue C09_01 (9 s antes do loop mudar).

**Status do asset:**
- ❌ **Logo do Kinoplex: MISSING_OFFICIAL_ASSET** — não encontrada em `v2/`, em `v3-preflight/` nem em `EP300_HANDOFF_LUCIAN/03_SHARED_ASSETS/logos`.
- Ação: Confirmar com Taciana/Design se existe logo oficial do Kinoplex e fornecê-lo em `.webp` (formato padrão).

**Integração no V3:**

1. **Se o logo existir:** adicionar a plan.py no cue C00_02 (após Reportei, se 4º patrocinador, ou em seção "APOIADOR" separada, decisão editorial).
2. **Rótulo:** "APOIADOR" em cinza (mesma cor), pequeno (20–22 px).
3. **Posição:** lado a lado com os demais, respeitando sway (oscilação) para dinâmica visual.
4. **Final:** incluir no mosaico de `customs_v2.py` que monta o lockup do loop.

**QA checklist V3:**
- [ ] PATROCÍNIO presentes e identificados (Purple Metrics, Onfly, Reportei)
- [ ] CAFÉ OFICIAL presente (Coffee++ Plus)
- [ ] APOIADOR presente (Kinoplex) — **bloqueador até ter o asset**
- [ ] Logos legíveis e sem overlap
- [ ] Ordem consistente (abertura + final/loop)

**Human decision (H11):**
- Confirme com Taciana o asset oficial do Kinoplex.
- Escolha gramática: rótulo separado "APOIADOR" ou integrado junto de "PATROCÍNIO"?

---
