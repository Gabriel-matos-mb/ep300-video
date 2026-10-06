# ÁUDIO — diálogo, trilha, SFX, ducking

**Loop:** sem áudio (silencioso por decisão). Tudo abaixo é da **Abertura**.

## Camadas
| Camada | Origem | Notas |
|---|---|---|
| **Diálogo** | Áudio da mesa da `CAM_GERAL` (+ regravações em `NOVOS TAKES-REGRAVADO`). Tratamento do Gabriel no Premiere (88 filtros) é autoridade. | Não reconstruir via FFmpeg. Diálogo da base intocado, só cortes nos holds + censura "fucking" (`review01/mix_audio.py`). |
| **Trilha** | 3 faixas Motion Array (abaixo) | Baixa (**−31 dB**) sob o diálogo. |
| **SFX** | 8 do Motion Array + 12 sintéticos (numpy) | **74 SFX** na baseline: 11 KEEP · 58 RETIME · 5 DROP_SCRIPT. Ducking **−12 dB** sob a voz. |
| **Gags** | `SFX_BLEEP_1kHz.wav` (bleep do "fucking"), `SFX_LEADER_BEEP_1kHz.wav` | Bleep alinhado **pelo espectro** (o ASR errou ~0,4 s). Não estão nos 74. |

Regra: **SFX nunca compete com voz**; música/SFX/ducking da V2 são baseline (não trocar trilha nem reconstruir o desenho sonoro sem pedido do Gabriel).

## Trilhas (Motion Array — licença da conta MB; **não estão neste repo**)
| Faixa | Uso |
|---|---|
| *Beat The Odds* (LEX Music), 30 s | C00_03 "aviso antes da sessão" |
| *A Groove Pool* (Trigubovich), loop | cama sob o diálogo (S1…S7) |
| *In The Spotlight* (Puremusic), 12 s | C08_01 título / C09_01 final |

## SFX Motion Array (também só no Drive) — ganho no mix (`review01/mix_audio.py › SFXLIB`)
click −14 dB (C03_02) · whoosh pass-by −21 (C00_02, C02_02, C04_01; **DROP_SCRIPT** em C04_02) · impact −24 · tvoff −17 (C03_02) · wrong answer −15 (C05_02) ·
ding −21 (C07_06) · clock ticking −21 (C07_03) · woosh+boom −21 (C04_05 GRITEM).
Mix: `REL = −5,4 dB` (base −19,5 LUFS vs CAM_GERAL da V2) para manter o balanço V2 música/SFX × voz.

## SFX sintéticos (reprodutíveis)
`SFX_SYN_{pop, thump, party, rise2.6, tickup0.8/0.9/0.95/1.0/1.1/2.6}.wav`, geradas por `opening/v2/sfx_v2.py` (ganhos em `mix_audio.py › SYN_GAIN`:
thump −20, pop −19, party −17, tickup −20, rise −23). Cópias em `handoff-2026-09-30/shared-assets/sfx/sinteticos/`.
Para a página P02 (aviso), os pops estão sincronizados às viradas de página/eventos visuais (`opening/review01/layers_r03/P02.json`).

## Onde pegar o áudio
| O quê | Caminho no Drive (sob `01_VIDEO DE ABERTURA/`) |
|---|---|
| Música + SFX Motion Array (originais) | `EP300_HANDOFF_LUCIAN/03_SHARED_ASSETS/audio/musica/` e `…/sfx/motion_array/`; também `02_PROJETOS/EP300_ABERTURA_R03_EDITAVEL/_insumos/audio_ma/` |
| **Stems V2** (`STEM_DIALOGO`, `STEM_SFX`, `STEM_TRILHA`, `REF_MIX_V2` — 71 MB cada, 6:10) | `EP300_HANDOFF_LUCIAN/01_OPENING/EDITABLE/audio_stems/` |
| Áudio gerado por revisão | `00_ASSETS E INSERTS/V2_GERADOS/AUDIO`; Review 03: `02_PROJETOS/EP300_ABERTURA_R03_EDITAVEL/media/audio` |
| Bastidores do cold open (2023) | `EP300_HANDOFF_LUCIAN/03_SHARED_ASSETS/audio/bastidores/` (`COLD_B_*.wav`) |

Proveniência completa de cada arquivo: [`handoff-2026-09-30/manifest/provenance.md`](../handoff-2026-09-30/manifest/provenance.md).
Cobertura cue × SFX: `opening/review01/cues_final.json`, `editable_r03/timing_map_review03.json`, `opening/EP300_V4_MOTIONS/EP300_V2_TO_V4_MIGRATION_MAP.md` (§ SFX).
