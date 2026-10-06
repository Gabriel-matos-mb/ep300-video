# EP300 fechado — Consolidation Pass (03/10/2026)

> Execução do `POST_EP300_TRIGGER` ([[../../CLAUDE.md]]). Evidência = trabalho real do EP300 (Opening V0→V4/Review 03 + 4K,
> Loop final, Manifesto V2–V4). **Não é arquitetura nova**; é consolidação. Detalhe de storage:
> `projects/ep300-cinema-opening/EP300_STORAGE_RECONCILIATION.md`. Estado operacional: [[checkpoint]].

## 1. Fechamento
Opening exportado em 4K + Full HD, Loop final em 1080p + 4K (`03_EDITADOS/VERSÃO FINAL` no Drive), projeto Premiere final em
`02_PROJETOS`. Picture lock = Premiere do Gabriel. Nenhuma frente criativa EP300 aberta.

## 2. Regras operacionais (do que aconteceu, não da teoria)

**Quem decide**
1. **Premiere = autoridade editorial.** Claude orquestra/executa; não é editor soberano. Decisão humana existente → trabalhar AO REDOR ([[../concepts/audiovisual-execution-router]] § 7).
2. **Edição humana é dado.** XML/`.prproj` final do Gabriel volta como aprendizado (comparar entrega automatizada × final) — só depois do master, nunca no meio.
3. **Placeholder > invenção.** Asset ausente = placeholder/flag; asset aprovado nunca regenerado ("conferir pasta antes de dizer MISSING" — os 10 stickers de convidados chegaram depois).
4. **Documentação/auditoria não autoriza execução.** Auditoria acha dívida; não a corrige na hora (nem durante fechamento de entrega).

**Como entregar**
5. **Componentes > vídeo inteiro.** Corrigir = re-renderizar UMA camada (C02_03, S10, O01, O02), nunca remontar. Layers com alfa + XML + fontes editáveis; MP4 nunca é a única entrega.
6. **Review leve → aprovação humana → master.** Proxy 720p para revisar; 4K nativo só após OK, só dos componentes aprovados; master é exportado no Premiere.
7. **Remapear por fala/beat, não por timecode.** KEEP BY DEFAULT, DROP BY EXCEPTION; V2 aprovada = DNA criativo (recuperar, não reinventar).
8. **Medir antes de afirmar.** Bleep alinhado pelo espectro (o ASR errou ~0,4 s); flashes de 1 quadro achados por varredura automática (bug de arredondamento no compositor), não "no olho". Implementação ≠ validação.

**Como trabalhar (custo)**
9. **Contexto é custo.** Sessões longas, enxames de subagentes, releitura e reprocessamento foram o maior retrabalho. `/clear` em contexto novo; `/compact` em tarefa longa; checkpoint curto > conversa como database; sem subagentes criativos.
10. **Projetos isolados.** Opening, Loop, Manifesto não herdam narrativa/timing/regras de cue; compartilham só biblioteca de assets/identidade/componentes aprovados.

**Roteamento (ver [[../concepts/audiovisual-execution-router]])**
`TRABALHO → MOTOR → MODELO`. Remotion = sistema/componentes (V4 slots, escala 2 = 4K nativo). **Motor V2 (Python/PIL)** = motions já definidos na V2 (re-render nativo 1080p; 4K = ampliação 2×, ver limite). HyperFrames = **CANDIDATE** p/ motion editorial com direção de arte pronta (benchmark de bandeiras não virou entrega). FFmpeg/ffprobe = processamento, composição de decisão já tomada e QA. Motion Canvas = especialista, fora do default.

## 3. O que funcionou × o que falhou

| Funcionou | Falhou / gerou retrabalho |
|---|---|
| Corrigir componentes isolados; Gabriel decidindo no Premiere | Reconstruir montagem que o Premiere já resolvia; tratar bruto acima da edição humana |
| Remotion/V2 para motions definidos; FFmpeg p/ QA e composição técnica | Contexto gigante, sessões longas, subagentes em excesso |
| Proxies leves → aprovação → 4K só do aprovado | Reprocessar o que já foi analisado; auditoria durante fechamento |
| Layers com alfa; V2 como DNA; checkpoints + non-negotiables | Versão inteira para corrigir detalhe pequeno |
| Opening × Loop separados, Loop reusando identidade | SSD acumulando ~31 GB de mídia; workspace de código misturado com storage permanente |

## 4. Abandonment Check

Varredura em CLAUDE.md, `wiki/roadmap`, `concepts`, `principles`, `tools`. (O item de backlog "Abandonment Check" não tinha página própria — critérios = as 5 categorias do pedido.)

| # | Tipo | Ocorrência | Evidência | Decisão |
|---|---|---|---|---|
| 1 | REGRA OBSOLETA | `checkpoint.md`: "VIDEO DISABLED = SLOT OBRIGATÓRIO", "P0 entrega 08/10", "Claude não exporta 4K" | NON_NEGOTIABLES §3: slots não são o único lugar de motion; EP300 fechado; 4K de componentes foi gerado por Claude (master é do Gabriel) | **DEPRECATE** (checkpoint reescrito) |
| 2 | DECISÃO ÓRFÃ | Router datado "26/10/2026" | data impossível (hoje 03/10) | **DEPRECATE** (corrigido p/ 03/10/2026) |
| 3 | REDESCOBERTA | Motor V2 (Python/PIL) produziu a maior parte dos layers e dos re-renders; wiki só documentava Remotion/HyperFrames | `v2/engine.py`, `review01/b2`, `b3` | **DOCUMENT** (router + este doc) |
| 4 | REGRA ABANDONADA | `hyperframes.md` "Pendente: FFmpeg" | FFmpeg instalado e usado em todo o EP300 | **DEPRECATE** |
| 5 | REGRA ABANDONADA | `roadmap-automacao.md` (jun/2026): híbrido Adobe+Remotion, sem router/HyperFrames, Opus Clip como ponto de entrada | Router 02/10 + EP300 | **DOCUMENT** (banner de supersessão; plano A–E preservado) |
| 6 | EXCEÇÃO VIRANDO PADRÃO | Layers por "matte" extraído de render V2 (C06_03_*) | recortes ruins visíveis; refeitos nativos na R03 | **DEPRECATE** matte; re-render nativo é o padrão |
| 7 | EXCEÇÃO VIRANDO PADRÃO | "Remontar via FFmpeg" (V4 assembly) | REJEITADA (`DO_NOT_USE_AS_BASELINE`) | **DEPRECATE** (já está no router §4) |
| 8 | DECISÃO ÓRFÃ | Lora (design-video × marca-metricas-boss × sistema-marca) | marca-metricas-boss: Lora saiu jul/2026; design-video já acompanha | **DOCUMENT** resolvido (prevalece o mais recente até confirmação do time) |
| 9 | CONTRADIÇÃO | `production-model`: "workspace" × "Drive" sem regra de precedência | EP300 acumulou 31 GB local | **RESTORE** a intenção (Drive = source of truth, CLAUDE.md §Source of truth) + **Drive First** (§5) |
| 10 | DECISÃO ÓRFÃ | "MB Studio V2 FROZEN" sem razão escrita | — | **DOCUMENT** (§6) |
| 11 | REGRA ABANDONADA | `EXECUTION_READY = NO` do handoff EP300 | superado pelo fechamento | **DEPRECATE** (handoff já tem bloco de fechamento) |
| 12 | REDESCOBERTA | Princípio 14 "O Studio é a interface humana" × EP300 revisado por proxy + Premiere | Studio só serviu em Shared Review (EP289/CRO07) | **DOCUMENT** (§6; sem mudar o princípio) |
| 13 | IGNORE | Cursos Prime, CRO Talks system, Team Workspace, Copilot 04 V2 | PAUSADO consciente (princípio 8) | **IGNORE** |

## 5. Regra universal — DRIVE FIRST (incorporada em CLAUDE.md)
`DRIVE = CASA DO PROJETO · SSD LOCAL = BANCADA TEMPORÁRIA`. Local: código, scripts, `.md`, handoffs, configs, manifests/mapas. Drive: mídia original, assets, áudio, stickers/logos, projetos editáveis, layers finais, renders reutilizáveis, masters. Fluxo `DRIVE → LOCAL TEMP → PROCESSAMENTO → DRIVE → VALIDAÇÃO → LIMPEZA LOCAL`; `COPIAR → VALIDAR → MARCAR SEGURO → (aprovação) APAGAR`; nunca apagar a única cópia. Antes de gerar arquivo pesado: persistente? já existe no Drive? destino? precisa ficar local?

## 6. Backlog documental pós-EP300 (itens do checkpoint 03/10)
1. **Notion Skills/Nina** — síntese: já em CLAUDE.md § Operação Notion Skills + [[../concepts/tarefas-x-acervo-encomendas]]. Sem duplicar; Claude/Studio = execução, não duplicar a automação. Integração segue adiada (observar uso real). **DOCUMENT/feito.**
2. **Marco Pós-Lucian + 5 princípios** — fonte única = CLAUDE.md § Marco Arquitetural; os 5 princípios entram na lista de regras operacionais acima (1, 2/5, 9). Sem página nova.
3. **roadmap-automacao** — banner de supersessão (item 5 do Abandonment).
4. **design-video/Lora** — resolvido (item 8).
5. **production-model Drive × local** — ponteiro para Drive First.
6. **MB Studio V2 — por que está congelado:** (a) reunião Lucian (30/09) pôs a infra dele como foundation candidata (contratos, servidor, custos, ownership ainda a investigar) — construir Studio V2 agora arrisca clone/retrabalho; (b) o EP300 foi entregue com Premiere + Claude CLI + Remotion/FFmpeg, sem depender do Studio (a evidência não pede features novas); (c) custo R$ 0 adicional. **Dependências p/ descongelar:** decisão sobre a infra Lucian + EP291 integration test com métricas (Human Touch Time, correções humanas, etapas automatizadas, custo/contexto) + fluxo Notion→execução→review→Notion provado. **Descobertas alimentam o Studio; não viram features imediatas.** Não construir "Studio V2" nem V3.

## 7. Próximos passos (nada executado além de inventário/plano)
Reconciliação LOCAL ↔ DRIVE do EP300: plano pronto, **aguardando aprovação do Gabriel** antes de copiar/mover/apagar. Depois: EP291 como integration test; Loop e Opening como biblioteca de componentes.

Fonte: [[../../projects/ep300-cinema-opening/EP300_CHAT_CLEAR_HANDOFF]] · [[../concepts/principios-confirmados-ep300]]
