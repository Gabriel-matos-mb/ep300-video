"""EP300 · V2 — artes ORIGINAIS desenhadas para gags (sem reproduzir personagem/marca de terceiros):
 - carton de achocolatado ("TODDYNHO" só como texto, arte própria) com selo GA4  -> gag "o GA4 era esse todinho todo?"
 - silhueta de pica-pau (pássaro genérico, crista vermelha) + telefone  -> gag "se o Pica-Pau tivesse chamado a polícia"
 - tile Amplitude (wordmark) no formato dos logos"""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'work', 'v2', 'assets'); os.makedirs(OUT, exist_ok=True)
SORA = os.path.join(HERE, 'fonts', 'Sora-VariableFont_wght.ttf')
def font(sz, w=800):
    f = ImageFont.truetype(SORA, sz)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
INK = (18, 18, 19); S = 3

def carton():
    W, H = 360 * S, 520 * S; im = Image.new('RGBA', (W + 40 * S, H + 40 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ox, oy = 20 * S, 20 * S; w, h = 320 * S, 400 * S
    top = [(ox + 20 * S, oy + 100 * S), (ox + w / 2, oy), (ox + w - 20 * S, oy + 100 * S)]
    d.polygon([(ox + 10 * S + 6 * S, oy + 110 * S), (ox + w / 2, oy + 6 * S), (ox + w - 16 * S, oy + 110 * S)], fill=(214, 178, 140), outline=INK)
    d.rounded_rectangle((ox, oy + 100 * S, ox + w, oy + h + 100 * S), radius=14 * S, fill=(96, 52, 32), outline=INK, width=6 * S)
    d.polygon([(ox + w / 2 - 40 * S, oy + 4 * S), (ox + w / 2 + 40 * S, oy + 4 * S), (ox + w / 2 + 34 * S, oy + 60 * S), (ox + w / 2 - 34 * S, oy + 60 * S)], fill=(230, 200, 160), outline=INK)
    d.rounded_rectangle((ox + 20 * S, oy + 170 * S, ox + w - 20 * S, oy + 250 * S), radius=14 * S, fill=(255, 235, 200), outline=INK, width=4 * S)
    t = 'TODDYNHO'; f = font(int(37 * S), 800)
    tw = d.textlength(t, font=f); d.text((ox + w / 2 - tw / 2, oy + 190 * S), t, font=f, fill=(96, 52, 32))
    # respingo de leite
    d.ellipse((ox + 30 * S, oy + 280 * S, ox + 120 * S, oy + 330 * S), fill=(255, 245, 230))
    d.ellipse((ox + 90 * S, oy + 300 * S, ox + 150 * S, oy + 345 * S), fill=(255, 245, 230))
    # selo GA4 (o gag)
    cx, cy, r = ox + w - 95 * S, oy + 350 * S, 62 * S
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(227, 116, 0), outline=INK, width=5 * S)
    f2 = font(int(46 * S), 800); tw = d.textlength('GA4', font=f2); d.text((cx - tw / 2, cy - 30 * S), 'GA4', font=f2, fill=(255, 255, 255))
    # canudo
    d.line((ox + w - 70 * S, oy + 10 * S, ox + w - 30 * S, oy - 5 * S), fill=(244, 115, 64), width=9 * S)
    return im.resize((im.width // S, im.height // S), Image.LANCZOS)

def woodpecker():
    W = 520 * S; im = Image.new('RGBA', (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(im); K = (28, 28, 34)
    d.rounded_rectangle((300 * S, 40 * S, 420 * S, 500 * S), radius=16 * S, fill=(120, 80, 50))        # tronco
    d.ellipse((150 * S, 200 * S, 360 * S, 430 * S), fill=K)                                               # corpo
    d.polygon([(250 * S, 380 * S), (330 * S, 500 * S), (270 * S, 510 * S), (200 * S, 410 * S)], fill=K)   # cauda
    d.ellipse((120 * S, 110 * S, 250 * S, 240 * S), fill=K)                                               # cabeça
    d.polygon([(122 * S, 160 * S), (30 * S, 175 * S), (124 * S, 195 * S)], fill=(240, 190, 70))           # bico
    for i, (dx, dy) in enumerate([(0, 0), (22, -8), (44, -4)]):                                            # crista
        d.polygon([(150 * S + dx * S, 118 * S), (176 * S + dx * S, 118 * S), (190 * S + dx * S, 60 * S + dy * S)], fill=(214, 40, 40))
    d.ellipse((148 * S, 145 * S, 172 * S, 169 * S), fill=(255, 255, 255)); d.ellipse((153 * S, 150 * S, 166 * S, 163 * S), fill=K)
    d.ellipse((190 * S, 250 * S, 320 * S, 380 * S), fill=(245, 245, 245))                                 # peito claro
    return im.resize((W // S, W // S), Image.LANCZOS)

def amplitude_tile(size=600):
    from PIL import ImageFilter
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im); pad = int(size * .06); r = int(size * .2); k = int(size * .04)
    d.rounded_rectangle((pad + k, pad + k, size - pad, size - pad), radius=r, fill=INK)
    d.rounded_rectangle((pad, pad, size - pad - k, size - pad - k), radius=r, fill=(255, 255, 255), outline=INK, width=int(size * .018))
    f = font(int(size * .118), 800); t = 'amplitude'; tw = d.textlength(t, font=f)
    d.text(((size - k) / 2 - tw / 2, size * .44), t, font=f, fill=(30, 97, 240))
    # onda
    import math
    pts = [(size * .22 + i * size * .56 / 60, size * .30 + math.sin(i / 60 * 2 * math.pi * 1.5) * size * .05) for i in range(61)]
    d.line(pts, fill=(30, 97, 240), width=int(size * .022), joint='curve')
    return im

carton().save(os.path.join(OUT, 'gag_toddynho_ga4.png')); woodpecker().save(os.path.join(OUT, 'gag_picapau_silhueta.png'))
os.makedirs(os.path.join(OUT, 'logos'), exist_ok=True); amplitude_tile().save(os.path.join(OUT, 'logos', 'amplitude.png'))
import shutil, glob
for f in glob.glob(os.path.join(HERE, '..', 'work', 'v2', 'logos', 'png', '*.png')): shutil.copy(f, os.path.join(OUT, 'logos', os.path.basename(f)))
print('ok')
