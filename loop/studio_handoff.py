"""EP300 · Loop V0 — handoff no MB Studio (API local :4321). Entregável SEPARADO da Abertura:
output 'ep300-loop' (projeto de board 'ep300-video-looping', produção 'ep300-telao-looping').
Não toca no output 'ep300-abertura'. Idempotente."""
import os, sys, json, urllib.request, shutil, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
STUDIO = os.path.join(HERE, '..', '..', 'studio')
API = 'http://127.0.0.1:4321'
OID, PID, PRODID = 'ep300-loop', 'ep300-video-looping', 'ep300-telao-looping'
TODAY = '2026-09-29'
NAME = 'EP300_LOOP_V0_PROXY.mp4'


def call(path, data=None, raw=None, ctype='application/json'):
    body = raw if raw is not None else (json.dumps(data).encode('utf-8') if data is not None else None)
    req = urllib.request.Request(API + path, data=body, method='POST' if body is not None else 'GET',
                                 headers={'Content-Type': ctype if body is not None else 'text/plain'})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read().decode('utf-8'))


def main():
    items = call('/api/outputs')['items']
    o = next((x for x in items if x['id'] == OID), None)
    vfile = f'/outputs-media/{OID}/{NAME}'
    if not os.path.exists(os.path.join(STUDIO, 'data', 'outputs', OID, NAME)):
        up = call(f'/api/outputs/upload?id={OID}&name={NAME}', raw=open(os.path.join(HERE, 'out', NAME), 'rb').read(), ctype='application/octet-stream')
        vfile = up['url']; print('upload', up)
    A = [
        ('qa-loop-1', 20, 'media', 'Gustavo e Lucian são os adesivos vivos do site (placeholders): cabeça inteira com contorno, mas você está produzindo versões melhores.',
         'Trocar os PNGs em assets/stickers/<gustavo|lucian>/ mantendo o nome — a animação não muda (testado).'),
        ('qa-loop-2', 55, 'baixa', 'Pipoca = STICKER PIPOCA.png (sua nova referência) só como microinteração: aparece, dá um pulinho, Lucian reage, some.',
         'Manter / mais discreta (props[0].size) / remover.'),
        ('qa-loop-3', 5, 'media', 'Layout estático aprovado não foi encontrado como arquivo — recriei a composição pelo brief com os assets do EP300. Patrocínio = Purple Metrics, Eletromidia, Onfly, Reportei, Sinatra; Café Oficial = Coffee++ (mapa do handoff /300).',
         'Conferir lista de patrocinadores e comparar com o layout aprovado; ajustar em scene.json.'),
        ('qa-loop-4', 100, 'baixa', '3 microinterações em 120 s (≈ 25 s de vida, ≈ 95 s de calma). Loop exato na fonte; no MP4 há um pulso de keyframe a cada 2 s (invisível a olho, igual em todos os limites de GOP).',
         'Achou muito? Dá pra afastar os eventos (presence em scene.json) ou dobrar a duração.'),
        ('qa-loop-5', 110, 'baixa', 'Não validado em projetor real: brilho/contraste de fundo escuro e safe area do Kinoplex.',
         'Testar num projetor/monitor grande antes do master.'),
    ]
    novo = dict(id=OID, projectId=PID, tipo='video', titulo='EP300 — Looping do Telão', status='pronto', escopo='completo',
                aviso='PROXY 1920x1080 (CRF 20) aguardando conferência — não é o master de cinema. Entregável separado da Abertura.',
                explicacao=('Loop de 120 s para o telão durante o podcast: colagem escura de episódios antigos com parallax lentíssimo, '
                            '"EPISÓDIO 300" em adesivo, logo Analytics Talks, "Toca pra ver o que rolou até aqui." e patrocinadores estáticos. '
                            '3 microinterações (Gustavo, Lucian + pipoca, dupla) e ~95 s de calma. Loop exato (frame 120 s = frame 0). '
                            'Editável: 02_PROJETOS/EP300_LOOP_V0 (scene.json + assets; trocar sticker/logo/thumb sem reconstruir a cena).'),
                versoes=[dict(v='V0', file=vfile, status='pronto', created=TODAY,
                              nota='V0 — 120 s · 1920x1080 30 fps · sem áudio · loop exato. Pergunta: isso distrairia alguém assistindo ao podcast?')],
                comentarios=[], created=TODAY, updated=TODAY)
    novo['achados'] = [dict(id=i, v='V0', origem='qa', ts=ts, severidade=sev, confianca='alta', problema=pb, correcao=cr) for i, ts, sev, pb, cr in A]
    if o is None: items.insert(0, novo); print('output criado')
    else: o.update({k: v for k, v in novo.items() if k not in ('comentarios',)}); print('output atualizado')
    call('/api/outputs', {'items': items})

    pm = os.path.join(STUDIO, 'data', 'productions', PRODID + '.json')
    bk = os.path.join(STUDIO, 'data', 'backup', f'{PRODID}.pre-loop-v0-{datetime.datetime.now():%Y%m%d%H%M}.json')
    os.makedirs(os.path.dirname(bk), exist_ok=True); shutil.copy2(pm, bk)
    m = json.load(open(pm, encoding='utf-8'))
    for mat in m['materials']:
        if mat['id'] == 'conceito':
            mat.update(status='existe', note='Conceito no README do projeto (projects/ep300-cinema-loop): estado-base calmo + 3 microinterações em 120 s.')
        if mat['id'] == 'projeto':
            mat.update(status='existe', note='Drive: 01_VIDEO DE ABERTURA/02_PROJETOS/EP300_LOOP_V0 (scene.json + assets + build.py + qa.py). Troca de sticker/logo/thumb sem reconstruir a cena.')
        if mat['id'] == 'renders':
            mat.update(status='existe', note='EP300_LOOP_V0_PROXY.mp4 (1920x1080, 120 s) no Studio e em 03_EDITADOS.')
    m['storage'] = dict(m.get('storage') or {}, drivePathHint='01_VIDEO DE ABERTURA/02_PROJETOS/EP300_LOOP_V0 · 03_EDITADOS/EP300_LOOP_V0_PROXY.mp4')
    if not any(v.get('v') == 0 for v in m.get('versions', [])):
        m['versions'].append(dict(v=0, label='Loop V0 — proxy', status='aguardando_conferencia', outputId=OID, created=TODAY, file=vfile,
                                  nota='Proxy 1920x1080 · 120 s. Assistir em EP 300 → Looping do telão → ▶ Revisar.'))
    if not any(d['id'] == 'revisao-loop-v0' for d in m.get('dependencies', [])):
        m.setdefault('dependencies', []).append(dict(id='revisao-loop-v0', label='Revisão do Loop V0 pelo Gabriel (Studio)', status='pendente',
            blocks=['master'], naoBlocks=['conceito', 'projeto', 'renders'],
            humanAction='Assistir o Loop V0 no Studio (EP 300 → Looping do telão → ▶ Revisar). Pergunta: isso distrairia alguém assistindo ao podcast?',
            origem='Loop V0 entregue em 2026-09-29 (output ep300-loop)'))
    m['updatedAt'] = TODAY + 'T00:00:00.000Z'
    json.dump(m, open(pm, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('production ok (backup', bk, ')')

    b = call('/api/board')
    p = next(x for x in b['projects'] if x['id'] == PID)
    p['status'] = 'andamento'; p['progress'] = max(p.get('progress', 0), 50)
    p['summary'] = ('Produção separada da Abertura — loop no telão durante a gravação do podcast. Loop V0 (proxy 1920x1080, 120 s, sem áudio) '
                    'entregue para conferência: estado-base calmo + 3 microinterações; editável por manifesto (troca de sticker/logo/thumb sem reconstruir).')
    p['next'] = 'Assistir o Loop V0 no Studio: EP 300 → Looping do telão → ▶ Revisar (ou Produções → este card → Revisão).'
    p['links'] = [l for l in p.get('links', []) if 'Loop' not in l.get('label', '')] + [
        {'label': '▶ Loop V0 (player)', 'url': '#/ep300'},
        {'label': 'Projeto (README, scene.json, QA)', 'path': 'C:\\Users\\gabri\\Code\\audio-visual\\projects\\ep300-cinema-loop\\README.md'}]
    p.setdefault('log', [])
    if not any('Loop V0' in (x.get('text', '') if isinstance(x, dict) else str(x)) for x in p['log']):
        p['log'].append({'date': TODAY, 'text': 'Loop V0 entregue para conferência (proxy 1920x1080, 120 s). Entregável separado da Abertura; master não gerado.'})
    p['updated'] = TODAY
    call('/api/board', b); print('board ok')


if __name__ == '__main__':
    main()
