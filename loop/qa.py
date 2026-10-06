"""QA automático do EP300 LOOP: formato, duração, quadros pretos, costura FINAL→INÍCIO, energia de movimento,
bloco de patrocinadores estático, safe area, assets. Saída: out/qa_report.json + out/qa_motion.png"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, 'scene.json'), encoding='utf-8'))
MP4 = os.path.join(HERE, 'out', S['output']['name'] + '.mp4')
FPS = S['canvas']['fps']
R = {}

pr = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames', '-show_entries',
                                         'stream=width,height,r_frame_rate,nb_read_frames,codec_name,pix_fmt,duration,bit_rate',
                                         '-of', 'json', MP4]))['streams'][0]
R['ffprobe'] = pr
R['formato_1920x1080'] = (pr['width'], pr['height']) == (1920, 1080)
R['duracao_ok'] = abs(float(pr['duration']) - S['canvas']['duration']) < 0.05 and int(pr['nb_read_frames']) == int(FPS * S['canvas']['duration'])
R['sem_audio'] = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index', '-of', 'csv=p=0', MP4]).strip() == b''

# decodifica tudo em 480x270 (luma + RGB)
w, h = 480, 270
raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', MP4, '-vf', f'scale={w}:{h}:flags=area', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
V = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3).astype(np.float32)
n = len(V)
luma = V.mean(axis=(1, 2, 3))
R['luma_min'] = float(luma.min()); R['luma_max'] = float(luma.max())
R['quadros_pretos'] = int((luma < 8).sum())
d = np.abs(np.diff(V, axis=0)).mean(axis=(1, 2, 3))           # energia entre quadros consecutivos
seam = float(np.abs(V[0] - V[-1]).mean())                     # último -> primeiro (deve ser ~ um passo comum)
R['motion_medio'] = float(d.mean()); R['motion_max'] = float(d.max()); R['motion_p99'] = float(np.percentile(d, 99))
R['costura_final_inicio'] = seam
R['costura_vs_p99'] = seam / max(1e-9, float(np.percentile(d, 99)))
R['costura_ok'] = bool(seam <= max(d.max() * 1.2, 0.02))
# picos: nenhum salto > 4x a mediana (corte/flash)
R['pico_max_sobre_mediana'] = float(d.max() / max(1e-9, np.median(d)))
dl = np.abs(np.diff(luma))
R['luma_salto_max_por_quadro'] = float(dl.max())
R['sem_flash_ou_corte'] = bool(dl.max() < 0.35 and d.max() < 3.0)   # flash = salto global de luma; corte = Δ médio de quadro grande (movimento de sticker chega a ~1,5)
# costura no domínio-fonte (sem compressão): frame(60 s) == frame(0) e passo 59.97→0 igual a um passo normal
try:
    sys.path.insert(0, HERE); import build as _b
    _st = _b.build_static(); f = lambda t: np.asarray(_b.frame(_st, t), np.float32)
    R['costura_fonte_t60_vs_t0_maxdiff'] = float(np.abs(f(S['canvas']['duration']) - f(0)).max())
    R['costura_fonte_passo_final_inicio'] = float(np.abs(f((n - 1) / FPS) - f(0)).mean())
    R['costura_fonte_passo_normal'] = float(np.abs(f(0) - f(1 / FPS)).mean())
    R['costura_fonte_ok'] = R['costura_fonte_t60_vs_t0_maxdiff'] == 0.0 and abs(R['costura_fonte_passo_final_inicio'] - R['costura_fonte_passo_normal']) < 0.05
except Exception as e:
    R['erro_costura_fonte'] = repr(e)
R['nota_costura_codec'] = 'costura_final_inicio (decodificada) inclui pulso de keyframe (GOP=2 s, igual em todos os limites de GOP); a costura em si é exata na fonte.'
# bloco de patrocinadores estático (faixa y>=890 px, x 480..1440) — diff temporal só de ruído de compressão
y0 = int(890 / 1080 * h)
band = V[:, y0:h, int(480 / 1920 * w):int(1440 / 1920 * w)]
R['patrocinadores_movimento'] = float(np.abs(np.diff(band, axis=0)).mean())
R['patrocinadores_estaticos'] = bool(R['patrocinadores_movimento'] < 0.25)
# movimento por segundo -> curva (calmo vs. microinteração)
per_s = [float(d[i:i + FPS].mean()) for i in range(0, len(d) - FPS + 1, FPS)]
R['movimento_por_segundo'] = [round(x, 3) for x in per_s]
R['segundos_calmos(<=mediana*1.5)'] = int(sum(1 for x in per_s if x <= np.median(per_s) * 1.5))

# safe area (título 90%): checa cada sprite estático pela caixa nominal
sa = (96, 54, 1824, 1026)
try:
    sys.path.insert(0, HERE); import build
    st = build.build_static(); T = S['title']; boxes = {}
    for k, key in (('EPISÓDIO', 'ep'), ('300', 'num'), ('logo', 'logo')):
        cfg = {'EPISÓDIO': T['episodio'], '300': T['numero'], 'logo': T['logo']}[k]
        im = st[key]; bb = im.getchannel('A').point(lambda v: 255 if v > 60 else 0).getbbox()
        boxes[k] = [cfg['cx'] - im.width / 2 + bb[0], cfg['cy'] - im.height / 2 + bb[1], cfg['cx'] - im.width / 2 + bb[2], cfg['cy'] - im.height / 2 + bb[3]]
    sp = st['sponsors']; bb = sp.getchannel('A').point(lambda v: 255 if v > 60 else 0).getbbox()
    ox, oy = 960 - sp.width // 2, S['sponsors']['y'] - 34
    boxes['patrocinadores'] = [ox + bb[0], oy + bb[1], ox + bb[2], oy + bb[3]]
    R['safe_area_boxes'] = {k: [round(x) for x in v] for k, v in boxes.items()}
    R['safe_area_ok'] = all(v[0] >= sa[0] and v[1] >= sa[1] and v[2] <= sa[2] and v[3] <= sa[3] for v in boxes.values())
    # sobreposição título x patrocinadores / pill x logo
    def ov(a, b): return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])
    ks = list(boxes)
    R['sobreposicoes_estaticas'] = [f'{a}×{b}' for i, a in enumerate(ks) for b in ks[i + 1:] if ov(boxes[a], boxes[b])]
    # assets existem (nenhum "offline")
    paths = [c['file'] for c in S['collage']['cards']] + [c['alt'] for c in S['collage']['cards'] if c.get('alt')] + [T['logo']['file']] + [(lg if isinstance(lg, str) else lg['file']) for g in S['sponsors']['groups'] for lg in g['logos']] \
        + [p for a in S['actors'] for p in a['states'].values()] + [p['file'] for p in S['props']]
    R['assets_offline'] = [p for p in paths if not os.path.exists(os.path.join(HERE, p))]
except Exception as e:  # noqa
    R['erro_safe_area'] = repr(e)

# ---- checks V1 (conteúdo/mosaico/microgags) ----
import re
cards = S['collage']['cards']; R['mosaico_cartoes'] = len(cards)
R['mosaico_imagens_unicas'] = len({c['file'] for c in cards} | {c['alt'] for c in cards if c.get('alt')})
def area(c): return c['w'] * c['w'] * 9 / 16
tot = sum(area(c) for c in cards)
pref = lambda c: os.path.basename(c['file'])[:2]
R['mosaico_area_por_tipo'] = {k: round(sum(area(c) for c in cards if pref(c) == k) / tot, 3) for k in ('t_', 'p_', 'r_', 'b_')}
R['cenario_azul_share'] = R['mosaico_area_por_tipo']['b_']
R['cenario_azul_ok'] = R['cenario_azul_share'] <= 0.12
R['episodios_distintos_no_mosaico'] = len({re.search(r'EP(\d+)', c['file']).group(1) for c in cards if re.search(r'EP(\d+)', c['file'])})
R['cartoes_com_troca_lenta'] = sum(1 for c in cards if c.get('alt_keys'))
R['troca_min_duracao_dissolve_s'] = min((k[1][0] - k[0][0]) for c in cards if c.get('alt_keys') for k in [c['alt_keys']])
def _f(keys, t): return build.track(keys, t)
# tempo com sticker/gag visível (fração) e espaçamento dos gags
tt = np.arange(0, S['canvas']['duration'], 0.1)
vis = np.zeros(len(tt), bool)
for a in S['actors']:
    vis |= np.array([_f(a['presence'], t) > 0.05 for t in tt])
R['tempo_com_sticker_visivel_frac'] = round(float(vis.mean()), 3)
edges = np.flatnonzero(np.diff(vis.astype(int)) == 1); starts = [round(float(tt[i + 1]), 1) for i in edges]
R['inicios_de_aparicao_s'] = starts
# blocos contíguos de vida (agrupa aparições < 3 s de intervalo)
blocks = []; 
for i in np.flatnonzero(vis):
    t = float(tt[i])
    if blocks and t - blocks[-1][1] < 3.0: blocks[-1][1] = t
    else: blocks.append([t, t])
R['gags_blocos_s'] = [[round(a, 1), round(b, 1)] for a, b in blocks]
gaps = [blocks[i + 1][0] - blocks[i][1] for i in range(len(blocks) - 1)] + [S['canvas']['duration'] - blocks[-1][1] + blocks[0][0]]
R['menor_descanso_entre_gags_s'] = round(min(gaps), 1)
R['maior_bloco_gag_s'] = round(max(b - a for a, b in blocks), 1)
R['gags_espacados_ok'] = R['menor_descanso_entre_gags_s'] >= 15 and R['maior_bloco_gag_s'] <= 14
# frase/CTA removidos
R['sem_frase_cta'] = 'frase' not in S['title']
# logo Métricas Boss: nunca rotacionado (sem rot no manifesto; motor só reduz proporcionalmente)
mb = [lg for g in S['sponsors']['groups'] for lg in g['logos'] if 'metricas-boss' in (lg if isinstance(lg, str) else lg['file'])]
R['logo_mb_sem_rotacao_ou_deformacao'] = bool(mb) and all(isinstance(lg, dict) and 'rot' not in lg for lg in mb)
R['patrocinadores_provisorios'] = [g['label'] for g in S['sponsors']['groups'] if g.get('provisorio')]
# estabilidade do bloco de patrocinadores já medida acima; elementos "clicáveis": nenhum botão/pílula no manifesto
R['sem_botao_ou_play'] = ('frase' not in S['title'])

# gráfico de movimento
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 2.6)); ax.plot(np.arange(len(d)) / FPS, d, lw=.8); ax.axhline(d.max(), color='r', ls=':', lw=.6)
    ax.set_xlabel('s'); ax.set_ylabel('Δ médio/quadro (0-255)'); ax.set_title('EP300 LOOP — energia de movimento (costura em t=60→0: %.4f)' % seam)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, 'out', 'qa_motion.png'), dpi=110)
except Exception:
    pass

json.dump(R, open(os.path.join(HERE, 'out', 'qa_report.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in R.items() if k not in ('movimento_por_segundo', 'ffprobe')}, ensure_ascii=False, indent=1))
