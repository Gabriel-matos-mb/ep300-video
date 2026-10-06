"""EP300 · V1 — adesivos de convidados a partir de FOTOS REAIS curadas pelo Gabriel.

Mesmo estilo dos personagens do handoff (Gustavo/Lucian): cabeça recortada (rosto + cabelo),
contorno branco de papel, sem sombra embutida (a sombra é aplicada no render, como em gfx.face).
Nada generativo: só recorte (rembg local, gratuito), enquadramento, escala e correção leve.

Saída: work/v1/stickers/<PESSOA>/<NN_estado>.png  (+ _recorte.png sem contorno, _tratada.jpg quando houver
upscale/ajuste) e work/v1/stickers/PROVENANCE.json (arquivo original, md5, recorte, tratamento).
"""
import os, json, hashlib, glob
import numpy as np, cv2
from PIL import Image, ImageOps, ImageFilter
from rembg import remove, new_session

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'work', 'v1', 'stickers')
YUNET = 'C:/Users/gabri/Code/podcast-cutter/models/face_detection_yunet_2023mar.onnx'
TIME = 'I:/Drives compartilhados/Educação/Marketing Métricas Boss/03_INSTITUCIONAL/03_FOTOS_TIME/'
EP = glob.glob('I:/Drives compartilhados/Educa*/Marketing M*/01_CANAIS_ATIVOS/02_PODCAST/2026/300_*/01_VIDEO*/00_ASSETS E INSERTS/fotos para gerar stickers')[0] + '/'

# pessoa → [(estado, arquivo)]  — escolhidos na folha de contato (triagem barata)
PLAN = {
    'PHILLIP': [('01_still', TIME + '05_PHILLIP/01_ILHA_DIA_12.07/IMG_4460.JPG'),
                ('02_reacao_sorriso', TIME + '05_PHILLIP/01_ILHA_DIA_12.07/IMG_4467.JPG'),
                ('03_reacao_risada', TIME + '05_PHILLIP/01_ILHA_DIA_12.07/IMG_4411.JPG')],
    'MAFE': [('01_still', TIME + '09_MAFE/04_GRAVAÇÃO_LOOKER STUDIO/IMG_0410.JPG'),
             ('02_reacao_sorriso', TIME + '09_MAFE/04_GRAVAÇÃO_LOOKER STUDIO/IMG_0411.JPG'),
             ('03_reacao_marota', TIME + '09_MAFE/02_NOVAS_FOTOS_MAIO_2022/IMG_3510.JPG')],
    'BONEL': [('01_still', EP + 'CLAUDIO-BONEL-3.jpg'), ('02_alt', EP + 'CLAUDIO-BONEL2.jpg'), ('03_alt', EP + 'CLAUDIO-BONEL.jpg')],
    'VITORIA': [('01_still', EP + 'VITORIA-COMARIN.webp')],
    'LAYLA': [('01_still', EP + 'LAYLA-SAYED.jpg')],
}
TARGET = 900        # lado maior do adesivo final (px) — maior que o uso previsto (≤ 480 px no 1080p)
BORDER = 14         # contorno branco (proporcional ao dos personagens do handoff: ~3% do lado)


def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def head_crop(im):
    """recorte quadrado em torno da cabeça (rosto + cabelo), a partir do YuNet."""
    a = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    s = 900 / max(a.shape[:2]); small = cv2.resize(a, None, fx=s, fy=s)
    det = cv2.FaceDetectorYN.create(YUNET, '', (small.shape[1], small.shape[0]), 0.6)
    _, fs = det.detect(small)
    f = max(fs, key=lambda f: f[2] * f[3]) / s
    x, y, w, h = f[:4]
    cx = x + w / 2; cy = y + h * 0.40
    side = h * 2.1
    box = (int(cx - side / 2), int(cy - side * 0.55), int(cx + side / 2), int(cy + side * 0.45))
    chin = (y + h * 1.04 - box[1])  # y do queixo dentro do recorte
    return box, chin, (x, y, w, h)


def round_dilate(alpha, r):
    a = alpha.filter(ImageFilter.GaussianBlur(r / 2))
    return a.point(lambda v: 255 if v > 18 else 0).filter(ImageFilter.GaussianBlur(1.2))


def make(person, state, src, session, prov):
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    box, chin, face = head_crop(im)
    pad = Image.new('RGB', (box[2] - box[0], box[3] - box[1]), (128, 128, 128))
    pad.paste(im.crop((max(0, box[0]), max(0, box[1]), min(im.width, box[2]), min(im.height, box[3]))),
              (max(0, -box[0]), max(0, -box[1])))
    crop = pad
    treated = None
    if crop.width < TARGET:  # recuperação técnica leve: LANCZOS + unsharp moderado (sem IA generativa)
        k = TARGET / crop.width
        crop = crop.resize((TARGET, TARGET), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.6, 60, 2))
        chin *= k
        treated = f'upscale LANCZOS ×{k:.2f} + unsharp(1.6,60)'
    else:
        k = TARGET / crop.width; crop = crop.resize((TARGET, TARGET), Image.LANCZOS); chin *= k
    cut = remove(crop, session=session, post_process_mask=True)
    a = np.array(cut.split()[3]).astype(np.float32)
    # corta abaixo do queixo com borda suave (adesivo = cabeça, como os personagens do handoff)
    yy = np.arange(TARGET)[:, None]
    fade = np.clip((chin + 0.07 * TARGET - yy) / 3.0, 0, 1)  # corte firme; o contorno de papel fecha a borda
    a = a * fade
    # tira fragmentos soltos: mantém o maior componente
    m = (a > 40).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m)
    if n > 2:
        keep = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA])); a[lab != keep] = 0
    alpha = Image.fromarray(a.astype(np.uint8))
    rgba = crop.convert('RGBA'); rgba.putalpha(alpha)
    bb = alpha.point(lambda v: 255 if v > 20 else 0).getbbox()
    marg = BORDER + 6
    bb = (max(0, bb[0] - marg), max(0, bb[1] - marg), min(TARGET, bb[2] + marg), min(TARGET, bb[3] + marg))
    rgba = rgba.crop(bb); alpha = rgba.split()[3]
    paper = round_dilate(alpha, BORDER)
    st = Image.new('RGBA', rgba.size, (255, 255, 255, 0)); st.putalpha(paper)
    st.alpha_composite(rgba)
    d = os.path.join(OUT, person); os.makedirs(d, exist_ok=True)
    st.save(os.path.join(d, state + '.png'))
    rgba.save(os.path.join(d, state + '_recorte.png'))
    if treated: crop.save(os.path.join(d, state + '_tratada.jpg'), quality=92)
    prov[f'{person}/{state}.png'] = {'original': src, 'md5_original': md5(src), 'original_px': list(im.size),
                                     'recorte_px': [box[2] - box[0], box[3] - box[1]], 'tratamento': treated or 'nenhum (só redução)',
                                     'recorte_fundo': 'rembg isnet-general-use (local, gratuito)', 'contorno_px': BORDER}
    print(person, state, rgba.size, treated or '')


if __name__ == '__main__':
    sess = new_session('isnet-general-use')
    prov = {}
    for p, states in PLAN.items():
        for st, src in states:
            make(p, st, src, sess, prov)
    json.dump(prov, open(os.path.join(OUT, 'PROVENANCE.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # folha de QA sobre fundo creme e escuro
    fs = sorted(glob.glob(os.path.join(OUT, '*', '0*.png')))
    fs = [f for f in fs if '_recorte' not in f]
    sh = Image.new('RGB', (len(fs) * 260, 520), (247, 244, 237))
    sh.paste((18, 18, 19), (0, 260, sh.width, 520))
    for i, f in enumerate(fs):
        im = Image.open(f); im.thumbnail((240, 240))
        for row in (0, 1): sh.paste(im, (i * 260 + 10, row * 260 + 10), im)
    sh.save(os.path.join(OUT, 'QA_stickers.jpg'), quality=85)
