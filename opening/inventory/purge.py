"""EP300 — EXCLUSAO AUTORIZADA (03/10/2026): T1 + T1B + T2 validado, EXATAMENTE conforme inventory/safe_to_delete.json. Nao amplia a lista.
Pre-condicao T2: o arquivo local deve (a) constar no migration_manifest com status OK, (b) ter tamanho e MD5 locais iguais ao md5_src do manifesto
(= identico ao que foi copiado), (c) ter o destino no Drive com o mesmo tamanho e md5_dst == md5_src. Senao: PULA e reporta.
Pre-condicao geral: arquivo existe com o tamanho do inventario e esta dentro de ep300-cinema-opening/ ou ep300-cinema-loop/ (nunca VERSAO FINAL/Manifesto).
Pre-condicao T1 'DUPLICADO_DO_DRIVE_HASH_IGUAL': dr_hash_manifest = HASH_IGUAL com o mesmo tamanho."""
import os, sys, json, shutil, hashlib, time

P = 'C:/Users/gabri/Code/audio-visual/projects'
INV = P + '/ep300-cinema-opening/inventory'
OK_ROOTS = (P + '/ep300-cinema-opening/', P + '/ep300-cinema-loop/')
BS = chr(92)


def X(p):
    q = p.replace('/', BS)
    return BS * 2 + '?' + BS + q if len(p) >= 240 and q[1:2] == ':' else p


def md5(p):
    h = hashlib.md5()
    with open(X(p), 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()


def main(dry=False):
    inv = json.load(open(INV + '/safe_to_delete.json', encoding='utf-8'))
    man = {r['src'].replace(os.sep, '/'): r for r in json.load(open(INV + '/migration_manifest.json', encoding='utf-8'))}
    dr = {r['src'].replace(os.sep, '/'): r for r in json.load(open(INV + '/dr_hash_manifest.json', encoding='utf-8'))}
    md5_copied = {r['md5_src'] for r in man.values() if r['status'] == 'OK'}
    log = dict(deleted=[], skipped=[], bytes_deleted=0, dirs_removed=[]); t0 = time.time()
    items = inv['items']
    for it in items:
        t, cat, p, s = it['tier'], it['cat'], it['path'].replace(os.sep, '/'), it['size']
        def skip(why): log['skipped'].append(dict(path=p, tier=t, cat=cat, why=why))
        if not p.startswith(OK_ROOTS) or 'VERS' in p.split('/')[-1].upper() and 'FINAL' in p.upper() or 'manifesto' in p.lower(): skip('fora do escopo/protegido'); continue
        if '/work/inv/' in p: skip('inventario/hashes preservados por ordem do Gabriel'); continue
        if p.endswith('/'):   # node_modules
            q = X(p.rstrip('/'))
            if os.path.basename(p.rstrip('/')) != 'node_modules' or not os.path.isdir(q): skip('node_modules ausente/inesperado'); continue
            if os.path.islink(q) or (os.stat(q, follow_symlinks=False).st_file_attributes & 0x400): skip('node_modules e JUNCTION para outro projeto (remotion-mb/node_modules): fora do escopo, nada a liberar neste projeto'); continue
            if not dry: shutil.rmtree(X(p.rstrip('/')), ignore_errors=False)
            log['deleted'].append(dict(path=p, tier=t, size=s)); log['bytes_deleted'] += s; continue
        if not os.path.isfile(X(p)): skip('JA_REMOVIDO na 1a passada (gate aplicado antes; processo caiu no node_modules antes de gravar o log)'); log['already'] = log.get('already', 0) + s; continue
        if os.path.getsize(X(p)) != s: skip('tamanho difere do inventario'); continue
        if t == 'T2':
            r = man.get(p)
            if not r or r['status'] != 'OK' or r['md5_src'] != r['md5_dst']: skip('T2 sem copia validada no manifesto'); continue
            d = r['dst']
            if not os.path.isfile(X(d)) or os.path.getsize(X(d)) != s: skip('T2 destino ausente/tamanho diferente no Drive'); continue
            if md5(p) != r['md5_src']: skip('T2 local mudou desde a copia (md5)'); continue
            if md5(d) != r['md5_src']: skip('T2 md5 do Drive difere agora'); continue
        elif cat.startswith('DUPLICADO_DO_DRIVE'):
            r = dr.get(p)
            if not r or r['status'] != 'HASH_IGUAL' or r['size'] != s: skip('DR sem HASH_IGUAL no manifesto'); continue
        elif cat in ('R02_DUP_R03',) and md5(p) not in md5_copied: skip('R02 dup sem equivalente copiado/validado no Drive'); continue
        if not dry: os.remove(X(p))
        log['deleted'].append(dict(path=p, tier=t, size=s)); log['bytes_deleted'] += s
    # diretorios que ficaram vazios (apenas dentro dos projetos EP300; sem tocar em nada com arquivo)
    if not dry:
        for root in OK_ROOTS:
            for dp, dn, fn in os.walk(root[:-1], topdown=False):
                dpn = dp.replace(os.sep, '/')
                if dpn + '/' == root or '/.git' in dpn or 'node_modules' in dpn: continue
                try:
                    if not os.listdir(X(dpn)): os.rmdir(X(dpn)); log['dirs_removed'].append(dpn)
                except OSError: pass
    from collections import Counter
    log['summary'] = dict(deleted=len(log['deleted']), skipped=len(log['skipped']), bytes=log['bytes_deleted'], by_tier=dict(Counter()), seconds=round(time.time() - t0))
    bt = {}
    for d in log['deleted']: bt[d['tier']] = bt.get(d['tier'], 0) + d['size']
    log['summary']['by_tier'] = bt
    json.dump(log, open(INV + ('/purge_dry.json' if dry else '/purge_log.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('DRY' if dry else 'EXECUTADO', log['summary'])
    for s in log['skipped'][:20]: print('PULADO', s['why'], s['path'][-90:])


if __name__ == '__main__':
    main(dry='--dry' in sys.argv)
