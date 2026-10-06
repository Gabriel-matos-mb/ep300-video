"""EP300 — pacote de HANDOFF para o Lucian (Abertura V2 + Loop V2). Só COPIA/DERIVA; nada da produção é movido, alterado ou sobrescrito.
Saída: <01_VIDEO DE ABERTURA>/EP300_HANDOFF_LUCIAN/  (estrutura em README.md).  Uso: python handoff_lucian.py
used_in = varredura estática do plan.py/customs (aproximada: aponta cenas em que o arquivo aparece no código, não garante que esteja visível o tempo todo)."""
import os, sys, json, shutil, glob, re, inspect, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'v2'))
sys.stdout.reconfigure(encoding='utf-8')
import build, plan, customs  # noqa: E402

EP = build.EP
OUT = os.path.join(EP, 'EP300_HANDOFF_LUCIAN')
W = build.WORK
V2W = os.path.join(W, 'v2'); V1W = os.path.join(W, 'v1')
LOOP = os.path.abspath(os.path.join(HERE, '..', 'ep300-cinema-loop'))
A_V2 = os.path.join(EP, '00_ASSETS E INSERTS', 'V2_GERADOS')
MA = build.MA
TODAY = '2026-09-30'


def _lp(p):
    p = os.path.abspath(p).replace('/', os.sep)
    pre = os.sep * 2 + '?' + os.sep
    return p if p.startswith(pre) else pre + p


def cp(src, rel):
    dst = os.path.join(OUT, rel)
    os.makedirs(_lp(os.path.dirname(dst)), exist_ok=True)
    s, d = _lp(src), _lp(dst)
    if not (os.path.exists(d) and os.path.getsize(d) == os.path.getsize(s)):
        shutil.copy2(s, d)
    return rel.replace('\\', '/')


def wr(rel, text):
    dst = _lp(os.path.join(OUT, rel)); os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'w', encoding='utf-8').write(text)


# ---------------------------------------------------------------- uso por cena (varredura estática)
T = build.timeline()
CUE = {c['id']: c for c in T['cues']}
BLOB = {}
for c in plan.CUES:
    b = json.dumps(c['els'], default=str, ensure_ascii=False)
    for el in c['els']:
        if el.get('k') == 'custom':
            fn = customs.FUNCS[el['fn']]
            b += inspect.getsource(fn)
    BLOB[c['id']] = b
LOOP_SCENE = open(os.path.join(LOOP, 'scene.json'), encoding='utf-8').read()


def used(pats, loop_pats=None):
    cues = [f"{cid} {CUE[cid]['name']}" for cid, b in BLOB.items() if any(p in b for p in pats)]
    if loop_pats and any(p in LOOP_SCENE for p in loop_pats): cues.append('LOOP V2')
    return cues


def why_of(cue_label):
    cid = cue_label.split()[0]
    return CUE[cid].get('why', '') if cid in CUE else ''


REG = []


def add(id_, name, type_, rel, source, pats=None, purpose='', meaning='', ctx='', reusable=True, lic='', notes='', loop_pats=None, used_in=None):
    ui = used_in if used_in is not None else (used(pats, loop_pats) if pats else [])
    if not ctx and ui:
        w = why_of(ui[0])
        ctx = f'Usado na cena {ui[0]}: ' + (w[:260] + ('…' if len(w) > 260 else '')) if w else ('Usado no Loop V2 (ver scene.json).' if ui[0].startswith('LOOP') else '')
    if not ctx and not ui:
        ctx = 'Nenhuma referência encontrada em plan.py/customs/scene.json (varredura estática): disponível no pacote (variação/estado alternativo ou material histórico), não visível na V2.'
    REG.append(dict(id=id_, name=name, type=type_, file=rel, source=source, used_in=ui, purpose=purpose, visual_meaning=meaning,
                    usage_context=ctx or 'Não há evidência de uso específico registrada.', reusable=reusable, license_or_provenance=lic, notes=notes))


STK = os.path.join(V2W, 'assets', 'stickers')
PROV_ST = json.load(open(os.path.join(STK, 'PROVENANCE.json'), encoding='utf-8'))
PERSON = dict(GUTA='Guta Tolmasquim (Purple Metrics)', LUCAS='Lucas Yokota (Purple Metrics)', VITORIA='Vitória Comarin', MAFE='Mafê Neurauter',
              PHILLIP='Phill Mello', BONEL='Cláudio “Coisa Rica” Bonel', LAYLA='Layla Sayed')

# ================================================================ 03_SHARED_ASSETS / stickers de pessoas
for f in sorted(glob.glob(os.path.join(STK, '*', '*.png'))):
    person = os.path.basename(os.path.dirname(f)); fn = os.path.basename(f)
    rel = cp(f, f'03_SHARED_ASSETS/stickers/{person}/{fn}')
    pv = PROV_ST.get(f'{person}/{fn}', {})
    add(f'sticker_{person}_{fn[:-4]}'.lower(), f'Sticker {PERSON[person]} — {fn[3:-4]}', 'sticker_pessoa', rel, 'CREATED FOR EP300',
        [f'{person}/{fn}'], 'Rosto-adesivo (contorno branco) para momentos de pessoas/convidados', 'Linguagem de colagem/sticker do site; estados = reações',
        lic=f"Adesivo feito pelo Gabriel para o EP300 a partir de foto da pessoa (arquivo original: {pv.get('origem', '?')}). Tratamento neste pacote: {pv.get('tratamento', '?')}",
        notes='Rostos não foram alterados; só corte de margem / fundo preto→alpha. Original em 00_ASSETS E INSERTS/stickers e emojis refeitos.')
for who in ('gustavo', 'lucian'):
    for st in ('still', 'hover-transicao', 'hover-final', 'arraste-final'):
        src = os.path.join(build.EP, '00_ASSETS E INSERTS', '300-handoff-video', 'assets', 'personagens', who, st + '.webp')
        rel = cp(src, f'03_SHARED_ASSETS/stickers/{who.upper()}_oficial/{st}.webp')
        add(f'personagem_{who}_{st}', f'{who.capitalize()} (site) — {st}', 'sticker_pessoa', rel, 'MB OFFICIAL',
            [f'"who": "{who}"', f"'{who}'", f'personagens/{who}/{st}'], 'Rosto-adesivo vivo dos apresentadores (4 estados do site)',
            'still=base · hover-transicao=sorriso · hover-final=surpresa · arraste-final=olhar de lado',
            lic='Handoff visual do site do EP300 (Claudio/Lucian), 28/09 — 00_ASSETS E INSERTS/300-handoff-video/assets/personagens', loop_pats=[f'stickers/{who}/'],
            notes='used_in aproximado: a varredura encontra o apresentador, não o estado exato.')
for nm, src, rel_ in (('balde_pipoca_cheio', os.path.join(V2W, 'assets', 'balde_pipoca_cheio.png'), 'graphics'),
                      ('viatura', os.path.join(V2W, 'assets', 'viatura.png'), 'graphics'),
                      ('pipoca_icone', os.path.join(V2W, 'assets', 'pipoca_icone.png'), 'graphics')):
    rel = cp(src, f'03_SHARED_ASSETS/{rel_}/{nm}.png')
    meta = dict(balde_pipoca_cheio=('Balde de pipoca EP300 (versão CORRIGIDA: borda traseira → pipocas dentro → borda frontal à frente)', 'Objeto do cinema; arte oficial da embalagem (logos/textos preservados)', ['balde_pipoca_cheio'], 'Arte da caixa de pipoca do EP300 (PDFs de gabarito em 00_ASSETS E INSERTS) — versão refeita pelo Gabriel em 29/09', 'CREATED FOR EP300'),
                viatura=('Viatura (sticker)', 'Gag “se o Pica-Pau tivesse chamado a polícia” / “nós chamamos” (PM-RJ)', ['viatura.png'], 'Sticker feito pelo Gabriel em 29/09; método de criação não registrado', 'CREATED FOR EP300'),
                pipoca_icone=('Ícone de pipoca', 'Usado no gag do loop antes do balde corrigido (V1); na V2 o loop usa o balde', ['pipoca_icone'], 'STICKER PIPOCA.png (stickers e emojis refeitos)', 'CREATED FOR EP300'))[nm]
    add(nm, meta[0], 'grafico', rel, meta[4], meta[2], meta[1], 'Elemento de ambientação de cinema/humor', lic=meta[3])

# gags originais, logos de ferramentas
for nm, rel_src, what, pats in (
        ('gag_toddynho_ga4', 'gag_toddynho_ga4.png', 'Carton de achocolatado ORIGINAL (texto TODDYNHO + selo GA4) — gag “o GA4 era esse todinho todo?”', ['gag_toddynho_ga4']),
        ('gag_picapau_silhueta', 'gag_picapau_silhueta.png', 'Silhueta ORIGINAL de pica-pau (“Alô, polícia?”) — referência indireta, sem o personagem protegido', ['gag_picapau_silhueta'])):
    rel = cp(os.path.join(V2W, 'assets', rel_src), f'03_SHARED_ASSETS/graphics/{rel_src}')
    add(nm, nm, 'grafico', rel, 'GENERATED', pats, what, 'Piada visual sem reproduzir marca/personagem de terceiros',
        lic='Desenhado em código (v2/make_art_v2.py, Pillow) para o EP300 — sem fonte externa', notes='Se a marca Toddynho precisar de clearance, trocar por carton genérico.')
TOOLS = dict(googleanalytics='Google Analytics', googletagmanager='Google Tag Manager', googlebigquery='BigQuery', looker='Looker Studio', powerbi='Power BI',
             googleads='Google Ads', meta='Meta', hotjar='Hotjar', googlesearchconsole='Google Search Console', google='Google', amplitude='Amplitude')
for k, nm in TOOLS.items():
    src = os.path.join(V2W, 'assets', 'logos', k + '.png')
    rel = cp(src, f'03_SHARED_ASSETS/logos/ferramentas/{k}.png')
    svg = os.path.join(V2W, 'logos', k + '.svg')
    if os.path.exists(svg): cp(svg, f'03_SHARED_ASSETS/logos/ferramentas/fonte_svg/{k}.svg')
    add(f'logo_{k}', f'Logo {nm} (tile-adesivo)', 'logo', rel, 'GENERATED', [f'logos/{k}.png'], 'Ecossistema de ferramentas de analytics/mídia/BI na cena “no começo, quase tudo era ferramenta”',
        'Glifo da marca em cor oficial sobre tile branco arredondado com sombra sólida (linguagem de adesivo)',
        lic=('Glifo de simple-icons@13 (CC0) renderizado em tile por v2/make_logos.py; marcas registradas pertencem aos respectivos donos — uso referencial/editorial' if k != 'amplitude'
             else 'Wordmark tipográfico desenhado em código (não há logo livre no simple-icons); não é o logo oficial da Amplitude'),
        notes='Para uso com logo oficial, substituir pelo arquivo de marca do fabricante.')
# patrocinadores / marca
for f in sorted(glob.glob(os.path.join(LOOP, 'assets', 'sponsors', '*.webp'))):
    nm = os.path.basename(f)[:-5]
    rel = cp(f, f'03_SHARED_ASSETS/logos/patrocinadores/{nm}.webp')
    add(f'patrocinador_{nm}', f'Logo {nm}', 'logo', rel, 'MB OFFICIAL', [f'patrocinadores/{nm}', f'sponsors/{nm}'], 'Bloco de patrocínio / café oficial / realização',
        'Logos dos parceiros do evento', lic='Handoff visual do site do EP300 (assets/patrocinadores) — logos dos parceiros; uso autorizado pelo evento',
        loop_pats=[f'sponsors/{nm}'], notes='PROVISÓRIO: naming/logos finais de Purple Metrics e Onfly a confirmar (registrado no Studio).')
for nm, src, pats in (('logo_metricas_boss_branca', os.path.join(LOOP, 'assets', 'brand', 'logo-metricas-boss-branca.png'), ['selo_metricas_boss', 'logo-metricas-boss']),
                      ('logo_metricas_boss_branca_svg', os.path.join(LOOP, 'assets', 'brand', 'logo-metricas-boss-branca.svg'), None)):
    rel = cp(src, f'03_SHARED_ASSETS/logos/{os.path.basename(src)}')
    add(nm, 'Logo Métricas Boss (branca)', 'logo', rel, 'MB OFFICIAL', pats, 'Realização no bloco de patrocinadores do loop', 'Logo oficial — nunca rotacionar/deformar',
        lic='SVG do repositório remotion-mb (logo-mb-branca.svg)', loop_pats=['logo-metricas-boss'] if pats else None)
for nm, src, rel_ in (('selo_analytics_talks', os.path.join(LOOP, 'assets', 'brand', 'selo-analytics-talks.webp'), 'logos'),
                      ('selo_episodio_300', os.path.join(V1W, 'pipoca', 'selo_episodio_300.png'), 'logos'),
                      ('selo_metricas_boss_pipoca', os.path.join(V1W, 'pipoca', 'selo_metricas_boss.png'), 'logos'),
                      ('selo_purple_metrics_pipoca', os.path.join(V1W, 'pipoca', 'selo_purple_metrics.png'), 'logos')):
    rel = cp(src, f'03_SHARED_ASSETS/{rel_}/{os.path.basename(src)}')
    add(nm, nm, 'logo', rel, 'MB OFFICIAL' if 'analytics_talks' in nm else 'CREATED FOR EP300', [os.path.basename(src)[:-4]] if 'selo_ep' in nm or 'analytics' in nm else [os.path.basename(src)[:-4]],
        'Selo/lockup do programa ou do evento', 'Selo “EPISÓDIO 300” com Gustavo e Lucian / logo Analytics Talks',
        lic=('Handoff visual do site (stickers/selo-analytics-talks.webp)' if 'analytics_talks' in nm else 'Recortado (rembg local) do PDF de gabarito da caixa de pipoca EP300 (3_caixa_de_pipoca_EP300_sem_linhas.pdf)'),
        loop_pats=['selo-analytics-talks'] if 'analytics_talks' in nm else None)

# imagens históricas e prints
HIST_INFO = dict(EP001_2021_DIGITAL_ANALYTICS_EM_2021=('EP 1 (2021) — Digital Analytics em 2021', 'YouTube Métricas Boss 4EPVBU7WgDg (canal próprio), frame em 1985 s'),
                 EP073_2022_BIGQUERY=('EP 73 (2022) — BigQuery', '00_ARQUIVO_HISTORICO/…/01_2022/73_BIG QUERY/01_BRUTOS'),
                 EP084_2022_VERDADES=('EP 84 (2022) — Verdades inconvenientes', '00_ARQUIVO_HISTORICO/…/01_2022/84_VERDADES…/03_EDITADOS'),
                 EP100_2023_PLATEIA=('EP 100 (2023) — ao vivo com plateia', '00_ARQUIVO_HISTORICO/…/02_2023/100_EPISODIO 100/03_EDITADOS'),
                 EP153_2024_POWERBI_LOOKER=('EP 153 (2024) — Power BI × Looker Studio', '00_ARQUIVO_HISTORICO/…/03_2024/153_…/02_EDITADO'),
                 EP187_2024_MMM=('EP 187 (2024) — Marketing Mix Modeling (convidado remoto)', '00_ARQUIVO_HISTORICO/…/03_2024/187_MARKETIN MIX MODELING/03_EDITADOS'),
                 EP210_2025_MERIDIAN=('EP 210 (2025) — Google Meridian', '00_ARQUIVO_HISTORICO/…/04_2025/210_GOOGLE MERIDIAN/03_EDITADOS'),
                 EP300_2026_HOJE=('EP 300 (2026) — hoje (CAM_GERAL)', '01_BRUTOS/CAM_GERAL.mp4 em 514,9 s'))
for f in sorted(glob.glob(os.path.join(V2W, 'assets', 'hist', '*.png'))):
    k = os.path.basename(f)[:-4]; ttl, org = HIST_INFO[k]
    rel = cp(f, f'03_SHARED_ASSETS/images/historico/{k}.png')
    add(f'hist_{k.lower()}', ttl, 'imagem_frame', rel, 'MB OFFICIAL', [k], 'Mostrar tempo + evolução visual do programa (cenário, roupa, iluminação, formato)',
        'Frame único representativo da época', lic=f'Frame extraído de material MB: {org}', notes='Frame em baixa resolução (miniatura de contact sheet / 960 px); re-extrair do original para uso em alta.')
pr = json.load(open(os.path.join(V1W, 'prints', 'PROVENANCE.json'), encoding='utf-8'))
for f in sorted(glob.glob(os.path.join(V1W, 'prints', 'EP*.png'))):
    fn = os.path.basename(f)
    rel = cp(f, f'03_SHARED_ASSETS/images/prints_episodios/{fn}')
    add(f'print_{fn[:-4].lower()}', f'Print {fn[:-4]}', 'imagem_frame', rel, 'MB OFFICIAL', [fn[:-4]], 'Quadro real de episódio recente (polaroid na pilha do bordão / mural 191)',
        'Prova visual de que o programa existe há anos', lic=f"Print das pastas de produção do podcast: {pr.get(fn, '?')}", loop_pats=[fn[:-4]])
for fn, t_ in (('f_guest.png', 'PM-RJ convidado'), ('f_duo.png', 'PM-RJ dupla')):
    rel = cp(os.path.join(V1W, 'ep126', fn), f'03_SHARED_ASSETS/images/ep126_pmerj/{fn}')
    add(f'ep126_{fn[:-4]}', f'EP 126 PMERJ — {t_}', 'imagem_frame', rel, 'MB OFFICIAL', [f'ep126/{fn}'], 'Gag “nós chamamos a polícia… gravamos com a PM do RJ”',
        'Trecho real do EP 126', lic='Frame de 00_ARQUIVO_HISTORICO/01_VIDEOS/08_OUTROS/02_MAKING_OFF/126_ANALISE DE DADOS NA PMERJ.mp4', loop_pats=[fn])
for fn in ('caixa_pipoca_frente.png', 'caixa_pipoca_verso.png'):
    rel = cp(os.path.join(V1W, 'pipoca', fn), f'03_SHARED_ASSETS/graphics/{fn}')
    add(fn[:-4], fn[:-4], 'grafico', rel, 'CREATED FOR EP300', [], 'Caixa de pipoca EP300 (versão V1, anterior à corrigida)', 'Referência histórica', reusable=False,
        lic='Recortada (rembg local) de 4_caixa_de_pipoca_EP300_simulacao_3D_e_gabarito.pdf', notes='SUPERADA pelo balde_pipoca_cheio (geometria corrigida). Mantida só como referência.')
# sofá, stickers de referência
sofa = os.path.join(build.EP, '00_ASSETS E INSERTS', '300-handoff-video', 'assets', 'cena-sofa')
for i in range(1, 7):
    f = os.path.join(sofa, f'{i}.webp')
    if os.path.exists(f):
        rel = cp(f, f'03_SHARED_ASSETS/graphics/cena_sofa/{i}.webp')
        add(f'cena_sofa_{i}', f'Cena do sofá — quadro {i}', 'grafico', rel, 'MB OFFICIAL', ['cena-sofa', '"sofa"', 'fn_sofa', "'sofa'"], 'Animação do sofá (6 quadros) usada em “de volta para 2038”',
            'Cena do site', lic='Handoff visual do site do EP300 (assets/cena-sofa)', notes='Homenagem tipográfica a “De Volta para o Futuro” foi feita só com texto; nenhuma imagem de terceiros.')

# fontes (referência)
for fn, fam in (('Sora-VariableFont_wght.ttf', 'Sora'), ('Inter-VariableFont_opsz_wght.ttf', 'Inter')):
    rel = cp(os.path.join(HERE, 'v2', 'fonts', fn), f'03_SHARED_ASSETS/fonts_reference/{fn}')
    add(f'fonte_{fam.lower()}', f'Fonte {fam}', 'fonte', rel, 'EXTERNAL REFERENCE', [f"'{fam.lower()}'", 'sora' if fam == 'Sora' else 'inter'], 'Sora = títulos/números/adesivos (peso 800); Inter = overlines/legendas pequenas',
        'Tipografia pesada do site', ctx='Usada em todos os textos renderizados da Abertura (gfx.py) e do Loop (build.py).', lic=f'{fam} — Google Fonts (SIL Open Font License)', notes='Emojis são renderizados com Segoe UI Emoji do Windows (não redistribuível, não copiado).')

# ================================================================ ÁUDIO
MUS = {'MA_LEXMusic_BeatTheOdds_30s.wav': ('aviso', 'Beat The Odds (LEX Music) 30 s', 'Trilha do “antes da sessão”, −13 dB, repete para cobrir os ~31 s'),
       'Trigubovich_A_Groove_Pool_loop_long.wav': ('bed', 'A Groove Pool (Trigubovich) — loop', 'Cama sob o diálogo, −31 dB (+10 dB no respiro “Gritem”)'),
       'MA_Puremusic_InTheSpotlight_12s.wav': ('final', 'In The Spotlight (Puremusic) 12 s', 'Trilha do título/final, −9 dB, fade-in 1,2 s')}
src_ma = {}
for ln in open(os.path.join(MA, 'SOURCES.txt'), encoding='utf-8'):
    if '<-' in ln:
        a, b = ln.strip().split(' <- ', 1); src_ma[a] = b
sfx_uses = {}
for t, k in build.sfx_events(T):
    sfx_uses.setdefault(k, set())
for c in T['cues']:
    for dt, k in c.get('sfx', []): sfx_uses.setdefault(k, set()).add(f"{c['id']} {c['name']}")
for f, (role, nm, use) in MUS.items():
    rel = cp(os.path.join(MA, f), f'03_SHARED_ASSETS/audio/musica/{f}')
    add(f'musica_{role}', nm, 'musica', rel, 'MOTION ARRAY', used_in=[{'aviso': 'C00_03 AVISO_ANTES_DA_SESSAO', 'bed': 'fundo sob o diálogo (S1…S7)', 'final': 'C08_01/C09_01 título e final'}[role]],
        purpose='Trilha da abertura', meaning='Energia leve de cinema/pré-sessão', ctx=use,
        lic=f'Motion Array — obtido pela conta/licença já disponível da Métricas Boss. Origem local: {src_ma.get(f, "?")}',
        notes='license_note: asset licenciado pela MB; não tratar como criação própria; redistribuição fora do ambiente autorizado não verificada — manter dentro da MB.')
for k, (f, g, rng) in build.SFX.items():
    rel = cp(os.path.join(MA, f), f'03_SHARED_ASSETS/sfx/motion_array/{f}')
    add(f'sfx_ma_{k}', f"SFX “{k}” ({f})", 'sfx', rel, 'MOTION ARRAY', used_in=sorted(sfx_uses.get(k, [])), purpose='Efeito sonoro da abertura', meaning='',
        ctx=f'Ganho no mix: {g} dB + low-pass 7 kHz + ducking −12 dB sob a voz.', lic=f'Motion Array — licença da conta MB. Origem local: {src_ma.get(f, "?")}',
        notes='license_note: obtido pela licença já disponível da Métricas Boss; manter dentro da MB.')
for f in sorted(glob.glob(os.path.join(build.L_AUD, 'SFX_*.wav'))):
    fn = os.path.basename(f); k = fn[4:-4]
    rel = cp(f, f'03_SHARED_ASSETS/sfx/sinteticos/{fn}')
    key = k.replace('SYN_', '')
    add(f'sfx_{k.lower()}', f'SFX {k}', 'sfx', rel, 'GENERATED', used_in=sorted(sfx_uses.get(key, [])), purpose={'SYN_party': 'Festa do 300: estouro + confete + língua de sogra', 'BLEEP_1kHz': 'Bleep de palavrão', 'LEADER_BEEP_1kHz': 'Bipe da contagem de película'}.get(k, 'Big numbers (tique-taque que sobe), impactos e pops macios'),
        meaning='', ctx='Sintetizado em numpy (v2/sfx_v2.py), macio, sem agudos agressivos.', lic='Gerado em código (sfx_v2.py) para o EP300 — custo zero, sem fonte externa')
for f, nm in (('COLD_B_2023_05_24.wav', 'Áudio do bastidor 24/05/2023 (cold open)'), ('COLD_B_VERDADES.wav', 'Áudio do bastidor “Verdades Inconvenientes” (cold open)')):
    rel = cp(os.path.join(build.L_AUD, f), f'03_SHARED_ASSETS/audio/bastidores/{f}')
    add(f'audio_{f[:-4].lower()}', nm, 'audio_bastidor', rel, 'MB OFFICIAL', used_in=['C00_00 COLD_OPEN_ARQUIVO'], purpose='Som ambiente + voz do cold open', ctx='Normalizado (loudnorm −20) e com highpass 80 Hz.',
        lic='Extraído de 00_ASSETS E INSERTS/erros de gravação antigos/ (material MB)')

# ================================================================ 01_OPENING
op = dict(master=[], editable=[], xml=[], assets=[])
op['master'].append(cp(os.path.join(build.D_EDIT, 'EP300_ABERTURA_V2_PROXY.mp4'), '01_OPENING/MASTER_REFERENCE/EP300_ABERTURA_V2_PROXY.mp4'))
P2 = os.path.join(EP, '02_PROJETOS', 'EP300_ABERTURA_V2')
op['xml'].append(cp(os.path.join(P2, 'EP300_ABERTURA_V2.xml'), '01_OPENING/XML/EP300_ABERTURA_V2.xml'))
for f in ('timeline_v2.json', 'README_EDITAVEL_V2.md', 'EDIT_PLAN_V2.md', 'BACKUP_VERIFICACAO_V2.txt'):
    op['editable'].append(cp(os.path.join(P2, f), f'01_OPENING/EDITABLE/{f}'))
for f in sorted(glob.glob(os.path.join(P2, 'FONTE_CODIGO', '*.py'))) + [os.path.join(HERE, 'v2', 'fonts', 'Sora-VariableFont_wght.ttf')]:
    op['editable'].append(cp(f, f'01_OPENING/EDITABLE/FONTE_CODIGO/{os.path.basename(f)}'))
for f in ('STEM_DIALOGO.wav', 'STEM_TRILHA.wav', 'STEM_SFX.wav'):
    op['editable'].append(cp(os.path.join(build.L_AUD, f), f'01_OPENING/EDITABLE/audio_stems/{f}'))
op['editable'].append(cp(os.path.join(build.B, 'mix.wav'), '01_OPENING/EDITABLE/audio_stems/REF_MIX_V2.wav'))
for f in sorted(glob.glob(os.path.join(build.L_OVL, '*_ref.png'))):
    op['assets'].append(cp(f, f'01_OPENING/ASSETS/overlays_ref/{os.path.basename(f)}'))
for k in ('B_2023_05_24', 'B_VERDADES'):
    op['assets'].append(cp(build.MEDIA_XML[k], f'01_OPENING/ASSETS/bastidores_cold_open/{k}.mp4'))
wr('01_OPENING/ASSETS/OVERLAYS_LOCALIZACAO.txt',
   'Os 44 overlays ProRes 4444 com alpha (1920x1080, 30 fps, ~3,5 GB) NÃO foram duplicados. Localização oficial (estável, a mesma que o XML referencia):\n'
   f'  {os.path.join(A_V2, "OVERLAYS")}\n'
   'Nomes: Cxx_yy_NOME.mov (ver 04_MANIFEST/timeline-notes.md para a tabela cena → tempo → intenção). As miniaturas *_ref.png ao lado são quadros de referência.\n'
   'Telas cheias encadeadas se estendem 0,4 s sob a seguinte (empurrão) — por isso alguns .mov têm 12 quadros a mais que a duração nominal.\n')
for k, (f, nm) in (('B_2023_05_24', ('B_2023_05_24.mp4', 'Bastidor 24/05/2023')), ('B_VERDADES', ('B_VERDADES.mp4', 'Bastidor Verdades Inconvenientes'))):
    add(f'bastidor_{k.lower()}', nm, 'video_bastidor', f'01_OPENING/ASSETS/bastidores_cold_open/{f}', 'MB OFFICIAL', used_in=['C00_00 COLD_OPEN_ARQUIVO'],
        purpose='Cold open humano: erro + reação + risada', meaning='Começar com pessoas', ctx='Trecho 0–9,3 s (b0) e 19,45–21,92 s (b3); tratado em PB + grão + REC no render.',
        lic='Cópia de 00_ASSETS E INSERTS/erros de gravação antigos/ (nome curto por limite de 260 caracteres do Windows)')
add('overlays_abertura_v2', 'Overlays da Abertura V2 (44 × ProRes 4444 alpha)', 'overlay', 'NÃO COPIADO → ' + os.path.join(A_V2, 'OVERLAYS'), 'GENERATED', used_in=['todas as cenas Cxx'],
    purpose='Camada de motion sobre a câmera', meaning='Linguagem de colagem/sticker animada', ctx='Gerados por v2/build.py a partir de plan.py (determinístico).', lic='Gerado para o EP300 com Pillow/numpy/FFmpeg (custo zero)')

# ================================================================ 02_LOADING_LOOP
lp = dict(master=[], editable=[], xml=[], assets=[])
lp['master'].append(cp(os.path.join(LOOP, 'out', 'EP300_LOOP_V2_PROXY.mp4'), '02_LOADING_LOOP/MASTER_REFERENCE/EP300_LOOP_V2_PROXY.mp4'))
PL = os.path.join(EP, '02_PROJETOS', 'EP300_LOOP_V2')
for f in ('scene.json', 'build.py', 'make_v1_scene.py', 'qa.py', 'README.md', 'LEIAME_V2.md', 'scene_V1.json'):
    lp['editable'].append(cp(os.path.join(PL, f), f'02_LOADING_LOOP/EDITABLE/{f}'))
lp['editable'].append(cp(os.path.join(PL, 'fonts', 'Sora-VariableFont_wght.ttf'), '02_LOADING_LOOP/EDITABLE/fonts/Sora-VariableFont_wght.ttf'))
lp['editable'].append(cp(os.path.join(PL, 'QA', 'qa_report.json'), '02_LOADING_LOOP/EDITABLE/qa_report.json'))
wr('02_LOADING_LOOP/XML/SEM_XML.txt', 'O loop NÃO tem XML/projeto de Premiere: ele é renderizado por scene.json + build.py (manifesto editável; ver README do EDITABLE). Não há timeline de NLE para exportar.\n')
mosaic = sorted(glob.glob(os.path.join(LOOP, 'assets', 'mosaic', '*.jpg')))
for f in mosaic: lp['assets'].append(cp(f, f'02_LOADING_LOOP/ASSETS/mosaic/{os.path.basename(f)}'))
for f in sorted(glob.glob(os.path.join(LOOP, 'assets', 'thumbs', '*.png'))): lp['assets'].append(cp(f, f'02_LOADING_LOOP/ASSETS/thumbs/{os.path.basename(f)}'))
add('loop_mosaico_acervo', f'Mosaico de acervo do loop ({len(mosaic)} imagens)', 'imagem_colagem', '02_LOADING_LOOP/ASSETS/mosaic/', 'MB OFFICIAL', used_in=['LOOP V2'],
    purpose='Fundo “300 episódios de história” (92 cartões, parallax lento, troca lenta em 16)', meaning='Acervo = tempo acumulado',
    ctx='t_EP* = thumbs oficiais EP260–289; p_EP* = prints do estúdio; b_EP* = prints de bastidor; r_f_* = quadros do EP 126 (Rio). Só acervo conhecido (busca dirigida).',
    lic='Thumbs oficiais e prints dos episódios (pastas de produção do podcast, Drive MB)', notes='Não há thumbs de episódios anteriores ao 251 — limitação registrada no README do loop. EXCLUSIVO do loop.')
add('loop_scene_json', 'scene.json (manifesto do loop)', 'manifesto', '02_LOADING_LOOP/EDITABLE/scene.json', 'CREATED FOR EP300', used_in=['LOOP V2'],
    purpose='Toda a composição/animação do loop (cartões, atores, presença por keyframes, patrocinadores)', meaning='', ctx='Asset visual ≠ lógica de animação: trocar arquivo mantendo nome, ou editar os caminhos.',
    lic='Gerado por make_v1_scene.py, editável à mão')

# ================================================================ documentação
ovl = json.load(open(os.path.join(build.B, 'timeline_v2.json'), encoding='utf-8'))
rows = '\n'.join(f"| {o['id']} | {o['tl_in']} → {o['tl_out']} | {'tela cheia' if o['tela_cheia'] else 'sobre câmera'} | {o['intencao']} |" for o in ovl['overlays'])
segs = '\n'.join(f"| {s['id']} | {s['fonte_in_s']}–{s['fonte_out_s']} s | {s['tl_in']} → {s['tl_out']} |" for s in ovl['segmentos'])
wr('04_MANIFEST/timeline-notes.md', f'''# EP300 · Abertura V2 — notas da timeline (gerado de timeline_v2.json em {TODAY})

Duração {ovl['duracao']} ({ovl['duracao_s']} s) · {ovl['fps']} fps · master de edição 1920x1080 (proxy 1280x720). Timecodes = MM:SS:FF.

## Sync
{ovl['sync']['correcao']}. `w_video_lead_frames` = {ovl['sync']['w_video_lead_frames']}. Validação: SYNC_E_FEEDBACK/sync_report.json no projeto.

## Segmentos de diálogo (CAM_GERAL, áudio da mesa)
| id | fonte | timeline |
|---|---|---|
{segs}

## Overlays (cena → tempo → intenção)
| id | timeline | tipo | intenção |
|---|---|---|---|
{rows}

## Áudio
{json.dumps(ovl['audio'], ensure_ascii=False, indent=1)}

SFX: {len(ovl['sfx'])} eventos (lista em timeline_v2.json › sfx). Mix final −16 LUFS / −1,5 dBTP; SFX com ducking −12 dB sob a voz.

## Cortes editoriais e bleeps
{json.dumps(ovl['cortes_editoriais'], ensure_ascii=False, indent=1)}
{json.dumps(ovl['bleeps'], ensure_ascii=False, indent=1)}

## Loop (separado da abertura)
1920x1080 · 30 fps · 120 s · sem áudio · loop exato (frame 120 s ≡ frame 0). Os últimos 1,5 s da abertura (C09_01) são os quadros 118,5–120 s do loop — o loop recomeça no quadro 0 sem corte.
''')

CATS = {}
for a in REG: CATS.setdefault(a['source'], 0); CATS[a['source']] += 1
json.dump(dict(gerado_em=TODAY, nota='Estado do EP300 no momento do handoff; pode receber refinamentos da validação final. used_in = varredura estática (aproximada).',
               categorias_proveniencia=['MB OFFICIAL', 'MOTION ARRAY', 'GENERATED', 'CREATED FOR EP300', 'EXTERNAL REFERENCE', 'UNKNOWN'], contagem=CATS, assets=REG),
          open(_lp(os.path.join(OUT, '04_MANIFEST', 'assets.json')) if os.path.isdir(_lp(os.path.join(OUT, '04_MANIFEST'))) else (os.makedirs(_lp(os.path.join(OUT, '04_MANIFEST')), exist_ok=True) or _lp(os.path.join(OUT, '04_MANIFEST', 'assets.json'))), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

ma_rows = '\n'.join(f"| {a['name']} | {', '.join(a['used_in'][:3]) or '—'} | {a['license_or_provenance']} |" for a in REG if a['source'] == 'MOTION ARRAY')
wr('04_MANIFEST/provenance.md', f'''# Proveniência dos assets (EP300 · {TODAY})

Categorias: MB OFFICIAL · MOTION ARRAY · GENERATED · CREATED FOR EP300 · EXTERNAL REFERENCE · UNKNOWN. Contagem em assets.json: {json.dumps(CATS, ensure_ascii=False)}.

## Motion Array (licença da conta da Métricas Boss)
Somente ÁUDIO foi usado (nenhum template/vídeo/gráfico do Motion Array entrou na Abertura V2 nem no Loop V2). Arquivos brutos vieram de pastas `02_PROJETOS/Motion Array Assets/` de outros episódios (origem completa em `work/audio/ma/SOURCES.txt`; aqui por arquivo).
Não tratar como criação própria. Redistribuição fora do ambiente autorizado não foi verificada — mantido referência/cópia dentro da MB.

| item | usado em | licença / origem |
|---|---|---|
{ma_rows}

## Itens sem fonte externa (GENERATED)
Logos de ferramentas (simple-icons@13, CC0 — marcas pertencem aos donos), Amplitude (wordmark nosso), gags Toddynho/pica-pau (arte original), SFX sintéticos (numpy), overlays (código), bandeiras (desenhadas em extra.py; os 65 .webp oficiais ficam no repositório do site, privado/não acessado).

## Referências externas
Fontes Sora/Inter (Google Fonts, OFL) — cópia incluída. Emojis: Segoe UI Emoji (Windows) — NÃO incluído. Personagens/marcas de terceiros (Pica-Pau, Game of Thrones, Breaking Bad, De Volta para o Futuro): NÃO usados como imagem; só referência textual/indireta.

## UNKNOWN / a confirmar
- Autoria/método dos stickers refeitos (viatura, balde): feitos pelo Gabriel; método não registrado.
- Naming/logos finais de Purple Metrics/Onfly: provisórios.
- Logo MB Prime: ausente (carimbo tipográfico na Abertura).
''')

wr('README.md', f'''# EP300 — HANDOFF VISUAL
Analytics Talks — Episódio 300

> Este pacote representa o estado atual do EP300 no momento do handoff e pode receber refinamentos posteriores decorrentes da validação final de Gustavo/Lucian.
> Preparado em {TODAY}. É uma CÓPIA/derivação da produção — nada da pasta oficial foi movido, reorganizado ou sobrescrito.

## O que tem aqui
| Pasta | Conteúdo |
|---|---|
| `01_OPENING/` | **Abertura V2** (vídeo narrativo antes da gravação, 6:10). `MASTER_REFERENCE` = proxy 720p (master de cinema 1920x1080 **ainda não renderizado**); `XML` = Premiere (2 sequências, 42 marcadores); `EDITABLE` = manifesto, edit plan, código-fonte (`plan.py` decide tudo), stems de áudio; `ASSETS` = miniaturas dos overlays + bastidores do cold open. |
| `02_LOADING_LOOP/` | **Loop do telão V2** (120 s, 1920x1080, 30 fps, sem áudio, loop exato) — **outra peça**, exibida durante a gravação. Editável = `scene.json` + `build.py` (não há XML). `ASSETS` = mosaico de acervo (exclusivo do loop). |
| `03_SHARED_ASSETS/` | Assets usados pelas duas peças: `stickers` (pessoas), `logos`, `graphics`, `images`, `audio`/`sfx`, `fonts_reference`. |
| `04_MANIFEST/` | `assets.json` (um registro por asset), `timeline-notes.md` (cena → tempo → intenção), `provenance.md`. |

## Como ler `assets.json`
Cada item: `id`, `name`, `type`, `file` (caminho dentro do pacote), `source` (MB OFFICIAL / MOTION ARRAY / GENERATED / CREATED FOR EP300 / EXTERNAL REFERENCE / UNKNOWN),
`used_in` (cenas em que aparece — varredura estática, aproximada), `purpose`, `visual_meaning`, **`usage_context`** (o porquê, extraído da intenção da cena), `reusable`, `license_or_provenance`, `notes`.

## Linguagem visual da Abertura (resumo útil para reuso)
- **Paleta:** off‑white (#F7F3EA) · laranja MB (#F47340) · tinta (#121213). Fundo **pontilhado** (bolinhas 3 px a cada 20–26 px), creme nas cenas “de papel” e preto nas “de noite”.
- **Tipografia:** Sora 800 (números, títulos, adesivos) + Inter 700–800 tracking aberto (overlines em caixa alta).
- **Colagem/sticker:** tudo tem rotação do conjunto {{−8, 5, −4, 7, −6, 3}}°, contorno branco e **sombra sólida deslocada** (tipo adesivo colado); rostos = adesivos com estados (sorriso/surpresa/pensando).
- **Motion:** entradas “tapa do adesivo” (125%→100%), “pop”, “carimbo”; telas cheias encadeadas por **empurrão** (a seguinte desliza e empurra a anterior — sem câmera aparecendo); números contam; linhas do tempo desenham.
- **Ritmo/música:** câmera geral como base (fechadas só em reação); telas cheias quando a fala vira voz‑off; trilha baixa (−31 dB) sob o diálogo; SFX macios e sempre abaixo da voz (ducking −12 dB); 300 = confete + língua de sogra.
- **Regras de cinema:** sem linguagem de interface (clique/toque/play/cursor), safe area 90×54 px, tempo de leitura em telas sem voz, LAYLA com Y, “a volta do Lucian”.

## Loop (separado)
Composição: fundo pontilhado + mosaico de acervo (parallax lento) + “EPISÓDIO 300” + selo Analytics Talks + patrocinadores (Patrocínio oficial / Café oficial / Realização) + 3–4 microgags espaçados (Gustavo espia, pipoca, empurrão). Compartilha com a abertura: paleta, tipografia, patrocinadores, stickers Gustavo/Lucian, balde; é **exclusivo do loop**: o mosaico. Os últimos 1,5 s da abertura são os quadros finais do loop.

## Mais reutilizáveis
Stickers de pessoas (3–4 estados cada), logos de ferramentas em tile, gags originais, estrutura `plan.py` (cena = lista de elementos com tempo relativo), `sfx_v2.py` (SFX sintéticos), `qa_leak.py` / `qa_cues_v2.py --safe` / `qa_reading.py` (QAs determinísticos).

## Restrições / licença
- **Motion Array:** só 11 arquivos de áudio (música + SFX), licença da conta MB — ver `04_MANIFEST/provenance.md`. Não redistribuir fora da MB.
- **Logos de parceiros e de ferramentas:** marcas dos respectivos donos; patrocinadores ainda **provisórios**.
- **Emojis** (Segoe UI Emoji) não incluídos.

## Só referência (não editáveis)
Proxies MP4 (`MASTER_REFERENCE`), `caixa_pipoca_frente/verso` (versão superada), `overlays_ref/*.png`. Os 44 overlays ProRes (3,5 GB) **não foram duplicados**: estão em `00_ASSETS E INSERTS/V2_GERADOS/OVERLAYS` (ver `01_OPENING/ASSETS/OVERLAYS_LOCALIZACAO.txt`).

## Contexto do estado
Cor: o XML não leva o Lumetri do Gabriel (colar atributos no Premiere). Pendências abertas: master 1920x1080, logo MB Prime, naming dos patrocinadores, números falados × site (191/196, 140/146, 106/107 mil), SFX ainda não auditionados na sala.
''')

# resumo
def n(sub): return sum(len(fs) for _, _, fs in os.walk(_lp(os.path.join(OUT, sub))))
print('PACOTE:', OUT)
print('assets.json:', len(REG), 'registros', CATS)
for d in ('01_OPENING', '02_LOADING_LOOP', '03_SHARED_ASSETS', '04_MANIFEST'): print(d, n(d), 'arquivos')
unk = [a['id'] for a in REG if a['source'] == 'UNKNOWN']; print('UNKNOWN:', unk)
noctx = [a['id'] for a in REG if a['usage_context'].startswith('Não há evidência')]; print('sem contexto de uso:', len(noctx), noctx[:30])
