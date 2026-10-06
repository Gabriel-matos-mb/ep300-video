# EP300 · Vídeo de abertura · V2 — como reeditar (Premiere) e como regenerar

> V2 = V1 + feedback do Gabriel (arco cinema, continuidade, safe area, SFX, história, final→looping). V0 e V1 continuam intactas
> (`02_PROJETOS/EP300_ABERTURA_V0|V1`, `V0_GERADOS`, `V1_GERADOS`). Projeto do Gabriel: backup imutável em
> `02_PROJETOS/BACKUP_INTERVENCAO_GABRIEL_V0_2026-09-29/` (ver `BACKUP_VERIFICACAO_V2.txt` — nada mudou desde o backup).

## Onde está cada coisa (Drive · `300_[Kinoplex] …/01_VIDEO DE ABERTURA/`)

| Camada | Local | O que é |
|---|---|---|
| SOURCE | `01_BRUTOS/` + `00_ASSETS E INSERTS/erros de gravação antigos/` | câmeras e bastidores originais — só lidos |
| SOURCE | `00_ARQUIVO_HISTORICO/…/02_PODCAST` (Drive institucional) | frames dos episódios 73/84/100/153/187/210 (acervo) — só lidos |
| PROJECT | `02_PROJETOS/EP300_ABERTURA_V2/EP300_ABERTURA_V2.xml` | Premiere: *Arquivo › Importar* (2 sequências, 42 marcadores do Gabriel preservados) |
| PROJECT | `…/timeline_v2.json` | manifesto legível: planos, overlays, cortes, SFX, sync, cor |
| PROJECT | `…/FONTE_CODIGO/` | `plan.py` (decisões) + motor + fontes; `customs_v2.py` (final→loop) |
| ASSETS | `00_ASSETS E INSERTS/V2_GERADOS/OVERLAYS/` | 44 overlays `Cxx_yy_NOME.mov` — ProRes 4444 **alpha** 1920x1080 30 fps (+ `_ref.png`). Telas cheias encadeadas **se estendem 0,4 s** sob a seguinte (empurrão) |
| ASSETS | `…/V2_GERADOS/ASSETS_V2/` | stickers normalizados (Guta, Lucas, Vitória, Mafê, Phill, Bonel, Layla), balde corrigido, viatura, gags originais (Toddynho, pica-pau), logos, frames históricos — com `PROVENANCE.json` |
| ASSETS | `…/V2_GERADOS/AUDIO/` | trilhas/SFX usados (MA + sintéticos `SFX_SYN_*.wav`), stems `STEM_DIALOGO/TRILHA/SFX` (SFX já com ducking) e `REF_MIX_V2.wav` |
| PREVIEW | `03_EDITADOS/EP300_ABERTURA_V2_PROXY.mp4` | 1280x720 · 30 fps · −16 LUFS (o que está no Studio) |
| DELIVERABLE | — | **master não gerado** (fica para depois da revisão da V2) |

## XML no Premiere
- **EP300_ABERTURA_V2**: V1 = bastidores (cold open) + câmeras nos **brutos originais** + freeze; reenquadramentos (punch-in) = Movimento no clipe;
  V2+ = overlays; áudio: diálogo (CAM_GERAL), bastidores, trilhas, SFX (um clipe por evento), `REF_MIX_V2` desligada. Os 42 comentários do Gabriel na V0 estão como marcadores.
- **EP300_SYNC_3CAM_V2**: as 3 câmeras alinhadas **com a correção de sync** (imagem da geral +5 quadros).
- **Cor**: FCP XML não leva Lumetri — siga o procedimento da V1 (importar dentro do projeto do Gabriel e colar atributos; 3 colagens). O proxy usa aproximação numérica.
- Cold open em P&B/REC: no proxy; no Premiere entra colorido (aplicar P&B + ruído).
- Pausa sem voz (`P_EVOL`, 2,4 s) não tem clipe de câmera: o overlay `C02_03` cobre.
- Ducking do SFX não está no XML (ganho fixo por clipe): use `STEM_SFX.wav` (já com ducking) como referência.

## Sync
Imagem da CAM_GERAL chega ~5 quadros depois do áudio da mesa (captura). Correção: imagem +5 quadros em todo clipe da geral. Revalidado na V2 (imagem×imagem, começo/meio/fim): resíduos ≤ 35 ms.

## Regenerar
```
cd projects/ep300-cinema-opening/v2
python build.py                          # stills, overlays (cache por hash), base, áudio, preview, xml, manifesto
python build.py overlays --only C03_01   # um overlay só
python qa_cues_v2.py C03_01 | --safe     # contact sheet / safe area de todas as cenas
python qa_leak.py                        # vazamento de câmera entre telas cheias (composição sobre magenta)
python qa_reading.py                     # tempo de leitura das telas sem voz
python sync_check.py --vidvid --v1       # re-auditoria de sync
```
O final (`C09_01`) importa `../ep300-cinema-loop/build.py` (mosaico, logo, patrocinadores e os quadros 118,5–120 s do loop).
