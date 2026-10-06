"""EP300 · V1 — handoff no MB Studio (API local :4321). Nada da V0 é removido: a V1 entra como nova versão do
mesmo output; achados da V0 ficam marcados v='V0' (histórico) e os da V1 v='V1'. Idempotente."""
import os, sys, json, urllib.request, shutil, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build

API = 'http://127.0.0.1:4321'
OID = 'ep300-abertura'; PID = 'ep300-video-abertura'
STUDIO = os.path.join(HERE, '..', '..', '..', 'studio')
TODAY = '2026-09-29'


def call(path, data=None, raw=None, ctype='application/json'):
    body = raw if raw is not None else (json.dumps(data).encode('utf-8') if data is not None else None)
    req = urllib.request.Request(API + path, data=body, method='POST' if body is not None else 'GET',
                                 headers={'Content-Type': ctype if body is not None else 'text/plain'})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read().decode('utf-8'))


def ts_of(T, cue_id=None, src=None, off=0.0):
    if cue_id: return round(next(c for c in T['cues'] if c['id'] == cue_id)['tl_in'] / 30 + off, 1)
    return round(T['src2tl'](src) / 30 + off, 1)


def main():
    T = build.timeline()
    dur = T['total'] / 30
    items = call('/api/outputs')['items']
    o = next(x for x in items if x['id'] == OID)
    vfile = f'/outputs-media/{OID}/{build.NAME}_PROXY.mp4'
    already = os.path.exists(os.path.join(STUDIO, 'data', 'outputs', OID, f'{build.NAME}_PROXY.mp4'))
    if not any(v['v'] == 'V1' for v in o['versoes']) and not already:
        up = call(f'/api/outputs/upload?id={OID}&name={build.NAME}_PROXY.mp4',
                  raw=open(os.path.join(build.B, f'{build.NAME}_PROXY.mp4'), 'rb').read(), ctype='application/octet-stream')
        vfile = up['url']
        print('upload', up)
    for a in o.get('achados', []):
        a.setdefault('v', 'V0')
    for v in o['versoes']:
        if v['v'] == 'V0':
            v['status'] = 'revisado'
            v['nota'] = (v.get('nota', '').split(' · Revisada')[0] +
                         ' · Revisada pelo Gabriel no Premiere (48 marcadores + Lumetri) em 29/09 — virou a V1.')
    if not any(v['v'] == 'V1' for v in o['versoes']):
        o['versoes'].append(dict(v='V1', file=vfile, status='pronto', created=TODAY,
            nota=f'V1 — direção do Gabriel aplicada · {int(dur // 60)}:{int(dur % 60):02d} · sync corrigido (geral +5 quadros) · '
                 'cor aproximada do seu Lumetri · 43 motions (26 cenas em tela cheia) · pré-sessão nova · adesivos reais de convidados. '
                 'Pergunta da revisão: a V1 ficou mais viva e sem cara de teleprompter?'))
    o['status'] = 'pronto'; o['updated'] = TODAY
    o['aviso'] = 'PROXY 1280x720 para revisão — não é o master de cinema (1920x1080). Cor = aproximação do Lumetri do Gabriel.'
    o['explicacao'] = ('V1 derivada da V0 com os 48 marcadores do Gabriel no Premiere: câmera geral como base (fechadas só em reação), '
                       '18 cenas em tela cheia com a fala como VO, pré-sessão nova (bastidor PB + aviso "antes da sessão" + selo EP 300), '
                       'adesivos reais (Phill, Mafê, Bonel, Layla, Vitória), prints de episódios e do EP 126, sync corrigido. '
                       'Editável: 02_PROJETOS/EP300_ABERTURA_V1 (XML com os seus marcadores + o que foi feito em cada um).')
    A = [
        ('qa-v1-1', ts_of(T, 'C00_00', off=.5), 'media', 'Cold open de bastidor real (2023: "Começou mesmo?" → "Tá no ar, tá valendo."), PB/REC. É teste — removível.',
         'Manter / remover (plan.py PRESHOTS; a abertura encurta 7,4 s).'),
        ('qa-v1-2', ts_of(T, 'C00_03', off=.5), 'media', 'Aviso "antes da sessão" sem narração: texto + trilha Beat The Odds (Motion Array). Não usei voz por IA (custo zero; voz local soaria robótica no telão).',
         'Aprovar as 3 regras (saídas p/ quem disser "eu acho" · celular só se marcar a gente · pipoca) / pedir 15 s de voz real do Gustavo ou Lucian se quiser narrado.'),
        ('qa-v1-3', ts_of(T, src=514.9), 'alta', 'SYNC: a imagem da CAM_GERAL chegava ~5 quadros atrasada em relação ao áudio (captura). Corrigido na V1 (proxy e XML). Você não tinha mexido na sequência.',
         'Conferir lábios nos planos abertos (base de quase todo o vídeo).'),
        ('qa-v1-4', ts_of(T, src=515.5), 'media', 'Cor no proxy = aproximação numérica do seu Lumetri (por câmera). No Premiere, o seu Lumetri original é que vale.',
         'Seguir README_EDITAVEL_V1: importar o XML no seu projeto e colar atributos (3 colagens).'),
        ('qa-v1-5', ts_of(T, src=641.80, off=-1.5), 'media', 'Corte do "Nesse ano de 2025" (o certo é 2026; a tela diz HOJE). Retranscrição confirma: "…você acredita? Que isso. Está em um a cada quatro…". A reação do Gustavo continua por baixo.',
         'Ouvir a emenda; se incomodar, manter o áudio e só trocar o número na tela.'),
        ('qa-v1-6', ts_of(T, 'C04_05'), 'baixa', 'Respiro "Gritem se concordam" agora com 3 s (era 1,6) sobre o Gustavo apontando pra câmera principal.',
         'Manter / ajustar HOLD_GRITEM.'),
        ('qa-v1-7', ts_of(T, 'C03_01', off=2), 'media', 'Placeholders: logos oficiais (GA4, GTM, Looker, BigQuery, Amplitude, empresas, Google), logo MB Prime e fotos de Guta Tomalsquin e Lucas Yokota ("foto pendente").',
         'Enviar os assets (lista no relatório) ou aprovar os placeholders tipográficos.'),
        ('qa-v1-8', ts_of(T, 'C05_01', off=1), 'media', 'Números falados ≠ site: 191/140+ (site 196/146), 106 mil h (site 107K), 16 apelidos (site 40+). A V1 mostra o que foi falado.',
         'Confirmar com o Lucian antes do master.'),
        ('qa-v1-9', ts_of(T, 'C07_03', off=3.5), 'baixa', '"De volta para o futuro": homenagem tipográfica + sofá + ano correndo. Fotos do Marty/Doc/DeLorean não usadas (direitos de terceiros).',
         'Manter homenagem / decidir se vale licenciar imagem.'),
        ('qa-v1-10', round(dur - 3, 1), 'media', f'Duração {int(dur // 60)}:{int(dur % 60):02d} (V0 5:32): a pré-sessão pedida soma ~25 s; o corpo ficou ~9 s menor.',
         'Confirmar se cabe na grade do cinema ou cortar cold open/aviso.'),
    ]
    old = [a for a in o.get('achados', []) if a.get('v') != 'V1']
    o['achados'] = old + [dict(id=i, v='V1', origem='qa', ts=ts, severidade=sev, confianca='alta', problema=pb, correcao=cr)
                          for i, ts, sev, pb, cr in A]
    call('/api/outputs', {'items': items})
    print('outputs ok', [v['v'] for v in o['versoes']], len(o['achados']))
    # --------- produção (manifesto) — backup antes
    pm = os.path.join(STUDIO, 'data', 'productions', 'ep300-cinema-opening.json')
    bk = os.path.join(STUDIO, 'data', 'backup', f'ep300-cinema-opening.pre-v1-{datetime.datetime.now():%Y%m%d%H%M}.json')
    os.makedirs(os.path.dirname(bk), exist_ok=True); shutil.copy2(pm, bk)
    m = json.load(open(pm, encoding='utf-8'))
    for d in m.get('dependencies', []):
        if d['id'] == 'revisao-v0':
            d['status'] = 'resolvido'
            d['note'] = 'Revisada pelo Gabriel no Premiere em 29/09 (48 marcadores + Lumetri) — aplicada na V1.'
    if not any(d['id'] == 'revisao-v1' for d in m.get('dependencies', [])):
        dv0 = next((d for d in m['dependencies'] if d['id'] == 'revisao-v0'), {})
        m['dependencies'].append(dict({k: v for k, v in dv0.items() if k not in ('id', 'status', 'note', 'label')},
                                      id='revisao-v1', status='pendente', label='Revisão da V1 pelo Gabriel (Studio)',
                                      humanAction='Assistir a V1 no Studio (EP 300 → Versões → ▶ Revisar; a V0 fica no mesmo player), comentar e responder os 10 achados. Pergunta: a V1 ficou mais viva e sem cara de teleprompter?',
                                      origem='V1 entregue em 2026-09-29 (output ep300-abertura, versão V1)'))
    for v in m.get('versions', []):
        if v.get('v') == 0: v['status'] = 'revisada'
    if not any(v.get('v') == 1 for v in m.get('versions', [])):
        m['versions'].append(dict(v=1, label='V1 — Direção do Gabriel aplicada', status='aguardando_conferencia', outputId=OID,
                                  created=TODAY, file=vfile, nota=f'Proxy {int(dur // 60)}:{int(dur % 60):02d}. Revisar em EP 300 → Versões → ▶ Revisar.'))
    json.dump(m, open(pm, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('production ok (backup', bk, ')')
    # --------- board
    b = call('/api/board')
    p = next(x for x in b['projects'] if x['id'] == PID)
    p['next'] = 'Revisar a V1 no Studio: EP 300 → Versões → ▶ Revisar (V0 continua disponível no mesmo player).'
    links = [l for l in p.get('links', []) if 'Revisão V' not in l.get('label', '')]
    p['links'] = links + [{'label': '▶ Revisão V1 (player)', 'url': '#/ep300'}]
    p.setdefault('log', [])
    if not any('V1 entregue' in (x.get('text', '') if isinstance(x, dict) else str(x)) for x in p['log']):
        p['log'].append({'date': TODAY, 'text': 'V1 entregue para revisão (direção do Gabriel no Premiere aplicada; sync corrigido).'})
    p['progress'] = max(p.get('progress', 0), 55)
    call('/api/board', b)
    print('board ok')


if __name__ == '__main__':
    main()
