"""EP300 · V2 — QA de VAZAMENTO DE CÂMERA entre transições: compõe todos os overlays sobre MAGENTA puro (no lugar da câmera) e mede,
quadro a quadro, quanto magenta sobra dentro de intervalos de tela cheia. Esperado: 0 em todo o intervalo de cada tela cheia, exceto
nas janelas de wipe (0,3 s) de entrada/saída de telas cheias ISOLADAS (câmera visível de propósito). Em telas encadeadas (empurrão): 0 sempre."""
import os, sys, subprocess, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding='utf-8')
import build
W, H = 480, 270
T = build.timeline(); FPS = 30
fulls = [c for c in T['cues'] if c.get('full')]
# janelas onde ver a câmera é INTENCIONAL (wipe de tela cheia isolada + íris do selo)
allowed = set()
for c in fulls:
    wipe = int(0.3 * FPS) + 2
    if not c.get('push_in'): allowed.update(range(c['tl_in'], c['tl_in'] + wipe))
    if 'push_len' not in c and not c.get('iris'): allowed.update(range(c['tl_out'] - wipe, c['tl_out']))
    if c.get('iris'): allowed.update(range(c['tl_in'] + int(4.55 * FPS), c['tl_out']))
if '--strict' in sys.argv: allowed = set()
frames = set()
for c in fulls: frames.update(range(c['tl_in'], c['tl_out']))
frames = sorted(frames)
readers = {}
def rd(c):
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', build.ovl_path(c), '-vf', f'scale={W}:{H}:flags=bilinear', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'],
                         stdout=subprocess.PIPE); return p
active = []; starts = {}
for c in T['cues']: starts.setdefault(c['tl_in'], []).append(c)
bad = []; worst = 0
lo, hi = frames[0], frames[-1]
# percorre todos os quadros de lo a hi mantendo leitores dos cues ativos
for f in range(0, hi + 1):
    for c in starts.get(f, []): active.append([c, rd(c)])
    img = None; keep = []
    for c, pr in active:
        if f >= c['tl_out']:
            pr.stdout.close(); pr.wait(); continue
        ob = pr.stdout.read(W * H * 4)
        if len(ob) < W * H * 4: pr.stdout.close(); pr.wait(); continue
        keep.append([c, pr])
        if f < lo: continue
        o = np.frombuffer(ob, np.uint8).reshape(H, W, 4).astype(np.float32); a = o[:, :, 3:4] / 255
        if img is None: img = np.zeros((H, W, 3), np.float32) + np.array([255, 0, 255], np.float32)
        img = o[:, :, :3] * a + img * (1 - a)
    active = keep
    if f in frames and img is not None:
        mag = ((img[:, :, 0] > 200) & (img[:, :, 1] < 60) & (img[:, :, 2] > 200)).mean()
        if mag > 0.002 and f not in allowed:
            bad.append((f, round(f / FPS, 2), round(float(mag) * 100, 2)))
    elif f in frames and img is None and f not in allowed:
        bad.append((f, round(f / FPS, 2), 100.0))
print('quadros de tela cheia com câmera visível FORA das janelas intencionais:', len(bad))
for b in bad[:60]: print('  frame', b[0], 't=', b[1], f'{b[2]}% magenta')
json.dump(bad, open(os.path.join(HERE, '..', 'work', 'v2', 'qa', 'leak_report.json'), 'w'))
