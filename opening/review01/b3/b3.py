"""B3 — Review 03: re-render NATIVO (motor V2, 1080p -> 720p com alfa pre-multiplicado) das camadas corrigidas.
Substitui os layers extraidos por matte (MMM/DEZ/VI) e refaz C02_01a (retime pela fala), C02_03 (EP153), C04_03 (balao), C05_01 (17 pessoas), C06_04 (Guta+Lucas).
Uso: python b3.py ID [ID...]   -> ../layers_r03/<ID>.mov + .json
Nota 4K: o motor V2 e 1920x1080 nativo; para o master 4K re-renderizar com este mesmo script ajustando a escala de saida (stickers fonte >=1200 px)."""
import sys, os, json, math, subprocess
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'b2'))
import b2                                   # reutiliza motor V2 + cues B2
from b2 import engine, extra, gfx, place, prog, ease_mid, WHITE, ORANGE, INK2, _txt, FULL_INK, FULL_CREAM, FPS_N, FPS_D, FPS
from b2 import slap, pop, counter, overline, stk, face, PILL_W, PILL_O, ST2
from PIL import Image
import customs
AS = os.path.join(HERE, 'assets'); PEO = os.path.join(AS, 'people')
OUT = os.environ.get('B3_OUT') or os.path.abspath(os.path.join(HERE, '..', 'layers_r03')); os.makedirs(OUT, exist_ok=True)
CREAM = b2.CREAM
CR = dict(bg=list(CREAM), full=True, trans=.3, trans_out=False)       # entra empurrando, sai sem empurrao (a proxima tela cobre)
CR_IO = dict(bg=list(CREAM), full=True, trans=.25)


def evolucao_r3(c, t, cue):
    """'a pergunta foi mudando' — igual a V2, com EP153 trocado (frame com os 4 sorrindo) e cadencia .4 s da Review 02."""
    gfx.place(c, _txt('A PERGUNTA FOI MUDANDO', 30, ORANGE, 'inter', 800, 200), 960, 105, alpha=prog(t, 0, .3))
    items = [(os.path.join(AS, 'hist', 'EP001_2021_b.png'), '2021', 'EP 1'), ('v2/hist/EP073_2022_BIGQUERY.png', '2022', 'EP 73'),
             ('v2/hist/EP100_2023_PLATEIA.png', '2023', 'EP 100 · ao vivo'), (os.path.join(AS, 'hist', 'EP153_2024_r3.png'), '2024', 'EP 153'),
             ('v2/hist/EP210_2025_MERIDIAN.png', '2025', 'EP 210'), ('v2/hist/EP300_2026_HOJE.png', '2026', 'HOJE · EP 300')]
    xs = [262, 533, 804, 1075, 1346, 1617]
    for i, ((img, yr, cap), x) in enumerate(zip(items, xs)):
        at = .05 + i * .4
        if t < at: continue
        y = 540 + (-95 if i % 2 == 0 else 95)
        s, dy, a, dr = engine.enter('slap', t - at)
        big = 1.18 if i == len(items) - 1 else 1.0
        extra.polaroid(c, dict(img=img, w=290, caption=cap, cap=22), t - at, -1, x, y + dy, [-5, 4, -3, 5, -4, 3][i] + dr, s * big, a)
        gfx.place(c, _txt(yr, 48, ORANGE if i < len(items) - 1 else INK2, tracking=-20), x, y - 170 * big + dy, 1, 0, a)


def mural_r3(c, t, cue):
    """quase 200 pessoas / quase 350 vezes / mais de 140 empresas — 17 PESSOAS REAIS distintas (7 da base + 10 novas), nenhuma repetida."""
    out = cue['dur'] - .35
    s2, dy2, a2, _ = engine.leave('up', t - out)
    n2, n3 = 2.8, 5.8
    P = lambda n: os.path.join(PEO, n + '.png')
    S2 = lambda p: os.path.join(gfx.V2A, 'stickers', p)
    swap = {'PHILLIP/02_sorriso.png': 'PHILLIP/04_pensando.png', 'MAFE/01_sorriso.png': 'MAFE/03_lateral.png', 'LAYLA/01_sorriso.png': 'LAYLA/03_pensando.png',
            'BONEL/01_sorriso.png': 'BONEL/00_sorriso_grande.png', 'GUTA/01_natural.png': 'GUTA/02_reacao.png', 'LUCAS/01_natural.png': 'LUCAS/02_reacao.png'}
    old = lambda k: (S2(k), S2(swap.get(k, k)))
    new = lambda k: (P(k + '_1'), P(k + '_2'))
    vit = (S2('VITORIA/04_sorriso.png'), S2('VITORIA/04_sorriso.png'))
    slots = [(old('PHILLIP/02_sorriso.png'), 240, 195, -6), (new('taciana'), 520, 190, 5), (old('GUTA/01_natural.png'), 800, 195, -4),
             (new('rez'), 1120, 190, 6), (vit, 1400, 195, -5), (new('bruno'), 1680, 200, 5),
             (old('BONEL/01_sorriso.png'), 230, 440, 5), (new('marcola'), 520, 440, -6), (new('liana'), 1400, 440, 6), (old('LAYLA/01_sorriso.png'), 1690, 440, -5),
             (new('godoy'), 230, 680, -5), (old('MAFE/01_sorriso.png'), 520, 680, 6), (new('thiago'), 1400, 680, -6), (old('LUCAS/01_natural.png'), 1690, 680, 5),
             (new('gabrielm'), 420, 915, 4), (new('kleber'), 960, 925, -4), (new('lavreca'), 1500, 915, 5)]
    for i, (pair, x, y, r) in enumerate(slots):
        at = .15 + i * .27
        if t < at: continue
        s, dy, a, dr = engine.enter('pop', t - at)
        br = math.sin(2 * math.pi * max(0, t - at) / (2.6 + .3 * (i % 4)))
        p = pair[1] if t > n3 - .3 + (i % 3) * .1 else pair[0]
        extra.stk(c, dict(path=p, size=225), t - at, -1, x, y + dy2, r + 1.5 * br + dr, s * (1 + .015 * (br + 1)), a * a2)
    seq = [(0.0, 200, 'QUASE', 'PESSOAS'), (n2, 350, 'QUASE', 'VEZES'), (n3, 140, 'MAIS DE', 'EMPRESAS')]
    cur = [x for x in seq if t >= x[0]][-1]; lt = t - cur[0]
    v = int(cur[1] * ease_mid(prog(lt, .05, .9)))
    num = _txt(str(v), 250, WHITE, tracking=-40)
    s, dy, a, dr = engine.enter('slap', lt)
    place(c, _txt(cur[2], 40, ORANGE, 'inter', 800, 250), 960, 395 + dy2, alpha=prog(lt, 0, .3) * a2)
    place(c, gfx.hard_shadow(num, (9, 12), ORANGE, .95), 960, 535 + dy2, s, -3, a * a2)
    place(c, _txt(cur[3], 44, WHITE, 'inter', 800, 250), 960, 695 + dy2, alpha=prog(lt, .2, .3) * a2)
    if cur[3] == 'PESSOAS':
        place(c, _txt('SENTARAM NESSA MESA', 28, (190, 190, 190), 'inter', 800, 200), 960, 765 + dy2, alpha=prog(t, .8, .3) * a2)


customs.FUNCS.update(evolucao_r3=evolucao_r3, mural_r3=mural_r3)

c403 = dict(b2.CUES['C04_03']); c403['els'] = [dict(e) for e in c403['els']]
for e in c403['els']:
    if e.get('k') == 'balloon': e.update(x=690, y=475)          # rabicho (embaixo-esquerda) cai sobre a cabeca do Gustavo
    if e.get('k') == 'stk' and 'gustavo' in e.get('path', ''): e.update(x=372, y=700)
c403['notes'] = 'R03: balao "O diamante negro..." reposicionado — o rabicho aponta para o Gustavo (quem fala).'

PURPLE = 'patrocinadores/purple-metrics.webp'
P = lambda n: os.path.join(PEO, n + '.png')
CUES = {
    'C02_01a': dict(dur=14.55, alpha=True, els=[
        overline(0, 'DE ONDE VEM', 960, 110, size=30),
        dict(k='tl_axis', at=.2, x0=160, x1=1760, y=560, anim='none', draw=1.2, nodes=[(260, '2015', .66), (620, 'PRIME', 3.9), (980, 'MB TALKS', 5.0)]),
        pop(.66, 'stamp', 260, 380, rot=-6, lines=['2015'], size=80, anim='stamp'),
        pop(3.9, 'stamp', 620, 390, rot=4, lines=['MB PRIME'], size=50, anim='stamp', fill=ORANGE),
        pop(5.0, 'label', 980, 380, rot=-3, lines=['“MB Talks”'], size=46),
        pop(6.5, 'label', 980, 735, rot=3, lines=['2 pessoas + 1 pergunta', 'por semana'], size=40),
        face(7.4, 'gustavo', 800, 895, size=190, rot=7, state='still'),
        dict(k='stk', at=7.7, path='personagens/lucian/still.webp', x=1160, y=895, size=190, rot=-8, anim='pop', states=[(2.2, 'personagens/lucian/arraste-final.webp')]),
    ], sfx=[(.66, 'SFX_SYN_thump.wav')], notes='R03: V2 C02_01 re-renderizada NATIVA e re-temporizada pela fala (2015@62.4, Prime@65.6, MB Talks@66.6, duas pessoas@68.1) e SEGURADA ate "dia 4" (75.7); A VOLTA/PODCAST ficam no S01.', **CR),
    'C02_03': dict(dur=4.5, alpha=True, els=[dict(k='custom', fn='evolucao_r3')], sfx=[(.45, 'SFX_SYN_pop.wav'), (.85, 'SFX_SYN_pop.wav'), (1.25, 'SFX_SYN_pop.wav'), (1.65, 'SFX_SYN_pop.wav'), (2.05, 'SFX_SYN_pop.wav'), (2.3, 'SFX_SYN_thump.wav')],
                   notes='R03: EP153 trocado (frame 133.5 s do MATERIAL COMPLETO: 4 pessoas sorrindo); demais prints iguais a R02.', **CR),
    'C04_03': dict(c403, alpha=False),
    'C05_01': dict(dur=7.0, alpha=False, els=[dict(k='custom', fn='mural_r3')], sfx=[(0.0, 'SFX_SYN_tickup0.95.wav'), (2.8, 'SFX_SYN_tickup0.95.wav'), (5.8, 'SFX_SYN_tickup0.95.wav')],
                   placeholders=[], notes='R03: 17 pessoas reais distintas (Phill, Mafe, Guta, Lucas, Vitoria, Layla, Bonel + Kleber, Taciana, Godoy, Rez, Marcola, Gabriel Mineiro, Bruno, Thiago Cruz, Lavreca, Liana); zero placeholder.', **FULL_INK),
    'C06_03_MMM': dict(dur=2.0, alpha=True, els=[
        dict(k='tl_axis', at=0, x0=140, x1=1780, y=520, anim='none', draw=.01, nodes=[(960, 'OUT 2024', 0)]),
        pop(.1, 'label', 960, 330, rot=-3, lines=['episódio inteiro', 'sobre MMM'], size=38)], sfx=[], notes='R03: re-render nativo (sem matte).', **CR_IO),
    'C06_05_DEZ': dict(dur=3.0, alpha=True, els=[
        dict(k='tl_axis', at=0, x0=140, x1=1780, y=520, anim='none', draw=.01, nodes=[(960, 'DEZ 2024', 0)]),
        pop(.1, 'label', 960, 330, rot=-2, lines=['“vai dar pra conversar', 'com os dados”'], size=34)], sfx=[], notes='R03: re-render nativo (sem matte).', **CR_IO),
    'C06_03_VI': dict(dur=2.586, alpha=True, els=[
        dict(k='stk_fx', at=0, path=ST2 + 'VITORIA/02_reacao.png', x=230, y=800, size=240, rot=-6, out=2.2, anim='slap'),
        pop(.2, 'pill', 470, 900, rot=-4, text='desculpa, Vi.', emoji='🙏', size=30, out=2.2, **PILL_W)], sfx=[], bg=None, notes='R03: re-render nativo (sem matte); sticker da Vitoria + pill.'),
    'C06_04': dict(dur=1.92, alpha=True, els=[
        pop(.05, 'asset', 330, 150, rot=-3, path=PURPLE, size=300, anim='slap'),
        pop(.25, 'pill', 770, 175, rot=4, text='de nada', emoji='👋', size=30, **PILL_W),
        dict(k='stk', at=.3, path=P('01_Guta_Tolmasquim_natural'), x=230, y=790, size=300, rot=-6, anim='pop', states=[(.8, P('02_Guta_Tolmasquim_reacao'))]),
        pop(.5, 'pill', 230, 975, rot=-3, text='Guta', size=28, **PILL_W),
        dict(k='stk', at=.5, path=P('01_Lucas_Yokota_natural'), x=1690, y=790, size=300, rot=6, anim='pop', states=[(.9, P('03_Lucas_Yokota_lateral'))]),
        pop(.7, 'pill', 1690, 975, rot=3, text='Lucas', size=28, **PILL_W)], sfx=[], placeholders=[],
        notes='R03: Purple Metrics + Guta Tolmasquim (esq.) e Lucas Yokota (dir.), stickers reais fornecidos; sem translate.', bg=None),
}


OW, OH = (int(os.environ.get('B3_W', 1280)), int(os.environ.get('B3_H', 720)))


def to720(im):
    return im.convert('RGBa').resize((OW, OH), Image.LANCZOS).convert('RGBA')


def render(cid):
    C = CUES[cid]; dur = C['dur']; n = round(dur * FPS)
    cu = dict(id=cid, name=cid, dur=dur, els=C['els'], bg=C.get('bg'), full=bool(C.get('bg')) and C.get('full', False))
    for k in ('trans', 'trans_out'):
        if k in C: cu[k] = C[k]
    mov = os.path.join(OUT, cid + '.mov')
    alpha = C['alpha']
    enc = (['-pix_fmt', 'rgba'], ['-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le']) if alpha else (['-pix_fmt', 'rgb24'], ['-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le'])
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo'] + enc[0] + ['-s', f'{OW}x{OH}', '-r', f'{FPS_N}/{FPS_D}', '-i', '-', '-frames:v', str(n)] + enc[1] + ['-r', f'{FPS_N}/{FPS_D}', mov], stdin=subprocess.PIPE)
    for i in range(n):
        t = i * FPS_D / FPS_N
        fr = to720(engine.render_frame(cu, t))
        if not alpha:
            bgc = Image.new('RGBA', fr.size, tuple(C['bg']) + (255,)); bgc.alpha_composite(fr); p.stdin.write(bgc.convert('RGB').tobytes())
        else:
            p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()
    side = dict(id=cid, dur_s=dur, frames=n, kind='alpha' if alpha else 'opaque', sfx=[dict(file=f, t=round(t, 3)) for t, f in C['sfx']], placeholders=C.get('placeholders', []), notes=C.get('notes', ''))
    json.dump(side, open(os.path.join(OUT, cid + '.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    return cid, n


if __name__ == '__main__':
    ids = sys.argv[1:] or list(CUES)
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=4) as ex:
        for r in ex.map(render, ids): print(r, flush=True)
