"""Triagem barata das fotos curadas: miniatura (JPEG draft), rosto (YuNet), folha de contato."""
import os, sys, glob, json
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageOps
YUNET = 'C:/Users/gabri/Code/podcast-cutter/models/face_detection_yunet_2023mar.onnx'
BASE = 'I:/Drives compartilhados/Educação/Marketing Métricas Boss/03_INSTITUCIONAL/03_FOTOS_TIME/'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'work', 'v1', 'stickers')

def scan(name, folder, maxn=400):
    files = []
    for r, _, fs in os.walk(folder):
        files += [os.path.join(r, f) for f in fs if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    files = sorted(files)[:maxn]
    rows = []
    for p in files:
        try:
            im = Image.open(p); full = im.size; im.draft('RGB', (480, 480)); im = ImageOps.exif_transpose(im.convert('RGB'))
            im.thumbnail((480, 480))
        except Exception:
            continue
        a = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        det = cv2.FaceDetectorYN.create(YUNET, '', (a.shape[1], a.shape[0]), 0.7)
        _, fs = det.detect(a)
        if fs is None: continue
        f = max(fs, key=lambda f: f[2] * f[3])
        g = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
        x, y, w, h = [max(0, int(v)) for v in f[:4]]
        sharp = float(cv2.Laplacian(g[y:y + h, x:x + w], cv2.CV_64F).var()) if w > 5 else 0
        rows.append({'path': p, 'full': full, 'face_frac': round(float(f[2]) / a.shape[1], 3), 'nfaces': int(len(fs)),
                     'sharp': round(sharp, 1), 'thumb': im})
    # shortlist: 1 rosto dominante, rosto grande e nítido
    rows = [r for r in rows if r['face_frac'] > 0.10]
    rows.sort(key=lambda r: -(r['face_frac'] * 2 + min(r['sharp'], 400) / 400 - 0.3 * (r['nfaces'] > 1)))
    top = rows[:24]
    sheet = Image.new('RGB', (6 * 250, ((len(top) + 5) // 6) * 270), 'white'); d = ImageDraw.Draw(sheet)
    for i, r in enumerate(top):
        t = r['thumb'].copy(); t.thumbnail((240, 240))
        sheet.paste(t, ((i % 6) * 250 + 5, (i // 6) * 270 + 5))
        d.text(((i % 6) * 250 + 5, (i // 6) * 270 + 250), f"{i:02d} {os.path.basename(r['path'])}", fill='black')
    os.makedirs(OUT, exist_ok=True)
    sheet.save(os.path.join(OUT, f'triagem_{name}.jpg'), quality=80)
    json.dump([{k: v for k, v in r.items() if k != 'thumb'} for r in top], open(os.path.join(OUT, f'triagem_{name}.json'), 'w'), indent=0)
    print(name, 'fotos', len(files), 'com rosto grande', len(rows))

if __name__ == '__main__':
    scan('PHILLIP', BASE + '05_PHILLIP')
    scan('MAFE', BASE + '09_MAFE')
