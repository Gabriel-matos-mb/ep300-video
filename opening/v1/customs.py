"""EP300 · V1 (derivado da V0) — cenas especiais (desenhadas por função). Tempos relativos ao início do cue."""
import math, random
from PIL import Image, ImageDraw
import gfx, engine
from gfx import place, prog, ease_out, ease_in, ease_io, ease_mid, pop_soft, CREAM, ORANGE, INK, INK2, WHITE

FREEZES = {}   # preenchido pelo build: 'freeze:G:508.60' -> caminho PNG 1920x1080


def _txt(s, size, color=INK2, kind='sora', weight=800, tracking=0):
    return engine.build_img('text', tuple(sorted(dict(text=s, size=size, color=color, font=kind, weight=weight,
                                                      tracking=tracking).items())))


def leader(c, t, cue):
    """contagem de película (pré-sessão) na gramática EP300."""
    d = ImageDraw.Draw(c)
    ink = (18, 18, 19, 40)
    d.line((0, 540, 1920, 540), fill=ink, width=3); d.line((960, 0, 960, 1080), fill=ink, width=3)
    for r in (300, 380):
        d.ellipse((960 - r, 540 - r, 960 + r, 540 + r), outline=(18, 18, 19, 70), width=6)
    n = 3 - int(t / 0.95)
    if n >= 1:
        f = (t % 0.95) / 0.95
        wedge = Image.new('RGBA', (760, 760), (0, 0, 0, 0))
        ImageDraw.Draw(wedge).pieslice((0, 0, 759, 759), -90, -90 + 360 * f, fill=ORANGE + (255,))
        c.alpha_composite(wedge, (960 - 380, 540 - 380))
        d.ellipse((960 - 300, 540 - 300, 960 + 300, 540 + 300), fill=CREAM + (255,), outline=INK2, width=6)
        num = _txt(str(n), 430, INK2, tracking=-40)
        s = 1 + 0.12 * (1 - ease_out(min(1, f / .25)))
        place(c, gfx.hard_shadow(num, (13, 17), (0, 0, 0), .15), 960, 548, s)
    else:
        a = 1 - prog(t, 2.85, .05)
        c.alpha_composite(Image.new('RGBA', (1920, 1080), (255, 255, 255, int(255 * a))))
    ov = _txt('PRÉ-SESSÃO', 30, ORANGE, 'inter', 800, 200)
    place(c, ov, 960, 90)
    ft = _txt('ANALYTICS TALKS · EP 300', 26, (120, 120, 120), 'inter', 700, 150)
    place(c, ft, 960, 1000)


def placar(c, t, cue):
    """dados × acho: 11.526 × 11.032 → 494 de diferença → 'aumentar essa distância'."""
    place(c, _txt('A PALAVRA MAIS DITA EM 300 EPISÓDIOS', 28, ORANGE, 'inter', 800, 200), 960, 110,
          alpha=prog(t, 0, .4))
    spread = 170 * ease_io(prog(t, 4.0, 1.2))
    for i, (word, n, emo, col) in enumerate((('dados', 11526, '🤓', ORANGE), ('acho', 11032, '🤔', INK2))):
        x = (560 - spread) if i == 0 else (1360 + spread)
        lt = t - i * .25
        if lt < 0: continue
        engine.draw_slap(c, dict(text=word, size=120, color=col, emoji=emo, rot=-3 if i == 0 else 4), lt, -1, x, 330,
                         -3 if i == 0 else 4, 1, 1, auto=True)
        p = prog(lt, .3, 1.1)
        num = _txt(gfx.counter_text(n * ease_mid(p)), 130, INK2, tracking=-40)
        place(c, gfx.hard_shadow(num, (4, 5), (0, 0, 0), .15), x, 540, 1, 0, min(1, p * 4))
        place(c, _txt('VEZES', 26, (110, 110, 110), 'inter', 800, 200), x, 640, alpha=min(1, p * 4))
    # 494
    if t > 1.2:
        lt = t - 1.2
        s, dy, a, dr = engine.enter('stamp', lt)
        st = engine.build_img('stamp', (('color', ORANGE), ('fill', ORANGE), ('lines', ('494',)), ('size', 110)))
        place(c, st, 960, 835, s, -6 + dr, a)
        place(c, _txt('de diferença', 34, INK2, 'inter', 700), 960, 965, alpha=prog(lt, .3, .3))
    if t > 4.3:
        pl = engine.build_img('pill', (('border', INK2), ('emoji', '↔️'), ('shadow', INK2), ('size', 34),
                                       ('text', 'aumentar essa distância'), ('bg', ORANGE)))
        s, dy, a, dr = engine.enter('pop', t - 4.3)
        place(c, pl, 960, 668, s, 2, a)


def question_rain(c, t, cue):
    rnd = random.Random(300)
    for i in range(26):
        while True:
            x, y = rnd.randint(90, 1830), rnd.randint(90, 990)
            if cue.get('avoid_faces'):   # V1: rostos na CAM_GERAL (Lucian à esquerda, Gustavo à direita)
                if not ((260 < x < 780 and 20 < y < 600) or (1000 < x < 1500 and 100 < y < 740)): break
            elif not (720 < x < 1350 and 150 < y < 700): break
        size = rnd.choice([90, 110, 130, 150]); rot = rnd.choice(gfx.ROTS) * 1.5
        at = i * .045
        if t < at: continue
        im = engine.slap_parts('?', size, INK2 if i % 3 else ORANGE, None)
        sp, let, em, lpos, epos = im
        st = sp.copy(); st.alpha_composite(let, lpos)
        s, dy, a, dr = engine.enter('pop', t - at)
        fall = max(0, t - 2.3 - i * .02)
        yy = y + 1400 * ease_in(min(1, fall / .8))
        place(c, st, x, yy, s, rot + dr + 40 * ease_in(min(1, fall / .8)) * (1 if i % 2 else -1), a)


def _polaroid(img_path, box, w):
    src = Image.open(img_path).convert('RGBA')
    crop = src.crop(box).resize((w, int(w * (box[3] - box[1]) / (box[2] - box[0]))), Image.LANCZOS)
    b = 16
    fr = Image.new('RGBA', (crop.width + 2 * b, crop.height + 2 * b + 30), WHITE + (255,))
    fr.alpha_composite(crop, (b, b))
    return gfx.soft_shadow(fr, (0, 10), 18, .4)


_POL = {}
def bordao_stack(c, t, cue):
    key = FREEZES['freeze:G:508.60']
    if key not in _POL:
        _POL[key] = _polaroid(key, (400, 60, 1640, 760), 380)
    pol = _POL[key]
    place(c, _txt('O BORDÃO DO GUSTAVO', 26, ORANGE, 'inter', 800, 200), 420, 120, alpha=prog(t, 0, .3))
    n = int(1 + 202 * ease_mid(prog(t, .2, 2.6)))
    k = min(12, 1 + int(prog(t, .1, 2.4) * 11))
    rnd = random.Random(203)
    for i in range(k):
        rx, ry, rr = rnd.randint(-60, 60), rnd.randint(-40, 40), rnd.choice(gfx.ROTS)
        s, dy, a, dr = engine.enter('slap', t - .1 - i * .2)
        place(c, pol, 420 + rx, 400 + ry, s * .95, rr + dr, a)
    cnt = _txt(f'{n}×', 150, WHITE, tracking=-40)
    place(c, gfx.hard_shadow(cnt, (5, 6), (0, 0, 0), .3), 430, 690, 1, -4, prog(t, .2, .2))
    if t > 3.0:
        lab = engine.build_img('label', (('lines', ('“Fala aí, analítica e', 'analítico de plantão!”')), ('size', 34)))
        s, dy, a, dr = engine.enter('pop', t - 3.0)
        place(c, lab, 450, 880, s, 3, a)
    _exit_fade(c, t, cue)


def _exit_fade(c, t, cue):
    pass


def ficha(c, t, cue):
    """ficha de presença: Phill 29 · Mafê 24 (EP 1) · Cláudio 'Coisa Rica' Bonel 7."""
    out = cue['dur'] - .35
    s2, dy2, a2, _ = engine.leave('up', t - out)
    if a2 <= 0: return
    w, h = 700, 520
    sheet = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(sheet)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=18, fill=WHITE, outline=INK2, width=4)
    for yy in range(150, h - 20, 118):
        d.line((30, yy, w - 30, yy), fill=(210, 210, 210), width=3)
    d.line((110, 110, 110, h - 20), fill=(244, 115, 64, 120), width=3)
    sheet.alpha_composite(_txt('FICHA DE PRESENÇA', 34, INK2, 'sora', 800, 40), (40, 40))
    R = cue.get('rows', (2.5, 5.7, 13.0)); X = cue.get('extras', (8.6, 15.5))
    rows = [(R[0], 'Phill', 29, None), (R[1], 'Mafê', 24, (X[0], ('convidada do EP 1', '⭐'))),
            (R[2], 'Cláudio “Coisa Rica” Bonel', 7, (X[1], ('recordista de fora', '🏆')))]
    sheet = gfx.hard_shadow(sheet, (8, 10), (0, 0, 0), .85)
    s, dy, a, dr = engine.enter('up', t)
    base = Image.new('RGBA', (sheet.width + 200, sheet.height + 120), (0, 0, 0, 0))
    base.alpha_composite(sheet, (20, 20))
    bd = ImageDraw.Draw(base)
    for i, (at, name, n, extra) in enumerate(rows):
        if t < at: continue
        y = 20 + 150 + i * 118 - 60
        p = prog(t, at, .8)
        base.alpha_composite(_txt(name, 34 if len(name) < 12 else 28, INK2, 'sora', 700), (150, y + 18))
        bd.line([(62, y + 36), (76, y + 52), (100, y + 18)], fill=ORANGE, width=9, joint='curve')
        num = _txt(f'{int(1 + (n - 1) * ease_mid(p))}×', 52, ORANGE, 'sora', 800, -30)
        base.alpha_composite(num, (560, y + 6))
        if extra and t >= extra[0]:
            ex = engine.build_img('pill', (('bg', ORANGE), ('border', INK2), ('emoji', extra[1][1]), ('shadow', INK2), ('size', 22), ('text', extra[1][0])))
            base.alpha_composite(ex, (150, y + 62))
    place(c, base, 420, 560 + dy + dy2, s * .92, -3, a * a2)


def titulo(c, t, cue):
    place(c, _txt('EPISÓDIO 300 · AO VIVO', 30, ORANGE, 'inter', 800, 200), 960, 250, alpha=prog(t, 0, .3))
    l1 = _txt('Do Império dos Dados', 110, WHITE, tracking=-30)
    s, dy, a, dr = engine.enter('rise', t - .05)
    place(c, l1, 960, 420 + dy, 1, 0, a)
    engine.draw_slap(c, dict(text='ao Futuro da Mensuração.', size=110, color=ORANGE, emoji='🔮', rot=-3), t - .55, -1,
                     960, 610, -3, 1, 1, auto=True)
    for who, x, rot, per in (('lucian', 330, -8, 3.2), ('gustavo', 1600, 7, 2.7)):
        im = engine.build_img('face', (('size', 250), ('state', 'still'), ('who', who)))
        s, dy, a, dr = engine.enter('pop', t - 1.0)
        br = math.sin(2 * math.pi * t / per)
        place(c, im, x, 860, s * (1 + .015 * (br + 1)), rot + 1.5 * br, a)


def final(c, t, cue):
    num = _txt(str(int(300 * ease_mid(prog(t, .1, 1.1)))), 360, ORANGE, tracking=-40)
    place(c, gfx.hard_shadow(num, (11, 14), (0, 0, 0), .15), 560, 400)
    txt = [_txt('e contando.', 58, WHITE, 'sora', 700)]
    place(c, txt[0], 470, 610, alpha=prog(t, .8, .4))
    for who, x, rot, per, at in (('lucian', 820, -7, 3.2, .5), ('gustavo', 1040, 7, 2.7, .65)):
        im = engine.build_img('face', (('size', 230), ('state', 'still'), ('who', who)))
        s, dy, a, dr = engine.enter('pop', t - at)
        br = math.sin(2 * math.pi * max(0, t - 1.2) / per)
        place(c, im, x, 830, s * (1 + .015 * (br + 1)), rot + 1.5 * br, a)
    place(c, _txt('PATROCÍNIO', 22, (150, 150, 150), 'inter', 800, 200), 1560, 150, alpha=prog(t, 1.2, .3))
    logos = [('purple-metrics', 4), ('eletromidia', -3), ('onfly', -4), ('reportei', 5), ('sinatra', 2), ('coffee-plusplus', -5)]
    for i, (lg, rot) in enumerate(logos):
        at = 1.3 + i * .18
        im = engine.build_img('asset', (('path', f'patrocinadores/{lg}.webp'), ('size', 250)))
        s, dy, a, dr = engine.enter('pop', t - at)
        sw = math.sin(2 * math.pi * max(0, t - at) / (2.6 + .2 * i))
        x = 1400 + (i % 2) * 330; y = 290 + (i // 2) * 200
        place(c, im, x, y, s * (1 + .02 * abs(sw)), rot + 3 * sw, a)
    pl = engine.build_img('pill', (('bg', ORANGE), ('border', INK2), ('emoji', '🍿'), ('shadow', INK2), ('size', 40),
                                   ('text', 'a sessão já vai começar')))
    s, dy, a, dr = engine.enter('slap', t - 2.6)
    place(c, pl, 1560, 930, s, -2 + dr, a)
    fade = prog(t, cue['dur'] - .9, .9)
    if fade > 0:
        c.alpha_composite(Image.new('RGBA', (1920, 1080), (0, 0, 0, int(255 * fade))))


FUNCS = dict(leader=leader, placar=placar, question_rain=question_rain, bordao_stack=bordao_stack, ficha=ficha,
             titulo=titulo, final=final)


def iris_post(c, t, cue):
    ir = cue.get('iris')
    if not ir or t < ir['at']: return
    p = ease_in(prog(t, ir['at'], ir['dur']))
    R = int(2300 * p)
    if R <= 0: return
    m = Image.new('L', c.size, 255)
    ImageDraw.Draw(m).ellipse((ir['x'] - R, ir['y'] - R, ir['x'] + R, ir['y'] + R), fill=0)
    a = c.getchannel('A'); c.putalpha(Image.fromarray(__import__('numpy').minimum(__import__('numpy').array(a), __import__('numpy').array(m))))


try:
    import customs_v1  # noqa: F401  (registra as cenas da V1 em FUNCS)
except ImportError:
    pass
