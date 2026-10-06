# EP300 — Reconciliação LOCAL SSD ↔ DRIVE (inventário + plano) — 03/10/2026

> **Status final (03/10/2026): `EP300_STORAGE_RECONCILIATION = COMPLETE` · `DRIVE = PERSISTENT SOURCE` · `LOCAL = LIGHTWEIGHT WORKSPACE`.** Preservação validada (MD5) e limpeza T1+T1B+T2 executada conforme `inventory/safe_to_delete.json` (aprovada pelo Gabriel). Ver §9.
> Regra: [[../../wiki/roadmap/ep300-closeout-consolidation]] § 5 (Drive First). Fluxo: COPIAR → VALIDAR → MARCAR SEGURO → (aprovação) APAGAR.
> Dados brutos (leves, versionáveis): `inventory/` (`classes.json`, `compare.json`, `drive_ep300_files.json`, scripts `walk.py`/`drive_walk.py`/`classify.py`). Reexecutar = reproduzir os números.
> Escopo: `projects/ep300-cinema-opening` + `projects/ep300-cinema-loop`. **Fora do escopo:** `analytics-summit-manifesto` (7,0 GB), `studio` (1,7 GB), `remotion-mb` (1,2 GB), `newsreel` (0,6 GB).

## 1. Tamanho atual
- **SSD:** repo `audio-visual` ≈ **41 GB**; EP300 Opening **31,2 GB** (3.318 arquivos), Loop **0,58 GB** (158). Manifesto 7,0 GB à parte.
- **Drive (pasta `300_[Kinoplex]…`):** **59,8 GB**, 1.313 arquivos (brutos 4K ≈ 26 GB; `V0/V1/V2_GERADOS` ≈ 11 GB; `03_EDITADOS/VERSÃO FINAL` 3,9 GB).
- **Já seguro no Drive (finais):** `ABERTURA-EP300 - VF EM 4Q.mp4` (2,85 GB), `…VF EM FULL HD.mp4` (0,96 GB), `EP300_LOOP_FINAL_4K.mp4`, `EP300_LOOP_FINAL_1080p.mp4`, projeto Premiere final (`02_PROJETOS/ep 300 final.prproj`), brutos/regravação, handoff V2 (`EP300_HANDOFF_LUCIAN`), stickers refeitos, `V0–V2_GERADOS` (overlays/áudio).
- **Existe SÓ no SSD (não está no Drive):** tudo da Review 02/03 e das correções 4K — layers R03, XML/timing map/stems/SFX do pacote editável, 4K do C02_03/S10/O01/O02, insumos de rebuild, código (b2/b3/compose/mix/build_xml, Remotion V4). O Drive tem só o handoff **V2**.

## 2. Maiores subpastas / arquivos (SSD, Opening)
| MB | Pasta | Nota |
|---:|---|---|
| 3.555 | `work/build_v2/OVERLAYS` | = `V2_GERADOS/OVERLAYS` no Drive |
| 3.438 | `review01/work` | track_base 2,2 GB, seg/ (b2.mov 1,0 GB), layers_raw 1,3 GB, chunks, r03, r3 (4K) |
| 3.145 | `work/build_v1/OVERLAYS` | = `V1_GERADOS/OVERLAYS` |
| 2.700 | `review01/layers_r03` | layers da R03 (96) |
| 2.479 | `review01/layers` | layers da R02 (1,79 GB idênticos aos da R03) |
| 1.318 | `work/build/OVERLAYS` | = `V0_GERADOS/OVERLAYS` |
| 999 | `EP300_V4_MOTIONS/remotion/node_modules` | 16.844 arquivos |
| 948 | `work/proxy` | 3 proxies |
Maiores arquivos: `review01/work/track_base.mov` 2.169 MB · `review01/work/seg/b2.mov` 1.049 MB.

## 3. Classificação (A–F) — `inventory/classes.json`
| Cl. | Significado | MB | Conteúdo | Ação proposta |
|---|---|---:|---|---|
| **A** | FINAL / INTOCÁVEL | 836 | 4K reutilizáveis: `rem4k/{O01,O02,S10}.mov`, `layers_r03_ep1fix_4k/C02_03.mov` | **copiar p/ Drive**; só-local hoje |
| **B** | NECESSÁRIO P/ REABRIR/EDITAR | 6.667 | `layers_r03` 2.711 · `editable_r03` 522 · MP4 R03 182 · insumos de rebuild 735 (áudio base, blooper, freeze 4K, stems) · V0–V3 `work/*` 2.316 (1.822 só-local; **a revisar**) · Remotion/mapas V4 65 · Loop 133 | copiar o que for só-local e necessário; código fica local (git) |
| **C** | ASSET/FONTE ORIGINAL | 130 | `b2/b3/assets` (inclui cópias dos stickers que o Drive já tem em `stickers e emojis refeitos`) | só o que não tem origem no Drive |
| **D** | REGENERÁVEL | 10.489 | intermediários `review01/work` (seg/chunks/raw/fix/track_base/r03) 7.235 · node_modules 999 · proxies 948 · `build*/pieces` 895 · Remotion 720p 355 · previews 57 | candidato a exclusão local (receita preservada em código) |
| **DR** | DUPLICADO DO DRIVE | 9.058 | `work/build*/{OVERLAYS,AUDIO,…}` (8.616) + finais do Loop em `ep300-cinema-loop/out` (442) — mesmo nome+tamanho no Drive | candidato a exclusão **após verificação por hash** |
| **E** | TEMPORÁRIO/DESCARTÁVEL | 762 | sheets, frames, testes, `review01/work/qa`, `r3/stk` (cópia de stickers), inventário | candidato a exclusão |
| **F** | OBSOLETO/SUPERADO | 3.799 | layers R02 2.490 · editável R02 521 · reviews 01/02 356 · `_assembly_work` (V4 REJEITADA) 337 · 720p do C02_03 95 | avaliar (precisa de OK) |
Total classificado: **31,7 GB**.

## 4. Plano de migração (proposta de destino — Taxonomia Marco Zero)
Base: `01_CANAIS_ATIVOS/02_PODCAST/2026/300_[Kinoplex] …/01_VIDEO DE ABERTURA/`
| Origem (SSD) | Destino (Drive) | Cl. | ≈ MB |
|---|---|---|---:|
| `review01/layers_r03_ep1fix_4k/`, `review01/work/r3/rem4k/` | `00_ASSETS E INSERTS/R03_COMPONENTES_FINAIS_4K/` | A | 836 |
| `review01/layers_r03/` (96 layers 720p/ProRes + sidecars `.json`) | `00_ASSETS E INSERTS/R03_LAYERS/` | B | 2.711 |
| `review01/editable_r03/` (XML, timing map, stems, SFX) | `02_PROJETOS/EP300_ABERTURA_R03_EDITAVEL/` | B | 522 |
| `review01/V4_PRESENTABLE_REVIEW_03.mp4` | `03_EDITADOS/REFERENCIA_REVISAO/` | B | 182 |
| insumos de rebuild (`base_audio_orig.wav`, `blooper.mov`, `gritem_4k.png`, `stem_*`, `words_tl.json`, `cues_final.json`) | `02_PROJETOS/EP300_ABERTURA_R03_EDITAVEL/_insumos/` | B | 735 |
| código (`review01/*.py`, `b2/`, `b3/`, `EP300_V4_MOTIONS/remotion/src`, `v2/` engine, docs) | **fica no repo local + git** (leve) | B | < 80 |
| `V0–V3 work/*` só-local (1.822 MB) | **decidir após revisão** (provável: regenerável pelo motor V2) | B? | 1.822 |
Não vão para o Drive: node_modules, proxies, `build*/pieces`, caches/intermediários (D), sheets/frames (E), `build*/OVERLAYS|AUDIO` (já lá).

### Procedimento por arquivo (execução só após aprovação)
1. origem local · 2. destino · 3. `copy` **sem sobrescrever** (abortar se destino existir com tamanho diferente) · 4. confirmar existência · 5. tamanho **+ hash (MD5/SHA-256)** origem × destino; mídia: `ffprobe` (duração/resolução/codec) · 6. registrar em manifest (`inventory/migration_manifest.json`) e só então marcar a cópia local como **ELEGÍVEL P/ EXCLUSÃO** · 7. apagar **somente** com aprovação explícita, em lote por classe.
Para **DR**: a equivalência hoje é por nome+tamanho (`compare.json`); exige hash antes de qualquer exclusão. 44 arquivos locais de `build_v2/OVERLAYS` não têm par no Drive (0 MB) — tratar como D.

## 5. Estimativa de espaço recuperável (do SSD, 31,7 GB)
| Cenário | Libera | Condição |
|---|---:|---|
| Seguro/regenerável: **DR + D + E** | **≈ 20,3 GB** | hash em DR; D regenera via código |
| + obsoletos **F** (layers/editável R02 etc.) | ≈ 24,1 GB | OK do Gabriel; 1,79 GB dos layers R02 são idênticos aos da R03 |
| + A/B/C locais **depois** de copiados e validados | ≈ 28,5 GB | cópia validada no Drive |
| **Workspace local final** | ≈ 3 GB (código, docs, Remotion src, V0–V3 a decidir) | node_modules (1 GB) só se não houver mais re-render 4K |
Nada disso conta o **Manifesto** (7,0 GB; 4,5 GB em `work/`) — reconciliação própria após a finalização dele.

## 6. Higiene opcional do lado Drive (não tocar sem decisão)
Proxies V0/V1/V2 duplicados em 3 lugares (`03_EDITADOS`, `VERSÃO 02`, `HANDOFF_LUCIAN/MASTER_REFERENCE`); pasta `desatualizado/` (127 MB); `V*_GERADOS` ≈ 11 GB regeneráveis. Registro apenas.

## 7. Decisões que dependem do Gabriel
1. **Aprovar os destinos** da tabela §4 (ou indicar outra pasta oficial).
2. **Layers/editável/reviews R02 (F):** apagar depois da R03 segura no Drive? (recomendado: sim)
3. **V0–V3 `work/*` só-local (1,8 GB):** guardar ou deixar regenerável?
4. **node_modules:** manter até o fim dos re-renders 4K ou remover já?
5. Há mais correção 4K a gerar no Opening/Loop? (se sim, manter intermediários D por enquanto).

## 8. Fase de preservação — resultado (decisões do Gabriel aprovadas em 03/10)
- **Copiado:** 260 arquivos / 4.871 MB (`inventory/migration_manifest.json`): `R03_COMPONENTES_FINAIS_4K` 836 MB (5) · `R03_LAYERS` 2.806 MB (101) · `02_PROJETOS/EP300_ABERTURA_R03_EDITAVEL` 1.045 MB (153: XML, timing map, mídia, `_insumos/`, `_codigo/` snapshot zip) · `03_EDITADOS/REFERENCIA_REVISAO` 182 MB (1).
- **Validado:** existência + tamanho + **MD5 origem × destino = 260/260 iguais**, 0 divergências, 0 `.partial`. 1 destino já existia (teste de caminho longo) e foi revalidado. `VERSÃO FINAL`, brutos e Premiere final: **não tocados** (mtimes inalterados).
- **Incidente:** 84 cópias falharam na 1ª passada (caminho do Drive > 260 caracteres no Windows). Resolvido com prefixo de caminho estendido (`\?\`), sem alterar nomes. Atenção: **no Drive esses caminhos longos podem não abrir em apps que não suportem >260** (ex.: `.../media/audio/sfx/MA_SoundsByGFXSounds_DingNotification_1.wav`); se o editável precisar ser usado direto do Drive, melhor copiar a pasta para um caminho curto local primeiro.
- **Hash dos duplicados (DR):** 382 arquivos; **310 HASH_IGUAL (9.059 MiB)**, **0 HASH_DIFERENTE**, 72 sem par no Drive (sidecars `.hash`, logs, `base_720.mp4`/`mix*.wav` de V0–V2, `base_list.txt`: derivados; 44 `.hash` + finais de Loop V3_REVIEW etc. ficam RETIDOS). `inventory/dr_hash_manifest.json`.
- **Fontes únicas:** R02 → nenhuma usada pela R03 (R03 reescreve layers/XML/stems; `HOLD_*.png` já estão no pacote R03). Únicos só-R02: XML/timing map (retidos, 160 KB) e **stems/mix de áudio R02** (≈ 0,96 GiB, saída do mix R02 — ver T1B). V0–V3 `work/`: preservados `base_audio_orig.wav`, `blooper.mov`, `gritem_4k.png`, `work/v2/b0.mp4` (diálogo do blooper), 5 `audio_ma/*.wav` + músicas do `MA`, `pipoca/caixa.ai` + `img_644.png`, assets V4/b3; código/configs em `_codigo/EP300_CODIGO_SNAPSHOT_2026-10-03.zip` (o git só rastreia md + v0–v3; `review01`, `b2`, `b3`, Remotion V4 **não estavam no git** — agora têm cópia no Drive).

## 9. Limpeza executada — estado final (03/10/2026)
- **Autorizado e executado:** T1 + T1B + T2 (gate por arquivo: T2 só com cópia no manifesto `OK`, MD5 local = MD5 origem copiada e destino no Drive de mesmo tamanho; DR só com `HASH_IGUAL`). Log: `inventory/purge_log.json`, script `inventory/purge.py`. Nenhum arquivo foi pulado por falha de gate.
- **Liberado:** **31,86 GB (29,67 GiB)** em Opening + Loop. Antes 32,26 GB → **agora 0,39 GB** (Opening 0,25 GB, Loop 0,14 GB). **Repositório `audio-visual` completo: ≈ 41 GB → 10,96 GiB (11,77 GB)** (o resto = Manifesto 7 GB, studio 1,7 GB, remotion-mb 1,2 GB, newsreel 0,6 GB — fora desta passagem).
- **Exceções/pulados (intencionais):** (1) `EP300_V4_MOTIONS/remotion/node_modules` é uma **JUNCTION** para `remotion-mb/node_modules` (outro projeto) → **não removida** e nada a liberar aqui (os "999 MB" do inventário eram do `remotion-mb`); `package.json`/`tsconfig`/`src` intactos. (2) 10 arquivos de `work/inv` (inventário/hashes) preservados por ordem do Gabriel. (3) XML R02 e `timing_map.json` R02 retidos.
- **Incidente corrigido:** a 1ª execução caiu no `node_modules` (junction) *depois* de processar todos os arquivos e *antes* de gravar o log; a 2ª passada confirmou 2.104 arquivos já removidos (30.388 MiB) e recriou o log. Por estarem na lista T2 mas serem configs de rebuild, **restaurei do Drive (MD5 conferido)** `review01/cues_final.json`, `cues_raw.json`, `words_tl.json`, `work/base_path.txt` (política "preservar configs/manifests").
- **Para re-renderizar no futuro:** trazer do Drive (`DRIVE → LOCAL TEMP`): `R03_LAYERS`, `02_PROJETOS/EP300_ABERTURA_R03_EDITAVEL/_insumos/` (inclui `EP300_V4_MOTIONS_assets/` = `publicDir` do Remotion, `b3_assets`, áudios base, blooper, `b0.mp4`) e o código em `_codigo/`; `npm install` no `remotion-mb` (o `node_modules` é compartilhado por junction).
- **Intactos:** `03_EDITADOS/VERSÃO FINAL` (4 finais, mtimes/tamanhos inalterados), projeto Premiere final (`ep 300 final.prproj`), brutos, Manifesto.

## 10. ESTADO FINAL (registro do Gabriel, 03/10/2026)
```
EP300 STORAGE RECONCILIATION = COMPLETE
31.86 GB LOCAL STORAGE RECOVERED
OPENING + LOOP LOCAL WORKSPACE = ~0.39 GB
DRIVE = PERSISTENT SOURCE
LOCAL = LIGHTWEIGHT WORKSPACE
MASTERS / PREMIERE / RAW MEDIA = PROTECTED
```
**Regra comprovada em produção:** Drive = casa persistente do projeto; SSD = bancada temporária (CLAUDE.md § DRIVE FIRST).
**Pendência futura (NÃO executar agora) — CODE GOVERNANCE:** revisar o código importante hoje preservado só em ZIP/Drive
(`_codigo/EP300_CODIGO_SNAPSHOT_2026-10-03.zip`; `review01`, `b2`, `b3`, Remotion V4 não estão no git) e decidir o que deve ser versionado no Git.
Frente encerrada: sem nova limpeza, auditoria ou reorganização.
