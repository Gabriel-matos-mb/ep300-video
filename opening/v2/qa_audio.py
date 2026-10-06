"""EP300 · V2 — QA de ÁUDIO: loudness/true-peak do mix, SFX × voz (nunca competir), música × voz, emendas (clicks) e risada preservada."""
import os, sys, json, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding='utf-8')
import build
SR = build.SR
A = build.L_AUD
dia = build.rd(os.path.join(A, 'STEM_DIALOGO.wav')).mean(1); mus = build.rd(os.path.join(A, 'STEM_TRILHA.wav')).mean(1); sfx = build.rd(os.path.join(A, 'STEM_SFX.wav')).mean(1)
mix = build.rd(os.path.join(build.B, 'mix.wav'))


def rms_db(x): return 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)


out = {}
r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', os.path.join(build.B, 'mix.wav'), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
i = r.rindex('Summary:'); s = r[i:]
import re
out['lufs'] = float(re.search(r'I:\s+(-?\d+\.?\d*) LUFS', s).group(1)); out['lra'] = float(re.search(r'LRA:\s+(-?\d+\.?\d*) LU', s).group(1))
out['true_peak_dbtp'] = float(re.search(r'Peak:\s+(-?\d+\.?\d*) dBFS', s).group(1))
out['clip_samples'] = int((np.abs(mix) >= 0.999).sum())
# SFX × voz: em cada evento de SFX, nível do SFX (RMS 0,4 s) vs voz (RMS 0,4 s) na mesma janela
T = build.timeline(); rows = []; worst = -99
for t, k in build.sfx_events(T):
    a = int(max(0, t) * SR); b = a + int(.4 * SR)
    d, sx = dia[a:b], sfx[a:b]
    if len(d) < 100: continue
    dd, ss = rms_db(d), rms_db(sx)
    if dd > -50:      # há voz
        diff = ss - dd; rows.append((round(t, 1), k, round(float(diff), 1))); worst = max(worst, diff)
out['sfx_sobre_voz_pior_db'] = round(float(worst), 1); out['eventos_sfx_com_voz'] = len(rows)
out['sfx_mais_altos_que_voz_-6dB'] = [r for r in rows if r[2] > -6]
# música × voz: durante fala
mask = np.abs(dia) > 0.02
out['musica_menos_voz_db_media'] = round(float(rms_db(mus[mask]) - rms_db(dia[mask])), 1)
# clicks: saltos de amostra > 0,5 no diálogo
jump = np.abs(np.diff(dia)); out['saltos_>0.5_no_dialogo'] = int((jump > 0.5).sum())
# risada preservada: cold open — nível do diálogo entre 5 e 9,3 s (risada) deve estar presente
seg = dia[int(5.5 * SR):int(9.0 * SR)]; out['cold_open_riso_rms_db'] = round(float(rms_db(seg)), 1)
print(json.dumps(out, ensure_ascii=False, indent=1))
json.dump(out, open(os.path.join(HERE, '..', 'work', 'v2', 'qa', 'audio_report.json'), 'w'), ensure_ascii=False, indent=1)
