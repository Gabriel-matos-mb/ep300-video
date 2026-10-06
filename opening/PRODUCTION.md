# Produção — EP300 Cinema Opening

Complementa o breakdown cena-a-cena em
[wiki/concepts/ep300-roteiro-edicao.md](../../wiki/concepts/ep300-roteiro-edicao.md)
(que já cobre trecho/insert/tratamento). Este arquivo cobre o que falta para a
produção em si: preparar a captação e mapear estados de dependência por bloco.

## Shot list operacional (visão de produção — detalhe cena a cena continua em `ep300-roteiro-edicao.md`)

Legenda: ✓ disponível · ○ aguardando gravação/site/telão · ? a definir.

| Cena | Fala/trecho (resumo) | Plano | Motion/insert | Asset | Status | Observação |
|---|---|---|---|---|---|---|
| Cold open | "Começou mesmo? Começa de novo aí" → "Fala aí, analítica..." | câmera já rodando antes do "start", cru | nenhum (propositalmente cru) | — | ○ gravação | não regravar "limpo" — a falha é a piada |
| Ato I | "300 episódios são mais de 300 perguntas" (Gustavo, em câmera) | estável, espaço negativo pro contador | contador subindo até 300 | print/thumbnail 2015 (opcional) | ○ gravação · ○ asset | sem material de arquivo, ícone + "2015" resolve |
| Ato II | "...hoje pergunta se dá pra confiar num modelo" (Gustavo, seco) | fechado, corte seco no "hoje" | split screen ícone antigo × IA + 3 grades de proporção repetidas | — | ○ gravação | grades reaproveitam o mesmo visual, só muda preenchimento |
| Ato III | "Diamante Negro é o oficial" (Lucian, pra câmera) + piada do pica-pau | destaque isolado, maior | colagem tipo post-it (apelidos) + cards empilhados "replay stack" | ícone do pica-pau (a criar, reaparece no Ato IV) | ○ gravação · ○ asset | contraste com a rajada anterior |
| Ato IV | "as respostas quase nunca foram nossas" + Phill/Mafê/Bonel | câmera + espaço pra parede de avatares | parede de avatares/logos; placar pessoal (foto + contador) | fotos Phill/Mafê/Bonel; logos das empresas (⚠️ nunca a Uncover) | ○ asset | sem fotos de todos: iniciais/silhuetas cobrem o resto |
| Ato V | módulo repetido 4× "nossa pergunta → resposta do mercado" | majoritariamente narração, sem exigência forte de câmera | módulo único (carimbo de data → corte → carimbo de data) repetido 4× | — | ✓ dados prontos · 🟡 aberto | comentário editorial aberto sobre frase de transição — ver wiki |
| Epílogo | mapa-múndi + contadores; capa ep. 197; fechamento "os dois juntos" | fechamento em câmera, os dois juntos | infográfico mapa-múndi (insert mais produzido); moldura "prêmio" pro ep. 197; cartaz final tela cheia | capa do ep. 197; screenshot do painel de números congelado no dia | ○ gravação · ○ asset · 🟡 aberto | trecho "não entendi" (Nina/Gustavo) ainda em validação |

## Formato/resolução/safe area de exportação

**RESOLVIDO (28/09, visita técnica ao Kinoplex de 25/09 — notas de Taciana/Rafael):**
playback é notebook → HDMI → projetor. Resolução nativa informada pela fonte: **2K (1920x1080)**
— nomenclatura mantida como recebida, sem "corrigir" para 1080p. Formato ideal de projeção seria
DCP, mas **não é requisito** nesse fluxo (é via HDMI). **Entrega: 1920x1080, 16:9, MP4.**

Distinção importante: a **captação** do vídeo de abertura é orientada em **4K 16:9** (margem de
reenquadramento/pós) — isso não muda o arquivo final, que continua 1920x1080. Não misturar as duas
especificações. Ainda sem resposta registrada: safe area, sonorização, quem dispara o conteúdo no
dia, janela de teste na sala — ver [QA.md](QA.md) (não bloqueiam edição, só o QA final).

## Linguagem visual fina (como cards/números/telas se comportam)

**AGUARDANDO SITE** — ver [VISUAL_SYSTEM.md](VISUAL_SYSTEM.md). O que já está definido (tom, tratamento de números, cold open cru) já é suficiente para editar; o resto trava só a gramática de motion final.

## O que preparar agora, sem esperar as dependências

Pergunta orientadora: *o que deixa o Gabriel pronto pra editar assim que o material chegar?*

- Estrutura de projeto editável (bins/sequência-base) pode ser montada agora, mesmo vazia.
- Módulo repetido do Ato V (carimbo de data → corte → carimbo de data) pode ser prototipado agora — não depende de gravação nem de site.
- Placar de números do cold open ("dados" × "acho") pode ser produzido agora — são só os dois números.
- Checklist de assets a levantar (fotos, logos, prints) pode ser disparado agora, em paralelo à gravação.
- O que **não** dá pra adiantar: qualquer corte com câmera real, e qualquer decisão de motion fino que dependa do site.

## Preparação da gravação (para quando a data for confirmada)

A partir do texto de teleprompter e do breakdown, a montagem já indica o que a
captação precisa garantir:

- **Cold open**: um único take "errado" de propósito (Lucian: "Começou mesmo?
  Começa de novo aí") — precisa soar genuinamente cru, não ensaiado. Gravar com
  câmera já rodando antes do "start" oficial, para pegar o momento sem corte.
- **Falas em câmera vs. falas em voice-over**: o teleprompter já marca cada trecho
  como `[em câmera]` ou `[voz]`. Os trechos `[em câmera]` são os que precisam de
  enquadramento estável e espaço negativo para inserts entrarem por cima (Ato I
  "300 episódios são mais de 300 perguntas", Ato II "seco", Ato III "Diamante Negro
  é o oficial", Ato IV abertura, Ato V abertura, Epílogo "os dois juntos" no final).
  Os `[voz]` são narração e podem ser cobertos inteiramente por insert.
- **Takes alternativos**: pelo menos 1 take extra nos momentos de humor (piada do
  Diamante Negro, piada do pica-pau) e no fechamento "os dois juntos" — são os
  pontos de maior peso emocional/comédia e mais sensíveis a timing.
- **Espaço negativo / margem antes-depois**: cada trecho `[em câmera]` precisa de
  1–2s de folga antes e depois da fala (para corte e para entrada/saída de insert)
  — não gravar "colado".
- **Continuidade**: Gustavo e Lucian aparecem juntos só no cold open e no
  fechamento; todo o miolo intercala falas individuais — não é necessário manter
  os dois em quadro o tempo todo, mas o figurino/luz precisa ser consistente entre
  as janelas de gravação (se cold open e miolo forem gravados em datas diferentes).
- **Riscos de pós-produção a mitigar na captação**: (1) cold open perder a graça se
  regravado "limpo demais" — orientar para não repetir até sair perfeito; (2) falta
  de espaço negativo forçar recomposição/crop nos inserts de dado; (3) não gravar
  reação/silêncio suficiente antes do corte para o preto pós-cold-open.

Não complexificar além disso — a montagem já orienta a captação; não é necessário
um plano de câmeras dedicado além do que o roteiro e o teleprompter já implicam.

## Fonte

Notion: [Roteiro — Vídeo de abertura EP 300](https://app.notion.com/p/3e29812d8c37810fbd27d05645aec554),
[Texto corrido para teleprompter](https://app.notion.com/p/3e29812d8c3781028f79f2a630bf766a).
Wiki: [[../../wiki/concepts/ep300-roteiro-edicao]].
