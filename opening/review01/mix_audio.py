"""Review 01 — mixagem: diálogo da BASE (intocado, só cortes nos holds + censura 'fucking') + trilhas V2 + SFX V2 (sidecars) com ducking."""
import numpy as np, subprocess, json, os, glob, sys, math, re
from scipy.io import wavfile
from common import *
sys.path.insert(0, os.path.join(ROOT, 'v2'))
import sfx_v2

D = glob.glob('I:/Drives compartilhados/Educa*/Marketing*/01_CANAIS_ATIVOS/02_PODCAST/2026/300_*/01_VIDEO DE ABERTURA/00_ASSETS E INSERTS')[0]
MA = D + '/V2_GERADOS/AUDIO'
db = lambda x: 10 ** (x / 20)
REL = -5.4   # base (−19.5 LUFS) vs CAM_GERAL V2 (−16.1 +2 dB): mantém o balanço V2 música/SFX × voz


def rd(path, ss=None, t=None, af=None):
    cmd = ['ffmpeg', '-v', 'error']
    if ss is not None: cmd += ['-ss', str(ss)]
    if t is not None: cmd += ['-t', str(t)]
    cmd += ['-i', path]
    if af: cmd += ['-af', af]
    cmd += ['-f', 'f32le', '-ac', '2', '-ar', str(SR), '-']
    r = subprocess.run(cmd, capture_output=True)
    return np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy()


def wr(path, x):
    wavfile.write(path, SR, x.astype(np.float32))


def fade(x, fi, fo):
    x = x.copy(); n = len(x)
    if fi: k = min(n, int(fi * SR)); x[:k] *= np.linspace(0, 1, k)[:, None]
    if fo: k = min(n, int(fo * SR)); x[n - k:] *= np.linspace(1, 0, k)[:, None]
    return x


SFXLIB = {'MA_SergeySopko_MouseClick_1.wav': (-14, None), 'MA_Amenteramco_Whoosh_Pass-By_1.wav': (-21, None),
          '01 Impact.wav': (-24, (0, 1.6)), 'Turn the TV Off and On 1.wav': (-17, None),
          'MA_AppleHillStudios_WrongAnswer_1.wav': (-15, None), 'MA_SoundsByGFXSounds_DingNotification_1.wav': (-21, (0, 1.2)),
          '01 Clock Ticking.wav': (-21, (0, 3.0)), 'MA_AleXZavesa_WooshAndBoom_1.wav': (-21, None)}
SYN_GAIN = {'thump': -20, 'pop': -19, 'party': -17, 'tickup': -20, 'rise': -23}


def sfx_sample(name):
    base = os.path.basename(name)
    if base in SFXLIB:
        g, rng = SFXLIB[base]
        x = rd(os.path.join(MA, base))
        if rng: x = fade(x[int(rng[0] * SR):int((rng[0] + rng[1]) * SR)], 0, .3)
        x = x * db(g)
        return np.stack([sfx_v2._lp_fast(x[:, 0], 7000), sfx_v2._lp_fast(x[:, 1], 7000)], 1).astype(np.float32) * db(REL)
    if base.startswith('SFX_LEADER_BEEP'):
        return rd(os.path.join(MA, base)) * db(REL)
    m = re.match(r'SFX_SYN_(.+)\.wav', base)
    key = m.group(1)
    return sfx_v2.make(key) * db(SYN_GAIN[re.match(r'[a-z]+', key).group(0)] + REL)


def put(buf, t_s, x):
    p = max(0, int(round(t_s * SR)))
    n = max(0, min(len(x), len(buf) - p))
    buf[p:p + n] += x[:n]


def main():
    total_s = sec(total_frames()) + 1.0
    N = int(total_s * SR)
    dia = np.zeros((N, 2), np.float32); mus = np.zeros((N, 2), np.float32); sfx = np.zeros((N, 2), np.float32)

    # --- diálogo: blooper (b0) + base
    b0 = os.path.join(ROOT, 'work', 'v2', 'b0.mp4')
    x = rd(b0, 0.0, 10.5, 'highpass=f=80,loudnorm=I=-20:TP=-3')
    put(dia, sec(pre_start('BLOOPER')), fade(x, .05, .25))
    base = rd(os.environ.get('BASE_AUDIO') or os.path.join(WORK, 'base_720.mp4'))   # BASE_AUDIO = audio original do export 4K (preferido)
    cuts = [0] + [h[0] for h in HOLDS] + [INS_AT, BASE_FR + 5]
    shifts = [PRE_FR + cuts[0], PRE_FR + cuts[1] + HOLDS[0][1], PRE_FR + cuts[2] + HOLDS[0][1] + HOLDS[1][1], PRE_FR + cuts[3] + HOLDS[0][1] + HOLDS[1][1] + INS_FR]
    for i in range(4):
        a, b = sec(cuts[i]), sec(cuts[i + 1])
        seg = base[int(a * SR):int(b * SR)]
        seg = fade(seg, .01 if i else 0, .01 if i < 3 else 0)
        put(dia, sec(shifts[i]) + 0.0, seg)
    # censura divertida (H7): diálogo mudo na palavra + bleep 1 kHz
    b_a = sec(shifts[0]) + BLEEP[0]; b_b = sec(shifts[0]) + BLEEP[1]
    i0, i1 = int(b_a * SR), int(b_b * SR)
    env = np.ones(len(dia), np.float32); env[i0:i1] = 0
    k = int(.008 * SR); env[i0 - k:i0] = np.linspace(1, 0, k); env[i1:i1 + k] = np.linspace(0, 1, k)
    dia *= env[:, None]
    n = i1 - i0; tt = np.arange(n) / SR
    tone = fade(np.stack([.18 * np.sin(2 * np.pi * 1000 * tt)] * 2, 1).astype(np.float32), .008, .008) * db(REL + 2)
    put(sfx, b_a, tone)

    # --- música
    ins_s = sec(PRE_FR + INS_AT + sum(h[1] for h in HOLDS))
    base_s = sec(PRE_FR)
    av = rd(os.path.join(MA, 'MA_LEXMusic_BeatTheOdds_30s.wav'))
    a0 = sec(pre_start('P02')); a1 = sec(pre_start('BLOOPER'))   # aviso -> sai sob o fim do P03
    L = int((a1 - a0) * SR)
    av = np.concatenate([fade(av, 0, .5), fade(av, .5, 0)] * (1 + L // (2 * len(av))))[:L]
    e = np.ones(L, np.float32); k0 = int((a1 - a0 - 1.6) * SR); e[k0:] = np.linspace(1, db(-30), L - k0)
    put(mus, a0, fade(av, .4, .2) * e[:, None] * db(-13 + REL))
    bed = rd(os.path.join(MA, 'Trigubovich_A_Groove_Pool_loop_long.wav'))
    b0s, b1s = base_s - 0.3, ins_s - 0.2
    L = int((b1s - b0s) * SR)
    bedl = fade(np.concatenate([bed] * (int(math.ceil(L / len(bed))) + 1))[:L], 2.5, 1.4) * db(-31 + REL)
    e2 = np.ones(L, np.float32); ramp = int(.15 * SR)
    g0 = int((sec(PRE_FR + HOLDS[0][0] + HOLDS[0][1] + 0) - b0s) * SR)
    g0 = int((sec(PRE_FR + HOLDS[1][0] + HOLDS[0][1]) - b0s) * SR); g1 = g0 + int(sec(HOLDS[1][1]) * SR)
    e2[g0 - ramp:g0] = np.linspace(1, db(10), ramp); e2[g0:g1] = db(10); e2[g1:g1 + ramp] = np.linspace(db(10), 1, ramp)
    put(mus, b0s, bedl * e2[:, None])
    fin = rd(os.path.join(MA, 'MA_Puremusic_InTheSpotlight_12s.wav'))[:int(sec(INS_FR) * SR)]
    put(mus, ins_s, fade(fin, 1.2, 1.2) * db(-9 + REL))

    mus *= db(MUSIC_TRIM_DB)   # R03: -4.5 dB na trilha (inclui o +10 dB do GRITEM, relativo)

    # --- SFX dos sidecars
    cache = {}; EVENTS = []
    for p in placements():
        if not os.path.exists(p['side']): continue
        sc = json.load(open(p['side'], encoding='utf-8'))
        t0 = sec(p['start_f'])
        for ev in sc.get('sfx', []):
            f = ev['file']
            if f not in cache: cache[f] = sfx_sample(f)
            put(sfx, t0 + ev['t'], cache[f] * (db(ev['gain_db']) if 'gain_db' in ev else 1))
            EVENTS.append(dict(layer=p['id'], file=f, t=round(t0 + ev['t'], 3)))

    # --- ducking (VOZ > SFX), como na V2
    mono = np.abs(dia).mean(1); h = int(.02 * SR); m = len(mono) // h * h
    rms = 20 * np.log10(np.sqrt((mono[:m].reshape(-1, h) ** 2).mean(1)) + 1e-6)
    pres = np.clip((rms + 50) / 8, 0, 1); sm = np.zeros_like(pres); v = 0.0
    for i, q in enumerate(pres):
        v = v + (q - v) * (0.5 if q > v else 0.065); sm[i] = v
    duck = np.interp(np.arange(N) / SR, (np.arange(len(sm)) + .5) * .02, db(-12 * sm)).astype(np.float32)
    bleep_zone = slice(i0 - k, i1 + k)
    sfx_d = sfx * duck[:, None]; sfx_d[bleep_zone] = sfx[bleep_zone]
    mix = dia + mus + sfx_d
    pk = float(np.abs(mix).max())
    if pk > .95: mix *= .95 / pk
    AD = os.path.join(ED, 'media', 'audio', 'sfx'); os.makedirs(AD, exist_ok=True)
    for f, x in cache.items(): wr(os.path.join(AD, os.path.splitext(os.path.basename(f))[0].replace(' ', '_') + '.wav'), x)
    wr(os.path.join(AD, 'BLEEP_fucking.wav' if REV == '02' else f'BLEEP_fucking_R{REV}.wav'), tone)
    EVENTS.append(dict(layer='C06_02_BLEEP', file='BLEEP_fucking.wav' if REV == '02' else f'BLEEP_fucking_R{REV}.wav', t=round(b_a, 3)))
    json.dump(EVENTS, open(os.path.join(OUTW, 'sfx_events.json'), 'w'), indent=1)
    out = os.path.join(OUTW, 'mix.wav')
    wr(out, mix)
    wr(os.path.join(OUTW, 'stem_dia.wav'), dia); wr(os.path.join(OUTW, 'stem_mus.wav'), mus); wr(os.path.join(OUTW, 'stem_sfx.wav'), sfx_d)
    print('mix ok', out, 'peak', pk, 'sfx events', sum(len(json.load(open(p['side'], encoding='utf-8')).get('sfx', [])) for p in placements() if os.path.exists(p['side'])))


if __name__ == '__main__':
    main()
