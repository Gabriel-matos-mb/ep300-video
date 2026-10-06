"""Review 02: C06_03_MMM e C06_05_DEZ viram CARD de tela cheia (fundo creme pontilhado + linha do tempo), C06_03_VI sem o sticker de coracoes nos olhos."""
import subprocess, numpy as np, os
from PIL import Image, ImageDraw
from common import *
O = os.path.join(LAYERS, '_orig')
FPSS = f'{FPSN}/{FPSD}'

def run(c): 
    r = subprocess.run(['ffmpeg', '-v', 'error', '-y'] + c, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[-400:])

# 1) VI: sem o sticker (so a pilula "desculpa, Vi.")
run(['-i', f'{O}/C06_03_VI.mov', '-vf', "format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if(lt(X,200)+lt(Y,572),0,alpha(X,Y))',format=yuva444p10le",
     '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', f'{LAYERS}/C06_03_VI.mov'])

def bgpng(path, line_y):
    im = Image.new('RGB', (1280, 720), (247, 244, 237)); d = ImageDraw.Draw(im)
    for y in range(7, 720, 13):
        for x in range(7, 1280, 13): d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=(222, 217, 207))
    d.rounded_rectangle((90, line_y - 3, 1190, line_y + 3), 3, fill=(18, 18, 19))
    im.save(path)

for lid in ('C06_03_MMM', 'C06_05_DEZ'):
    src = f'{O}/{lid}.mov'
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', '1.0', '-i', src, '-frames:v', '1', '-vf', 'format=rgba', '-f', 'rawvideo', '-'], capture_output=True)
    a = np.frombuffer(r.stdout, np.uint8).reshape(720, 1280, 4)
    m = (a[:, :, 3] > 200) & (a[:, :, 0] > 220) & (a[:, :, 1] > 90) & (a[:, :, 1] < 150) & (a[:, :, 2] < 110)   # ponto laranja
    ys, xs = np.where(m); dx, dy = int(xs.mean()), int(ys.mean())
    ty = 430; tx = 640
    bg = f'{WORK}/{lid}_bg.png'; bgpng(bg, ty)
    n = int(subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout.strip().strip(','))
    run(['-loop', '1', '-framerate', FPSS, '-i', bg, '-i', src, '-filter_complex',
         f"[1:v]format=rgba,scale=iw*1.7:ih*1.7:flags=lanczos[l];[0:v][l]overlay=x={int(tx - dx * 1.7)}:y={int(ty - dy * 1.7)}:shortest=1,format=yuv422p10le[v]", '-map', '[v]', '-frames:v', str(n),
         '-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le', '-r', FPSS, f'{LAYERS}/{lid}.mov'])
    print(lid, 'dot', dx, dy, 'frames', n)
