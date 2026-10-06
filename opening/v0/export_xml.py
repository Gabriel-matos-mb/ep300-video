"""EP300 · V0 — exporta a timeline para XML FCP7 (xmeml v4), importável no Premiere (Arquivo › Importar).

Sequência 1  EP300_ABERTURA_V0      V1 câmeras (brutos ORIGINAIS 4K/1080) + freeze · V2..Vn overlays ProRes 4444 alpha
                                     A1 diálogo (CAM_GERAL) · A2 trilhas · A3 SFX · A4 REF_MIX_V0 (desligada)
Sequência 2  EP300_SYNC_3CAM         as 3 câmeras sincronizadas pelo áudio (base para criar multicam no Premiere)
Os caminhos apontam para a estrutura oficial no Drive (I:). Ver README_EDITAVEL.md.
"""
import os, math
from urllib.parse import quote
from xml.sax.saxutils import escape
import build, plan

FPS = plan.FPS
MEDIA_SECS = {'W': 1047.133, 'G': 482.315, 'L': 484.150}


def purl(p):
    return 'file://localhost/' + quote(os.path.abspath(p).replace('\\', '/'), safe='/:')


def rate(tb=30, ntsc=False):
    return f'<rate><timebase>{tb}</timebase><ntsc>{"TRUE" if ntsc else "FALSE"}</ntsc></rate>'


class Files:
    def __init__(self): self.seen = set(); self.n = 0
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


def write(T, dest_assets=None, out_path=None):
    """dest_assets = pasta V0_GERADOS no Drive (onde overlays/stills/áudio vão morar)."""
    A = dest_assets or build.D_ASSETS
    F, S = Files(), Seq()
    total = T['total']
    # ------------------------------------------------ V1: câmeras + freeze
    v1 = []
    for s in T['shots']:
        n = s['tl_out'] - s['tl_in']
        if s['cam'] == 'FREEZE':
            p = os.path.join(A, 'STILLS', os.path.basename(build.freeze_path(s['still'])))
            fr = F.ref('file-freeze-hold', p, n, 30, False, (1920, 1080))
            v1.append(S.clip('FREEZE_GRITEM (respiro p/ plateia)', s['tl_in'], s['tl_out'], 0, n, fr))
            continue
        fr, tb, ntsc, fps = cam_file(F, s['cam'])
        src = s['src_in'] - plan.OFFSETS[s['cam']]
        cin = int(round(src * fps)); cout = cin + int(round(n / FPS * fps))
        name = {'W': 'CAM_GERAL', 'G': 'CAM_GUSTAVO', 'L': 'CAM_LUCIAN'}[s['cam']]
        v1.append(S.clip(f'{name} [{s["seg"]}]', s['tl_in'], s['tl_out'], cin, cout, fr, tb, ntsc,
                         dur=int(MEDIA_SECS[s['cam']] * fps)))
    # ------------------------------------------------ V2..: overlays (alocação gulosa sem sobreposição)
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
    # ------------------------------------------------ A1: diálogo (CAM_GERAL, canal 1; a câmera grava mono duplicado)
    a1 = []
    frW, tbW, _, _ = cam_file(F, 'W')
    bleeps = [(T['src2tl'](a), T['src2tl'](a) + build.fr(b - a), a, b) for a, b, _ in plan.BLEEPS]
    for sg in T['segs']:
        if sg['id'] == 'HOLD': continue
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
    # ------------------------------------------------ A2: trilhas (arquivos copiados para V0_GERADOS/AUDIO)
    AUD = os.path.join(A, 'AUDIO')
    def aclip(name, f, start, n, db, cin=0, fdur=None):
        p = os.path.join(AUD, f)
        fid = 'file-aud-' + f.replace(' ', '_')
        fr = F.ref(fid, p, fdur or (cin + n), 30, False, None, 2)
        return S.clip(name, start, start + n, cin, cin + n, fr, audio_track=1, extra=gain_filter(db), dur=fdur or (cin + n))
    a2 = []
    s1 = T['segs'][0]['tl_in']; speech0 = s1 + build.fr(507.85 - plan.SEGMENTS[0][1])
    a2.append(aclip('TRILHA abertura (Got The Swag · Opener)', 'MA_LEXMusic_GotTheSwag_Opener.wav', 0, speech0 + 36, -10, fdur=320))
    title = next(c for c in T['cues'] if c['id'] == 'C08_01')['tl_in']
    b0 = speech0 - 30; loopn = int(33.684 * 30); t = b0
    while t < title:
        n = min(loopn, title - t)
        a2.append(aclip('TRILHA fundo (A Groove Pool · loop)', 'Trigubovich_A_Groove_Pool_loop_long.wav', t, n, -31, fdur=loopn))
        t += n
    a2.append(aclip('TRILHA final (In The Spotlight 12s)', 'MA_Puremusic_InTheSpotlight_12s.wav', title, min(364, total - title), -9, fdur=364))
    # ------------------------------------------------ A3: SFX
    a3 = []
    for tsec, k in build.sfx_events(T):
        if k == 'beep':
            a3.append(aclip('SFX beep contagem', 'SFX_LEADER_BEEP_1kHz.wav', build.fr(tsec), 3, 0, fdur=3)); continue
        f, g, rng = build.SFX[k]
        n = build.fr(rng[1]) if rng else max(3, build.fr(ffdur(os.path.join(build.MA, f))))
        a3.append(aclip(f'SFX {k}', f, build.fr(tsec), n, g, fdur=max(n, build.fr(ffdur(os.path.join(build.MA, f))))))
    for b0_, b1_, a, b in bleeps:
        a3.append(aclip('SFX bleep (palavrão)', 'SFX_BLEEP_1kHz.wav', b0_, b1_ - b0_, 0, fdur=b1_ - b0_))
    # ------------------------------------------------ A4: mix de referência (desligada)
    ref = F.ref('file-refmix', os.path.join(AUD, 'REF_MIX_V0.wav'), total, 30, False, None, 2)
    a4 = [S.clip('REF_MIX_V0 (mix do proxy — referência, desligada)', 0, total, 0, total, ref, audio_track=1, enabled=False)]

    def vtrack(x): return f'<track>{x}<enabled>TRUE</enabled><locked>FALSE</locked></track>'
    def atrack(x): return f'<track>{x}<enabled>TRUE</enabled><locked>FALSE</locked><outputchannelindex>1</outputchannelindex></track>'
    fmt = (f'<format><samplecharacteristics>{rate()}<width>1920</width><height>1080</height><anamorphic>FALSE</anamorphic>'
           f'<pixelaspectratio>square</pixelaspectratio><fielddominance>none</fielddominance></samplecharacteristics></format>')
    import re
    def alloc(items):   # distribui clipes sobrepostos em faixas separadas (sem sobreposição por faixa)
        out = []
        for it in sorted(items, key=lambda x: int(re.search(r'<start>(\d+)</start>', x).group(1))):
            st = int(re.search(r'<start>(\d+)</start>', it).group(1)); en = int(re.search(r'<end>(\d+)</end>', it).group(1))
            for tr in out:
                if tr[0] <= st: tr[0] = en; tr[1].append(it); break
            else: out.append([en, [it]])
        return [tr[1] for tr in out]
    atracks = [a1] + alloc(a2) + alloc(a3) + [a4]
    seq1 = (f'<sequence id="sequence-1"><name>EP300_ABERTURA_V0</name><duration>{total}</duration>{rate()}'
            f'<timecode>{rate()}<string>00:00:00:00</string><frame>0</frame><displayformat>NDF</displayformat></timecode>'
            f'<media><video>{fmt}{"".join(vtrack(v) for v in vtracks)}</video>'
            f'<audio><numOutputChannels>2</numOutputChannels>'
            f'{"".join(atrack("".join(a)) for a in atracks)}</audio></media></sequence>')
    # ------------------------------------------------ sequência 2: SYNC 3 câmeras
    sv, sa = [], []
    for cam in ('W', 'G', 'L'):
        fr, tb, ntsc, fps = cam_file(F, cam)
        st = build.fr(plan.OFFSETS[cam]); n = build.fr(MEDIA_SECS[cam]) - 1
        name = {'W': 'CAM_GERAL', 'G': 'CAM_GUSTAVO', 'L': 'CAM_LUCIAN'}[cam]
        sv.append(vtrack(S.clip(name, st, st + n, 0, int(n / FPS * fps), fr, tb, ntsc, dur=int(MEDIA_SECS[cam] * fps))))
        sa.append(atrack(S.clip(name, st, st + n, 0, int(n / FPS * fps), fr, tb, ntsc, audio_track=1, dur=int(MEDIA_SECS[cam] * fps))))
    dur2 = build.fr(MEDIA_SECS['W'])
    seq2 = (f'<sequence id="sequence-2"><name>EP300_SYNC_3CAM (sincronia por áudio)</name><duration>{dur2}</duration>{rate()}'
            f'<media><video>{fmt}{"".join(sv)}</video><audio><numOutputChannels>2</numOutputChannels>{"".join(sa)}</audio></media></sequence>')
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n<xmeml version="4"><project><name>EP300_ABERTURA_V0</name>'
           f'<children>{seq1}{seq2}</children></project></xmeml>\n')
    out = out_path or os.path.join(build.B, 'EP300_ABERTURA_V0.xml')
    open(out, 'w', encoding='utf-8').write(xml)
    print('xml ok', out, f'{len(vtracks)} trilhas de vídeo, {S.k} clipitems')
    return out


_DUR = {}
def ffdur(p):
    if p not in _DUR:
        import subprocess
        _DUR[p] = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                                       capture_output=True, text=True).stdout.strip())
    return _DUR[p]
