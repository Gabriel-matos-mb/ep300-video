"""EP300 · V2 — posição dos olhos nos adesivos (YuNet, modelo local do podcast-cutter) para o gag 'coração nos olhos'.
Salva work/v2/assets/eyes.json {path: {lx,ly,rx,ry,face_w}} em FRAÇÕES da imagem do adesivo."""
import os, json, glob, cv2, numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, '..', 'work', 'v2', 'assets')
M = 'C:/Users/gabri/Code/podcast-cutter/models/face_detection_yunet_2023mar.onnx'
out = {}
for f in sorted(glob.glob(os.path.join(A, 'stickers', '*', '*.png'))):
    im = Image.open(f).convert('RGBA'); bg = Image.new('RGB', im.size, (128, 128, 128)); bg.paste(im, (0, 0), im)
    a = cv2.cvtColor(np.array(bg), cv2.COLOR_RGB2BGR); h, w = a.shape[:2]
    det = cv2.FaceDetectorYN.create(M, '', (w, h), 0.5, 0.3, 5000); det.setInputSize((w, h))
    _, faces = det.detect(a)
    rel = os.path.relpath(f, A).replace(chr(92), '/')
    if faces is None or not len(faces): print('sem rosto', rel); continue
    fc = max(faces, key=lambda r: r[2] * r[3])
    rx, ry, lx, ly = fc[4], fc[5], fc[6], fc[7]     # olho direito da pessoa (esq. da imagem) e esquerdo
    out[rel] = dict(lx=float(rx / w), ly=float(ry / h), rx=float(lx / w), ry=float(ly / h), face_w=float(fc[2] / w))
json.dump(out, open(os.path.join(A, 'eyes.json'), 'w'), indent=1)
print(len(out), 'ok')
