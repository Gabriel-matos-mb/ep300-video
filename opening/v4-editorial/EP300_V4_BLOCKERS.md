# EP300 V4 — Blockers

> 2026-10-02. Só bloqueios **reais**. Decisão criativa pequena não é blocker.
> Classes: **BLOCKS BUILD** (impede montar/renderizar) · **BLOCKS FINAL** (impede finalizar/QA daquele item) · **DOES NOT BLOCK**.

## Bloqueios reais (2)

| # | Bloqueio | Classe | O que trava exatamente | Quem destrava | Entrada necessária |
|---|---|---|---|---|---|
| B1 | **Spec da sequência (fps/resolução)** | **BLOCKS BUILD** — só o re-render de overlays; **não** trava sync/montagem de diálogo | Master é 4K 23,976 fps; overlays V2 são 1080p 30 fps. Overlay pré-renderizado em 30 fps dentro de sequência 23,976 repete/pula quadros. Render em fps/res errados é retrabalho certo. | Gabriel | 1 linha: sequência 4K ou 1080p, e 23,976 ou 30 fps. **Recomendação: 23,976 fps; resolução da entrega que o cinema pedir (a sequência "SYNC 4K" sugere 4K).** |
| B2 | **K1 Kinoplex — tratamento visual** | **BLOCKS FINAL** — somente a aplicação do Kinoplex (slot em A4 e G4); **não** trava a montagem estrutural | Posição, rótulo, tratamento e agrupamento são desconhecidos. Não inventar; sem logo em sticker, sem redesenho. | Cláudio Miranda (site/handoff); Taciana/Taci como ponte quando aplicável | Design oficial + logo. Data: sem data confirmada. |

## Não bloqueiam (reclassificados)

| Item | Classe | Por quê |
|---|---|---|
| Projeto Premiere não salva no Drive | DOES NOT BLOCK | Arquivo do Drive é stub (3 clipes empilhados, nenhuma edição). Workaround: Save As **local**. O "SYNC 4K.prproj" nunca chegou ao disco. |
| H1 abertura | DOES NOT BLOCK | Resolvido pela fala (take 42.5). |
| H9 atribuição/incrementalidade | DOES NOT BLOCK | Resolvido pela fala. |
| H2, H4, H7, H8, H10 | DOES NOT BLOCK | Estreitados; cada um afeta um beat isolado e tem default seguro (+100; sem carimbo; bleep/dip; prints; sem gag). |
| H3 "de nada, Purple" | DOES NOT BLOCK | Ouvir 2 s; DROP\* provisório não trava nada. |
| H5 Pica-Pau, H6 fecho | DOES NOT BLOCK | Default existe (curta; 592–607). Só mudam recortes de EDL. |
| Roteiro Notion — qual bloco é vigente | DOES NOT BLOCK | A gravação é a autoridade; roteiro só confere. |
| Orientações de cinema / estrutura adicionais | DOES NOT BLOCK | Nenhuma orientação nova estava no material lido; a fala manteve a ordem do roteiro (uma troca: C7). Se chegarem, afetam sobretudo o bloco A (pré-sessão). |
| Sync entre câmeras (offsets) | DOES NOT BLOCK | Passo de produção (Premiere), não dependência externa. |
| Thumb — remover uma pessoa (feedback Lucian) | DOES NOT BLOCK | `EP300_BACKLOG / SECONDARY_ASSET / NEEDS_IDENTIFICATION`. Não afeta a abertura. Não identificável no material existente. |
| Loop (EP300 Cinema Loop Video) | FORA DE ESCOPO | Atualizado só depois da abertura V4 consolidada. |
