"""Gera SAFE_TO_DELETE (NAO apaga nada). Le migration_manifest.json (copias validadas por MD5) e dr_hash_manifest.json (duplicados por MD5).
TIER 1 = aprovado no plano (DR hash igual + regeneraveis D + temporarios E + obsoletos F verificados + node_modules)
TIER 2 = copias locais de A/B/C ja VALIDADAS no Drive (Drive First; opcional, manter se for retrabalhar)
RETIDO = codigo/config/manifests e tudo que nao tem copia/regeneracao comprovada."""
import os, re, json, hashlib, collections

P = 'C:/Users/gabri/Code/audio-visual/projects'
INV = P + '/ep300-cinema-opening/inventory'
src = open(INV + '/classify.py', encoding='utf-8').read()
ns = {}
exec(src[src.index('rules=['):src.index('tot=collections')], {'re': re}, ns)
rules = ns['rules']
man = json.load(open(INV + '/migration_manifest.json', encoding='utf-8'))
copied = {r['src'] for r in man if r['status'] == 'OK'}
dr = {r['src'].replace(os.sep, '/'): r for r in json.load(open(INV + '/dr_hash_manifest.json', encoding='utf-8'))}
dridx = json.load(open(INV + '/drive_ep300_files.json'))
drive_names = {(os.path.basename(p).lower(), s) for s, p, m in dridx['files']}
CODE = ('.py', '.md', '.json', '.txt', '.tsx', '.ts', '.mjs', '.js', '.css', '.html', '.xml', '.cmd', '.bat', '.yml', '.yaml', '.lock', '.svg', '.webp', '.log')


def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()


# indice MD5 do que e da R03 (para provar que a R02 nao tem fonte unica)
r03_dirs = ['review01/layers_r03', 'review01/editable_r03', 'review01/layers_r03_ep1fix', 'review01/layers_r03_ep1fix_4k', 'review01/work/r3/rem4k']
r03_hash = {}; r03_names = set()
OP = P + '/ep300-cinema-opening'
for d in r03_dirs:
    for dp, dn, fn in os.walk(OP + '/' + d):
        for f in fn:
            p = os.path.join(dp, f); r03_hash[md5(p)] = p; r03_names.add(f)
r02_status = {}
for d in ('review01/layers', 'review01/editable'):
    for dp, dn, fn in os.walk(OP + '/' + d):
        for f in fn:
            p = os.path.join(dp, f).replace(os.sep, '/'); h = md5(p)
            r02_status[p] = 'DUP_R03' if h in r03_hash else ('SUBSTITUIDO_R03' if f in r03_names else 'R02_UNICO')

rows = []; nm_dirs = {}
for proj in ('ep300-cinema-opening', 'ep300-cinema-loop'):
    root = P + '/' + proj
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in ('.git', '__pycache__')]
        if os.path.basename(dp) == 'node_modules':
            tot = 0; n = 0
            for d2, _, f2 in os.walk(dp):
                for f in f2: tot += os.path.getsize(os.path.join(d2, f)); n += 1
            nm_dirs[dp.replace(os.sep, '/')] = (tot, n); dn[:] = []; continue
        for f in fn:
            p = os.path.join(dp, f).replace(os.sep, '/'); s = os.path.getsize(p); rel = os.path.relpath(p, root).replace(os.sep, '/')
            ext = os.path.splitext(f)[1].lower(); ondrive = (f.lower(), s) in drive_names
            if proj == 'ep300-cinema-loop':
                cl, why = ('DR', 'finais do Loop') if rel.startswith('out') and ondrive else ('B', 'Loop codigo/assets')
            else:
                for rx, cl, why in rules:
                    if re.search(rx, rel): break
            tier, cat = 'RETIDO', 'codigo/config/manifest ou sem copia comprovada'
            if p in copied:
                tier, cat = 'T2', 'COPIADO_VALIDADO_NO_DRIVE (' + why + ')'
            elif cl == 'DR':
                r = dr.get(p)
                if r and r['status'] == 'HASH_IGUAL': tier, cat = 'T1', 'DUPLICADO_DO_DRIVE_HASH_IGUAL'
                else: tier, cat = 'RETIDO', 'DR_SEM_HASH_IGUAL (' + (r['status'] if r else 'nao verificado') + ')'
            elif cl == 'D':
                if s < 3 * 2 ** 20 and ext in CODE: tier, cat = 'RETIDO', 'config pequena'
                else: tier, cat = 'T1', 'REGENERAVEL (' + why + ')'
            elif cl == 'E':
                if s < 1 * 2 ** 20 and ext in CODE and 'work/inv' not in rel: tier, cat = 'RETIDO', 'config pequena'
                else: tier, cat = 'T1', 'TEMPORARIO (' + why + ')'
            elif cl == 'F':
                if rel.startswith('review01/layers/') or rel.startswith('review01/editable/'):
                    st = r02_status.get(p, '?')
                    if st == 'R02_UNICO' and ext == '.wav': tier, cat = 'T1B', 'R02_SAIDA_AUDIO (stems do mix R02; nao usados pela R03)'; rows.append((tier, cat, p, s)); continue
                    if ext in ('.xml',) or f == 'timing_map.json': tier, cat = 'RETIDO', 'manifest R02 (pequeno)'
                    elif st in ('DUP_R03', 'SUBSTITUIDO_R03'): tier, cat = 'T1', 'R02_' + st
                    else: tier, cat = 'RETIDO', 'R02_UNICO (revisar)'
                elif 'V4_PRESENTABLE_REVIEW_0' in rel: tier, cat = 'T1', 'REVIEW_ANTERIOR (R01/R02 mp4)'
                elif '_assembly_work' in rel: tier, cat = 'T1', 'V4_REJEITADA (_assembly_work)'
                elif 'layers_r03_ep1fix/' in rel: tier, cat = 'T1', '720p do C02_03 (copiado como C02_03_EP1FIX_720p)' if p in copied else 'T1'
            elif cl == 'B' and re.match(r'review01/work/(mix\.wav|stem_)', rel): tier, cat = 'T1B', 'R02_SAIDA_AUDIO (mix/stems R02 em review01/work)'
            elif cl == 'B' and rel.startswith('work/') and ext in ('.wav', '.mp4', '.npy', '.mov'):
                tier, cat = 'T1', 'DERIVADO_V0-V3_REGENERAVEL'
            rows.append((tier, cat, p, s))
for d, (s, n) in nm_dirs.items(): rows.append(('T1', 'node_modules (reinstalar via package.json/lock)', d + '/', s))

agg = collections.defaultdict(lambda: [0, 0])
for t, c, p, s in rows: agg[(t, c)][0] += s; agg[(t, c)][1] += 1
tot = sum(s for *_, s in rows)
t1 = sum(s for t, *_, s in rows if t == 'T1'); t2 = sum(s for t, *_, s in rows if t == 'T2'); t1b = sum(s for t, *_, s in rows if t == 'T1B'); ret = sum(s for t, *_, s in rows if t == 'RETIDO')
nm_files = sum(n for s, n in nm_dirs.values())
print(f'TOTAL local (Opening+Loop): {tot} bytes = {tot / 2**30:.2f} GiB ({tot / 1e9:.2f} GB)')
for (t, c), (s, n) in sorted(agg.items(), key=lambda x: (x[0][0], -x[1][0])):
    print(f'{t:7s} {s / 2**20:9.0f} MiB {n:6d}f  {c}')
print(f'TIER1 (aprovado): {t1} bytes = {t1 / 2**30:.2f} GiB')
print(f'TIER1B (saidas de audio R02, recomendado): {t1b} bytes = {t1b / 2**30:.2f} GiB | workspace apos T1+T1B: {(tot - t1 - t1b) / 2**30:.2f} GiB | apos T1+T1B+T2: {(tot - t1 - t1b - t2) / 2**30:.2f} GiB')
print(f'TIER2 (copiado+validado, opcional): {t2} bytes = {t2 / 2**30:.2f} GiB')
print(f'RETIDO: {ret} bytes = {ret / 2**30:.2f} GiB  | workspace apos T1: {(tot - t1) / 2**30:.2f} GiB | apos T1+T2: {(tot - t1 - t2) / 2**30:.2f} GiB')
json.dump(dict(total=tot, tier1=t1, tier1b=t1b, tier2=t2, retido=ret, summary={f'{t}|{c}': v for (t, c), v in agg.items()},
               r02_unico=[p for p, st in r02_status.items() if st == 'R02_UNICO'],
               items=[dict(tier=t, cat=c, path=p, size=s) for t, c, p, s in rows if t in ('T1', 'T1B', 'T2')]), open(INV + '/safe_to_delete.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('R02_UNICO:', [p for p, st in r02_status.items() if st == 'R02_UNICO'][:10])
