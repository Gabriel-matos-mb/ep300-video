# TRILHA — como o vídeo do EP300 chegou até aqui

Cronologia de decisões e entregas. Cada versão é **versionada**: feedback de uma versão não vale automaticamente para a seguinte.
Detalhe por fase: `opening/STATUS.md`, `opening/V0_EDIT_PLAN.md`, `V1_…`, `V2_…`, `opening/EP300_CHAT_CLEAR_HANDOFF.md`,
`opening/EP300_V4_MOTIONS/EP300_DECISIONS_LOG.md`, `docs/wiki/ep300-closeout-consolidation.md`.

## Linha do tempo

| Data (2026) | Marco | Artefatos | Onde está |
|---|---|---|---|
| 28/09 | **Gravação** (3 câmeras: CAM_GERAL + Gustavo + Lucian). **V0** proxy 5:32 — primeira montagem criativa, 8 achados de QA. | `opening/v0/`, `V0_EDIT_PLAN.md` | brutos em `01_BRUTOS/`; XML em `02_PROJETOS/EP300_ABERTURA_V0` |
| 29/09 | **V1** (5:48): direção do Gabriel aplicada (48 marcadores + Lumetri por câmera). **Sync corrigido**: imagem da CAM_GERAL vinha ~5 quadros atrasada em relação ao áudio (medido; lag residual ≤ 25 ms). | `opening/v1/`, `V1_EDIT_PLAN.md` | `02_PROJETOS/EP300_ABERTURA_V1`, `V1_GERADOS` |
| 29/09 | **V2** (6:10) — **baseline criativa aprovada**: cold open (erro + reação + risada), "aviso antes da sessão" falado para a sala, telas cheias encadeadas por empurrão, SFX novos + ducking, logos reais, evolução do programa com frames do arquivo histórico, "a volta do Lucian", LAYLA com Y. | `opening/v2/` (motor Python), `V2_EDIT_PLAN.md`, `handoff-2026-09-30/opening-editable/` | `V2_GERADOS` (44 overlays ProRes 4444), proxy `EP300_ABERTURA_V2_PROXY.mp4` |
| 29/09 | **Loop** V0→V1→V2: mosaico de acervo (92 cartões), patrocinadores modulares, microgags; V2 = sem microgag do cursor (cinema ≠ interface). | `loop/versions/scene_V0..V2.json` | `02_PROJETOS/EP300_LOOP_V0..V2` |
| 30/09 | **Reunião com Lucian** — redirecionou a arquitetura (contexto + exemplos humanos + assets + regras + componentes → execução). Handoff v1 para o Lucian. | `handoff-2026-09-30/` | `EP300_HANDOFF_LUCIAN/` |
| 01–02/10 | **V3 preflight** e **V4**: Premiere do Gabriel vira autoridade (sequência `MVI_9939`, 5:15, 101 cortes, 11 slots de câmera desativada). Motions dos slots em **Remotion**. NON-NEGOTIABLES, Migration Map V2→V4 (44 overlays, 74 SFX), 8 casos V2×V4 resolvidos. | `opening/v3-preflight/`, `opening/EP300_V4_MOTIONS/`, `EP300_NON_NEGOTIABLES.md` | — |
| 02–03/10 | **Review 01 → 02 → 03** (`V4_PRESENTABLE_REVIEW_01/02/03.mp4`) com 26 redlines do Gabriel (17 resolvidos como anti-regressão). Correções 4K por componente: `C02_03` (print novo do EP1), `S10` (JUL 2026), `O01`/`O02` (DeLorean de frente, sofá), `S05_FIX_TACI`. Balde de pipoca trocado pelo A "EPISÓDIO 300". | `opening/review01/` (`build_xml.py`, `compose_video.py`, `mix_audio.py`, `cues_final.json`, `editable_r03/timing_map_review03.json`), `EP300_V4_REDLINES.md` | `R03_LAYERS`, `R03_COMPONENTES_FINAIS_4K`, `02_PROJETOS/EP300_ABERTURA_R03_EDITAVEL` |
| 03/10 | **Loop final (V3)**: sobre o V2 — créditos Realização/Patrocínio/Café/Apoiador (Kinoplex branco, Onfly inteira), balde EP300 A, 3 pipocas escapando, 4 microgags. Aprovado e exportado 1080p + 4K. **Fechamento** + consolidation pass + reconciliação de storage (Drive First). | `loop/`, `docs/wiki/ep300-closeout-consolidation.md` | `03_EDITADOS/VERSÃO FINAL/` |
| 05/10 | **Abertura final** exportada do Premiere do Gabriel: `ABERTURA-EP300 - VF EM 4Q.mp4` e `…FULL HD.mp4`. | — | `03_EDITADOS/VERSÃO FINAL/`; projeto `02_PROJETOS/ep 300 final.prproj` |

## Hierarquia de autoridade (quando houver conflito)
1. Decisões humanas explícitas do Gabriel → 2. **Premiere final do Gabriel** → 3. `EP300_ABERTURA_V2_PROXY` (baseline criativa) →
4. handoff visual oficial EP300/site → 5. nova gravação → 6. melhorias V4/redlines aprovadas → 7. Migration Map (só reconciliação).
Correções 4K por componente > Review 03; Premiere final > tudo. `EP300_V4_ASSEMBLY_REVIEW.mp4` = **rejeitado** (não usar como base).

## Arco macro do filme (travado)
Orientações de cinema → interação com a plateia → brincadeiras/personalidade → história/números/evolução → Episódio 300 → fechamento →
blooper final (P&B + reverb) → **Loop**. Blooper inicial: só o trecho "começou? começa de novo" + risada (nunca "tá no ar, tá valendo").
Duas funções de blooper distintas.

## Mapa de cenas (V2, 44 overlays)
Tabela completa cena → tempo → intenção: [`handoff-2026-09-30/manifest/timeline-notes.md`](../handoff-2026-09-30/manifest/timeline-notes.md).
Mapa V4 slot a slot (S01…S11): [`opening/EP300_V4_MOTIONS/EP300_V4_MOTION_MAP.md`](../opening/EP300_V4_MOTIONS/EP300_V4_MOTION_MAP.md).
Timeline real do Premiere: `EP300_V4_TIMELINE_MAP.md`. Roteiro oficial: Notion "Roteiro — Vídeo de abertura EP 300"; breakdown em `docs/wiki/ep300-roteiro-edicao.md`.

## Decisões LOCKED que o Lucian não deve reabrir
- **FUCKING / H7:** censurar com o tom divertido da V2 (bleep + reação 🙊), sem cortar a fala; remapeado para ~80,9 s.
- **GRITEM:** freeze de ~2–3 s para a plateia gritar; não comprimir por ritmo.
- **H4:** sem o carimbo "IA NA HOME DO GA". **H9:** "4 EM 10" só em INCREMENTALIDADE. **H10:** "meia-culpa" ancorada em 445,1–448,3 s.
- **Supercut** `BORDAO_SUPERCUT_158_cortes.mp4` = só arquivo de referência; **não inserir** por padrão.
- **Stickers** já feitos pelo Gabriel — conferir `stickers e emojis refeitos/` antes de dizer "faltando"; não regenerar os aprovados.
- **Institucional:** Realização Métricas Boss · Patrocínio Purple Metrics + Onfly · Café oficial Coffee++ · Apoiador Kinoplex (logo branco, sem sticker).
- Remapeamento por **fala/beat**, nunca por timecode antigo. Premiere = master; FFmpeg só utilidade/QA/transcode.

## Pendências que dependem de humano (estado em 03/10; confirmar se ainda valem)
Naming/logos finais de Purple Metrics e Onfly (provisórios) · logo MB Prime (ausente) · números falados × site (191/196, 140/146, 106/107 mil) ·
"mais de 100 países" × "mais de 110 países" (H2) · ouvir 412,3–414,1 s "De nada, por favor"/"Purple"? (H3) · SFX ainda não auditionados na sala ·
teste do Loop no projetor real do Kinoplex (brilho/contraste, safe area).

## Aprendizados (curtos)
Corrigir = re-renderizar **uma camada** · review leve (720p) → aprovação → 4K só do aprovado · medir antes de afirmar (bleep alinhado pelo espectro; flashes de
1 quadro achados por varredura automática) · asset aprovado nunca regenerado · Opening e Loop são projetos isolados que compartilham só identidade.
Detalhe: `opening/LEARNINGS.md`, `docs/wiki/principios-confirmados-ep300.md`, `docs/wiki/ep300-closeout-consolidation.md`.
