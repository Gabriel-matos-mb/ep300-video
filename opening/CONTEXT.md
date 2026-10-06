# Contexto — EP300 Cinema Opening

## O que é

Vídeo de abertura para a gravação presencial do episódio 300 do Analytics Talks,
exibido no telão de uma sala de cinema antes/durante o evento. Tema da campanha:
"Do Império dos Dados Ao Futuro da Mensuração".

**Evento** (fonte: Notion, [Episódio 300 Analytics Talks Especial no Cinema](https://app.notion.com/p/3d09812d8c378048b43fcf7b35c2f6fd)):
- Data: 08/10/2026, 10h–12h.
- Local: Kinoplex — Shopping Parque da Cidade, São Paulo/SP.
- Capacidade: 70 pessoas, evento gratuito, inscrição prévia.
- Patrocinador: Purple Metrics.

## Por que isto não é "mais um episódio do Podcast"

O Podcast (`podcast-cutter`, cortes verticais) tem regras editoriais, pipeline e QA
próprios para conteúdo recorrente semanal. O EP300 Cinema Opening é uma peça única,
de evento, com telão físico (não feed/stream), câmera + gravação em estúdio para
falas em câmera, e uma linguagem visual herdada de uma experiência digital
interativa (o site do EP300) — não do padrão visual do podcast. Misturar as duas
frentes contaminaria as regras gerais de Podcast/Cursos/Analytics Copilot com
exceções específicas de evento/telão.

Ao mesmo tempo, reutiliza o que já existe no ecossistema: Skills de motion
(`hyperframes-*`), tokens de marca (`design-kit/tokens/`), Evidence, e o Studio como
cockpit — nada disso é reimplementado aqui.

## Dependências reais (não inventar enquanto não chegarem)

1. **Gravação** — falas em câmera (Gustavo/Lucian) e cold open.
   > ⚠️ Contradição a resolver com o Gabriel (2026-09-26): o pedido original fala em
   > "gravação prevista para segunda-feira" (2026-09-28), mas o registro existente no
   > board (`ep300-video-abertura`, 2026-09-22) e a memória do projeto apontam para a
   > semana de 29/09–01/10 (terça a quinta), com fechamento até 07/10. Não presumir
   > qual data está certa — confirmar antes de travar a preparação de captação.
2. **Especificações do telão** — resolução nativa, aspect ratio, codec/container,
   frame rate, safe areas, sonorização, teste na sala. Perguntas já levantadas no
   Notion ([Dúvidas para Visita técnica](https://app.notion.com/p/32b9812d8c3782ae9e6101c29acf62de),
   status CONCLUÍDO na tarefa, mas as respostas em si não estão registradas nas
   fontes lidas até agora — confirmar se já foram respondidas e onde). Enquanto isso,
   ver [QA.md](QA.md) para a lista parametrizável.
3. **Site do EP300** (Claudio + Lucian) — experiência de retrospectiva interativa
   (conceito próximo de Spotify Wrapped, mas não uma cópia dele). É a fonte principal
   da linguagem visual do vídeo. Sem acesso ainda — ver [VISUAL_SYSTEM.md](VISUAL_SYSTEM.md)
   para o mapa provisório e o que muda quando o site chegar.

Nenhuma destas três é presumida ou inventada. O trabalho que **não** depende delas
(breakdown do roteiro, preparação de captação, estrutura de QA parametrizável,
estrutura de produção/pastas) avança agora.

## Roteiro

Fonte oficial (não editar, não duplicar): Notion —
[Roteiro — Vídeo de abertura EP 300 · "O podcast em números"](https://app.notion.com/p/3e29812d8c37810fbd27d05645aec554)
e [Texto corrido para teleprompter](https://app.notion.com/p/3e29812d8c3781028f79f2a630bf766a).
O breakdown operacional (cena a cena, tipo de insert, tratamento visual) já existia
antes deste projeto, em [wiki/concepts/ep300-roteiro-edicao.md](../../wiki/concepts/ep300-roteiro-edicao.md) —
continua sendo o banco de trabalho vivo, atualizado ali, não copiado aqui.

Três trechos do roteiro têm comentário editorial aberto (Nina/Gustavo) e dependem de
validação antes de travar a edição — marcados `🟡` no arquivo acima.

## Case replicável

Ver [LEARNINGS.md](LEARNINGS.md). Ainda não generalizar — primeiro FAZER → USAR →
OBSERVAR → APRENDER, só depois GENERALIZAR.
