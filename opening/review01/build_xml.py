"""Review 02 — sequencia editavel (xmeml v4 / FCP7 XML) para importar no Premiere.
V1 base 4K do Gabriel (video SO, sem audio) + holds (stills) + pre-sessao; V2 underlays; V3+ telas cheias; V-acima overlays/stickers; A1/A2 dialogo; A3/A4 musica;
A5/A6 stem de SFX (DESLIGADO — referencia); A7+ SFX individuais. NAO VALIDADO NO PREMIERE (sem Premiere automatizavel aqui)."""
import json, os, glob, shutil, subprocess, urllib.parse
from common import *
import compose_video as cv

MV = os.path.join(ED, 'media', 'video'); MS = os.path.join(ED, 'media', 'stills'); MA = os.path.join(ED, 'media', 'audio')
for d in (MV, MS, MA): os.makedirs(d, exist_ok=True)
SEQ_NAME = 'EP300_ABERTURA_REVIEW_02' if REV == '02' else f'EP300_V4_PRESENTABLE_REVIEW_{REV}'
SUF = '' if REV == '02' else f'_R{REV}'
if REV != '02':   # stills de hold da R02 (mesmos quadros 4K) acompanham o pacote R03
    for f in glob.glob(os.path.join(HERE, 'editable', 'media', 'stills', 'HOLD_*.png')): shutil.copy(f, MS)
BASE4K = open(os.path.join(WORK, 'base_path.txt'), encoding='utf-8').read().strip()
SEQ_W, SEQ_H = 3840, 2160
TB = 24

def url(p):
    p = os.path.abspath(p).replace('\\', '/')
    return 'file://localhost/' + urllib.parse.quote(p, safe='/').replace(':', '%3a', 1) if p[1] == ':' else 'file://localhost' + urllib.parse.quote(p)

_ids = {'n': 0}; _files = {}
def nid(p): _ids['n'] += 1; return f'{p}-{_ids["n"]}'
def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def vfile_xml(path, dur_f, w, h, name=None):
    if path in _files: return f'<file id="{_files[path]}"/>'
    fid = nid('file'); _files[path] = fid
    return (f'<file id="{fid}"><name>{esc(name or os.path.basename(path))}</name><pathurl>{url(path)}</pathurl><rate><timebase>{TB}</timebase><ntsc>TRUE</ntsc></rate>'
            f'<duration>{dur_f}</duration><media><video><samplecharacteristics><rate><timebase>{TB}</timebase><ntsc>TRUE</ntsc></rate><width>{w}</width><height>{h}</height>'
            f'<anamorphic>FALSE</anamorphic><pixelaspectratio>square</pixelaspectratio><fielddominance>none</fielddominance></samplecharacteristics></video></media></file>')

def afile_xml(path, dur_f, name=None):
    if path in _files: return f'<file id="{_files[path]}"/>'
    fid = nid('file'); _files[path] = fid
    return (f'<file id="{fid}"><name>{esc(name or os.path.basename(path))}</name><pathurl>{url(path)}</pathurl><rate><timebase>{TB}</timebase><ntsc>TRUE</ntsc></rate>'
            f'<duration>{dur_f}</duration><media><audio><samplecharacteristics><depth>24</depth><samplerate>48000</samplerate></samplecharacteristics><channelcount>2</channelcount></audio></media></file>')

def motion(scale_pct, cx_norm=0.0, cy_norm=0.0):
    return ('<filter><effect><name>Basic Motion</name><effectid>basic</effectid><effectcategory>motion</effectcategory><effecttype>motion</effecttype><mediatype>video</mediatype>'
            f'<parameter><parameterid>scale</parameterid><name>Scale</name><valuemin>0</valuemin><valuemax>1000</valuemax><value>{scale_pct:.2f}</value></parameter>'
            f'<parameter><parameterid>center</parameterid><name>Center</name><value><horiz>{cx_norm:.5f}</horiz><vert>{cy_norm:.5f}</vert></value></parameter></effect></filter>')

def vclip(name, path, w, h, start, dur, src_in, src_dur_f, scale_pct, cx=0.0, cy=0.0, note=''):
    cid = nid('clipitem')
    return (f'<clipitem id="{cid}"><name>{esc(name)}</name><enabled>TRUE</enabled><duration>{src_dur_f}</duration><rate><timebase>{TB}</timebase><ntsc>TRUE</ntsc></rate>'
            f'<start>{start}</start><end>{start + dur}</end><in>{src_in}</in><out>{src_in + dur}</out>{vfile_xml(path, src_dur_f, w, h)}{motion(scale_pct, cx, cy)}'
            f'<comments><mastercomment1>{esc(note)}</mastercomment1></comments></clipitem>')

def aclip(name, path, start, dur, src_in, src_dur_f, ch, enabled=True):
    cid = nid('clipitem')
    return (f'<clipitem id="{cid}"><name>{esc(name)}</name><enabled>{"TRUE" if enabled else "FALSE"}</enabled><duration>{src_dur_f}</duration><rate><timebase>{TB}</timebase><ntsc>TRUE</ntsc></rate>'
            f'<start>{start}</start><end>{start + dur}</end><in>{src_in}</in><out>{src_in + dur}</out>{afile_xml(path, src_dur_f)}'
            f'<sourcetrack><mediatype>audio</mediatype><trackindex>{ch}</trackindex></sourcetrack></clipitem>')

def still(path, dur_f):  # PNG como clip de video de duracao fixa
    return dur_f

def nframes_png(p): return 10 ** 6  # stills: duracao "infinita"

def png_size(p):
    from PIL import Image
    return Image.open(p).size

def audio_frames(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True)
    return int(round(float(r.stdout.strip()) * FPS))

def main():
    P = json.load(open(os.path.join(OUTW, 'placement_final.json'), encoding='utf-8'))
    byid = {e['id']: e for e in P}
    tracks = {}      # nome -> lista de clipitems xml (com start para ordenar)
    def put_track(tr, start, xml): tracks.setdefault(tr, []).append((start, xml))

    # ---- V1: pre-sessao
    blooper = os.path.join(MV, 'COLD_OPEN_blooper_inicial.mov'); shutil.copy(os.path.join(WORK, 'blooper.mov'), blooper)
    for name, n in PRE_ORDER:
        path = blooper if name == 'BLOOPER' else os.path.join(LAYERS, name + '.mov')
        put_track('V1', pre_start(name), vclip(name, path, 1280, 720, pre_start(name), n, 0, n, 300, note='pre-sessao'))
    # ---- V1: base 4K (video so) segmentada nos holds / insert
    h1, h2 = HOLDS
    segs = [(0, h1[0]), (h1[0], h2[0]), (h2[0], INS_AT), (INS_AT, BASE_FR)]
    shift = [PRE_FR, PRE_FR + h1[0] + h1[1], PRE_FR + h2[0] + h1[1] + h2[1], PRE_FR + INS_AT + h1[1] + h2[1] + INS_FR]
    for k, ((a, b), st) in enumerate(zip(segs, shift)):
        put_track('V1', st + 0, vclip(f'BASE_4K_{k + 1} (export consolidado do Gabriel)', BASE4K, 3840, 2160, st, b - a, a, BASE_FR, 100, note='VIDEO SO (audio do export desligado: dialogo vem do stem)'))
    # holds
    p1 = os.path.join(MS, 'HOLD_P_EVOL_frame1031.png'); p2 = os.path.join(MS, 'HOLD_GRITEM_4k_123.2s.png')
    put_track('V1', PRE_FR + h1[0], vclip('HOLD P_EVOL (2.4 s, freeze do quadro 1031)', p1, 3840, 2160, PRE_FR + h1[0], h1[1], 0, 10 ** 5, 100))
    # GRITEM: still 4K do quadro 123.2s, reenquadrado (escala 135%, rosto a esquerda) — animacao do push NAO reproduzida no XML (estatico)
    put_track('V1', PRE_FR + h2[0] + h1[1], vclip('HOLD GRITEM (3.0 s, freeze 4K 123.2s reenquadrado)', p2, 3840, 2160, PRE_FR + h2[0] + h1[1], h2[1], 0, 10 ** 5, 135, -0.0975, 0.0, note='escala 135% (no render: push animado 0->135% em 9 quadros)'))

    # ---- layers
    full_tr = ['V3', 'V4', 'V5']; ov_tr = ['V6', 'V7', 'V8', 'V9']
    busy = {t: 0 for t in full_tr + ov_tr + ['V2']}
    placements_meta = []
    def assign(pool, a, b):
        for t in pool:
            if busy[t] <= a: busy[t] = b; return t
        raise SystemExit('sem trilha livre')
    from compose_video import TRANSFORMS, _bbox_center
    for e in sorted(P, key=lambda x: x['a']):
        path = os.path.join(LAYERS, e['file']); n = e['n']; clone = e['clone']
        pool = full_tr if e['full'] else ov_tr
        trk = assign(pool, e['a'], e['a'] + n + clone)
        meta = json.load(open(os.path.join(LAYERS, e['id'] + '.json'), encoding='utf-8')) if os.path.exists(os.path.join(LAYERS, e['id'] + '.json')) else {}
        note = '; '.join(meta.get('placeholders', [])) if isinstance(meta.get('placeholders'), list) else ''
        if e['under']:   # underlay solido (evita camera vazando durante push-in/out)
            from PIL import Image
            up = os.path.join(MS, f"UNDERLAY_{e['id']}_{e['color']}.png"); Image.new('RGB', (1280, 720), tuple(int(e['color'][i:i + 2], 16) for i in (0, 2, 4))).save(up)
            ua, ub = e['under']; put_track('V2', ua, vclip(f"UNDERLAY {e['id']}", up, 1280, 720, ua, ub - ua, 0, 10 ** 5, 300, note='cor solida sob o layer'))
            busy['V2'] = max(busy['V2'], ub)
        tf = sorted(TRANSFORMS.get(e['id'], []), key=lambda w: w[0])
        segs_ = []; cur = e['a']
        for (wa, wb, spec) in tf:
            wa = max(wa, e['a']); wb = min(wb, e['a'] + n)
            if wb <= wa: continue
            if wa > cur: segs_.append((cur, wa, None))
            segs_.append((wa, wb, spec)); cur = wb
        if cur < e['a'] + n: segs_.append((cur, e['a'] + n, None))
        for (sa, sb, spec) in segs_:
            scp, cx, cy = 300.0, 0.0, 0.0
            if spec:
                if spec[0] == 'c': sc = spec[1]; ex, ey = _bbox_center(path, n); tx, ty = spec[2], spec[3]
                elif spec[0] == 's': sc = spec[1]; ex, ey = _bbox_center(path, n); tx, ty = ex + spec[2], ey + spec[3]
                else: sc, ex, ey, tx, ty = spec
                ccx = tx - (ex - 640) * sc; ccy = ty - (ey - 360) * sc          # centro do layer (espaco 1280x720)
                scp = 300.0 * sc; cx = (ccx - 640) * 3 / SEQ_W; cy = (ccy - 360) * 3 / SEQ_H
            put_track(trk, sa, vclip(e['id'] + (' [transform por plano]' if spec else ''), path, 1280, 720, sa, sb - sa, sa - e['a'], n, scp, cx, cy, note))
        if clone:      # ponte: ultimo quadro do layer segurado
            png = os.path.join(MS, f"BRIDGE_{e['id']}_lastframe.png")
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-vf', 'select=eq(n\,' + str(n - 1) + ')', '-frames:v', '1', '-fps_mode', 'passthrough', png])
            put_track(trk, e['a'] + n, vclip(f"BRIDGE {e['id']} (hold {clone}f)", png, 1280, 720, e['a'] + n, clone, 0, 10 ** 5, 300, note='segura o ultimo quadro: sem camera entre telas'))
        placements_meta.append(dict(id=e['id'], track=trk, start_f=e['a'], dur_f=n, start_s=round(e['a'] / FPS, 3), clone_f=clone, underlay=bool(e['under']), placeholders=meta.get('placeholders', []), transform=bool(tf)))

    # ---- audio
    atr = {}
    def aput(tr, start, xml): atr.setdefault(tr, []).append((start, xml))
    stems = [('DIALOGO_stem.wav', 'A1', 'A2', True), ('MUSICA_stem.wav', 'A3', 'A4', True), ('SFX_stem_ducked.wav', 'A5', 'A6', False)]
    TOT = total_frames()
    for fn, L, R, en in stems:
        src = {'DIALOGO_stem.wav': 'stem_dia.wav', 'MUSICA_stem.wav': 'stem_mus.wav', 'SFX_stem_ducked.wav': 'stem_sfx.wav'}[fn]
        fn = fn.replace('.wav', SUF + '.wav'); shutil.copy(os.path.join(OUTW, src), os.path.join(MA, fn))
        path = os.path.join(MA, fn); d = audio_frames(path)
        aput(L, 0, aclip(fn + (' (DESLIGADO: referencia; SFX individuais em A7+)' if not en else ''), path, 0, TOT, 0, d, 1, en))
        aput(R, 0, aclip(fn, path, 0, TOT, 0, d, 2, en))
    ev = json.load(open(os.path.join(OUTW, 'sfx_events.json'), encoding='utf-8'))
    pair_busy = []
    for x in sorted(ev, key=lambda z: z['t']):
        base = os.path.splitext(os.path.basename(x['file']))[0].replace(' ', '_')
        path = os.path.join(MA, 'sfx', base + '.wav'); d = audio_frames(path); st = int(round(x['t'] * FPS))
        for i, b in enumerate(pair_busy):
            if b <= st: pair_busy[i] = st + d; k = i; break
        else:
            pair_busy.append(st + d); k = len(pair_busy) - 1
        aput(f'A{7 + 2 * k}', st, aclip(f"SFX {x['layer']} {base}", path, st, d, 0, d, 1)); aput(f'A{8 + 2 * k}', st, aclip(f"SFX {x['layer']} {base}", path, st, d, 0, d, 2))

    def vtrack(tr): return '<track>' + ''.join(x for _, x in sorted(tracks[tr], key=lambda z: z[0])) + '</track>'
    vnames = ['V1', 'V2'] + full_tr + ov_tr
    vt = ''.join(vtrack(t) if t in tracks else '<track></track>' for t in vnames)
    anames = sorted(atr, key=lambda t: int(t[1:]))
    allA = [f'A{i}' for i in range(1, int(anames[-1][1:]) + 1)]
    at = ''.join('<track>' + ''.join(x for _, x in sorted(atr.get(t, []), key=lambda z: z[0])) + '</track>' for t in allA)
    xml = (f'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE xmeml><xmeml version="4"><sequence id="seq-1"><name>{SEQ_NAME}</name><duration>{TOT}</duration>'
           f'<rate><timebase>{TB}</timebase><ntsc>TRUE</ntsc></rate><timecode><rate><timebase>{TB}</timebase><ntsc>TRUE</ntsc></rate><string>00:00:00:00</string><frame>0</frame><displayformat>NDF</displayformat></timecode>'
           f'<media><video><format><samplecharacteristics><rate><timebase>{TB}</timebase><ntsc>TRUE</ntsc></rate><width>{SEQ_W}</width><height>{SEQ_H}</height><anamorphic>FALSE</anamorphic>'
           f'<pixelaspectratio>square</pixelaspectratio><fielddominance>none</fielddominance></samplecharacteristics></format>{vt}</video>'
           f'<audio><numOutputChannels>2</numOutputChannels><format><samplecharacteristics><depth>24</depth><samplerate>48000</samplerate></samplecharacteristics></format>{at}</audio></media></sequence></xmeml>')
    out = os.path.join(ED, SEQ_NAME + '.xml'); open(out, 'w', encoding='utf-8').write(xml)
    json.dump(dict(sequence=dict(frames=TOT, fps='23.976', size=[SEQ_W, SEQ_H], holds=[dict(id=h[2], base_frame=h[0], frames=h[1]) for h in HOLDS], insert=dict(base_frame=INS_AT, frames=INS_FR, title_frames=TITLE_FR, f01_frames=F01_FR),
                   loop_exit='ultimo quadro = ultimo quadro da base (blooper P&B do Premiere, frame 7572 da base); audio termina em silencio natural; sem fade/elemento — encaixar LOOP apos o frame %d' % (TOT - 1)),
                   layers=placements_meta), open(os.path.join(ED, 'timing_map.json' if REV == '02' else f'timing_map_review{REV}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('xml', out, len(xml) // 1024, 'KB')

if __name__ == '__main__':
    main()
