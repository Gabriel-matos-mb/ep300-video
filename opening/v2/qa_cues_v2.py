"""EP300 · V2 — QA por cue: contact sheet de quadros amostrados + checagem de SAFE AREA (bbox de tudo que é colado via place()).
Uso: python qa_cues_v2.py C03_01 [C03_02 ...]   |   python qa_cues_v2.py --safe   (todas as cues, relatório em work/v2/qa/safe_report.json)"""
import os, sys, json, glob
sys.stdout.reconfigure(encoding='utf-8')
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
SAFE = (90, 54, 1830, 1026)      # 4,7 % lateral / 5 % vertical — conservador para cinema
QA = os.path.join(HERE, '..', 'work', 'v2', 'qa'); os.makedirs(QA, exist_ok=True)


def _load():
    import build, engine, customs, gfx
    build.load_freezes(); return build, engine, gfx


def sheet(cid, n=8):
    build, engine, gfx = _load()
    c = next(x for x in build.timeline()['cues'] if x['id'] == cid)
    dur = (c.get('nfr') or round(c['dur'] * 30)) / 30
    ts = [min(dur - .05, .3 + i * (dur - .4) / (n - 1)) for i in range(n)]
    bgc = Image.new('RGB', (480 * 4, 270 * ((n + 3) // 4)), (90, 90, 90))
    for i, t in enumerate(ts):
        im = engine.render_frame(c, t); base = Image.new('RGB', im.size, (70, 110, 70)); base.paste(im, (0, 0), im)
        d = ImageDraw.Draw(base); d.rectangle(SAFE, outline=(255, 0, 255), width=3)
        base.thumbnail((480, 270)); bgc.paste(base, ((i % 4) * 480, (i // 4) * 270))
        ImageDraw.Draw(bgc).text(((i % 4) * 480 + 6, (i // 4) * 270 + 4), f'{cid} t={t:.2f}', fill=(255, 255, 0))
    p = os.path.join(QA, f'sheet_{cid}.jpg'); bgc.save(p, quality=82); return p


def safe_one(cid):
    build, engine, gfx = _load()
    c = next(x for x in build.timeline()['cues'] if x['id'] == cid)
    dur = (c.get('nfr') or round(c['dur'] * 30)) / 30
    viol = {}
    t = 0.2
    while t < dur - .1:
        gfx.SAFE_LOG = []
        engine.render_frame(c, t)
        for x0, y0, x1, y1, tag in gfx.SAFE_LOG:
            if x1 - x0 > 1700 or y1 - y0 > 1000: continue        # fundos/quadros inteiros
            if '~slide' in (tag or '') or 'push' in (tag or ''): continue   # elementos em deslize de página (intencional)
            out = max(SAFE[0] - x0, SAFE[1] - y0, x1 - SAFE[2], y1 - SAFE[3])
            tol = 6 if '~enter' not in (tag or '') else 90
            if '~fall' in (tag or '') or 'custom:question_rain' in (tag or ''): continue
            if out > tol:
                k = tag or '?'
                if k not in viol or out > viol[k][0]: viol[k] = (int(out), round(t, 2), [int(x0), int(y0), int(x1), int(y1)])
        t += .25
    gfx.SAFE_LOG = None
    return cid, viol


if __name__ == '__main__':
    args = sys.argv[1:]
    if '--safe' in args:
        import build
        ids = [c['id'] for c in build.timeline()['cues']]
        rep = {}
        with ProcessPoolExecutor(max_workers=8) as ex:
            for cid, v in ex.map(safe_one, ids):
                rep[cid] = v
                for k, (o, t, bb) in v.items(): print(f'{cid} t={t} fora {o}px  {k}  {bb}')
        json.dump(rep, open(os.path.join(QA, 'safe_report.json'), 'w'), ensure_ascii=False, indent=1)
        print('cues com violação:', sum(1 for v in rep.values() if v))
    else:
        for cid in args: print(sheet(cid))
