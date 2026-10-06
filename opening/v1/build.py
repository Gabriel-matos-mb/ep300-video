"""EP300 · V1 — build: plan.py → overlays (ProRes 4444 alpha) + base de câmera + mix + preview + XML Premiere.

Derivado do build da V0 (../v0/build.py continua intacto e gera a V0). Tudo da V1 vai para work/build_v1 e, no
Drive, para V1_GERADOS / EP300_ABERTURA_V1 / *_V1_PROXY.mp4 — nenhum arquivo da V0 é reescrito.

Uso:  python build.py [stills] [overlays] [base] [audio] [preview] [xml] [manifest]   (sem args = tudo)
      python build.py overlays --only C04_04
"""
import os, sys, glob, json, math, subprocess, wave, time
from concurrent.futures import ProcessPoolExecutor
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plan, grade

FPS = plan.FPS
WORK = os.path.join(HERE, '..', 'work')
B = os.path.join(WORK, 'build_v1'); os.makedirs(B, exist_ok=True)
EP = glob.glob('I:/Drives compartilhados/Educa*/Marketing*/01_CANAIS_ATIVOS/02_PODCAST/2026/300_*/01_VIDEO DE ABERTURA')[0]
BRUTOS = os.path.join(EP, '01_BRUTOS')
SRC = {'W': os.path.join(BRUTOS, 'CAM_GERAL.mp4'), 'G': os.path.join(BRUTOS, 'MVI_9943-CAM_GUSTAVO.MP4'),
       'L': os.path.join(BRUTOS, 'MVI_9943-CAM_LUCIAN.MP4')}
SRC_RATE = {'W': (30, False), 'G': (24, True), 'L': (24, True)}
BLOOP_DIR = glob.glob(os.path.join(glob.escape(EP), '00_ASSETS E INSERTS', 'erros de grava*'))[0]
MEDIA = {  # mídias da pré-sessão (só leitura) — (arquivo, fps, (w,h), duração s)
    'B_2023_05_24': (os.path.join(BLOOP_DIR, '2023-05-24 09-51-47.mp4'), 60, (1920, 1080), 12.95),
    'B_VERDADES': (os.path.join(BLOOP_DIR, 'VERDADES INCONVENIENTES SOBRE ANALYTICS.mp4'), 30, (1920, 1080), 24.667),
}
# o XML aponta para CÓPIAS com nome curto em V1_GERADOS/BASTIDORES (o caminho original de um deles passa de 260
# caracteres — limite do Windows/Premiere). Originais continuam em 'erros de gravação antigos'.
MEDIA_XML = {k: os.path.join(EP, '00_ASSETS E INSERTS', 'V1_GERADOS', 'BASTIDORES', k + '.mp4') for k in MEDIA}
PROXY = {k: os.path.join(WORK, 'proxy', f'{n}_720p30.mp4') for k, n in (('W', 'geral'), ('G', 'gustavo'), ('L', 'lucian'))}
D_ASSETS = os.path.join(EP, '00_ASSETS E INSERTS', 'V1_GERADOS')
D_PROJ = os.path.join(EP, '02_PROJETOS', 'EP300_ABERTURA_V1')
D_EDIT = os.path.join(EP, '03_EDITADOS')
L_OVL = os.path.join(B, 'OVERLAYS'); L_STILL = os.path.join(B, 'STILLS'); L_AUD = os.path.join(B, 'AUDIO')
L_LUT = os.path.join(B, 'LUTS')
for d in (L_OVL, L_STILL, L_AUD, L_LUT): os.makedirs(d, exist_ok=True)
MA = os.path.join(WORK, 'audio', 'ma')
LEAD = plan.W_VIDEO_LEAD_FRAMES / FPS
NAME = 'EP300_ABERTURA_V1'


def fr(t):
    return int(round(t * FPS))


def base_cam(cam):
    return 'W' if cam.startswith('W') else cam


# ------------------------------------------------------------------ timeline
def timeline():
    segs, shots = [], []
    pre = []
    for tl, key, a, b, trt in plan.PRESHOTS:
        pre.append(dict(key=key, tl_in=fr(tl), tl_out=fr(tl) + fr(b - a), m_in=a, m_out=b, trt=trt))
    cur = fr(plan.INTRO_DUR - plan.INTRO_OVERLAP)
    for sid, a, b, cams in plan.SEGMENTS:
        n = fr(b - a) if sid != 'HOLD' else fr(plan.HOLD_GRITEM)
        seg = dict(id=sid, src_in=a, src_out=a + n / FPS, tl_in=cur, tl_out=cur + n)
        segs.append(seg)
        if sid == 'HOLD':
            shots.append(dict(seg=sid, cam='FREEZE', still=cams, tl_in=cur, tl_out=cur + n, src_in=None))
        else:
            for i, (st, cam) in enumerate(cams):
                ti = cur + fr(st - a)
                to = cur + (fr(cams[i + 1][0] - a) if i + 1 < len(cams) else n)
                shots.append(dict(seg=sid, cam=cam, tl_in=ti, tl_out=to, src_in=a + (ti - cur) / FPS))
        cur += n
    end = cur

    def src2tl(s, strict=True):
        for sg in segs:
            if sg['id'] != 'HOLD' and sg['src_in'] - 1e-6 <= s < sg['src_out'] + 1e-6:
                return sg['tl_in'] + fr(s - sg['src_in'])
        if strict: raise ValueError(f'fonte {s} fora da montagem')
        nxt = [sg for sg in segs if sg['id'] != 'HOLD' and sg['src_in'] >= s]
        return nxt[0]['tl_in'] if nxt else end

    cues = []
    for c in plan.CUES:
        tl = c.get('tl')
        if tl == 'END': t0 = end
        elif tl == 'END+TITLE': t0 = end + fr(plan.TITLE_DUR)
        elif tl is not None: t0 = fr(tl)
        else: t0 = src2tl(c['st'])
        cues.append(dict(c, tl_in=t0, tl_out=t0 + fr(c['dur'])))
    total = end + fr(plan.OUTRO_DUR)
    return dict(pre=pre, segs=segs, shots=shots, cues=cues, end=end, total=total, src2tl=src2tl,
                cam0=fr(plan.INTRO_DUR - plan.INTRO_OVERLAP))


# ------------------------------------------------------------------ reenquadramento (punch-in na CAM_GERAL)
def crop_box(cam, w_in, h_in):
    s, cx, cy = plan.CROPS.get(cam, (1.0, 960, 540))
    k = w_in / 1920
    cw, ch = int(round(w_in / s / 2)) * 2, int(round(h_in / s / 2)) * 2
    x = min(max(0, int(cx * k - cw / 2)), w_in - cw); y = min(max(0, int(cy * k - ch / 2)), h_in - ch)
    return cw, ch, x, y


def vf_cam(cam, w_in, h_in, W=1280, H=720, graded=True):
    f = []
    if cam in plan.CROPS and cam != 'W':
        cw, ch, x, y = crop_box(cam, w_in, h_in); f.append(f'crop={cw}:{ch}:{x}:{y}')
    f.append(f'scale={W}:{H}:flags=lanczos')
    if graded and plan.GRADE: f.append(grade.vf(base_cam(cam), L_LUT))
    return ','.join(f)


# ------------------------------------------------------------------ stills (freeze, a partir do ORIGINAL)
def freeze_path(key):
    _, cam, t = key.split(':')
    return os.path.join(L_STILL, f'FREEZE_{cam}_{t.replace(".", "_")}.png')

def freeze_keys():
    return sorted({cams for sid, a, b, cams in plan.SEGMENTS if sid == 'HOLD'})

def do_stills():
    for k in freeze_keys():
        _, cam, t = k.split(':'); p = freeze_path(k)
        if os.path.exists(p): continue
        bc = base_cam(cam)
        ts = float(t) - plan.OFFSETS[bc] + (LEAD if bc == 'W' else 0)
        w_in, h_in = (1920, 1080) if bc == 'W' else (3840, 2160)
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{ts:.3f}', '-i', SRC[bc], '-frames:v', '1',
                        '-vf', vf_cam(cam, w_in, h_in, 1920, 1080, graded=False), p], check=True)
        print('still', p)


def load_freezes():
    import customs
    for k in freeze_keys():
        customs.FREEZES[k] = freeze_path(k)


# ------------------------------------------------------------------ overlays
def ovl_path(c):
    return os.path.join(L_OVL, f"{c['id']}_{c['name']}.mov")

def render_cue(cid):
    import engine, customs
    load_freezes()
    c = next(x for x in plan.CUES if x['id'] == cid)
    n = fr(c['dur']); out = ovl_path(c)
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', '1920x1080',
                          '-r', str(FPS), '-i', '-', '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le',
                          '-alpha_bits', '16', '-vendor', 'apl0', '-qscale:v', '9', out], stdin=subprocess.PIPE)
    t0 = time.time()
    for i in range(n):
        p.stdin.write(engine.render_frame(c, i / FPS).tobytes())
    p.stdin.close(); p.wait()
    mid = engine.render_frame(c, min(c['dur'] - .4, max(.6, c['dur'] * .6)))
    mid.save(os.path.join(L_OVL, f"{c['id']}_ref.png"))
    return cid, n, round(time.time() - t0, 1)

def do_overlays(only=None):
    ids = [c['id'] for c in plan.CUES if not only or c['id'] in only]
    with ProcessPoolExecutor(max_workers=8) as ex:
        for cid, n, dt in ex.map(render_cue, ids):
            print(f'overlay {cid}: {n} frames em {dt}s', flush=True)


# ------------------------------------------------------------------ base de câmera (preview 720p)
def do_base(T):
    parts = []
    lst = os.path.join(B, 'base_list.txt')
    def piece(name, args):
        p = os.path.join(B, 'pieces', name); os.makedirs(os.path.dirname(p), exist_ok=True)
        if not os.path.exists(p):
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y'] + args + ['-r', str(FPS), '-c:v', 'h264_nvenc', '-preset', 'p4',
                            '-cq', '20', '-pix_fmt', 'yuv420p', '-an', p], check=True)
        parts.append(p)
    g = 'g' if plan.GRADE else 'n'
    for s in T['pre']:
        n = s['tl_out'] - s['tl_in']
        path, mfps, _, _ = MEDIA[s['key']]
        vf = ('fps=30,scale=1280:720:flags=lanczos,hue=s=0,eq=contrast=1.12:brightness=-0.03,'
              'noise=alls=14:allf=t,vignette=angle=PI/4')
        piece(f"pre_{s['key']}_{s['tl_in']}_{n}.mp4", ['-ss', f"{s['m_in']:.3f}", '-i', path, '-vf', vf, '-frames:v', str(n)])
    gap = T['cam0'] - T['pre'][-1]['tl_out']
    piece(f'black_{gap}.mp4', ['-f', 'lavfi', '-i', f'color=black:s=1280x720:r={FPS}', '-frames:v', str(gap)])
    for s in T['shots']:
        n = s['tl_out'] - s['tl_in']
        if s['cam'] == 'FREEZE':
            piece(f"freeze_{s['tl_in']}_{n}_{g}.mp4", ['-loop', '1', '-i', freeze_path(s['still']), '-vf',
                                                       vf_cam('W', 1920, 1080), '-frames:v', str(n)])
            continue
        cam = s['cam']; bc = base_cam(cam)
        ss = s['src_in'] - plan.OFFSETS[bc] + (LEAD if bc == 'W' else 0)
        if bc == 'W' and cam != 'W':   # punch-in: lê o ORIGINAL 1080p (proxy 720 perderia definição)
            args = ['-ss', f'{ss:.4f}', '-i', SRC['W'], '-vf', vf_cam(cam, 1920, 1080), '-frames:v', str(n)]
        else:
            args = ['-ss', f'{ss:.4f}', '-i', PROXY[bc], '-vf', vf_cam(cam, 1280, 720), '-frames:v', str(n)]
        piece(f"{cam}_{s['tl_in']}_{n}_{ss:.3f}_{g}.mp4", args)
    tail = T['total'] - T['shots'][-1]['tl_out']
    piece(f'black_tail_{tail}.mp4', ['-f', 'lavfi', '-i', f'color=black:s=1280x720:r={FPS}', '-frames:v', str(tail)])
    with open(lst, 'w') as f:
        for p in parts: f.write(f"file '{p.replace(os.sep, '/')}'\n")
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy',
                    os.path.join(B, 'base_720.mp4')], check=True)
    print('base ok', T['total'], 'frames')


# ------------------------------------------------------------------ áudio
SR = 48000
def rd(path):
    w = wave.open(path); n = w.getnframes(); ch = w.getnchannels(); sw = w.getsampwidth(); sr = w.getframerate()
    raw = w.readframes(n)
    if sw == 2: x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    elif sw == 3:
        b = np.frombuffer(raw, np.uint8).reshape(-1, 3)
        x = ((b[:, 0].astype(np.int32) << 8 | b[:, 1].astype(np.int32) << 16 | b[:, 2].astype(np.int32) << 24) >> 8).astype(np.float32) / 8388608
    elif sw == 4: x = np.frombuffer(raw, np.int32).astype(np.float32) / 2147483648
    x = x.reshape(-1, ch)
    if ch == 1: x = np.repeat(x, 2, 1)
    if sr != SR:
        idx = np.arange(0, len(x), sr / SR); x = np.stack([np.interp(idx, np.arange(len(x)), x[:, i]) for i in range(2)], 1)
    return x[:, :2].astype(np.float32)

def wr(path, x):
    y = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    w = wave.open(path, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.tobytes()); w.close()

def db(g): return 10 ** (g / 20)

def fade(x, fi, fo):
    x = x.copy(); n = len(x)
    if fi: k = min(n, int(fi * SR)); x[:k] *= np.linspace(0, 1, k)[:, None]
    if fo: k = min(n, int(fo * SR)); x[n - k:] *= np.linspace(1, 0, k)[:, None]
    return x

SFX = {  # (arquivo, ganho dB, (início, duração) no arquivo) — biblioteca Motion Array da MB
    'click': ('MA_SergeySopko_MouseClick_1.wav', -6, None),
    'whoosh': ('MA_Amenteramco_Whoosh_Pass-By_1.wav', -12, None),
    'impact': ('01 Impact.wav', -16, (0, 1.6)),
    'tvoff': ('Turn the TV Off and On 1.wav', -8, None),
    'wrong': ('MA_AppleHillStudios_WrongAnswer_1.wav', -8, None),
    'ding': ('MA_SoundsByGFXSounds_DingNotification_1.wav', -16, (0, 1.2)),
    'tick': ('01 Clock Ticking.wav', -14, (0, 3.0)),
    'pencil': ('Pencil Line 1.wav', -10, None),
    'woosh_boom': ('MA_AleXZavesa_WooshAndBoom_1.wav', -14, None),
}
MUSIC = dict(aviso='MA_LEXMusic_BeatTheOdds_30s.wav', bed='Trigubovich_A_Groove_Pool_loop_long.wav',
             final='MA_Puremusic_InTheSpotlight_12s.wav')

def sfx_events(T):
    ev = []
    for c in T['cues']:
        for dt, k in c.get('sfx', []):
            ev.append((c['tl_in'] / FPS + dt, k))
    return sorted(ev)

def pre_audio_path(key):
    return os.path.join(L_AUD, f'COLD_{key}.wav')

def snap_min(env, t, r=.06):
    """borda de corte no ponto mais silencioso num raio de ±r s (envelope 10 ms da CAM_GERAL)."""
    i0, i1 = int((t - r) * 100), int((t + r) * 100)
    return (i0 + int(np.argmin(env[i0:i1 + 1]))) / 100

def music_marks(T):
    aviso = next(c for c in T['cues'] if c['id'] == 'C00_03')['tl_in'] / FPS
    speech0 = T['cam0'] / FPS + plan.INTRO_OVERLAP + (507.85 - plan.SEGMENTS[0][1])
    title = next(c for c in T['cues'] if c['id'] == 'C08_01')['tl_in'] / FPS
    return aviso, speech0, title

def do_audio(T):
    N = int(T['total'] / FPS * SR) + SR
    dia, mus, sfx = np.zeros((N, 2), np.float32), np.zeros((N, 2), np.float32), np.zeros((N, 2), np.float32)
    G = rd(os.path.join(WORK, 'audio', 'geral_48k.wav'))
    # pré-sessão: áudio dos bastidores
    for s in T['pre']:
        p = pre_audio_path(s['key'])
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f"{s['m_in']:.3f}", '-t', f"{s['m_out'] - s['m_in']:.3f}",
                        '-i', MEDIA[s['key']][0], '-ac', '2', '-ar', str(SR), '-af', 'highpass=f=80,loudnorm=I=-20:TP=-3', p], check=True)
        x = fade(rd(p), .08, .06)
        q = int(s['tl_in'] / FPS * SR); dia[q:q + len(x)] += x[:N - q]
    ids = [sg['id'] for sg in T['segs']]
    for i, sg in enumerate(T['segs']):
        if sg['id'] == 'HOLD': continue
        a, b = int(sg['src_in'] * SR), int(sg['src_out'] * SR)
        fi = .06 if i > 0 and ids[i - 1] == 'HOLD' else .02
        fo = .06 if i + 1 < len(ids) and ids[i + 1] == 'HOLD' else .02
        if sg['id'] in ('S2a', 'S2a2'): fi, fo = (fi, .04) if sg['id'] == 'S2a' else (.04, fo)  # emenda do "2025" (-32 dB)
        x = fade(G[a:b], fi, fo)
        p = int(sg['tl_in'] / FPS * SR); dia[p:p + len(x)] += x
    for a, b, why in plan.BLEEPS:
        p0 = int((T['src2tl'](a) / FPS) * SR); n = int((b - a) * SR)
        dia[p0:p0 + n] = 0
        tt = np.arange(n) / SR; tone = (0.18 * np.sin(2 * np.pi * 1000 * tt)).astype(np.float32)
        tone = fade(np.stack([tone, tone], 1), .01, .01); sfx[p0:p0 + n] += tone
        wr(os.path.join(L_AUD, 'SFX_BLEEP_1kHz.wav'), tone)
    aviso, speech0, title = music_marks(T)
    # trilha do aviso (pré-sessão) — entra com o aviso, sai por baixo da íris
    av = rd(os.path.join(MA, MUSIC['aviso']))
    a0 = int(aviso * SR); a1 = int((speech0 + .6) * SR)
    av = av[:a1 - a0]
    env = np.ones(len(av), np.float32); k0 = int((speech0 - 1.6 - aviso) * SR)
    if 0 < k0 < len(av): env[k0:] = np.linspace(1, db(-30), len(av) - k0)
    mus[a0:a0 + len(av)] += fade(av, .4, .2) * env[:, None] * db(-13)
    # fundo sob o diálogo
    bed = rd(os.path.join(MA, MUSIC['bed']))
    b0, b1 = int((speech0 - 1.0) * SR), int((title - .2) * SR)
    reps = int(math.ceil((b1 - b0) / len(bed))) + 1
    bedl = fade(np.concatenate([bed] * reps)[:b1 - b0], 2.5, 1.4) * db(-31)
    hold = next(s for s in T['segs'] if s['id'] == 'HOLD')
    h0, h1 = int(hold['tl_in'] / FPS * SR) - b0, int(hold['tl_out'] / FPS * SR) - b0
    e2 = np.ones(len(bedl), np.float32)
    ramp = int(.15 * SR); e2[h0 - ramp:h0] = np.linspace(1, db(10), ramp); e2[h0:h1] = db(10); e2[h1:h1 + ramp] = np.linspace(db(10), 1, ramp)
    mus[b0:b1] += bedl * e2[:, None]
    # final: entra com fade (marcador 5:18 — não entrar estourando) e segue sob o "300 e contando"
    out = rd(os.path.join(MA, MUSIC['final']))
    o0 = int(title * SR); out = fade(out[:N - o0], 1.2, 1.2) * db(-9)
    mus[o0:o0 + len(out)] += out
    cache = {}
    for t, k in sfx_events(T):
        if k == 'beep':
            n = int(.09 * SR); tt = np.arange(n) / SR; x = (0.25 * np.sin(2 * np.pi * 1000 * tt)).astype(np.float32)
            x = fade(np.stack([x, x], 1), .004, .01)
            if 'beep' not in cache: wr(os.path.join(L_AUD, 'SFX_LEADER_BEEP_1kHz.wav'), x); cache['beep'] = 1
        else:
            f, g, rng = SFX[k]
            x = rd(os.path.join(MA, f))
            if rng: x = fade(x[int(rng[0] * SR):int((rng[0] + rng[1]) * SR)], 0, .3)
            x = x * db(g)
        p = max(0, int(t * SR)); sfx[p:p + len(x)] += x[:max(0, N - p)]
    wr(os.path.join(L_AUD, 'STEM_DIALOGO.wav'), dia); wr(os.path.join(L_AUD, 'STEM_TRILHA.wav'), mus)
    wr(os.path.join(L_AUD, 'STEM_SFX.wav'), sfx)
    mix = dia * db(2) + mus + sfx
    wr(os.path.join(B, 'mix_raw.wav'), mix)
    m = subprocess.run(['ffmpeg', '-hide_banner', '-i', os.path.join(B, 'mix_raw.wav'), '-af',
                        'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
    j = json.loads(m[m.rindex('{'):m.rindex('}') + 1])
    af = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', os.path.join(B, 'mix_raw.wav'), '-af', af, '-ar', str(SR),
                    os.path.join(B, 'mix.wav')], check=True)
    print('audio ok', j['input_i'], '->', '-16')


# ------------------------------------------------------------------ preview (composição)
def do_preview(T, W=1280, H=720):
    out = os.path.join(B, f'{NAME}_PROXY.mp4'); tmp = os.path.join(B, '_preview_video.mp4')
    base = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', os.path.join(B, 'base_720.mp4'), '-f', 'rawvideo',
                             '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                            '-r', str(FPS), '-i', '-', '-c:v', 'h264_nvenc', '-preset', 'p5', '-cq', '21', '-pix_fmt',
                            'yuv420p', '-profile:v', 'high', tmp], stdin=subprocess.PIPE)
    starts = {}
    for c in T['cues']: starts.setdefault(c['tl_in'], []).append(c)
    active = []
    fsz = W * H * 3
    for f in range(T['total']):
        for c in starts.get(f, []):
            pr = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', ovl_path(c), '-vf', f'scale={W}:{H}:flags=bicubic',
                                   '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], stdout=subprocess.PIPE)
            active.append([c, pr])
        buf = base.stdout.read(fsz)
        if len(buf) < fsz: buf = bytes(fsz)
        img = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32)
        keep = []
        for c, pr in active:
            ob = pr.stdout.read(W * H * 4) if f < c['tl_out'] else b''
            if len(ob) < W * H * 4:
                pr.stdout.close(); pr.wait(); continue
            o = np.frombuffer(ob, np.uint8).reshape(H, W, 4).astype(np.float32)
            a = o[:, :, 3:4] / 255.0
            img = o[:, :, :3] * a + img * (1 - a)
            keep.append([c, pr])
        active = keep
        enc.stdin.write(np.clip(img + .5, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait(); base.wait()
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', tmp, '-i', os.path.join(B, 'mix.wav'), '-map', '0:v',
                    '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart',
                    '-t', f"{T['total'] / FPS:.3f}", out], check=True)
    os.remove(tmp)
    print('preview ok', out)


# ------------------------------------------------------------------ manifesto
def tc(frames):
    s, f = divmod(int(frames), FPS); m, s = divmod(s, 60)
    return f'{m:02d}:{s:02d}:{f:02d}'

def do_manifest(T):
    camname = {'W': 'CAM_GERAL.mp4', 'Wz': 'CAM_GERAL.mp4 (reenquadro 1.2×)', 'WG': 'CAM_GERAL.mp4 (punch-in Gustavo 1.6×)',
               'WL': 'CAM_GERAL.mp4 (punch-in Lucian 1.6×)', 'G': 'MVI_9943-CAM_GUSTAVO.MP4', 'L': 'MVI_9943-CAM_LUCIAN.MP4',
               'FREEZE': 'STILLS/FREEZE'}
    man = dict(
        producao='EP300 — Vídeo de Abertura', versao='V1 — Segunda montagem (direção do Gabriel no Premiere)', deriva_de='V0',
        fps=FPS, resolucao_master='1920x1080', duracao=tc(T['total']), duracao_s=round(T['total'] / FPS, 2),
        fontes={k: os.path.basename(v) for k, v in SRC.items()}, offsets_na_CAM_GERAL_s=plan.OFFSETS,
        sync=dict(correcao='imagem da CAM_GERAL lida 5 quadros adiante do áudio da mesa (atraso de captura)',
                  w_video_lead_frames=plan.W_VIDEO_LEAD_FRAMES, validacao='work/v1/sync_report.json (sync_check.py)'),
        cor='proxy: aproximação numérica do Lumetri do Gabriel (grade.py/LUTs); no Premiere: Lumetri original do projeto dele',
        pre_sessao=[dict(tl_in=tc(s['tl_in']), tl_out=tc(s['tl_out']), midia=os.path.basename(MEDIA[s['key']][0]),
                         midia_in_s=s['m_in'], midia_out_s=s['m_out'], tratamento='PB + grão + REC') for s in T['pre']],
        segmentos=[dict(id=s['id'], fonte_in_s=round(s['src_in'], 3), fonte_out_s=round(s['src_out'], 3),
                        tl_in=tc(s['tl_in']), tl_out=tc(s['tl_out'])) for s in T['segs']],
        cortes_editoriais=[dict(fonte_de=a, fonte_ate=b, motivo=m) for a, b, m in plan.CUTS],
        bleeps=[dict(fonte_de=a, fonte_ate=b, motivo=m) for a, b, m in plan.BLEEPS],
        planos=[dict(tl_in=tc(s['tl_in']), tl_out=tc(s['tl_out']), camera=camname[s['cam']], enquadramento=s['cam'],
                     fonte_s=(round(s['src_in'] - plan.OFFSETS[base_cam(s['cam'])] + (LEAD if base_cam(s['cam']) == 'W' else 0), 3)
                              if s['cam'] != 'FREEZE' else s['still'])) for s in T['shots']],
        overlays=[dict(id=c['id'], arquivo=f"OVERLAYS/{c['id']}_{c['name']}.mov", tl_in=tc(c['tl_in']), tl_out=tc(c['tl_out']),
                       tela_cheia=bool(c.get('full')), intencao=c.get('why', '')) for c in T['cues']],
        sfx=[dict(tl=tc(fr(t)), sfx=k) for t, k in sfx_events(T)],
        audio=dict(dialogo='CAM_GERAL (mesa de som) +2 dB; pré-sessão = áudio dos bastidores', trilha_aviso=f"{MUSIC['aviso']} −13 dB",
                   trilha_fundo=f"{MUSIC['bed']} −31 dB (+10 dB no respiro 'Gritem')", trilha_final=f"{MUSIC['final']} −9 dB, fade-in 1,2 s",
                   loudness='mix normalizado −16 LUFS / −1.5 dBTP'),
    )
    p = os.path.join(B, 'timeline_v1.json')
    json.dump(man, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('manifest ok', p)


if __name__ == '__main__':
    only = None
    argv = sys.argv[1:]
    if '--only' in argv:
        k = argv.index('--only'); only = argv[k + 1].split(','); argv = argv[:k] + argv[k + 2:]
    args = [a for a in argv if not a.startswith('--')]
    steps = args or ['stills', 'overlays', 'base', 'audio', 'preview', 'xml', 'manifest']
    T = timeline()
    print(f"timeline: {T['total']} frames = {T['total'] / FPS:.2f}s; fala termina em {T['end'] / FPS:.2f}s")
    if 'stills' in steps: do_stills()
    if 'overlays' in steps: do_overlays(only)
    if 'base' in steps: do_base(T)
    if 'audio' in steps: do_audio(T)
    if 'preview' in steps: do_preview(T)
    if 'xml' in steps:
        import export_xml; export_xml.write(T)
    if 'manifest' in steps: do_manifest(T)
