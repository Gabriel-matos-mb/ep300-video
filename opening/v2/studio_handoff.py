"""EP300 · V2 — handoff no MB Studio (API local :4321). A V2 entra como NOVA versão do mesmo output 'ep300-abertura'.
V0/V1 ficam (histórico); achados/comentários são versionados (a.v / c.v) — só os da V2 aparecem como pendência quando a V2 está selecionada.
Idempotente. Depois de rodar: validar no player real (studio_validate.py)."""
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
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read().decode('utf-8'))


def ts_of(T, cue_id, off=0.0):
    return round(next(c for c in T['cues'] if c['id'] == cue_id)['tl_in'] / 30 + off, 1)


def main():
    T = build.timeline()
    dur = T['total'] / 30
    items = call('/api/outputs')['items']
    o = next(x for x in items if x['id'] == OID)
    name = f'{build.NAME}_PROXY.mp4'
    vfile = f'/outputs-media/{OID}/{name}'
    dst = os.path.join(STUDIO, 'data', 'outputs', OID, name)
    src = os.path.join(build.B, name)
    if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(src):
        up = call(f'/api/outputs/upload?id={OID}&name={name}', raw=open(src, 'rb').read(), ctype='application/octet-stream')
        vfile = up['url']; print('upload', up)
    for a in o.get('achados', []): a.setdefault('v', 'V0')
    for v in o['versoes']:
        if v['v'] == 'V1':
            v['status'] = 'superada'
            v['nota'] = (v.get('nota', '').split(' · Superada')[0] + ' · Superada pela V2 em 29/09 (feedback do Gabriel por chat aplicado).')
    mm = f'{int(dur // 60)}:{int(dur % 60):02d}'
    if not any(v['v'] == 'V2' for v in o['versoes']):
        o['versoes'].append(dict(v='V2', file=vfile, status='pronto', created=TODAY,
            nota=f'V2 — {mm} · cold open com erro+reação+risada · "antes da sessão" falado para a sala (sem clique) · telas cheias encadeadas por empurrão (sem câmera vazando) · '
                 'evolução do programa com frames do acervo (EP 1 → hoje) · logos reais · SFX novos sob a voz · final que vira o LOOP. '
                 'Pergunta da revisão: a V2 parece uma peça contínua e feita para a sala?'))
    else:
        for v in o['versoes']:
            if v['v'] == 'V2': v['file'] = vfile
    o['status'] = 'pronto'; o['updated'] = TODAY
    o['aviso'] = 'PROXY 1280x720 para revisão — não é o master de cinema (1920x1080). Cor = aproximação do Lumetri do Gabriel; SFX sintéticos ainda não auditionados na sala.'
    o['explicacao'] = ('V2 = V1 refinada: arco cinema (cold open humano → "antes da sessão" → Gustavo+Lucian → de onde veio → evolução do programa → mercado → números → pessoas → '
                       '300 → plateia → looping), continuidade entre telas cheias, safe area conservadora, logos reais, stickers novos (Guta, Lucas, Vitória, Bonel, Mafê, Phill, Layla), '
                       'balde de pipoca corrigido, sound design novo. Editável: 02_PROJETOS/EP300_ABERTURA_V2.')
    A = [
        ('qa-v2-1', ts_of(T, 'C00_00', .5), 'alta', 'Cold open humano: bastidor de 2023 mostrando o erro ("Começou mesmo?"), a percepção e a RISADA dos dois — agora sem cortar na frase — e "Tá no ar, tá valendo." Removível (PRESHOTS).',
         'Manter como abertura do filme? Ritmo dos 12 s ok?'),
        ('qa-v2-2', ts_of(T, 'C00_03', .5), 'alta', '"Antes da sessão começar" agora fala com a SALA em 5 páginas (saídas de emergência, levanta a mão, olha pro lado, celular, pipoca + "vocês vieram ao cinema assistir a um podcast"). ~28 s sem voz, ~4,5 s de leitura por página.',
         'Texto e tempo funcionam num cinema? Se estiver longo, corto uma página (A2/A3 em plan.py).'),
        ('qa-v2-3', ts_of(T, 'C00_03', 22), 'media', 'Balde de pipoca: usei a versão corrigida do Gabriel (pipocas dentro, borda frontal na frente).',
         'Confirmar.'),
        ('qa-v2-4', ts_of(T, 'C02_01', 7.3), 'alta', 'História corrigida: "a volta do LUCIAN" (não do Gustavo) + frame real do EP 1 (2021).',
         'Confirmar a linha do tempo (2015 · Prime · MB Talks · volta · podcast).'),
        ('qa-v2-5', ts_of(T, 'C02_03', 1), 'media', 'Evolução do programa: 6 épocas (EP 1/2021, EP 73/2022, EP 100/2023 ao vivo, EP 153/2024, EP 210/2025, hoje) em frames do arquivo histórico oficial + 2,4 s de pausa sem voz para ler. Adicionou ~5 s ao filme.',
         'Vale o tempo? Quer outras épocas/episódios?'),
        ('qa-v2-6', ts_of(T, 'C03_01', 3), 'media', 'Ferramentas: logos reais (GA, GTM, BigQuery, Looker Studio, Power BI, Amplitude*, Ads, Meta, Hotjar, Search Console, Google, Reportei) em adesivo-tile. *Amplitude = wordmark tipográfico (não há logo livre).',
         'Alguma ferramenta a trocar/tirar?'),
        ('qa-v2-7', ts_of(T, 'C03_04', 1), 'media', 'Vitória: mesma foto, sem rótulo de "zoeira"; a graça agora é visual (corações nos olhos).', 'Funciona?'),
        ('qa-v2-8', ts_of(T, 'C06_03', 4.5), 'media', 'Gag "todinho": carton de achocolatado ORIGINAL (texto TODDYNHO + selo GA4). Pica-Pau (24×): silhueta ORIGINAL de pica-pau ligando pra polícia + viatura do Gabriel — o personagem protegido não foi usado nem imitado.',
         'A piada pega? Trocar por outra referência?'),
        ('qa-v2-9', ts_of(T, 'C05_01', 1), 'media', '191 pessoas: só 4 convidados históricos (Phill, Mafê, Bonel, Layla) + 2 frames reais; reações trocam a cada número. Ninguém ficou sem foto.', 'Falta alguém que deveria estar?'),
        ('qa-v2-10', ts_of(T, 'C04_01', 0), 'media', 'Continuidade: telas cheias encostadas agora se empurram (a seguinte desliza da direita) — nenhuma câmera aparece entre elas. Setas removidas, safe area conservadora (90 px), tempo de leitura ajustado nas telas sem voz.',
         'Ainda vê vazamento de câmera em algum ponto? Anote o tempo.'),
        ('qa-v2-11', ts_of(T, 'C01_01', 0), 'alta', 'Áudio: SFX refeitos (sintéticos, macios) e sempre −10 dB sob a voz; big numbers com "tiquetaque" que acompanha o contador (sem scratch); 300 = estouro + confete + língua de sogra curtos. NÃO auditionado em sala/cinema.',
         'Ouvir com o volume de cinema em mente: algum som incomoda ou aparece demais?'),
        ('qa-v2-12', round(dur - 8, 1), 'alta', 'Final → LOOPING: o 300 conta, estoura, Gustavo e Lucian comemoram, e o 300 vira o lockup do loop (mosaico, logo, patrocinadores). Os últimos 1,5 s são os quadros 118,5–120 s do próprio loop — o loop recomeça em 0 sem corte.',
         'Ver o encaixe (a opção "Loop" no Studio começa no mesmo quadro).'),
        ('qa-v2-13', round(dur - 3, 1), 'media', f'Duração {mm} (V1 5:48). Pendências herdadas: números falados × site (191/196, 140/146, 106/107 mil), logo MB Prime (ainda carimbo tipográfico), patrocinadores provisórios (Purple/Onfly).',
         'Confirmar duração aceitável e os dados antes do master.'),
    ]
    o['achados'] = [a for a in o.get('achados', []) if a.get('v') != 'V2'] + [
        dict(id=i, v='V2', origem='qa', ts=ts, severidade=sev, confianca='alta', problema=pb, correcao=cr) for i, ts, sev, pb, cr in A]
    o.pop('revisaoConcluida', None) if o.get('revisaoConcluida') else None      # nova rodada de revisão (histórico fica nos comentários/achados por versão)
    call('/api/outputs', {'items': items})
    print('outputs ok', [v['v'] for v in o['versoes']], len(o['achados']))
    # --------- produção (manifesto) — backup antes
    pm = os.path.join(STUDIO, 'data', 'productions', 'ep300-cinema-opening.json')
    bk = os.path.join(STUDIO, 'data', 'backup', f'ep300-cinema-opening.pre-v2-{datetime.datetime.now():%Y%m%d%H%M}.json')
    os.makedirs(os.path.dirname(bk), exist_ok=True); shutil.copy2(pm, bk)
    m = json.load(open(pm, encoding='utf-8'))
    for d in m.get('dependencies', []):
        if d['id'] == 'revisao-v1':
            d['status'] = 'resolvido'; d['note'] = 'Feedback do Gabriel (chat, 29/09) aplicado na V2 — histórico, não é pendência da V2.'
    if not any(d['id'] == 'revisao-v2' for d in m.get('dependencies', [])):
        dv = next((d for d in m['dependencies'] if d['id'] == 'revisao-v1'), {})
        m['dependencies'].append(dict({k: v for k, v in dv.items() if k not in ('id', 'status', 'note', 'label', 'humanAction', 'origem')},
                                      id='revisao-v2', status='pendente', label='Revisão da V2 pelo Gabriel (Studio)',
                                      humanAction='MB Studio → EP 300 → V2 → ▶ Play → Revisão. Pergunta: a V2 parece uma peça contínua, feita para a sala, e pronta para o master?',
                                      origem='V2 entregue em 2026-09-29 (output ep300-abertura, versão V2)'))
    for v in m.get('versions', []):
        if v.get('v') == 1: v['status'] = 'superada'
    if not any(v.get('v') == 2 for v in m.get('versions', [])):
        m['versions'].append(dict(v=2, label='V2 — Refinamento editorial e fechamento', status='aguardando_conferencia', outputId=OID,
                                  created=TODAY, file=vfile, nota=f'Proxy {mm}. Revisar em EP 300 → V2 → ▶ Play.'))
    json.dump(m, open(pm, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('production ok (backup', bk, ')')
    # --------- board
    b = call('/api/board')
    p = next(x for x in b['projects'] if x['id'] == PID)
    p['next'] = 'Revisar a V2 no Studio: EP 300 → V2 → ▶ Play (V0/V1 continuam no mesmo player como histórico).'
    links = [l for l in p.get('links', []) if 'Revisão V' not in l.get('label', '')]
    p['links'] = links + [{'label': '▶ Revisão V2 (player)', 'url': '#/ep300'}]
    p.setdefault('log', [])
    if not any('V2 entregue' in (x.get('text', '') if isinstance(x, dict) else str(x)) for x in p['log']):
        p['log'].append({'date': TODAY, 'text': 'V2 entregue para revisão (arco cinema, continuidade, SFX, história, final→looping).'})
    p['progress'] = max(p.get('progress', 0), 70)
    call('/api/board', b)
    print('board ok')


if __name__ == '__main__':
    main()
