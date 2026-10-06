"""QA visual: renderiza cues em instantes escolhidos SOBRE o quadro real da câmera naquele ponto da timeline
e monta folhas de contato. Uso: python qa_frames.py C01_02:1.0,3.0 C04_04:.1,1.0 ...   (sem args = todos, 2 quadros)"""
import sys, os, subprocess
from PIL import Image, ImageDraw
import build, plan, engine, gfx

T = build.timeline(); build.load_freezes()
OUT = os.path.join(build.WORK, 'qa'); os.makedirs(OUT, exist_ok=True)

def cam_frame(tl_frame):
    for s in T['shots']:
        if s['tl_in'] <= tl_frame < s['tl_out']:
            if s['cam'] == 'FREEZE':
                return Image.open(build.freeze_path(s['still'])).convert('RGBA').resize((960, 540))
            src = s['src_in'] + (tl_frame - s['tl_in']) / 30 - plan.OFFSETS[s['cam']]
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{src:.3f}', '-i', build.PROXY[s['cam']],
                            '-frames:v', '1', '-vf', 'scale=960:540', os.path.join(OUT, '_f.png')])
            return Image.open(os.path.join(OUT, '_f.png')).convert('RGBA')
    return Image.new('RGBA', (960, 540), (0, 0, 0, 255))

req = []
for a in sys.argv[1:]:
    cid, ts = a.split(':'); req += [(cid, float(t)) for t in ts.split(',')]
if not req:
    for c in T['cues']:
        req += [(c['id'], min(c['dur'] - .45, 1.0)), (c['id'], max(.5, c['dur'] - .5))]
tiles = []
for cid, t in req:
    c = next(x for x in T['cues'] if x['id'] == cid)
    base = cam_frame(c['tl_in'] + int(t * 30))
    ov = engine.render_frame(c, t).resize((960, 540), Image.BILINEAR)
    base.alpha_composite(ov)
    ImageDraw.Draw(base).text((8, 8), f'{cid} +{t:.2f}s  tl {(c["tl_in"] / 30 + t):.2f}', fill=(255, 255, 0))
    tiles.append(base)
cols = 2
for k in range(0, len(tiles), 8):
    grp = tiles[k:k + 8]; rows = (len(grp) + 1) // 2
    S = Image.new('RGB', (cols * 960, rows * 540))
    for i, im in enumerate(grp): S.paste(im.convert('RGB'), ((i % 2) * 960, (i // 2) * 540))
    p = os.path.join(OUT, f'sheet_{k // 8:02d}.jpg'); S.save(p, quality=82); print(p)
