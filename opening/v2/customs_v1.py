"""EP300 · V1 — cenas especiais novas (somam-se às do customs.py herdado da V0). Tempos relativos ao cue."""
import math, random
from PIL import Image, ImageDraw
import gfx, engine, extra, customs
from gfx import place, prog, ease_out, ease_in, ease_io, ease_mid, CREAM, ORANGE, INK, INK2, WHITE
from customs import _txt


def acho_wall(c, t, cue):
    """a partir de acho_at: a tela se enche de 'acho' ordenados (grade), abrindo espaço pro contador."""
    t0 = cue.get('acho_at', 6.6)
    if t < t0: return
    lt = t - t0
    out = cue['dur'] - .35
    s2, dy2, a2, _ = engine.leave('up', t - out)
    cols, rows = 6, 5
    for j in range(rows):
        for i in range(cols):
            k = j * cols + i
            at = k * 0.035
            if lt < at: continue
            x = 200 + i * 304 + (60 if j % 2 else 0); y = 150 + j * 195
            if 520 < x < 1400 and 300 < y < 760: continue
            s, dy, a, dr = engine.enter('pop', lt - at)
            pl = engine.build_img('pill', (('bg', WHITE), ('border', INK2), ('emoji', '🤔'), ('fg', INK2), ('shadow', INK2),
                                           ('size', 34), ('text', 'acho')))
            place(c, pl, x, y + dy2, s, gfx.ROTS[k % len(gfx.ROTS)], a * a2)


def bordao_prints(c, t, cue):
    """203× 'Fala aí': prints reais de episódios (pastas do podcast) empilhando como fotos-adesivo."""
    prints = [('v1/prints/EP282_GUSTAVO_LUCIAN.png', 'EP 282'), ('v1/prints/EP284_GUSTAVO_LUCIAN.png', 'EP 284'),
              ('v1/prints/EP286_GUSTAVO_LUCIAN.png', 'EP 286'), ('v1/prints/EP288_GUSTAVO_LUCIAN.png', 'EP 288')]
    out = cue['dur'] - .35
    s2, dy2, a2, _ = engine.leave('up', t - out)
    place(c, _txt('O BORDÃO DO GUSTAVO', 30, ORANGE, 'inter', 800, 200), 960, 80, alpha=prog(t, 0, .3) * a2)
    pos = [(520, 330, -6), (1400, 320, 5), (560, 720, 4), (1360, 730, -5)]
    for i, ((pth, cap), (x, y, r)) in enumerate(zip(prints, pos)):
        at = .15 + i * .32
        if t < at: continue
        s, dy, a, dr = engine.enter('slap', t - at)
        extra.polaroid(c, dict(img=pth, w=500, caption=cap, cap=30), t - at, -1, x, y + dy2, r + dr, s, a * a2)
    n = int(1 + 202 * ease_mid(prog(t, .3, 2.6)))
    cnt = _txt(f'{n}×', 230, ORANGE, tracking=-40)
    place(c, gfx.hard_shadow(cnt, (8, 10), (0, 0, 0), .3), 960, 520 + dy2, 1, -4, prog(t, .3, .2) * a2)
    if t > 2.9:
        lab = engine.build_img('label', (('lines', ('“Fala aí, analítica e analítico de plantão!”',)), ('size', 40)))
        s, dy, a, dr = engine.enter('pop', t - 2.9)
        place(c, lab, 960, 945 + dy2, s, 2, a * a2)


def mural_191(c, t, cue):
    """quem senta na mesa: prints reais de convidados + adesivos de convidados; número grande no centro."""
    out = cue['dur'] - .35
    s2, dy2, a2, _ = engine.leave('up', t - out)
    prints = [('v1/prints/EP282_CONVIDADA.png', (200, 250, -6)), ('v1/prints/EP283_CONVIDADO.png', (1720, 250, 5)),
              ('v1/prints/EP284_CONVIDADA.png', (220, 840, 4)), ('v1/prints/EP286_CONVIDADOS.png', (1700, 850, -4)),
              ('v1/prints/EP288_CONVIDADOS.png', (960, 930, 2))]
    for i, (pth, (x, y, r)) in enumerate(prints):
        at = .2 + i * .15
        if t < at: continue
        s, dy, a, dr = engine.enter('pop', t - at)
        extra.polaroid(c, dict(img=pth, w=330), t - at, -1, x, y + dy2, r, s * .95, a * a2)
    people = [('v1/stickers/PHILLIP/02_reacao_sorriso.png', 560, 200, -6), ('v1/stickers/MAFE/01_still.png', 1370, 190, 6),
              ('v1/stickers/BONEL/01_still.png', 540, 650, 5), ('v1/stickers/LAYLA/01_still.png', 1400, 660, -5),
              ('v1/stickers/VITORIA/01_still.png', 960, 150, 3)]
    for i, (pth, x, y, r) in enumerate(people):
        at = .8 + i * .14
        if t < at: continue
        s, dy, a, dr = engine.enter('pop', t - at)
        br = math.sin(2 * math.pi * max(0, t - at) / (2.6 + .3 * i))
        extra.stk(c, dict(path=pth, size=220), t - at, -1, x, y + dy2, r + 1.5 * br, s * (1 + .015 * (br + 1)), a * a2)
    seq = [(0.0, 191, 'PESSOAS', False), (cue.get('n2', 5.6), 348, 'PARTICIPAÇÕES', False), (cue.get('n3', 9.2), 140, 'EMPRESAS', True)]
    cur = [x for x in seq if t >= x[0]][-1]
    lt = t - cur[0]
    p = prog(lt, .05, .9)
    v = int(cur[1] * ease_mid(p))
    num = _txt(f'{v}+' if cur[3] else str(v), 250, WHITE, tracking=-40)
    s, dy, a, dr = engine.enter('slap', lt)
    place(c, gfx.hard_shadow(num, (9, 12), ORANGE, .95), 960, 440 + dy2, s, -3, a * a2)
    place(c, _txt(cur[2], 40, ORANGE, 'inter', 800, 250), 960, 610 + dy2, alpha=prog(lt, .2, .3) * a2)
    if cur[1] == 191:
        place(c, _txt('SENTARAM NESSA MESA', 28, (190, 190, 190), 'inter', 800, 200), 960, 670 + dy2, alpha=prog(t, .4, .3) * a2)


def ficha_v1(c, t, cue):
    """ficha de presença (V0) + fotos-adesivo reais de Phill, Mafê e Bonel quando cada nome é dito."""
    customs.ficha(c, t, cue)
    out = cue['dur'] - .35
    R = cue['rows']
    rows = [(R[0], 'v1/stickers/PHILLIP/03_reacao_risada.png', 'Phill', 1230, 300, -6),
            (R[1], 'v1/stickers/MAFE/03_reacao_marota.png', 'Mafê', 1600, 560, 6),
            (R[2], 'v1/stickers/BONEL/03_alt.png', 'Cláudio Bonel', 1250, 820, -4)]
    s2, dy2, a2, _ = engine.leave('up', t - out)
    for at, pth, name, x, y, r in rows:
        if t < at: continue
        s, dy, a, dr = engine.enter('slap', t - at)
        br = math.sin(2 * math.pi * max(0, t - at) / 2.9)
        extra.stk(c, dict(path=pth, size=320), t - at, -1, x, y + dy2, r + dr + 1.5 * br, s, a * a2)
        pl = engine.build_img('pill', (('bg', WHITE), ('border', INK2), ('fg', INK2), ('shadow', INK2), ('size', 28), ('text', name)))
        place(c, pl, x, y + 190 + dy2, s, -r / 2, a * a2)


def flags_110(c, t, cue):
    codes = ['BR', 'PT', 'US', 'AR', 'MX', 'ES', 'FR', 'IT', 'DE', 'JP', 'CO', 'CL', 'CA', 'AO', 'UK', 'IE']
    rnd = random.Random(110)
    for i, cd in enumerate(codes):
        at = i * .04
        if t < at: continue
        ang = 2 * math.pi * i / len(codes); R = 400 + 50 * (i % 2)
        x = 960 + R * 1.6 * math.cos(ang); y = 540 + R * .98 * math.sin(ang)
        s, dy, a, dr = engine.enter('burst', t - at)
        extra.flag(c, dict(code=cd, w=170), t - at, -1, x, y, rnd.choice(gfx.ROTS) + dr * .3, s, a)
    engine.draw_slap(c, dict(text='110 países', size=140, color=INK2, emoji='🌎', rot=-3), t - .2, -1, 960, 540, -3, 1, 1, auto=True)


def final_v1(c, t, cue):
    """'300 e contando' + realização / patrocínio / café oficial (só as marcas pedidas) + rostos com reação."""
    num = _txt(str(int(300 * ease_mid(prog(t, .1, 1.1)))), 300, ORANGE, tracking=-40)
    place(c, gfx.hard_shadow(num, (10, 13), (0, 0, 0), .15), 960, 230)
    place(c, _txt('e contando.', 54, WHITE, 'sora', 700), 960, 400, alpha=prog(t, .8, .4))
    for who, x, rot, per, at in (('lucian', 330, -7, 3.2, .5), ('gustavo', 1590, 7, 2.7, .65)):
        lt = t - at
        state = 'still'
        if 2.2 < lt < 2.42 or 5.0 < lt < 5.2: state = 'hover-transicao'
        elif 3.4 < lt < 4.4: state = 'hover-final'
        im = engine.build_img('face', (('size', 250), ('state', state), ('who', who)))
        s, dy, a, dr = engine.enter('pop', lt)
        br = math.sin(2 * math.pi * max(0, lt - 1.2) / per)
        place(c, im, x, 280, s * (1 + .015 * (br + 1)), rot + 1.5 * br, a)
    cols = [('REALIZAÇÃO', 'v1/pipoca/selo_metricas_boss.png', 300, 390),
            ('PATROCÍNIO', 'patrocinadores/purple-metrics.webp', 270, 780),
            ('PATROCÍNIO', 'patrocinadores/onfly.webp', 240, 1140),
            ('CAFÉ OFICIAL', 'patrocinadores/coffee-plusplus.webp', 240, 1530)]
    for i, (lab, pth, size, x) in enumerate(cols):
        at = 1.3 + i * .2
        s, dy, a, dr = engine.enter('pop', t - at)
        sw = math.sin(2 * math.pi * max(0, t - at) / (2.6 + .2 * i))
        im = engine.build_img('asset', (('path', pth), ('size', size)))
        place(c, im, x, 690, s * (1 + .02 * abs(sw)), 3 * sw, a)
        place(c, _txt(lab, 22, (170, 170, 170), 'inter', 800, 200), x, 545, alpha=prog(t, at, .3))
    pl = engine.build_img('pill', (('bg', ORANGE), ('border', INK2), ('emoji', '🍿'), ('shadow', INK2), ('size', 40),
                                   ('text', 'a sessão já vai começar')))
    s, dy, a, dr = engine.enter('slap', t - 2.8)
    place(c, pl, 960, 920, s, -2 + dr, a)
    fade = prog(t, cue['dur'] - .9, .9)
    if fade > 0:
        c.alpha_composite(Image.new('RGBA', (1920, 1080), (0, 0, 0, int(255 * fade))))


def cold_grain(c, t, cue):
    """textura de arquivo sobre o cold open (PB e grão vêm do build; aqui scanlines + fade de entrada)."""
    d = ImageDraw.Draw(c)
    for y in range(0, 1080, 4):
        d.line((0, y, 1920, y), fill=(0, 0, 0, 26))
    fi = 1 - prog(t, 0, .45)
    if fi > 0: c.alpha_composite(Image.new('RGBA', (1920, 1080), (0, 0, 0, int(255 * fi))))


def dim(c, t, cue):
    """escurece a imagem de baixo (respiro 'Gritem') para a placa de cinema ganhar a tela."""
    a = min(1, prog(t, cue.get('dim_at', .3), .25)) * (1 - prog(t, cue['dur'] - .35, .3))
    if a > 0: c.alpha_composite(Image.new('RGBA', (1920, 1080), (18, 18, 19, int(cue.get('dim_alpha', 170) * a))))


customs.FUNCS.update(acho_wall=acho_wall, bordao_prints=bordao_prints, mural_191=mural_191, ficha_v1=ficha_v1,
                     flags_110=flags_110, final_v1=final_v1, cold_grain=cold_grain, dim=dim)
