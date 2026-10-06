# QA — EP300 Cinema Opening

QA específico deste projeto (telão/cinema). QA geral de finalização/entrega (delivery,
validação humana vs. build) continua sendo a skill `mb-studio-delivery` — não
duplicado aqui.

## Especificações do telão

Respostas da visita técnica ao Kinoplex (25/09, notas de Taciana/Rafael), registradas 28/09:

- [x] Resolução nativa e proporção da tela/projetor — **2K (1920x1080)**, nomenclatura da fonte mantida.
- [x] Playback — **notebook → HDMI → projetor**; DCP seria o formato ideal de cinema mas **não é
      requisito** nesse fluxo.
- [x] Entrega — **1920x1080, 16:9, MP4** (mesma especificação para abertura e looping).
- [ ] Codec/container e frame rate específicos — não pedidos/confirmados; não inventar até surgir.
- [ ] Safe area de projeção (a tela pode cortar bordas).
- [ ] Sonorização: áudio entra direto no sistema de som da sala ou precisa de
      estrutura externa? Formato de entrega do áudio (estéreo? níveis?). (A prioridade da sala é a
      captação do podcast: caixas para a plateia ficam em volume baixo para evitar vazamento/eco nos
      microfones — locação a cargo do Rafael, sem técnico definido ainda.)
- [ ] Quem dispara os conteúdos no dia, e em que formato/pasta eles esperam
      receber o arquivo final.
- [ ] Janela disponível para teste de imagem+áudio na própria sala antes do evento.

Nenhum destes itens em aberto bloqueia edição/render — só o QA final antes do Kinoplex (ver abaixo).

## Resolução de exportação — confirmada

1920x1080, 16:9. Pode montar a composição direto nesse formato (não precisa mais
manter os blocos desacoplados de uma resolução fixa por causa do telão).

## QA de conteúdo

- [ ] Roteiro final bate com a versão travada (sem comentário `🟡` aberto).
- [ ] Números/dados conferidos contra a fonte (`Levantamento de dados para vídeo`, Notion).
- [ ] Nomes e grafias corretos (convidados, empresas).
- [ ] Ordem dos atos e transições fazem sentido narrativo.

## QA visual

- [ ] Legibilidade dos números/texto pequeno (marca-texto laranja + circulado à mão).
- [ ] Composição e espaço negativo preservados nos trechos `[em câmera]`.
- [ ] Ritmo e contraste consistentes entre os 5 atos + epílogo.
- [ ] Nenhum elemento crítico cortado pela safe area.
- [ ] Coerência com a linguagem do site (quando o site chegar — ver VISUAL_SYSTEM.md).

## QA técnico

- [ ] Resolução, aspect ratio e FPS batem com o confirmado pelo Kinoplex.
- [ ] Codec/container aceito pelo sistema de playback da sala.
- [ ] Áudio no formato/nível esperado pela sonorização da sala.
- [ ] Duração final bate com a janela do evento.

## QA final (antes de levar pro Kinoplex)

- [ ] Assistir o master completo, do início ao fim, sem pular trechos.
- [ ] Testar o arquivo real (não um proxy/preview) no formato de entrega.
- [ ] Testar playback na própria sala antes do evento, se a janela for concedida
      (ver perguntas da visita técnica).
- [ ] Confirmar qual é a versão aprovada (nome de arquivo sem ambiguidade).
- [ ] Gerar backup do master antes do dia do evento.

## Contingência

Entrega mínima: **master principal + backup** (cópia separada, não é a mesma mídia
física). Quando o sistema do cinema for conhecido, avaliar se vale também uma
versão alternativa (ex.: codec mais compatível) como contingência de playback.

Distinção que não pode se perder: **arquivo existir ≠ master ≠ testado localmente
≠ testado no sistema do cinema.** Cada seta dessas é uma verificação própria, não
uma consequência automática da anterior.

## QA editorial (herda do wiki)

Regras editoriais e de fala/legenda válidas para qualquer produção da MB (não
duplicadas aqui): `podcast-cutter/editorial/` (`glossary.md`, `subtitles.md`,
`editing.md`). Cuidado específico deste roteiro: **não destacar a Uncover**
(concorrente da Purple, patrocinadora) nos grids de logos do Ato IV.
