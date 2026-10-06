"""EP300 · V1 — auditoria de sincronia a partir dos BRUTOS originais (só leitura).

1) Drift de relógio: correlação áudio-câmera × áudio-mesa (CAM_GERAL) em 9 janelas ao longo do take.
2) Lip-sync real: movimento da boca (YuNet + diferença de quadros na região da boca) × envelope da fala
   da mesa, em 3 janelas (começo/meio/fim) por câmera. Lag > 0 = imagem atrasada em relação ao áudio.
Saída: work/v1/sync_report.json
"""
import os, sys, json, subprocess, wave, glob
import numpy as np, cv2

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
W = os.path.join(ROOT, 'work')
BR = glob.glob('I:/Drives compartilhados/Educa*/Marketing M*/01_CANAIS_ATIVOS/02_PODCAST/2026/300_*/01_VIDEO*/01_BRUTOS')[0]
SRC = {'W': os.path.join(BR, 'CAM_GERAL.mp4'), 'G': os.path.join(BR, 'MVI_9943-CAM_GUSTAVO.MP4'),
       'L': os.path.join(BR, 'MVI_9943-CAM_LUCIAN.MP4')}
FPS = {'W': 30.0, 'G': 24000 / 1001, 'L': 24000 / 1001}
OFF = {'W': 0.0, 'G': 476.503, 'L': 476.320}
YUNET = 'C:/Users/gabri/Code/podcast-cutter/models/face_detection_yunet_2023mar.onnx'
# --v1: aplica a correção da V1 (imagem da CAM_GERAL lida 5 quadros adiante) — o resultado esperado é lag ≈ 0
W_LEAD = 5 / 30 if '--v1' in sys.argv else 0.0


def wav(p):
    w = wave.open(p); sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
    if w.getnchannels() > 1: x = x.reshape(-1, w.getnchannels()).mean(1)
    return x, sr


def env100(x, sr):
    h = sr // 100; x = x[:len(x) // h * h].reshape(-1, h)
    return 20 * np.log10(np.sqrt((x ** 2).mean(1)) + 1e-3)


def xcorr_lag(a, b, maxlag):
    """lag (amostras) que maximiza corr(a[t], b[t+lag])."""
    a = (a - a.mean()) / (a.std() + 1e-9); b = (b - b.mean()) / (b.std() + 1e-9)
    best = None
    for L in range(-maxlag, maxlag + 1):
        if L >= 0: c = float(np.mean(a[:len(a) - L] * b[L:]))
        else: c = float(np.mean(a[-L:] * b[:len(b) + L]))
        if best is None or c > best[1]: best = (L, c)
    return best


def audio_drift():
    g, sr = wav(os.path.join(W, 'audio', 'geral_16k.wav'))
    out = {}
    for cam, name in (('G', 'gustavo'), ('L', 'lucian')):
        y, _ = wav(os.path.join(W, 'audio', name + '_16k.wav'))
        rows = []
        for tg in np.linspace(515, 945, 9):
            tc = tg - OFF[cam]
            a = g[int(tg * sr):int((tg + 8) * sr)]; b = y[int(tc * sr):int((tc + 8) * sr)]
            # correlação cruzada fina (±80 ms) em amostras a 16 kHz, via FFT
            n = 1 << int(np.ceil(np.log2(len(a) + len(b))))
            cc = np.fft.irfft(np.fft.rfft(a, n) * np.conj(np.fft.rfft(b, n)), n)
            m = int(0.08 * sr); cc = np.concatenate([cc[-m:], cc[:m + 1]])
            lag = (int(np.argmax(np.abs(cc))) - m) / sr
            rows.append({'geral_t': round(float(tg), 1), 'resid_ms': round(lag * 1000, 1)})
        out[cam] = rows
    return out


def frames(cam, t0, dur, scale_w):
    src = SRC[cam]; tc = t0 - OFF[cam] + (W_LEAD if cam == 'W' else 0)
    h = int(scale_w * 9 / 16)
    cmd = ['ffmpeg', '-v', 'error', '-ss', f'{tc:.3f}', '-i', src, '-t', f'{dur}', '-vf', f'scale={scale_w}:{h}',
           '-pix_fmt', 'bgr24', '-f', 'rawvideo', '-']
    raw = subprocess.run(cmd, capture_output=True).stdout
    arr = np.frombuffer(raw, np.uint8).reshape(-1, h, scale_w, 3)
    return arr, tc


def mouth_signal(arr, want_faces):
    det = cv2.FaceDetectorYN.create(YUNET, '', (arr.shape[2], arr.shape[1]), 0.6)
    boxes = []
    for i in range(0, len(arr), max(1, len(arr) // 25)):
        _, fs = det.detect(np.ascontiguousarray(arr[i]))
        if fs is not None: boxes += [f[:14] for f in fs]
    if not boxes: return []
    boxes = np.array(boxes)
    # agrupa rostos por x (até want_faces), mediana de cada grupo
    boxes = boxes[np.argsort(boxes[:, 0])]
    groups = [[boxes[0]]]
    for b in boxes[1:]:
        if abs(b[0] - groups[-1][-1][0]) < b[2]: groups[-1].append(b)
        else: groups.append([b])
    groups = sorted(groups, key=len, reverse=True)[:want_faces]
    sigs = []
    for gr in groups:
        f = np.median(np.array(gr), 0)
        x, y, w, h = f[:4]; nose_y = f[9]; mly, mry = f[11], f[13]; mlx, mrx = f[10], f[12]
        y0 = int((nose_y + max(mly, mry)) / 2); y1 = int(max(mly, mry) + 0.22 * h)
        x0 = int(mlx - 0.12 * w); x1 = int(mrx + 0.12 * w)
        roi = arr[:, y0:y1, x0:x1].astype(np.float32).mean(3)
        d = np.abs(np.diff(roi, axis=0)).mean((1, 2))
        sigs.append({'x': float(x), 'w': float(w), 'sig': np.concatenate([[d[0]], d])})
    return sigs


def lipsync():
    g, sr = wav(os.path.join(W, 'audio', 'geral_16k.wav'))
    E = env100(g, sr)
    res = {}
    for cam in ('G', 'L', 'W'):
        rows = []
        for t0 in (512.0, 700.0, 905.0):
            dur = 40.0
            arr, tc = frames(cam, t0, dur, 960 if cam != 'W' else 1920)
            for s in mouth_signal(arr, 2 if cam == 'W' else 1):
                n = len(s['sig']); tt = t0 + np.arange(n) / FPS[cam]
                grid = np.arange(t0 + 0.5, t0 + dur - 0.5, 0.01)
                m = np.interp(grid, tt, s['sig'])
                e = E[(grid * 100).astype(int)]
                de = np.maximum(np.diff(np.concatenate([[e[0]], e])), 0)  # ataque da fala
                # fala → boca: movimento acompanha o envelope; usar o envelope suavizado
                k = np.ones(8) / 8; es = np.convolve(e, k, 'same'); ms = np.convolve(m, k, 'same')
                L, c = xcorr_lag(es, ms, 40)
                rows.append({'geral_t0': t0, 'face_x': round(s['x']), 'lag_ms': L * 10, 'corr': round(c, 3)})
            print(cam, rows[-2:] if cam == 'W' else rows[-1:], flush=True)
        res[cam] = rows
    return res


if __name__ == '__main__' and '--vidvid' not in sys.argv:
    rep = {'offsets_s': OFF, 'audio_drift_ms': audio_drift()}
    print(json.dumps(rep['audio_drift_ms']), flush=True)
    if '--audio-only' not in sys.argv:
        rep['lipsync'] = lipsync()
    os.makedirs(os.path.join(W, 'v2'), exist_ok=True)
    json.dump(rep, open(os.path.join(W, 'v2', 'sync_report.json'), 'w'), indent=1)


def vidvid(t0s=(512.0, 700.0, 905.0), dur=40.0):
    """Imagem × imagem: movimento do rosto da pessoa na câmera fechada × a mesma pessoa na CAM_GERAL.
    Independe do áudio. lag_ms > 0 = a câmera fechada está ATRASADA em relação à geral no alinhamento atual."""
    out = {}
    det = None
    for cam in ('G', 'L'):
        rows = []
        for t0 in t0s:
            a, _ = frames('W', t0, dur, 960); b, _ = frames(cam, t0, dur, 480)
            # rosto na geral: G à direita, L à esquerda (960 px de largura)
            det = cv2.FaceDetectorYN.create(YUNET, '', (960, 540), 0.5)
            _, fs = det.detect(np.ascontiguousarray(a[len(a) // 2]))
            fs = sorted([f for f in fs], key=lambda f: f[0]) if fs is not None else []
            if len(fs) < 2: print('VV', cam, t0, 'sem 2 rostos na geral — janela pulada'); continue
            f = fs[-1] if cam == 'G' else fs[0]
            x, y, w, h = [int(v) for v in f[:4]]
            ra = a[:, max(0, y - h // 2):y + 2 * h, max(0, x - w // 2):x + w + w // 2].astype(np.float32).mean(3)
            rb = b.astype(np.float32).mean(3)
            sa = np.abs(np.diff(ra, axis=0)).mean((1, 2)); sb = np.abs(np.diff(rb, axis=0)).mean((1, 2))
            grid = np.arange(t0 + 1, t0 + dur - 1, 0.005)
            ma = np.interp(grid, t0 + np.arange(1, len(sa) + 1) / FPS['W'], sa)
            mb = np.interp(grid, t0 + np.arange(1, len(sb) + 1) / FPS[cam], sb)
            L, c = xcorr_lag(ma, mb, 200)
            rows.append({'geral_t0': t0, 'lag_ms': L * 5, 'corr': round(c, 3)})
            print('VV', cam, rows[-1], flush=True)
        out[cam] = rows
    return out


if __name__ == '__main__' and '--vidvid' in sys.argv:
    rep = json.load(open(os.path.join(W, 'v2', 'sync_report.json')))
    rep['video_x_video_V1_corrigido' if W_LEAD else 'video_x_video'] = vidvid(tuple(float(x) for x in os.environ.get('SYNC_T0S', '512,700,905').split(',')))
    json.dump(rep, open(os.path.join(W, 'v2', 'sync_report.json'), 'w'), indent=1)
