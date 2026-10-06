"""EP300 · V0 — build: plan.py → overlays (ProRes 4444 alpha) + base de câmera + mix + preview + XML Premiere.

Uso:  python build.py [stills] [overlays] [base] [audio] [preview] [xml] [publish]   (sem args = tudo menos publish)
      python build.py overlays --only C04_04
Nada aqui escreve nos BRUTOS: câmeras só são lidas.
"""
import os, sys, glob, json, math, subprocess, shutil, wave, time
from concurrent.futures import ProcessPoolExecutor
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plan

FPS = plan.FPS
WORK = os.path.join(HERE, '..', 'work')
B = os.path.join(WORK, 'build'); os.makedirs(B, exist_ok=True)
EP = glob.glob('I:/Drives compartilhados/Educa*/Marketing*/01_CANAIS_ATIVOS/02_PODCAST/2026/300_*/01_VIDEO DE ABERTURA')[0]
BRUTOS = os.path.join(EP, '01_BRUTOS')
SRC = {'W': os.path.join(BRUTOS, 'CAM_GERAL.mp4'), 'G': os.path.join(BRUTOS, 'MVI_9943-CAM_GUSTAVO.MP4'),
       'L': os.path.join(BRUTOS, 'MVI_9943-CAM_LUCIAN.MP4')}
SRC_RATE = {'W': (30, False), 'G': (24, True), 'L': (24, True)}
PROXY = {k: os.path.join(WORK, 'proxy', f'{n}_720p30.mp4') for k, n in (('W', 'geral'), ('G', 'gustavo'), ('L', 'lucian'))}
D_ASSETS = os.path.join(EP, '00_ASSETS E INSERTS', 'V0_GERADOS')
D_PROJ = os.path.join(EP, '02_PROJETOS', 'EP300_ABERTURA_V0')
D_EDIT = os.path.join(EP, '03_EDITADOS')
L_OVL = os.path.join(B, 'OVERLAYS'); L_STILL = os.path.join(B, 'STILLS'); L_AUD = os.path.join(B, 'AUDIO')
for d in (L_OVL, L_STILL, L_AUD): os.makedirs(d, exist_ok=True)
MA = os.path.join(WORK, 'audio', 'ma')


def fr(t):  # segundos -> frame inteiro da timeline
    return int(round(t * FPS))


# ------------------------------------------------------------------ timeline
def timeline():
    """-> dict com segmentos (em frames de timeline), shots, cues posicionados."""
    segs, shots = [], []
    cur = fr(plan.INTRO_DUR - plan.INTRO_OVERLAP)
    for sid, a, b, cams in plan.SEGMENTS:
        n = fr(b - a) if sid != 'HOLD' else fr(plan.HOLD_GRITEM)
        seg = dict(id=sid, src_in=a, src_out=a + n / FPS, tl_in=cur, tl_out=cur + n)
        segs.append(seg)
        if sid == 'HOLD':
            shots.append(dict(seg=sid, cam='FREEZE', still=cams, tl_in=cur, tl_out=cur + n, src_in=None))
        else:
            for i, (st, cam) in enumerate(cams):
                en = cams[i + 1][0] if i + 1 < len(cams) else a + n / FPS
                ti, to = cur + fr(st - a), cur + (fr(en - a) if i + 1 < len(cams) else n)
                shots.append(dict(seg=sid, cam=cam, tl_in=ti, tl_out=to, src_in=a + (ti - cur) / FPS))
        cur += n
    end = cur

    def src2tl(s):
        for sg in segs:
            if sg['id'] != 'HOLD' and sg['src_in'] - 1e-6 <= s < sg['src_out'] + 1e-6:
                return sg['tl_in'] + fr(s - sg['src_in'])
        raise ValueError(f'fonte {s} fora da montagem')

    cues = []
    for c in plan.CUES:
        if c.get('tl') == 'END': t0 = end
        elif c.get('tl') is not None: t0 = fr(c['tl'])
        else: t0 = src2tl(c['st'])
        cues.append(dict(c, tl_in=t0, tl_out=t0 + fr(c['dur'])))
    total = max(end + fr(plan.OUTRO_DUR), max(c['tl_out'] for c in cues))
    return dict(segs=segs, shots=shots, cues=cues, end=end, total=total, src2tl=src2tl)


# ------------------------------------------------------------------ stills (freeze frames, a partir do ORIGINAL 4K)
def freeze_path(key):
    _, cam, t = key.split(':')
    return os.path.join(L_STILL, f'FREEZE_{cam}_{t.replace(".", "_")}.png')

def freeze_keys():
    keys = {'freeze:G:508.60'}
    for sid, a, b, cams in plan.SEGMENTS:
        if sid == 'HOLD': keys.add(cams)
    return sorted(keys)

def do_stills():
    for k in freeze_keys():
        _, cam, t = k.split(':'); p = freeze_path(k)
        if os.path.exists(p): continue
        ts = float(t) - plan.OFFSETS[cam]
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{ts:.3f}', '-i', SRC[cam], '-frames:v', '1',
                        '-vf', 'scale=1920:1080:flags=lanczos', p], check=True)
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
        im = engine.render_frame(c, i / FPS)
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()
    # frame de referência (meio do cue) para QA visual
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
                            '-cq', '21', '-pix_fmt', 'yuv420p', '-an', p], check=True)
        parts.append(p)
    first = T['shots'][0]['tl_in']
    piece(f'black_{first}.mp4', ['-f', 'lavfi', '-i', f'color=black:s=1280x720:r={FPS}', '-frames:v', str(first)])
    for s in T['shots']:
        n = s['tl_out'] - s['tl_in']
        if s['cam'] == 'FREEZE':
            piece(f"freeze_{s['tl_in']}_{n}.mp4", ['-loop', '1', '-i', freeze_path(s['still']), '-vf', 'scale=1280:720',
                                                   '-frames:v', str(n)])
        else:
            ss = s['src_in'] - plan.OFFSETS[s['cam']]
            piece(f"{s['cam']}_{s['tl_in']}_{n}.mp4", ['-ss', f'{ss:.4f}', '-i', PROXY[s['cam']], '-frames:v', str(n)])
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

SFX = {  # (arquivo, ganho dB, (início, duração) no arquivo)
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

def sfx_events(T):
    """(tl_segundos, chave) — SFX ancorados nos cues."""
    ev = []
    cue = {c['id']: c['tl_in'] / FPS for c in T['cues']}
    for k in (0, .95, 1.9): ev.append((cue['C00_01'] + k, 'beep'))
    ev += [(cue['C00_02'] + 3.2 + 1.25, 'click'), (cue['C00_02'] + 4.95, 'whoosh')]
    ev += [(cue['C01_01'], 'pencil'), (cue['C01_03'] + 1.2, 'impact'), (cue['C02_02'], 'whoosh'),
           (cue['C03_01'] + 11.4, 'impact'), (cue['C03_02'] + 1.85, 'tvoff'), (cue['C03_04'], 'pencil'),
           (cue['C03_07'] + 14.0, 'impact'), (cue['C03_08'] + 1.1 + 1.2, 'click'), (cue['C04_01'] + .1, 'whoosh'),
           (cue['C04_03'] + 6.1, 'impact'), (cue['C04_04'], 'woosh_boom'), (cue['C04_05'] + .35, 'impact'),
           (cue['C05_02'] + 5.9, 'wrong'), (cue['C05_04'] + 2.5, 'impact'), (cue['C06_03'] + 6.7, 'impact'),
           (cue['C06_04'] + 8.3, 'impact'), (cue['C06_05'] + 4.9, 'impact'), (cue['C06_06'] + 14.6, 'impact'),
           (cue['C07_01'], 'pencil'), (cue['C07_02'] + 2.5 + .9, 'click'), (cue['C07_03'] + 2.9, 'tick'),
           (cue['C07_06'], 'ding'), (cue['C08_01'], 'whoosh')]
    return ev

def do_audio(T):
    N = int(T['total'] / FPS * SR) + SR
    dia, mus, sfx = np.zeros((N, 2), np.float32), np.zeros((N, 2), np.float32), np.zeros((N, 2), np.float32)
    G = rd(os.path.join(WORK, 'audio', 'geral_48k.wav'))
    ids = [sg['id'] for sg in T['segs']]
    for i, sg in enumerate(T['segs']):
        if sg['id'] == 'HOLD': continue
        a, b = int(sg['src_in'] * SR), int(sg['src_out'] * SR)
        fi = .06 if i > 0 and ids[i - 1] == 'HOLD' else .012      # emendas do respiro: fade mais longo
        fo = .06 if i + 1 < len(ids) and ids[i + 1] == 'HOLD' else .012
        x = fade(G[a:b], fi, fo)
        p = int(sg['tl_in'] / FPS * SR); dia[p:p + len(x)] += x
    # bleeps (substitui o trecho por tom de 1 kHz)
    bleep_files = []
    for a, b, why in plan.BLEEPS:
        p0 = int((T['src2tl'](a) / FPS) * SR); n = int((b - a) * SR)
        dia[p0:p0 + n] = 0
        tt = np.arange(n) / SR; tone = (0.18 * np.sin(2 * np.pi * 1000 * tt)).astype(np.float32)
        tone = fade(np.stack([tone, tone], 1), .01, .01); sfx[p0:p0 + n] += tone
        wr(os.path.join(L_AUD, 'SFX_BLEEP_1kHz.wav'), tone)
    # voz: ganho para ~-18 LUFS depois (normalização final cuida do total)
    # trilhas
    st = T['cues'][0]['tl_in'] / FPS
    op = rd(os.path.join(MA, 'MA_LEXMusic_GotTheSwag_Opener.wav'))
    s1 = T['segs'][0]['tl_in'] / FPS
    speech0 = s1 + (507.85 - plan.SEGMENTS[0][1])
    op = op[:int((speech0 + 1.2) * SR)]
    env = np.ones(len(op), np.float32); k0 = int((speech0 - .6) * SR)
    env[k0:] = np.linspace(1, db(-22), len(op) - k0)
    mus[:len(op)] += op * env[:, None] * db(-10)
    bed = rd(os.path.join(MA, 'Trigubovich_A_Groove_Pool_loop_long.wav'))
    title = next(c for c in T['cues'] if c['id'] == 'C08_01')['tl_in'] / FPS
    b0, b1 = int((speech0 - 1.0) * SR), int(title * SR)
    reps = int(math.ceil((b1 - b0) / len(bed))) + 1
    bedl = np.concatenate([bed] * reps)[:b1 - b0]
    bedl = fade(bedl, 2.5, 1.2) * db(-31)
    # respiro "gritem": trilha sobe no hold
    hold = next(s for s in T['segs'] if s['id'] == 'HOLD')
    h0, h1 = int(hold['tl_in'] / FPS * SR) - b0, int(hold['tl_out'] / FPS * SR) - b0
    e2 = np.ones(len(bedl), np.float32)
    ramp = int(.15 * SR); e2[h0 - ramp:h0] = np.linspace(1, db(10), ramp); e2[h0:h1] = db(10); e2[h1:h1 + ramp] = np.linspace(db(10), 1, ramp)
    mus[b0:b1] += bedl * e2[:, None]
    out = rd(os.path.join(MA, 'MA_Puremusic_InTheSpotlight_12s.wav'))
    o0 = int(title * SR); tot = N - o0
    out = out[:tot]; out = fade(out, .3, 1.0) * db(-9)
    ob = np.ones(len(out), np.float32)  # baixa sob "Obrigado, gente"
    mus[o0:o0 + len(out)] += out
    # sfx
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
        p = int(t * SR); sfx[p:p + len(x)] += x[:max(0, N - p)]
    wr(os.path.join(L_AUD, 'STEM_DIALOGO.wav'), dia); wr(os.path.join(L_AUD, 'STEM_TRILHA.wav'), mus)
    wr(os.path.join(L_AUD, 'STEM_SFX.wav'), sfx)
    mix = dia * db(2) + mus + sfx
    wr(os.path.join(B, 'mix_raw.wav'), mix)
    # loudness: -16 LUFS integrado, pico -1.5 dBTP (loudnorm 2 passos)
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
    """composição em streaming: base 720p + overlays ativos (lidos sob demanda) -> NVENC; áudio = mix.wav."""
    out = os.path.join(B, 'EP300_ABERTURA_V0_PROXY.mp4'); tmp = os.path.join(B, '_preview_video.mp4')
    base = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', os.path.join(B, 'base_720.mp4'), '-f', 'rawvideo',
                             '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                            '-r', str(FPS), '-i', '-', '-c:v', 'h264_nvenc', '-preset', 'p5', '-cq', '21', '-pix_fmt',
                            'yuv420p', tmp], stdin=subprocess.PIPE)
    starts = {}
    for c in T['cues']: starts.setdefault(c['tl_in'], []).append(c)
    active = []   # (cue, proc)
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



# ------------------------------------------------------------------ manifesto (timeline legível, p/ reconstrução manual)
def tc(frames):
    s, f = divmod(int(frames), FPS); m, s = divmod(s, 60)
    return f'{m:02d}:{s:02d}:{f:02d}'

def do_manifest(T):
    cam = {'W': 'CAM_GERAL.mp4', 'G': 'MVI_9943-CAM_GUSTAVO.MP4', 'L': 'MVI_9943-CAM_LUCIAN.MP4', 'FREEZE': 'STILLS/FREEZE'}
    man = dict(
        producao='EP300 — Vídeo de Abertura', versao='V0 — Primeira montagem criativa', fps=FPS, resolucao_master='1920x1080',
        duracao=tc(T['total']), duracao_s=round(T['total'] / FPS, 2),
        fontes={k: os.path.basename(v) for k, v in SRC.items()}, offsets_na_CAM_GERAL_s=plan.OFFSETS,
        segmentos=[dict(id=s['id'], fonte_in_s=round(s['src_in'], 3), fonte_out_s=round(s['src_out'], 3),
                        tl_in=tc(s['tl_in']), tl_out=tc(s['tl_out'])) for s in T['segs']],
        cortes_editoriais=[dict(fonte_de=a, fonte_ate=b, motivo=m) for a, b, m in plan.CUTS],
        bleeps=[dict(fonte_de=a, fonte_ate=b, motivo=m) for a, b, m in plan.BLEEPS],
        planos=[dict(tl_in=tc(s['tl_in']), tl_out=tc(s['tl_out']), camera=cam[s['cam']],
                     fonte_s=(round(s['src_in'] - plan.OFFSETS[s['cam']], 3) if s['cam'] != 'FREEZE' else s['still']))
                for s in T['shots']],
        overlays=[dict(id=c['id'], arquivo=f"OVERLAYS/{c['id']}_{c['name']}.mov", tl_in=tc(c['tl_in']), tl_out=tc(c['tl_out']),
                       tela_cheia=bool(c.get('full')), intencao=c.get('why', '')) for c in T['cues']],
        sfx=[dict(tl=tc(fr(t)), sfx=k) for t, k in sfx_events(T)],
        audio=dict(dialogo='CAM_GERAL (mesa de som, mono duplicado) +2 dB', trilha_abertura='GotTheSwag Opener −10 dB',
                   trilha_fundo='A Groove Pool loop −31 dB (+10 dB no respiro "Gritem")', trilha_final='In The Spotlight 12s −9 dB',
                   loudness='mix normalizado −16 LUFS / −1.5 dBTP'),
    )
    p = os.path.join(B, 'timeline_v0.json')
    json.dump(man, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('manifest ok', p)


if __name__ == '__main__':
    only = None
    argv = sys.argv[1:]
    if '--only' in argv:
        k = argv.index('--only'); only = argv[k + 1].split(','); argv = argv[:k] + argv[k + 2:]
    args = [a for a in argv if not a.startswith('--')]
    steps = args or ['stills', 'overlays', 'base', 'audio', 'preview', 'xml']
    T = timeline()
    print(f"timeline: {T['total']} frames = {T['total'] / FPS:.2f}s; fala termina em {T['end'] / FPS:.2f}s")
    if 'stills' in steps: do_stills()
    if 'overlays' in steps: do_overlays(only)
    if 'base' in steps: do_base(T)
    if 'audio' in steps: do_audio(T)
    if 'preview' in steps: do_preview(T)
    if 'xml' in steps:
        import export_xml; export_xml.write(T)
    if 'manifest' in steps or not args: do_manifest(T)

