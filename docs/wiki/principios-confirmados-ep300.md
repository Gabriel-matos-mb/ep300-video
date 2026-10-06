# Princípios confirmados pelo trabalho real — EP300, Manifesto, Copilot

Consolidação de 29/09/2026 de aprendizados validados durante a produção do EP300 Cinema Opening (V1 → V2 → validação Gustavo/Lucian), Analytics Summit Manifesto (V1 Claude → V2 Gabriel) e Analytics Copilot 04.

Fonte: [[../../CLAUDE.md]] § Princípios confirmados (resumo); este documento expande cada um com contexto, contraexemplo e por que importa.

---

## 14 Princípios

### 1. FILE EXISTS ≠ DELIVERED

**O quê:** Um arquivo gerado e salvo em disco não é sinônimo de entrega operacional.

**Contexto:** EP300 V2 render concluído em 24/09 → arquivo existe em `projects/ep300-cinema-opening/v2/` → mas não foi assistido, não foi validado contra critérios editoriais, não foi aprovado por Gustavo e Lucian. A existência de arquivo foi confundida com "pronto".

**Impacto:** Sem essa distinção, código ou design que roda sem erro é marcado como "feito" e handoff para review acontece errado — humano não consegue validar porque pressupostos técnicos não foram testados.

**Como reconhecer:** Pergunta: "alguém humano já viu e aprovou isto?" Se não, ainda não está delivered, mesmo que arquivo exista e seja tecnicamente correto.

**Aplicação:** Sempre: "arquivo existe" → "validação humana" → "aprovação" → "entrega documentada".

---

### 2. RENDER COMPLETE ≠ HANDOFF COMPLETE

**O quê:** Um render terminou no FFmpeg/Remotion/Premiere não é igual a "material pronto para humano usar".

**Contexto:** EP300 V2: renders H264 prontos para revisão. Mas Gabriel descobriu que direção de câmera, leitura de teleprompter e "naturalidade" da performance ainda tinham pontos que preferiu revisar antes de rodar a próxima rodada inteira de refinamentos — render técnico não captura tudo.

**Impacto:** Confundir render completo com "pronto" acelera iterações erradas — humano quer refinar performance, não quer refazer timecode ou codec.

**Como reconhecer:** Pergunta: "o render passou em QA técnico (codec/resolução/duration/áudio)?" vs. "alguém validou a performance/conceito/decisão criativa?" São revisores e critérios diferentes.

**Aplicação:** QA técnico sempre; depois QA de escopo (faz o que foi pedido?); depois QA editorial (é bom?).

---

### 3. QA TÉCNICO ≠ QA DE ESCOPO ≠ QA EDITORIAL

**O quê:** Três camadas de validação, cada uma com critério e revisor diferentes.

**Contexto:** Manifesto V2: Claude gerou inserções e gráficos. Gabriel revisor técnico conferiu: "codec OK, áudio sincronizado, sem crash." Mas descobriu depois que V2 seguia diferentes (e melhores em alguns pontos, piores em outros) que V1 — isso é QA de escopo ("segue o pedido?"), não QA técnico. Depois Gabriel tem que fazer QA editorial ("é bom visualmente?").

**Impacto:** Pular camadas = descobrir problemas tarde. Fazer tudo como QA editorial = nunca sai do draft.

**Como reconhecer:** 
- QA técnico: "funciona?" (codec, sync, não há erro).
- QA escopo: "faz o que foi pedido?" (brief atendido, decisões implementadas).
- QA editorial: "é bom?" (julgamento, gosto, narrativa, ritmo).

**Aplicação:** Sempre em ordem. QA técnico passa → QA escopo passa → QA editorial passa = vai para delivery.

---

### 4. READY_FOR_HUMAN ≠ APROVADO ≠ MASTER ≠ FINAL

**O quê:** Quatro estados bem distintos; confundir aumenta retrabalho exponencialmente.

**Contexto:** EP300: "READY_FOR_HUMAN" = "Claude fez a parte, humano quer ver/revisar agora". Não = aprovado. V1 foi ready_for_human → Gabriel viu → rejeitou por problemas de direção → V2 ready_for_human → Gabriel viu → pediu refinamentos. Apenas DEPOIS V2 com refinamentos = "APPROVED" (Gabriel e co-reviews concordam). Depois sim, é candidata a MASTER (versão que será usada). E só depois do render final + arquivo liberado = FINAL.

**Impacto:** Se chamar V2 de "aprovado" quando é só "ready_for_human", cria expectativa errada — "já tem OK?" → "não, só pronto pra revisar" → desconforto operacional.

**Como reconhecer:**
- **READY_FOR_HUMAN**: output do pipeline pronto, artefatos completos, esperando review.
- **APPROVED**: humano(s) revisaram e concordaram explicitamente.
- **MASTER**: versão que será usada em produção (pode haver múltiplas versões aprovadas).
- **FINAL**: released, arquivo deletável com segurança (backup preservado), pronto para consumo.

**Aplicação:** Usar termo certo em cada etapa. No Studio/Notion, marcar estado certo reduz confusão.

---

### 5. REVIEW É VERSIONADA

**O quê:** Feedback de uma versão é específico dela; não transfere automaticamente para versão seguinte.

**Contexto:** Manifesto V1 Claude: Gabriel apontou 10 achados (som/cortes/ritmo/gráficos). V2 Claude: feito sobre feedback de V1, corrigiu vários, mas Gabriel descobre que alguns "achados" de V1 — que ele considerou importantes — sumiram silenciosamente (porque Claude interpretou diferente). V1 feedback agora é obsoleto; V2 precisa de review novo.

**Impacto:** Sem registrar "que feedback era específico de V1", humano não consegue rastrear se V2 de verdade incorporou a direção dele, ou apenas interpretou diferente.

**Como reconhecer:** Cada versão tem seu próprio histórico de feedback. Ao passar para V2, copiar feedback relevante e marcar "origem: V1, ainda aplicável? (sim/não/parcial)".

**Aplicação:** No Notion/Studio, feedback fica atrelado à versão. V2 = nova etapa de review, não iteração silenciosa de V1.

---

### 6. HISTÓRICO ≠ PENDÊNCIA ATIVA

**O quê:** Trabalho antigo em git/archive não é o mesmo que tarefa aberta no Notion/Studio agora.

**Contexto:** Continuation Engine V0 (23/09) teve bug: snapshots manuais de 22/09 com 3 tarefas já concluídas no Notion continuavam marcadas como "em execução" em Atenção — o snapshot era histórico, não fonte viva. Reconciliar Estado de Atenção com Notion atual ficou impossível sem distinguir: "isso já foi feito (arquivo no git)" vs. "isso está aberto (Notion agora)".

**Impacto:** Repetir trabalho antigo ou deixar tarefa antiga aberta por confusão = perda de tempo e confiança no sistema de tarefas.

**Como reconhecer:** Snapshot/arquivo antigo ≠ Notion/board vivo agora. Source of truth para o que está aberto agora é o board, não o histórico.

**Aplicação:** `continuation.js` reconcilia Notion (vivo) com snapshots históricos; não o contrário.

---

### 7. TIMECODE ANTIGO ≠ TIMECODE NOVO

**O quê:** Se um vídeo foi reeditado ou comprimido, timecodes de referência antiga não valem mais.

**Contexto:** EP300 V1 tinha timecode específicos para inserts (Ato I em 01:15, Ato II em 03:45, etc.). Ao fazer V2 com diferentes câmeras e direção, timecodes mudaram (Ato I em 01:22, Ato II em 03:58). Referências visuais da V1 ("coloca o gráfico em 02:30") não funcionam em V2 sem reconciliação — o gráfico em 02:30 da V1 cai no meio da frase em V2.

**Impacto:** Sem reconciliar timecodes, feedback e assets da versão anterior viram ruído quando aplicados à versão nova.

**Como reconhecer:** Cada versão do vídeo principal = novos timecodes para todos os inserts/gráficos relacionados.

**Aplicação:** Ao reeditarfacto: revalidar timecodes, reconciliar referencias, comunicar mudanças.

---

### 8. PAUSED ≠ FORGOTTEN

**O quê:** Trabalho pausado conscientemente continua sendo ativo na arquitetura; não desaparece.

**Contexto:** Curso Estatística foi pausado por prioridade (EP300 saiu na frente). Mas está documentado em [[../concepts/curso-prime-preparacao-editorial]] com: aprendizados validados, piloto concluído (Aula 03), próximos passos claros. "Pausado" ≠ "cancelado". Auto Adjust segue na mesma situação: pausado, não deletado do roadmap.

**Impacto:** Sem essa distinção, voltar a um projeto pausado = reconstruir contexto do zero; contexto já existe, só não está sendo executado agora.

**Como reconhecer:** Pausado tem documentação, data, motivo, próximos passos. Cancelado é explícito ("não vamos fazer isso").

**Aplicação:** Roadmap/checkpoint: pausado = H3/LATER; ativo = H1/H2/NOW.

---

### 9. ROADMAP ≠ CHECKPOINT

**O ququê:** Roadmap é intenção durável (o que queremos construir); checkpoint é estado operacional semanal (o que estamos fazendo agora).

**Contexto:** MB Studio Product Roadmap (23/09 em diante) lista H1/H2/H3/Backlog — visão de longo prazo. Checkpoint (semanal, sobrescrito) tem "agora: EP300, Manifesto, Copilot" vs. "pausado: Curso, Auto Adjust". Parecem conflitantes, mas não são — checkpoint mostra a rota atual dentro do roadmap.

**Impacto:** Confundir os = achando que roadmap "sumiu" porque não está no checkpoint da semana, ou achando que tudo do roadmap é urgente agora.

**Como reconhecer:** Roadmap é consolidação (cresce, nunca diminui, muda com decisão explícita). Checkpoint é snapshot (muda toda semana, é leitura rápida do "e agora?").

**Aplicação:** Antes de redesenhar algo, ler o backlog de roadmap relacionado — muitas ideias velhas ali resolvem o problema novo.

---

### 10. CAPACIDADE DISPONÍVEL ≠ PRÓXIMA AÇÃO REAL

**O quê:** "A gente pode fazer X" não é o mesmo que "X é a próxima coisa que devemos fazer agora".

**Contexto:** Studio pode rodar edições, gerar thumbnails, transcrever, automatizar nomenclatura de pastas. Tudo "pronto tecnicamente". Mas prioridade de 29/09 é: EP300 (H1) antes de Auto Adjust (H3) antes de GPU optimization (LATER). Tecnicamente possível ≠ prioridade agora.

**Impacto:** Sem essa distinção, roadmap vira fila infinita; tudo "pronto" é confundido com tudo "urgent".

**Como reconhecer:** Pergunta: "qual problema do Gabriel isto resolve AGORA?" vs. "qual problema poderia resolver no futuro?"

**Aplicação:** Checkpoint responde a pergunta; roadmap lista o resto.

---

### 11. EDITABILIDADE É PARTE DA ENTREGA AUDIOVISUAL QUANDO APLICÁVEL

**O quê:** Quando humano vai refinar material após entrega, arquivos devem ser editáveis (XML/FCP), não só renders finais.

**Contexto:** Manifesto V2: Gabriel recebeu Claude V2 (nova concepção). Mas como? Se só render MP4, não consegue refinar; como Gabriel edita no Premiere? Necessário: entregar também XML/FCP (arquivo editável Premiere), áudio stems (não mixado), gráficos em camadas (não flattened), assim Gabriel consegue refinar sem reconstruir.

**Impacto:** Sem editabilidade, humano é forçado a "aceitar como está" ou refazer do zero — não pode refinar iterativamente.

**Como reconhecer:** Ao entregar audiovisual para humano editar: sempre incluir arquivo editável + stems/camadas.

**Aplicação:** Manifesto: entrega = `MANIFESTO_V2.xml` (Premiere) + áudio stems + gráficos em Figma/After Effects editáveis.

---

### 12. HUMAN EDIT ≠ FIM DO LOOP DE IA

**O quê:** Quando Gabriel edita algo no Premiere após receber de Claude, essa alteração é informação editorial valiosa que deveria retornar ao loop de aprendizado.

**Contexto:** Manifesto: Gabriel recebe V2 → abre no Premiere → refina som, timing, gráfico → salva nova versão. Esse refinamento é feedback silencioso — "essas mudanças que Gabriel fez" = "o que Claude deveria ter feito diferente". Hoje é histórico; futuro desejado: Claude consegue ler edições de Gabriel e aprender.

**Impacto:** Sem capturar feedback humano implícito, o loop de aprendizado é limitado a feedback explícito ("mude X para Y").

**Como reconhecer:** Sempre: "what did the human actually do to the artifact?" = feedback valioso, mesmo que não escrito.

**Aplicação:** Future roadmap: diff do XML do Premiere antes/depois = "mudanças que Gabriel fez" → análise de padrão → aprendizado.

---

### 13. CONFLICT ≠ BLOCKED

**O quê:** Uma dependência só bloqueia o que realmente depende dela; não bloqueia frentes paralelas.

**Contexto:** EP300: gravação de Gustavo marcada para 28/09 (depois 29/09). Isso bloqueia "vídeo final com Gustavo em câmera", mas NÃO bloqueia "roteiro de edição", "inventário de assets", "pedido de acesso ao site do EP300", "pesquisa de logos de empresas". Continuation Engine V0 primeiro bug: marcava EP300 inteiro como BLOCKED porque gravação pendente — incorreto.

**Impacto:** Se tudo fica BLOCKED por uma dependência parcial, equipe fica parada quando poderia avançar em paralelo.

**Como reconhecer:** Sempre: "isto realmente depende do Y para andar?" vs. "isto é independente de Y e pode andar em paralelo?"

**Aplicação:** `continuation.js` agora lê quais materiais de cada produção dependem do que, marca bloqueio só quando TODOS os materiais estão presos.

---

### 14. O STUDIO É A INTERFACE HUMANA

**O quê:** Filesystem, scripts, JSON, renders, FFmpeg, XML, automações são infraestrutura. O Studio é a superfície humana que ordena tudo.

**Contexto:** Quando Gabriel quer verificar status de EP300, ele não quer entrar em terminal rodando `ls projects/ep300-cinema-opening/`. Ele abre Studio, vê a produção, clica "Revisar", vê todos os assets e contexto. Isso é a interface humana. Filesystem/scripts são means, não ends.

**Impacto:** Sem essa clareza, subestima-se a importância da interface — "o código rodou certo" não é o mesmo que "Gabriel conseguiu ver e agir".

**Como reconhecer:** Pergunta: "Gabriel consegue fazer isto clicando no Studio?" vs. "Gabriel precisa entrar em terminal?"

**Aplicação:** Toda automação → Studio interface para resultado; todo asset armazenado em disco → renderizado e acessível no Studio.

---

## Aprendizados Audiovisuais — EP300 V1→V2→Validação

### Direção de câmera e naturalidade

- Câmera técnicamente superior (sharp, iluminação balanceada) pode ser editorialmente pior se performance parece forçada.
- Direção do olhar importa muito — câmera que captura olho direto para câmera vs. pensativo vs. lendo teleprompter são bem diferentes.
- Câmera geral (plano aberto) pode ser preferível quando performance visual está artificial — dá espaço para naturalmente ser.

### Leitura de teleprompter

- Leitura evidente = aviso editorial imediato.
- Sincronizar VO com vídeo: validar no início, meio e fim (não só no render final).

### Sync e timing

- Distinguir offset constante (+ 200ms sistemático) de drift progressivo (começa sync, termina desincronizado).
- Retranscrever o corte final pode funcionar como QA de conteúdo — "o que realmente foi dito?" vs. "o que o teleprompter planejou?".

### Fullscreen + VO

- Fullscreen (tela cheia do apresentador) + voice-over pode resolver trechos em que performance visual está menos natural — foco na voz, não na imagem.

### QA técnico ≠ QA editorial

- Melhorias técnicas de imagem (nitidez, contraste) ≠ recriação da pessoa/performance.
- Filtros/efeitos aplicados uniformemente podem ser piores que deixar grão natural.

### Assets e Reutilização

- Assets existentes/licenciados podem ser descobertos e reutilizados autonomamente sem novo custo (Motion Array já licenciada).
- Buscas curadas em Drive (saber onde procurar: "esse episódio de 2024, essa pasta específica") são melhores que varreduras gigantes.

### Stickers e Identidade

- Stickers devem preservar identidade (quem é?), proveniência (de onde é?), reutilização (como reaproveitar?).
- Não criar por coleção; criar por necessidade narrativa (cena → pessoa → sticker).

### Projeto editável

- Projeto Premiere (.prproj) + áudio stems é importante para continuidade humana.
- "Entregar render" sem arquivos editáveis = Gabriel não consegue refinar.

---

## Aprendizado do Manifesto — V1 Claude → V2 Gabriel

Claude consegue:
- Explorar conceitos, gerar possibilidades editoriais.
- Executar montagem e gráficos.
- Produzir uma base editável.

Mas refinamento subjetivo não deve necessariamente gerar sucessivas rodadas caras de inferência.

**Fluxo validado**: IA gera base → humano refina diretamente no ferramenta de edição (Premiere) → resultado final.

**Futuro desejado (não implementar agora)**: Gabriel modifica no Premiere → sistema consegue compreender as alterações → aprendizado retorna ao loop Claude.

---

## Métrica Experimental: Human Touch Time

Wall-clock time da automação não deve ser avaliado isoladamente. **Importa quanto tempo humano ativo foi necessário** para dirigir, corrigir e concluir o trabalho.

Exemplo EP300: render técnico 4 horas, mas Gabriel 3 horas de revisão → "custo" real é 3h, não 4h.

---

## Fonte

[[../../CLAUDE.md]] (registrado 29/09/2026); detalhes em checkpoint/roadmap históricos (git).

Consolidado para futuro: incorporar aprendizados em refine de processo, Skills, Premiere/automações, caso de transformação do fluxo ([[case-transformacao-fluxo-ia]]).
