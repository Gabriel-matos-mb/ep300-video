"""Recorta assets reais do arquivo de impressão da caixa de pipoca EP300 (PDF vetorial) — sem geração."""
import glob, os, io, json
import pymupdf as fitz
from PIL import Image
from rembg import remove, new_session
D = glob.glob('I:/Drives compartilhados/Educa*/Marketing M*/01_CANAIS_ATIVOS/02_PODCAST/2026/300_*/caixa_de_pipoca_EP300_arquivos')[0]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'work', 'v1', 'pipoca')
S = new_session('isnet-general-use')
def page(f, i, dpi):
    pix = fitz.open(os.path.join(D, f))[i].get_pixmap(dpi=dpi)
    return Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
prov = {}
# (arquivo, página, dpi, caixa em px a 60 dpi, nome)
for f, pg, dpi, box, name in [
    ('4_caixa_de_pipoca_EP300_simulacao_3D_e_gabarito.pdf', 0, 240, (62, 92, 462, 612), 'caixa_pipoca_frente'),
    ('4_caixa_de_pipoca_EP300_simulacao_3D_e_gabarito.pdf', 0, 240, (508, 128, 950, 612), 'caixa_pipoca_verso'),
    ('3_caixa_de_pipoca_EP300_sem_linhas.pdf', 0, 300, (218, 432, 332, 532), 'selo_metricas_boss'),
    ('3_caixa_de_pipoca_EP300_sem_linhas.pdf', 0, 300, (228, 162, 508, 392), 'selo_episodio_300'),
]:
    im = page(f, pg, dpi); k = dpi / 60
    c = im.crop(tuple(int(v * k) for v in box))
    cut = remove(c, session=S, post_process_mask=True)
    cut = cut.crop(cut.split()[3].point(lambda v: 255 if v > 20 else 0).getbbox())
    cut.save(os.path.join(OUT, name + '.png')); prov[name] = {'origem': f, 'pagina': pg, 'dpi': dpi, 'recorte': 'rembg isnet (local)'}
    print(name, cut.size)
json.dump(prov, open(os.path.join(OUT, 'PROVENANCE.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
sh = Image.new('RGB', (1600, 450), (247, 244, 237)); x = 0
for n in prov:
    im = Image.open(os.path.join(OUT, n + '.png')); im.thumbnail((390, 430)); sh.paste(im, (x + 5, 10), im); x += 400
sh.save(os.path.join(OUT, 'QA_pipoca.jpg'))
