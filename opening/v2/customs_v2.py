"""EP300 · V2 — cenas especiais novas (somam-se às de customs.py / customs_v1.py). Tempos relativos ao cue."""
import math, os, importlib.util
from PIL import Image, ImageDraw
import numpy as np
import gfx, engine, extra, extra_v2, customs
import customs_v1  # noqa: F401  (registra as cenas da V1)
from gfx import place, prog, ease_out, ease_in, ease_io, ease_mid, CREAM, ORANGE, INK, INK2, WHITE
from customs import _txt

ST2 = 'v2/stickers/'


def acho_wall_v2(c, t, cue):
    """'acho' como TEXTURA: só nas laterais (fora da coluna DADOS/11.526/VEZES), dentro da safe area, sem tocar topo/base."""
    t0 = cue.get('acho_at', 6.6)
    if t < t0: return
    lt = t - t0
    s2, dy2, a2, _ = engine.leave('up', t - (cue['dur'] - .35))
    xs_l, xs_r = (240, 470), (1450, 1680)
    rows = (420, 620, 820)
    k = 0
    for j, y in enumerate(rows):
        for i, x in enumerate(xs_l + xs_r):
            at = k * 0.06; k += 1
            if lt < at: continue
            s, dy, a, dr = engine.enter('pop', lt - at)
            em = '🤔' if (i + j) % 3 else '😅'
            pl = engine.build_img('pill', (('bg', WHITE), ('border', INK2), ('emoji', em), ('fg', INK2), ('shadow', INK2),
                                           ('size', 30), ('text', 'acho')))
            place(c, pl, x + (30 if j % 2 else 0), y + dy2, s, gfx.ROTS[(i * 3 + j) % len(gfx.ROTS)], a * a2)


def evolucao(c, t, cue):
    """'a pergunta foi mudando' — 6 épocas do programa em frames reais do acervo, do EP 1 (2021) até hoje."""
    out = cue['dur'] - .35
    s2, dy2, a2, _ = engine.leave('up', t - out) if cue.get('out_fade', False) else (1, 0, 1, 0)
    place(c, _txt('A PERGUNTA FOI MUDANDO', 30, ORANGE, 'inter', 800, 200), 960, 105, alpha=prog(t, 0, .3) * a2)
    items = [('EP001_2021_DIGITAL_ANALYTICS_EM_2021', '2021', 'EP 1'), ('EP073_2022_BIGQUERY', '2022', 'EP 73'),
             ('EP100_2023_PLATEIA', '2023', 'EP 100 · ao vivo'), ('EP153_2024_POWERBI_LOOKER', '2024', 'EP 153'),
             ('EP210_2025_MERIDIAN', '2025', 'EP 210'), ('EP300_2026_HOJE', '2026', 'HOJE · EP 300')]
    xs = [262, 533, 804, 1075, 1346, 1617]
    for i, ((img, yr, cap), x) in enumerate(zip(items, xs)):
        at = .35 + i * .55
        if t < at: continue
        y = 540 + (-95 if i % 2 == 0 else 95)
        s, dy, a, dr = engine.enter('slap', t - at)
        big = 1.18 if i == len(items) - 1 else 1.0
        extra.polaroid(c, dict(img=f'v2/hist/{img}.png', w=290, caption=cap, cap=22), t - at, -1, x, y + dy, [-5, 4, -3, 5, -4, 3][i] + dr,
                       s * big, a * a2)
        place(c, _txt(yr, 48, ORANGE if i < len(items) - 1 else INK2, tracking=-20), x, y - 170 * big + dy, 1, 0, a * a2)


def _people(c, t, cue, specs, out_fade=True):
    out = cue['dur'] - .35
    s2, dy2, a2, _ = engine.leave('up', t - out) if out_fade else (1, 0, 1, 0)
    for i, sp in enumerate(specs):
        at = sp['at']
        if t < at: continue
        s, dy, a, dr = engine.enter('pop', t - at)
        br = math.sin(2 * math.pi * max(0, t - at) / (2.6 + .3 * i))
        path = sp['states'][0][1]
        for t0, p in sp['states']:
            if t - at >= t0: path = p
        extra.stk(c, dict(path=path, size=sp['size']), t - at, -1, sp['x'], sp['y'] + dy2, sp['rot'] + 1.5 * br + dr,
                  s * (1 + .015 * (br + 1)), a * a2)
        if sp.get('name'):
            pl = engine.build_img('pill', (('bg', WHITE), ('border', INK2), ('fg', INK2), ('shadow', INK2), ('size', 26), ('text', sp['name'])))
            place(c, pl, sp['x'], sp['y'] + sp['size'] * .5 + 20 + dy2, s, -sp['rot'] / 2, a * a2)


def mural_v2(c, t, cue):
    """quem senta na mesa: 4 convidados históricos (adesivo) + 2 frames reais; número no centro; reações trocam a cada número."""
    out = cue['dur'] - .35
    s2, dy2, a2, _ = engine.leave('up', t - out)
    n2, n3 = cue.get('n2', 6.6), cue.get('n3', 9.3)
    prints = [('v2/hist/EP187_2024_MMM.png', 'EP 187 · convidado remoto', (620, 900, -3)),
              ('v1/prints/EP286_CONVIDADOS.png', 'EP 286', (1300, 900, 3))]
    for i, (pth, cap, (x, y, r)) in enumerate(prints):
        at = .3 + i * .2
        if t < at: continue
        s, dy, a, dr = engine.enter('pop', t - at)
        extra.polaroid(c, dict(img=pth, w=330, caption=cap, cap=20), t - at, -1, x, y + dy2, r, s * .95, a * a2)
    specs = [
        dict(at=.7, x=300, y=300, size=250, rot=-6, name='Phill', states=[(0, ST2 + 'PHILLIP/02_sorriso.png'), (n2 - .7, ST2 + 'PHILLIP/03_surpresa.png'), (n3 - .7, ST2 + 'PHILLIP/04_pensando.png')]),
        dict(at=.85, x=1620, y=300, size=250, rot=6, name='Mafê', states=[(0, ST2 + 'MAFE/01_sorriso.png'), (n2 - .85, ST2 + 'MAFE/03_lateral.png')]),
        dict(at=1.0, x=300, y=700, size=250, rot=5, name='Cláudio Bonel', states=[(0, ST2 + 'BONEL/01_sorriso.png'), (n2 - 1.0, ST2 + 'BONEL/02_surpresa.png'), (n3 - 1.0, ST2 + 'BONEL/03_pensando.png')]),
        dict(at=1.15, x=1620, y=700, size=250, rot=-5, name='Layla', states=[(0, ST2 + 'LAYLA/01_sorriso.png'), (n2 - 1.15, ST2 + 'LAYLA/02_surpresa.png'), (n3 - 1.15, ST2 + 'LAYLA/03_pensando.png')]),
    ]
    _people(c, t, cue, specs)
    seq = [(0.0, 191, 'PESSOAS', False), (n2, 348, 'PARTICIPAÇÕES', False), (n3, 140, 'EMPRESAS', True)]
    cur = [x for x in seq if t >= x[0]][-1]
    lt = t - cur[0]
    v = int(cur[1] * ease_mid(prog(lt, .05, .9)))
    num = _txt(f'{v}+' if cur[3] else str(v), 250, WHITE, tracking=-40)
    s, dy, a, dr = engine.enter('slap', lt)
    place(c, gfx.hard_shadow(num, (9, 12), ORANGE, .95), 960, 440 + dy2, s, -3, a * a2)
    place(c, _txt(cur[2], 40, ORANGE, 'inter', 800, 250), 960, 610 + dy2, alpha=prog(lt, .2, .3) * a2)
    if cur[1] == 191:
        place(c, _txt('SENTARAM NESSA MESA', 28, (190, 190, 190), 'inter', 800, 200), 960, 670 + dy2, alpha=prog(t, .4, .3) * a2)


def ficha_v2(c, t, cue):
    """ficha de presença (V0) + adesivos novos de Phill, Mafê e Bonel; frame real do EP 1 quando Mafê 'foi a convidada do EP 1'."""
    customs.ficha(c, t, cue)
    out = cue['dur'] - .35
    R = cue['rows']
    rows = [(R[0], ST2 + 'PHILLIP/02_sorriso.png', 'Phill', 1230, 330, -6),
            (R[1], ST2 + 'MAFE/01_sorriso.png', 'Mafê', 1600, 610, 6),
            (R[2], ST2 + 'BONEL/00_sorriso_grande.png', 'Cláudio Bonel', 1250, 800, -4)]
    s2, dy2, a2, _ = engine.leave('up', t - out)
    for at, pth, name, x, y, r in rows:
        if t < at: continue
        s, dy, a, dr = engine.enter('slap', t - at)
        br = math.sin(2 * math.pi * max(0, t - at) / 2.9)
        extra.stk(c, dict(path=pth, size=290), t - at, -1, x, y + dy2, r + dr + 1.5 * br, s, a * a2)
        pl = engine.build_img('pill', (('bg', WHITE), ('border', INK2), ('fg', INK2), ('shadow', INK2), ('size', 28), ('text', name)))
        place(c, pl, x, y + 185 + dy2, s, -r / 2, a * a2)
    at = cue['extras'][0]
    if t >= at:
        s, dy, a, dr = engine.enter('slap', t - at)
        extra.polaroid(c, dict(img='v2/hist/EP001_2021_DIGITAL_ANALYTICS_EM_2021.png', w=300, caption='EP 1 · 2021', cap=22), t - at, -1,
                       1620, 260 + dy2, 4 + dr, s, a * a2)


def flags_v2(c, t, cue):
    codes = ['BR', 'PT', 'US', 'AR', 'MX', 'ES', 'FR', 'IT', 'DE', 'JP', 'CO', 'CL', 'CA', 'AO', 'UK', 'IE']
    for i, cd in enumerate(codes):
        at = i * .04
        if t < at: continue
        ang = 2 * math.pi * i / len(codes) - math.pi / 2
        x = 960 + 690 * math.cos(ang); y = 540 + 340 * math.sin(ang)
        s, dy, a, dr = engine.enter('burst', t - at)
        extra_v2.flag_sq(c, dict(code=cd, size=150), t - at, -1, x, y, gfx.ROTS[i % len(gfx.ROTS)] + dr * .3, s, a)
    engine.draw_slap(c, dict(text='110 países', size=140, color=INK2, emoji='🌎', rot=-3), t - .2, -1, 960, 540, -3, 1, 1, auto=True)


# ------------------------------------------------------------------ final → looping
LOOP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ep300-cinema-loop'))
_LB = None
_ST = None


def _loop():
    global _LB, _ST
    if _LB is None:
        spec = importlib.util.spec_from_file_location('loop_build', os.path.join(LOOP_DIR, 'build.py'))
        _LB = importlib.util.module_from_spec(spec); spec.loader.exec_module(_LB)
        _ST = _LB.build_static()
    return _LB, _ST


def loop_layers(tl, cards=1.0, sponsors=1.0, logo=1.0, num_fill='ink', ep=1.0, num_scale=1.0, num_alpha=1.0):
    """recompõe o quadro do LOOP no instante tl (s do loop) com camadas controláveis — com tudo em 1 é IDÊNTICO ao quadro do loop."""
    LB, st = _loop()
    S = LB.S; DUR = LB.DUR
    drift = int(round((tl / DUR) * S['background']['dot_drift_px_per_loop'])) % 20
    cv = Image.fromarray(np.ascontiguousarray(st['bg'][drift:drift + LB.H, drift:drift + LB.W]), 'RGB').convert('RGBA')
    if cards > 0.003:
        layer = Image.new('RGBA', cv.size, (0, 0, 0, 0))
        cb = S['background']
        breath = 1 + cb['collage_breath'] * math.sin(2 * math.pi * tl / cb['collage_breath_period'])
        for i, cd in enumerate(S['collage']['cards']):
            base_i, pm, hi, hipm = st['cards'][i]
            ph = 2 * math.pi * (tl / cd['period'] + cd['phase']); amp = 6 + 16 * cd['depth']
            dx, dy = amp * math.cos(ph), amp * 0.6 * math.sin(ph)
            cx = 960 + (cd['cx'] - 960) * breath + dx; cy = 540 + (cd['cy'] - 540) * breath + dy
            rot = cd['rot'] + 0.8 * math.sin(ph + 1.0); sc = breath; sp = 0
            for spl in S['collage']['spotlights']:
                if spl['card'] == i:
                    sp = LB.track(spl['keys'], tl); sc *= 1 + spl['lift_scale'] * sp
            LB.place(layer, base_i, cx, cy, sc, rot, 1.0, pm)
            if hi is not None and cd.get('alt_keys'):
                sp = max(LB.track(cd['alt_keys'], tl), LB.track(cd['alt_keys'], tl + DUR))
            if hi is not None and sp > 0: LB.place(layer, hi, cx, cy, sc, rot, sp, hipm)
        layer.alpha_composite(st['scrim'])
        if cards < .999: layer.putalpha(layer.getchannel('A').point(lambda v: int(v * cards)))
        cv.alpha_composite(layer)
    T = S['title']; n = T['numero']
    if ep > .003:
        e = st['ep'] if ep >= .999 else _fade(st['ep'], ep)
        LB.place(cv, e, T['episodio']['cx'], T['episodio']['cy'])
    sway = n['rot'] + n['sway_deg'] * math.sin(2 * math.pi * tl / n['sway_period'])
    nb = 1 + n['breath'] * math.sin(2 * math.pi * tl / n['breath_period'])
    if num_alpha > .003:
        spr = st['num']
        if num_fill == 'orange': spr = _num_orange()
        elif isinstance(num_fill, float):   # mistura orange→ink
            spr = Image.blend(_num_orange(), st['num'], num_fill)
        LB.place(cv, spr, n['cx'], n['cy'], nb * num_scale, sway, num_alpha)
    if logo > .003:
        L = T['logo']; LB.place(cv, st['logo'], L['cx'], L['cy'], 1.0, L['rot'], logo)
    if sponsors > .003:
        sp_im = st['sponsors']; layer = Image.new('RGBA', cv.size, (0, 0, 0, 0))
        layer.alpha_composite(sp_im, (960 - sp_im.width // 2, S['sponsors']['y'] - 34))
        if sponsors < .999: layer.putalpha(layer.getchannel('A').point(lambda v: int(v * sponsors)))
        cv.alpha_composite(layer)
    return cv


_ORANGE_NUM = None
def _num_orange():
    global _ORANGE_NUM
    if _ORANGE_NUM is None:
        LB, st = _loop(); T = LB.S['title']['numero']
        _ORANGE_NUM = LB.shadow(LB.sticker_text(T['text'], T['size'], LB.ORANGE, 20), 16, 20, .6)
    return _ORANGE_NUM


def _fade(im, a):
    im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * a))); return im


def final_v2(c, t, cue):
    """300 conta → estoura → 'vocês estão aqui' → Gustavo e Lucian comemoram → o 300 vira o lockup do LOOP (mosaico, logo, patrocinadores).
    Tempo do loop tl = 120 − (dur − t): os últimos 1,5 s são os quadros 118,5–120 s do LOOP (o MP4 do loop recomeça em 0 sem corte)."""
    LB, st = _loop(); DUR = LB.DUR; dur = cue['dur']
    tl = DUR - (dur - t)
    p_fill = ease_io(prog(t, 4.6, 1.2))          # laranja → tinta
    cards = ease_io(prog(t, 4.8, 2.2))
    sponsors = ease_io(prog(t, 6.2, 1.0))
    logo = ease_out(prog(t, 5.6, .7))
    ep = ease_out(prog(t, 1.3, .35))
    # número: conta até 300, estoura em 1.3
    count = ease_mid(prog(t, .1, 1.1))
    n = int(300 * count)
    sc_pop = 1 + .10 * (1 - ease_out(prog(t, 1.3, .5))) if t >= 1.3 else 1
    if t < 1.3:
        T = LB.S['title']['numero']
        im = LB.shadow(LB.sticker_text(str(n), T['size'], LB.ORANGE, 20), 16, 20, .6)
        base = loop_layers(tl, cards=0, sponsors=0, logo=0, ep=0, num_alpha=0)
        LB.place(base, im, T['cx'], T['cy'], 1.0, T['rot'], min(1, t * 8))
    else:
        fill = p_fill if p_fill > 0 else 'orange'
        if p_fill >= .999: fill = 'ink'
        elif p_fill > 0: fill = float(p_fill)
        base = loop_layers(tl, cards=cards, sponsors=sponsors, logo=logo, num_fill=fill, ep=ep, num_scale=sc_pop)
    c.alpha_composite(base)
    # celebração (confete + Gustavo e Lucian reagindo + 'vocês estão aqui'), saindo antes da fusão terminar
    exit_ = 1 - ease_in(prog(t, 4.6, .9))
    if t >= 1.3 and exit_ > 0.003:
        el = dict(k='confetti', at=1.3, x=960, y=470, n=60, seed=11, anim='none')
        extra.confetti(c, el, t - 1.3, -1, 960, 470, 0, 1, exit_)
        for who, x, rot, per, at in (('lucian', 300, -7, 3.2, 1.6), ('gustavo', 1620, 7, 2.7, 1.75)):
            lt = t - at
            if lt < 0: continue
            state = 'still'
            if 1.0 < lt < 1.2 or 2.6 < lt < 2.8: state = 'hover-transicao'
            elif 1.2 <= lt < 2.4: state = 'hover-final'
            im = engine.build_img('face', (('size', 300), ('state', state), ('who', who)))
            s, dy, a, dr = engine.enter('pop', lt)
            br = math.sin(2 * math.pi * max(0, lt - 1.2) / per)
            xx = x + (-180 if who == 'lucian' else 180) * (1 - exit_)   # saem para os lados quando a fusão começa
            place(c, im, xx, 640, s * (1 + .015 * (br + 1)), rot + 1.5 * br + dr, a * exit_)
        if t > 2.4:
            s, dy, a, dr = engine.enter('slap', t - 2.4)
            pl = engine.build_img('pill', (('bg', WHITE), ('border', INK2), ('emoji', '📍'), ('fg', INK2), ('shadow', INK2), ('size', 44),
                                           ('text', 'vocês estão aqui')))
            place(c, pl, 960, 800, s, -2 + dr, a * exit_)
        if 3.4 < t:
            s, dy, a, dr = engine.enter('pop', t - 3.4)
            pl = engine.build_img('pill', (('bg', ORANGE), ('border', INK2), ('shadow', INK2), ('size', 40), ('text', 'e contando.')))
            place(c, pl, 960, 900, s, 2 + dr, a * exit_)


customs.FUNCS.update(acho_wall_v2=acho_wall_v2, evolucao=evolucao, mural_v2=mural_v2, ficha_v2=ficha_v2, flags_v2=flags_v2, final_v2=final_v2)
