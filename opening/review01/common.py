"""Review 01 — eixo de tempo da timeline FINAL (frames @ 24000/1001) e colocação dos layers."""
import json, os, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
WORK = os.path.join(HERE, 'work')
REV = os.environ.get('REV', '02')                      # 02 = Review 02 (arquivada); 03 = Review 03
LAYERS = os.path.join(HERE, 'layers' if REV == '02' else f'layers_r{REV}')
OUTW = WORK if REV == '02' else os.path.join(WORK, f'r{REV}')   # saidas por revisao (chunks, mix, video); base/track_base seguem em WORK
os.makedirs(OUTW, exist_ok=True)
SHIFT = {} if REV == '02' else {'C03_02': -13}          # Review 03: antecipa a chave ON/OFF p/ cobrir o corte de camera (quadro 2584) sem 'pulinho'
FPSN, FPSD = 24000, 1001
FPS = FPSN / FPSD
SR = 48000


def fr(s):
    return int(round(s * FPS))


def sec(f):
    return f / FPS


BASE_FR = 7573                      # base 315.857 s
HOLDS = [(1032, 58, 'P_EVOL'),      # (frame da base onde o hold entra, nº de quadros, id) — 2.4 s / 3.0 s
         (2983, 72, 'GRITEM')]   # 124.4 s: silêncio digital do gate logo após 'concordam.'
BLEEP = (39.69, 40.09) if REV == '02' else (39.68, 40.72)   # R03: palavra 'fucking' INTEIRA, medida no espectro do áudio real (f-ricativa 39.70 -> 'ing' 40.70); R02 cobria só o 'f'
MUSIC_TRIM_DB = 0.0 if REV == '02' else -4.5   # R03: trilha ~4-5 dB abaixo da R02 (diálogo/SFX/ducking intactos)
ED = os.path.join(HERE, 'editable' if REV == '02' else f'editable_r{REV}')
INS_AT = 7395                       # frame da base (início do gap preto + blooper P&B do Premiere)
TITLE_FR = 86                       # 3.6 s de título visível; F01 entra aí (título se estende 0.4 s sob o F01)
F01_FR = 169                        # 7.061 s
INS_FR = TITLE_FR + F01_FR

# quadros exatos dos slots desativados do Premiere (timeline_dump)
SLOT_F = {'S01': 625, 'S02S03': 1414, 'S04': 2064, 'S05': 2466, 'S06': 3534, 'S07': 3922, 'S08': 4234,
          'S09': 4581, 'S10': 5012, 'S11': 6019}
PRE_ORDER = [('P01', 71), ('P02', 744), ('P03', 138), ('BLOOPER', 252)]
PRE_FR = sum(n for _, n in PRE_ORDER)


def pre_start(name):
    s = 0
    for k, n in PRE_ORDER:
        if k == name:
            return s
        s += n
    raise KeyError(name)


def F(base_frame):
    """quadro da base -> quadro final (inicia NO começo do hold quando coincide com o ponto do hold)."""
    return PRE_FR + base_frame + sum(n for hf, n, _ in HOLDS if hf < base_frame) + (INS_FR if INS_AT < base_frame else 0)


def cues():
    return json.load(open(os.path.join(HERE, 'cues_final.json'), encoding='utf-8'))


def placements():
    """lista de {id, start_f (final), file, sidecar, dur_f?}"""
    out = []
    ins_start = PRE_FR + INS_AT + sum(n for _, n, _ in HOLDS)  # início do bloco do insert
    for l in cues()['layers']:
        i = l['id']
        t = l['tl_start']
        if t == 'PRE':
            start = pre_start(i)
        elif t == 'INSERT':
            start = ins_start if i == 'C08_01' else ins_start + TITLE_FR
        elif i == 'C04_05_GRITEM':
            start = F(HOLDS[1][0])
        elif i in SLOT_F:
            start = F(SLOT_F[i])
        else:
            start = F(fr(t))
        start += SHIFT.get(i, 0)
        out.append(dict(id=i, start_f=start, file=os.path.join(LAYERS, i + '.mov'), side=os.path.join(LAYERS, i + '.json'), meta=l))
    return out


def total_frames():
    return PRE_FR + BASE_FR + sum(n for _, n, _ in HOLDS) + INS_FR


if __name__ == '__main__':
    for p in placements():
        print(f"{p['id']:16s} start_f={p['start_f']:6d} t={sec(p['start_f']):8.2f}s  exists={os.path.exists(p['file'])}")
    print('total', total_frames(), sec(total_frames()))
