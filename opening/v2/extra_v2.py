"""EP300 · V2 — elementos novos do motor (somam-se a extra.KINDS). Mesma assinatura: (c, el, lt, lout, x, y, rot, s, a)."""
import math, json, os, functools
from PIL import Image, ImageDraw
import gfx, extra
from gfx import place, prog, ease_out, ease_io, pop_soft, INK2, WHITE, ORANGE

_EYES = None
def eyes_of(path):
    global _EYES
    if _EYES is None:
        _EYES = json.load(open(os.path.join(gfx.V2A, 'eyes.json')))
    return _EYES.get(path[3:] if path.startswith('v2/') else path)


def heart(size, color=(232, 33, 65)):
    S = 4; n = size * S; im = Image.new('RGBA', (n, n), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = []
    for i in range(200):
        t = 2 * math.pi * i / 200
        pts.append((16 * math.sin(t) ** 3, -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))))
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    k = n * .9 / max(max(xs) - min(xs), max(ys) - min(ys)); cx = (max(xs) + min(xs)) / 2; cy = (max(ys) + min(ys)) / 2
    poly = [(n / 2 + (x - cx) * k, n / 2 + (y - cy) * k) for x, y in pts]
    d.polygon(poly, fill=(255, 255, 255, 255)); d2 = ImageDraw.Draw(im)
    poly2 = [(n / 2 + (x - cx) * k * .82, n / 2 + (y - cy) * k * .82) for x, y in pts]
    d2.polygon(poly2, fill=color + (255,))
    d2.ellipse((n * .30, n * .26, n * .40, n * .34), fill=(255, 255, 255, 200))
    return im.resize((size, size), Image.LANCZOS)


def sparkle(size):
    S = 4; n = size * S; im = Image.new('RGBA', (n, n), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = n / 2; pts = []
    for i in range(8):
        a = math.pi / 4 * i; r = n * .48 if i % 2 == 0 else n * .12
        pts.append((c + r * math.cos(a - math.pi / 2), c + r * math.sin(a - math.pi / 2)))
    d.polygon(pts, fill=(255, 226, 120, 255), outline=(255, 255, 255, 255))
    return im.resize((size, size), Image.LANCZOS)


def stk_fx(c, el, lt, lout, x, y, rot, s, a):
    """adesivo com estados + efeito nos olhos (fx='hearts'|'sparkle') a partir de fx_at — cartoon sobre o adesivo, rosto intacto."""
    path = el['path']
    for t0, p in el.get('states', []):
        if lt >= t0: path = p
    base = extra.sticker_img(path, el.get('size', 320)).copy()
    e = eyes_of(path); fx_at = el.get('fx_at', 0)
    if e and lt >= fx_at:
        # base tem margem de sombra: recalcula a posição dos olhos sobre a imagem do adesivo (sem sombra)
        raw = gfx.asset(path, el.get('size', 320)); ox = (base.width - raw.width) // 2; oy = (base.height - raw.height) // 2
        d = math.hypot((e['rx'] - e['lx']) * raw.width, (e['ry'] - e['ly']) * raw.height)
        k = ease_out(prog(lt, fx_at, .25)); pulse = 1 + .12 * math.sin((lt - fx_at) * 9)
        sz = max(8, int(d * .78 * (.4 + .6 * k) * pulse))
        icon = heart(sz) if el.get('fx', 'hearts') == 'hearts' else sparkle(sz)
        for (fx_, fy_) in ((e['lx'], e['ly']), (e['rx'], e['ry'])):
            px = ox + int(fx_ * raw.width) - icon.width // 2; py = oy + int(fy_ * raw.height) - icon.height // 2
            base.alpha_composite(icon, (max(0, px), max(0, py)))
    if el.get('flip'): base = base.transpose(Image.FLIP_LEFT_RIGHT)
    place(c, base, x, y, s, rot, a)


@functools.lru_cache(maxsize=64)
def _tile(path, size):
    im = gfx.asset(path, size)
    return gfx.soft_shadow(im, (0, 10), 14, .35)


def logo(c, el, lt, lout, x, y, rot, s, a):
    """logo de ferramenta em adesivo-tile quadrado (v2/logos/*.png)."""
    place(c, _tile(el['path'], el.get('size', 190)), x, y, s, rot, a)


@functools.lru_cache(maxsize=64)
def flag_tile_img(code, size):
    """bandeira no formato do site: QUADRADA, cantos arredondados, borda de tinta e sombra sólida deslocada (adesivo colado)."""
    raw = extra.flag_raw(code, 300); h = raw.height
    sq = raw.crop(((raw.width - h) // 2, 0, (raw.width + h) // 2, h)).resize((size, size), Image.LANCZOS)
    pad = 14; im = Image.new('RGBA', (size + 2 * pad, size + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    r = int(size * .2)
    d.rounded_rectangle((pad + 7, pad + 9, pad + size + 7, pad + size + 9), radius=r, fill=INK2 + (255,))
    m = Image.new('L', (size, size), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, size - 1, size - 1), radius=r, fill=255)
    im.paste(sq.convert('RGB'), (pad, pad), m)
    ImageDraw.Draw(im).rounded_rectangle((pad, pad, pad + size - 1, pad + size - 1), radius=r, outline=INK2 + (255,), width=max(4, size // 28))
    return im


def flag_sq(c, el, lt, lout, x, y, rot, s, a):
    place(c, flag_tile_img(el['code'], el.get('size', 150)), x, y, s, rot, a)


extra.KINDS.update(stk_fx=stk_fx, logo=logo, flag_sq=flag_sq)
