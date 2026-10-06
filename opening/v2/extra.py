"""EP300 · V1 — elementos novos do motor (somam-se aos do engine.py da V0; nada da V0 muda de comportamento).

Todos recebem (c, el, lt, lout, x, y, rot, s, a): lt = tempo desde a entrada do elemento, lout = tempo desde
a saída (negativo antes), (x, y, rot, s, a) já com entrada/saída/respiração aplicadas pelo engine.
"""
import math, random, functools
from PIL import Image, ImageDraw, ImageFilter
import gfx
from gfx import place, prog, ease_out, ease_in, ease_io, pop_soft, pop_strong, ORANGE, INK, INK2, WHITE, CREAM


@functools.lru_cache(maxsize=256)
def sticker_img(path, size):
    im = gfx.asset(path, size)
    return gfx.soft_shadow(im, (0, 12), 22, 0.4)


def stk(c, el, lt, lout, x, y, rot, s, a):
    """adesivo de pessoa com estados: states=[(t, path), ...] (t relativo à entrada)."""
    path = el['path']
    for t0, p in el.get('states', []):
        if lt >= t0: path = p
    im = sticker_img(path, el.get('size', 320))
    if el.get('flip'): im = im.transpose(Image.FLIP_LEFT_RIGHT)
    place(c, im, x, y, s, rot, a)


@functools.lru_cache(maxsize=64)
def polaroid_img(path, w, caption, cap_size, crop):
    src = Image.open(gfx.asset_path(path)).convert('RGB')
    if crop:
        cw, ch = src.size; l, t, r, b = crop
        src = src.crop((int(l * cw), int(t * ch), int(r * cw), int(b * ch)))
    h = int(w * src.height / src.width)
    src = src.resize((w, h), Image.LANCZOS)
    pad = int(w * .045); bot = int(w * .16) if caption else pad
    im = Image.new('RGBA', (w + 2 * pad, h + pad + bot), WHITE + (255,))
    im.paste(src, (pad, pad))
    if caption:
        t = gfx.text_img(caption, cap_size, INK2, 'sora', 700)
        if t.width > w: t = t.resize((w, int(t.height * w / t.width)), Image.LANCZOS)
        im.alpha_composite(t, ((im.width - t.width) // 2, h + pad + (bot - t.height) // 2))
    return gfx.soft_shadow(im, (0, 14), 22, 0.42)


def polaroid(c, el, lt, lout, x, y, rot, s, a):
    im = polaroid_img(el['img'], el.get('w', 520), el.get('caption'), el.get('cap', 30), tuple(el['crop']) if el.get('crop') else None)
    place(c, im, x, y, s, rot, a)


def switch(c, el, lt, lout, x, y, rot, s, a):
    """chave ON/OFF em papel: desliga em el['off'] (s)."""
    w, h = el.get('w', 360), el.get('h', 170)
    im = Image.new('RGBA', (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    p = ease_io(prog(lt, el.get('off', 1.0), .22))
    on_col = (88, 196, 120); off_col = (190, 190, 190)
    col = tuple(int(on_col[i] + (off_col[i] - on_col[i]) * p) for i in range(3))
    d.rounded_rectangle((20, 20, 20 + w, 20 + h), radius=h // 2, fill=col, outline=INK2, width=7)
    kx = 20 + h // 2 + (w - h) * (1 - p)
    d.ellipse((kx - h // 2 + 14, 34, kx + h // 2 - 14, 20 + h - 14), fill=WHITE, outline=INK2, width=6)
    lab = gfx.text_img('ON' if p < .5 else 'OFF', int(h * .32), WHITE if p < .5 else INK2, 'sora', 800)
    lx = 20 + int(h * .45) if p < .5 else 20 + w - int(h * .45) - lab.width
    im.alpha_composite(lab, (lx, 20 + (h - lab.height) // 2))
    im = gfx.hard_shadow(im, (6, 8), (0, 0, 0), .5)
    place(c, im, x, y, s, rot, a)


def tl_axis(c, el, lt, lout, x, y, rot, s, a):
    """linha do tempo: eixo desenhado + nós (x_rel, rótulo, at). x..x1 em px, y fixo."""
    x0, x1 = el['x0'], el['x1']; yy = el['y']
    p = ease_out(prog(lt, 0, el.get('draw', .8)))
    d = ImageDraw.Draw(c)
    col = el.get('color', INK2) + (int(255 * a),)
    d.line((x0, yy, x0 + (x1 - x0) * p, yy), fill=col, width=el.get('width', 8))
    for nx, lab, at in el.get('nodes', []):
        ln = lt - at
        if ln < 0: continue
        ss = pop_strong(prog(ln, 0, .35))
        r = int(18 * ss)
        d.ellipse((nx - r, yy - r, nx + r, yy + r), fill=ORANGE + (int(255 * a),), outline=INK2 + (int(255 * a),), width=5)
        if lab:
            t = gfx.text_img(lab, el.get('lab', 30), el.get('lab_color', INK2), 'inter', 800, tracking=100)
            place(c, t, nx, yy + 52, 1, 0, a * min(1, ln * 4))


def tears(c, el, lt, lout, x, y, rot, s, a):
    """lágrimas de desenho caindo dos dois lados do rosto (efeito gráfico, não altera a foto)."""
    rng = random.Random(el.get('seed', 1))
    for side in (-1, 1):
        for k in range(4):
            ph = (lt * 1.4 + k * .25 + rng.random() * .1) % 1.0
            dx = side * (el.get('spread', 70) + 20 * ph); dy = 30 + 170 * ph ** 1.6
            r = 13 * (1 - ph * .4)
            im = Image.new('RGBA', (60, 80), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            d.polygon([(30, 8), (30 - r, 44), (30 + r, 44)], fill=(96, 176, 255))
            d.ellipse((30 - r, 44 - r, 30 + r, 44 + r), fill=(96, 176, 255), outline=WHITE, width=3)
            place(c, im, x + dx, y + dy, s, 0, a * (1 - ph) ** .5)


def confetti(c, el, lt, lout, x, y, rot, s, a):
    """confete leve saindo de um ponto (poucas peças, gravidade)."""
    rng = random.Random(el.get('seed', 3)); n = el.get('n', 26)
    cols = [ORANGE, WHITE, INK2, (255, 206, 84), (120, 196, 255)]
    d = ImageDraw.Draw(c)
    for i in range(n):
        ang = rng.uniform(-math.pi * .95, -math.pi * .05); v = rng.uniform(420, 900)
        t = lt - rng.uniform(0, .12)
        if t < 0 or t > 2.2: continue
        px = x + math.cos(ang) * v * t; py = y + math.sin(ang) * v * t + 520 * t * t
        al = int(255 * a * max(0, 1 - t / 2.2))
        w = rng.randint(10, 18); h = rng.randint(6, 10); sp = rng.uniform(4, 11)
        piece = Image.new('RGBA', (w, h), cols[i % len(cols)] + (al,))
        c.alpha_composite(piece.rotate(math.degrees(sp * t), expand=True), (int(px), int(py)))


FLAGS = {   # bandeiras desenhadas (simplificadas) — (tipo, cores)
    'BR': ('br',), 'PT': ('v2', (0, 102, 0), (255, 0, 0)), 'US': ('us',), 'AR': ('h3', (116, 172, 223), WHITE, (116, 172, 223)),
    'MX': ('v3', (0, 104, 71), WHITE, (206, 17, 38)), 'ES': ('h3w', (170, 21, 27), (241, 191, 0), (170, 21, 27)),
    'FR': ('v3', (0, 85, 164), WHITE, (239, 65, 53)), 'IT': ('v3', (0, 146, 70), WHITE, (206, 43, 55)),
    'DE': ('h3', (0, 0, 0), (221, 0, 0), (255, 206, 0)), 'JP': ('jp',), 'CO': ('h3w', (252, 209, 22), (0, 56, 147), (206, 17, 38)),
    'CL': ('cl',), 'CA': ('ca',), 'AO': ('h2', (204, 9, 47), (0, 0, 0)), 'UK': ('uk',), 'IE': ('v3', (22, 155, 98), WHITE, (255, 136, 62)),
}

@functools.lru_cache(maxsize=64)
def flag_raw(code, w=180):
    return _flag_draw(code, w)


@functools.lru_cache(maxsize=32)
def flag_img(code, w=180):
    return _flag_paper(_flag_draw(code, w), w)


def _flag_draw(code, w):
    h = int(w * 2 / 3); im = Image.new('RGBA', (w, h), WHITE + (255,)); d = ImageDraw.Draw(im)
    f = FLAGS[code]; k = f[0]
    if k == 'v3':
        for i in range(3): d.rectangle((i * w / 3, 0, (i + 1) * w / 3, h), fill=f[1 + i])
    elif k == 'v2':
        d.rectangle((0, 0, w * .4, h), fill=f[1]); d.rectangle((w * .4, 0, w, h), fill=f[2])
    elif k == 'h3':
        for i in range(3): d.rectangle((0, i * h / 3, w, (i + 1) * h / 3), fill=f[1 + i])
    elif k == 'h3w':
        d.rectangle((0, 0, w, h * .25), fill=f[1]); d.rectangle((0, h * .25, w, h * .75), fill=f[2]); d.rectangle((0, h * .75, w, h), fill=f[3])
    elif k == 'h2':
        d.rectangle((0, 0, w, h / 2), fill=f[1]); d.rectangle((0, h / 2, w, h), fill=f[2])
    elif k == 'br':
        d.rectangle((0, 0, w, h), fill=(0, 151, 57)); d.polygon([(w * .08, h / 2), (w / 2, h * .1), (w * .92, h / 2), (w / 2, h * .9)], fill=(254, 221, 0))
        d.ellipse((w / 2 - h * .24, h / 2 - h * .24, w / 2 + h * .24, h / 2 + h * .24), fill=(1, 33, 105))
    elif k == 'us':
        for i in range(13): d.rectangle((0, i * h / 13, w, (i + 1) * h / 13), fill=(178, 34, 52) if i % 2 == 0 else WHITE)
        d.rectangle((0, 0, w * .4, h * 7 / 13), fill=(60, 59, 110))
    elif k == 'jp':
        d.ellipse((w / 2 - h * .3, h / 2 - h * .3, w / 2 + h * .3, h / 2 + h * .3), fill=(188, 0, 45))
    elif k == 'cl':
        d.rectangle((0, h / 2, w, h), fill=(213, 43, 30)); d.rectangle((0, 0, w / 3, h / 2), fill=(0, 57, 166))
    elif k == 'ca':
        d.rectangle((0, 0, w / 4, h), fill=(216, 6, 33)); d.rectangle((w * .75, 0, w, h), fill=(216, 6, 33))
        d.regular_polygon((w / 2, h / 2, h * .22), 5, fill=(216, 6, 33))
    elif k == 'uk':
        d.rectangle((0, 0, w, h), fill=(1, 33, 105)); d.line((0, 0, w, h), fill=WHITE, width=int(h * .2)); d.line((0, h, w, 0), fill=WHITE, width=int(h * .2))
        d.rectangle((w * .42, 0, w * .58, h), fill=WHITE); d.rectangle((0, h * .38, w, h * .62), fill=WHITE)
        d.rectangle((w * .46, 0, w * .54, h), fill=(200, 16, 46)); d.rectangle((0, h * .43, w, h * .57), fill=(200, 16, 46))
    return im


def _flag_paper(im, w):
    h = im.height
    # papel: contorno branco arredondado + sombra
    mask = Image.new('L', (w, h), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=14, fill=255)
    im.putalpha(mask)
    out = Image.new('RGBA', (w + 20, h + 20), (0, 0, 0, 0)); ImageDraw.Draw(out).rounded_rectangle((0, 0, w + 19, h + 19), radius=20, fill=WHITE)
    out.alpha_composite(im, (10, 10))
    return gfx.soft_shadow(out, (0, 8), 14, .35)


def flag(c, el, lt, lout, x, y, rot, s, a):
    place(c, flag_img(el['code'], el.get('w', 180)), x, y, s, rot, a)


def rec(c, el, lt, lout, x, y, rot, s, a):
    """moldura de câmera antiga: REC piscando, cantos, rótulo e timecode (arquivo de bastidor)."""
    d = ImageDraw.Draw(c); al = int(255 * a)
    for (cx, cy, sx, sy) in ((70, 70, 1, 1), (1850, 70, -1, 1), (70, 1010, 1, -1), (1850, 1010, -1, -1)):
        d.line((cx, cy, cx + 90 * sx, cy), fill=(255, 255, 255, al), width=6); d.line((cx, cy, cx, cy + 90 * sy), fill=(255, 255, 255, al), width=6)
    if int(lt * 2) % 2 == 0:
        d.ellipse((120, 112, 158, 150), fill=(230, 40, 40, al))
    place(c, gfx.text_img('REC', 44, WHITE, 'inter', 800, tracking=100), 220, 131, 1, 0, a)
    place(c, gfx.text_img(el.get('label', 'ARQUIVO'), 30, WHITE, 'inter', 700, tracking=150), 1500, 131, 1, 0, a * .9)
    tc = el.get('tc0', 0) + lt
    txt = f"{int(tc // 3600):02d}:{int(tc // 60 % 60):02d}:{int(tc % 60):02d}:{int(tc * 30 % 30):02d}"
    place(c, gfx.text_img(txt, 34, WHITE, 'inter', 600, tracking=60), 1640, 960, 1, 0, a * .9)


def exit_sign(c, el, lt, lout, x, y, rot, s, a):
    """placa SAÍDA: [ícone] SAÍDA [seta] — largura calculada pelo conteúdo (V2: a seta não cruza mais o texto)."""
    h = el.get('h', 170)
    glow = .75 + .25 * math.sin(lt * 9)
    t = gfx.text_img(el.get('text', 'SAÍDA'), int(h * .42), WHITE, 'sora', 800, tracking=40)
    e = gfx.emoji_img('🏃', int(h * .52))
    ar = gfx.text_img(el.get('arrow', '→'), int(h * .5), WHITE, 'inter', 800)
    pad, gap = int(h * .22), int(h * .16)
    w = pad + e.width + gap + t.width + gap + ar.width + pad
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=22, fill=(24, 140, 76), outline=WHITE, width=7)
    xx = pad
    im.alpha_composite(e, (xx, (h - e.height) // 2)); xx += e.width + gap
    im.alpha_composite(t, (xx, (h - t.height) // 2)); xx += t.width + gap
    im.alpha_composite(ar, (xx, (h - ar.height) // 2 - 4))
    im = gfx.hard_shadow(im, (6, 8), (0, 0, 0), .45)
    place(c, im, x, y, s * (0.98 + .02 * glow), rot, a)


def ph_person(c, el, lt, lout, x, y, rot, s, a):
    """PLACEHOLDER claramente identificado para foto que falta (nunca rosto inventado)."""
    r = el.get('r', 120)
    im = Image.new('RGBA', (2 * r + 40, 2 * r + 110), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((20, 20, 20 + 2 * r, 20 + 2 * r), fill=(235, 232, 225), outline=WHITE, width=10)
    for k in range(0, 360, 20):
        a0 = math.radians(k); a1 = math.radians(k + 10)
        d.arc((26, 26, 14 + 2 * r, 14 + 2 * r), k, k + 10, fill=INK2, width=4)
    t = gfx.text_img(el['initials'], int(r * .7), INK2, 'sora', 800)
    im.alpha_composite(t, (20 + r - t.width // 2, 20 + r - t.height // 2))
    tag = gfx.pill('foto pendente', 20, fg=INK2, bg=(255, 214, 120), border=INK2, shadow=INK2)
    im.alpha_composite(tag, (20 + r - tag.width // 2, 2 * r + 30))
    place(c, gfx.soft_shadow(im, (0, 10), 16, .35), x, y, s, rot, a)


def diamond(c, el, lt, lout, x, y, rot, s, a):
    """diamante facetado desenhado (brilho girando)."""
    R = el.get('r', 120); col = el.get('color', (40, 40, 44))
    im = Image.new('RGBA', (2 * R + 40, 2 * R + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, cy = R + 20, R + 20
    top = cy - R * .55; mid = cy - R * .15; bot = cy + R * .95
    pts = [(cx - R, mid), (cx - R * .55, top), (cx + R * .55, top), (cx + R, mid), (cx, bot)]
    d.polygon(pts, fill=col, outline=WHITE, width=6)
    lc = tuple(min(255, v + 60) for v in col)
    d.polygon([(cx - R * .55, top), (cx - R * .2, mid), (cx - R, mid)], fill=lc)
    d.polygon([(cx + R * .55, top), (cx + R * .2, mid), (cx + R, mid)], fill=lc)
    d.polygon([(cx - R * .2, mid), (cx + R * .2, mid), (cx, bot)], fill=tuple(min(255, v + 30) for v in col))
    d.line([(cx - R, mid), (cx + R, mid)], fill=WHITE, width=4)
    for px in (cx - R * .55, cx - R * .2, cx + R * .2, cx + R * .55):
        d.line([(px, mid), (cx, bot)], fill=(255, 255, 255, 120), width=3)
    # brilho
    sp = (math.sin(lt * 3 + el.get('seed', 0)) + 1) / 2
    if sp > .6:
        k = (sp - .6) / .4; L = 26 + 30 * k; sx, sy = cx + R * .35, top + R * .12
        d.line((sx - L, sy, sx + L, sy), fill=WHITE, width=6); d.line((sx, sy - L, sx, sy + L), fill=WHITE, width=6)
    place(c, gfx.soft_shadow(im, (0, 12), 18, .4), x, y, s, rot, a)


def choco(c, el, lt, lout, x, y, rot, s, a):
    """barra de chocolate genérica meio desembrulhada (referência, sem marca de terceiros)."""
    w, h = el.get('w', 640), el.get('h', 300)
    im = Image.new('RGBA', (w + 30, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((15, 15, 15 + w, 15 + h), radius=24, fill=(74, 44, 30), outline=WHITE, width=8)
    cols, rows = 4, 2; cw = w * .55 / cols; rh = (h - 40) / rows
    for i in range(cols):
        for j in range(rows):
            x0 = 35 + i * cw; y0 = 35 + j * rh
            d.rounded_rectangle((x0, y0, x0 + cw - 14, y0 + rh - 14), radius=10, fill=(96, 60, 42), outline=(58, 34, 22), width=4)
    # embalagem (paleta EP300)
    wx = 15 + w * .58
    d.rectangle((wx, 15, 15 + w, 15 + h), fill=INK)
    d.rectangle((wx, 15, wx + 16, 15 + h), fill=ORANGE)
    t1 = gfx.text_img(el.get('l1', 'DIAMANTE'), int(h * .17), WHITE, 'sora', 800)
    t2 = gfx.text_img(el.get('l2', 'NEGRO'), int(h * .17), ORANGE, 'sora', 800)
    t3 = gfx.text_img(el.get('l3', 'do Analytics'), int(h * .09), WHITE, 'inter', 700)
    bx = int(wx + 30)
    for t, yy in ((t1, h * .2), (t2, h * .42), (t3, h * .68)):
        if t.width > w * .38: t = t.resize((int(w * .38), int(t.height * w * .38 / t.width)), Image.LANCZOS)
        im.alpha_composite(t, (bx, int(15 + yy)))
    place(c, gfx.soft_shadow(im, (0, 14), 22, .45), x, y, s, rot, a)


def ga4(c, el, lt, lout, x, y, rot, s, a):
    """ícone de barras (tipo GA) desenhado em papel — placeholder do logo oficial."""
    S = el.get('size', 220); im = Image.new('RGBA', (S + 40, S + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, S + 39, S + 39), radius=int(S * .22), fill=WHITE)
    bw = S * .22; g = S * .08; base = S * .92 + 20
    hs = [.38, .62, .86]; cols = [(249, 171, 0), (232, 113, 10), (227, 116, 0)]
    for i, (hh, cc) in enumerate(zip(hs, cols)):
        p = ease_out(prog(lt, .1 + i * .1, .4))
        x0 = 20 + S * .12 + i * (bw + g)
        top = base - S * hh * p
        if i == 0:
            r = bw / 2; d.ellipse((x0, base - bw, x0 + bw, base), fill=cc)
        else:
            d.rounded_rectangle((x0, top, x0 + bw, base), radius=int(bw / 2), fill=cc)
    place(c, gfx.soft_shadow(im, (0, 10), 16, .4), x, y, s, rot, a)


def balloon(c, el, lt, lout, x, y, rot, s, a):
    """balão de fala em papel com rabinho (tail='left'|'right')."""
    t = gfx.text_img(el['text'], el.get('size', 44), INK2, 'sora', 800)
    pw, ph = t.width + 60, t.height + 44
    im = Image.new('RGBA', (pw + 60, ph + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, 10 + pw, 10 + ph), radius=ph // 2, fill=WHITE, outline=INK2, width=6)
    tx = 50 if el.get('tail', 'left') == 'left' else pw - 30
    d.polygon([(tx, 6 + ph), (tx + 34, 6 + ph), (tx - 8 if el.get('tail', 'left') == 'left' else tx + 44, ph + 52)], fill=WHITE, outline=INK2)
    d.line((tx + 2, 10 + ph - 3, tx + 32, 10 + ph - 3), fill=WHITE, width=8)
    im.alpha_composite(t, (40, 32))
    place(c, gfx.hard_shadow(im, (5, 7), (0, 0, 0), .3), x, y, s, rot, a)


def wordmark(c, el, lt, lout, x, y, rot, s, a):
    """palavra com letras em cores diferentes (placeholder de marca de terceiros, sem logo oficial)."""
    cols = el.get('colors', [(66, 133, 244), (234, 67, 53), (251, 188, 5), (66, 133, 244), (52, 168, 83), (234, 67, 53)])
    parts = [gfx.text_img(ch, el.get('size', 90), cols[i % len(cols)], 'sora', 800) for i, ch in enumerate(el['text'])]
    w = sum(p.width for p in parts) + 60; h = max(p.height for p in parts) + 50
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=WHITE, outline=INK2, width=5)
    xx = 30
    for p in parts: im.alpha_composite(p, (xx, 22)); xx += p.width - 2
    place(c, gfx.hard_shadow(im, (5, 7), (0, 0, 0), .35), x, y, s, rot, a)


KINDS = dict(stk=stk, polaroid=polaroid, switch=switch, tl_axis=tl_axis, tears=tears, confetti=confetti, flag=flag, rec=rec,
             exit_sign=exit_sign, ph_person=ph_person, diamond=diamond, choco=choco, ga4=ga4, balloon=balloon, wordmark=wordmark)
