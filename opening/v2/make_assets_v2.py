"""EP300 · V2 — normaliza os stickers refeitos pelo Gabriel (29/09) em work/v2/assets/stickers/<PESSOA>/NN_estado.png.
Só trata o que precisa: fundo preto -> alpha (flood-fill das bordas; o contorno branco do adesivo separa), recorte de
tiras de 3 rostos, corte das margens transparentes. Rostos NÃO são alterados. PROVENANCE.json ao lado."""
import os, glob, json, shutil
import numpy as np, cv2
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'work', 'v2', 'assets'); ST = os.path.join(OUT, 'stickers'); os.makedirs(ST, exist_ok=True)
SRC = glob.glob('I:/Drives compartilhados/Educa*/Marketing*/01_CANAIS_ATIVOS/02_PODCAST/2026/300_*/01_VIDEO DE ABERTURA/00_ASSETS E INSERTS/stickers e emojis refeitos')[0]
prov = {}

def alpha_from_black(im):
    a = np.array(im.convert('RGB')); h, w = a.shape[:2]
    dark = (a.max(2) < 14).astype(np.uint8)
    ff = dark.copy(); mask = np.zeros((h + 2, w + 2), np.uint8)
    bg = np.zeros((h, w), np.uint8)
    for seed in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        if dark[seed[1], seed[0]]:
            m = np.zeros((h + 2, w + 2), np.uint8); cv2.floodFill(ff.copy(), m, seed, 2, flags=4 | (255 << 8))
            bg |= m[1:-1, 1:-1]
    # regiões escuras conectadas às bordas, inclusive vãos entre rostos (varre todas as componentes escuras que tocam a borda)
    n, lab = cv2.connectedComponents(dark, connectivity=4)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bgm = np.isin(lab, list(edge))
    alpha = np.where(bgm, 0, 255).astype(np.uint8)
    alpha = cv2.GaussianBlur(alpha, (3, 3), 0)
    rgba = np.dstack([a, alpha]); return Image.fromarray(rgba, 'RGBA')

def trim(im, pad=6):
    bb = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    im = im.crop(bb); out = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); out.alpha_composite(im, (pad, pad)); return out

def split3(im):
    a = np.array(im.getchannel('A')) > 40
    cols = a.any(0); segs = []; s = None
    for x, v in enumerate(cols):
        if v and s is None: s = x
        if not v and s is not None:
            if x - s > 60: segs.append((s, x))
            s = None
    if s is not None: segs.append((s, len(cols)))
    return [im.crop((x0, 0, x1, im.height)) for x0, x1 in segs]

def save(person, idx, state, im, src, note):
    d = os.path.join(ST, person); os.makedirs(d, exist_ok=True)
    fn = f'{idx:02d}_{state}.png'; trim(im).save(os.path.join(d, fn))
    prov[f'{person}/{fn}'] = dict(origem=src, tratamento=note)

def load(n):
    return Image.open(os.path.join(SRC, n))

# rostos individuais (RGBA já recortados)
for person, base in (('GUTA', 'Guta_Tolmasquim'), ('LUCAS', 'Lucas_Yokota'), ('VITORIA', 'Vitoria_Comarin')):
    for i, st in ((1, 'natural'), (2, 'reacao'), (3, 'lateral')):
        f = f'{i:02d}_{base}_{st}.png'; save(person, i, st, load(f).convert('RGBA'), f, 'adesivo do Gabriel; só corte de margem')
save('VITORIA', 4, 'sorriso', load('VITORIA_COMARIN-1.png').convert('RGBA'), 'VITORIA_COMARIN-1.png', 'adesivo do Gabriel; só corte de margem')
for i in (1, 2, 3):
    save('MAFE', i, ('sorriso', 'serena', 'lateral')[i - 1], load(f'MAFE_0{i}.png').convert('RGBA'), f'MAFE_0{i}.png', 'adesivo do Gabriel; só corte de margem')
save('PHILLIP', 1, 'sorriso', load('STICKERS PHILLIP MELLO.png').convert('RGBA') if load('STICKERS PHILLIP MELLO.png').mode == 'RGBA' else alpha_from_black(load('STICKERS PHILLIP MELLO.png')),
     'STICKERS PHILLIP MELLO.png', 'fundo preto -> alpha' )
# tiras de 3 rostos
for person, f in (('PHILLIP', 'STICKERS PHILLIP MELLO 2.png'), ('LAYLA', 'STICKERS LAYLA SAYED.png'), ('BONEL', 'STICKERS BONEL.png'), ('BONEL_B', 'STICKERS_BONEL 2.png')):
    im = load(f); im = im if im.mode == 'RGBA' else alpha_from_black(im)
    parts = split3(im); print(f, len(parts))
    for i, p in enumerate(parts[:3]):
        pn = 'BONEL' if person.startswith('BONEL') else person
        off = 10 if person == 'BONEL_B' else (1 if person != 'PHILLIP' else 2)
        save(pn, off + i, ('sorriso', 'surpresa', 'pensando')[i], p, f, 'tira de 3 rostos do Gabriel; fundo -> alpha (se preto) e corte individual')
save('BONEL', 0, 'sorriso_grande', alpha_from_black(load('BONEL_SORRISO.png')), 'BONEL_SORRISO.png', 'fundo preto -> alpha')
# objetos
for name, f in (('balde_pipoca_cheio', 'balde de pipoca com pipocas.png'), ('viatura', 'viatura_sticker.png'), ('pipoca_icone', 'STICKER PIPOCA.png')):
    trim(load(f).convert('RGBA')).save(os.path.join(OUT, name + '.png')); prov[name + '.png'] = dict(origem=f, tratamento='corte de margem')
json.dump(prov, open(os.path.join(ST, 'PROVENANCE.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for p in sorted(glob.glob(ST + '/*/*.png')): print(os.path.relpath(p, OUT), Image.open(p).size)
