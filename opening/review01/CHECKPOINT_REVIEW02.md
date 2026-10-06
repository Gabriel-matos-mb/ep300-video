# Checkpoint EP300 — Review 02 entregue (03/10/2026)

## Estado
- `review01/V4_PRESENTABLE_REVIEW_02.mp4` pronto: 1280x720, 23,976 fps, 382,17 s, AAC, -20 LUFS. Nao assistido inteiro em tempo real (so quadros + analise de audio).
- Editavel: `review01/editable/EP300_ABERTURA_REVIEW_02.xml` (xmeml v4, seq 3840x2160) + `timing_map.json` + `media/{audio,stills,video}`. **NAO validado no Premiere** (Basic Motion center/scale pode divergir; push animado do GRITEM e estatico).
- Estrutura: PRE (P01,P02,P03, cold open 10,5 s completo) -> base 4K do Gabriel com holds P_EVOL (frame 1032, +58) e GRITEM (frame 2983, +72, freeze 4K 123,2 s reenquadrado) -> insert final no frame 7395 (C08 titulo + F01) -> gap preto + blooper P&B do Premiere (preservado, ultimo quadro = ponto de entrada do loop). Total 9163 quadros.

## Rebuild (pasta review01/)
`BASE_AUDIO=work/base_audio_orig.wav python mix_audio.py` -> `python compose_video.py stage1 stage2 mux` (stage1 ~4 min; `chunkN` refaz 1 chunk; stage1_f2 refaz so o freeze GRITEM) -> `python build_xml.py`.
Layers em `layers/` (49 .mov + .json; originais C06_03_* em `layers/_orig`). Fontes: Remotion em `EP300_V4_MOTIONS/remotion` (render: `node tools/render_layers.mjs ../../review01/work/layers_fix ID,ID`), V2 engine via `b2/b2.py` (usar `EP300_V1_ASSETS=work/v1assets`), `fix_c203.py`, `make_cards.py`, `build_blooper.py`.

## Bugs resolvidos nesta sessao
- Audio: segmentos do dialogo sem somar cuts[i] (sobrepostos) -> corrigido; validado por correlacao (offsets 50,26 / +2,42 / +3,0 s).
- Compose: overlay eof_action=pass truncava fim dos layers -> repeat + enable. Gaps tela->tela <=30 quadros: underlay solido (push-in/out) ou hold do ultimo quadro.

## Pendencias (decisao/asset do Gabriel)
H2 (100 x 110 paises); posicao do cold open (R09 x estrutura V2); sticker novo do Pica-Pau (`PLACEHOLDER_R21`); 11 `PLACEHOLDER_PERSON_STICKER` no C05_01; prints finais EP1/EP100/EP210 (R17); C07_04 bandeiras onduladas (R24 pede quadradas); S11 legenda "ALGUEM APERTOU O PLAY"; ponto exato de saida p/ o LOOP; `PENDING_H3` (C06_04); NEEDS_REVIEW quem falou "Queria." (layer C05_03 removido: camera do Gustavo). Layers 720p: re-renderizar em resolucao de entrega.

## Regras novas do Gabriel (aplicar sempre)
Pessoas sao zonas protegidas (rosto/cabelo/mao/logo): mapear antes de posicionar; frame humano escolhido (olhos abertos, sem mao no rosto, sem blur), nao capturado; nao falsificar variedade (placeholder, nunca repetir pessoa); tela->tela = transicao limpa sem camera; cold open = cena completa, blooper final = preservar.
Locks do EP300 (NON_NEGOTIABLES, HANDOFF) continuam valendo; nao usar Opus; sem novos subagentes criativos.
