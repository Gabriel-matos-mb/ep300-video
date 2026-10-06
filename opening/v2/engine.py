"""EP300 · V1 (derivado da V0) — motor de overlays: cada cue do plan.py vira uma lista de elementos animados.

Tempos dos elementos são RELATIVOS ao início do cue (segundos). Animações = Biblioteca de
animações do Guia (tapa do adesivo, etiqueta estoura, linha sobe, contador, bloco sai...).
"""
import math, functools
from PIL import Image, ImageDraw, ImageChops
import gfx, extra, extra_v2
from gfx import place, prog, pop_strong, pop_soft, ease_out, ease_mid, ease_in, ease_io

FPS = 30


@functools.lru_cache(maxsize=512)
def build_img(kind, key):
    """imagens estáticas cacheadas (key = tupla hashável de parâmetros)."""
    p = dict(key)
    if kind == 'pill':
        return gfx.pill(p['text'], p.get('size', 34), fg=p.get('fg', gfx.WHITE), bg=p.get('bg', gfx.INK),
                        border=p.get('border', gfx.WHITE), shadow=p.get('shadow', gfx.ORANGE), emoji=p.get('emoji'))
    if kind == 'label':
        return gfx.label(list(p['lines']), p.get('size', 34), sub=p.get('sub'), bg=p.get('bg', gfx.WHITE))
    if kind == 'text':
        im = gfx.text_img(p['text'], p['size'], p.get('color', gfx.INK2), p.get('font', 'sora'), p.get('weight', 800),
                          p.get('tracking', 0))
        if p.get('shadow'):
            s = p['size']; im = gfx.hard_shadow(im, (int(s * .03), int(s * .04)), (0, 0, 0), p.get('shadow'))
        return im
    if kind == 'face':
        return gfx.face(p['who'], p.get('state', 'still'), p.get('size', 300))
    if kind == 'asset':
        im = gfx.asset(p['path'], p.get('size'))
        return gfx.soft_shadow(im, (0, 10), 18, 0.4) if p.get('shadow', True) else im
    if kind == 'emoji':
        return gfx.emoji_img(p['ch'], p['size'])
    if kind == 'stamp':
        return stamp_img(p['lines'], p.get('size', 60), p.get('color', gfx.ORANGE), p.get('fill'))
    if kind == 'arrow':
        return gfx.arrow(p.get('length', 220), p.get('color', gfx.WHITE), p.get('width', 12), p.get('curve', .25))
    if kind == 'sign':
        return None
    raise KeyError(kind)


def stamp_img(lines, size, color, fill=None):
    ts = [gfx.text_img(l, size, color if not fill else gfx.WHITE, 'sora', 800, tracking=-10) for l in lines]
    w = max(t.width for t in ts) + int(size * 1.0); lh = int(size * 1.12)
    h = lh * len(ts) + int(size * .7)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if fill:
        d.rounded_rectangle((0, 0, w - 1, h - 1), radius=int(size * .25), fill=fill)
    d.rounded_rectangle((6, 6, w - 7, h - 7), radius=int(size * .2), outline=color if not fill else gfx.WHITE,
                        width=max(5, int(size * .09)))
    y = int(size * .35)
    for t in ts:
        im.alpha_composite(t, ((w - t.width) // 2, y)); y += lh
    return gfx.hard_shadow(im, (6, 8), (0, 0, 0), .35)


def img_of(el):
    k = el['k']
    if k in ('pill', 'label', 'text', 'face', 'asset', 'emoji', 'stamp', 'arrow'):
        key = tuple(sorted((a, tuple(b) if isinstance(b, list) else b) for a, b in el.items()
                           if a not in ('k', 'at', 'out', 'x', 'y', 'rot', 'anim', 'scale', 'exit', 'fx', 'susto', 'breath', 'sway', 'states')))
        return build_img(k, key)
    return None


# ---------------------------------------------------------------- animação de entrada/saída
def enter(anim, lt):
    """-> (scale, dy, alpha, drot) para tempo local lt desde a entrada."""
    if lt < 0: return 0, 0, 0, 0
    if anim == 'pop':          # etiqueta estoura (50%→100%)
        p = prog(lt, 0, .5); return .5 + .5 * pop_soft(p), 0, min(1, p * 3), 0
    if anim == 'slap':         # tapa do adesivo (125% → 100%, -9° → 0)
        p = prog(lt, 0, .4); s = 1.25 - .25 * pop_strong(p) / 1.0
        return (s if p > 0 else 1.25), 0, min(1, p * 5), -9 * (1 - ease_out(p))
    if anim == 'rise':         # linha sobe 24px
        p = prog(lt, 0, .7); return 1, 24 * (1 - ease_out(p)), ease_out(p), 0
    if anim == 'up':           # etiqueta sobe 16px
        p = prog(lt, 0, .5); return 1, 16 * (1 - ease_out(p)), min(1, p * 2), 0
    if anim == 'stamp':        # carimbo: bate de 160%
        p = prog(lt, 0, .28); return 1.6 - .6 * ease_in(p) if p < 1 else 1, 0, min(1, p * 4), 0
    if anim == 'burst':        # emoji estoura (0→100%, gira -40→+12)
        p = prog(lt, 0, .45); return pop_strong(p), 0, min(1, p * 4), -52 * (1 - ease_out(p))
    if anim == 'drop':         # cai de cima
        p = prog(lt, 0, .55); return 1, -700 * (1 - pop_soft(p)), 1, 0
    if anim == 'none':
        return 1, 0, 1, 0
    if anim == 'fromR':        # V2: entra deslizando pela direita (a página anterior sai pela esquerda)
        return 1, 0, 1, 0
    raise KeyError(anim)


def dx_in(anim, lt):
    if anim == 'fromR':
        p = prog(lt, 0, .5); return 1920 * (1 - ease_io(p))
    return 0


def dx_out(kind, lt):
    if kind == 'toL' and lt >= 0:
        p = prog(lt, 0, .5); return -1920 * ease_io(p)
    return 0


def leave(kind, lt):
    """lt = tempo desde a saída. 'up' = bloco sai (sobe e some, acelera 0.3s)."""
    if lt < 0: return 1, 0, 1, 0
    if kind == 'up':
        p = prog(lt, 0, .3); return 1, -40 * ease_in(p), 1 - ease_in(p), 0
    if kind == 'fall':
        p = prog(lt, 0, .7); return 1, 1200 * ease_in(p), 1, 25 * ease_in(p)
    if kind == 'shrink':
        p = prog(lt, 0, .3); return 1 - ease_in(p), 0, 1, 0
    if kind == 'cut':
        return 1, 0, 0, 0
    if kind == 'toL':
        return 1, 0, 1, 0
    raise KeyError(kind)


def draw_el(c, el, t, cue_dur):
    at = el.get('at', 0); out = el.get('out', cue_dur - 0.32)
    if t < at: return
    lt = t - at
    s, dy, a, dr = enter(el.get('anim', 'pop'), lt)
    s2, dy2, a2, dr2 = leave(el.get('exit', 'up'), t - out)
    if a * a2 <= 0.003: return
    x, y, rot = el.get('x', 960), el.get('y', 540), el.get('rot', 0)
    _dx = dx_in(el.get('anim', 'pop'), lt) + dx_out(el.get('exit', 'up'), t - out)
    x += _dx
    gfx.CUR_TAG[0] = f"{el['k']}:{str(el.get('text') or el.get('lines') or el.get('path') or el.get('ch') or '')[:28]}" + ('~slide' if abs(_dx) > 1 else '') + ('~enter' if lt < .5 else '') + ('~fall' if el.get('exit') == 'fall' and t > out else '')
    sc = el.get('scale', 1.0)
    # vida contínua
    if el.get('breath'):
        per = el['breath']; ph = math.sin(2 * math.pi * max(0, lt - 1.2) / per)
        sc *= 1 + .03 * (ph + 1) / 2; rot += 1.5 * ph
    if el.get('sway'):
        per = el['sway']; ph = math.sin(2 * math.pi * lt / per)
        sc *= 1 + .03 * (1 - math.cos(2 * math.pi * lt / per)) / 2; rot += 4 * ph
    k = el['k']
    if k == 'slap':
        draw_slap(c, el, lt, t - out, x, y + dy + dy2, rot + dr + dr2, s * s2 * sc, a * a2)
        return
    if k == 'counter':
        p = prog(lt, el.get('delay', 0), el.get('cdur', 1.1))
        n = el['from'] + (el['to'] - el['from']) * ease_mid(p)
        txt = el.get('fmt', '{}').format(gfx.counter_text(n) if not el.get('raw') else int(n))
        im = gfx.text_img(txt, el['size'], el.get('color', gfx.INK2), 'sora', 800, tracking=-40)
        im = gfx.hard_shadow(im, (int(el['size'] * .03), int(el['size'] * .04)), (0, 0, 0), .15)
        place(c, im, x, y + dy + dy2, s * s2 * sc, rot + dr + dr2, a * a2); return
    if k == 'scribble':
        p = ease_out(prog(lt, 0, el.get('dur', .45)))
        im = gfx.circle_scribble(el['w'], el['h'], el.get('color', gfx.ORANGE), el.get('width', 9), p, el.get('seed', 0))
        place(c, im, x, y + dy2, 1, rot, a2); return
    if k == 'strike':
        p = ease_out(prog(lt, 0, .3)); w = el['w']
        im = Image.new('RGBA', (w + 20, 40), (0, 0, 0, 0))
        ImageDraw.Draw(im).line((10, 26, 10 + w * p, 14), fill=el.get('color', gfx.ORANGE), width=el.get('width', 10))
        place(c, im, x, y + dy2, 1, rot, a2); return
    if k == 'grid':
        n, fill = el['n'], el['fill']; r = el.get('r', 34); gap = el.get('gap', 22)
        cols = el.get('cols', n)
        for i in range(n):
            px = x + (i % cols - (cols - 1) / 2) * (2 * r + gap); py = y + (i // cols) * (2 * r + gap)
            li = lt - i * 0.06
            if li < 0: continue
            ss, _, aa, _ = enter('pop', li)
            im = Image.new('RGBA', (2 * r + 8, 2 * r + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            on = i < fill and lt > el.get('fill_at', 0) + i * 0.12
            d.ellipse((4, 8, 2 * r + 4, 2 * r + 8), fill=(0, 0, 0, 90))
            d.ellipse((0, 0, 2 * r, 2 * r), fill=gfx.ORANGE if on else gfx.WHITE, outline=gfx.INK2, width=4)
            place(c, im, px, py + dy2, ss * s2, 0, aa * a2)
        return
    if k == 'sofa':
        ts = [0, .78, 1.41, 2.12, 2.92, 3.64]
        fr = max(i for i, v in enumerate(ts) if lt >= v) + 1
        im = build_img('asset', (('path', f'cena-sofa/{fr}.webp'), ('size', el.get('size', 640))))
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        place(c, im, x, y + dy + dy2, s * s2 * sc, rot + dr + dr2, a * a2); return
    if k == 'susto':
        pass
    if k == 'face' and el.get('susto') is not None:
        st = lt - el['susto']
        state = 'still'
        if 0 <= st < .11: state = 'hover-transicao'
        elif .11 <= st < .96: state = 'hover-final'
        im = build_img('face', (('who', el['who']), ('state', state), ('size', el.get('size', 300))))
        place(c, im, x, y + dy + dy2, s * s2 * sc, rot + dr + dr2, a * a2); return
    if k == 'photo':
        draw_photo(c, el, lt, t - out, a2); return
    if k == 'marquee':
        draw_marquee(c, el, lt, x, y + dy + dy2, rot + dr + dr2, s * s2 * sc, a * a2); return
    if k == 'cursor':
        draw_cursor(c, el, lt); return
    if k == 'iris':
        return
    if k == 'clock':
        draw_clock(c, el, lt, x, y + dy + dy2, s * s2 * sc, a * a2); return
    if k == 'bleep':
        draw_bleep(c, el, lt, x, y, s * s2, a * a2); return
    if k in extra.KINDS:
        extra.KINDS[k](c, el, lt, t - out, x, y + dy + dy2, rot + dr + dr2, s * s2 * sc, a * a2); return
    if k == 'emoji' and el.get('states'):   # V2: emoji troca de reação ao longo da cena
        ch = el['ch']
        for t0, cc in el['states']:
            if lt >= t0: ch = cc
        im = build_img('emoji', (('ch', ch), ('size', el['size'])))
        place(c, im, x, y + dy + dy2, s * s2 * sc, rot + dr + dr2, a * a2); return
    im = img_of(el)
    place(c, im, x, y + dy + dy2, s * s2 * sc, rot + dr + dr2, a * a2)


def draw_slap(c, el, lt, lout, x, y, rot, s, a, auto=False):
    if lt < 0: return
    if auto:
        s0, dy0, a0, dr0 = enter('slap', lt); s *= s0; a *= a0; rot += dr0
    size = el['size']; letter = el.get('color', gfx.INK2)
    key = (el['text'], size, letter, el.get('emoji'))
    sp, let, em, lpos, epos = slap_parts(*key)
    base_rot = el.get('rot', -3)
    im = Image.new('RGBA', (sp.width + (em.width if em is not None else 0) + 20, max(sp.height, (em.height if em is not None else 0) + 20)), (0, 0, 0, 0))
    im.alpha_composite(sp, (0, 0))
    # letras preenchem (0.1s depois do papel)
    pl = prog(lt, .1, .3)
    if pl > 0:
        l2 = let
        if pl < 1:
            l2 = let.copy(); l2.putalpha(let.getchannel('A').point(lambda v: int(v * ease_mid(pl))))
        im.alpha_composite(l2, (lpos[0], lpos[1] + int(size * .45 * (1 - ease_mid(pl)))))
    if em is not None:
        pe = prog(lt, .35, .45)
        if pe > 0:
            es = pop_strong(pe); er = -40 + 52 * ease_out(pe)
            e2 = em.resize((max(1, int(em.width * es)), max(1, int(em.height * es))), Image.BILINEAR).rotate(-er, resample=Image.BICUBIC, expand=True)
            cx, cy = epos[0] + em.width // 2, epos[1] + em.height // 2
            im.alpha_composite(e2, (max(0, cx - e2.width // 2), max(0, cy - e2.height // 2)))
    place(c, im, x, y, s, rot, a)


@functools.lru_cache(maxsize=128)
def slap_parts(text, size, letter, emoji):
    return gfx.paper_sticker(text, size, letter, emoji, parts=True)


# ---------------------------------------------------------------- elementos especiais
PHOTO_CACHE = {}

def draw_photo(c, el, lt, lout, a2):
    """REALIDADE → STICKER: o quadro congelado (tela cheia) encolhe e vira foto-adesivo torta."""
    src = PHOTO_CACHE.get(el['img'])
    if src is None:
        import customs
        src = Image.open(customs.FREEZES.get(el['img'], el['img'])).convert('RGBA').resize((gfx.W, gfx.H), Image.LANCZOS)
        PHOTO_CACHE[el['img']] = src
    p = ease_io(prog(lt, el.get('hold', .25), el.get('shrink', .55)))
    tx, ty, ts, tr = el['to']
    scale = 1 + (ts - 1) * p; rot = tr * p
    cx = 960 + (tx - 960) * p; cy = 540 + (ty - 540) * p
    border = int(28 * p)
    if border > 0:
        fr = Image.new('RGBA', (gfx.W + 2 * border, gfx.H + 2 * border), gfx.WHITE + (255,))
        fr.alpha_composite(src, (border, border))
    else:
        fr = src
    small = fr.resize((max(1, int(fr.width * scale)), max(1, int(fr.height * scale))), Image.BILINEAR)
    if p > 0.02:
        small = gfx.soft_shadow(small, (0, int(14 * p)), int(24 * p) + 1, .45 * p)
    # flash branco no congelamento
    if lt < .12 and el.get('flash', True):
        c.alpha_composite(Image.new('RGBA', (gfx.W, gfx.H), (255, 255, 255, int(160 * (1 - lt / .12)))))
    place(c, small, cx, cy, 1, rot, a2)


def draw_marquee(c, el, lt, x, y, rot, s, a):
    """placa de cinema com lâmpadas piscando (objeto de pré-sessão)."""
    lines = el['lines']; size = el.get('size', 70)
    ts = [gfx.text_img(l, size, gfx.INK2, 'sora', 800, tracking=-20) for l in lines]
    w = max(t.width for t in ts) + size * 2; lh = int(size * 1.15); h = lh * len(ts) + size * 2
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=26, fill=gfx.INK, outline=gfx.WHITE, width=5)
    d.rounded_rectangle((size * .55, size * .55, w - size * .55, h - size * .55), radius=16, fill=gfx.CREAM)
    yy = size
    for t in ts:
        im.alpha_composite(t, ((w - t.width) // 2, int(yy))); yy += lh
    # lâmpadas
    ph = int(lt * 8)
    per = 2 * (w + h); n = int(per / 34)
    for i in range(n):
        dpos = i * per / n
        if dpos < w: bx, by = dpos, size * .27
        elif dpos < w + h: bx, by = w - size * .27, dpos - w
        elif dpos < 2 * w + h: bx, by = w - (dpos - w - h), h - size * .27
        else: bx, by = size * .27, h - (dpos - 2 * w - h)
        on = (i + ph) % 2 == 0
        r = 7
        d.ellipse((bx - r, by - r, bx + r, by + r), fill=(255, 214, 120) if on else (120, 90, 50))
    im = gfx.hard_shadow(im, (8, 10), gfx.ORANGE, .95)
    place(c, im, x, y, s, rot, a)


CURSOR = None
def draw_cursor(c, el, lt):
    """mão/cursor que clica: vem de (x0,y0) até (x,y) em 'move' s, clica em 'click'."""
    global CURSOR
    if CURSOR is None:
        CURSOR = gfx.emoji_img('👆', 110)
    p = ease_io(prog(lt, 0, el.get('move', .6)))
    x = el['x0'] + (el['x'] - el['x0']) * p; y = el['y0'] + (el['y'] - el['y0']) * p
    ck = lt - el.get('click', .7)
    s = 1 - .15 * (1 - abs(ck / .08 - 1)) if 0 <= ck < .16 else 1
    place(c, CURSOR, x + 20, y + 55, s, 0, 1 if lt < el.get('gone', 99) else 0)


def draw_clock(c, el, lt, x, y, s, a):
    r = el.get('r', 60)
    im = Image.new('RGBA', (2 * r + 10, 2 * r + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((5, 5, 2 * r + 5, 2 * r + 5), fill=gfx.WHITE, outline=gfx.INK2, width=5)
    cx = cy = r + 5
    for per, ln, wd in ((6, r * .72, 6), (2 * el.get('fast', 1), r * .5, 8)):
        ang = 2 * math.pi * lt / per - math.pi / 2
        d.line((cx, cy, cx + ln * math.cos(ang), cy + ln * math.sin(ang)), fill=gfx.INK2, width=wd)
    place(c, gfx.hard_shadow(im, (4, 5), (0, 0, 0), .8), x, y, s, 6, a)


def draw_bleep(c, el, lt, x, y, s, a):
    w, h = el.get('w', 520), el.get('h', 120)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=18, fill=gfx.INK2, outline=gfx.WHITE, width=5)
    t = gfx.text_img(el.get('text', '#@!%&!'), int(h * .55), gfx.ORANGE, 'sora', 800)
    im.alpha_composite(t, ((w - t.width) // 2, (h - t.height) // 2))
    jit = math.sin(lt * 60) * 3
    place(c, gfx.hard_shadow(im, (6, 8), gfx.ORANGE, .95), x + jit, y, s, el.get('rot', -4), a)


# ---------------------------------------------------------------- render de um cue
def _shift(im, dx):
    dx = int(round(dx))
    if dx == 0: return im
    out = gfx.blank()
    if abs(dx) < gfx.W: out.paste(im, (dx, 0))
    return out


def render_frame(cue, t):
    """t em segundos desde o início do cue -> Image RGBA 1920x1080.
    V2: cue['push_out'] (s) = a cena é empurrada para a esquerda nos últimos push_out s por cue['push_in'] da cena seguinte,
    que desliza da direita — as duas se encostam, sem câmera aparecendo entre elas."""
    P_out = cue.get('push_out') if cue.get('push_len') else None; P_in = cue.get('push_in')
    if P_out is not None or P_in:
        base = dict(cue, trans_in=False if P_in else cue.get('trans_in', True), trans_out=False if P_out is not None else cue.get('trans_out', True))
        if P_out is not None: base['dur'] = cue['dur'] + P_out + 1.0      # elementos não saem antes do empurrão
        c = _render(base, t)
        if P_out is not None:
            PL = cue.get('push_len', P_out); end = cue['dur'] + P_out
            c = _shift(c, -gfx.W * ease_io(prog(t, end - PL, PL)))
        if P_in:
            p = ease_io(prog(t, 0, P_in)); c = _shift(c, gfx.W * (1 - p))
            if 0 < p < 1:
                ImageDraw.Draw(c).rectangle((int(gfx.W * (1 - p)) - 14, 0, int(gfx.W * (1 - p)), gfx.H), fill=gfx.ORANGE + (255,))
        return c
    return _render(cue, t)


def _render(cue, t):
    c = gfx.blank()
    mask = None; bands = []
    if cue.get('bg'):
        b = cue['bg']
        if isinstance(b, dict):
            if t >= b.get('from', 0) and t < b.get('to', 1e9):
                c.alpha_composite(gfx.bg(tuple(b['color'])))
        else:
            bgim = gfx.bg(tuple(b))
            if cue.get('full') and cue.get('drift', True):   # V1: papel pontilhado deriva devagar (vida sutil em cena parada)
                bgim = ImageChops.offset(bgim, int(t * 10) % 26, int(t * 4) % 26)
            tr = cue.get('trans')
            if tr:
                pin = ease_io(prog(t, 0, tr)) if cue.get('trans_in', True) else 1
                pout = ease_io(prog(t, cue['dur'] - tr, tr)) if cue.get('trans_out', True) else 0
                x0 = int(gfx.W * (1 - pin)); x1 = int(gfx.W * (1 - pout))
                mask = Image.new('L', (gfx.W, gfx.H), 0)
                if x1 > x0:
                    ImageDraw.Draw(mask).rectangle((x0, 0, x1, gfx.H), fill=255)
                    c.paste(bgim, (0, 0), mask)
                if 0 < pin < 1: bands.append((x0 - 14, x0))
                if 0 < pout < 1: bands.append((x1, x1 + 14))
                if pin >= 1 and pout <= 0: mask = None
            else:
                c.alpha_composite(bgim)
    L = gfx.blank() if mask is not None else c
    for el in cue['els']:
        if el['k'] == 'custom':
            import customs
            fn = el['fn'] if callable(el['fn']) else customs.FUNCS[el['fn']]
            gfx.CUR_TAG[0] = 'custom:' + str(el['fn'])
            fn(L, t, cue)
        else:
            draw_el(L, el, t, cue['dur'])
    if mask is not None:   # elementos só existem onde o papel já chegou (sem vazar sobre a câmera)
        L.putalpha(ImageChops.multiply(L.getchannel('A'), mask))
        c.alpha_composite(L)
    d = ImageDraw.Draw(c)
    for a, b in bands:
        d.rectangle((a, 0, b, gfx.H), fill=gfx.ORANGE + (255,))
    if cue.get('iris'):
        import customs
        customs.iris_post(c, t, cue)
    return c
