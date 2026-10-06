"""EP300 · V2 — exporta a timeline para XML FCP7 (xmeml v4), importável no Premiere (Arquivo › Importar).

Sequência 1  EP300_ABERTURA_V2   V1 pré-sessão (bastidores) + câmeras (brutos ORIGINAIS) + freeze · V2..Vn overlays alpha
                                 A1.. diálogo (CAM_GERAL) + áudio dos bastidores · trilhas · SFX · REF_MIX_V1 (desligada)
                                 Marcadores: os 48 comentários do Gabriel na V0 (preservados), reposicionados na V2 via tempo-fonte.
Sequência 2  EP300_SYNC_3CAM_V2  as 3 câmeras sincronizadas — com a correção de 5 quadros na imagem da CAM_GERAL.
Reenquadramentos da CAM_GERAL (WG/WL/Wz) = efeito Movimento (escala/posição) no clipe — sem render.
"""
import os, re, json
from urllib.parse import quote
from xml.sax.saxutils import escape
import build, plan

FPS = plan.FPS
MEDIA_SECS = {'W': 1047.133, 'G': 482.315, 'L': 484.150}
CAMNAME = {'W': 'CAM_GERAL', 'Wz': 'CAM_GERAL (reenquadro)', 'WG': 'CAM_GERAL (punch-in Gustavo)',
           'WL': 'CAM_GERAL (punch-in Lucian)', 'G': 'CAM_GUSTAVO', 'L': 'CAM_LUCIAN'}


def purl(p):
    return 'file://localhost/' + quote(os.path.abspath(p).replace('\\', '/'), safe='/:')


def rate(tb=30, ntsc=False):
    return f'<rate><timebase>{tb}</timebase><ntsc>{"TRUE" if ntsc else "FALSE"}</ntsc></rate>'


class Files:
    def __init__(self): self.seen = set()
    def ref(self, fid, path, dur_frames, tb=30, ntsc=False, video=None, audio_ch=0):
        if fid in self.seen:
            return f'<file id="{fid}"/>'
        self.seen.add(fid)
        media = ''
        if video:
            media += (f'<video><samplecharacteristics>{rate(tb, ntsc)}<width>{video[0]}</width><height>{video[1]}</height>'
                      f'<pixelaspectratio>square</pixelaspectratio></samplecharacteristics></video>')
        if audio_ch:
            media += (f'<audio><samplecharacteristics><depth>16</depth><samplerate>48000</samplerate></samplecharacteristics>'
                      f'<channelcount>{audio_ch}</channelcount></audio>')
        return (f'<file id="{fid}"><name>{escape(os.path.basename(path))}</name><pathurl>{purl(path)}</pathurl>'
                f'{rate(tb, ntsc)}<duration>{dur_frames}</duration><media>{media}</media></file>')


def gain_filter(db):
    lin = 10 ** (db / 20)
    return ('<filter><effect><name>Audio Levels</name><effectid>audiolevels</effectid><effectcategory>audiolevels</effectcategory>'
            '<effecttype>audiolevels</effecttype><mediatype>audio</mediatype><parameter authoringApp="PremierePro">'
            f'<parameterid>level</parameterid><name>Level</name><valuemin>0</valuemin><valuemax>3.98109</valuemax>'
            f'<value>{lin:.5f}</value></parameter></effect></filter>')


def motion_filter(scale_pct, h=0.0, v=0.0):
    return ('<filter><effect><name>Basic Motion</name><effectid>basic</effectid><effectcategory>motion</effectcategory>'
            '<effecttype>motion</effecttype><mediatype>video</mediatype>'
            f'<parameter authoringApp="PremierePro"><parameterid>scale</parameterid><name>Scale</name><valuemin>0</valuemin>'
            f'<valuemax>1000</valuemax><value>{scale_pct:.2f}</value></parameter>'
            f'<parameter authoringApp="PremierePro"><parameterid>center</parameterid><name>Center</name>'
            f'<value><horiz>{h:.5f}</horiz><vert>{v:.5f}</vert></value></parameter></effect></filter>')


class Seq:
    def __init__(self): self.k = 0
    def clip(self, name, start, end, cin, cout, fileref, tb=30, ntsc=False, audio_track=None, extra='', enabled=True, dur=None):
        self.k += 1
        st = (f'<sourcetrack><mediatype>audio</mediatype><trackindex>{audio_track}</trackindex></sourcetrack>'
              if audio_track else '')
        return (f'<clipitem id="clipitem-{self.k}"><name>{escape(name)}</name><enabled>{"TRUE" if enabled else "FALSE"}</enabled>'
                f'<duration>{dur if dur is not None else cout}</duration>{rate(tb, ntsc)}<start>{start}</start><end>{end}</end>'
                f'<in>{cin}</in><out>{cout}</out>{fileref}{st}{extra}</clipitem>')


def cam_file(F, cam):
    tb, ntsc = build.SRC_RATE[cam]
    fps = 24000 / 1001 if ntsc else tb
    vid = (3840, 2160) if cam in 'GL' else (1920, 1080)
    return F.ref(f'file-{cam}', build.SRC[cam], int(MEDIA_SECS[cam] * fps), tb, ntsc, vid, 2), tb, ntsc, fps


def v0_markers_to_v1(T):
    """reposiciona os comentários do Gabriel (timecode da V0) na V1 via tempo-fonte."""
    p = os.path.join(build.WORK, 'v1', 'human', 'feedback_markers.json')
    v0 = json.load(open(os.path.join(build.WORK, 'build', 'timeline_v0.json'), encoding='utf-8'))
    notes = json.load(open(os.path.join(os.path.dirname(__file__), 'feedback_v1.json'), encoding='utf-8'))
    def tcf(s):
        m, sec, f = [int(x) for x in s.split(':')]; return (m * 60 + sec) * 30 + f
    segs = [(tcf(s['tl_in']), tcf(s['tl_out']), s['fonte_in_s'], s['id']) for s in v0['segmentos']]
    out = []
    for i, mk in enumerate(json.load(open(p, encoding='utf-8'))):
        f = mk['f']; src = None
        for a, b, s0, sid in segs:
            if a <= f < b and sid != 'HOLD': src = s0 + (f - a) / 30; break
        if src is not None: tl = T['src2tl'](src, strict=False)
        elif f < segs[0][0]: tl = 0   # pré-sessão da V0 → início da V1
        else: tl = T['end'] + 5       # final da V0 → final da V1
        note = notes.get(str(i), '')
        cm = (mk.get('comment') or '').strip()
        if not cm: continue
        out.append((tl, f"V0 {mk['f'] // 1800:02d}:{mk['f'] // 30 % 60:02d}", cm, note))
    return out


def write(T, dest_assets=None, out_path=None):
    A = dest_assets or build.D_ASSETS
    F, S = Files(), Seq()
    total = T['total']
    lead = plan.W_VIDEO_LEAD_FRAMES
    # ------------------------------------------------ V1: pré-sessão + câmeras + freeze
    v1 = []
    for s in T['pre']:
        _, mfps, wh, mdur = build.MEDIA[s['key']]; path = build.MEDIA_XML[s['key']]
        fref = F.ref(f"file-{s['key']}", path, int(mdur * mfps), mfps, False, wh, 2)
        n = s['tl_out'] - s['tl_in']
        cin = int(round(s['m_in'] * mfps)); cout = cin + int(round(n / FPS * mfps))
        v1.append(S.clip(f"COLD OPEN · {os.path.basename(path)} (aplicar P&B no Premiere)", s['tl_in'], s['tl_out'], cin, cout,
                         fref, mfps, False, dur=int(mdur * mfps)))
    for s in T['shots']:
        n = s['tl_out'] - s['tl_in']
        if s['cam'] == 'PAUSE': continue      # respiro sem voz: coberto por tela cheia (sem clipe de câmera)
        if s['cam'] == 'FREEZE':
            p = os.path.join(A, 'STILLS', os.path.basename(build.freeze_path(s['still'])))
            fr = F.ref('file-freeze-hold', p, n, 30, False, (1920, 1080))
            v1.append(S.clip('FREEZE_GRITEM (respiro 3 s p/ plateia)', s['tl_in'], s['tl_out'], 0, n, fr))
            continue
        cam = s['cam']; bc = build.base_cam(cam)
        fr, tb, ntsc, fps = cam_file(F, bc)
        src = s['src_in'] - plan.OFFSETS[bc]
        if bc == 'W':
            cin = int(round(src * 30)) + lead      # SYNC V1: imagem da geral 5 quadros adiante do áudio
            cout = cin + n
        else:
            cin = int(round(src * fps)); cout = cin + int(round(n / FPS * fps))
        extra = ''
        if bc == 'W' and cam != 'W':
            sc, cx, cy = plan.CROPS[cam]
            extra = motion_filter(100 * sc, (960 - cx) * sc / 1920, (540 - cy) * sc / 1080)
        elif bc in 'GL':
            extra = motion_filter(50)
        v1.append(S.clip(f'{CAMNAME[cam]} [{s["seg"]}]', s['tl_in'], s['tl_out'], cin, cout, fr, tb, ntsc, extra=extra,
                         dur=int(MEDIA_SECS[bc] * fps)))
    # ------------------------------------------------ V2..: overlays
    tracks = []
    for c in sorted(T['cues'], key=lambda c: c['tl_in']):
        n = c['tl_out'] - c['tl_in']
        p = os.path.join(A, 'OVERLAYS', os.path.basename(build.ovl_path(c)))
        fr = F.ref(f"file-{c['id']}", p, n, 30, False, (1920, 1080))
        item = S.clip(f"{c['id']}_{c['name']}", c['tl_in'], c['tl_out'], 0, n, fr)
        for tr in tracks:
            if tr[-1][0] <= c['tl_in']:
                tr.append((c['tl_out'], item)); break
        else:
            tracks.append([(c['tl_out'], item)])
    vtracks = [''.join(v1)] + [''.join(i for _, i in tr) for tr in tracks]
    # ------------------------------------------------ A1: diálogo + bastidores
    a1 = []
    frW, tbW, _, _ = cam_file(F, 'W')
    for s in T['pre']:
        _, mfps, wh, mdur = build.MEDIA[s['key']]; path = build.MEDIA_XML[s['key']]
        fref = F.ref(f"file-{s['key']}", path, int(mdur * mfps), mfps, False, wh, 2)
        n = s['tl_out'] - s['tl_in']; cin = int(round(s['m_in'] * mfps)); cout = cin + int(round(n / FPS * mfps))
        a1.append(S.clip(f"BASTIDOR {s['key']}", s['tl_in'], s['tl_out'], cin, cout, fref, mfps, False, audio_track=1,
                         dur=int(mdur * mfps)))
    bleeps = [(T['src2tl'](a), T['src2tl'](a) + build.fr(b - a), a, b) for a, b, _ in plan.BLEEPS]
    for sg in T['segs']:
        if sg['kind'] != 'dialogue': continue
        pieces = [(sg['tl_in'], sg['tl_out'])]
        for b0, b1, _, _ in bleeps:
            new = []
            for x0, x1 in pieces:
                if x0 < b0 < x1: new += [(x0, b0), (b1, x1)]
                else: new.append((x0, x1))
            pieces = new
        for x0, x1 in pieces:
            cin = int(round(sg['src_in'] * 30)) + (x0 - sg['tl_in'])
            a1.append(S.clip(f"DIALOGO {sg['id']}", x0, x1, cin, cin + (x1 - x0), frW, 30, False, audio_track=1,
                             extra=gain_filter(2), dur=int(MEDIA_SECS['W'] * 30)))
    # ------------------------------------------------ trilhas
    AUD = os.path.join(A, 'AUDIO')
    def aclip(name, f, start, n, db, cin=0, fdur=None):
        p = os.path.join(AUD, f)
        fid = 'file-aud-' + re.sub(r'[^A-Za-z0-9_.-]', '_', f)
        fr = F.ref(fid, p, fdur or (cin + n), 30, False, None, 2)
        return S.clip(name, start, start + n, cin, cin + n, fr, audio_track=1, extra=gain_filter(db), dur=fdur or (cin + n))
    aviso, speech0, title = build.music_marks(T)
    a2 = []
    n_av = build.fr(speech0 + .6 - aviso)
    a2.append(aclip('TRILHA aviso pré-sessão (Beat The Odds 30s)', build.MUSIC['aviso'], build.fr(aviso), n_av, -13,
                    fdur=build.fr(export_dur(build.MUSIC['aviso']))))
    loopn = build.fr(export_dur(build.MUSIC['bed'])); t = build.fr(speech0 - 1.0); tend = build.fr(title - .2)
    while t < tend:
        n = min(loopn, tend - t)
        a2.append(aclip('TRILHA fundo (A Groove Pool · loop)', build.MUSIC['bed'], t, n, -31, fdur=loopn)); t += n
    fdur = build.fr(export_dur(build.MUSIC['final']))
    a2.append(aclip('TRILHA final (In The Spotlight 12s) — fade-in 1,2 s', build.MUSIC['final'], build.fr(title),
                    min(fdur, total - build.fr(title)), -9, fdur=fdur))
    # ------------------------------------------------ SFX
    a3 = []
    for tsec, k in build.sfx_events(T):
        if k == 'beep':
            a3.append(aclip('SFX beep contagem', 'SFX_LEADER_BEEP_1kHz.wav', build.fr(tsec), 3, 0, fdur=3)); continue
        if k in build.SFX:
            f, g, rng = build.SFX[k]
            full = build.fr(export_dur(f))
            n = build.fr(rng[1]) if rng else max(3, full)
            a3.append(aclip(f'SFX {k}', f, max(0, build.fr(tsec)), n, g, fdur=max(n, full)))
        else:      # sintético (sfx_v2.py) — ganho já embutido no WAV
            f = f'SFX_SYN_{k}.wav'
            import wave as _w
            w_ = _w.open(os.path.join(build.L_AUD, f)); full = int(round(w_.getnframes() / w_.getframerate() * FPS)); w_.close()
            a3.append(aclip(f'SFX {k} (sintético)', f, max(0, build.fr(tsec)), full, 0, fdur=full))
    for b0_, b1_, a, b in bleeps:
        a3.append(aclip('SFX bleep (palavrão)', 'SFX_BLEEP_1kHz.wav', b0_, b1_ - b0_, 0, fdur=b1_ - b0_))
    ref = F.ref('file-refmix', os.path.join(AUD, 'REF_MIX_V2.wav'), total, 30, False, None, 2)
    a4 = [S.clip('REF_MIX_V2 (mix do proxy, com ducking — referência, desligada)', 0, total, 0, total, ref, audio_track=1, enabled=False)]

    def vtrack(x): return f'<track>{x}<enabled>TRUE</enabled><locked>FALSE</locked></track>'
    def atrack(x): return f'<track>{x}<enabled>TRUE</enabled><locked>FALSE</locked><outputchannelindex>1</outputchannelindex></track>'
    fmt = (f'<format><samplecharacteristics>{rate()}<width>1920</width><height>1080</height><anamorphic>FALSE</anamorphic>'
           f'<pixelaspectratio>square</pixelaspectratio><fielddominance>none</fielddominance></samplecharacteristics></format>')
    def alloc(items):
        out = []
        for it in sorted(items, key=lambda x: int(re.search(r'<start>(\d+)</start>', x).group(1))):
            st = int(re.search(r'<start>(\d+)</start>', it).group(1)); en = int(re.search(r'<end>(\d+)</end>', it).group(1))
            for tr in out:
                if tr[0] <= st: tr[0] = en; tr[1].append(it); break
            else: out.append([en, [it]])
        return [tr[1] for tr in out]
    atracks = alloc(a1) + alloc(a2) + alloc(a3) + [a4]
    markers = ''
    for tl, lab, cm, note in v0_markers_to_v1(T):
        txt = f'[{lab}] {cm}' + (f'  ||  V1/V2: {note}' if note else '')
        markers += (f'<marker><name>{escape("Gabriel · " + lab)}</name><comment>{escape(txt)}</comment>'
                    f'<in>{tl}</in><out>-1</out></marker>')
    seq1 = (f'<sequence id="sequence-1"><name>{build.NAME}</name><duration>{total}</duration>{rate()}'
            f'<timecode>{rate()}<string>00:00:00:00</string><frame>0</frame><displayformat>NDF</displayformat></timecode>'
            f'{markers}<media><video>{fmt}{"".join(vtrack(v) for v in vtracks)}</video>'
            f'<audio><numOutputChannels>2</numOutputChannels>'
            f'{"".join(atrack("".join(a)) for a in atracks)}</audio></media></sequence>')
    # ------------------------------------------------ sequência 2: SYNC 3 câmeras (V1 corrigida)
    sv, sa = [], []
    for cam in ('W', 'G', 'L'):
        fr, tb, ntsc, fps = cam_file(F, cam)
        st = build.fr(plan.OFFSETS[cam]); n = build.fr(MEDIA_SECS[cam]) - 1 - (lead if cam == 'W' else 0)
        name = {'W': 'CAM_GERAL', 'G': 'CAM_GUSTAVO', 'L': 'CAM_LUCIAN'}[cam]
        vin = lead if cam == 'W' else 0
        sv.append(vtrack(S.clip(name + (' (imagem +5 quadros: sync corrigido)' if cam == 'W' else ''), st, st + n, vin,
                                vin + int(n / FPS * fps), fr, tb, ntsc, dur=int(MEDIA_SECS[cam] * fps))))
        sa.append(atrack(S.clip(name, st, st + n, 0, int(n / FPS * fps), fr, tb, ntsc, audio_track=1, dur=int(MEDIA_SECS[cam] * fps))))
    dur2 = build.fr(MEDIA_SECS['W'])
    seq2 = (f'<sequence id="sequence-2"><name>EP300_SYNC_3CAM_V2 (sync corrigido)</name><duration>{dur2}</duration>{rate()}'
            f'<media><video>{fmt}{"".join(sv)}</video><audio><numOutputChannels>2</numOutputChannels>{"".join(sa)}</audio></media></sequence>')
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n<xmeml version="4"><project><name>EP300_ABERTURA_V2</name>'
           f'<children>{seq1}{seq2}</children></project></xmeml>\n')
    out = out_path or os.path.join(build.B, f'{build.NAME}.xml')
    open(out, 'w', encoding='utf-8').write(xml)
    print('xml ok', out, f'{len(vtracks)} trilhas de vídeo, {S.k} clipitems, {markers.count("<marker>")} marcadores')
    return out


_DUR = {}
def export_dur(f):
    p = os.path.join(build.MA, f)
    if p not in _DUR:
        import subprocess
        _DUR[p] = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                                       capture_output=True, text=True).stdout.strip())
    return _DUR[p]
