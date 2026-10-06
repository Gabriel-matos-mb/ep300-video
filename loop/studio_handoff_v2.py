"""EP300 · Loop V2 — handoff no MB Studio (API local :4321). V2 = V1 sem o microgag do cursor (nenhuma linguagem de interface no telão) +
balde de pipoca corrigido no gag da pipoca; o fim da Abertura V2 termina nos quadros 118,5–120 s deste loop. V0/V1 ficam como histórico. Idempotente."""
import os, sys, json, urllib.request, shutil, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
STUDIO = os.path.join(HERE, '..', '..', 'studio')
API = 'http://127.0.0.1:4321'
OID, PID, PRODID = 'ep300-loop', 'ep300-video-looping', 'ep300-telao-looping'
TODAY = '2026-09-29'
NAME = 'EP300_LOOP_V2_PROXY.mp4'


def call(path, data=None, raw=None, ctype='application/json'):
    body = raw if raw is not None else (json.dumps(data).encode('utf-8') if data is not None else None)
    req = urllib.request.Request(API + path, data=body, method='POST' if body is not None else 'GET',
                                 headers={'Content-Type': ctype if body is not None else 'text/plain'})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read().decode('utf-8'))


def main():
    items = call('/api/outputs')['items']
    o = next(x for x in items if x['id'] == OID)
    vfile = f'/outputs-media/{OID}/{NAME}'
    dst = os.path.join(STUDIO, 'data', 'outputs', OID, NAME); src = os.path.join(HERE, 'out', NAME)
    if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(src):
        up = call(f'/api/outputs/upload?id={OID}&name={NAME}', raw=open(src, 'rb').read(), ctype='application/octet-stream')
        vfile = up['url']; print('upload', up)
    for a in o.get('achados', []): a.setdefault('v', 'V0')
    for v in o['versoes']:
        if v['v'] == 'V1': v['status'] = 'superada'
    if not any(v['v'] == 'V2' for v in o['versoes']):
        o['versoes'].append(dict(v='V2', file=vfile, status='pronto', created=TODAY,
            nota='V2 — 120 s · 1920x1080 · sem áudio · sem CTA/cursor · balde de pipoca corrigido · começa exatamente no quadro em que a Abertura V2 termina. '
                 'Pergunta: o telão continua calmo e o encaixe com a Abertura funciona?'))
    o['status'] = 'pronto'; o['updated'] = TODAY
    A = [('qa-loop-v2-1', 0, 'alta', 'Encaixe com a Abertura V2: os últimos 1,5 s da abertura são os quadros 118,5–120 s deste loop; ele começa no quadro 0 sem corte (mosaico, 300, logo e patrocinadores idênticos).',
          'Ver a passagem Abertura → Loop no Studio (o final da Abertura V2 é o mesmo universo).'),
         ('qa-loop-v2-2', 80, 'baixa', 'Microgag do cursor removido (nada com cara de interface no telão): nessa janela o Lucian só espia de lado e sai. Gag da pipoca agora usa o balde corrigido do Gabriel.',
          'Manter / trocar por outro microgag?'),
         ('qa-loop-v2-3', 118, 'alta', 'Patrocinadores continuam PROVISÓRIOS (Purple Metrics/Onfly a confirmar; Coffee++; Realização Métricas Boss).', 'Confirmar naming/logos finais antes do master.')]
    o['achados'] = [a for a in o.get('achados', []) if a.get('v') != 'V2'] + [
        dict(id=i, v='V2', origem='qa', ts=ts, severidade=sev, confianca='alta', problema=pb, correcao=cr) for i, ts, sev, pb, cr in A]
    o.pop('revisaoConcluida', None) if o.get('revisaoConcluida') else None
    call('/api/outputs', {'items': items}); print('outputs ok', [v['v'] for v in o['versoes']], len(o['achados']))

    pm = os.path.join(STUDIO, 'data', 'productions', PRODID + '.json')
    bk = os.path.join(STUDIO, 'data', 'backup', f'{PRODID}.pre-loop-v2-{datetime.datetime.now():%Y%m%d%H%M}.json')
    shutil.copy2(pm, bk)
    m = json.load(open(pm, encoding='utf-8'))
    for v in m.get('versions', []):
        if v.get('v') == 1: v['status'] = 'superada'
    if not any(v.get('v') == 2 for v in m['versions']):
        m['versions'].append(dict(v=2, label='Loop V2 — encaixe com a Abertura V2 (sem cursor)', status='aguardando_conferencia', outputId=OID,
                                  created=TODAY, file=vfile, nota='Proxy 1920x1080 · 120 s. Assistir em EP 300 → Looping do telão → ▶ Revisar.'))
    for d in m['dependencies']:
        if d['id'] == 'revisao-loop-v1': d['status'] = 'resolvido'; d['note'] = 'Superada pela V2 (29/09).'
    if not any(d['id'] == 'revisao-loop-v2' for d in m['dependencies']):
        m['dependencies'].append(dict(id='revisao-loop-v2', label='Revisão do Loop V2 pelo Gabriel (Studio) + confirmar patrocinadores', status='pendente',
            blocks=['master'], naoBlocks=['conceito', 'projeto', 'renders'],
            humanAction='Assistir o Loop V2 no Studio (EP 300 → Looping do telão → ▶ Revisar) e confirmar naming/logos finais dos patrocinadores.',
            origem='Loop V2 entregue em 2026-09-29 (output ep300-loop, versão V2)'))
    m['updatedAt'] = TODAY + 'T00:00:00.000Z'
    json.dump(m, open(pm, 'w', encoding='utf-8'), ensure_ascii=False, indent=2); print('production ok (backup', bk, ')')

    b = call('/api/board'); p = next(x for x in b['projects'] if x['id'] == PID)
    p['next'] = 'Assistir o Loop V2 no Studio: EP 300 → Looping do telão → ▶ Revisar (V0/V1 no mesmo player).'
    if not any('Loop V2' in (x.get('text', '') if isinstance(x, dict) else str(x)) for x in p['log']):
        p['log'].append({'date': TODAY, 'text': 'Loop V2 entregue (sem cursor; encaixe com o final da Abertura V2).'})
    p['updated'] = TODAY
    call('/api/board', b); print('board ok')


if __name__ == '__main__':
    main()
