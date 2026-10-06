"""Correção objetiva C02_03: troca SÓ a imagem EP1·2021 (frame ruim rejeitado) pelo frame EP1 aprovado (EP001_2021_b, o mesmo do S07/R03). Resto idêntico (V2 + mesmo time-warp)."""
import sys, os, subprocess, json
os.environ['EP300_V2_ASSETS'] = os.path.abspath('work/c203assets')
sys.path.insert(0, os.path.abspath('../v2')); sys.dont_write_bytecode = True
import gfx, engine, extra, extra_v2, customs, customs_v2, plan
from PIL import Image
C = [c for c in plan.CUES if c['id'] == 'C02_03'][0]
cu = dict(C, push_in=.4, push_out=5.5667 - C['dur'], push_len=.4, full=True)
D = 5.5667; n = 167
F = '24000/1001'
fc = (f"[0:v]scale=1280:720:flags=lanczos,format=yuva444p10le,split=3[a][b][c];[a]trim=0:3.4,setpts=(PTS-STARTPTS)*(2.3/3.4)[a1];"
      f"[b]trim=3.4:5.1,setpts=(PTS-STARTPTS)*(1.8/1.7)[b1];[c]trim=5.1:5.5667,setpts=(PTS-STARTPTS)*(0.4/0.4667)[c1];"
      f"[a1][b1][c1]concat=n=3:v=1:a=0,fps={F},trim=end_frame=108[v]")
out = 'layers/C02_03.mov'
p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', '1920x1080', '-r', '30', '-i', '-',
                      '-filter_complex', fc, '-map', '[v]', '-frames:v', '108', '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', out], stdin=subprocess.PIPE)
for i in range(n):
    p.stdin.write(engine.render_frame(cu, i / 30).convert('RGBA').tobytes())
p.stdin.close(); p.wait(); print('rc', p.returncode)
