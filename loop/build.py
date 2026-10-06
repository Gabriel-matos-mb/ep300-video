"""EP300 · Loop do telão — renderizador. Lê scene.json (manifesto) + assets/ e gera o MP4.
Uso:  python build.py                 # render completo -> out/EP300_LOOP_V0_PROXY.mp4
      python build.py --frame 12.5    # PNG de um instante (out/frame_12.50.png)
      python build.py --contact       # folha de contato (out/contact.jpg)
Tudo é função periódica/de keyframes que volta ao estado-base => loop perfeito por construção (60 s)."""
import json, math, os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, 'scene.json'), encoding='utf-8'))
W, H, FPS, DUR = S['canvas']['w'], S['canvas']['h'], S['canvas']['fps'], S['canvas']['duration']
N = int(round(FPS * DUR))
OUT = os.path.join(HERE, 'out'); os.makedirs(OUT, exist_ok=True)


def hexc(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


INK, ORANGE, WHITE = (hexc(S['palette'][k]) for k in ('ink', 'orange', 'white'))


def P(p): return os.path.normpath(os.path.join(HERE, p))


def font(size, w=800):
    f = ImageFont.truetype(P(S['fonts']['sora']), size); f.set_variation_by_axes([w]); return f


def load(p): return Image.open(P(p)).convert('RGBA')


def trim(im):
    b = im.getbbox(); return im.crop(b) if b else im


def fit_h(im, h): return im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS)


def fit_box(im, bw, bh):
    r = min(bw / im.width, bh / im.height)
    return im.resize((max(1, round(im.width * r)), max(1, round(im.height * r))), Image.LANCZOS)


def shadow(im, dy=10, blur=14, a=0.55, pad=40):
    canvas = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    al = Image.new('L', canvas.size, 0); al.paste(im.getchannel('A'), (pad, pad + dy))
    al = al.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * a))
    sh = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); sh.putalpha(al)
    canvas.alpha_composite(sh); canvas.alpha_composite(im, (pad, pad)); return canvas


def sticker_text(text, size, fill, ring, w=800):
    f = font(size, w); l, t, r, b = f.getbbox(text, stroke_width=ring)
    pad = ring + 6; im = Image.new('RGBA', (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im); pos = (pad - l, pad - t)
    d.text(pos, text, font=f, fill=WHITE + (255,), stroke_width=ring, stroke_fill=WHITE + (255,))
    d.text(pos, text, font=f, fill=fill + (255,))
    return im


def rounded_card(path, w, bright, border=7, radius=16):
    im = load(path); h = round(w * im.height / im.width)
    im = im.resize((w - 2 * border, h - 2 * border), Image.LANCZOS)
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius - 5, fill=255)
    card = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle((0, 0, w - 1, h - 1), radius, fill=WHITE + (255,))
    card.paste(im.convert('RGB'), (border, border), m)
    arr = np.asarray(card).astype(np.float32); arr[..., :3] *= bright
    return shadow(Image.fromarray(arr.clip(0, 255).astype(np.uint8), 'RGBA'), dy=12, blur=16, a=0.6)


# ---------- transform com sub-pixel (evita jitter em movimentos lentos) ----------
def place(canvas, sprite, cx, cy, scale=1.0, rot=0.0, alpha=1.0, pm=None):
    """sprite RGBA no tamanho nominal; pm = versão pré-multiplicada (RGBa) em cache."""
    if alpha <= 0.003: return
    sw, sh = sprite.size
    th = math.radians(rot); c, s = math.cos(th), math.sin(th)
    hw, hh = sw * scale / 2, sh * scale / 2
    ex = abs(hw * c) + abs(hh * s); ey = abs(hw * s) + abs(hh * c)
    x0, y0 = int(math.floor(cx - ex)) - 1, int(math.floor(cy - ey)) - 1
    ow, oh = int(math.ceil(2 * ex)) + 3, int(math.ceil(2 * ey)) + 3
    ux, uy = x0 - cx, y0 - cy
    a, b = c / scale, s / scale
    d, e = -s / scale, c / scale
    cc = a * ux + b * uy + sw / 2
    ff = d * ux + e * uy + sh / 2
    src = pm if pm is not None else sprite.convert('RGBa')
    out = src.transform((ow, oh), Image.AFFINE, (a, b, cc, d, e, ff), resample=Image.BICUBIC).convert('RGBA')
    if alpha < 0.999: out.putalpha(out.getchannel('A').point(lambda v: int(v * alpha)))
    sx, sy = max(0, -x0), max(0, -y0); ex2, ey2 = min(ow, W - x0), min(oh, H - y0)
    if ex2 > sx and ey2 > sy: canvas.alpha_composite(out.crop((sx, sy, ex2, ey2)), (x0 + sx, y0 + sy))


def ss(x):
    x = min(1, max(0, x)); return x * x * x * (x * (x * 6 - 15) + 10)


def track(keys, t):
    if t <= keys[0][0]: return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1: return v0 + (v1 - v0) * ss((t - t0) / (t1 - t0)) if t1 > t0 else v1
    return keys[-1][1]


def state_weights(keys, t, fade=0.3):
    """[[t,estado]...] -> {estado: peso} com crossfade de `fade` s na troca."""
    cur = keys[0][1]; prev = cur; ts = -1e9
    for tk, st in keys:
        if tk <= t:
            if st != cur: prev, cur, ts = cur, st, tk
        else: break
    k = ss((t - ts) / fade)
    return {cur: k, prev: 1 - k} if prev != cur and k < 1 else {cur: 1.0}


def make_pill(text, size):
    f = font(size, 700); l, t, r, b = f.getbbox(text)
    tri = int(size * 0.75); padx, pady, gap = 34, 18, 16
    w = padx * 2 + tri + gap + (r - l); h = (b - t) + pady * 2
    ring = 6; im = Image.new('RGBA', (w + 2 * ring, h + 2 * ring), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w + 2 * ring - 1, h + 2 * ring - 1), (h + 2 * ring) // 2, fill=WHITE + (255,))
    d.rounded_rectangle((ring, ring, ring + w - 1, ring + h - 1), h // 2, fill=ORANGE + (255,), outline=INK + (255,), width=3)
    tx = ring + padx; cy = ring + h // 2
    d.polygon([(tx, cy - tri // 2), (tx, cy + tri // 2), (tx + int(tri * .9), cy)], fill=INK + (255,))
    d.text((tx + tri + gap - l, ring + pady - t), text, font=f, fill=INK + (255,))
    return shadow(im, 8, 10, .5)


def make_sponsors():
    """Grupos modulares (scene.json > sponsors.groups): cada grupo = rótulo + logos. Logo nunca é rotacionado/deformado
    (só reduzido proporcionalmente para caber na caixa). Grupos com "provisorio": true são só marcação editorial."""
    sp = S['sponsors']; lf = font(sp['label_size'], 700); gap = sp['gap']; div = sp.get('divider', 64)
    groups = []
    for g in sp['groups']:
        imgs = []
        for lg in g['logos']:
            f, box = (lg, g.get('logo_box', sp['logo_box'])) if isinstance(lg, str) else (lg['file'], lg.get('box', g.get('logo_box', sp['logo_box'])))
            imgs.append(fit_box(trim(load(f)), box[0], box[1]))
        w = sum(i.width for i in imgs) + gap * (len(imgs) - 1)
        groups.append((g, imgs, w))
    total = sum(w for _, _, w in groups) + div * (len(groups) - 1)
    bh = sp['row_h']
    im = Image.new('RGBA', (total + 40, 34 + bh + 6), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x = 20
    def lab(txt, x0, w):
        tw = sum(d.textlength(ch, font=lf) + 3 for ch in txt) - 3
        xx = x0 + (w - tw) / 2
        for ch in txt:
            d.text((xx, 0), ch, font=lf, fill=(175, 175, 178, 255)); xx += d.textlength(ch, font=lf) + 3
    for gi, (g, imgs, w) in enumerate(groups):
        lab(g['label'], x, w); xx = x
        for i in imgs:
            im.alpha_composite(i, (xx, 34 + (bh - i.height) // 2)); xx += i.width + gap
        x += w
        if gi < len(groups) - 1:
            d.line((x + div // 2, 40, x + div // 2, 34 + bh - 6), fill=(90, 90, 94, 255), width=2); x += div
    return im


def build_static():
    st = {}
    im = Image.new('RGB', (W + 40, H + 40), INK); d = ImageDraw.Draw(im); dot = hexc(S['palette']['dots'])
    for y in range(0, H + 40, 20):
        for x in range(0, W + 40, 20): d.ellipse((x, y, x + 2, y + 2), fill=dot)
    st['bg'] = np.asarray(im)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - 960) / 610) ** 2 + ((yy - 520) / 430) ** 2)
    a = 0.86 * np.clip(1 - (r - 0.55) / 0.85, 0, 1) ** 1.3
    a = np.maximum(a, 0.93 * np.clip((yy - 850) / 110, 0, 1))
    a = np.maximum(a, 0.28 * np.clip(np.sqrt(((xx - 960) / 1250) ** 2 + ((yy - 540) / 760) ** 2) - 0.55, 0, 1) * 2.2)
    sc = np.zeros((H, W, 4), np.uint8); sc[..., :3] = INK; sc[..., 3] = (a.clip(0, 1) * 255).astype(np.uint8)
    st['scrim'] = Image.fromarray(sc, 'RGBA')
    st['cards'] = []
    for i, c in enumerate(S['collage']['cards']):
        base = rounded_card(c['file'], c['w'], c['bright']); hi = None
        for sp in S['collage']['spotlights']:
            if sp['card'] == i: hi = rounded_card(c['file'], c['w'], min(1.0, c['bright'] + sp['lift_bright']))
        if c.get('alt'): hi = rounded_card(c['alt'], c['w'], c['bright'])
        st['cards'].append((base, base.convert('RGBa'), hi, hi.convert('RGBa') if hi else None))
    T = S['title']
    st['ep'] = shadow(sticker_text(T['episodio']['text'], T['episodio']['size'], hexc(T['episodio']['color']), 9), 8, 10, .5)
    st['num'] = shadow(sticker_text(T['numero']['text'], T['numero']['size'], hexc(T['numero']['color']), 20), 16, 20, .6)
    st['logo'] = shadow(fit_h(trim(load(T['logo']['file'])), T['logo']['h']), 8, 10, .5)
    st['pill'] = make_pill(T['frase']['text'], T['frase']['size']) if 'frase' in T else None
    st['sponsors'] = make_sponsors()
    st['actors'] = []
    for a in S['actors']:
        spr = {}
        for name, path in a['states'].items():
            im = trim(load(path)); r = a['size'] / max(im.size)
            spr[name] = shadow(im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS), 10, 12, .55)
        wmax = max(s.width for s in spr.values()); hmax = max(s.height for s in spr.values())
        for k, im in spr.items():   # mesmo canvas p/ todos os estados: trocar PNG não desloca o rosto
            c = Image.new('RGBA', (wmax, hmax), (0, 0, 0, 0)); c.alpha_composite(im, ((wmax - im.width) // 2, (hmax - im.height) // 2)); spr[k] = c
        st['actors'].append({k: (v, v.convert('RGBa')) for k, v in spr.items()})
    st['props'] = []
    for p in S['props']:
        im = trim(load(p['file'])); r = p['size'] / max(im.size)
        im = shadow(im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS), 8, 10, .5)
        st['props'].append((im, im.convert('RGBa')))
    return st


def frame(st, t):
    drift = int(round((t / DUR) * S['background']['dot_drift_px_per_loop'])) % 20
    cv = Image.fromarray(np.ascontiguousarray(st['bg'][drift:drift + H, drift:drift + W]), 'RGB').convert('RGBA')
    cb = S['background']
    breath = 1 + cb['collage_breath'] * math.sin(2 * math.pi * t / cb['collage_breath_period'])
    for i, c in enumerate(S['collage']['cards']):
        base_i, pm, hi, hipm = st['cards'][i]
        ph = 2 * math.pi * (t / c['period'] + c['phase']); amp = 6 + 16 * c['depth']
        dx, dy = amp * math.cos(ph), amp * 0.6 * math.sin(ph)
        cx = 960 + (c['cx'] - 960) * breath + dx; cy = 540 + (c['cy'] - 540) * breath + dy
        rot = c['rot'] + 0.8 * math.sin(ph + 1.0); sc = breath; sp = 0
        for spl in S['collage']['spotlights']:
            if spl['card'] == i:
                sp = track(spl['keys'], t); sc *= 1 + spl['lift_scale'] * sp
        place(cv, base_i, cx, cy, sc, rot, 1.0, pm)
        if hi is not None and c.get('alt_keys'):   # troca lenta: dissolve A→B→A (max com t+DUR = costura circular)
            sp = max(track(c['alt_keys'], t), track(c['alt_keys'], t + DUR))
        if hi is not None and sp > 0: place(cv, hi, cx, cy, sc, rot, sp, hipm)
    cv.alpha_composite(st['scrim'])
    T = S['title']; n = T['numero']
    place(cv, st['ep'], T['episodio']['cx'], T['episodio']['cy'])
    sway = n['rot'] + n['sway_deg'] * math.sin(2 * math.pi * t / n['sway_period'])
    nb = 1 + n['breath'] * math.sin(2 * math.pi * t / n['breath_period'])
    place(cv, st['num'], n['cx'], n['cy'], nb, sway)
    L = T['logo']; place(cv, st['logo'], L['cx'], L['cy'], 1.0, L['rot'])
    if st['pill'] is not None: F = T['frase']; place(cv, st['pill'], F['cx'], F['cy'])
    for a, spr in zip(S['actors'], st['actors']):
        pres = track(a['presence'], t)
        if pres <= 0.002: continue
        sc = (0.55 + 0.45 * pres) * (1 + a['breath'] * math.sin(2 * math.pi * t / a['breath_period']))
        rot = a['rot'] + 1.2 * math.sin(2 * math.pi * t / a['breath_period'] + 0.7) + (1 - pres) * (-10 if a['rot'] < 0 else 10)
        cy = a['cy'] + (1 - pres) * 40 + (track(a['dy'], t) if 'dy' in a else 0)
        cx = a['cx'] + (track(a['dx'], t) if 'dx' in a else 0)
        if 'rot_extra' in a: rot += track(a['rot_extra'], t)
        for stt, w in state_weights(a['state'], t).items():
            place(cv, spr[stt][0], cx, cy, sc, rot, pres * w, spr[stt][1])
    for p, (im, pm) in zip(S['props'], st['props']):
        pres = track(p['presence'], t)
        if pres <= 0.002: continue
        hop = track(p['hop'], t) if 'hop' in p else 0
        px = track(p['x_keys'], t) if 'x_keys' in p else p['cx']
        py = track(p['y_keys'], t) if 'y_keys' in p else p['cy'] + (1 - pres) * 30
        pr = track(p['rot_keys'], t) if 'rot_keys' in p else p['rot']
        ps = track(p['scale_keys'], t) if 'scale_keys' in p else (0.6 + 0.4 * pres)
        place(cv, im, px, py - 16 * hop, ps * (1 + 0.04 * hop), pr + 3 * hop, pres, pm)
    sp_im = st['sponsors']
    cv.alpha_composite(sp_im, (960 - sp_im.width // 2, S['sponsors']['y'] - 34))
    return cv.convert('RGB')


_ST = None


def _init():
    global _ST; _ST = build_static()


def _job(i): return frame(_ST, i / FPS).tobytes()


def render():
    st = build_static(); path = os.path.join(OUT, S['output']['name'] + '.mp4')
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-c:v', 'libx264', '-preset', 'slow', '-crf', str(S['output']['crf']), '-pix_fmt', 'yuv420p', '-g', str(FPS * 2),
           '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-movflags', '+faststart', '-an', path]
    import multiprocessing as mp
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with mp.Pool(int(os.environ.get('BUILD_WORKERS', max(1, (os.cpu_count() or 2) // 2))), initializer=_init) as pool:
        for i, raw in enumerate(pool.imap(_job, range(N), chunksize=6)):
            p.stdin.write(raw)
            if i % 150 == 0: print(f'{i}/{N}', flush=True)
    p.stdin.close(); p.wait(); print('ok', path)


if __name__ == '__main__':
    if '--frame' in sys.argv:
        t = float(sys.argv[sys.argv.index('--frame') + 1]); st = build_static()
        frame(st, t).save(os.path.join(OUT, f'frame_{t:05.2f}.png'))
    elif '--contact' in sys.argv:
        st = build_static(); ts = [0, 15, 17, 34, 55, 56.5, 59, 75, 97, 100, 110, 119.9]
        sheet = Image.new('RGB', (640 * 3, 360 * 4))
        for k, t in enumerate(ts): sheet.paste(frame(st, t).resize((640, 360), Image.LANCZOS), ((k % 3) * 640, (k // 3) * 360))
        sheet.save(os.path.join(OUT, 'contact.jpg'), quality=88)
    else:
        render()
