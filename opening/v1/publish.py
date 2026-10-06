"""EP300 · V1 — publica na estrutura OFICIAL do Drive. Só CRIA/ADICIONA em pastas da V1; nunca apaga nem
sobrescreve V0, brutos ou o projeto do Gabriel.

00_ASSETS E INSERTS/V1_GERADOS/{OVERLAYS,STILLS,AUDIO,STICKERS,PIPOCA,PRINTS,EP126,LUTS}
02_PROJETOS/EP300_ABERTURA_V1/   XML Premiere (V1 + SYNC corrigido), manifesto, código-fonte, sync, feedback, edit plan
03_EDITADOS/EP300_ABERTURA_V1_PROXY.mp4
"""
import os, shutil, glob, json, hashlib
import build

W = build.WORK; B = build.B
HERE = os.path.dirname(os.path.abspath(__file__))
V1W = os.path.join(W, 'v1')


def _lp(p):   # caminho longo (>260) no Windows
    p = os.path.abspath(p).replace('/', os.sep)
    pre = os.sep * 2 + '?' + os.sep
    return p if p.startswith(pre) else pre + p


def cp(src, dst):
    src = _lp(src)
    assert 'V0' not in os.path.basename(dst) or 'V1' in dst, dst   # nunca escrever arquivo de V0
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if (os.path.exists(dst) and os.path.getsize(dst) == os.path.getsize(src)
            and int(os.path.getmtime(dst)) >= int(os.path.getmtime(src))):   # tamanho igual não basta (edição de mesmo tamanho)
        return 'igual'
    shutil.copy2(src, dst); return 'copiado'


def tree(src_dir, dst_dir, pats=('*',), log=None, tag=''):
    for pat in pats:
        for f in sorted(glob.glob(os.path.join(src_dir, '**', pat), recursive=True)):
            if os.path.isdir(f): continue
            rel = os.path.relpath(f, src_dir)
            log.append((cp(f, os.path.join(dst_dir, rel)), tag + rel.replace('\\', '/')))


def main():
    log = []
    A = build.D_ASSETS; P = build.D_PROJ
    for sub in ('OVERLAYS', 'STILLS', 'LUTS'):
        tree(os.path.join(B, sub), os.path.join(A, sub), log=log, tag=sub + '/')
    tree(os.path.join(B, 'AUDIO'), os.path.join(A, 'AUDIO'), ('*.wav',), log=log, tag='AUDIO/')
    log.append((cp(os.path.join(B, 'mix.wav'), os.path.join(A, 'AUDIO', 'REF_MIX_V1.wav')), 'AUDIO/REF_MIX_V1.wav'))
    used = set(build.MUSIC.values()) | {v[0] for v in build.SFX.values()}
    for f in sorted(used):
        log.append((cp(os.path.join(build.MA, f), os.path.join(A, 'AUDIO', f)), 'AUDIO/' + f))
    cp(os.path.join(build.MA, 'SOURCES.txt'), os.path.join(A, 'AUDIO', 'ORIGEM_MOTION_ARRAY.txt'))
    # bastidores usados no cold open: cópia com nome curto (limite de 260 caracteres do Windows/Premiere)
    for k, (src, *_r) in build.MEDIA.items():
        log.append((cp(src, build.MEDIA_XML[k]), f'BASTIDORES/{k}.mp4'))
    # assets gerados nesta rodada (com proveniência)
    tree(os.path.join(V1W, 'stickers'), os.path.join(A, 'STICKERS'), ('*.png', '*.jpg', '*.json'), log=log, tag='STICKERS/')
    tree(os.path.join(V1W, 'pipoca'), os.path.join(A, 'PIPOCA'), ('caixa_pipoca_*.png', 'selo_*.png', 'PROVENANCE.json'), log=log, tag='PIPOCA/')
    tree(os.path.join(V1W, 'prints'), os.path.join(A, 'PRINTS'), ('EP*.png', 'PROVENANCE.json'), log=log, tag='PRINTS/')
    tree(os.path.join(V1W, 'ep126'), os.path.join(A, 'EP126'), ('f_*.png', 'PROVENANCE.json'), log=log, tag='EP126/')
    # projeto
    log.append((cp(os.path.join(B, f'{build.NAME}.xml'), os.path.join(P, f'{build.NAME}.xml')), f'{build.NAME}.xml'))
    log.append((cp(os.path.join(B, 'timeline_v1.json'), os.path.join(P, 'timeline_v1.json')), 'timeline_v1.json'))
    for f, dst in (('README.md', 'README_EDITAVEL_V1.md'), (os.path.join('..', 'V1_EDIT_PLAN.md'), 'EDIT_PLAN_V1.md')):
        src = os.path.join(HERE, f)
        if os.path.exists(src): log.append((cp(src, os.path.join(P, dst)), dst))
    for f in glob.glob(os.path.join(HERE, '*.py')) + glob.glob(os.path.join(HERE, '*.json')) + glob.glob(os.path.join(HERE, 'fonts', '*')) + [os.path.join(HERE, 'README.md')]:
        if os.path.basename(f).startswith('_'): continue
        rel = os.path.relpath(f, HERE)
        log.append((cp(f, os.path.join(P, 'FONTE_CODIGO', rel)), 'FONTE_CODIGO/' + rel.replace('\\', '/')))
    for f in ['sync_report.json', 'human/feedback_markers.json', 'transcript_geral_times.txt']:
        src = os.path.join(V1W, f)
        if os.path.exists(src): log.append((cp(src, os.path.join(P, 'SYNC_E_FEEDBACK', os.path.basename(f))), 'SYNC_E_FEEDBACK/' + os.path.basename(f)))
    for f in glob.glob(os.path.join(V1W, 'qa', 'final_*.jpg')):
        log.append((cp(f, os.path.join(P, 'QA', os.path.basename(f))), 'QA/' + os.path.basename(f)))
    log.append((cp(os.path.join(B, f'{build.NAME}_PROXY.mp4'), os.path.join(build.D_EDIT, f'{build.NAME}_PROXY.mp4')),
                f'03_EDITADOS/{build.NAME}_PROXY.mp4'))
    n = sum(1 for s, _ in log if s == 'copiado')
    print(f'{len(log)} arquivos ({n} copiados agora)')
    json.dump(log, open(os.path.join(B, 'publish_log.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)


if __name__ == '__main__':
    main()
