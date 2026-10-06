# EP300 · Vídeo de abertura · V0 — mapa audiovisual (edit plan)

> Fonte de verdade narrativa = **material gravado em 28/09** (3 câmeras), não o roteiro do Notion.
> Fonte de verdade técnica = `v0/plan.py` (este documento o descreve para humanos).
> Timecodes `mm:ss` = posição na V0 (5:32). Fonte = segundos na CAM_GERAL.

## Material

| Arquivo (01_BRUTOS) | Formato | Duração | Papel |
|---|---|---|---|
| `CAM_GERAL.mp4` | 1920x1080 · 30 fps · AAC 48k (mono duplicado, **vem da mesa de som**) | 17:27 | plano aberto + **áudio de diálogo** (piso de ruído −73 dB) |
| `MVI_9943-CAM_GUSTAVO.MP4` | 3840x2160 · 23,976 · H.264 | 8:02 | close do Gustavo; áudio de câmera estourado (10k amostras clipadas) — não usado |
| `MVI_9943-CAM_LUCIAN.MP4` | 3840x2160 · 23,976 · H.264 | 8:04 | close do Lucian; áudio de câmera baixo (−43 dB) — só sincronia |

Sincronia por correlação de áudio: Gustavo começa em **476,503 s** e Lucian em **476,320 s** da CAM_GERAL
(3 janelas conferidas, desvio ≤ 20 ms). Os nomes `MVI_9943` repetidos são coincidência de numeração das duas Canon.

**Estrutura real da gravação (CAM_GERAL):** 0:00–8:08 bastidor/briefing (Lucian explicando a ideia ao Gustavo,
ajuste de mic "é áudio de cinema") · **8:27–15:54 take gravado** · 15:57+ bastidor (levantando).

## Transcrição

Não existia transcrição do vídeo de abertura no Drive (a pasta 300 não tem `08_TRANSCRICAO` nem srt/txt).
Gerada localmente, custo zero: faster-whisper **large-v3** (modelo do podcast-cutter) + large-v3-turbo, GPU, sem VAD,
palavra por palavra. Arquivos em `02_PROJETOS/EP300_ABERTURA_V0/TRANSCRICAO/`.

## Narrativa real gravada × roteiro

O take segue o roteiro "O podcast em números" (Notion) quase na ordem, com improvisos que são o melhor do material:

- **Zoeira com a Vitória** — "De nada, Vitória Comarim" (2 versões; eles pediram *"volta aí que eu vou zoar a Vitória"* → usada a 2ª) e depois "Desculpa, Vi." no "todinho".
- **4ª parede real** — Gustavo aponta pra câmera: *"diamante negro é oficial, né galera? Gritem se concordam"*.
- **Recados para a plateia** — "de nada, viu, Purple…", "viu, Laila?".
- **Ironia** — "é um tema que eu gosto pouco, meu parceiro: inteligência artificial".
- **"Muito obrigado"** ao Phill; **"Eu queria. / Também queria."** (parceria com o Google).
- **Fechamento** — "Qual o futuro da mensuração? / Esse é o tema do episódio? / Obrigado, gente" + risada.

Diferenças vs. roteiro: "16 maneiras" de apresentar o Lucian (o site diz **40+**); **106 mil horas** (site: 107K);
**191 pessoas / 140+ empresas** (site: 196 / 146). A V0 usa **o que foi falado**; ver Pendências.

## Cortes editoriais (retomadas e pedidos)

| Fonte | O que saiu | Por quê |
|---|---|---|
| 598,3–620,3 | 1ª versão do "de nada, Vitória" + orientação de teleprompter ("sobe mais…") | retomada pedida por eles |
| 712,9–756,6 | bloco das empresas travado em "a Meta… confirma, não tem Meta" | retomada; usada a 2ª a partir de "Banco, varejo" |
| 783,8–785,8 | "Fora casa, o recordista—" | gaguejo repetido na hora |
| 796,2–855,2 | "volta ali, a entonação ficou errada" + 3ª versão ("acho que não ficou boa… só corta") | eles mesmos descartaram |
| 891,0–897,6 | **"Chupa, Google" + "é só não colocar, eu só queria falar aqui"** | **pedido explícito do Lucian para não entrar** |
| 861,2–862,5 | palavrão (reação) → **bleep** com 🙊 | gag; remover o trecho se preferir |

Inserido: **1,6 s de respiro** após "Gritem, se concordam" (freeze + placa de cinema) para a sala responder.

## Mapa (fala → intenção → câmera → visual → som)

| V0 | Fala real | Intenção | Câmera | Visual (cue) | Som |
|---|---|---|---|---|---|
| 0:00 | — | pré-sessão | — | contagem de película EP300 (C00_01) | beeps 1 kHz |
| 0:03 | — | "trailer" do site | — | tela "EPISÓDIO 300" + clique no botão → **íris abre para a câmera real** (C00_02) | Got The Swag, clique, whoosh |
| 0:08 | "Fala aí, analítica…" / "número 300" | abertura | Gustavo | adesivo **300 🥳** (C01_01) | lápis |
| 0:15 | "chegamos a 300" | os dois | aberta | — (calma) | trilha baixa |
| 0:23 | "Pô, dados… 11.526 … acho" | dado + graça | Lucian→Gustavo | "dados, 🤓" + contador + "acho 🤔" (C01_02) | — |
| 0:33 | "494 vezes de diferença… aumentar essa distância" | informação | tela cheia | **placar dados × acho**, colunas se afastam (C01_03) | impacto |
| 0:45 | 2015 / Prime / MB Talks | história | Lucian | carimbo + 2 etiquetas (C02_01) — **calma** | — |
| 0:59 | "mais de 300 perguntas" | microgag | Gustavo | **chuva de "?"** (C02_02) | whoosh |
| 1:11 | "Como instalar? Como taguear?… até hoje" | rajada | Gustavo→Lucian | etiquetas + carimbo ATÉ HOJE (C03_01) | impacto |
| 1:25 | "desligou o Universal" | gag física | Lucian | pílula UA **desliga e cai do quadro** (C03_02) | TV off |
| 1:30 | "153 episódios, 4 em cada 10 GA4" | dado | Lucian | contador + grade 4/10 (C03_03) | — |
| 1:39 | "De nada, hein, Vitória" | piada interna | Gustavo | adesivo + seta pra fora do quadro + "zoeira nº 1" (C03_04) | lápis |
| 1:42 | "1 a cada 3… o que entrou do lado dele" | dado | Gustavo | pílula GA4 + grade 1/3 (C03_05) | — |
| 1:51 | "gosto pouco… inteligência artificial" | ironia | aberta | "“gosto pouco” 🙃" + adesivo IA (C03_06) | — |
| 1:56 | 2021→2025, atribuição, BigQuery→marketing | dado | Lucian | grade 1/4, pílulas, risco + carimbo MARKETING (C03_07) | impacto |
| 2:11 | "taguear um botão… confiar no modelo" / "Modelo." | virada | Gustavo→Lucian | **botão do site é clicado e vira a pergunta nova** (C03_08) | clique |
| 2:19 | "o assunto mudou…" | respiro | aberta | — (calma) | — |
| 2:28 | "203 vezes que eu falei 'fala aí'" | callback | Gustavo | **o quadro real da abertura vira pilha de fotos-adesivo** 1→203 (C04_01) | whoosh |
| 2:34 | "qual episódio nasceu? — Nem eu" | graça | aberta | "episódio de origem: ???" 🤷 (C04_02) | — |
| 2:38 | "16 maneiras… diamante negro é oficial" | lista + payoff | Lucian→Gustavo | etiquetas de apelido do site + carimbo OFICIAL (C04_03) | impacto |
| 2:48 | "Gritem se concordam" | **4ª parede** | Gustavo | **freeze → vira foto-adesivo → placa de cinema piscando**, 1,6 s de respiro (C04_04) | woosh-boom, trilha sobe |
| 2:50 | "Pelo amor de Deus" / Pica-Pau 24× | reação + frase clássica | Lucian→Gustavo | citação + carimbo 24× (C04_05) | impacto |
| 3:04 | "191 pessoas… 348… 140+ empresas" | números | Gustavo | 3 contadores (C05_01) | — |
| 3:13 | "banco, varejo… não é parceiro do Google?" | gag | Lucian | pílulas de setor + "PARCEIRO DO GOOGLE? / AINDA NÃO" (C05_02) | resposta errada |
| 3:19 | "Eu queria. / Também queria." | reação | Lucian | os 2 rostos-adesivo levam o **susto** do site (C05_03) | — |
| 3:21 | "nós chamamos… PM do RJ" | callback | Lucian | Pica-Pau volta + NÓS CHAMAMOS + 🚓 (C05_04) | impacto |
| 3:30 | ficha de presença: Phill 29, Mafê 24 (EP 1), Bonel 7 | homenagem | Gustavo→Lucian | **ficha de presença** preenchendo (C05_05) | — |
| 3:55 | "você acerta antes" + palavrão | gag | Gustavo→Lucian | "acerta antes 🎯" + **bleep 🙊** (C06_01/02) | bleep |
| 3:57–4:42 | fev/22 · out/24 · abr/25 · dez/24 | "chegamos antes" | Lucian/Gustavo | **módulo repetido**: carimbo de data → carimbo "+X dias/meses, Google…", zoeira nº 2 com a Vi, logo Purple, "viu, Laila?" (C06_03–06) | impactos |
| 4:43 | "E do outro lado da pergunta: vocês." | **4ª parede** | Gustavo | "vocês. 🫵" + setas para a sala (C07_01) | lápis |
| 4:44 | "700 mil… apertou o play… 106 mil horas" | números | Gustavo | botão ▶ do site clicado + contadores + relógio (C07_02) | clique |
| 4:51 | "terminaria em 2038" | maratona | Lucian | **cena do sofá** do site + ano 2026→2038 (C07_03) | relógio |
| 4:58 | "110 países" / EP 197 | dados | Gustavo/Lucian | adesivo + carimbo EP 197 🏆 (C07_04/05) | — |
| 5:10 | "era sobre… gente." | payoff emocional | aberta | "gente. 🧡" (C07_06) | ding |
| 5:12 | "300 episódios… uma pergunta pra te fazer" | calma | Lucian | — | — |
| 5:19 | "Qual o futuro da mensuração?" / "Esse é o tema?" | título | tela cheia | **DO IMPÉRIO DOS DADOS / AO FUTURO DA MENSURAÇÃO** (C08_01) | In The Spotlight |
| 5:22 | "Obrigado, gente" + risada | fecho humano | aberta | — | — |
| 5:25 | — | fim | tela cheia | "300 e contando" + patrocinadores + "🍿 a sessão já vai começar" (C09_01) | — |

Ritmo pretendido: CALMA (história, "o assunto mudou", "300 episódios… uma pergunta") → SURPRESA (chuva de ?,
UA caindo) → GAG (Vitória, bleep, "ainda não") → INFORMAÇÃO (placar, contadores, módulo das datas) → INTERAÇÃO
(Gritem, vocês) → PAYOFF (gente → título → 300 e contando).
