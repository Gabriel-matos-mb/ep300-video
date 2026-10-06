# EP300 · Vídeo de abertura · V0 — como reeditar (Premiere) e como regenerar

> Automação não pode destruir editabilidade: o MP4 proxy é só o preview. A edição vive em
> **XML do Premiere + overlays separados com alpha + código-fonte que regenera tudo**.

## Onde está cada coisa (Drive · `300_[Kinoplex] …/01_VIDEO DE ABERTURA/`)

| Camada | Local | O que é |
|---|---|---|
| SOURCE | `01_BRUTOS/` | 3 câmeras originais — **nunca modificadas** (só lidas) |
| PROJECT | `02_PROJETOS/EP300_ABERTURA_V0/EP300_ABERTURA_V0.xml` | timeline FCP7 XML → Premiere: *Arquivo › Importar* |
| PROJECT | `02_PROJETOS/EP300_ABERTURA_V0/timeline_v0.json` | manifesto legível: cada plano, overlay, SFX, corte (tl + fonte) |
| PROJECT | `02_PROJETOS/EP300_ABERTURA_V0/FONTE_CODIGO/` | este código (plan.py = decisões editoriais) + fontes Sora/Inter |
| PROJECT | `02_PROJETOS/EP300_ABERTURA_V0/TRANSCRICAO/` | transcrição palavra a palavra do take (large-v3) |
| ASSETS | `00_ASSETS E INSERTS/V0_GERADOS/OVERLAYS/` | 39 overlays `Cxx_yy_NOME.mov` — ProRes 4444 **com alpha**, 1920x1080, 30 fps (+ `_ref.png`) |
| ASSETS | `00_ASSETS E INSERTS/V0_GERADOS/STILLS/` | freeze frames 1080p tirados do bruto 4K |
| ASSETS | `00_ASSETS E INSERTS/V0_GERADOS/AUDIO/` | trilhas/SFX usados (cópias da biblioteca Motion Array da MB), bleep/beep gerados, **stems** DIALOGO/TRILHA/SFX e `REF_MIX_V0.wav` |
| PREVIEW | `03_EDITADOS/EP300_ABERTURA_V0_PROXY.mp4` | 1280x720 · 30 fps · −16 LUFS (o que está no Studio) |
| DELIVERABLE | — | **não gerado** (master 1920x1080 fica para depois da revisão) |

## XML no Premiere

- Sequência **EP300_ABERTURA_V0** (1920x1080, 30 fps): V1 = cortes de câmera apontando para os **brutos originais 4K**
  (sem proxy) + freeze do respiro "Gritem"; V2–V3 = overlays; A1 = diálogo (CAM_GERAL, +2 dB);
  A2–A3 = trilhas; A4 = SFX; A5 = `REF_MIX_V0` **desligada** (mix exata do proxy, para comparar de ouvido).
- Sequência **EP300_SYNC_3CAM**: as 3 câmeras alinhadas pelo áudio → selecionar e *Criar sequência multicâmera*
  se quiser trocar ângulos manualmente.
- Trocar um texto/timing de overlay: editar `plan.py` e rodar `python build.py overlays --only C04_03` (regera só aquele
  .mov com o mesmo nome — o Premiere pega o novo arquivo).

## Limitações conhecidas (reedição)

- Overlays chegam **pré-renderizados** (1 .mov por cue): editáveis em tempo/posição/opacidade no Premiere, mas o
  conteúdo interno (texto, animação) se muda no `plan.py` + render — não é MOGRT/AE.
- Envelopes de trilha (fade da abertura, subida de +10 dB no respiro) e a normalização −16 LUFS **não** estão
  no XML — estão na `REF_MIX_V0` e nos stems. O XML traz ganho de clipe fixo por faixa.
- Cor: sem correção (câmeras 4K e aberta como gravadas). Reframe/zoom: nenhum.
- 4K 23,976 numa sequência 30 fps: o Premiere converte a cadência (como na V0).

## Regenerar

```
cd projects/ep300-cinema-opening/v0      (repo audio-visual)  ou  FONTE_CODIGO/ (Drive)
python build.py              # stills, overlays, base, áudio, preview, xml, manifesto
python build.py overlays --only C01_02   # um overlay só
python qa_frames.py C04_04:.1,1.0        # quadro de QA sobre a câmera real
```
Requer: Python 3.12 + Pillow + numpy, ffmpeg com NVENC, faster-whisper (só para transcrever), proxies 720p
(`work/proxy`, regeneráveis a partir dos brutos) e o handoff do Claudio (`00_ASSETS E INSERTS/300-handoff-video/assets`).
