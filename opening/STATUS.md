# Status — EP300 Cinema Opening

> Snapshot para quem lê o repositório sem abrir o Studio. **A fonte viva é o Studio**
> (`studio/data/board.json` id `ep300-video-abertura`, página `#/ep300`) — este
> arquivo não substitui aquilo e pode ficar desatualizado; não editar como se fosse
> o estado real.

**Última atualização deste snapshot:** 2026-09-29 (tarde)

**V2 — Refinamento editorial e fechamento: entregue para revisão (READY_FOR_HUMAN).** Proxy 6:10 no Studio: EP 300 → V2 → ▶ Play/Revisão
(V0/V1 no mesmo player como histórico; achados versionados). Arco cinema (cold open com erro+reação+risada → "antes da sessão" falado para a sala →
… → 300 → vira o LOOP), telas cheias encadeadas por empurrão (sem câmera vazando — `v2/qa_leak.py`), safe area 90/54 px (`qa_cues_v2.py --safe`),
SFX novos + ducking, logos reais, evolução do programa com frames do arquivo histórico, "volta do Lucian", LAYLA com Y. Decisões em
[V2_EDIT_PLAN.md](V2_EDIT_PLAN.md); código em [v2/](v2/README.md). Editável: `02_PROJETOS/EP300_ABERTURA_V2/EP300_ABERTURA_V2.xml`.
Loop V2 (sem cursor, começa no quadro em que a abertura termina) em `ep300-cinema-loop`. Master NÃO renderizado. Pendências: MB Prime (logo),
patrocinadores provisórios, números × site, duração 6:10, SFX ainda não auditionados na sala.

---
**V1 — Direção do Gabriel aplicada: entregue para revisão (READY_FOR_HUMAN).** Proxy 5:48 no Studio: EP 300 → Versões →
▶ Revisar (V0 no mesmo player). Entradas: 48 marcadores do Gabriel no Premiere + Lumetri por câmera (backup em
`02_PROJETOS/BACKUP_INTERVENCAO_GABRIEL_V0_2026-09-29`). **Sync corrigido**: imagem da CAM_GERAL chegava ~5 quadros atrasada
em relação ao áudio (captura) — medido e revalidado (lag residual ≤ 25 ms). Decisões em [V1_EDIT_PLAN.md](V1_EDIT_PLAN.md);
código em [v1/](v1/README.md) (V0 intacta em v0/). Editável: `02_PROJETOS/EP300_ABERTURA_V1/EP300_ABERTURA_V1.xml` +
`00_ASSETS E INSERTS/V1_GERADOS`. Handoff do Studio corrigido: `#/ep300` não abria o player (versão era só texto).
Master NÃO renderizado. Pendências: logos oficiais, MB Prime, fotos Guta/Lucas, números × site, duração.

---

**V0 — Primeira montagem criativa: entregue para revisão (READY_FOR_HUMAN).**
Gravação feita em 28/09 (3 câmeras). V0 proxy 5:32 no Studio (Produção EP300 → Revisão → "EP300 — Vídeo de
Abertura" · V0), 8 achados de QA para responder. Mapa narrativo em [V0_EDIT_PLAN.md](V0_EDIT_PLAN.md); fonte
editorial/código em [v0/](v0/README.md). Editável no Premiere: `02_PROJETOS/EP300_ABERTURA_V0/EP300_ABERTURA_V0.xml`
(Drive) + overlays ProRes 4444 alpha em `00_ASSETS E INSERTS/V0_GERADOS`. Master 1920x1080 NÃO renderizado.

**Pendências abertas:** números falados × site (16/40+, 106K/107K, 191/196, 140/146); duração 5:32 vs ~2 min do
guia; confirmar nomes nos recados (Purple/"Guta", Laila) e o produto de "jun/2026"; site ao vivo/Figma não
acessados (handoff bastou); safe area/som da sala seguem no QA final.

---
Histórico do snapshot anterior (antes da gravação):



**Direção visual:** definida em nível de tom (colagem/documentário, leve, ref.
Johnny Harris) — tratamento de números como marca-texto laranja MB + circulado à
mão. Linguagem visual detalhada **provisória**, aguardando o site do EP300 (ver
[VISUAL_SYSTEM.md](VISUAL_SYSTEM.md)).

**Roteiro:** breakdown operacional completo (cold open → 5 atos → epílogo) em
[wiki/concepts/ep300-roteiro-edicao.md](../../wiki/concepts/ep300-roteiro-edicao.md).
3 trechos com comentário editorial aberto.

**Bloqueios reais:**
- Nenhum bloqueio total. Gravação (cold open/falas em câmera) é hoje, 28/09, 16h-17h
  (confirmado pelo Gabriel) — não iniciar pós-produção antes disso.
- Sem acesso ao site do EP300 (Claudio/Lucian) — não bloqueia roteiro/preparação.
- Resolução/safe area/som da sala: playback e entrega já confirmados (1920x1080
  16:9 MP4, ver PRODUCTION.md); safe area e sonorização finas ainda em aberto, mas
  só afetam o QA final, não a edição.

**Escopo (28/09):** o EP300 tem dois deliverables — vídeo de abertura (este projeto)
e vídeo de looping do telão (produção separada, `ep300-video-looping` no board, sem
conceito ainda, não é prioridade de hoje). A captação do podcast em si (4 câmeras,
áudio, fotografia) é da produtora — não é tarefa do Gabriel; ele leva um SSD externo
para copiar o bruto 4K LOG dela (~300GB) no fim do evento (08/10) — confirmado pela
visita técnica de 25/09.

**Próxima ação concreta:** gravação do vídeo de abertura hoje, 16h-17h. Depois:
inventário de assets visuais/logos/fotos e pedido de acesso ao site do EP300.
