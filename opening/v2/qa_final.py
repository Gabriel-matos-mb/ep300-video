"""EP300 · V1 — QA final automatizado (sem depender do Gabriel para o previsível).

1 técnico: duração/codec/resolução, preto, congelamento, loudness/pico
2 sync ponta-a-ponta: quadro da BASE (o que foi montado) × quadro do BRUTO no tempo esperado, testando ±6 quadros
  → o melhor casamento tem que ser 0 (inclui a correção de 5 quadros da geral)
3 emendas: energia do diálogo ±40 ms em cada corte (≤ −38 dB, exceto respiro intencional)
4 conteúdo: retranscrição do proxy (large-v3) + busca de termos que não podem aparecer
5 folhas de contato do proxy (a cada 10 s) para QA visual
Saída: work/v1/qa/qa_final.json + final_*.jpg
"""
import os, sys, json, subprocess, re, io, glob
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build, plan

OUT = os.path.join(build.WORK, 'v1', 'qa'); os.makedirs(OUT, exist_ok=True)
PROXY = os.path.join(build.B, f'{build.NAME}_PROXY.mp4')
R = {}


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')


def tecnico():
    j = json.loads(sh(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,size:stream=codec_name,profile,width,height,r_frame_rate,pix_fmt,nb_frames,sample_rate,channels',
                       '-of', 'json', PROXY]).stdout)
    e = sh(['ffmpeg', '-hide_banner', '-i', PROXY, '-vf', 'blackdetect=d=0.1:pix_th=0.06,freezedetect=n=0.003:d=2.5', '-af', 'ebur128=peak=true',
            '-f', 'null', '-']).stderr
    blacks = re.findall(r'black_start:([\d.]+) black_end:([\d.]+)', e)
    freezes = re.findall(r'freeze_start: ([\d.]+)', e)
    I = re.findall(r'I:\s+(-?[\d.]+) LUFS', e); P = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', e)
    R['tecnico'] = dict(ffprobe=j, black=blacks, freezes=freezes, lufs=float(I[-1]) if I else None, peak_dbfs=float(P[-1]) if P else None)
    print('tecnico', j['format']['duration'], 'black', blacks, 'freeze', freezes, 'I', R['tecnico']['lufs'], 'peak', R['tecnico']['peak_dbfs'])


def gray_small(img):
    a = np.asarray(img.convert('L').resize((160, 90)), np.float32)
    return (a - a.mean()) / (a.std() + 1e-6)


def grab(src, t, vf=None):
    cmd = ['ffmpeg', '-v', 'error', '-ss', f'{max(0, t):.4f}', '-i', src, '-frames:v', '1']
    if vf: cmd += ['-vf', vf]
    cmd += ['-f', 'image2pipe', '-vcodec', 'png', '-']
    return Image.open(io.BytesIO(subprocess.run(cmd, capture_output=True).stdout))


def sync_e2e(T):
    base = os.path.join(build.B, 'base_720.mp4')
    shots = [s for s in T['shots'] if s['cam'] != 'FREEZE' and s['tl_out'] - s['tl_in'] > 40]
    picks = []
    for cam in ('W', 'WG', 'WL', 'G', 'L'):
        cs = [s for s in shots if s['cam'] == cam]
        if cs: picks += [cs[0], cs[len(cs) // 2], cs[-1]] if cam == 'W' else [cs[len(cs) // 2]]
    rows = []
    for s in picks:
        tl = (s['tl_in'] + s['tl_out']) // 2
        b = gray_small(grab(base, tl / 30))
        bc = build.base_cam(s['cam'])
        src_t = s['src_in'] + (tl - s['tl_in']) / 30 - plan.OFFSETS[bc] + (build.LEAD if bc == 'W' else 0)
        fps = 30 if bc == 'W' else 24000 / 1001
        vf = build.vf_cam(s['cam'], 1920 if bc == 'W' else 3840, 1080 if bc == 'W' else 2160, 320, 180, graded=False)
        sc = {}
        for k in range(-6, 7):
            r = gray_small(grab(build.SRC[bc], src_t + k / fps, vf))
            sc[k] = float((b * r).mean())
        best = max(sc, key=sc.get)
        rows.append(dict(cam=s['cam'], seg=s['seg'], tl_s=round(tl / 30, 2), best_offset_frames=best, corr=round(sc[best], 3),
                         corr_at_0=round(sc[0], 3)))
        print('sync', rows[-1], flush=True)
    R['sync_e2e'] = rows


def emendas(T):
    import wave
    w = wave.open(os.path.join(build.L_AUD, 'STEM_DIALOGO.wav')); sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, 2)[:, 0] / 32768
    env = np.load(os.path.join(build.WORK, 'env10ms.npy'))
    rows = []
    for sg in T['segs']:
        if sg['id'] == 'HOLD': continue
        for edge, src in (('in', sg['src_in']), ('out', sg['src_out'])):
            v = float(env[int(src * 100) - 4:int(src * 100) + 4].max())
            rows.append(dict(seg=sg['id'], edge=edge, fonte_s=round(src, 2), db_bruto_pm40ms=round(v, 1)))
    R['emendas'] = rows
    bad = [r for r in rows if r['db_bruto_pm40ms'] > -38 and not (r['seg'] in ('S2b',) and r['edge'] == 'in') and not (r['seg'] == 'S2a2' and r['edge'] == 'out')]
    R['emendas_acima_-38dB'] = bad
    print('emendas >-38 dB (fora do respiro):', bad)


def conteudo():
    wav = os.path.join(OUT, 'proxy_16k.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', PROXY, '-ac', '1', '-ar', '16000', wav], check=True)
    out = os.path.join(OUT, 'proxy_transcript.json')
    subprocess.run([sys.executable, os.path.join(build.WORK, 'transcribe.py'), wav, out,
                    'C:/Users/gabri/Code/podcast-cutter/models/faster-whisper-large-v3'], capture_output=True)
    d = json.load(open(out, encoding='utf-8'))
    txt = ' '.join(s['text'] for s in d['segments'])
    open(os.path.join(OUT, 'proxy_transcript.txt'), 'w', encoding='utf-8').write(
        '\n'.join(f"{s['start']:7.2f} {s['text']}" for s in d['segments']))
    proib = {'chupa': r'chupa', 'nao colocar': r'n[ãa]o colocar', '2025 (ano errado)': r'nesse ano de 2025|ano de 2025',
             'retomada/TP': r'sobe mais|volta a[íi]|entona[çc][ãa]o|s[óo] corta|fora casa', 'tema do episodio': r'esse [ée] o tema',
             'palavrão': r'puta|caralho', 'meta confirma': r'confirma'}
    hits = {k: re.findall(v, txt, re.I) for k, v in proib.items()}
    R['conteudo'] = dict(palavras=len(txt.split()), proibidos={k: len(v) for k, v in hits.items()})
    print('conteudo', R['conteudo'])


def contato(T):
    n = int(T['total'] / 30 // 10) + 1
    tiles = []
    for i in range(n):
        t = min(T['total'] / 30 - .2, i * 10 + 5)
        im = grab(PROXY, t).convert('RGB').resize((480, 270))
        ImageDraw.Draw(im).text((6, 4), f'{int(t // 60)}:{int(t % 60):02d}', fill=(255, 0, 255))
        tiles.append(im)
    for k in range(0, len(tiles), 20):
        ch = tiles[k:k + 20]; S = Image.new('RGB', (4 * 480, ((len(ch) + 3) // 4) * 270))
        for i, im in enumerate(ch): S.paste(im, ((i % 4) * 480, (i // 4) * 270))
        S.save(os.path.join(OUT, f'final_{k // 20:02d}.jpg'), quality=80)
    print('contato', len(tiles))


if __name__ == '__main__':
    T = build.timeline()
    steps = sys.argv[1:] or ['tecnico', 'sync', 'emendas', 'conteudo', 'contato']
    p = os.path.join(OUT, 'qa_final.json')
    if os.path.exists(p): R.update(json.load(open(p, encoding='utf-8')))
    if 'tecnico' in steps: tecnico()
    if 'sync' in steps: sync_e2e(T)
    if 'emendas' in steps: emendas(T)
    if 'conteudo' in steps: conteudo()
    if 'contato' in steps: contato(T)
    json.dump(R, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
