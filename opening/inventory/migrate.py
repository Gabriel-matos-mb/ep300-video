"""EP300 — fase de PRESERVACAO (03/10/2026): COPIAR p/ Drive -> VALIDAR (existencia + tamanho + MD5 origem x destino) -> HASH dos duplicados (DR).
NAO apaga nada. NAO sobrescreve: se o destino existe com tamanho/hash diferente, registra DIVERGENCIA e nao toca.
Saida: inventory/migration_manifest.json (+ safe_to_delete.json gerado por safe_list.py)."""
import os, sys, json, glob, hashlib, shutil, time, zipfile
from concurrent.futures import ThreadPoolExecutor

P = 'C:/Users/gabri/Code/audio-visual/projects'
OP = P + '/ep300-cinema-opening'; LP = P + '/ep300-cinema-loop'
DRV = glob.glob('I:/Drives compartilhados/Educa*/Marketing*/01_CANAIS_ATIVOS/02_PODCAST/2026/300_*/01_VIDEO DE ABERTURA')[0].replace('\\', '/')
LOG = OP + '/inventory/migrate.log'
MAN = OP + '/inventory/migration_manifest.json'


def log(*a):
    s = time.strftime('%H:%M:%S ') + ' '.join(str(x) for x in a)
    print(s, flush=True)
    open(LOG, 'a', encoding='utf-8').write(s + '\n')


def X(p):
    """caminho estendido (>260 chars) no Windows: prefixo BS BS ? BS"""
    q = p.replace('/', chr(92))
    return p if len(p) < 240 or not q[1:2] == ':' else chr(92) * 2 + '?' + chr(92) + q


def md5(p):
    m = hashlib.md5()
    with open(X(p), 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): m.update(b)
    return m.hexdigest()


def walk(root, skip=()):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in ('node_modules', '__pycache__', '.git') and not any(s in (dp + '/' + d).replace(os.sep, '/') for s in skip)]
        for f in fn: yield os.path.join(dp, f).replace(os.sep, '/')


def plan():
    R = OP + '/review01'; items = []   # (src, dst)
    A = DRV + '/00_ASSETS E INSERTS/R03_COMPONENTES_FINAIS_4K'
    for f in glob.glob(R + '/work/r3/rem4k/*.mov') + glob.glob(R + '/layers_r03_ep1fix_4k/*'): items.append((f.replace(os.sep, '/'), A + '/' + os.path.basename(f)))
    L = DRV + '/00_ASSETS E INSERTS/R03_LAYERS'
    for f in walk(R + '/layers_r03'): items.append((f, L + '/' + os.path.relpath(f, R + '/layers_r03').replace(os.sep, '/')))
    for f in glob.glob(R + '/layers_r03_ep1fix/C02_03.*'):   # 720p corrigido (o C02_03 de layers_r03 e o antigo, com a foto do nariz)
        ext = os.path.splitext(f)[1]; items.append((f.replace(os.sep, '/'), L + '/C02_03_EP1FIX_720p' + ext))
    E = DRV + '/02_PROJETOS/EP300_ABERTURA_R03_EDITAVEL'
    for f in walk(R + '/editable_r03'): items.append((f, E + '/' + os.path.relpath(f, R + '/editable_r03').replace(os.sep, '/')))
    items.append((R + '/V4_PRESENTABLE_REVIEW_03.mp4', DRV + '/03_EDITADOS/REFERENCIA_REVISAO/V4_PRESENTABLE_REVIEW_03.mp4'))
    I = E + '/_insumos'
    for n in ('base_audio_orig.wav', 'blooper.mov', 'gritem_4k.png', 'cold_full.wav', 'base_path.txt'): items.append((R + '/work/' + n, I + '/review_work/' + n))
    for n in ('words_tl.json', 'cues_final.json', 'cues_raw.json'): items.append((R + '/' + n, I + '/review_work/' + n))
    items.append((OP + '/work/v2/b0.mp4', I + '/work_v2/b0.mp4'))   # dialogo do blooper inicial (mix_audio/build_blooper)
    for f in glob.glob(OP + '/work/audio/ma/*.wav'): items.append((f.replace(os.sep, '/'), I + '/audio_ma/' + os.path.basename(f)))
    for n in ('caixa.ai', 'img_644.png'): items.append((OP + '/work/v1/pipoca/' + n, I + '/pipoca/' + n))
    for f in walk(OP + '/EP300_V4_MOTIONS/assets'): items.append((f, I + '/EP300_V4_MOTIONS_assets/' + os.path.relpath(f, OP + '/EP300_V4_MOTIONS/assets').replace(os.sep, '/')))
    for f in glob.glob(OP + '/review01/b3/assets/hist/*') + glob.glob(OP + '/review01/b3/assets/people/*'): items.append((f.replace(os.sep, '/'), I + '/b3_assets/' + os.path.relpath(f, OP + '/review01/b3/assets').replace(os.sep, '/')))
    return [(s, d) for s, d in items if os.path.isfile(s)]


def code_zip():
    out = OP + '/inventory/EP300_CODIGO_SNAPSHOT_2026-10-03.zip'
    skip = ('node_modules', '/.git', '__pycache__', '/work/inv', '_assembly_work', '/layers', '/editable', '/work/build', '/work/proxy', '/rem4k', '/work/r3', '/work/r03', '/work/seg', '/work/chunks')
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        n = 0
        for root in (OP, LP):
            for f in walk(root):
                fl = f.replace(os.sep, '/')
                if any(s in fl for s in skip) and not fl.endswith(('.py', '.md', '.tsx', '.ts', '.mjs')): continue
                if any(s in fl for s in ('_assembly_work', 'node_modules')): continue
                ext = os.path.splitext(f)[1].lower(); sz = os.path.getsize(f)
                code = ext in ('.py', '.md', '.json', '.txt', '.tsx', '.ts', '.mjs', '.js', '.css', '.html', '.xml', '.cmd', '.bat', '.yml', '.yaml', '.lock', '.svg')
                if not code or sz > 8 * 2 ** 20: continue
                if '/out/' in fl or '/layers' in fl or '/editable' in fl or '/work/r3/' in fl or '/work/r03/' in fl or '/work/chunks' in fl or '/work/seg' in fl: continue
                z.write(f, os.path.relpath(f, P).replace(os.sep, '/')); n += 1
    log('zip codigo', n, 'arquivos', os.path.getsize(out) // 1024, 'KB')
    return out


def copy_one(it):
    s, d = it; ss = os.path.getsize(s); xd = X(d)
    rec = dict(src=s, dst=d, size=ss, status='?', dst_len=len(d))
    try:
        if os.path.exists(xd):
            if os.path.getsize(xd) != ss: rec['status'] = 'DIVERGENCIA_DESTINO_EXISTE_TAMANHO_DIFERENTE'; return rec
            rec['pre_existing'] = True
        else:
            os.makedirs(os.path.dirname(xd), exist_ok=True)
            tmp = xd + '.partial'
            shutil.copyfile(s, tmp); os.replace(tmp, xd)
        ds = os.path.getsize(xd)
        hs, hd = md5(s), md5(d)
        rec.update(dst_size=ds, md5_src=hs, md5_dst=hd)
        rec['status'] = 'OK' if (ds == ss and hs == hd) else 'DIVERGENCIA_HASH'
    except Exception as e:
        rec['status'] = 'ERRO ' + repr(e)
    return rec


def phase_retry():
    done = json.load(open(MAN, encoding='utf-8'))
    todo = [(r['src'], r['dst']) for r in done if r['status'] != 'OK']
    log('RETRY:', len(todo), 'arquivos (caminho estendido)')
    new = {}
    with ThreadPoolExecutor(max_workers=3) as ex:
        for r in ex.map(copy_one, todo):
            new[r['src'] + '|' + r['dst']] = r
            if r['status'] != 'OK': log('RETRY problema', r['status'], r['dst'][-80:])
    done = [new.get(r['src'] + '|' + r['dst'], r) for r in done]
    json.dump(done, open(MAN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    bad = [r for r in done if r['status'] != 'OK']
    log('COPIA FIM (apos retry):', len(done) - len(bad), 'OK,', len(bad), 'problemas')


def phase_copy():
    items = plan()
    zp = code_zip(); items.append((zp.replace(os.sep, '/'), DRV + '/02_PROJETOS/EP300_ABERTURA_R03_EDITAVEL/_codigo/' + os.path.basename(zp)))
    tot = sum(os.path.getsize(s) for s, _ in items)
    log('COPIA: ', len(items), 'arquivos', tot // 2 ** 20, 'MB ->', DRV)
    done = []; t0 = time.time(); b = 0
    with ThreadPoolExecutor(max_workers=3) as ex:
        for r in ex.map(copy_one, items):
            done.append(r); b += r['size']
            if r['status'] != 'OK' or len(done) % 20 == 0: log(len(done), '/', len(items), r['status'], r['dst'][-70:], f'{b // 2**20}MB/{tot // 2**20}MB')
    json.dump(done, open(MAN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    bad = [r for r in done if r['status'] != 'OK']
    log('COPIA FIM:', len(done) - len(bad), 'OK,', len(bad), 'problemas,', round(time.time() - t0), 's')
    return done


def phase_dr():
    """hash dos duplicados: work/build{,_v1,_v2}/* <-> V{0,1,2}_GERADOS/*  e  loop/out <-> Drive (mesmo nome+tamanho)."""
    A = DRV + '/00_ASSETS E INSERTS'
    mp = {OP + '/work/build': A + '/V0_GERADOS', OP + '/work/build_v1': A + '/V1_GERADOS', OP + '/work/build_v2': A + '/V2_GERADOS'}
    drv_idx = {}
    for dp, dn, fn in os.walk(DRV):
        for f in fn: (lambda q: drv_idx.setdefault((f.lower(), os.path.getsize(X(q))), []).append(q))(os.path.join(dp, f).replace(os.sep, '/'))
    cand = []
    for loc, dr in mp.items():
        for f in walk(loc):
            rel = os.path.relpath(f, loc).replace(os.sep, '/')
            if rel.startswith('pieces/'): continue
            cand.append((f, dr + '/' + rel))
    for f in walk(LP + '/out'): cand.append((f, None))

    def chk(it):
        try: return chk0(it)
        except Exception as e: return dict(src=it[0], size=os.path.getsize(it[0]), dst=None, status='ERRO_LEITURA ' + repr(e)[:80])

    def chk0(it):
        s, d = it; ss = os.path.getsize(s)
        rec = dict(src=s, size=ss, dst=None, status='SEM_PAR_NO_DRIVE')
        paths = [d] if d and os.path.isfile(X(d)) and os.path.getsize(X(d)) == ss else drv_idx.get((os.path.basename(s).lower(), ss), [])
        if not paths: return rec
        hs = md5(s)
        for p in paths:
            if md5(p) == hs: rec.update(dst=p, md5=hs, status='HASH_IGUAL'); return rec
        rec.update(dst=paths[0], md5=hs, status='HASH_DIFERENTE'); return rec
    log('DR: hash de', len(cand), 'arquivos')
    out = []; t0 = time.time(); b = 0
    with ThreadPoolExecutor(max_workers=3) as ex:
        for r in ex.map(chk, cand):
            out.append(r); b += r['size']
            if r['status'] != 'HASH_IGUAL': log(r['status'], r['src'][-80:])
            elif len(out) % 40 == 0: log('DR', len(out), '/', len(cand), f'{b // 2**20}MB')
    json.dump(out, open(OP + '/inventory/dr_hash_manifest.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    from collections import Counter
    log('DR FIM', Counter(r['status'] for r in out), round(time.time() - t0), 's')


if __name__ == '__main__':
    for ph in sys.argv[1:] or ['copy', 'dr']:
        {'copy': phase_copy, 'dr': phase_dr, 'retry': phase_retry}[ph]()
