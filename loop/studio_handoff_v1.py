"""EP300 · Loop V1 — handoff no MB Studio (API local :4321). V1 entra como NOVA VERSÃO do output 'ep300-loop'
(deliverable LOOPING). V0 e a Abertura ficam intactas. Idempotente."""
import os, sys, json, urllib.request, shutil, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
STUDIO = os.path.join(HERE, '..', '..', 'studio')
API = 'http://127.0.0.1:4321'
OID, PID, PRODID = 'ep300-loop', 'ep300-video-looping', 'ep300-telao-looping'
TODAY = '2026-09-29'
NAME = 'EP300_LOOP_V1_PROXY.mp4'


def call(path, data=None, raw=None, ctype='application/json'):
    body = raw if raw is not None else (json.dumps(data).encode('utf-8') if data is not None else None)
    req = urllib.request.Request(API + path, data=body, method='POST' if body is not None else 'GET',
                                 headers={'Content-Type': ctype if body is not None else 'text/plain'})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read().decode('utf-8'))


def main():
    qa = json.load(open(os.path.join(HERE, 'out', 'qa_report.json'), encoding='utf-8'))
    items = call('/api/outputs')['items']
    o = next(x for x in items if x['id'] == OID)
    vfile = f'/outputs-media/{OID}/{NAME}'
    if not os.path.exists(os.path.join(STUDIO, 'data', 'outputs', OID, NAME)):
        up = call(f'/api/outputs/upload?id={OID}&name={NAME}', raw=open(os.path.join(HERE, 'out', NAME), 'rb').read(), ctype='application/octet-stream')
        vfile = up['url']; print('upload', up)
    for a in o.get('achados', []): a.setdefault('v', 'V0')
    for v in o['versoes']:
        if v['v'] == 'V0': v['status'] = 'revisado'; v['nota'] = v.get('nota', '').split(' · Revisada')[0] + ' · Revisada pelo Gabriel em 29/09 — direção aprovada, virou a V1.'
    if not any(v['v'] == 'V1' for v in o['versoes']):
        o['versoes'].append(dict(v='V1', file=vfile, status='pronto', created=TODAY,
            nota=('V1 — 120 s · 1920x1080 · sem áudio · CTA removido · mosaico de acervo (%d cartões, %d imagens do acervo, azul SP %.0f%%) com troca lenta em %d cartões · '
                  '4 microgags (espiada, pipoca, cursor, empurrão) · patrocinadores provisórios. Pergunta: o fundo comunica 300 episódios e o telão continua calmo?'
                  % (qa['mosaico_cartoes'], qa['mosaico_imagens_unicas'], qa['cenario_azul_share'] * 100, qa['cartoes_com_troca_lenta']))))
    o['status'] = 'pronto'; o['updated'] = TODAY
    o['aviso'] = 'PROXY 1920x1080 (CRF 20) aguardando conferência — não é o master de cinema. Patrocinadores PROVISÓRIOS. Entregável separado da Abertura.'
    o['explicacao'] = ('Loop de 120 s para o telão durante o podcast (sem áudio, sem CTA). "EPISÓDIO 300" + Analytics Talks sobre um mosaico de acervo '
                       '(thumbs oficiais EP260–289 + prints do estúdio principal + EP126 + poucos do estúdio azul), com troca lenta de cartões. '
                       '4 microgags espaçadas (Gustavo espia · Lucian + pipoca · cursor puxa o Lucian pela bochecha · Lucian empurra o Gustavo) e ~85 s de calma. '
                       'Editável: 02_PROJETOS/EP300_LOOP_V1 (scene.json + assets; trocar sticker/logo/thumb/patrocinador sem reconstruir).')
    A = [
        ('qa-loop-v1-1', 118, 'alta', 'Patrocinadores estão PROVISÓRIOS: Patrocínio Oficial = Purple Metrics ("Corpo/Purple Metrics" a confirmar) e Onfly (naming/logo podem mudar); Café Oficial = Coffee++; Realização = Métricas Boss (logo oficial do repo, sem rotação/deformação).',
         'Confirmar naming/logos finais; trocar em scene.json > sponsors.groups antes do master.'),
        ('qa-loop-v1-2', 5, 'media', 'Mosaico usa só acervo já conhecido (busca dirigida): thumbs oficiais EP260–289, prints do estúdio principal EP254–292, 2 quadros do EP126 (Rio) e 3 prints do estúdio azul (SP, %.0f%% da área). Não achei thumbs/prints dos episódios anteriores ao 251 (Rio antigo).' % (qa['cenario_azul_share'] * 100),
         'Se tiver thumbs de episódios antigos (1–250), copie para assets/mosaic e rode make_v1_scene.py para o fundo ficar mais "história".'),
        ('qa-loop-v1-3', 18, 'baixa', 'Microgags: espiada (Gustavo, ~17 s), pipoca (Lucian, ~46 s), cursor puxa a bochecha do Lucian e leva pra fora (~80 s), empurrão (Lucian empurra o Gustavo, ~104 s). Mais de 15 s de calma entre eles; tudo sem áudio.',
         'Achou muito/pouco? Ajuste presence/state em scene.json ou remova um gag.'),
        ('qa-loop-v1-4', 30, 'baixa', 'Troca lenta de fundo: 16 cartões dissolvem (10 s) para outra imagem e voltam — sem slideshow. Vale conferir se dá para perceber "essa imagem não estava aí".',
         'Ajustar alt_keys (velocidade/quantidade) se quiser mais ou menos.'),
        ('qa-loop-v1-5', 110, 'baixa', 'Stickers Gustavo/Lucian e pipoca seguem substituíveis (arquivo PNG separado da animação). Cursor é asset simples gerado (assets/fx/cursor.png). Não validado em projetor real.',
         'Trocar quando os novos stickers chegarem; testar no telão do Kinoplex antes do master.'),
    ]
    o['achados'] = [a for a in o.get('achados', []) if a.get('v') != 'V1'] + [
        dict(id=i, v='V1', origem='qa', ts=ts, severidade=sev, confianca='alta', problema=pb, correcao=cr) for i, ts, sev, pb, cr in A]
    call('/api/outputs', {'items': items}); print('outputs ok', [v['v'] for v in o['versoes']], len(o['achados']))

    pm = os.path.join(STUDIO, 'data', 'productions', PRODID + '.json')
    bk = os.path.join(STUDIO, 'data', 'backup', f'{PRODID}.pre-loop-v1-{datetime.datetime.now():%Y%m%d%H%M}.json')
    shutil.copy2(pm, bk)
    m = json.load(open(pm, encoding='utf-8'))
    for v in m.get('versions', []):
        if v.get('v') == 0: v['status'] = 'revisada'
    for d in m.get('dependencies', []):
        if d['id'] == 'revisao-loop-v0': d['status'] = 'resolvido'; d['note'] = 'Revisado pelo Gabriel em 29/09 (direção aprovada) — refinamento na V1.'
    if not any(v.get('v') == 1 for v in m['versions']):
        m['versions'].append(dict(v=1, label='Loop V1 — refinamento (mosaico de acervo, microgags, sem CTA)', status='aguardando_conferencia', outputId=OID,
                                  created=TODAY, file=vfile, nota='Proxy 1920x1080 · 120 s. Assistir em EP 300 → Looping do telão → ▶ Revisar (V0 no mesmo player).'))
    if not any(d['id'] == 'revisao-loop-v1' for d in m['dependencies']):
        m['dependencies'].append(dict(id='revisao-loop-v1', label='Revisão do Loop V1 pelo Gabriel (Studio) + confirmar patrocinadores', status='pendente',
            blocks=['master'], naoBlocks=['conceito', 'projeto', 'renders'],
            humanAction='Assistir o Loop V1 no Studio (EP 300 → Looping do telão → ▶ Revisar) e confirmar naming/logos finais dos patrocinadores (Purple Metrics/"Corpo", Onfly).',
            origem='Loop V1 entregue em 2026-09-29 (output ep300-loop, versão V1)'))
    for mat in m['materials']:
        if mat['id'] == 'projeto': mat['note'] = 'Drive: 01_VIDEO DE ABERTURA/02_PROJETOS/EP300_LOOP_V1 (scene.json + assets + build.py + qa.py; V0 em EP300_LOOP_V0). Troca de sticker/logo/thumb/patrocinador sem reconstruir.'
        if mat['id'] == 'renders': mat['note'] = 'EP300_LOOP_V0_PROXY.mp4 e EP300_LOOP_V1_PROXY.mp4 (1920x1080, 120 s) no Studio e em 03_EDITADOS.'
    m['storage'] = dict(m.get('storage') or {}, drivePathHint='01_VIDEO DE ABERTURA/02_PROJETOS/EP300_LOOP_V1 · 03_EDITADOS/EP300_LOOP_V1_PROXY.mp4')
    m['updatedAt'] = TODAY + 'T00:00:00.000Z'
    json.dump(m, open(pm, 'w', encoding='utf-8'), ensure_ascii=False, indent=2); print('production ok (backup', bk, ')')

    b = call('/api/board'); p = next(x for x in b['projects'] if x['id'] == PID)
    p['progress'] = max(p.get('progress', 0), 65)
    p['summary'] = ('Produção separada da Abertura — loop no telão durante a gravação do podcast. Loop V1 (proxy 1920x1080, 120 s, sem áudio, sem CTA) entregue para conferência: '
                    'mosaico de acervo com troca lenta, 4 microgags espaçadas; patrocinadores provisórios; editável por manifesto.')
    p['next'] = 'Assistir o Loop V1 no Studio: EP 300 → Looping do telão → ▶ Revisar (V0 no mesmo player) e confirmar naming/logos dos patrocinadores.'
    p['links'] = [l for l in p.get('links', []) if 'Loop V0' not in l.get('label', '')] + ([] if any('Loop V1' in l.get('label', '') for l in p.get('links', [])) else [{'label': '▶ Loop V1 (player)', 'url': '#/ep300'}])
    if not any('Loop V1' in (x.get('text', '') if isinstance(x, dict) else str(x)) for x in p['log']):
        p['log'].append({'date': TODAY, 'text': 'Loop V1 entregue para conferência (refinamento pós-revisão do V0: CTA removido, mosaico de acervo, microgags, patrocinadores provisórios). Master não gerado.'})
    p['updated'] = TODAY
    call('/api/board', b); print('board ok')


if __name__ == '__main__':
    main()
