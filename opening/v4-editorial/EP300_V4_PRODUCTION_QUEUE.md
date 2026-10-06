# EP300 V4 — Fila de produção

> 2026-10-02. Ordenada por dependência. **Nada daqui foi iniciado.** Prazo do evento: 08/10/2026.
> Itens de frentes diferentes **não se bloqueiam** (CONFLICT ≠ BLOCKED). Referências de beat = `EP300_V4_EDITORIAL_MAP.md`.

## 0. Pré-requisito técnico (1 linha de decisão)
**Spec da sequência: resolução e fps.** Master 4K 23,976 fps; overlays V2 saíram 1080p 30 fps. Recomendação: sequência **23,976 fps** (cadência nativa do master) e re-render dos overlays no mesmo fps/resolução. Detalhe em BLOCKERS B1.

## 1. PREMIERE — GABRIEL
1. **Salvar cópia local** de `ep 300 final.prproj` (o save no Drive falhou; o arquivo do Drive é stub de 15 KB sem edição) e trabalhar nela. Não escrever no Drive durante a edição.
2. **Sync das 3 câmeras 4K** pelo áudio, tendo a `MVI_9939` como referência. (Offsets antigos do preflight — Gustavo ≈ +2,54 s, Lucian ≈ −0,11 s — **não são confiáveis**.) Medir de novo o lead de 5 quadros da geral (`W_VIDEO_LEAD_FRAMES`).
3. **Montagem do diálogo** pela EDL E01–E12 do mapa (já descartando o ruído de set). Aplicar: pausa de 2,4 s (C2), respiro de 3 s (D5), troca de ordem C6→C7.
4. **Cortes de câmera** vendo o vídeo (geral frontal por padrão; fechadas em reação: C7, D9, F7, G1; punch-ins). 4K permite reenquadrar sem perda numa sequência 1080p.
5. Depois dos overlays: conferir sync visual e entregar XML editável (editabilidade é parte da entrega).

*Posso gerar a EDL como XML/FCPXML para você abrir no Premiere (revisão humana antes de usar).*

## 2. REMOTION / CODE
Depende de 0 (spec) e do passo 3 do Premiere (ou das âncoras por palavra em `transcript_new_geral.json`, que dispensam o timeline final).
1. `v4/plan.py` derivado de `v2/plan.py` (V2 intacta), cues ancorados por **palavra** (campo `st`/`tl` por fala), não por timecode antigo.
2. Troca de dado/texto e re-render **só dos overlays afetados** (cache por hash): C6, C9, D1, D3, D7, F2, F4 (dado) · B1, B4, D9, E5, E6, E7 (texto) · re-âncora de G2 e G4.
3. Re-render dos overlays no spec final (fps/resolução) — **todos**, se B1 mudar o spec.
4. Áudio: recalcular ducking −10 dB e âncoras de SFX (todas atreladas a cue); `BLEEPS` antigo sai; bleep novo só se H7 mandar.
5. QA: `qa_leak` (telas encostadas), safe area 90/54 px, `qa_reading` (≥0,35 s/palavra + 0,9 s em tela sem voz), sync.

## 3. ASSETS EXISTENTES — LOCALIZAR
- Overlays/inserts V2: Drive `02_PROJETOS/EP300_ABERTURA_V2` e `00_ASSETS E INSERTS/V2_GERADOS` (44 alpha) — conferir que estão íntegros antes de reaproveitar.
- Stickers e emojis refeitos (Guta, Lucas, Vitória, Mafê, Phill, Bonel, Layla, balde, viatura) e logos `…/logos`.
- Cold open de arquivo (`b0`), contagem, aviso, trilhas/SFX, `final_v2`.
- **Supercut**: assistir `BORDAO_SUPERCUT_158_cortes.mp4` (16:43) e escolher um trecho de ≈3–4 s para D1 (ou manter prints).
- **Frame histórico do cenário antigo / MesaCast** (B5, opcional): busca dirigida no arquivo oficial do podcast — não inventariar a pasta.

## 4. ASSETS NOVOS — CRIAR
- **Nenhum obrigatório.**
- Opcional: gag gráfica da piada de autoria dez/2024 (E6, H10).

## 5. FEEDBACK / DECISÃO HUMANA (ordem de impacto)
1. **H3** — ouvir 412.3–413.6 (2 s): é "Purple"? Define E4 (DROP\* ↔ ADAPT).
2. **H6 / G1** — fecho: confirmar passada 592–607 e ouvir o improviso hard/soft skill (581–591) para manter ou cortar (~8–10 s).
3. **H8** — supercut: trecho curto ou prints.
4. **H5** — Pica-Pau curta (default) ou longa com splice da ponte.
5. **H7** — "fucking" (80.9): bleep, deixar ou dip.
6. **H4** — manter ou não "IA NA HOME DO GA" (precisa de confirmação de fato).
7. **H10** — gag da piada de autoria: sim/não.
8. **H2** — só se quiserem "110+": confirmar o número real.
9. **H1** — confirmar take 42.5 e o eco "Tá no ar, tá valendo" com o cold open.
10. **Thumb (feedback Lucian):** qual thumb e qual pessoa — `EP300_BACKLOG / SECONDARY_ASSET / NEEDS_IDENTIFICATION` (não identificável no material: `Criativos` só tem criativos de convidados e banners).

## 6. BLOCKED
- **K1 Kinoplex** — `KINOPLEX_VISUAL_TREATMENT`: BLOCKED / WAITING DESIGN. Fonte: Cláudio Miranda / site-handoff. Fato: apoiador oficial do EP300. Desconhecido: posição, rótulo, tratamento, agrupamento. Não montar nada; as soluções V3 são históricas.

## Ordem de dependência
```
0 spec ──┬─> 1.1 salvar local ─> 1.2 sync ─> 1.3 montagem EDL ─> 1.4 câmeras ─> 1.5 XML + QA
         └─> 2.1 v4/plan.py ─> 2.2/2.3 re-render ─> 2.4 áudio ─> 2.5 QA
5 (H) ──> só destrava seleção de trechos (D1, D6, G1, G2, E4); não trava o resto
6 (K1) ──> só o slot de Kinoplex em A4/G4
```
