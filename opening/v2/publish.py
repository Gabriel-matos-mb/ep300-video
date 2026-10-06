"""EP300 · V2 — publica na estrutura OFICIAL do Drive. Só CRIA/ADICIONA em pastas da V2; nunca apaga nem sobrescreve V0, V1, brutos
ou o projeto do Gabriel. Também verifica (MD5) que o projeto do Gabriel não mudou desde o backup imutável.

00_ASSETS E INSERTS/V2_GERADOS/{OVERLAYS,STILLS,AUDIO,ASSETS_V2,PIPOCA,PRINTS,EP126,LUTS,BASTIDORES}
02_PROJETOS/EP300_ABERTURA_V2/   XML Premiere (V2 + SYNC corrigido), manifesto, código-fonte, sync, edit plan, QA
03_EDITADOS/EP300_ABERTURA_V2_PROXY.mp4
"""
import os, shutil, glob, json, hashlib
import build

W = build.WORK; B = build.B
HERE = os.path.dirname(os.path.abspath(__file__))
V1W = os.path.join(W, 'v1'); V2W = os.path.join(W, 'v2')


def _lp(p):   # caminho longo (>260) no Windows
    p = os.path.abspath(p).replace('/', os.sep)
    pre = os.sep * 2 + '?' + os.sep
    return p if p.startswith(pre) else pre + p


def cp(src, dst):
    src = _lp(src)
    assert '_V0' not in dst and '_V1' not in dst.replace('V1W', ''), dst      # nunca escrever em arquivos/pastas de V0/V1
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if (os.path.exists(dst) and os.path.getsize(dst) == os.path.getsize(src)
            and int(os.path.getmtime(dst)) >= int(os.path.getmtime(src))):
        return 'igual'
    shutil.copy2(src, dst); return 'copiado'


def tree(src_dir, dst_dir, pats=('*',), log=None, tag=''):
    for pat in pats:
        for f in sorted(glob.glob(os.path.join(src_dir, '**', pat), recursive=True)):
            if os.path.isdir(f): continue
            rel = os.path.relpath(f, src_dir)
            log.append((cp(f, os.path.join(dst_dir, rel)), tag + rel.replace('\\', '/')))


def md5(p):
    h = hashlib.md5()
    with open(_lp(p), 'rb') as f:
        for ch in iter(lambda: f.read(1 << 20), b''): h.update(ch)
    return h.hexdigest()


def verify_backup():
    """o projeto do Gabriel em 02_PROJETOS (prproj/xml/prin) deve ser idêntico ao backup imutável."""
    proj = os.path.join(build.EP, '02_PROJETOS'); bk = os.path.join(proj, 'BACKUP_INTERVENCAO_GABRIEL_V0_2026-09-29')
    lines = []; ok = True
    for f in sorted(os.listdir(bk)):
        a = os.path.join(bk, f); b = os.path.join(proj, f)
        if os.path.isdir(a) or not os.path.exists(b): continue
        same = md5(a) == md5(b); ok &= same
        lines.append(f'{"IGUAL   " if same else "DIFERENTE"} {f}')
    return ok, lines


def main():
    log = []
    A = build.D_ASSETS; P = build.D_PROJ
    for sub in ('OVERLAYS', 'STILLS', 'LUTS'):
        if os.path.isdir(os.path.join(B, sub)):
            tree(os.path.join(B, sub), os.path.join(A, sub), ('*.mov', '*.png', '*.cube', '*.json', '*.txt'), log=log, tag=sub + '/')
    tree(os.path.join(B, 'AUDIO'), os.path.join(A, 'AUDIO'), ('*.wav',), log=log, tag='AUDIO/')
    log.append((cp(os.path.join(B, 'mix.wav'), os.path.join(A, 'AUDIO', 'REF_MIX_V2.wav')), 'AUDIO/REF_MIX_V2.wav'))
    used = set(build.MUSIC.values()) | {v[0] for v in build.SFX.values()}
    for f in sorted(used):
        log.append((cp(os.path.join(build.MA, f), os.path.join(A, 'AUDIO', f)), 'AUDIO/' + f))
    cp(os.path.join(build.MA, 'SOURCES.txt'), os.path.join(A, 'AUDIO', 'ORIGEM_MOTION_ARRAY.txt'))
    for k, (src, *_r) in build.MEDIA.items():
        log.append((cp(src, build.MEDIA_XML[k]), f'BASTIDORES/{k}.mp4'))
    # assets da V2 (stickers normalizados, logos, frames históricos, gags originais, balde, viatura) — com proveniência
    tree(os.path.join(V2W, 'assets'), os.path.join(A, 'ASSETS_V2'), ('*.png', '*.json'), log=log, tag='ASSETS_V2/')
    tree(os.path.join(V2W, 'logos'), os.path.join(A, 'ASSETS_V2', 'LOGOS_FONTE_SVG'), ('*.svg',), log=log, tag='LOGOS_SVG/')
    # herdados da V1 que a V2 ainda usa (selo/prints/EP126) — copiados para V2_GERADOS
    tree(os.path.join(V1W, 'pipoca'), os.path.join(A, 'PIPOCA'), ('selo_*.png', 'PROVENANCE.json'), log=log, tag='PIPOCA/')
    tree(os.path.join(V1W, 'prints'), os.path.join(A, 'PRINTS'), ('EP*.png', 'PROVENANCE.json'), log=log, tag='PRINTS/')
    tree(os.path.join(V1W, 'ep126'), os.path.join(A, 'EP126'), ('f_*.png', 'PROVENANCE.json'), log=log, tag='EP126/')
    # projeto
    log.append((cp(os.path.join(B, f'{build.NAME}.xml'), os.path.join(P, f'{build.NAME}.xml')), f'{build.NAME}.xml'))
    log.append((cp(os.path.join(B, 'timeline_v2.json'), os.path.join(P, 'timeline_v2.json')), 'timeline_v2.json'))
    for f, dst in (('README.md', 'README_EDITAVEL_V2.md'), (os.path.join('..', 'V2_EDIT_PLAN.md'), 'EDIT_PLAN_V2.md')):
        src = os.path.join(HERE, f)
        if os.path.exists(src): log.append((cp(src, os.path.join(P, dst)), dst))
    for f in glob.glob(os.path.join(HERE, '*.py')) + glob.glob(os.path.join(HERE, '*.json')) + glob.glob(os.path.join(HERE, 'fonts', '*')) + [os.path.join(HERE, 'README.md')]:
        if os.path.basename(f).startswith('_'): continue
        rel = os.path.relpath(f, HERE)
        log.append((cp(f, os.path.join(P, 'FONTE_CODIGO', rel)), 'FONTE_CODIGO/' + rel.replace('\\', '/')))
    for f, dstn in (('sync_report.json', 'sync_report.json'), ('sync_run2.log', 'sync_video_x_video_V2.log')):
        src = os.path.join(V2W, f)
        if os.path.exists(src): log.append((cp(src, os.path.join(P, 'SYNC_E_FEEDBACK', dstn)), 'SYNC_E_FEEDBACK/' + dstn))
    for f in ['human/feedback_markers.json', 'transcript_geral_times.txt']:
        src = os.path.join(V1W, f)
        if os.path.exists(src): log.append((cp(src, os.path.join(P, 'SYNC_E_FEEDBACK', os.path.basename(f))), 'SYNC_E_FEEDBACK/' + os.path.basename(f)))
    for f in glob.glob(os.path.join(V2W, 'qa', '*.jpg')) + glob.glob(os.path.join(V2W, 'qa', '*.json')):
        log.append((cp(f, os.path.join(P, 'QA', os.path.basename(f))), 'QA/' + os.path.basename(f)))
    log.append((cp(os.path.join(B, f'{build.NAME}_PROXY.mp4'), os.path.join(build.D_EDIT, f'{build.NAME}_PROXY.mp4')),
                f'03_EDITADOS/{build.NAME}_PROXY.mp4'))
    ok, lines = verify_backup()
    txt = ('Verificação (MD5) do projeto do Gabriel em 02_PROJETOS × BACKUP_INTERVENCAO_GABRIEL_V0_2026-09-29 — feita na execução da V2.\n'
           + ('RESULTADO: nenhum arquivo do Gabriel mudou desde o backup.\n' if ok else 'ATENÇÃO: há diferenças — o backup NÃO foi tocado.\n') + '\n'.join(lines) + '\n')
    os.makedirs(P, exist_ok=True)
    open(os.path.join(P, 'BACKUP_VERIFICACAO_V2.txt'), 'w', encoding='utf-8').write(txt)
    print(txt)
    n = sum(1 for s, _ in log if s == 'copiado')
    print(f'{len(log)} arquivos ({n} copiados agora)')
    json.dump(log, open(os.path.join(B, 'publish_log.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)


if __name__ == '__main__':
    main()
