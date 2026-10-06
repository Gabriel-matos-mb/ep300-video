# EP300 — NON-NEGOTIABLES (leitura OBRIGATÓRIA antes de qualquer execução da Abertura)

> Criado em 02/10/2026 a partir da consolidação de autoridade pedida pelo Gabriel, após perda de contexto entre sessões.
> Pergunta que este documento responde: **"Antes de tocar no EP300, o que eu não tenho autorização para esquecer, reinterpretar ou destruir?"**
> Detalhes ficam nos documentos especializados (Migration Map, Asset Map, Redlines). Aqui só os locks.

## 1. Hierarquia de autoridade
1. Decisões humanas explícitas / LOCKED do Gabriel
2. Premiere atual editado pelo Gabriel (cortes, multicam, enquadramento, cor, áudio, markers)
3. `EP300_ABERTURA_V2_PROXY` + estrutura criativa aprovada anterior
4. Handoff visual oficial EP300/site
5. Nova gravação
6. Melhorias/redlines V4 aprovadas
7. `EP300_V2_TO_V4_MIGRATION_MAP` (mapa de reconciliação)

Uma camada inferior **não** invalida silenciosamente uma superior.

## 2. Regra-mãe
A nova gravação **não** autorizou remontar o vídeo do zero. Ela melhora captação, qualidade, execução, falas atualizadas, brincadeiras regravadas e dados. A linguagem audiovisual aprovada permanece baseline.
- `EP300_ABERTURA_V2_PROXY` = BASELINE CRIATIVA.
- Premiere atual do Gabriel = BASELINE EDITORIAL/TÉCNICA.

## 3. KEEP BY DEFAULT — DROP BY EXCEPTION
Tudo que funcionava na V2 permanece. Só sai com uma destas classificações:
- `DROP_USER` — Gabriel pediu remoção.
- `DROP_SCRIPT` — a fala correspondente deixou de existir.
- `DROP_FACT` — a informação/dado ficou incorreto.
- `REPLACE_APPROVED` — substituição posterior **explicitamente aprovada** como melhor.

Sem isso: KEEP. "Não existe Disabled slot", "achei desnecessário", "simplifiquei", "não achei slot" **não** são motivos.
Disabled = momento de substituição integral da câmera. **Não** delimita onde overlays, inserts, tipografia, stickers, SFX ou intervenções podem existir.

## 4. O que a baseline criativa inclui
Ritmo, dinâmica, música, SFX, ducking, inserts, overlays, fullscreens, tipografia, stickers, punch-ins, brincadeiras, interação com plateia, estrutura narrativa, timing audiovisual, humor, quarta parede, payoff, identidade visual. Não simplificar por iniciativa própria.

## 5. Direção audiovisual
Não é "pessoa falando + gráfico em cima". Quando adequado: FALA → VO → MOTION/INSERT/CENA FULLSCREEN → volta à câmera quando VER A PESSOA acrescenta valor.
Fechadas valem em reação, brincadeira, interação, punchline, gesto, espontaneidade, quebra da quarta parede. Se a fechada denuncia TP, não é automaticamente a melhor escolha (geral/fullscreen/insert podem ser).

## 6. Música / SFX / desenho sonoro
Parte da CREATIVE_BASELINE. Preservar como referência autoritativa: trilha aprovada, posição e função da música, SFX, impactos, transições sonoras, ducking, relação fala/música/efeitos, silêncios intencionais.
Não trocar trilha nem reconstruir o desenho sonoro porque existe outra opção. Substituição relevante só se: pedida pelo Gabriel, necessária por mudança estrutural real, ou apresentada como alternativa para HUMAN_REVIEW. Nunca em silêncio. Não criar SFX nem escolher músicas novas.

## 7. Os cues da baseline (~39 no briefing antigo; 44 no manifesto V2_PROXY)
Cada cue é reconciliado **individualmente** — não some dentro de "inserts".
Classificações permitidas: `KEEP`, `MOVE`, `ADAPT`, `FULLSCREEN`, `OVERLAY`, `REPLACE_APPROVED`, `DROP_USER`, `DROP_SCRIPT`, `DROP_FACT`. Todo DROP leva motivo explícito.
O objetivo não é manter N elementos visíveis; é garantir que nenhuma decisão aprovada desapareça por acidente.

## 8. Remapeamento semântico
Timecode antigo **não** é autoridade na nova gravação. A unidade de continuidade é **INTENÇÃO / FALA / BEAT NARRATIVO**.
Decisão V2 → achar a fala/beat equivalente → remapear timing → adaptar duração → preservar a função.
Fala mudou levemente, mesma função: ADAPT/MOVE. Fala sumiu: DROP_SCRIPT. Dado mudou: atualizar o conteúdo mantendo a linguagem. Não remover porque o TC antigo não bate.

## 9. Premiere é autoridade
Não reconstruir câmera com FFmpeg. Não substituir multicam, cortes, enquadramento, rotação (2,2°), escalas (112 / 107,7 / 122,1%), Lumetri/cor, tratamento de áudio (88 filtros), markers, decisões manuais. Não sobrescrever `.prproj` humano.
FFmpeg = utilidade/QA/transcode. Premiere = master editorial. Entrega futura = **camada adicional** (XML/assets) para o Gabriel colar na sequência dele.

## 10. Identidade
Mesma casa visual do EP300/site/handoff: creme, laranja, preto, Sora/Inter, scrapbook, stickers, papel, pontilhado, humor editorial, rostos adesivados, comportamento visual do `/300`. Divergência V4 contra o handoff é **corrigida**, não vira nova linguagem.

## 11. Arco macro LOCKED
1. Orientações de cinema → 2. Interação com a plateia → 3. Brincadeiras/personalidade → 4. História/números/evolução → 5. Episódio 300 → 6. Fechamento → 7. Blooper final → 8. Loop.
A peça é exibida PARA PESSOAS DENTRO DE UM CINEMA. Avaliar também por: "isso funciona como interação com aquela plateia?"

## 12. Bloopers
- Inicial: só o trecho aprovado de Lucian "começou? começa de novo" + risada. Nunca "tá no ar, tá valendo".
- Final: preservar gag P&B + reverb antes do loop.
Duas funções distintas.

## 13. Assets novos
Biblioteca: Toddynho, DeLorean, Marty+Doc, balde, extintor, microfone, stickers existentes, futuras pipocas soltas. **Asset disponível não cria obrigação de uso.** Só quando acrescenta função narrativa. Não inventar asset reconhecível ausente. Ordem: oficial fornecido > antigo > emoji genérico > placeholder.

## 14. De Volta para o Futuro
DeLorean + Marty/Doc servem ao SETUP ("voltando no tempo") e/ou ao PAYOFF (ouvir até 2038). Não sobrecarregar ambos obrigatoriamente.

## 15. Kinoplex
APOIADOR do EP300. Só logo/asset oficial (branca, original). Nunca sticker, nunca redesenhar, nunca inventar. Atualização 03/10: a logo é a **branca da pasta `logos`**, sem sticker (LOCKED, §24); só um tratamento institucional que vá além disso continua `BLOCKED / WAITING DESIGN`.

## 16. Loop é outro deliverable
Não misturar com a execução da abertura. "Movimento é recompensa para quem percebe, não competição com o podcast."
Loop: calmo, silencioso, atmosférico, microgags espaçadas. Abertura: narrativa, música, SFX, ritmo, surpresa, interação.

## 17. Status das versões
| Item | STATUS |
|---|---|
| `EP300_ABERTURA_V2_PROXY` | CREATIVE_BASELINE_APPROVED |
| Premiere atual do Gabriel | EDITORIAL_TECHNICAL_AUTHORITY |
| `EP300_V4_ASSEMBLY_REVIEW` | REJECTED · DO_NOT_USE_AS_BASELINE: TRUE |
| V4 motions / redlines | SELECTIVE_IMPROVEMENTS |
| `EP300_V2_TO_V4_MIGRATION_MAP` | RECOVERY_RECONCILIATION_MAP |

## 18. Conflict rule
Instrução nova que conflite com este documento: **não escolher em silêncio.** Registrar `CONFLICT_WITH_LOCKED_RULE` e preservar o estado anterior até decisão humana.

## 19. QA
`TECHNICAL_QA` ≠ `EDITORIAL_QA` ≠ `CREATIVE_QA` ≠ `HUMAN_REVIEW`. "QA PASSED" nunca declara o vídeo criativamente aprovado.

## 20. Documentação não autoriza execução
Achar conflito, cue perdido, asset faltante, erro no Migration Map ou melhoria clara **não** autoriza corrigir. Registrar e parar. Sem editar Premiere, motions, áudio; sem renderizar, gerar proxy, rodar FFmpeg ou alterar o Migration Map.

## 21. Restrições permanentes já vigentes
Não modificar `.prproj` original (trabalhar em cópia) · não renderizar 4K/master/alfa final sem autorização · previews só 960×540 · nunca inventar nomes de pessoas ("Tasse" não existe; é Taciana/Taci) · STICKER_BOUNDS_CHECK (safe area 90/54 px) · cinema ≠ interface (sem CTA de clique/toque) · LAYLA com Y · "volta do Lucian".

## 22. PROJECT ISOLATION — EP300
Este projeto pertence **EXCLUSIVAMENTE** a:
- EP300
- Analytics Talks
- Evento Kinoplex

**Não importar** decisões, assets, linguagem ou regras específicas de:
- Analytics Summit Manifesto
- Manifesto V4
- Summit 2026
- Ou qualquer outro projeto MB

Semelhanças de ferramenta, workflow ou técnica **não autorizam** compartilhamento de decisões criativas entre projetos.

Se um arquivo/regra encontrado mencionar Manifesto ou Summit e **não estiver explicitamente referenciado pelo EP300**:
→ `IGNORE_AS_FOREIGN_PROJECT_CONTEXT`

**Nunca preencher lacuna do EP300 com decisão do Manifesto.**


## 23. PRE_EDITED_4K_SAFETY_MASTER (registrado 03/10/2026)
`01_BRUTOS/NOVOS TAKES-REGRAVADO/VIDEO PRE EDITADO CINEMA EP 300 EM QUALIDADE MAXIMA.mp4` = referência consolidada da edição do Gabriel (cortes, multicam, framing, cor, áudio). **Não** substitui o Premiere como autoridade editável e **não** autoriza flatten da entrega. Para base consolidada, **preferir este arquivo**; nunca reconstruir a edição a partir dos brutos 4K (divergência → a reconstrução está errada). Não reencodar nem alterar; validar apenas FILE_EXISTS / VIDEO_READABLE / RESOLUTION / FPS / DURATION / AUDIO_PRESENT quando a exportação terminar.

## 24. Locks de 03/10/2026
H7 "fucking" = censura divertida baseada na V2 (não genérica) · GRITEM = freeze ~2–3 s · institucional: PATROCÍNIO Purple Metrics + Onfly (logo inteira, sem crop) · CAFÉ OFICIAL Coffee++ · APOIADOR Kinoplex (logo branca, sem sticker) · REALIZAÇÃO Métricas Boss · supercut = REFERENCE_ARCHIVE · WORD/PHRASE EMPHASIS PASS = REQUIRED_BEFORE_FINAL_EXECUTION. Detalhes: `EP300_V4_MOTIONS/EP300_DECISIONS_LOG.md`.

## 25. Handoff do /clear (03/10/2026)
`EP300_CHAT_CLEAR_HANDOFF.md` é o checkpoint de retomada: autoridade, estado, locks, **registro das 26 imagens/redlines** (cópias em `EP300_V4_MOTIONS/redlines_source/`), institucional, assets, pendências humanas e "DO NOT REOPEN". Ler junto com este documento.
