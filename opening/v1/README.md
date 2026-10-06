# EP300 · Vídeo de abertura · V1 — como reeditar (Premiere) e como regenerar

> V1 = V0 + direção do Gabriel (48 marcadores no Premiere) + sync corrigido. A V0 continua intacta
> (`02_PROJETOS/EP300_ABERTURA_V0/`, `V0_GERADOS/`, `03_EDITADOS/EP300_ABERTURA_V0_PROXY.mp4`).
> O projeto do Gabriel também: cópia de segurança em `02_PROJETOS/BACKUP_INTERVENCAO_GABRIEL_V0_2026-09-29/` (MD5).

## Onde está cada coisa (Drive · `300_[Kinoplex] …/01_VIDEO DE ABERTURA/`)

| Camada | Local | O que é |
|---|---|---|
| SOURCE | `01_BRUTOS/` + `00_ASSETS E INSERTS/erros de gravação antigos/` | câmeras e bastidores originais — só lidos |
| PROJECT | `02_PROJETOS/EP300_ABERTURA_V1/EP300_ABERTURA_V1.xml` | Premiere: *Arquivo › Importar* (2 sequências) |
| PROJECT | `…/timeline_v1.json` | manifesto legível: planos, overlays, cortes, SFX, sync, cor |
| PROJECT | `…/FONTE_CODIGO/` | `plan.py` (decisões) + motor + fontes + `feedback_v1.json` (o que foi feito em cada marcador) |
| PROJECT | `…/SYNC_E_FEEDBACK/` | relatório de sync (`sync_report.json`), marcadores do Gabriel extraídos, transcrição |
| ASSETS | `00_ASSETS E INSERTS/V1_GERADOS/OVERLAYS/` | 43 overlays `Cxx_yy_NOME.mov` — ProRes 4444 **alpha** 1920x1080 30 fps (+ `_ref.png`) |
| ASSETS | `…/V1_GERADOS/STICKERS/<PESSOA>/` | adesivos de convidados: `NN_estado.png` (com contorno), `_recorte.png` (sem), `_tratada.jpg` (quando houve upscale) + `PROVENANCE.json` |
| ASSETS | `…/V1_GERADOS/{PIPOCA,PRINTS,EP126}/` | caixa de pipoca/selos (do arquivo de impressão), prints de episódios, quadros do EP 126 — com proveniência |
| ASSETS | `…/V1_GERADOS/AUDIO/` | trilhas/SFX usados (Motion Array da MB), stems DIALOGO/TRILHA/SFX, áudio dos bastidores, `REF_MIX_V1.wav` |
| ASSETS | `…/V1_GERADOS/LUTS/` | aproximação do Lumetri do Gabriel por câmera (só usada no proxy) |
| PREVIEW | `03_EDITADOS/EP300_ABERTURA_V1_PROXY.mp4` | 1280x720 · 30 fps · −16 LUFS (o que está no Studio) |
| DELIVERABLE | — | **não gerado** (master fica para depois da revisão da V1) |

## XML no Premiere

- **EP300_ABERTURA_V1**: V1 = bastidores (cold open) + câmeras apontando para os **brutos originais** + freeze do respiro;
  reenquadramentos da CAM_GERAL (punch-in no Gustavo/Lucian) = **Movimento** (escala/posição) no próprio clipe;
  V2+ = overlays; áudio: diálogo (CAM_GERAL) e bastidores, trilhas, SFX, `REF_MIX_V1` desligada.
  **Marcadores**: os comentários do Gabriel na V0, reposicionados na V1, com "V1: o que foi feito".
- **EP300_SYNC_3CAM_V1**: as 3 câmeras alinhadas, **já com a correção de sync** (imagem da geral +5 quadros).

### Cor (Lumetri do Gabriel) — preservada, não refeita

O Lumetri que o Gabriel aplicou está no projeto dele (`EP300_ABERTURA_V0 Cópia.prproj`, sequência SYNC_3CAM),
por câmera. FCP XML não transporta Lumetri. Para levar para a V1 **sem perder nada**:
1. Importar `EP300_ABERTURA_V1.xml` **dentro do projeto do Gabriel** (a cópia de trabalho, não o backup).
2. Na SYNC_3CAM antiga, copiar o clipe da CAM_GERAL → na V1 selecionar os clipes `CAM_GERAL…` → *Colar atributos* (só Lumetri).
3. Repetir para `CAM_GUSTAVO` e `CAM_LUCIAN`. (3 colagens.)
O proxy da V1 usa uma **aproximação numérica** desses valores (`grade.py` / `LUTS/`) só para a revisão.

## Sync (corrigido na V1)

Medido nos brutos (imagem×imagem das fechadas contra a geral, começo/meio/fim): a **imagem da CAM_GERAL chega
~150–180 ms depois do áudio da mesa** gravado no mesmo arquivo. As fechadas (alinhadas pelo áudio) estavam certas;
drift de relógio ≤ 7 ms em 7 min. Correção: a imagem da geral entra **5 quadros adiante** (in-point +5) em todos os
clipes da geral; o áudio de diálogo não muda. Ver `SYNC_E_FEEDBACK/sync_report.json`.

## Limitações (reedição)

- Overlays pré-renderizados (conteúdo muda em `plan.py` + `python build.py overlays --only C04_04`).
- Envelopes de trilha e normalização −16 LUFS estão na `REF_MIX_V1`/stems, não no XML (lá o ganho é fixo por clipe).
- Cold open em P&B/grão/REC: no proxy; no Premiere o clipe entra colorido (aplicar Preto e Branco + ruído se mantiver).
- Posição dos reenquadramentos no XML (parâmetro Center) segue a convenção FCP7 — conferir no primeiro import.

## Regenerar

```
cd projects/ep300-cinema-opening/v1      (repo audio-visual)  ou  FONTE_CODIGO/ (Drive)
python build.py                          # stills, overlays, base, áudio, preview, xml, manifesto
python build.py overlays --only C05_05   # um overlay só
python qa_cues.py C05_05                 # quadro de QA sobre a câmera real (oclusão)
python sync_check.py --vidvid            # re-auditoria de sync (imagem×imagem)
```
