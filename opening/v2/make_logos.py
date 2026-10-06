"""EP300 · V2 — logos de ferramentas como adesivos (simple-icons@13, CC0; glifo em cor da marca sobre papel branco, borda de tinta).
Fonte: https://cdn.jsdelivr.net/npm/simple-icons@13/icons/<slug>.svg (baixados 2026-09-29 em work/v2/logos). Amplitude não existe na
biblioteca — vira wordmark tipográfico. Saída: work/v2/logos/png/<slug>.png + PROVENANCE.json"""
import os, re, json, skia
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'work', 'v2', 'logos'); OUT = os.path.join(SRC, 'png'); os.makedirs(OUT, exist_ok=True)
BRAND = {'googleanalytics': (0xE3, 0x74, 0x00), 'googletagmanager': (0x24, 0x6F, 0xDB), 'googlebigquery': (0x66, 0x9D, 0xF6),
         'looker': (0x43, 0x85, 0xF4), 'powerbi_v13': (0xF2, 0xC8, 0x11), 'meta': (0x08, 0x66, 0xFF), 'googleads': (0x42, 0x85, 0xF4),
         'hotjar': (0xFF, 0x3C, 0x00), 'mixpanel': (0x78, 0x56, 0xFF), 'tableau': (0xE9, 0x76, 0x27), 'matomo': (0x31, 0x52, 0xA0),
         'googlesearchconsole': (0x45, 0x8C, 0xF5), 'google': (0x42, 0x85, 0xF4)}
FILES = {'googleanalytics': 'googleanalytics.svg', 'googletagmanager': 'googletagmanager.svg', 'googlebigquery': 'googlebigquery.svg',
         'looker': 'looker.svg', 'powerbi': 'powerbi_v11.svg', 'meta': 'meta.svg', 'googleads': 'googleads.svg', 'hotjar': 'hotjar.svg',
         'googlesearchconsole': 'googlesearchconsole.svg', 'google': 'google.svg'}
BRAND['powerbi'] = BRAND['powerbi_v13']
def render(slug, size=600):
    svg = open(os.path.join(SRC, FILES[slug]), encoding='utf-8').read()
    col = BRAND[slug]; hexc = '#%02x%02x%02x' % col
    svg = re.sub(r'<svg ', '<svg fill="%s" width="24" height="24" ' % hexc, svg, 1)
    dom = skia.SVGDOM.MakeFromStream(skia.MemoryStream(svg.encode('utf-8')))
    s = skia.Surface(size, size); c = s.getCanvas(); c.clear(skia.ColorTRANSPARENT)
    pad = size * .06; r = size * .2
    def rr(inset): return skia.RRect.MakeRectXY(skia.Rect(pad + inset, pad + inset, size - pad - inset - size * .04, size - pad - inset - size * .04), r, r)
    sh = skia.Paint(AntiAlias=True, Color=skia.Color(18, 18, 19)); c.save(); c.translate(size * .04, size * .04); c.drawRRect(rr(0), sh); c.restore()
    c.drawRRect(rr(0), skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    c.drawRRect(rr(0), skia.Paint(AntiAlias=True, Color=skia.Color(18, 18, 19), Style=skia.Paint.kStroke_Style, StrokeWidth=size * .018))
    inner = (size - 2 * pad - size * .04) * .6; k = inner / 24
    cx = pad + (size - 2 * pad - size * .04) / 2
    c.save(); c.translate(cx - 12 * k, cx - 12 * k); c.scale(k, k); dom.setContainerSize(skia.Size(24, 24)); dom.render(c); c.restore()
    s.makeImageSnapshot().save(os.path.join(OUT, slug + '.png'), skia.kPNG)
prov = {}
for k in FILES:
    render(k); prov[k] = dict(fonte='simple-icons@13 (CC0)', arquivo=FILES[k], uso='logo em adesivo, cena de ferramentas (ecossistema)')
json.dump(prov, open(os.path.join(OUT, 'PROVENANCE.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(sorted(prov))
