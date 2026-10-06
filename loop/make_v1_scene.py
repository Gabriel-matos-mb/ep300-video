"""EP300 LOOP V1 — prepara assets do mosaico (acervo real, ~55 imagens) e GERA scene.json da V1.
Rodar só quando quiser re-sortear o mosaico / reescrever a timeline base (o scene.json resultante é o arquivo editável).
Fontes (só o que já está no acervo, busca dirigida): thumbs oficiais EP260–289 e prints do estúdio principal
(I:\\...\\02_PODCAST\\2026\\NNN_*\\04_THUMB*/04_PRINTS), EP126 e prints do estúdio azul (assets/thumbs já existentes)."""
import json, os, random, shutil
from PIL import Image, ImageDraw, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

HERE = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.join(HERE, 'work', 'cand')
MOS = os.path.join(HERE, 'assets', 'mosaic'); os.makedirs(MOS, exist_ok=True)
DUR = 120.0

pick = json.load(open(os.path.join(CAND, 'pick.json'), encoding='utf-8'))          # ep -> thumb oficial 1920x1080
sel2 = json.load(open(os.path.join(CAND, 'sel2.json'), encoding='utf-8'))          # [ep, print]


def small(src, dst, w=640, q=88):
    im = Image.open(src).convert('RGB'); im = im.resize((w, round(w * im.height / im.width)), Image.LANCZOS)
    im.save(dst, quality=q); return os.path.relpath(dst, HERE).replace('\\', '/')


# ---------- pools ----------
T = {}   # thumbs oficiais (cenário-neutro, convidados diversos)
for ep, p in pick.items():
    ep = int(ep)
    if not p or ep in (254, 256, 278, 290, 292): continue
    T[ep] = small(p, os.path.join(MOS, f't_EP{ep}.jpg'))
byep = {}
for ep, p in sel2: byep.setdefault(int(ep), []).append(p)
SP_BLUE = {282, 283, 284, 286, 288}
P, P2, B = {}, {}, {}
for ep, ps in byep.items():
    if ep in SP_BLUE:
        B[ep] = small(ps[0], os.path.join(MOS, f'b_EP{ep}.jpg'))
    else:
        P[ep] = small(ps[0], os.path.join(MOS, f'p_EP{ep}_a.jpg'))
        if len(ps) > 1: P2[ep] = small(ps[1], os.path.join(MOS, f'p_EP{ep}_b.jpg'))
R = {}
for n in ('f_duo', 'f_guest'):                                                     # EP126 (Rio, parede de tijolo)
    R[n] = small(os.path.join(HERE, 'assets', 'thumbs', n + '.png'), os.path.join(MOS, f'r_{n}.jpg'))
# azul (SP) limitado a 3 — parte do acervo, não a identidade
blue_keep = [B[k] for k in (282, 283, 286) if k in B]
print('thumbs', len(T), 'prints estúdio principal', len(P), '(alt', len(P2), ') EP126', len(R), 'azul', len(blue_keep))

# ---------- layout do mosaico ----------
rng = random.Random(300)
cells = []
CW, CH = 205, 128
for gy in range(-1, 10):
    for gx in range(-1, 11):
        x = gx * CW + CW / 2 + rng.uniform(-60, 60); y = gy * CH + CH / 2 + rng.uniform(-38, 38)
        if ((x - 960) / 500) ** 2 + ((y - 500) / 340) ** 2 < 1: continue      # miolo do 300 fica limpo
        if 520 < x < 1400 and y > 890: continue                              # faixa dos patrocinadores fica limpa
        if rng.random() < 0.07: continue                                     # respiros
        cells.append((x, y))
rng.shuffle(cells)
pool = [('T', v) for v in T.values()] + [('P', v) for v in P.values()] + [('R', v) for v in R.values()] + [('B', v) for v in blue_keep]
rng.shuffle(pool)
cards = []
placed = []   # (x,y,cat,file)


def near(x, y, r=340): return [q for q in placed if (q[0] - x) ** 2 + (q[1] - y) ** 2 < r * r]


FULL = list(pool)
for (x, y) in cells:
    if not pool:                     # acervo acabou: recicla imagens (o filtro abaixo impede repetição por perto)
        pool = list(FULL); rng.shuffle(pool)
    # escolhe a 1ª imagem cuja categoria/episódio não repete nos vizinhos
    choice = None
    for i, (cat, f) in enumerate(pool):
        nb = near(x, y)
        if cat in ('B', 'R') and any(q[2] in ('B', 'R') for q in nb): continue
        if sum(1 for q in nb if q[2] == cat) >= 2: continue
        if any(q[3] == f for q in near(x, y, 720)): continue
        choice = i; break
    if choice is None: choice = 0
    cat, f = pool.pop(choice)
    r = rng.random()
    layer = 'far' if r < 0.42 else ('mid' if r < 0.80 else 'near')
    if abs(x - 960) < 560 and abs(y - 500) < 420: layer = 'far' if r < 0.6 else 'mid'   # perto do centro nunca "near"
    w, br, dp = {'far': (rng.randint(170, 215), rng.uniform(0.17, 0.24), rng.uniform(0.2, 0.35)),
                 'mid': (rng.randint(230, 290), rng.uniform(0.23, 0.30), rng.uniform(0.45, 0.65)),
                 'near': (rng.randint(320, 380), rng.uniform(0.27, 0.34), rng.uniform(0.8, 0.95))}[layer]
    placed.append((x, y, cat, f))
    cards.append(dict(file=f, cx=round(x), cy=round(y), w=w, rot=round(rng.uniform(-7, 7), 1), depth=round(dp, 2), bright=round(br, 2),
                      period=rng.choice([30, 60, 60, 120]), phase=round(rng.random(), 2), _cat=cat))
# troca lenta: ~16 cartões ganham "alt" (imagem B que dissolve por cima, depois volta)
alts_p2 = list(P2.values()); alts_t = list(T.values()); rng.shuffle(alts_p2); rng.shuffle(alts_t)
cand_idx = [i for i, c in enumerate(cards) if c['w'] < 300]        # troca nos cartões menores/de fundo
rng.shuffle(cand_idx)
starts = [4, 12, 21, 30, 38, 47, 55, 63, 72, 80, 88, 96, 104, 111, 116, 26]
for k, i in enumerate(cand_idx[:len(starts)]):
    c = cards[i]
    c['alt'] = alts_p2.pop() if c['_cat'] == 'T' and alts_p2 else alts_t.pop()
    t0 = starts[k]; hold = rng.choice([22, 26, 30, 34])
    c['alt_keys'] = [[t0, 0], [t0 + 10, 1], [t0 + 10 + hold, 1], [t0 + 20 + hold, 0]]     # pode passar de 120: costura circular no build
for c in cards: c.pop('_cat')
print('cartões', len(cards), 'com troca', sum(1 for c in cards if 'alt' in c))

# ---------- cursor (asset gerado, substituível) ----------
os.makedirs(os.path.join(HERE, 'assets', 'fx'), exist_ok=True)
S4 = 4; pts = [(0, 0), (0, 33), (8, 25), (14, 38), (20, 35), (14, 23), (25, 23)]
im = Image.new('RGBA', (34 * S4, 46 * S4), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
big = [(x * S4 + 4 * S4, y * S4 + 4 * S4) for x, y in pts]
d.polygon(big, fill=(255, 255, 255, 255)); d.line(big + [big[0]], fill=(255, 255, 255, 255), width=5 * S4, joint='curve')
inner = [(x * S4 + 4 * S4, y * S4 + 4 * S4) for x, y in pts]
d.polygon(inner, fill=(18, 18, 19, 255))
im.resize((34 * 3, 46 * 3), Image.LANCZOS).save(os.path.join(HERE, 'assets', 'fx', 'cursor.png'))

# ---------- logo oficial Métricas Boss (SVG do repo -> PNG; sem alteração de proporção) ----------
brand = os.path.join(HERE, 'assets', 'brand')
svg_src = os.path.join(HERE, '..', '..', 'remotion-mb', 'public', 'logo-mb-branca.svg')
shutil.copy2(svg_src, os.path.join(brand, 'logo-metricas-boss-branca.svg'))
try:
    import resvg_py
    b = resvg_py.svg_to_bytes(svg_string=open(svg_src, encoding='utf-8').read(), width=1086)
    open(os.path.join(brand, 'logo-metricas-boss-branca.png'), 'wb').write(bytes(b))
except Exception as e:
    print('resvg_py indisponível — usando PNG já existente', e)

# ---------- timeline dos atores / microgags ----------
def A(**k): return k
gustavo = dict(id='gustavo', _doc='estados: troque o PNG de cada estado sem mexer na timeline. base=still · smile=hover-transicao · surprise=hover-final · glance=arraste-final (olhar de lado / bochecha puxada)',
    states={'base': 'assets/stickers/gustavo/still.webp', 'smile': 'assets/stickers/gustavo/hover-transicao.webp',
            'surprise': 'assets/stickers/gustavo/hover-final.webp', 'glance': 'assets/stickers/gustavo/arraste-final.webp'},
    cx=355, cy=520, size=270, rot=-7, breath=0.02, breath_period=3.0,
    presence=[[0, 0], [13.9, 0], [14.0, 1], [22.1, 1], [22.2, 0], [100.0, 0], [101.4, 1], [110.4, 1], [111.8, 0], [120, 0]],
    dx=[[0, -640], [14, -640], [16.6, -310], [21.0, -310], [22.0, -640], [22.2, -640], [99.5, 1200], [104.4, 1200], [105.1, 1130], [111.8, 1130], [112.0, -640], [120, -640]],
    dy=[[0, 130], [22.2, 130], [99.5, 0], [120, 0]],
    rot_extra=[[0, 22], [22.2, 22], [99.5, 0], [104.4, 0], [104.8, -9], [106.0, 0], [120, 0]],
    state=[[0, 'base'], [17.0, 'base'], [17.3, 'glance'], [20.0, 'glance'], [20.4, 'base'],
           [104.5, 'base'], [104.8, 'glance'], [107.8, 'glance'], [108.1, 'base']])
lucian = dict(id='lucian',
    states={'base': 'assets/stickers/lucian/still.webp', 'smile': 'assets/stickers/lucian/hover-transicao.webp',
            'surprise': 'assets/stickers/lucian/hover-final.webp', 'glance': 'assets/stickers/lucian/arraste-final.webp'},
    cx=1565, cy=520, size=270, rot=7, breath=0.02, breath_period=3.0,
    presence=[[0, 0], [42.0, 0], [43.3, 1], [52.6, 1], [53.9, 0], [74.0, 0], [75.3, 1], [84.6, 1], [85.4, 0],
              [102.9, 0], [103.5, 1], [109.2, 1], [110.8, 0], [120, 0]],
    dx=[[0, 0], [79.6, 0], [85.0, 640], [85.4, 640], [86.0, 760], [103.0, 760], [105.0, 175], [109.2, 175], [111.0, 760], [119, 0], [120, 0]],
    rot_extra=[[0, 0], [79.3, 0], [80.6, 12], [85.0, 16], [86.0, 0], [102.9, 0], [103.0, -12], [105.0, 0], [120, 0]],
    state=[[0, 'base'], [45.5, 'base'], [45.8, 'surprise'], [47.3, 'surprise'], [47.7, 'smile'], [49.6, 'smile'], [50.0, 'base'],
           [79.3, 'base'], [79.6, 'glance'], [85.4, 'glance'], [85.8, 'base'],
           [105.1, 'base'], [105.4, 'smile'], [108.6, 'smile'], [109.0, 'base']])
pipoca = dict(id='pipoca', file='assets/stickers/pipoca.png', cx=1650, cy=720, size=150, rot=8,
              presence=[[0, 0], [44.4, 0], [45.8, 1], [50.6, 1], [51.9, 0], [120, 0]],
              hop=[[46.2, 0.0], [46.6, 1.0], [47.1, 0.0]])
cursor = dict(id='cursor', file='assets/fx/cursor.png', size=92, cx=0, cy=0, rot=0,
              presence=[[0, 0], [76.6, 0], [77.2, 1], [84.8, 1], [85.2, 0], [120, 0]],
              x_keys=[[0, 1990], [76.6, 1990], [79.4, 1517], [79.6, 1517], [85.0, 2157], [85.4, 2157], [120, 1990]],
              y_keys=[[0, 1130], [76.6, 1130], [79.4, 602], [79.6, 602], [82.0, 596], [85.0, 610], [120, 1130]],
              scale_keys=[[0, 1], [79.4, 1], [79.7, 0.86], [85.0, 0.86], [85.4, 1], [120, 1]])

scene = dict(
    _doc='EP300 LOOP V1 — manifesto editável. ASSET VISUAL ≠ LÓGICA DE ANIMAÇÃO: troque arquivos em assets/ (mesmo nome) ou os caminhos aqui; as timelines (presence/state/dx/…) não dependem do PNG. '
         'Este arquivo foi gerado por make_v1_scene.py mas é o arquivo de trabalho: edite à mão à vontade.',
    canvas=dict(w=1920, h=1080, fps=30, duration=DUR),
    palette=dict(ink='#121213', dots='#232325', orange='#F47340', white='#FFFFFF'),
    background=dict(dot_drift_px_per_loop=20, collage_breath=0.010, collage_breath_period=20.0),
    fonts=dict(sora='fonts/Sora-VariableFont_wght.ttf'),
    collage=dict(_doc='cx,cy,w = centro/largura (px); rot graus; depth 0..1 (parallax); bright 0..1; period (s, divisor de 120); alt = imagem que dissolve por cima (alt_keys: [t,0..1], pode passar de 120 = costura circular)',
                 cards=cards, spotlights=[]),
    title=dict(episodio=dict(text='EPISÓDIO', size=62, cx=960, cy=232, color='#F47340'),
               numero=dict(text='300', size=410, cx=960, cy=472, color='#121213', rot=-3, sway_deg=0.7, sway_period=12.0, breath=0.012, breath_period=10.0),
               logo=dict(file='assets/brand/selo-analytics-talks.webp', h=205, cx=960, cy=752, rot=0)),
    sponsors=dict(_doc='PROVISÓRIO até o Gabriel confirmar naming/logos finais. Grupos modulares: troque/ordene logos em groups[].logos. Logo da Métricas Boss = asset oficial, NUNCA rotacionar/inclinar/esticar (o motor só reduz proporcionalmente).',
                  y=958, label_size=20, logo_box=[170, 62], row_h=64, gap=30, divider=70,
                  groups=[dict(label='PATROCÍNIO OFICIAL', provisorio=True, nota='Purple Metrics (naming/logo final a confirmar — "Corpo/Purple Metrics"); Onfly (pode mudar naming/logo)',
                               logos=[dict(file='assets/sponsors/purple-metrics.webp', box=[170, 62]), dict(file='assets/sponsors/onfly.webp', box=[160, 50])]),
                          dict(label='CAFÉ OFICIAL', provisorio=False, nota='Coffee++ conforme asset disponível', logos=[dict(file='assets/sponsors/coffee-plusplus.webp', box=[130, 62])]),
                          dict(label='REALIZAÇÃO', provisorio=False, nota='Métricas Boss — asset oficial (logo-mb-branca.svg do repo)', logos=[dict(file='assets/brand/logo-metricas-boss-branca.png', box=[190, 54])])]),
    actors=[gustavo, lucian], props=[pipoca, cursor],
    output=dict(name='EP300_LOOP_V1_PROXY', crf=20))


def dump(o, ind=0):
    """json compacto legível: dicts multi-linha, listas de números/pares em 1 linha, cartões 1 por linha."""
    sp = '  ' * ind
    if isinstance(o, dict):
        if all(not isinstance(v, (dict, list)) or (isinstance(v, list) and all(not isinstance(x, (dict, list)) or (isinstance(x, list) and all(not isinstance(y, (list, dict)) for y in x)) for x in v)) for v in o.values()) and len(json.dumps(o, ensure_ascii=False)) < 260:
            return json.dumps(o, ensure_ascii=False)
        items = [f'{sp}  {json.dumps(k, ensure_ascii=False)}: {dump(v, ind + 1)}' for k, v in o.items()]
        return '{\n' + ',\n'.join(items) + f'\n{sp}}}'
    if isinstance(o, list):
        if all(not isinstance(x, (dict,)) for x in o):
            return json.dumps(o, ensure_ascii=False)
        return '[\n' + ',\n'.join(f'{sp}  {dump(x, ind + 1)}' for x in o) + f'\n{sp}]'
    return json.dumps(o, ensure_ascii=False)


open(os.path.join(HERE, 'scene.json'), 'w', encoding='utf-8').write(dump(scene) + '\n')
print('scene.json escrito')
