"""Cold-open blooper (R07/NON_NEGOTIABLES §12): só 'Começou mesmo? Começa de novo aqui.' + risada (b0 4.15-6.50 s), P&B + grão + moldura REC da V2."""
import subprocess, os, glob
from common import *
D = glob.glob('I:/Drives compartilhados/Educa*/Marketing*/01_CANAIS_ATIVOS/02_PODCAST/2026/300_*/01_VIDEO DE ABERTURA/00_ASSETS E INSERTS')[0]
REC = D + '/V2_GERADOS/OVERLAYS/C00_00_COLD_OPEN_ARQUIVO.mov'
B0 = os.path.join(ROOT, 'work', 'v2', 'b0.mp4')
IN, DUR = 0.0, 10.5   # cold open COMPLETO: 'Fala aí...' -> 'Começou mesmo?' -> 'Começa de novo' -> reação/risada (fim natural ~10.45 s, antes de 'Eu fico chocatinho')
out = os.path.join(WORK, 'blooper.mov')
fps = f'{FPSN}/{FPSD}'
cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', str(IN), '-t', str(DUR), '-i', B0, '-ss', str(IN), '-t', str(DUR), '-i', REC,
       '-filter_complex',
       f"[0:v]scale=1280:720:flags=lanczos,fps={fps},hue=s=0,eq=contrast=1.12:brightness=-0.02,noise=alls=14:allf=t,format=yuv420p[a];"
       f"[1:v]scale=1280:720:flags=lanczos,fps={fps},format=rgba[b];[a][b]overlay=format=auto,format=yuv422p10le[v]",
       '-map', '[v]', '-frames:v', str(PRE_ORDER[3][1]), '-an', '-c:v', 'prores_ks', '-profile:v', '2', '-r', fps, out]
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.returncode, r.stderr[-400:])
