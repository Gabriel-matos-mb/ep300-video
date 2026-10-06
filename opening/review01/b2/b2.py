"""B2 — re-render de 7 overlays V2 (ADAPT) para a V4_PRESENTABLE_REVIEW_01.
Usa o motor da V2 (../../v2, só leitura) com cues redefinidos aqui. Saída: ../layers/<id>.mov + .json (1280x720, 23.976, ProRes 422 HQ opaco).
Uso: python b2.py C03_01 [C04_01 ...]   (sem argumentos = todos, em paralelo)
"""
import sys, os, json, math, subprocess, functools
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.abspath(os.path.join(HERE, '..', '..', 'v2'))
sys.path.insert(0, V2)
import gfx, engine, extra, extra_v2, customs, customs_v2   # noqa
from PIL import Image, ImageDraw
from gfx import place, prog, ease_out, ease_io, ease_mid, CREAM, ORANGE, INK, INK2, WHITE
from customs import _txt
import plan
from plan import slap, pop, counter, overline, stk, face, cue, PILL_W, PILL_O, ST2

FPS_N, FPS_D = 24000, 1001
FPS = FPS_N / FPS_D
OUT = os.path.abspath(os.path.join(HERE, '..', 'layers'))
AS = os.path.join(HERE, 'assets')
FLAGS = 'C:/Users/gabri/Code/audio-visual/experiments/hyperframes/ep300-countries-benchmark/assets'
FULL_INK = dict(bg=list(INK), full=True)       # sem 'trans': camada opaca desde o 1º quadro
FULL_CREAM = dict(bg=list(CREAM), full=True)


# ------------------------------------------------------------------ cenas custom
def bordao_v4(c, t, cue):
    """200+ 'Fala aí': parede de prints de várias épocas (sem EP288) + contador 200+."""
    out = cue['dur'] - .3
    s2, dy2, a2, _ = engine.leave('up', t - out)
    place(c, _txt('O BORDÃO DO GUSTAVO', 30, ORANGE, 'inter', 800, 200), 960, 90, alpha=prog(t, 0, .3) * a2)
    B = lambda n: os.path.join(AS, 'bordao', n + '.png')
    P = lambda n: 'v1/prints/' + n + '.png'
    H = lambda n: 'v2/hist/' + n + '.png'
    items = [  # (img, caption, x, y, rot, crop)   crop corta a tarja/rótulo do rodapé
        (B('EP061'), 'EP 61', 180, 250, -6, (0, 0, 1, .9)), (B('EP073'), 'EP 73', 500, 235, 4, (0, 0, 1, .9)),
        (B('EP121'), 'EP 121', 820, 255, -3, (0, 0, 1, .9)), (B('EP126'), 'EP 126', 1140, 240, 5, (0, 0, 1, .9)),
        (B('EP146'), 'EP 146', 1460, 255, -5, (0, 0, 1, .9)), (B('EP149'), 'EP 149', 1760, 245, 4, (0, 0, 1, .9)),
        (P('EP282_GUSTAVO_LUCIAN'), 'EP 282', 170, 800, 5, None), (P('EP284_GUSTAVO_LUCIAN'), 'EP 284', 490, 815, -4, None),
        (B('EP183'), 'EP 183', 810, 800, 3, (0, 0, 1, .9)), (B('EP197'), 'EP 197', 1130, 815, -5, (0, 0, 1, .9)),
        (B('EP206'), 'EP 206', 1450, 800, 4, (0, 0, 1, .9)), (P('EP286_GUSTAVO_LUCIAN'), 'EP 286', 1760, 815, -3, None),
        (H('EP100_2023_PLATEIA'), 'EP 100 · ao vivo', 235, 540, 3, None), (H('EP210_2025_MERIDIAN'), 'EP 210', 1685, 540, -4, (0, 0, 1, .82)),
    ]
    imgs = {it[1]: it for it in items}
    slots = [(it[2], it[3], it[4]) for it in items]
    arr = ['EP 61', 'EP 146', 'EP 282', 'EP 126', 'EP 197', 'EP 286', 'EP 121', 'EP 284', 'EP 149', 'EP 210', 'EP 73', 'EP 183', 'EP 100 · ao vivo', 'EP 206']
    items = [(imgs[n][0], n, sl[0], sl[1], sl[2], imgs[n][5]) for n, sl in zip(arr, slots)]
    order = [6, 0, 11, 5, 3, 9, 1, 8, 4, 10, 2, 7, 12, 13]     # entrada alternada pelos cantos
    for k, i in enumerate(order):
        pth, cap, x, y, r, crop = items[i]
        at = .12 + k * .09
        if t < at: continue
        s, dy, a, dr = engine.enter('slap', t - at)
        el = dict(img=pth, w=290, caption=cap, cap=20)
        if crop: el['crop'] = list(crop)
        extra.polaroid(c, el, t - at, -1, x, y + dy2, r + dr, s, a * a2)
    n = int(1 + 199 * ease_mid(prog(t, .1, .85)))
    txt = '200+' if n >= 200 else f'{n}'
    cnt = _txt(txt, 270, ORANGE, tracking=-40)
    place(c, gfx.hard_shadow(cnt, (9, 11), (0, 0, 0), .3), 960, 520 + dy2, 1, -4, prog(t, .1, .2) * a2)
    place(c, _txt('VEZES', 36, INK2, 'inter', 800, 250), 960, 650 + dy2, alpha=prog(t, 1.0, .3) * a2)
    if t > 2.1:
        lab = engine.build_img('label', (('lines', ('“Fala aí, analítica e analítico de plantão!”',)), ('size', 40)))
        s, dy, a, dr = engine.enter('pop', t - 2.1)
        place(c, lab, 960, 975 + dy2, s, 2, a * a2)


STK = lambda p: ST2 + p


def mural_v4(c, t, cue):
    """quase 200 pessoas / quase 350 vezes / mais de 140 empresas — MULTIDÃO de rostos (stickers + prints), sem ranking."""
    out = cue['dur'] - .35
    s2, dy2, a2, _ = engine.leave('up', t - out)
    n2, n3 = 2.8, 5.8
    # (arquivo, x, y, rot, size) — 20 posições em anel, miolo livre para o número
    PH = os.path.join(AS, 'placeholder_person.png')   # PLACEHOLDER_PERSON_STICKER: só há 7 pessoas distintas aprovadas
    people = [
        ('PHILLIP/02_sorriso.png', 240, 200, -6), ('MAFE/01_sorriso.png', 520, 190, 5), ('GUTA/01_natural.png', 800, 195, -4),
        ('LUCAS/01_natural.png', 1120, 190, 6), ('VITORIA/04_sorriso.png', 1400, 195, -5), ('LAYLA/01_sorriso.png', 1680, 200, 5),
        ('BONEL/01_sorriso.png', 230, 440, 5), (PH, 520, 440, -6), (PH, 1400, 440, 6),
        (PH, 1690, 440, -5), (PH, 230, 680, -5), (PH, 520, 680, 6),
        (PH, 1400, 680, -6), (PH, 1690, 680, 5), (PH, 250, 890, 4),
        (PH, 800, 890, -5), (PH, 1120, 890, 5), (PH, 1680, 890, -4),
    ]
    swap = {'PHILLIP/02_sorriso.png': 'PHILLIP/04_pensando.png', 'MAFE/01_sorriso.png': 'MAFE/03_lateral.png',
            'LAYLA/01_sorriso.png': 'LAYLA/03_pensando.png', 'BONEL/01_sorriso.png': 'BONEL/00_sorriso_grande.png',
            'GUTA/01_natural.png': 'GUTA/02_reacao.png', 'LUCAS/01_natural.png': 'LUCAS/02_reacao.png'}
    prints = [('v1/prints/EP282_CONVIDADA.png', 'EP 282', 660, 540, -4), ('v1/prints/EP286_CONVIDADOS.png', 'EP 286', 1260, 540, 4)]
    seq_t = [0.15 + i * .26 for i in range(len(people))]       # 0.15 .. ~4.6: a sala vai enchendo
    for i, (pth, x, y, r) in enumerate(people):
        at = seq_t[i]
        if t < at: continue
        s, dy, a, dr = engine.enter('pop', t - at)
        br = math.sin(2 * math.pi * max(0, t - at) / (2.6 + .3 * (i % 4)))
        p = pth
        if pth in swap and t > n3 - .3 + (i % 3) * .1: p = swap[pth]
        extra.stk(c, dict(path=(p if os.path.isabs(p) else STK(p)), size=225), t - at, -1, x, y + dy2, r + 1.5 * br + dr, s * (1 + .015 * (br + 1)), a * a2)
    for i, (pth, cap, x, y, r) in enumerate(prints):
        pass   # prints no miolo competem com o número: ficam fora (multidão só nas bordas)
    seq = [(0.0, 200, 'QUASE', 'PESSOAS'), (n2, 350, 'QUASE', 'VEZES'), (n3, 140, 'MAIS DE', 'EMPRESAS')]
    cur = [x for x in seq if t >= x[0]][-1]
    lt = t - cur[0]
    v = int(cur[1] * ease_mid(prog(lt, .05, .9)))
    num = _txt(str(v), 250, WHITE, tracking=-40)
    s, dy, a, dr = engine.enter('slap', lt)
    place(c, _txt(cur[2], 40, ORANGE, 'inter', 800, 250), 960, 395 + dy2, alpha=prog(lt, 0, .3) * a2)
    place(c, gfx.hard_shadow(num, (9, 12), ORANGE, .95), 960, 535 + dy2, s, -3, a * a2)
    place(c, _txt(cur[3], 44, WHITE, 'inter', 800, 250), 960, 695 + dy2, alpha=prog(lt, .2, .3) * a2)
    if cur[3] == 'PESSOAS':
        place(c, _txt('SENTARAM NESSA MESA', 28, (190, 190, 190), 'inter', 800, 200), 960, 760 + dy2, alpha=prog(t, .8, .3) * a2)


@functools.lru_cache(maxsize=80)
def _flag(name, px):
    im = Image.open(os.path.join(FLAGS, 'flags', name + '.png')).convert('RGBA').resize((px, px), Image.LANCZOS)
    return gfx.soft_shadow(im, (0, 5), 8, .45)


def flags_v4(c, t, cue):
    """'MAIS DE 100 PAÍSES': nuvem das 60 bandeiras oficiais (layout Print 11) em reveal progressivo — 6 heróis, depois o resto em stagger."""
    out = cue['dur'] - .3
    s2, dy2, a2, _ = engine.leave('up', t - out)
    L = json.load(open(os.path.join(FLAGS, 'flags_layout.json'), encoding='utf8'))
    K = 1.8; X0, Y0 = 852, 114
    rest = sorted(range(6, len(L)), key=lambda i: L[i]['y'] + L[i]['x'] * .35)
    ts = {}
    for i in range(6): ts[i] = .1 + i * .09
    for k, i in enumerate(rest): ts[i] = .6 + k * (1.7 / len(rest))
    for i, f in enumerate(L):
        lt = t - ts[i]
        if lt < 0: continue
        p = prog(lt, 0, .34)
        sc = .0 + engine.pop_soft(p) if hasattr(engine, 'pop_soft') else gfx.pop_soft(p)
        bob = 3 * math.sin(2 * math.pi * (t * .9 + i * .13)) if t > 2.2 else 0
        px = max(2, int(f['s'] * K * 256 / 256))
        cx = X0 + (f['x'] + f['s'] / 2) * K; cy = Y0 + (f['y'] + f['s'] / 2) * K + bob + dy2
        place(c, _flag(f['n'], px), cx, cy, max(.01, gfx.pop_soft(p)), f['r'] * (1 - .0) + (-14 * (1 - p)), min(1, p * 3) * a2)
    # manchete à esquerda
    lt = t - .05
    place(c, _txt('MAIS DE', 46, WHITE, 'inter', 800, 250), 450, 330 + dy2, alpha=prog(lt, 0, .3) * a2)
    v = int(100 * ease_mid(prog(t, .2, .8)))
    pulse = 1 + .07 * math.sin(math.pi * prog(t, 2.25, .25)) if t > 2.25 else 1
    s, dy, a, dr = engine.enter('slap', t - .2)
    num = _txt(str(v), 330, WHITE, tracking=-40)
    place(c, gfx.hard_shadow(num, (10, 13), ORANGE, .95), 450, 500 + dy2, s * pulse, -3, a * a2)
    place(c, _txt('PAÍSES', 120, ORANGE, 'sora', 800, -20), 450, 700 + dy2, alpha=prog(t, .9, .3) * a2)


customs.FUNCS.update(bordao_v4=bordao_v4, mural_v4=mural_v4, flags_v4=flags_v4)

# ------------------------------------------------------------------ cues (tempos relativos ao início do layer, s)
REP = os.path.join(AS, 'reportei_tile.png')
LG = [('googleanalytics', 190, 420), ('googletagmanager', 410, 420), ('googlebigquery', 190, 640), ('looker', 410, 640),
      ('powerbi', 190, 860), ('amplitude', 410, 860), ('googleads', 1510, 420), ('meta', 1730, 420), ('hotjar', 1510, 640),
      ('googlesearchconsole', 1730, 640), ('google', 1510, 860), ('REPORTEI', 1730, 860)]
ROTS_L = [-6, 5, 4, -5, -4, 6, 5, -6, -4, 6, 5, -5]
c03 = [overline(0, 'NO COMEÇO, QUASE TUDO ERA', 960, 110, color=WHITE, size=28),
       slap(1.3, 'ferramenta', 110, 960, 230, color=ORANGE, emoji='🔧')]
for i, (n, x, y) in enumerate(LG):
    path = REP if n == 'REPORTEI' else f'v2/logos/{n}.png'
    c03.append(pop(1.9 + i * .14, 'logo', x, y, path=path, size=190, rot=ROTS_L[i], sway=2.6 + .1 * (i % 6)))
c03 += [pop(2.5, 'label', 960, 470, rot=-4, lines=['Como instalar?'], size=52),
        pop(3.3, 'label', 960, 590, rot=3, lines=['Como taguear?'], size=52),
        pop(4.0, 'label', 960, 760, rot=-2, lines=['Por que o número do relatório', 'não bate com o do financeiro?'], size=40),
        pop(8.0, 'stamp', 960, 920, rot=-8, lines=['ATÉ HOJE'], size=64, anim='stamp', fill=ORANGE)]

CUES = {
    'C03_01': dict(dur=10.3, els=c03, sfx=[(8.0, 'SFX_SYN_thump.wav')], kind='opaque', **FULL_INK,
                   notes='V2 comprimido de 12,6 s p/ 10,3 s; Reportei em tile branco igual aos demais (wordmark sem recorte, não redesenhado).'),
    'C04_01': dict(dur=3.9, els=[dict(k='custom', fn='bordao_v4')], sfx=[(0.0, 'MA_Amenteramco_Whoosh_Pass-By_1.wav'), (0.1, 'SFX_SYN_tickup2.6.wav')],
                   kind='opaque', **FULL_CREAM,
                   notes='Contador 200+; 14 polaroids de épocas diferentes (EP61–EP286), sem EP288/EP187; 6 frames novos extraídos do BORDAO_SUPERCUT (só frames, rodapé cortado).'),
    'C04_03': dict(dur=3.6, els=[
        counter(.1, 60, 210, 960, 190, color=WHITE, fmt='{}+', cdur=.7),
        overline(.3, 'JEITOS DE APRESENTAR O LUCIAN', 960, 310, color=WHITE, size=24),
        stk(.4, 'personagens/gustavo/hover-final.webp', 340, 720, size=300, rot=6, breath=2.4),
        dict(k='balloon', at=.6, text='O diamante negro do Analytics!', size=40, x=560, y=470, tail='left', anim='pop', rot=-3),
        face(.5, 'lucian', 1580, 720, size=300, rot=-6, state='still', breath=2.9),
        pop(.9, 'label', 980, 600, rot=-4, lines=['“Super choque do analítico”'], sub='EP 205', size=32),
        pop(1.3, 'label', 1000, 720, rot=3, lines=['“CTO and Black Diamond”'], sub='EP 256', size=32),
        pop(1.7, 'label', 960, 840, rot=-2, lines=['“O cara pra quem o GTM pede bênção”'], sub='EP 270', size=30),
        pop(2.1, 'label', 1000, 960, rot=4, lines=['“Cebola: bota as tags pra chorar”'], sub='EP 69', size=30),
    ], sfx=[(0.1, 'SFX_SYN_tickup1.0.wav')], kind='opaque', **FULL_INK, notes='60+ (era 16); Lucian = sticker still (sorrindo), não o olhar de lado.'),
    'C04_06': dict(dur=13.0, els=[
        overline(0, 'FRASE CLÁSSICA DO LUCIAN', 960, 120, size=28),
        pop(.5, 'stamp', 350, 400, rot=7, lines=['24×'], size=130, anim='stamp'),
        pop(3.0, 'label', 960, 570, rot=-2, lines=['“Se o Pica-Pau tivesse', 'chamado a polícia, nada', 'disso teria acontecido.”'], size=48),
        pop(5.0, 'asset', 1490, 800, rot=-3, path='v2/viatura.png', size=330, anim='fromR', sway=1.6),
        face(6.6, 'lucian', 380, 800, size=240, rot=-7, state='still'),
        face(7.0, 'gustavo', 700, 830, size=220, rot=6, state='hover-final'),
        pop(11.2, 'pill', 1000, 960, rot=3, text='tem gente que nem sabe a referência', emoji='🤷', size=32, **PILL_W),
    ], sfx=[(.5, 'SFX_SYN_thump.wav'), (5.0, 'MA_Amenteramco_Whoosh_Pass-By_1.wav')], kind='opaque', **FULL_CREAM,
        placeholders=['PLACEHOLDER_R21_PICAPAU_NEW_STICKER (pássaro e balão removidos: sticker novo não localizado)'],
        notes='Retime p/ a passada longa (125.1–138.1); pill "tem gente que nem sabe a referência" em tl ~136.3. Pica-Pau = silhueta antiga (sticker novo do Gabriel não localizado).'),
    'C05_04': dict(dur=5.6, els=[
        pop(0, 'label', 560, 220, rot=3, lines=['“Se o Pica-Pau tivesse', 'chamado a polícia…”'], size=40),
        pop(1.6, 'stamp', 560, 420, rot=-6, lines=['NÓS CHAMAMOS'], size=64, anim='stamp', fill=ORANGE),
        dict(k='polaroid', at=2.9, img='v1/ep126/f_guest.png', w=560, caption='EP 126 · Inovação e Dados na PMERJ', cap=24, x=1360, y=380, rot=4, anim='slap'),
        dict(k='polaroid', at=3.5, img='v1/ep126/f_duo.png', w=480, x=700, y=780, rot=-5, anim='slap'),
        pop(3.8, 'asset', 1500, 800, rot=-3, path='v2/viatura.png', size=320, anim='fromR', sway=1.6),
    ], sfx=[(1.6, 'SFX_SYN_thump.wav'), (2.9, 'MA_Amenteramco_Whoosh_Pass-By_1.wav'), (3.8, 'MA_Amenteramco_Whoosh_Pass-By_1.wav')], kind='opaque', **FULL_CREAM,
        placeholders=['frame EP126 trocado (olhos abertos, t=1.0 s do making-off); PLACEHOLDER_R23 resolvido'],
        notes='C05_04 refeito no motor V2: frame vizinho do mesmo EP126 com olhos abertos.'),
    'C05_01': dict(dur=7.0, els=[dict(k='custom', fn='mural_v4')], sfx=[(0.0, 'SFX_SYN_tickup0.95.wav'), (2.8, 'SFX_SYN_tickup0.95.wav'), (5.8, 'SFX_SYN_tickup0.95.wav')],
                   kind='opaque', placeholders=['PLACEHOLDER_PERSON_STICKER x11 (só 7 pessoas distintas aprovadas: Phill, Mafê, Guta, Lucas, Vitória, Layla, Bonel)'], **FULL_INK, notes='quase 200 / quase 350 / mais de 140; 7 pessoas distintas + 11 placeholders em anel (multidão), sem prints de convidado remoto (EP187 fora), sem ranking.'),
    'C06_07': dict(dur=8.1, els=[
        overline(0, 'E AÍ…', 960, 90, size=28),
        pop(1.2, 'stamp', 520, 330, rot=-6, lines=['FEV 2026'], size=70, anim='stamp', fill=ORANGE),
        face(3.1, 'lucian', 1400, 420, size=300, rot=-7, state='still'),
        pop(3.4, 'pill', 1400, 640, rot=4, text='“NÃO DAVA PRA FAZER”', size=34, **PILL_W),
        pop(4.9, 'stamp', 1300, 860, rot=-8, lines=['ACERTOU'], size=80, anim='stamp', fill=ORANGE),
        pop(6.0, 'stamp', 520, 640, rot=5, lines=['JUN 2026', 'LANÇAMOS O', 'ANALYTICS COPILOT'], size=44, anim='stamp'),
    ], sfx=[(1.2, 'SFX_SYN_thump.wav'), (4.9, 'SFX_SYN_thump.wav')], kind='opaque', **FULL_CREAM,
        notes='Carimbo "IA NA HOME DO GA" removido; "IMPOSSÍVEL" -> "NÃO DAVA PRA FAZER"; ordem reordenada para seguir a fala (fev, não dava, fiz=ACERTOU, jun/Copilot).'),
    'C07_04': dict(dur=3.6, els=[dict(k='custom', fn='flags_v4')], sfx=[(0.0, 'SFX_SYN_pop.wav')], kind='opaque', **FULL_INK,
                   notes='MAIS DE 100 PAÍSES; 60 bandeiras oficiais (Print 11, wavy c/ contorno branco como nos assets oficiais — não quadradas) em reveal progressivo; layout cloud Print 11 à direita, manchete à esquerda; fundo tinta V2. Benchmark HF não reaproveitado como MP4.'),
}


def render(cid):
    C = CUES[cid]; dur = C['dur']
    n = round(dur * FPS)
    cu = dict(id=cid, name=cid, dur=dur, els=C['els'], bg=C['bg'], full=True)
    mov = os.path.join(OUT, cid + '.mov')
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080',
                          '-r', f'{FPS_N}/{FPS_D}', '-i', '-', '-vf', 'scale=1280:720:flags=lanczos', '-frames:v', str(n),
                          '-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le', '-r', f'{FPS_N}/{FPS_D}', mov],
                         stdin=subprocess.PIPE)
    for i in range(n):
        t = i * FPS_D / FPS_N
        fr = engine.render_frame(cu, t)
        bgc = Image.new('RGBA', fr.size, tuple(C['bg']) + (255,)); bgc.alpha_composite(fr)
        p.stdin.write(bgc.convert('RGB').tobytes())
    p.stdin.close(); p.wait()
    side = dict(id=cid, dur_s=dur, frames=n, kind=C['kind'], sfx=[dict(file=f, t=round(t, 3)) for t, f in C['sfx']],
                placeholders=C.get('placeholders', []), notes=C.get('notes', ''))
    json.dump(side, open(os.path.join(OUT, cid + '.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    return cid, n


if __name__ == '__main__':
    ids = sys.argv[1:] or list(CUES)
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=4) as ex:
        for r in ex.map(render, ids): print(r, flush=True)
