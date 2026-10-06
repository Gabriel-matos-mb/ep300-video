# EP300 Cinema Opening

Vídeo de abertura do episódio 300 do Analytics Talks, para exibição no telão do
Kinoplex (evento presencial, São Paulo, 08/10/2026). É uma **produção audiovisual
própria** dentro do ecossistema — relacionada ao Analytics Talks/EP300, mas com
objetivo, formato, linguagem visual, pipeline, QA e aprendizados próprios. Não é
"mais um episódio do Podcast".

> Princípio: projeto separado ≠ ecossistema separado. Este projeto reutiliza Skills,
> Evidence, QA, Studio e as convenções do wiki — só o que é específico do EP300 vive
> aqui. Ver [[../../wiki/concepts/production-model]] §9 para o critério de quando uma
> produção ganha uma pasta própria em `projects/`.

## Onde está cada coisa

| O quê | Onde |
|---|---|
| **Objetivo, formato, dependências, decisão de arquitetura** | [CONTEXT.md](CONTEXT.md) |
| **Estado atual (snapshot para quem não abre o Studio)** | [STATUS.md](STATUS.md) |
| **Breakdown operacional do roteiro (cena a cena)** | [wiki/concepts/ep300-roteiro-edicao.md](../../wiki/concepts/ep300-roteiro-edicao.md) — já existia antes deste projeto nascer; continua sendo o banco de trabalho, não duplicado aqui |
| **Preparação da gravação (o que garantir na captação)** | [PRODUCTION.md](PRODUCTION.md) |
| **Direção visual (mapa provisório, site ainda não chegou)** | [VISUAL_SYSTEM.md](VISUAL_SYSTEM.md) |
| **QA específico de telão/cinema** | [QA.md](QA.md) |
| **Case replicável — aprendizados e candidatos a capacidade reutilizável** | [LEARNINGS.md](LEARNINGS.md) |
| **Estado ao vivo, progresso, log** | Studio — `studio/data/board.json` id `ep300-video-abertura`, página `#/ep300` |
| **Roteiro oficial (não editar, não duplicar)** | Notion — [Roteiro — Vídeo de abertura EP 300](https://app.notion.com/p/3e29812d8c37810fbd27d05645aec554) |

## Por que não tem `agents/`, `workflows/`, `templates/`, `scripts/` ainda

A árvore hipotética original previa essas pastas, mas nenhuma tem função real
ainda — nenhum processo se repetiu o suficiente para justificar automação própria.
Candidatos identificados (Asset Checker, Motion QA, Screen/Cinema QA,
Script-to-Scene Mapper, Site Visual Analyzer, Render Validator) estão registrados
em [LEARNINGS.md](LEARNINGS.md) como candidatos, não implementados.
