"""EP300 · Vídeo de abertura · V2 — FONTE DE VERDADE EDITORIAL (deriva da V1; V0 e V1 ficam intactas em ../v0 e ../v1).

Tempos em segundos na timeline da CAM_GERAL (fonte do áudio de diálogo = mesa de som).
Entradas desta rodada: 48 marcadores do Gabriel no Premiere (work/v1/human/feedback_markers.json),
nova regra de câmera (TP), correção de sincronia e pré-sessão nova.

Câmeras: W = CAM_GERAL (frontal — é para ela que eles olham), G / L = fechadas laterais (denunciam leitura
de TP: só em reação/brincadeira). WG / WL / Wz = reenquadramentos da CAM_GERAL (punch-in).
"""
import gfx
from gfx import CREAM, ORANGE, INK, INK2, WHITE

FPS = 30
# início de cada câmera 4K na timeline da CAM_GERAL (correlação de áudio câmera × mesa; drift ≤ 7 ms — sync_check.py)
OFFSETS = {'W': 0.0, 'G': 476.503, 'L': 476.320}
# SYNC (V1): a IMAGEM da CAM_GERAL chega 5 quadros depois do áudio da mesa gravado no mesmo arquivo
# (medido imagem×imagem contra as fechadas: 135–190 ms, começo/meio/fim). Correção: a imagem da geral
# é lida 5 quadros adiante do áudio. As fechadas já estavam certas.
W_VIDEO_LEAD_FRAMES = 5
# reenquadramentos da CAM_GERAL (escala, centro x, centro y em px do quadro 1920x1080)
CROPS = {'W': (1.0, 960, 540), 'Wz': (1.2, 880, 470), 'WG': (1.6, 1210, 430), 'WL': (1.6, 560, 400)}
# cor: aproximação do Lumetri do Gabriel por câmera (grade.py) — só no PROXY; no Premiere vale o Lumetri dele
GRADE = True

# ------------------------------------------------------------------ pré-sessão (antes da câmera real)
# cold open: arquivo de bastidor real (00_ASSETS E INSERTS/erros de gravação antigos) em PB
COLD_A = 9.30      # V2: erro + REAÇÃO + risada (b0 inteiro até o auge do riso; não corta na frase)
PRESHOTS = [
    # (tl_in, chave_da_mídia, in, out, tratamento)
    (0.00, 'B_2023_05_24', 0.00, COLD_A, 'pb'),      # "Fala aí… sejam bem-vindos." / "Começou mesmo?" / "Começa de novo…" + os dois rindo
    (COLD_A, 'B_VERDADES', 19.45, 21.92, 'pb'),      # "Tá no ar, tá valendo."
]
COLD_DUR = COLD_A + (21.92 - 19.45)                  # 11.77 s
LEADER_DUR = 2.9
AVISO_DUR = 31.0
EP300_DUR = 5.7
INTRO_DUR = COLD_DUR + LEADER_DUR + AVISO_DUR + EP300_DUR
INTRO_OVERLAP = 0.7      # a câmera já roda por baixo da íris
HOLD_GRITEM = 3.0        # respiro maior para a sala responder (marcador 2:48)
TITLE_DUR = 3.6
FINAL_DUR = 9.0      # V2: termina no quadro (t=120 s) do LOOP — ver customs_v2.final_v2
PUSH = 0.4           # V2: duração do empurrão entre telas cheias encostadas (sem câmera aparecendo entre elas)
PAUSE_EVOLUCAO = 2.4 # V2: respiro sem voz para ler a evolução do programa
OUTRO_DUR = TITLE_DUR + FINAL_DUR

# ------------------------------------------------------------------ montagem (diálogo)
SEGMENTS = [
    ('S1', 507.15, 543.20, [(507.15, 'WG'), (514.75, 'W'), (521.80, 'G'), (522.70, 'W')]),
    ('S1b', 544.80, 565.35, [(544.80, 'W')]),
    ('P_EVOL', 565.35, 565.35 + PAUSE_EVOLUCAO, 'pause'),   # V2: sem voz — a tela cheia da evolução do programa precisa de tempo de leitura
    ('S1c', 570.75, 593.55, [(570.75, 'W')]),
    ('S1d', 594.55, 598.30, [(594.55, 'W')]),
    ('S2a', 620.30, 640.46, [(620.30, 'W')]),
    ('S2a2', 641.78, 689.74, [(641.78, 'W'), (659.30, 'L'), (660.15, 'W'), (674.78, 'WG'), (676.60, 'WL'),
                              (678.00, 'W'), (688.55, 'WG')]),
    ('HOLD', 689.74, 689.74 + HOLD_GRITEM, 'freeze:WG:689.60'),
    ('S2b', 689.74, 712.88, [(689.74, 'L'), (690.45, 'W')]),
    ('S3a', 756.55, 783.75, [(756.55, 'W')]),
    ('S3b', 785.80, 796.18, [(785.80, 'W')]),
    ('S4', 855.17, 891.00, [(855.17, 'W'), (860.90, 'L'), (862.40, 'W')]),
    ('S5', 897.62, 951.90, [(897.62, 'W'), (901.00, 'L'), (904.34, 'W'), (943.40, 'WL'), (948.85, 'WG'), (950.75, 'W')]),
]
CUTS = [
    (543.20, 544.80, 'pausa longa do Lucian (marcador 0:44)'),
    (565.35, 570.75, 'Gustavo travou: "Aí, tipo, o que mudou, né?" (marcador 1:06)'),
    (593.55, 594.55, 'Lucian erra e se corrige: "sendo que, sen—" (marcador 1:33)'),
    (598.30, 620.30, 'retomada: 1ª versão do "de nada, Vitória" + ajuste de teleprompter'),
    (640.46, 641.78, '"Nesse ano de 2025" (o certo é 2026 — marcador 1:57); a tela mostra HOJE: 1 a cada 4'),
    (712.88, 756.55, 'retomada: bloco das empresas travou em "a Meta"'),
    (783.75, 785.80, 'gaguejo: "Fora casa, o recordista—"'),
    (796.18, 855.17, 'retomada pedida por eles + 3ª versão'),
    (891.00, 897.62, '"Chupa, Google" + "é só não colocar" (pedido explícito do Lucian)'),
    (951.90, 957.00, '"Esse é o tema do episódio? / Obrigado, gente" — não volta pra mesa depois do título (marcador 5:21)'),
]
BLEEPS = [(861.20, 862.47, 'palavrão (reação do Lucian) — bleep como gag; removível')]


# ------------------------------------------------------------------ helpers de cue (mesmos da V0)
def slap(at, text, size, x, y, color=INK2, emoji=None, rot=-3, **k):
    return dict(k='slap', at=at, text=text, size=size, x=x, y=y, color=color, emoji=emoji, rot=rot, **k)

def pop(at, kind, x, y, rot=0, anim='pop', **k):
    return dict(k=kind, at=at, x=x, y=y, rot=rot, anim=anim, **k)

def counter(at, to, size, x, y, color=INK2, fmt='{}', frm=0, **k):
    return dict(k='counter', at=at, to=to, **{'from': frm}, size=size, x=x, y=y, color=color, fmt=fmt, anim='none', **k)

def overline(at, text, x, y, color=ORANGE, size=30, rot=0, **k):
    return dict(k='text', at=at, text=text, size=size, font='inter', weight=800, tracking=200, color=color,
                x=x, y=y, rot=rot, anim='rise', **k)

def stk(at, path, x, y, size=300, rot=0, anim='pop', **k):
    return dict(k='stk', at=at, path=path, x=x, y=y, size=size, rot=rot, anim=anim, **k)

def face(at, who, x, y, size=260, rot=0, state='still', anim='pop', **k):
    return dict(k='stk', at=at, path=f'personagens/{who}/{state}.webp', x=x, y=y, size=size, rot=rot, anim=anim, **k)

def cue(id, name, st, dur, els, **k):
    return dict(id=id, name=name, st=st, dur=dur, els=els, **k)

FULL_CREAM = dict(bg=list(CREAM), full=True, trans=.3)
FULL_INK = dict(bg=list(INK), full=True, trans=.3)
PILL_W = dict(bg=WHITE, border=INK2, shadow=INK2, fg=INK2)
PILL_O = dict(bg=ORANGE, border=INK2, shadow=INK2)
ST = 'v1/stickers/'

# ------------------------------------------------------------------ cues
V = 'v2/'
ST2 = 'v2/stickers/'


# --- páginas do aviso (cada página empurra a anterior; leitura sem voz => tempo folgado)
A1, A2, A3, A4, A5 = 0.0, 7.7, 12.9, 18.1, 23.7          # início de cada página (s relativos ao cue)
AVISO = [
    overline(.1, 'ANTES DA SESSÃO COMEÇAR', 960, 95, size=32, out=AVISO_DUR - .5),
    dict(k='text', at=.3, text='um aviso do Analytics Talks', size=28, font='inter', weight=700, color=(120, 120, 120),
         x=960, y=145, anim='rise', out=AVISO_DUR - .5),
    # página 1 — saídas de emergência
    pop(.7, 'exit_sign', 400, 580, rot=-4, anim='slap', text='SAÍDA', arrow='←', out=A2, exit='toL'),
    pop(.85, 'exit_sign', 1520, 580, rot=4, anim='slap', text='SAÍDA', arrow='→', out=A2, exit='toL'),
    dict(k='text', at=1.1, text='As saídas de emergência', size=64, color=INK2, x=960, y=300, anim='rise', out=A2, exit='toL'),
    dict(k='text', at=1.3, text='ficam nas laterais.', size=64, color=INK2, x=960, y=385, anim='rise', out=A2, exit='toL'),
    slap(2.9, 'se você falar “eu acho”,', 70, 960, 760, color=INK2, rot=-2, out=A2, exit='toL'),
    slap(4.4, 'sugerimos que use-as.', 70, 1000, 900, color=ORANGE, emoji='🏃', rot=2, out=A2, exit='toL'),
    face(3.6, 'lucian', 260, 880, size=240, rot=-8, state='hover-final', out=A2, exit='toL'),
    # página 2 — levanta a mão
    pop(A2, 'emoji', 960, 330, ch='🙋', size=190, anim='burst', out=A3, exit='toL', states=[(0, '🙋'), (3.2, '😅')]),
    dict(k='text', at=A2 + .1, text='Levanta a mão quem já disse', size=60, color=INK2, x=960, y=520, anim='fromR', out=A3, exit='toL'),
    slap(A2 + 1.0, '“eu acho”', 130, 960, 690, color=ORANGE, rot=-3, out=A3, exit='toL'),
    dict(k='text', at=A2 + 2.0, text='numa reunião de resultado.', size=54, color=INK2, x=960, y=860, anim='rise', out=A3, exit='toL'),
    # página 3 — olha pro lado
    pop(A3, 'emoji', 960, 330, ch='👀', size=190, anim='burst', out=A4, exit='toL'),
    dict(k='text', at=A3 + .1, text='Agora olha pro lado.', size=72, color=INK2, x=960, y=520, anim='fromR', out=A4, exit='toL'),
    dict(k='text', at=A3 + 1.1, text='A pessoa também levantou.', size=56, color=INK2, x=960, y=650, anim='rise', out=A4, exit='toL'),
    slap(A3 + 2.1, 'você não está sozinho.', 66, 960, 820, color=ORANGE, emoji='🤝', rot=2, out=A4, exit='toL'),
    face(A3 + 2.4, 'gustavo', 300, 860, size=210, rot=-6, state='hover-final', out=A4, exit='toL'),
    # página 4 — celular
    pop(A4, 'emoji', 960, 330, ch='📱', size=190, anim='burst', out=A5, exit='toL'),
    dict(k='text', at=A4 + .1, text='Celular liberado.', size=72, color=INK2, x=960, y=520, anim='fromR', out=A5, exit='toL'),
    slap(A4 + 1.0, 'só vamos reclamar', 70, 960, 680, color=INK2, rot=-2, out=A5, exit='toL'),
    slap(A4 + 1.9, 'se você não marcar a gente.', 70, 960, 830, color=ORANGE, emoji='📸', rot=2, out=A5, exit='toL'),
    face(A4 + 2.3, 'gustavo', 1680, 820, size=250, rot=7, state='arraste-final', out=A5, exit='toL'),
    # página 5 — pipoca + a plateia sabe onde está
    pop(A5, 'asset', 1400, 560, rot=5, anim='fromR', path='v2/balde_pipoca_cheio.png', size=640, sway=3.0),
    dict(k='text', at=A5 + .1, text='Podem pegar a pipoca.', size=76, color=INK2, x=640, y=400, anim='fromR'),
    slap(A5 + 1.6, 'vocês vieram ao cinema', 66, 640, 570, color=INK2, rot=-2),
    slap(A5 + 2.8, 'assistir a um podcast.', 66, 660, 700, color=ORANGE, emoji='🍿', rot=2),
    face(A5 + 4.0, 'lucian', 300, 880, size=210, rot=-6, state='still', breath=3.1),
    face(A5 + 4.2, 'gustavo', 980, 890, size=210, rot=6, state='still', breath=2.7),
]

CUES = [
    # ================= PRÉ-SESSÃO =================
    cue('C00_00', 'COLD_OPEN_ARQUIVO', None, COLD_DUR, [
        dict(k='rec', at=0, label='ARQUIVO · 24/05/2023', tc0=9 * 3600 + 51 * 60 + 47, anim='none', out=COLD_A, exit='cut'),
        dict(k='rec', at=COLD_A, label='ARQUIVO · BASTIDOR', tc0=1234.0, anim='none'),
        dict(k='custom', fn='cold_grain'),
    ], tl=0.0,
       why='Cold open (removível): bastidor real de 2023 — "Fala aí… sejam bem-vindos." / "Começou mesmo?" / "Começa de novo…" e a RISADA dos dois '
           '(erro → percepção → reação → riso, sem cortar na frase) → "Tá no ar, tá valendo." Em PB, estética REC.'),
    cue('C00_01', 'CONTAGEM_PRE_SESSAO', None, LEADER_DUR, [dict(k='custom', fn='leader')], tl=COLD_DUR, bg=list(CREAM), full=True,
        sfx=[(0, 'beep'), (.95, 'beep'), (1.9, 'beep')],
        why='Payoff do cold open: "tá valendo" → a película conta 3-2-1 (agora sim, a sessão).'),
    cue('C00_03', 'AVISO_ANTES_DA_SESSAO', None, AVISO_DUR, AVISO, tl=COLD_DUR + LEADER_DUR, **FULL_CREAM,
        sfx=[(.7, 'thump'), (4.4, 'pop'), (A2, 'pop'), (A2 + 1.0, 'pop'), (A3, 'pop'), (A3 + 2.1, 'pop'), (A4, 'pop'),
             (A4 + 1.9, 'pop'), (A5, 'pop'), (A5 + 1.6, 'pop'), (A5 + 2.8, 'pop')],
        why='"Falso vídeo de instruções do cinema" — aviso NOSSO, falado PARA A SALA (ninguém clica): saídas p/ quem disser "eu acho" · '
            'levanta a mão · olha pro lado · celular só se marcar a gente · pipoca (balde corrigido) · "vocês vieram ao cinema assistir a um podcast". '
            'Cada página empurra a anterior; ~4,5 s de leitura por página.'),
    cue('C00_02', 'TELA_EPISODIO_300', None, EP300_DUR, [
        pop(.1, 'asset', 960, 470, rot=-3, anim='slap', path='v1/pipoca/selo_episodio_300.png', size=680),
        face(.9, 'lucian', 250, 560, size=280, rot=-7, state='still', breath=3.0),
        face(1.05, 'gustavo', 1670, 560, size=280, rot=7, state='still', breath=2.7),
        overline(1.0, 'PATROCÍNIO', 1585, 868, color=(160, 160, 160), size=20),
        pop(1.05, 'asset', 1400, 945, rot=-4, path='patrocinadores/purple-metrics.webp', size=150, sway=3.1),
        pop(1.10, 'asset', 1585, 950, rot=3, path='patrocinadores/onfly.webp', size=150, sway=2.8),
        pop(1.15, 'asset', 1755, 945, rot=-5, path='patrocinadores/coffee-plusplus.webp', size=140, sway=3.4),
        dict(k='confetti', at=.2, x=960, y=470, n=30, seed=7, anim='none'),
        pop(1.6, 'pill', 830, 850, text='a sessão vai começar', emoji='🍿', size=38, **PILL_O, out=4.55, exit='shrink'),
    ], tl=COLD_DUR + LEADER_DUR + AVISO_DUR, bg=list(INK), full=True, iris=dict(at=4.6, x=960, y=470, dur=.8),
        sfx=[(.1, 'pop'), (4.6, 'whoosh')],
        why='Selo real "EPISÓDIO 300" (arte do balde) com Gustavo e Lucian → a íris abre a partir do selo (V2: sem botão/cursor/"toca pra ver").'),

    # ================= 300 / dados × acho =================
    cue('C01_01', 'ADESIVO_300_CONFETE', 512.9, 1.8, [
        slap(0, '300', 230, 530, 360, emoji='🥳'),
        dict(k='confetti', at=.25, x=530, y=360, n=24, seed=3, anim='none'),
    ], sfx=[(0, 'party')], why='"episódio especial de número 300" — punch-in no Gustavo; adesivo 300 + confete + pontuação festiva (estouro, confete, língua de sogra).'),
    cue('C01_02', 'DADOS_11526_TELA_CHEIA', 522.70, 9.55, [
        slap(0, 'dados,', 150, 960, 250, color=ORANGE, emoji='🤓'),
        counter(1.8, 11526, 200, 960, 480, color=WHITE, cdur=1.0),
        overline(2.0, 'VEZES', 960, 610, color=WHITE, size=30),
        dict(k='custom', fn='acho_wall_v2'),
    ], **FULL_INK, acho_at=6.8, sfx=[(1.8, 'tickup1.0')],
        why='VO: "Pô, dados… 11.526 vezes. A segunda mais falada foi acho" — hierarquia DADOS → 11.526 → VEZES; os "acho" são textura nas laterais, sem tocar o topo.'),
    cue('C01_03', 'PLACAR_DADOS_X_ACHO', 532.25, 7.75, [dict(k='custom', fn='placar')], **FULL_CREAM,
        sfx=[(.3, 'tickup1.1'), (1.2, 'thump')], why='"494 vezes de diferença… existe pra aumentar essa distância" — placar (mantido, funcionou).'),

    # ================= de onde vem (linha do tempo) =================
    cue('C02_01', 'HISTORIA_LINHA_DO_TEMPO', 544.80, 11.6, [
        overline(0, 'DE ONDE VEM', 960, 110, size=30),
        dict(k='tl_axis', at=.2, x0=160, x1=1760, y=560, anim='none', draw=1.2,
             nodes=[(260, '2015', .5), (620, 'PRIME', 1.4), (980, 'MB TALKS', 3.0), (1340, 'A VOLTA', 7.0), (1700, 'PODCAST', 9.1)]),
        pop(.6, 'stamp', 260, 380, rot=-6, lines=['2015'], size=80, anim='stamp'),
        pop(1.5, 'stamp', 620, 390, rot=4, lines=['MB PRIME'], size=50, anim='stamp', fill=ORANGE),
        pop(3.1, 'label', 980, 380, rot=-3, lines=['“MB Talks”'], size=46),
        pop(4.5, 'label', 980, 700, rot=3, lines=['2 pessoas + 1 pergunta', 'por semana'], size=40),
        face(4.9, 'gustavo', 800, 860, size=190, rot=7, state='still'),
        dict(k='stk', at=5.1, path='personagens/lucian/still.webp', x=1160, y=860, size=190, rot=-8, anim='pop',
             states=[(1.9, 'personagens/lucian/arraste-final.webp')]),
        pop(7.1, 'pill', 1340, 390, rot=-3, text='a volta do Lucian', emoji='🎙️', size=30, **PILL_W),
        pop(9.2, 'asset', 1700, 350, rot=5, anim='slap', path='stickers/selo-analytics-talks.webp', size=200),
        pop(10.0, 'pill', 1640, 470, rot=-4, text='e não parou mais', size=30, **PILL_O),
        dict(k='polaroid', at=9.6, img='v2/hist/EP001_2021_DIGITAL_ANALYTICS_EM_2021.png', w=400, caption='EP 1 · 2021', cap=26,
             x=1590, y=790, rot=-4, anim='slap'),
    ], **FULL_CREAM, sfx=[(.6, 'thump'), (9.2, 'pop'), (9.6, 'pop')],
        why='VO do Lucian: 2015 → Prime → MB Talks → "quando eu voltei a gravar com o Gustavo" (A VOLTA DO LUCIAN — correção factual) → podcast; '
            'frame real do EP 1 (2021, contagem oficial) para mostrar quanto o programa mudou.'),
    cue('C02_02', 'CHUVA_DE_PERGUNTAS', 558.7, 3.3, [dict(k='custom', fn='question_rain')], sfx=[(0, 'whoosh')],
        avoid_faces=True, why='"São mais de 300 perguntas" — microgag sobre a câmera aberta (sem cobrir rostos).'),
    cue('C02_03', 'EVOLUCAO_DO_PROGRAMA', 562.6, 565.35 - 562.6 + PAUSE_EVOLUCAO, [dict(k='custom', fn='evolucao')], **FULL_CREAM,
        sfx=[(.45, 'pop'), (1.0, 'pop'), (1.55, 'pop'), (2.1, 'pop'), (2.65, 'pop'), (3.2, 'thump')],
        why='"E a pergunta foi mudando" — seis épocas do programa (2021→hoje) em frames reais do acervo histórico; ~2,4 s de pausa sem voz para a sala ler.'),

    # ================= o que mudou =================
    cue('C03_01', 'ECOSSISTEMA_DE_FERRAMENTAS', 570.75, 12.6, [
        overline(0, 'NO COMEÇO, QUASE TUDO ERA', 960, 110, color=WHITE, size=28),
        slap(.2, 'ferramenta', 110, 960, 230, color=ORANGE, emoji='🔧'),
        pop(1.2, 'logo', 190, 420, path='v2/logos/googleanalytics.png', size=190, rot=-6, sway=3.1),
        pop(1.4, 'logo', 410, 420, path='v2/logos/googletagmanager.png', size=190, rot=5, sway=2.7),
        pop(1.6, 'logo', 190, 640, path='v2/logos/googlebigquery.png', size=190, rot=4, sway=3.3),
        pop(1.8, 'logo', 410, 640, path='v2/logos/looker.png', size=190, rot=-5, sway=2.9),
        pop(2.0, 'logo', 190, 860, path='v2/logos/powerbi.png', size=190, rot=-4, sway=3.0),
        pop(2.2, 'logo', 410, 860, path='v2/logos/amplitude.png', size=190, rot=6, sway=2.6),
        pop(2.4, 'logo', 1510, 420, path='v2/logos/googleads.png', size=190, rot=5, sway=3.2),
        pop(2.6, 'logo', 1730, 420, path='v2/logos/meta.png', size=190, rot=-6, sway=2.8),
        pop(2.8, 'logo', 1510, 640, path='v2/logos/hotjar.png', size=190, rot=-4, sway=3.4),
        pop(3.0, 'logo', 1730, 640, path='v2/logos/googlesearchconsole.png', size=190, rot=6, sway=2.7),
        pop(3.2, 'logo', 1510, 860, path='v2/logos/google.png', size=190, rot=5, sway=3.0),
        pop(3.4, 'asset', 1730, 860, rot=-5, path='patrocinadores/reportei.webp', size=170, sway=2.9),
        pop(4.0, 'label', 960, 470, rot=-4, lines=['Como instalar?'], size=52),
        pop(5.0, 'label', 960, 590, rot=3, lines=['Como taguear?'], size=52),
        pop(6.5, 'label', 960, 760, rot=-2, lines=['Por que o número do relatório', 'não bate com o do financeiro?'], size=40),
        pop(11.0, 'stamp', 960, 920, rot=-8, lines=['ATÉ HOJE'], size=64, anim='stamp', fill=ORANGE),
    ], **FULL_INK, sfx=[(11.0, 'thump')],
        why='"No começo, quase tudo era ferramenta" — ecossistema de LOGOS reais (GA, GTM, BigQuery, Looker Studio, Power BI, Amplitude, Ads, Meta, Hotjar, '
            'Search Console, Google, Reportei) em adesivos-tile; V2 substitui os placeholders tipográficos.'),
    cue('C03_02', 'UNIVERSAL_ON_OFF', 583.35, 6.4, [
        overline(0, '2023', 960, 150, size=40),
        pop(.3, 'label', 960, 330, rot=-3, lines=['Universal Analytics'], size=60, exit='fall', out=4.9),
        pop(.5, 'switch', 960, 610, rot=2, off=2.4, w=420, h=190, exit='fall', out=5.0),
        pop(2.9, 'stamp', 1450, 560, rot=-8, lines=['DESLIGADO'], size=70, anim='stamp'),
        pop(3.4, 'pill', 960, 880, rot=-2, text='a gente teve que correr', emoji='🏃', size=36, **PILL_O),
    ], **FULL_CREAM, sfx=[(2.4, 'click'), (2.55, 'tvoff')],
        why='"o Google Analytics desligou o Universal" — chave ON/OFF em papel.'),
    cue('C03_03', 'CONTADOR_153_GRADE_4_DE_10', 589.75, 7.45, [
        counter(1.4, 153, 260, 960, 330, color=WHITE),
        overline(1.7, 'EPISÓDIOS EM 2023', 960, 490, color=WHITE, size=32),
        dict(k='grid', at=3.9, n=10, fill=4, cols=10, r=42, gap=26, x=960, y=680, fill_at=.3),
        pop(5.2, 'pill', 960, 860, text='4 em cada 10 = GA4', size=44, **PILL_O),
    ], **FULL_INK, sfx=[(1.4, 'tickup1.1'), (4.2, 'pop')], why='"153 episódios… 4 em cada 10 GA4" — contador + grade que se preenche.'),
    cue('C03_04', 'DE_NADA_VITORIA', 620.30, 3.1, [
        dict(k='stk_fx', at=0, path=ST2 + 'VITORIA/04_sorriso.png', x=960, y=470, size=470, rot=-4, anim='slap', breath=2.4,
             fx='hearts', fx_at=.9),
        pop(.3, 'emoji', 720, 300, ch='✨', size=110, anim='burst'),
        pop(.45, 'emoji', 1200, 330, ch='✨', size=90, anim='burst'),
        slap(.5, 'de nada, Vitória.', 90, 960, 860, emoji='🫡'),
    ], **FULL_CREAM, sfx=[(0, 'pop'), (.9, 'pop')],
        why='Piada interna gravada — a graça é VISUAL: corações nos olhos da Vitória (sem rótulo de "zoeira").'),
    cue('C03_05', 'GA4_1_DE_3', 623.40, 8.2, [
        pop(0, 'ga4', 640, 430, rot=-6, size=300, anim='slap', sway=3.0),
        slap(.3, 'GA4', 150, 1180, 330, color=ORANGE),
        overline(.8, 'NUNCA SAIU DA PAUTA', 1180, 480, color=WHITE, size=28),
        dict(k='grid', at=2.4, n=3, fill=1, r=56, gap=34, x=1180, y=620),
        overline(2.8, '1 A CADA 3 EPISÓDIOS', 1180, 730, color=WHITE, size=30),
        pop(6.0, 'label', 960, 920, rot=3, lines=['+ o que entrou do lado dele…'], size=44),
    ], **FULL_INK, sfx=[(2.4, 'pop')], why='"o GA4 nunca saiu da pauta… um a cada três" — logo GA4 em adesivo, tela cheia.'),
    cue('C03_06', 'GOSTA_POUCO_IA', 633.4, 3.8, [
        pop(0, 'pill', 900, 130, rot=4, text='“gosto pouco”', emoji='🙃', size=34, **PILL_W),
        face(1.9, 'lucian', 880, 330, size=210, rot=-6, state='hover-final', anim='slap'),
        slap(2.2, 'inteligência artificial', 54, 880, 660, color=ORANGE, emoji='🤖', rot=-2),
    ], why='Ironia real ("gosto pouco… inteligência artificial") — entra no "inteligência"; adesivo do Lucian entre os dois, sem cobrir rosto.'),
    cue('C03_07', 'IA_LINHA_DO_TEMPO', 637.10, 14.33, [
        overline(0, 'O QUE ENTROU DO LADO DO GA4', 960, 110, size=28),
        dict(k='tl_axis', at=.1, x0=200, x1=1720, y=470, anim='none', draw=1.0,
             nodes=[(360, 'ATÉ 2021', .5), (1000, 'HOJE', 3.9), (1560, '', 10.8)]),
        pop(.9, 'label', 360, 310, rot=-3, lines=['IA: fora da pauta'], size=40),
        face(1.4, 'lucian', 360, 700, size=190, rot=-7, state='arraste-final'),
        dict(k='grid', at=4.1, n=4, fill=1, r=40, gap=24, x=1000, y=300),
        overline(4.4, 'IA: 1 A CADA 4 EPISÓDIOS', 1000, 380, size=26),
        pop(7.7, 'pill', 900, 680, rot=-2, text='atribuição', size=38, **PILL_W),
        pop(8.1, 'pill', 1080, 780, rot=3, text='incrementalidade', size=38, **PILL_W),
        pop(11.2, 'label', 1560, 320, rot=-3, lines=['BigQuery:', 'assunto de engenheiro'], size=36),
        dict(k='strike', at=12.0, w=330, x=1580, y=345, rot=-3, width=12),
        pop(12.6, 'stamp', 1520, 560, rot=-8, lines=['MARKETING'], size=56, anim='stamp', fill=ORANGE),
    ], **FULL_CREAM, sfx=[(4.1, 'pop'), (12.6, 'thump')],
        why='IA 2021 → hoje, atribuição/incrementalidade, BigQuery → marketing em LINHA DO TEMPO. "Nesse ano de 2025" cortado do áudio; a tela diz HOJE.'),
    cue('C03_08', 'BOTAO_VIRA_MODELO', 652.60, 7.4, [
        overline(0, 'A PERGUNTA MUDOU', 960, 150, color=WHITE, size=30),
        pop(.1, 'pill', 960, 480, rot=-2, text='como taguear um botão?', size=64, **PILL_O, out=3.9, exit='shrink'),
        pop(4.1, 'pill', 960, 480, rot=3, text='dá pra confiar no modelo?', emoji='🤖', size=64, anim='slap', **PILL_W),
        slap(5.9, 'modelo.', 110, 1300, 760, color=ORANGE, rot=6),
    ], **FULL_INK, sfx=[(3.9, 'pop'), (4.1, 'pop')], why='"taguear um botão → confiar no modelo" — tela cheia (V2: sem cursor).'),
]

CUES += [
    # ================= o que não mudou =================
    cue('C04_01', 'BORDAO_203_PRINTS', 669.30, 5.45, [dict(k='custom', fn='bordao_prints')], **FULL_CREAM,
        sfx=[(.1, 'whoosh'), (.3, 'tickup2.6')], why='"203 vezes… fala aí, analítica" — prints reais de episódios em pilha, contador correndo.'),
    cue('C04_02', 'EPISODIO_DE_ORIGEM', 675.10, 3.6, [
        pop(0, 'label', 960, 950, rot=-2, lines=['episódio de origem: ???'], size=48),
        pop(1.7, 'emoji', 1330, 930, ch='🤷', size=120, anim='burst'),
    ], sfx=[(-.3, 'whoosh'), (1.5, 'whoosh')],
        why='"qual foi o episódio que nasceu? — Não, nem eu." — tarja embaixo + punch-in nos rostos (jogada de câmera).'),
    cue('C04_03', 'APELIDOS_16', 679.90, 6.7, [
        counter(0, 16, 210, 960, 190, color=WHITE),
        overline(.3, 'JEITOS DE APRESENTAR O LUCIAN', 960, 310, color=WHITE, size=24),
        stk(.6, 'personagens/gustavo/hover-final.webp', 340, 720, size=300, rot=6, breath=2.4),
        dict(k='balloon', at=1.0, text='O diamante negro do Analytics!', size=40, x=560, y=470, tail='left', anim='pop', rot=-3),
        face(.9, 'lucian', 1580, 720, size=300, rot=-6, state='arraste-final', breath=2.9),
        pop(1.6, 'label', 980, 600, rot=-4, lines=['“Super choque do analítico”'], sub='EP 205', size=32),
        pop(1.9, 'label', 1000, 720, rot=3, lines=['“CTO and Black Diamond”'], sub='EP 256', size=32),
        pop(2.2, 'label', 960, 840, rot=-2, lines=['“O cara pra quem o GTM pede bênção”'], sub='EP 270', size=30),
        pop(2.5, 'label', 1000, 960, rot=4, lines=['“Cebola: bota as tags pra chorar”'], sub='EP 69', size=30),
    ], **FULL_INK, sfx=[(0, 'tickup1.0')], why='"16 maneiras de me apresentar" — Gustavo-adesivo com balão × Lucian "bolado".'),
    cue('C04_04', 'DIAMANTE_NEGRO_OFICIAL', 686.60, 2.6, [
        pop(0, 'diamond', 420, 300, rot=-8, r=110, seed=1, color=(34, 34, 38)),
        pop(.08, 'diamond', 1500, 250, rot=10, r=90, seed=2, color=(60, 40, 90)),
        pop(.16, 'diamond', 1620, 800, rot=-5, r=120, seed=3, color=(30, 30, 34)),
        pop(0, 'choco', 960, 470, rot=-4, w=760, h=320, anim='slap', l1='DIAMANTE', l2='NEGRO', l3='do Analytics'),
        pop(.5, 'stamp', 960, 820, rot=-8, lines=['É OFICIAL'], size=90, anim='stamp', fill=ORANGE),
        face(.7, 'lucian', 300, 800, size=240, rot=-7, state='hover-final'),
    ], **FULL_CREAM, sfx=[(.5, 'thump')],
        why='"diamante negro é oficial" — diamantes + barra de chocolate GENÉRICA (sem marca de terceiros).'),
    cue('C04_05', 'GRITEM_SE_CONCORDAM', 689.60, 0.14 + HOLD_GRITEM, [
        dict(k='custom', fn='dim'),
        dict(k='marquee', at=.25, lines=['GRITEM', 'SE CONCORDAM!'], size=74, x=1400, y=430, rot=4, anim='slap', out=HOLD_GRITEM - .2),
        stk(.45, 'personagens/gustavo/hover-final.webp', 1700, 860, size=260, rot=8, anim='slap', out=HOLD_GRITEM - .2,
            states=[(1.0, 'personagens/gustavo/hover-transicao.webp'), (1.3, 'personagens/gustavo/hover-final.webp'),
                    (2.0, 'personagens/gustavo/hover-transicao.webp'), (2.25, 'personagens/gustavo/hover-final.webp')]),
        pop(.6, 'emoji', 1180, 200, ch='📣', size=120, anim='burst', out=HOLD_GRITEM - .2, states=[(0, '📣'), (1.6, '🙌')]),
        pop(1.1, 'emoji', 1760, 200, ch='🗣️', size=100, anim='burst', out=HOLD_GRITEM - .2),
    ], hold=(0.14, HOLD_GRITEM), dim_at=.2, dim_alpha=90, sfx=[(0, 'woosh_boom')],
        why='4ª parede real: congela, placa de cinema + Gustavo-adesivo "gritando"; respiro de 3 s pra sala responder.'),
    cue('C04_06', 'PICA_PAU_24_TELA_CHEIA', 690.45, 10.45, [
        overline(0, 'FRASE CLÁSSICA DO LUCIAN', 960, 120, size=28),
        pop(.35, 'stamp', 350, 400, rot=7, lines=['24×'], size=130, anim='stamp'),
        pop(1.9, 'label', 960, 570, rot=-2, lines=['“Se o Pica-Pau tivesse', 'chamado a polícia, nada', 'disso teria acontecido.”'], size=48),
        pop(1.2, 'asset', 1600, 420, rot=4, path='v2/gag_picapau_silhueta.png', size=330, sway=2.5, anim='slap'),
        dict(k='balloon', at=3.0, text='Alô, polícia?', size=36, x=1360, y=215, tail='right', anim='pop', rot=-3),
        pop(4.4, 'asset', 1490, 800, rot=-3, path='v2/viatura.png', size=330, anim='fromR', sway=1.6),
        face(5.6, 'lucian', 380, 800, size=240, rot=-7, state='arraste-final'),
        face(5.9, 'gustavo', 700, 830, size=220, rot=6, state='hover-final'),
        pop(6.6, 'pill', 1000, 960, rot=3, text='tem gente que nem sabe a referência', emoji='🤷', size=32, **PILL_W),
    ], **FULL_CREAM, sfx=[(.35, 'thump'), (4.4, 'whoosh')],
        why='"24 vezes… Pica-Pau" — frase + 24× + pássaro (silhueta ORIGINAL, sem o personagem de terceiros) ligando pra polícia + viatura entrando + os dois olhando.'),
    cue('C05_01', 'MESA_191_348_140_MURAL', 701.10, 11.7, [dict(k='custom', fn='mural_v2')], **FULL_INK, n2=6.6, n3=9.3,
        sfx=[(0, 'tickup0.95'), (6.6, 'tickup0.95'), (9.3, 'tickup0.95')],
        why='"191 pessoas… 348 vezes… mais de 140 empresas" — número no centro + 4 convidados históricos em adesivo (Phill, Mafê, Bonel, Layla) e 2 frames reais; reações trocam a cada número.'),

    # ================= quem respondeu =================
    cue('C05_02', 'SETORES_E_GOOGLE', 756.55, 6.45, [
        overline(0, 'EMPRESAS QUE PASSARAM AQUI', 960, 110, size=28),
        pop(.4, 'pill', 420, 300, rot=-3, text='banco', emoji='🏦', size=44, **PILL_W),
        pop(.9, 'pill', 760, 330, rot=3, text='varejo', emoji='🛒', size=44, **PILL_W),
        pop(1.4, 'pill', 1120, 300, rot=2, text='mídia', emoji='📺', size=44, **PILL_W),
        pop(1.9, 'pill', 1480, 330, rot=-4, text='telecom', emoji='📡', size=44, **PILL_W),
        pop(2.5, 'logo', 960, 530, path='v2/logos/google.png', size=260, rot=-3, anim='slap'),
        pop(3.6, 'stamp', 960, 760, rot=-6, lines=['PARCEIRO DO GOOGLE?'], size=60, anim='stamp'),
        pop(4.7, 'stamp', 1000, 900, rot=5, lines=['AINDA NÃO'], size=80, anim='stamp', fill=ORANGE),
    ], **FULL_CREAM, sfx=[(4.7, 'wrong')],
        why='"banco, varejo, mídia, telecom e até o Google… não é parceiro do Google?" — logo G em adesivo.'),
    cue('C05_03', 'EU_QUERIA_CHORANDO', 763.00, 1.9, [
        face(0, 'lucian', 600, 520, size=460, rot=-6, state='hover-final', anim='slap'),
        dict(k='tears', at=.1, x=600, y=560, spread=150, seed=1, anim='none'),
        face(.5, 'gustavo', 1320, 520, size=460, rot=6, state='hover-final', anim='slap'),
        dict(k='tears', at=.6, x=1320, y=560, spread=150, seed=2, anim='none'),
        pop(.3, 'emoji', 960, 250, ch='😭', size=150, anim='burst'),
    ], **dict(FULL_INK, trans=.2), why='"Eu queria. / Também queria." — os dois adesivos grandes "chorando" (lágrimas desenhadas, sem mexer no rosto).'),
    cue('C05_04', 'PICA_PAU_PM_RJ_EP126', 764.90, 6.6, [
        pop(0, 'label', 560, 220, rot=3, lines=['“Se o Pica-Pau tivesse', 'chamado a polícia…”'], size=40),
        pop(1.9, 'stamp', 560, 420, rot=-6, lines=['NÓS CHAMAMOS'], size=64, anim='stamp', fill=ORANGE),
        dict(k='polaroid', at=3.4, img='v1/ep126/f_guest.png', w=560, caption='EP 126 · Inovação e Dados na PMERJ', cap=24,
             x=1360, y=380, rot=4, anim='slap'),
        dict(k='polaroid', at=4.1, img='v1/ep126/f_duo.png', w=480, x=700, y=780, rot=-5, anim='slap'),
        pop(4.5, 'asset', 1500, 800, rot=-3, path='v2/viatura.png', size=320, anim='fromR', sway=1.6),
    ], **FULL_CREAM, sfx=[(1.9, 'thump'), (3.4, 'whoosh'), (4.5, 'whoosh')],
        why='"nós chamamos. Gravamos até com a PM do RJ" — trecho REAL do EP 126 + a viatura (sticker do Gabriel) chegando.'),
    cue('C05_05', 'FICHA_DE_PRESENCA_FOTOS', 773.30, 20.8, [dict(k='custom', fn='ficha_v2')], **FULL_INK,
        rows=(2.0, 5.8, 11.6), extras=(8.0, 15.0),
        why='"Teve gente que gabaritou a ficha de presença" — Phill 29, Mafê 24 (convidada do EP 1: frame real), Bonel 7 + adesivos.'),

    # ================= a gente chegou antes =================
    cue('C06_01', 'ACERTA_ANTES', 859.75, 1.1, [slap(0, 'acerta antes.', 80, 1300, 130, emoji='🎯')],
        why='"de vez em quando você acerta antes" — sobre a câmera ABERTA, no topo entre os dois.'),
    cue('C06_02', 'BLEEP', 861.15, 1.25, [
        dict(k='bleep', at=0, x=700, y=900, w=560, h=140, anim='slap', out=1.0),
        pop(.1, 'emoji', 380, 880, ch='🙊', size=130, anim='burst', out=1.0),
    ], why='Palavrão real da reação — bleep como gag, embaixo (não cobre o rosto do Lucian).'),
    cue('C06_03', 'DATAS_FEV22_OUT24', 862.40, 14.85, [
        overline(0, 'A GENTE CHEGOU ANTES', 960, 90, size=28),
        dict(k='tl_axis', at=0, x0=140, x1=1780, y=520, anim='none', draw=1.0,
             nodes=[(380, 'FEV 2022', .2), (1240, 'OUT 2024', 10.9)]),
        pop(.5, 'label', 380, 330, rot=2, lines=['“o GA4 era esse', 'todinho todo?”'], size=38),
        pop(4.3, 'asset', 760, 780, rot=-5, anim='drop', path='v2/gag_toddynho_ga4.png', size=300, sway=3.0),
        dict(k='stk_fx', at=4.9, path=ST2 + 'VITORIA/02_reacao.png', x=220, y=800, size=230, rot=-6, out=8.6, anim='slap'),
        pop(5.1, 'pill', 450, 900, rot=-4, text='desculpa, Vi.', emoji='🙏', size=30, **PILL_W, out=8.6),
        pop(6.7, 'stamp', 1000, 700, rot=6, lines=['+27 DIAS', 'GOOGLE: FIM DO UA'], size=48, anim='stamp', fill=ORANGE),
        pop(11.2, 'label', 1240, 330, rot=-3, lines=['episódio inteiro', 'sobre MMM'], size=38),
    ], **FULL_CREAM, sfx=[(4.3, 'pop'), (6.7, 'thump')],
        why='Módulo "nossa pergunta → resposta do mercado" em LINHA DO TEMPO + gag do Toddynho (carton original com selo GA4) no "todinho todo" + desculpa, Vi.'),
    cue('C06_04', 'DE_NADA_PURPLE', 877.25, 3.4, [
        pop(.1, 'asset', 960, 130, rot=-3, path='patrocinadores/purple-metrics.webp', size=260, anim='slap'),
        pop(.5, 'pill', 1250, 190, rot=5, text='de nada', emoji='👋', size=30, **PILL_W),
        dict(k='stk', at=1.1, path=ST2 + 'GUTA/01_natural.png', x=260, y=790, size=290, rot=-6, anim='pop',
             states=[(1.2, ST2 + 'GUTA/02_reacao.png')]),
        pop(1.3, 'pill', 260, 960, rot=-3, text='Guta', size=28, **PILL_W),
        dict(k='stk', at=1.3, path=ST2 + 'LUCAS/01_natural.png', x=1660, y=780, size=290, rot=6, anim='pop',
             states=[(1.4, ST2 + 'LUCAS/03_lateral.png')]),
        pop(1.5, 'pill', 1660, 960, rot=3, text='Lucas', size=28, **PILL_W),
    ], why='"Olha aí, de nada, viu, Purple…" — câmera PRINCIPAL pra brincadeira; V2: stickers reais de Guta Tolmasquim e Lucas Yokota (Purple Metrics).'),
    cue('C06_05', 'DATAS_MERIDIAN_MCP_DEZ24', 880.65, 13.73, [
        overline(0, 'A GENTE CHEGOU ANTES', 960, 90, size=28),
        dict(k='tl_axis', at=0, x0=140, x1=1780, y=520, anim='none', draw=.01,
             nodes=[(380, 'OUT 2024', 0), (900, 'ABR 2025', 4.8), (1460, 'DEZ 2024', 10.4)]),
        pop(.4, 'stamp', 420, 340, rot=-6, lines=['+3 MESES', 'GOOGLE: MERIDIAN'], size=44, anim='stamp', fill=ORANGE),
        dict(k='stk', at=2.5, path=ST2 + 'LAYLA/01_sorriso.png', x=360, y=800, size=250, rot=6, anim='slap',
             states=[(3.3, ST2 + 'LAYLA/02_surpresa.png')]),
        pop(2.7, 'pill', 620, 900, rot=-4, text='viu, Layla?', emoji='👀', size=32, **PILL_W),
        pop(5.2, 'label', 900, 330, rot=2, lines=['1º MCP do mundo', 'pro Google Analytics'], size=36),
        pop(5.6, 'emoji', 1130, 250, ch='🌍', size=90, anim='burst'),
        pop(8.6, 'stamp', 1000, 740, rot=6, lines=['JUL 2025', 'O DO GOOGLE'], size=44, anim='stamp', fill=ORANGE),
        pop(10.6, 'label', 1460, 330, rot=-2, lines=['“vai dar pra conversar', 'com os dados”'], size=34),
    ], **FULL_CREAM, sfx=[(.4, 'thump'), (8.6, 'thump')],
        why='+3 meses Meridian, "viu, Layla?" (LAYLA com Y; sticker novo), MCP abr/25 → jul/25, dez/24.'),
    cue('C06_06', 'MEIA_CULPA', 901.20, 3.0, [
        pop(0, 'pill', 700, 930, rot=-3, text='meia-culpa', emoji='🙋', size=36, **PILL_W),
    ], why='Lucian na câmera só pra brincadeira "vou assumir minha meia-culpa" — tarja embaixo.'),
    cue('C06_07', 'DATAS_FEV26_JUN26_ACERTOU', 904.34, 8.0, [
        overline(0, 'E AÍ…', 960, 90, size=28),
        pop(.2, 'stamp', 520, 330, rot=-6, lines=['FEV 2026', 'IA NA HOME DO GA'], size=50, anim='stamp', fill=ORANGE),
        pop(3.3, 'stamp', 520, 620, rot=5, lines=['JUN 2026', 'A GENTE LANÇOU A', 'ANÁLISE COMPARATIVA'], size=40, anim='stamp'),
        face(5.3, 'lucian', 1400, 420, size=300, rot=-7, state='arraste-final'),
        pop(6.2, 'pill', 1400, 640, rot=4, text='“impossível”', size=36, **PILL_W),
        pop(6.6, 'stamp', 1300, 860, rot=-8, lines=['ACERTOU'], size=80, anim='stamp', fill=ORANGE),
    ], **FULL_CREAM, sfx=[(.2, 'thump'), (6.6, 'thump')],
        why='"GA colocou IA na home em fev/26… a gente lançou a análise comparativa em junho… Lucian falou que era impossível".'),

    # ================= vocês =================
    cue('C07_01', 'VOCES_PLATEIA', 914.70, 1.3, [
        slap(0, 'vocês.', 140, 1330, 130, color=ORANGE, emoji='🫵'),
    ], sfx=[(0, 'pop')], why='"do outro lado da pergunta: vocês" — 4ª parede na câmera frontal (V2: setas removidas; o emoji já aponta).'),
    cue('C07_02', 'OUVIDAS_700_MIL', 915.85, 6.25, [
        counter(.2, 700, 240, 960, 210, color=WHITE, fmt='{} mil', cdur=.9),
        overline(1.2, 'VEZES ALGUÉM APERTOU O PLAY', 960, 350, color=WHITE, size=26),
        counter(3.6, 106, 150, 900, 720, color=ORANGE, fmt='{} mil h', cdur=.8),
        dict(k='clock', at=3.7, x=1330, y=720, r=62, anim='pop'),
        overline(4.0, 'OUVIDAS', 900, 830, color=WHITE, size=24),
        pop(4.2, 'emoji', 1600, 720, ch='🎧', size=110, anim='burst'),
    ], **FULL_INK, sfx=[(.2, 'tickup0.9'), (3.6, 'tickup0.8')], why='"700 mil vezes… 106 mil horas" — tela cheia; V2: sem botão de play/cursor.'),
    cue('C07_03', 'DE_VOLTA_PARA_2038', 922.10, 6.75, [
        dict(k='sofa', at=.1, x=560, y=420, size=700, rot=2, anim='pop'),
        overline(.4, 'SE NINGUÉM APERTAR O PAUSE…', 1360, 200, size=26),
        counter(2.9, 2038, 170, 1360, 420, color=INK2, frm=2026, cdur=2.6, raw=True),
        slap(3.4, 'de volta para o futuro', 58, 1360, 620, color=ORANGE, emoji='⚡', rot=-3),
        pop(4.2, 'emoji', 1600, 780, ch='🚗', size=120, anim='burst'),
        dict(k='clock', at=2.9, x=1010, y=440, r=50, anim='pop', fast=.3),
    ], **FULL_CREAM, sfx=[(2.9, 'tick'), (2.9, 'rise2.6')],
        why='"terminaria em 2038" — cena do sofá + ano correndo + homenagem tipográfica (sem imagens de terceiros).'),
    cue('C07_04', 'PAISES_110_BANDEIRAS', 928.85, 1.6, [dict(k='custom', fn='flags_v2')], **dict(FULL_INK, trans=.2),
        sfx=[(0, 'pop')], why='"Em 110 países" — bandeiras QUADRADAS no formato do site (borda de tinta + sombra sólida), tela cheia.'),
    cue('C07_05', 'EP_197', 933.70, 3.95, [
        pop(0, 'stamp', 960, 230, rot=-5, lines=['EP 197'], size=110, anim='stamp'),
        pop(.5, 'label', 960, 470, rot=3, lines=['Transição de carreira', 'para dados'], size=56),
        pop(.9, 'emoji', 1360, 200, ch='🏆', size=130, anim='burst'),
        overline(1.2, 'O MAIS OUVIDO', 960, 660, size=30),
    ], **FULL_CREAM, sfx=[(0, 'thump')], why='"o episódio mais ouvido é o 197, Transição de Carreira para Dados".'),
    cue('C07_06', 'GENTE', 941.7, 1.7, [slap(0, 'gente.', 150, 960, 920, color=ORANGE, emoji='🧡')],
        sfx=[(0, 'ding')], why='Payoff: "…era sobre gente." — no meio, embaixo.'),

    # ================= final =================
    cue('C08_01', 'TITULO_EPISODIO', None, TITLE_DUR, [dict(k='custom', fn='titulo')], tl='END', bg=list(INK), full=True,
        why='Título do episódio (aprovado) — entra depois de um respiro, sem voltar pra mesa.'),
    cue('C09_01', 'FINAL_300_E_LOOPING', None, FINAL_DUR, [dict(k='custom', fn='final_v2')], tl='END+TITLE', bg=list(INK), full=True,
        sfx=[(.2, 'tickup1.1'), (1.3, 'party')],
        why='300 conta → estoura (confete + língua de sogra) → vocês estão aqui → Gustavo e Lucian comemoram → o 300 vira o lockup do LOOP: mosaico, logo e '
            'patrocinadores entram, e os últimos 1,5 s são os quadros 118,5–120 s do próprio loop (o loop começa no quadro 0 sem corte).'),
]
