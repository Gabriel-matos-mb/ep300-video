"""Review 01 — (1) trilha-base: pré-sessão + blooper + BASE do Gabriel (+ freezes P_EVOL/GRITEM + bloco do insert final) em ProRes; (2) composição dos layers em janelas; (3) mux com mix.wav."""
import subprocess, os, json, sys
from common import *

FPSS = f'{FPSN}/{FPSD}'
SEG = os.path.join(WORK, 'seg'); os.makedirs(SEG, exist_ok=True)
CH = os.path.join(OUTW, 'chunks'); os.makedirs(CH, exist_ok=True)
BASE = os.path.join(WORK, 'base_720.mp4')
PRO = ['-c:v', 'prores_ks', '-profile:v', '2', '-pix_fmt', 'yuv422p10le', '-r', FPSS, '-an']


def run(cmd, tag=''):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-y'] + cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode:
        sys.exit(f'FAIL {tag}: {r.stderr[-600:]}')


def nframes(f):
    r = subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', f], capture_output=True, text=True)
    return int(r.stdout.strip().strip(','))


def base_seg(a, b, out):
    run(['-i', BASE, '-vf', f'trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS,fps={FPSS},format=yuv422p10le', '-frames:v', str(b - a)] + PRO + [out], f'base {a}-{b}')


def freeze_seg(frame, n, out):
    run(['-i', BASE, '-vf', f'trim=start_frame={frame}:end_frame={frame + 1},setpts=PTS-STARTPTS,loop=loop={n - 1}:size=1:start=0,fps={FPSS},format=yuv422p10le', '-frames:v', str(n)] + PRO + [out], f'freeze {frame}')


def gritem_seg(n, out):
    # freeze do 4K (frame escolhido 123.2 s) com push de reenquadramento: Gustavo à esquerda, espaço negativo à direita p/ a placa
    e = '(1-pow(1-min(on/9,1),3))'
    vf = (f"zoompan=z='1+0.35*{e}':x='{e}*0.228*iw':y='{e}*0.086*ih':d={n}:s=1280x720:fps={FPSS},format=yuv422p10le")
    run(['-loop', '1', '-i', os.path.join(WORK, 'gritem_4k.png'), '-vf', vf, '-frames:v', str(n)] + PRO + [out], 'gritem')


def black_seg(n, out):
    run(['-f', 'lavfi', '-i', f'color=black:s=1280x720:r={FPSS}', '-frames:v', str(n), '-pix_fmt', 'yuv422p10le'] + PRO[:-1] + [out], 'black')


def pre_seg(name, n, out):
    src = os.path.join(LAYERS, name + '.mov') if name != 'BLOOPER' else os.path.join(WORK, 'blooper.mov')
    if os.path.exists(src):
        run(['-i', src, '-vf', f'fps={FPSS},format=yuv422p10le', '-frames:v', str(n)] + PRO + [out], name)
    else:
        print('  (placeholder preto para', name, ')'); black_seg(n, out)


GRITEM_FREEZE_FRAME = 2954   # 123.2 s: sorriso aberto + gesto de 'gritar' (frames vizinhos: mão cobrindo o rosto/olhos semicerrados)


# BQ_MARKETING: no plano fechado do Gustavo (base 96.97-98.47 s) o grupo vai para a parede livre à direita do rosto
_E = 10 ** 6
TRANSFORMS = {   # id -> [(quadro_final_ini, quadro_final_fim, spec)] ; spec = ('c', escala, alvo_x, alvo_y) | ('s', escala, dx, dy) | (escala, ex, ey, tx, ty)
    'BQ_MARKETING': [(F(2325), F(2361), (1.0, 0, 0, 330, 0))],
    'C01_01': [(F(141), F(156), ('c', 0.9, 640, 560)), (F(156), _E, ('c', 0.8, 640, 600))],
    'C06_01': [(F(fr(187.3)), F(fr(187.81)), ('c', 1.0, 640, 430)), (F(fr(187.81)), _E, ('c', 1.0, 1050, 400))],
    'C06_04': [] if REV != '02' else [(F(fr(207.3)), _E, (1.0, 0, 0, -520, 60))],
    'C07_01': [(F(fr(249.8)), _E, ('c', 0.9, 640, 440))],
    'CEM_MIL_HORAS': [(F(fr(255.8)), F(fr(256.46)), ('c', 0.6, 640, 590)), (F(fr(256.46)), _E, ('c', 0.6, 600, 655))],
}   # id -> [(quadro_final_ini, quadro_final_fim, (escala, ex, ey, tx, ty))]; preenchido abaixo


def stage1(only=None):
    segs = []
    for name, n in PRE_ORDER:
        o = os.path.join(SEG, f'pre_{name}.mov'); (pre_seg(name, n, o) if only is None else None); segs.append(o)
    h1, h2 = HOLDS
    plan = [('b0', lambda o: base_seg(0, h1[0], o)),
            ('f1', lambda o: freeze_seg(h1[0] - 1, h1[1], o)),
            ('b1', lambda o: base_seg(h1[0], h2[0], o)),
            ('f2', lambda o: gritem_seg(h2[1], o)),
            ('b2', lambda o: base_seg(h2[0], INS_AT, o)),
            ('ins', lambda o: black_seg(INS_FR, o)),
            ('b3', lambda o: base_seg(INS_AT, BASE_FR, o))]
    for k, fn in plan:
        o = os.path.join(SEG, k + '.mov')
        if only is None or k in only: fn(o)
        segs.append(o)
    lst = os.path.join(SEG, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{s.replace(chr(92), '/')}'\n" for s in segs))
    out = os.path.join(WORK, 'track_base.mov')
    run(['-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', out], 'concat base')
    n = nframes(out)
    print('track_base frames', n, 'esperado', total_frames())
    assert n == total_frames(), 'quadros da trilha-base != esperado'


DROP_LAYERS = {'C05_03'}   # choro: o Gustavo brinca de chorar na propria camera (R02); sem sticker


def _cov(path, n):
    """cobertura alfa (inicio, meio, fim) + cor de fundo do quadro do meio; cache por mtime"""
    import numpy as np
    cache = os.path.join(WORK, 'cov_cache.json')
    C = json.load(open(cache)) if os.path.exists(cache) else {}
    key = f'{os.path.basename(path)}:{os.path.getmtime(path):.0f}:{n}'
    if key in C: return C[key]
    cov = []
    col = None
    for q in (0.04, 0.5, 0.96):
        r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{n * q / FPS:.3f}', '-i', path, '-frames:v', '1', '-vf', 'scale=64:36,format=rgba', '-f', 'rawvideo', '-'], capture_output=True)
        a = np.frombuffer(r.stdout, np.uint8).reshape(-1, 4) if len(r.stdout) == 64 * 36 * 4 else np.zeros((1, 4), np.uint8)
        cov.append(round(float((a[:, 3] > 200).mean()), 2))
        if q == 0.5 and len(a) > 1: col = '%02x%02x%02x' % tuple(int(v) for v in np.median(a[a[:, 3] > 200][:, :3], axis=0)) if (a[:, 3] > 200).any() else '000000'
    C[key] = dict(cov=cov, color=col)
    json.dump(C, open(cache, 'w'))
    return C[key]


def _bbox_center(path, n):
    import numpy as np
    cache = os.path.join(WORK, 'bbox_cache.json')
    C = json.load(open(cache)) if os.path.exists(cache) else {}
    key = f'{os.path.basename(path)}:{os.path.getmtime(path):.0f}'
    if key in C: return C[key]
    ub = None
    for q in np.linspace(0.05, 0.95, 10):
        r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{n * q / FPS:.3f}', '-i', path, '-frames:v', '1', '-vf', 'format=rgba', '-f', 'rawvideo', '-'], capture_output=True)
        if len(r.stdout) != 1280 * 720 * 4: continue
        a = np.frombuffer(r.stdout, np.uint8).reshape(720, 1280, 4)[:, :, 3]
        ys, xs = np.where(a > 20)
        if len(xs):
            b = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
            ub = b if ub is None else (min(ub[0], b[0]), min(ub[1], b[1]), max(ub[2], b[2]), max(ub[3], b[3]))
    C[key] = [(ub[0] + ub[2]) / 2, (ub[1] + ub[3]) / 2]
    json.dump(C, open(cache, 'w'))
    return C[key]


def stage2(only_chunk=None):
    ev = []
    for p in placements():
        if p['id'] in DROP_LAYERS: continue
        if not os.path.exists(p['file']):
            print('  AUSENTE:', p['id']); continue
        n = nframes(p['file'])
        info = _cov(p['file'], n)
        ev.append(dict(id=p['id'], a=p['start_f'], n=n, b=min(p['start_f'] + n, total_frames()), file=p['file'], cov=info['cov'], color=info['color'],
                       full=info['cov'][1] > 0.95, clone=0, under=None))
    ev.sort(key=lambda e: e['a'])
    # --- tela grafica -> tela grafica: sem quadros de camera no meio (gap <= 30 quadros)
    fulls = [e for e in ev if e['full']]
    for e in fulls:
        if e['cov'][0] < 0.9 or e['cov'][2] < 0.9:
            e['under'] = [e['a'], e['b']]
    for A, B in zip(fulls, fulls[1:]):
        gap = B['a'] - A['b']
        if 0 < gap <= 30:
            if A['cov'][2] >= 0.9:
                A['clone'] = gap; A['b'] += gap
            else:
                A['under'][1] = B['a']
    for e in ev:
        e['bx'] = max(e['b'], e['under'][1]) if e['under'] else e['b']
    T = total_frames()
    cand = sorted({0, T} | {e['a'] for e in ev} | {e['bx'] for e in ev})
    def crossed(c): return any(e['a'] < c < e['bx'] for e in ev)
    cand = [c for c in cand if not crossed(c)]
    chunks = []; s = 0
    while s < T:
        nxt = [c for c in cand if c > s and c - s <= 1000]
        e_ = max(nxt) if nxt else min(c for c in cand if c > s)
        chunks.append((s, e_)); s = e_
    files = []
    for i, (a, b) in enumerate(chunks):
        o = os.path.join(CH, f'c{i:03d}.mp4'); files.append(o)
        if only_chunk is not None and i not in only_chunk and os.path.exists(o): continue
        inside = [e for e in ev if e['a'] >= a and e['bx'] <= b]
        inputs = ['-ss', f'{a / FPS:.5f}', '-i', os.path.join(WORK, 'track_base.mov')]
        fc = ['[0:v]fps=%s,format=yuv420p[v0]' % FPSS]
        last = 'v0'; k = 0
        for e in inside:
            off = (e['a'] - a) / FPS
            if e['under']:
                k += 1; inputs += ['-f', 'lavfi', '-i', f"color=c=0x{e['color']}:s=1280x720:r={FPSS}"]
                ua, ub = (e['under'][0] - a - 0.5) / FPS, (e['under'][1] - a - 0.5) / FPS
                fc.append(f"[{last}][{k}:v]overlay=eof_action=repeat:enable='between(t,{ua:.5f},{ub:.5f})'[u{k}]"); last = f'u{k}'
            k += 1; inputs += ['-i', e['file']]
            end = off + (e['n'] + e['clone'] - 0.5) / FPS
            pad = f",tpad=stop_mode=clone:stop={e['clone']}" if e['clone'] else ''
            tfm = TRANSFORMS.get(e['id'], [])
            wins = [(wa - a, wb - a, t) for (wa, wb, t) in tfm]
            segs_ = []; cur = e['a'] - a
            for (wa, wb, t) in sorted(wins, key=lambda w: w[0]):
                if wa > cur: segs_.append((cur, wa, None))
                segs_.append((wa, wb, t)); cur = wb
            if cur < e['a'] - a + e['n'] + e['clone']: segs_.append((cur, e['a'] - a + e['n'] + e['clone'], None))
            fc.append(f'[{k}:v]fps={FPSS}{pad},setpts=PTS-STARTPTS+{off:.5f}/TB,split={len(segs_)}' + ''.join(f'[l{k}_{j}]' for j in range(len(segs_))))
            for j, (wa, wb, t) in enumerate(segs_):
                en = f"between(t,{max(off, wa / FPS) - 0.5 / FPS:.5f},{min(end, (wb - 0.5) / FPS):.5f})"
                src = f'l{k}_{j}'
                if t:
                    if t[0] == 'c':
                        sc = t[1]; ex, ey = _bbox_center(e['file'], e['n']); tx, ty = t[2], t[3]
                    elif t[0] == 's':
                        sc = t[1]; ex, ey = _bbox_center(e['file'], e['n']); tx, ty = ex + t[2], ey + t[3]
                    else:
                        sc, ex, ey, tx, ty = t
                    fc.append(f'[{src}]scale=iw*{sc}:ih*{sc}:flags=lanczos[{src}s]'); src += 's'
                    x, y = int(tx - ex * sc), int(ty - ey * sc)
                else:
                    x = y = 0
                fc.append(f"[{last}][{src}]overlay=x={x}:y={y}:eof_action=repeat:format=auto:enable='{en}'[v{k}_{j}]")
                last = f'v{k}_{j}'
        fc.append(f'[{last}]format=yuv420p[vo]')
        run(inputs + ['-filter_complex', ';'.join(fc), '-map', '[vo]', '-frames:v', str(b - a), '-c:v', 'libx264', '-preset', 'medium', '-crf', '17',
                      '-g', '24', '-keyint_min', '24', '-sc_threshold', '0', '-pix_fmt', 'yuv420p', '-r', FPSS, '-an', o], f'chunk {i} {a}-{b} ({[e["id"] for e in inside]})')
        print(f'chunk {i:02d} {a}-{b} {[e["id"] for e in inside]}', flush=True)
    lst = os.path.join(CH, 'list.txt')
    open(lst, 'w').write(''.join("file '" + f.replace(chr(92), '/') + "'" + chr(10) for f in files))
    vid = os.path.join(OUTW, 'review_video.mp4')
    run(['-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], 'concat chunks')
    print('video', vid, nframes(vid))
    json.dump([{k_: v for k_, v in e.items() if k_ != 'file'} | {'file': os.path.basename(e['file'])} for e in ev], open(os.path.join(OUTW, 'placement_final.json'), 'w'), indent=1)


def mux(out):
    run(['-i', os.path.join(OUTW, 'review_video.mp4'), '-i', os.path.join(OUTW, 'mix.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac',
         '-b:a', '256k', '-shortest', '-movflags', '+faststart', out], 'mux')
    print('OK', out)


if __name__ == '__main__':
    what = sys.argv[1:] or ['stage1', 'stage2']
    if 'stage1' in what: stage1()
    if 'stage1_f2' in what: stage1(['f2'])
    if 'stage2' in what: stage2()
    for w in what:
        if w.startswith('chunk') and w[5:].isdigit(): stage2([int(w[5:])])
    if 'mux' in what: mux(os.path.join(HERE, f'V4_PRESENTABLE_REVIEW_{REV}.mp4'))
