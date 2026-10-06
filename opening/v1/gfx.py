"""EP300 · V0 — primitivas gráficas (Pillow) na gramática do handoff Claudio/Lucian.

Tudo é desenhado em 1920x1080 RGBA. Valores (cores, rotações, sombras, curvas) vêm do
"Guia visual — EP 300" e do "Guia de animação" (Lucian, 28/09). Este arquivo é FONTE:
os overlays .mov são regeneráveis a partir dele + overlays.py + plan.py.
"""
import math, os, functools
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H = 1920, 1080
CREAM, ORANGE, INK, WHITE = (247, 244, 237), (244, 115, 64), (18, 18, 19), (255, 255, 255)
INK2 = (2, 2, 2)
DOT_ON = {CREAM: (217, 217, 217), ORANGE: (226, 104, 56), INK: (42, 42, 42)}
ROTS = [-8, 5, -4, 7, -6, 3]

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.environ.get('EP300_HANDOFF', os.path.join(HERE, '..', 'work', 'handoff'))
if not os.path.isdir(ASSETS):   # fallback: handoff oficial no Drive
    import glob as _g
    _c = _g.glob('I:/Drives compartilhados/Educa*/Marketing*/01_CANAIS_ATIVOS/02_PODCAST/2026/300_*/01_VIDEO DE ABERTURA/00_ASSETS E INSERTS/300-handoff-video/assets')
    ASSETS = _c[0] if _c else ASSETS
FONT_DIR = os.path.join(HERE, 'fonts')
SORA = os.path.join(FONT_DIR, 'Sora-VariableFont_wght.ttf')
INTER = os.path.join(FONT_DIR, 'Inter-VariableFont_opsz_wght.ttf')
EMOJI = 'C:/Windows/Fonts/seguiemj.ttf'


# ---------------------------------------------------------------- curvas (guia p.5)
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def bezier(p1x, p1y, p2x, p2y):
    def f(x):
        x = clamp(x)
        lo, hi = 0.0, 1.0
        for _ in range(30):
            t = (lo + hi) / 2
            bx = 3*(1-t)**2*t*p1x + 3*(1-t)*t**2*p2x + t**3
            if bx < x: lo = t
            else: hi = t
        t = (lo + hi) / 2
        return 3*(1-t)**2*t*p1y + 3*(1-t)*t**2*p2y + t**3
    return f

ease_out = bezier(0.25, 1, 0.5, 1)        # "saída suave"
ease_mid = bezier(0.33, 1, 0.68, 1)       # "saída média"
ease_in = bezier(0.32, 0, 0.67, 0)        # "acelera"
ease_io = bezier(0.76, 0, 0.24, 1)        # "vai e vem"
pop_soft = bezier(0.34, 1.56, 0.64, 1)    # "pulo leve"

def pop_strong(x):                          # "pulo forte": 119% no meio, 100% no fim
    x = clamp(x)
    if x < 0.5: return 1.19 * ease_out(x / 0.5)
    return 1.19 - 0.19 * ease_io((x - 0.5) / 0.5)

def prog(t, t0, dur):
    return clamp((t - t0) / dur) if dur > 0 else float(t >= t0)


# ---------------------------------------------------------------- fontes
@functools.lru_cache(maxsize=256)
def font(kind, size, weight=800):
    path = SORA if kind == 'sora' else INTER
    f = ImageFont.truetype(path, int(size))
    try:
        f.set_variation_by_axes([weight] if kind == 'sora' else [min(32, max(14, size/4)), weight])
    except Exception:
        try: f.set_variation_by_axes([weight])
        except Exception: pass
    return f

@functools.lru_cache(maxsize=64)
def emoji_font(size):
    return ImageFont.truetype(EMOJI, 109 if size > 80 else int(size))


def text_img(text, size, color=INK2, kind='sora', weight=800, tracking=0):
    f = font(kind, size, weight)
    if tracking == 0:
        l, t, r, b = f.getbbox(text)
        im = Image.new('RGBA', (r - l + 4, b - t + 4), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((2 - l, 2 - t), text, font=f, fill=color)
        return im
    # tracking manual (unidades de 1/1000 em, como no After Effects)
    xs, x = [], 0
    for ch in text:
        xs.append(x); x += f.getlength(ch) + tracking * size / 1000
    asc, desc = f.getmetrics()
    im = Image.new('RGBA', (int(x) + 8, asc + desc + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for ch, x0 in zip(text, xs):
        d.text((4 + x0, 4), ch, font=f, fill=color)
    return im.crop(im.getbbox()) if im.getbbox() else im


def emoji_img(ch, size):
    f = emoji_font(size)
    im = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    bb = im.getbbox()
    im = im.crop(bb) if bb else im
    s = size / max(im.size)
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)


# ---------------------------------------------------------------- blocos
def round_dilate(alpha, r):
    """dilatação arredondada (papel recortado): blur + limiar."""
    pad = int(r * 2) + 4
    a = Image.new('L', (alpha.width + 2 * pad, alpha.height + 2 * pad), 0)
    a.paste(alpha, (pad, pad))
    b = a.filter(ImageFilter.GaussianBlur(r / 2))
    return b.point(lambda v: 255 if v > 18 else 0).filter(ImageFilter.GaussianBlur(1.2)), pad


def soft_shadow(im, offset=(0, 10), blur=18, opacity=0.4):
    pad = blur * 2 + max(abs(offset[0]), abs(offset[1]))
    base = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 255))
    sh.putalpha(im.getchannel('A').point(lambda v: int(v * opacity)))
    base.paste(sh, (pad + offset[0], pad + offset[1]), sh)
    base = base.filter(ImageFilter.GaussianBlur(blur / 2))
    base.alpha_composite(im, (pad, pad))
    return base


def hard_shadow(im, offset=(3, 4), color=(0, 0, 0), opacity=0.85):
    ox, oy = offset
    base = Image.new('RGBA', (im.width + abs(ox) + 2, im.height + abs(oy) + 2), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, color + (255,))
    sh.putalpha(im.getchannel('A').point(lambda v: int(v * opacity)))
    base.paste(sh, (max(ox, 0), max(oy, 0)), sh)
    base.alpha_composite(im, (max(-ox, 0), max(-oy, 0)))
    return base


def paper_sticker(text, size, letter=INK2, emoji=None, parts=False):
    """Adesivo de texto: papel branco arredondado (14% da fonte) + sombra suave + emoji num círculo.
    parts=True devolve (papel_com_sombra, letras, emoji_circulo, pos_letras, pos_emoji)."""
    let = text_img(text, size, letter, 'sora', 800)
    paper_a, pad = round_dilate(let.getchannel('A'), size * 0.14)
    paper = Image.new('RGBA', paper_a.size, WHITE + (255,)); paper.putalpha(paper_a)
    em = None
    if emoji:
        d = int(size * 0.8)
        circ = Image.new('RGBA', (d, d), (0, 0, 0, 0))
        ImageDraw.Draw(circ).ellipse((0, 0, d - 1, d - 1), fill=WHITE)
        e = emoji_img(emoji, size * 0.55)
        circ.alpha_composite(e, ((d - e.width) // 2, (d - e.height) // 2))
        em = soft_shadow(circ, (0, int(size * .05)), int(size * .1), .35)
    sp = soft_shadow(paper, (0, int(size * 0.05)), max(2, int(size * 0.1)), 0.4)
    spad = (sp.width - paper.width) // 2
    lpos = (pad + spad, pad + spad)
    epos = None
    if em is not None:
        # o círculo cola logo depois da última letra, sobrepondo a borda do papel
        epos = (lpos[0] + let.width + int(size * 0.02) - (em.width - int(size * .8)) // 2,
                lpos[1] + let.height // 2 - em.height // 2)
    if parts:
        return sp, let, em, lpos, epos
    ext = (epos[0] + em.width - sp.width) if em is not None else 0
    out = Image.new('RGBA', (sp.width + max(0, ext), sp.height), (0, 0, 0, 0))
    out.alpha_composite(sp); out.alpha_composite(let, lpos)
    if em is not None:
        e2 = em.rotate(-12, resample=Image.BICUBIC)
        out.alpha_composite(e2, (epos[0], max(0, epos[1])))
    return out


def pill(text, size=34, fg=WHITE, bg=INK, border=WHITE, shadow=ORANGE, bw=3, emoji=None):
    t = text_img(text, size, fg, 'sora', 700)
    ew = 0
    if emoji:
        e = emoji_img(emoji, size * 1.1); ew = e.width + size // 3
    h = t.height + int(size * 0.9); w = t.width + ew + int(size * 1.4)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=bg, outline=border, width=bw)
    x = int(size * 0.7)
    if emoji:
        im.alpha_composite(e, (x, (h - e.height) // 2)); x += ew
    im.alpha_composite(t, (x, (h - t.height) // 2))
    return hard_shadow(im, (int(size * .15), int(size * .2)), shadow, .9)


def label(lines, size=34, sub=None, width=None, bg=WHITE, fg=INK2, radius=22):
    """Etiqueta branca, borda preta 3px, sombra dura 3x4 (guia p.4) — escalada para 1080p."""
    f = font('sora', size, 700)
    ts = [text_img(l, size, fg, 'sora', 700) for l in lines]
    s_im = text_img(sub, size * 0.62, (150, 150, 150), 'sora', 600) if sub else None
    lh = int(size * 1.22)
    w = max(t.width for t in ts) + (s_im.width + size // 2 if s_im else 0)
    w = max(w, width or 0) + int(size * 1.2)
    h = lh * len(ts) + int(size * .9)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=bg, outline=INK2, width=4)
    y = int(size * .45)
    for i, t in enumerate(ts):
        im.alpha_composite(t, (int(size * .6), y + i * lh))
    if s_im:
        im.alpha_composite(s_im, (int(size * .6) + ts[-1].width + size // 3, y + (len(ts) - 1) * lh + int(size * .3)))
    return hard_shadow(im, (6, 8), (0, 0, 0), .85)


def dots_bg(color, size=(W, H), r=2.2, step=26):
    im = Image.new('RGBA', size, color + (255,)); d = ImageDraw.Draw(im)
    dc = DOT_ON.get(color, (0, 0, 0))
    for y in range(step // 2, size[1], step):
        for x in range(step // 2, size[0], step):
            d.ellipse((x - r, y - r, x + r, y + r), fill=dc)
    return im

@functools.lru_cache(maxsize=8)
def bg(color):
    return dots_bg(color)


V1A = os.environ.get('EP300_V1_ASSETS', os.path.join(HERE, '..', 'work', 'v1'))


def asset_path(rel):
    """'v1/...' = assets gerados na V1 (stickers, pipoca, prints); demais = handoff do Claudio."""
    if rel.startswith('v1/'): return os.path.join(V1A, rel[3:])
    if os.path.isabs(rel): return rel
    return os.path.join(ASSETS, rel)


@functools.lru_cache(maxsize=64)
def asset(rel, max_side=None):
    im = Image.open(asset_path(rel)).convert('RGBA')
    if max_side:
        s = max_side / max(im.size)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    return im

@functools.lru_cache(maxsize=64)
def face(who, state='still', size=300):
    """rosto-adesivo (contorno branco já vem na imagem) + sombra 35–45%, 10px, blur 18px."""
    im = asset(f'personagens/{who}/{state}.webp', size)
    return soft_shadow(im, (0, 12), 22, 0.4)


def circle_scribble(w, h, color=ORANGE, width=9, p=1.0, seed=0):
    """círculo 'feito à mão' desenhado progressivamente (p = 0..1)."""
    im = Image.new('RGBA', (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, cy = (w + 40) / 2, (h + 40) / 2
    pts = []
    n = 90
    for i in range(int(n * 1.12 * p) + 1):
        a = -2.2 + 2 * math.pi * i / n
        wob = 1 + 0.04 * math.sin(i * 0.37 + seed) + 0.03 * i / n
        pts.append((cx + math.cos(a) * w / 2 * wob, cy + math.sin(a) * h / 2 * (wob * 0.98)))
    if len(pts) > 1:
        d.line(pts, fill=color, width=width, joint='curve')
    return im


def arrow(length=220, color=WHITE, width=12, curve=0.25, head=46):
    im = Image.new('RGBA', (length + 80, int(length * 0.6) + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x0, y0 = 30, im.height - 40
    x1, y1 = length + 30, 50
    pts = []
    for i in range(41):
        t = i / 40
        mx, my = (x0 + x1) / 2 - curve * (y0 - y1), (y0 + y1) / 2 - curve * (x1 - x0) * 0.4
        x = (1-t)**2*x0 + 2*(1-t)*t*mx + t**2*x1; y = (1-t)**2*y0 + 2*(1-t)*t*my + t**2*y1
        pts.append((x, y))
    d.line(pts, fill=color, width=width, joint='curve')
    ang = math.atan2(pts[-1][1] - pts[-4][1], pts[-1][0] - pts[-4][0])
    for s in (-1, 1):
        a = ang + math.pi + s * 0.5
        d.line([pts[-1], (pts[-1][0] + head * math.cos(a), pts[-1][1] + head * math.sin(a))], fill=color, width=width)
    return im


# ---------------------------------------------------------------- transformações
def place(canvas, im, cx, cy, scale=1.0, rot=0.0, alpha=1.0):
    """cola im centrado em (cx,cy) com escala, rotação (graus, anti-horário = positivo no CSS invertido)."""
    if im is None or alpha <= 0.003 or scale <= 0.005:
        return
    if abs(scale - 1) > 1e-3:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if abs(rot) > 0.05:
        im = im.rotate(-rot, resample=Image.BICUBIC, expand=True)
    if alpha < 0.999:
        a = im.getchannel('A').point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    x, y = int(cx - im.width / 2), int(cy - im.height / 2)
    canvas.alpha_composite(im, (max(0, x), max(0, y)), (max(0, -x), max(0, -y)))


def blank():
    return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def counter_text(n, fmt='{:,}'):
    return fmt.format(int(n)).replace(',', '.')
