"""EP300 · V0 — publica na estrutura OFICIAL do Drive (só cria/adiciona; nunca apaga nem sobrescreve brutos).

00_ASSETS E INSERTS/V0_GERADOS/{OVERLAYS,STILLS,AUDIO}   assets novos (necessários para reeditar)
02_PROJETOS/EP300_ABERTURA_V0/                           XML Premiere, manifesto, código-fonte, transcrição, edit plan
03_EDITADOS/EP300_ABERTURA_V0_PROXY.mp4                  preview
"""
import os, shutil, glob, hashlib, json, sys
import build

W = build.WORK; B = build.B
HERE = os.path.dirname(os.path.abspath(__file__))


def cp(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst) and os.path.getsize(dst) == os.path.getsize(src):
        return 'igual'
    shutil.copy2(src, dst); return 'copiado'


def main():
    log = []
    A = build.D_ASSETS; P = build.D_PROJ
    for f in sorted(glob.glob(os.path.join(B, 'OVERLAYS', '*'))):
        log.append((cp(f, os.path.join(A, 'OVERLAYS', os.path.basename(f))), 'OVERLAYS/' + os.path.basename(f)))
    for f in sorted(glob.glob(os.path.join(B, 'STILLS', '*.png'))):
        log.append((cp(f, os.path.join(A, 'STILLS', os.path.basename(f))), 'STILLS/' + os.path.basename(f)))
    for f in sorted(glob.glob(os.path.join(B, 'AUDIO', '*.wav'))):
        log.append((cp(f, os.path.join(A, 'AUDIO', os.path.basename(f))), 'AUDIO/' + os.path.basename(f)))
    log.append((cp(os.path.join(B, 'mix.wav'), os.path.join(A, 'AUDIO', 'REF_MIX_V0.wav')), 'AUDIO/REF_MIX_V0.wav'))
    used = {'MA_LEXMusic_GotTheSwag_Opener.wav', 'Trigubovich_A_Groove_Pool_loop_long.wav', 'MA_Puremusic_InTheSpotlight_12s.wav'}
    used |= {v[0] for v in build.SFX.values()}
    for f in sorted(used):
        log.append((cp(os.path.join(build.MA, f), os.path.join(A, 'AUDIO', f)), 'AUDIO/' + f))
    cp(os.path.join(build.MA, 'SOURCES.txt'), os.path.join(A, 'AUDIO', 'ORIGEM_MOTION_ARRAY.txt'))
    # projeto
    log.append((cp(os.path.join(B, 'EP300_ABERTURA_V0.xml'), os.path.join(P, 'EP300_ABERTURA_V0.xml')), 'EP300_ABERTURA_V0.xml'))
    log.append((cp(os.path.join(B, 'timeline_v0.json'), os.path.join(P, 'timeline_v0.json')), 'timeline_v0.json'))
    log.append((cp(os.path.join(HERE, 'README.md'), os.path.join(P, 'README_EDITAVEL.md')), 'README_EDITAVEL.md'))
    log.append((cp(os.path.join(HERE, '..', 'V0_EDIT_PLAN.md'), os.path.join(P, 'EDIT_PLAN_V0.md')), 'EDIT_PLAN_V0.md'))
    for f in glob.glob(os.path.join(HERE, '*.py')) + glob.glob(os.path.join(HERE, 'fonts', '*')) + [os.path.join(HERE, 'README.md')]:
        rel = os.path.relpath(f, HERE)
        log.append((cp(f, os.path.join(P, 'FONTE_CODIGO', rel)), 'FONTE_CODIGO/' + rel.replace('\\', '/')))
    for f in ['transcript_take_v3.json', 'transcript_take_v3.txt', 'transcript_take.json', 'transcript_geral.txt', 'transcript_geral.json',
              'qa/preview_transcript.txt', 'sync.py', 'transcribe.py', 'mouth.json']:
        src = os.path.join(W, f)
        if os.path.exists(src):
            log.append((cp(src, os.path.join(P, 'TRANSCRICAO', os.path.basename(f))), 'TRANSCRICAO/' + os.path.basename(f)))
    # preview
    log.append((cp(os.path.join(B, 'EP300_ABERTURA_V0_PROXY.mp4'), os.path.join(build.D_EDIT, 'EP300_ABERTURA_V0_PROXY.mp4')),
                '03_EDITADOS/EP300_ABERTURA_V0_PROXY.mp4'))
    n = sum(1 for s, _ in log if s == 'copiado')
    print(f'{len(log)} arquivos ({n} copiados agora)')
    json.dump(log, open(os.path.join(B, 'publish_log.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)


if __name__ == '__main__':
    main()
