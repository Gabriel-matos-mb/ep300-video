"""EP300 · V1 — QA visual barato: renderiza quadros de cues (sem gerar .mov) sobre o quadro REAL da câmera que estará
por baixo (com o reenquadramento e a correção de sync da V1) e monta folhas de contato.
Uso: python qa_cues.py [C01_02,C03_04 ...] [--times .3,.6,.9]  → work/v1/qa/cues_*.jpg
"""
import os, sys, subprocess, io
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build, plan, engine

OUT = os.path.join(build.WORK, 'v1', 'qa'); os.makedirs(OUT, exist_ok=True)


def under_frame(T, tl):
    """quadro da câmera sob o instante tl (frames) — mesmo caminho do build (crop + sync), sem grade."""
    for s in T['shots']:
        if s['tl_in'] <= tl < s['tl_out']:
            if s['cam'] == 'FREEZE':
                return Image.open(build.freeze_path(s['still'])).convert('RGBA').resize((1920, 1080))
            bc = build.base_cam(s['cam'])
            ss = s['src_in'] + (tl - s['tl_in']) / 30 - plan.OFFSETS[bc] + (build.LEAD if bc == 'W' else 0)
            w_in, h_in = (1920, 1080) if bc == 'W' else (1280, 720)
            src = build.SRC['W'] if bc == 'W' else build.PROXY[bc]
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{ss:.3f}', '-i', src, '-frames:v', '1', '-vf',
                                  build.vf_cam(s['cam'], w_in, h_in, 1920, 1080, graded=False), '-f', 'image2pipe', '-vcodec', 'png', '-'],
                                 capture_output=True).stdout
            return Image.open(io.BytesIO(raw)).convert('RGBA')
    return Image.new('RGBA', (1920, 1080), (0, 0, 0, 255))


def main():
    build.load_freezes()
    T = build.timeline()
    ids = sys.argv[1].split(',') if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else [c['id'] for c in plan.CUES]
    times = [.35, .7, .95]
    if '--times' in sys.argv: times = [float(x) for x in sys.argv[sys.argv.index('--times') + 1].split(',')]
    tiles = []
    for c in T['cues']:
        if c['id'] not in ids: continue
        for f in times:
            t = min(c['dur'] - .05, max(.05, c['dur'] * f))
            fg = engine.render_frame(c, t)
            bg = under_frame(T, c['tl_in'] + int(t * 30)) if not c.get('full') else Image.new('RGBA', (1920, 1080), (60, 60, 60, 255))
            bg.alpha_composite(fg)
            im = bg.convert('RGB').resize((640, 360))
            ImageDraw.Draw(im).text((8, 6), f"{c['id']} t={t:.1f}", fill=(255, 0, 255))
            tiles.append(im)
    per = 12
    for k in range(0, len(tiles), per):
        chunk = tiles[k:k + per]
        sh = Image.new('RGB', (3 * 640, ((len(chunk) + 2) // 3) * 360))
        for i, im in enumerate(chunk): sh.paste(im, ((i % 3) * 640, (i // 3) * 360))
        p = os.path.join(OUT, f'cues_{k // per:02d}.jpg'); sh.save(p, quality=78); print(p)


if __name__ == '__main__':
    main()
