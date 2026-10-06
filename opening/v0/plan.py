"""EP300 · Vídeo de abertura · V0 — FONTE DE VERDADE EDITORIAL.

Tempos em segundos na timeline da CAM_GERAL (fonte do áudio de diálogo). As câmeras 4K
são sincronizadas por correlação de áudio (OFFSETS). Tudo o que é gerado (preview, XML
do Premiere, overlays) sai deste arquivo — editar aqui e rodar build.py de novo.

Câmeras: W = CAM_GERAL (aberta), G = MVI_9943-CAM_GUSTAVO, L = MVI_9943-CAM_LUCIAN.
"""
import gfx
from gfx import CREAM, ORANGE, INK, INK2, WHITE

FPS = 30
# início de cada câmera 4K na timeline da CAM_GERAL (correlação de áudio, precisão ~10 ms)
OFFSETS = {'W': 0.0, 'G': 476.503, 'L': 476.320}

INTRO_DUR = 8.6          # abertura gráfica (contagem + tela "EPISÓDIO 300")
INTRO_OVERLAP = 0.7      # a câmera já roda por baixo da íris
HOLD_GRITEM = 1.6        # respiro inserido para a plateia responder "Gritem, se concordam"
OUTRO_DUR = 7.0

# ------------------------------------------------------------------ montagem (diálogo)
# (id, src_in, src_out, [(src_t, câmera), ...])
SEGMENTS = [
    ('S1', 507.15, 598.30, [(507.15, 'G'), (514.75, 'W'), (518.40, 'L'), (521.80, 'G'), (522.75, 'L'),
                            (530.05, 'G'), (540.00, 'W'), (544.00, 'L'), (556.30, 'G'), (566.30, 'W'),
                            (570.30, 'G'), (583.20, 'L')]),
    ('S2a', 620.30, 689.74, [(620.30, 'G'), (631.55, 'W'), (636.00, 'L'),
                             (652.70, 'G'), (659.30, 'L'), (660.10, 'W'), (669.20, 'G'), (674.70, 'W'),
                             (679.90, 'L'), (684.55, 'G')]),
    ('HOLD', 689.74, 689.74 + HOLD_GRITEM, 'freeze:G:689.60'),
    ('S2b', 689.74, 712.88, [(689.74, 'L'), (690.45, 'G'), (696.50, 'W'), (700.90, 'G')]),
    ('S3a', 756.55, 783.75, [(756.55, 'L'), (773.30, 'G')]),
    ('S3b', 785.80, 796.18, [(785.80, 'L')]),
    ('S4', 855.17, 891.00, [(855.17, 'G'), (861.10, 'L'), (881.10, 'G')]),
    ('S5', 897.62, 956.30, [(897.62, 'L'), (904.35, 'G'), (911.70, 'W'), (913.00, 'G'), (922.05, 'L'),
                            (928.85, 'G'), (930.40, 'L'), (937.65, 'G'), (941.30, 'W'), (943.35, 'L'),
                            (948.80, 'G'), (950.70, 'W')]),
]
# trechos cortados (registro editorial — ver EDIT_PLAN.md):
CUTS = [
    (598.30, 620.30, 'retomada: 1ª versão do "de nada, Vitória" + ajuste de teleprompter; usa a 2ª versão'),
    (712.88, 756.55, 'retomada: bloco das empresas travou em "a Meta"; usa a 2ª versão a partir de "Banco, varejo"'),
    (783.75, 785.80, 'gaguejo: 1ª tentativa "Fora casa, o recordista—" (repetida em seguida)'),
    (796.18, 855.17, 'retomada: "volta ali, a entonação ficou errada" + 3ª versão (o próprio time pediu corte)'),
    (891.00, 897.62, '"Chupa, Google" + "é só não colocar, eu só queria falar aqui" (pedido explícito do Lucian)'),
]
BLEEPS = [(861.20, 862.47, 'palavrão (reação do Lucian) — bleep como gag; remover o trecho se preferir')]


# ------------------------------------------------------------------ helpers de cue
def slap(at, text, size, x, y, color=INK2, emoji=None, rot=-3, **k):
    return dict(k='slap', at=at, text=text, size=size, x=x, y=y, color=color, emoji=emoji, rot=rot, **k)

def pop(at, kind, x, y, rot=0, anim='pop', **k):
    return dict(k=kind, at=at, x=x, y=y, rot=rot, anim=anim, **k)

def counter(at, to, size, x, y, color=INK2, fmt='{}', frm=0, **k):
    return dict(k='counter', at=at, to=to, **{'from': frm}, size=size, x=x, y=y, color=color, fmt=fmt, anim='none', **k)

def overline(at, text, x, y, color=ORANGE, size=30, rot=0, **k):
    return dict(k='text', at=at, text=text, size=size, font='inter', weight=800, tracking=200, color=color,
                x=x, y=y, rot=rot, anim='rise', **k)

def cue(id, name, st, dur, els, **k):
    return dict(id=id, name=name, st=st, dur=dur, els=els, **k)


FACES_INTRO = [
    dict(k='face', who='lucian', size=300, at=.2, x=1590, y=235, rot=-8, anim='pop', breath=3.2),
    dict(k='face', who='gustavo', size=300, at=.35, x=330, y=850, rot=6, anim='pop', breath=2.7),
]

# ------------------------------------------------------------------ cues de motion
# st = instante de ENTRADA na timeline da CAM_GERAL (ou 'tl' absoluto), 'at' dos elementos = segundos
# relativos ao início do cue. Cada cue vira um overlay .mov com alpha (1920x1080, ProRes 4444).
CUES = [
    # ---------------- ABERTURA (pré-sessão) ----------------
    cue('C00_01', 'CONTAGEM_PRE_SESSAO', None, 2.9, [dict(k='custom', fn='leader')], tl=0.0, bg=list(CREAM), full=True,
        why='Pré-sessão de cinema: contagem de película traduzida para a gramática EP300 (creme, pontinhos, laranja).'),
    cue('C00_02', 'TELA_EPISODIO_300', None, INTRO_DUR - 2.9, [
        overline(.15, 'EPISÓDIO', 960, 330, size=34),
        counter(.25, 300, 300, 930, 520, color=(245, 245, 245)),
        pop(.9, 'asset', 1330, 560, rot=6, path='stickers/selo-analytics-talks.webp', size=210),
        *FACES_INTRO,
        overline(1.0, 'PATROCÍNIO', 1640, 868, color=(160, 160, 160), size=20),
        pop(1.05, 'asset', 1455, 945, rot=-4, path='patrocinadores/purple-metrics.webp', size=150, sway=3.1),
        pop(1.10, 'asset', 1640, 950, rot=3, path='patrocinadores/onfly.webp', size=150, sway=2.8),
        pop(1.15, 'asset', 1815, 945, rot=-5, path='patrocinadores/coffee-plusplus.webp', size=140, sway=3.4),
        pop(1.6, 'pill', 960, 735, text='Toca pra ver o que rolou até aqui', emoji='▶️', size=34, bg=ORANGE, border=INK2, shadow=INK2),
        dict(k='cursor', at=3.2, x0=1300, y0=1150, x=1000, y=742, move=.9, click=1.25, gone=2.2),
    ], tl=2.9, bg=list(INK), full=True, iris=dict(at=4.95, x=960, y=740, dur=.75),
        why='Tela 01 do site ("EPISÓDIO 300") vira o "trailer": o clique no botão abre a íris para a câmera real.'),

    # ---------------- ATO: 300 / dados × acho ----------------
    cue('C01_01', 'ADESIVO_300', 513.05, 2.0, [slap(0, '300', 230, 470, 330, emoji='🥳')],
        why='"episódio especial de número 300" — adesivo 300 da intro do site.'),
    cue('C01_02', 'DADOS_11526', 522.85, 9.4, [
        slap(0, 'dados,', 150, 430, 250, color=ORANGE, emoji='🤓'),
        counter(1.75, 11526, 150, 430, 470, color=WHITE, frm=0, cdur=1.0),
        overline(1.9, 'VEZES', 430, 575, color=WHITE, size=28),
        slap(6.5, 'acho', 110, 440, 760, color=INK2, emoji='🤔', rot=4),
    ], why='"Pô, dados, né? 11.526 vezes. A segunda mais falada foi acho."'),
    cue('C01_03', 'PLACAR_DADOS_X_ACHO', 532.25, 6.3, [
        dict(k='custom', fn='placar'),
    ], bg=list(CREAM), full=True, why='"494 vezes de diferença" + "existe pra aumentar essa distância" — placar.'),

    # ---------------- ATO: de onde vem ----------------
    cue('C02_01', 'CARIMBO_2015_MB_TALKS', 544.3, 11.0, [
        pop(0, 'stamp', 400, 250, rot=-6, lines=['2015'], size=90, anim='stamp'),
        pop(1.6, 'label', 420, 420, rot=3, lines=['programa do Prime', '“MB Talks”'], size=40),
        pop(5.2, 'label', 400, 610, rot=-4, lines=['2 pessoas + 1 pergunta', 'por semana'], size=36),
    ], why='Calma: só um carimbo de data e duas etiquetas (fala de história, sem gag).'),
    cue('C02_02', 'CHUVA_DE_PERGUNTAS', 558.7, 3.3, [dict(k='custom', fn='question_rain')],
        why='"São mais de 300 perguntas" — microgag: chuva de adesivos "?".'),

    # ---------------- ATO: o que mudou ----------------
    cue('C03_01', 'RAJADA_FERRAMENTA', 570.4, 12.9, [
        pop(3.5, 'pill', 380, 200, rot=-3, text='ferramenta', emoji='🔧', size=40),
        pop(4.55, 'label', 380, 340, rot=-4, lines=['Como instalar?'], size=44),
        pop(5.6, 'label', 420, 470, rot=3, lines=['Como taguear?'], size=44),
        pop(7.0, 'label', 400, 640, rot=-2, lines=['Por que o número do relatório', 'não bate com o do financeiro?'], size=36),
        pop(11.4, 'stamp', 470, 780, rot=-8, lines=['ATÉ HOJE'], size=64, anim='stamp'),
    ], why='"Como instalar? Como taguear? ... Parece que até hoje essa realidade existe."'),
    cue('C03_02', 'UNIVERSAL_DESLIGADO', 584.6, 5.4, [
        pop(0, 'pill', 380, 170, rot=-3, text='Universal Analytics', emoji='📊', size=40, exit='fall', out=1.9),
        pop(1.85, 'stamp', 340, 320, rot=-7, lines=['DESLIGADO'], size=70, anim='stamp', exit='fall', out=4.9),
    ], why='"o Google Analytics desligou o Universal" — o objeto desliga e cai do quadro.'),
    cue('C03_03', 'CONTADOR_153_E_GRADE_4_DE_10', 589.9, 8.35, [
        counter(1.4, 153, 190, 360, 250, color=WHITE),
        overline(1.7, 'EPISÓDIOS EM 2023', 360, 380, color=WHITE, size=28),
        dict(k='grid', at=4.7, n=10, fill=4, cols=5, r=34, gap=20, x=360, y=520, fill_at=.4),
        pop(5.5, 'pill', 360, 720, text='4 em cada 10 = GA4', size=36, bg=ORANGE, border=INK2, shadow=INK2),
    ], why='"153 episódios, 4 em cada 10 falavam sobre o GA4" — grade de proporção.'),
    cue('C03_04', 'DE_NADA_VITORIA_1', 620.45, 3.2, [
        slap(0, 'de nada, Vitória.', 80, 450, 860, emoji='🫡'),
        pop(.5, 'arrow', 140, 640, rot=130, length=200, color=WHITE),
        pop(.6, 'pill', 640, 750, rot=4, text='zoeira nº 1', size=26, bg=WHITE, border=INK2, shadow=INK2, fg=INK2),
    ], why='Piada interna gravada ("volta aí que eu vou zoar a Vitória") — seta aponta pra fora do quadro (plateia).'),
    cue('C03_05', 'GA4_1_DE_3_E_O_LADO_DELE', 623.5, 8.1, [
        pop(0, 'pill', 420, 250, rot=-3, text='GA4', size=56, bg=ORANGE, border=INK2, shadow=INK2),
        dict(k='grid', at=2.6, n=3, fill=1, r=40, gap=24, x=420, y=400),
        overline(3.0, '1 A CADA 3 EPISÓDIOS', 420, 500, color=WHITE, size=26),
        pop(6.2, 'label', 420, 650, rot=4, lines=['+ o que entrou do lado dele…'], size=34),
    ], why='"ainda tá em um a cada três episódios. O que mudou foi o que entrou do lado dele."'),
    cue('C03_06', 'GOSTA_POUCO_IA', 632.2, 4.1, [
        slap(2.4, 'inteligência artificial', 76, 960, 105, color=ORANGE, emoji='🤖'),
        pop(1.5, 'pill', 1520, 360, rot=6, text='“gosto pouco”', emoji='🙃', size=30, bg=WHITE, border=INK2, shadow=INK2, fg=INK2),
    ], why='Ironia real ("é um tema que eu gosto pouco, meu parceiro: IA").'),
    cue('C03_07', 'IA_2021_2025_E_BIGQUERY', 637.2, 15.4, [
        pop(0, 'label', 400, 220, rot=-3, lines=['até 2021: IA fora da pauta'], size=36),
        pop(2.7, 'stamp', 400, 360, rot=5, lines=['2025'], size=64, anim='stamp'),
        dict(k='grid', at=3.3, n=4, fill=1, r=38, gap=22, x=400, y=480),
        overline(3.7, '1 A CADA 4 EPISÓDIOS', 400, 570, color=WHITE, size=24),
        pop(8.95, 'pill', 260, 670, rot=-2, text='atribuição', size=32),
        pop(9.2, 'pill', 470, 755, rot=3, text='incrementalidade', size=32),
        pop(11.8, 'label', 420, 860, rot=-3, lines=['BigQuery: assunto de engenheiro'], size=34, out=15.1),
        dict(k='strike', at=13.4, w=300, x=560, y=868, rot=-3, width=10, out=15.1),
        pop(14.0, 'stamp', 640, 965, rot=-8, lines=['MARKETING'], size=48, anim='stamp', out=15.1),
    ], why='IA 2021→2025, atribuição/incrementalidade e o BigQuery que "virou assunto de marketing".'),
    cue('C03_08', 'BOTAO_VIRA_MODELO', 652.85, 7.3, [
        pop(0, 'pill', 420, 420, rot=-2, text='como taguear um botão?', size=40, bg=ORANGE, border=INK2, shadow=INK2, out=3.9, exit='shrink'),
        dict(k='cursor', at=1.1, x0=700, y0=1100, x=430, y=430, move=.8, click=1.2, gone=2.6),
        pop(4.1, 'pill', 420, 420, rot=3, text='dá pra confiar no modelo?', emoji='🤖', size=40, anim='slap'),
        slap(6.55, 'modelo.', 70, 640, 600, color=ORANGE, rot=6),
    ], why='"começou perguntando como taguear um botão / hoje: se dá pra confiar no modelo" — o botão do site vira a pergunta nova.'),

    # ---------------- ATO: o que não mudou ----------------
    cue('C04_01', 'BORDAO_203_REPLAY', 669.3, 5.6, [dict(k='custom', fn='bordao_stack')],
        why='"203 vezes que eu falei fala aí, analítica" — o quadro real da abertura vira pilha de adesivos (REALIDADE→ADESIVO).'),
    cue('C04_02', 'EPISODIO_DE_ORIGEM_INTERROGACAO', 675.2, 3.3, [
        pop(0, 'label', 960, 160, rot=-3, lines=['episódio de origem: ???'], size=42),
        pop(1.9, 'emoji', 1250, 150, ch='🤷', size=110, anim='burst'),
    ], why='"você sabe qual foi o episódio que nasceu? — Não, nem eu."'),
    cue('C04_03', 'APELIDOS_16', 680.0, 9.5, [
        counter(0, 16, 210, 330, 210, color=WHITE, out=4.4),
        overline(.3, 'JEITOS DE APRESENTAR O LUCIAN', 390, 330, color=WHITE, size=22, out=4.4),
        pop(1.2, 'label', 370, 450, rot=-4, lines=['“O diamante negro', 'do Analytics”'], sub='EP 203', size=32, out=4.4),
        pop(5.3, 'label', 1480, 380, rot=4, lines=['“O diamante negro', 'do Analytics”'], sub='EP 203', size=40, anim='slap', out=9.2),
        pop(1.46, 'label', 400, 590, rot=3, lines=['“Super choque', 'do analítico”'], sub='EP 205', size=32, out=4.5),
        pop(1.72, 'label', 360, 720, rot=-2, lines=['“CTO and Black Diamond”'], sub='EP 256', size=32, out=4.6),
        pop(1.98, 'label', 420, 840, rot=5, lines=['“O cara na qual', 'o GTM pede bênção”'], sub='EP 270', size=30, out=4.7),
        pop(2.24, 'label', 420, 970, rot=-3, lines=['“Cebola, porque bota', 'as tags pra chorar”'], sub='EP 69', size=30, out=4.8),
        pop(6.1, 'stamp', 1500, 560, rot=-9, lines=['OFICIAL'], size=86, anim='stamp', fill=ORANGE, out=9.2),
    ], why='"16 maneiras de me apresentar" + "diamante negro é oficial" — etiquetas do site (tela 05) + carimbo.'),
    cue('C04_04', 'GRITEM_SE_CONCORDAM', 689.60, 0.14 + HOLD_GRITEM + 0.36, [
        dict(k='photo', at=0.0, img='freeze:G:689.60', to=(620, 560, .52, -5), hold=.15, shrink=.5, out=0.14 + HOLD_GRITEM),
        dict(k='marquee', at=.55, lines=['GRITEM', 'SE CONCORDAM!'], size=74, x=1390, y=520, rot=4, anim='slap', out=0.14 + HOLD_GRITEM),
        pop(.75, 'emoji', 1760, 280, ch='📣', size=120, anim='burst', out=0.14 + HOLD_GRITEM),
    ], hold=(0.14, HOLD_GRITEM), why='Quebra da 4ª parede real ("né galera? Gritem se concordam"): congela, vira adesivo, placa de cinema e 1,6 s de respiro pra sala responder.'),
    cue('C04_05', 'PICA_PAU_24', 690.55, 6.2, [
        overline(0, 'FRASE CLÁSSICA DO LUCIAN', 360, 190, color=ORANGE, size=22),
        pop(1.9, 'label', 370, 330, rot=-2, lines=['“Se o Pica-Pau tivesse', 'chamado a polícia, nada', 'disso teria acontecido.”'], size=38),
        pop(.35, 'stamp', 400, 560, rot=7, lines=['24×'], size=96, anim='stamp'),
    ], why='"24 vezes alguém lembrou que se o Pica-Pau..." (tela 04 do site).'),
    cue('C05_01', 'MESA_191_348_140', 703.85, 8.3, [
        overline(-.2 + .2, 'QUEM SENTA NA MESA', 400, 150, size=24),
        counter(.05, 191, 150, 330, 270, color=WHITE), overline(.3, 'PESSOAS', 330, 370, color=WHITE, size=24),
        counter(4.65, 348, 150, 330, 500, color=WHITE), overline(4.9, 'PARTICIPAÇÕES', 360, 600, color=WHITE, size=24),
        counter(6.85, 140, 150, 330, 730, color=ORANGE, fmt='{}+'), overline(7.1, 'EMPRESAS', 330, 830, color=WHITE, size=24),
    ], why='"191 pessoas sentaram nessa mesa, 348 vezes, mais de 140 empresas."'),

    # ---------------- ATO: quem respondeu ----------------
    cue('C05_02', 'SETORES_E_GOOGLE', 756.6, 8.0, [
        pop(0, 'pill', 300, 200, rot=-3, text='banco', emoji='🏦', size=34),
        pop(.65, 'pill', 540, 250, rot=3, text='varejo', emoji='🛒', size=34),
        pop(1.25, 'pill', 320, 320, rot=2, text='mídia', emoji='📺', size=34),
        pop(1.75, 'pill', 560, 380, rot=-4, text='telecom', emoji='📡', size=34),
        slap(2.85, 'até o Google', 90, 440, 520, color=INK2, emoji='👀', rot=-3),
        pop(4.3, 'stamp', 440, 720, rot=-6, lines=['PARCEIRO DO GOOGLE?'], size=46, anim='stamp'),
        pop(5.9, 'stamp', 470, 840, rot=5, lines=['AINDA NÃO'], size=62, anim='stamp', fill=ORANGE),
    ], why='"banco, varejo, mídia, telecom e até o Google ... ainda assim a gente não é parceiro do Google?"'),
    cue('C05_03', 'EU_QUERIA_TAMBEM_QUERIA', 763.0, 1.8, [
        dict(k='face', who='lucian', size=230, at=0, x=200, y=210, rot=-6, anim='pop', susto=.05),
        dict(k='face', who='gustavo', size=230, at=.6, x=1720, y=210, rot=6, anim='pop', susto=.8),
    ], why='"Eu queria. / Também queria." — os dois adesivos levam o susto do site.'),
    cue('C05_04', 'PICA_PAU_CHAMAMOS_A_POLICIA', 764.9, 8.2, [
        pop(0, 'label', 430, 300, rot=3, lines=['“Se o Pica-Pau tivesse', 'chamado a polícia…”'], size=36),
        pop(2.5, 'stamp', 470, 470, rot=-6, lines=['NÓS CHAMAMOS'], size=56, anim='stamp'),
        pop(4.1, 'label', 440, 640, rot=-2, lines=['gravamos até com a PM do RJ'], size=34),
        pop(4.4, 'emoji', 760, 610, ch='🚓', size=110, anim='burst'),
    ], why='Callback do Pica-Pau: "não chamou a polícia, mas nós chamamos. Gravamos até com a PM do Rio".'),
    cue('C05_05', 'FICHA_DE_PRESENCA', 773.4, 20.3, [dict(k='custom', fn='ficha')],
        why='"Teve gente que gabaritou a ficha de presença" — Phill 29, Mafê 24 (ep. 1), Cláudio Bonel 7.'),

    # ---------------- ATO: a gente chegou antes ----------------
    cue('C06_01', 'ACERTA_ANTES', 859.85, 1.5, [slap(0, 'acerta antes.', 110, 480, 260, emoji='🎯')],
        why='"de vez em quando você acerta antes".'),
    cue('C06_02', 'BLEEP', 861.15, 1.4, [
        dict(k='bleep', at=0, x=420, y=300, w=560, h=140, anim='slap', out=1.15),
        pop(.1, 'emoji', 150, 170, ch='🙊', size=120, anim='burst', out=1.15),
    ], why='Palavrão real da reação — bleep como gag (removível).'),
    cue('C06_03', 'FEV_2022_TODINHO', 862.55, 10.1, [
        pop(0, 'stamp', 400, 200, rot=-5, lines=['FEV 2022'], size=70, anim='stamp'),
        pop(.4, 'label', 430, 350, rot=2, lines=['“o GA4 era esse', 'todinho todo?”'], size=38),
        pop(4.3, 'emoji', 700, 310, ch='🥛', size=90, anim='burst'),
        pop(5.5, 'pill', 420, 500, rot=-4, text='desculpa, Vi.', emoji='🙏', size=30, bg=WHITE, border=INK2, shadow=INK2, fg=INK2),
        pop(5.75, 'pill', 640, 560, rot=5, text='zoeira nº 2', size=24, bg=ORANGE, border=INK2, shadow=INK2),
        pop(6.7, 'stamp', 450, 740, rot=6, lines=['+27 DIAS', 'GOOGLE: FIM DO UA'], size=50, anim='stamp', fill=ORANGE),
    ], why='Módulo "nossa pergunta → resposta do mercado" (1/4) + zoeira nº 2 com a Vi.'),
    cue('C06_04', 'OUT_2024_MMM_MERIDIAN', 873.0, 10.6, [
        pop(0, 'stamp', 400, 200, rot=4, lines=['OUT 2024'], size=70, anim='stamp'),
        pop(.6, 'label', 420, 340, rot=-3, lines=['episódio inteiro sobre MMM'], size=36),
        pop(3.7, 'asset', 1560, 280, rot=5, path='patrocinadores/purple-metrics.webp', size=300, sway=2.9, out=7.8),
        pop(4.1, 'pill', 1540, 440, rot=-4, text='de nada', emoji='👋', size=32, bg=WHITE, border=INK2, shadow=INK2, fg=INK2, out=7.8),
        pop(8.3, 'stamp', 370, 560, rot=-6, lines=['+3 MESES', 'GOOGLE: MERIDIAN'], size=50, anim='stamp', fill=ORANGE),
        pop(9.9, 'pill', 330, 720, rot=4, text='viu, Laila?', emoji='👀', size=30, bg=WHITE, border=INK2, shadow=INK2, fg=INK2),
    ], why='Módulo 2/4 + recados reais para a plateia (Purple Metrics, Laila).'),
    cue('C06_05', 'ABR_2025_MCP', 883.8, 7.15, [
        pop(0, 'stamp', 400, 200, rot=-4, lines=['ABR 2025'], size=70, anim='stamp'),
        pop(1.6, 'label', 380, 350, rot=2, lines=['1º MCP do mundo', 'pro Google Analytics'], size=38),
        pop(2.2, 'emoji', 150, 300, ch='🌍', size=90, anim='burst'),
        pop(4.9, 'stamp', 380, 560, rot=6, lines=['JUL 2025', 'O DO GOOGLE'], size=50, anim='stamp', fill=ORANGE),
    ], why='Módulo 3/4.'),
    cue('C06_06', 'DEZ_2024_CONVERSAR_COM_DADOS', 897.7, 15.9, [
        pop(0, 'stamp', 400, 200, rot=5, lines=['DEZ 2024'], size=70, anim='stamp', out=14.0),
        pop(.5, 'label', 430, 350, rot=-2, lines=['“vai dar pra conversar', 'com os dados”'], size=38, out=14.0),
        pop(5.4, 'pill', 470, 500, rot=4, text='meia-culpa', emoji='🙋', size=30, bg=WHITE, border=INK2, shadow=INK2, fg=INK2, out=7.0),
        pop(6.8, 'stamp', 370, 540, rot=-6, lines=['FEV 2026', 'IA NA HOME DO GA'], size=50, anim='stamp', fill=ORANGE, out=14.0),
        pop(10.1, 'stamp', 370, 740, rot=5, lines=['JUN 2026', 'A GENTE LANÇOU'], size=50, anim='stamp', out=14.0),
        dict(k='face', who='lucian', size=230, at=11.8, x=1640, y=250, rot=-7, anim='pop', susto=.1, out=14.0),
        pop(13.3, 'pill', 1610, 420, rot=4, text='“impossível”', size=30, bg=WHITE, border=INK2, shadow=INK2, fg=INK2, out=14.0),
        pop(14.6, 'stamp', 1450, 380, rot=-8, lines=['ACERTOU'], size=70, anim='stamp', fill=ORANGE),
    ], why='Módulo 4/4 (quebra o padrão: 3 datas) + "o Lucian falou que era impossível... mas eu acertei".'),

    # ---------------- ATO: do outro lado — vocês ----------------
    cue('C07_01', 'VOCES_PLATEIA', 914.80, 1.3, [
        slap(0, 'vocês.', 190, 960, 190, color=ORANGE, emoji='🫵'),
        pop(.2, 'arrow', 330, 800, rot=175, length=240, color=WHITE),
        pop(.25, 'arrow', 1600, 800, rot=85, length=240, color=WHITE),
    ], why='"E do outro lado da pergunta: vocês." — quebra da 4ª parede no cinema (setas para a sala).'),
    cue('C07_02', 'PLAY_700_MIL', 915.90, 6.2, [
        counter(.2, 700, 170, 400, 230, color=WHITE, fmt='{} mil', cdur=.9),
        overline(1.2, 'VEZES ALGUÉM APERTOU O PLAY', 420, 345, color=WHITE, size=22),
        pop(2.4, 'pill', 400, 520, rot=-2, text='play', emoji='▶️', size=64, bg=ORANGE, border=INK2, shadow=INK2),
        dict(k='cursor', at=2.5, x0=760, y0=1100, x=390, y=532, move=.75, click=.9, gone=1.8),
        counter(4.6, 106, 110, 330, 740, color=ORANGE, fmt='{} mil h', cdur=.8),
        dict(k='clock', at=4.7, x=660, y=740, r=48, anim='pop'),
    ], why='"700 mil vezes alguém apertou o play... 106 mil horas ouvidas" — botão do site + contadores.'),
    cue('C07_03', 'MARATONA_ATE_2038', 922.1, 6.9, [
        dict(k='sofa', at=.1, x=470, y=330, size=640, rot=2, anim='pop'),
        counter(2.9, 2038, 150, 430, 690, color=WHITE, frm=2026, cdur=2.6, raw=True),
        overline(3.1, 'SE NINGUÉM APERTAR O PAUSE', 430, 800, color=WHITE, size=22),
    ], why='"Se você apertasse o play agora e não parasse, terminaria em 2038" — cena do sofá (maratona) do site.'),
    cue('C07_04', 'PAISES_110', 928.9, 1.6, [slap(0, '110 países', 120, 480, 260, emoji='🌎')],
        why='"Em 110 países."'),
    cue('C07_05', 'EP_197', 933.75, 3.85, [
        pop(0, 'stamp', 420, 230, rot=-5, lines=['EP 197'], size=90, anim='stamp'),
        pop(.5, 'label', 430, 420, rot=3, lines=['Transição de carreira', 'para dados'], size=40),
        pop(.9, 'emoji', 700, 190, ch='🏆', size=100, anim='burst'),
        overline(1.2, 'O MAIS OUVIDO', 420, 560, color=WHITE, size=24),
    ], why='"o episódio mais ouvido é o 197, Transição de Carreira para Dados".'),
    cue('C07_06', 'GENTE', 941.7, 1.65, [slap(0, 'gente.', 150, 1580, 150, color=ORANGE, emoji='🧡')],
        why='Payoff: "A pergunta que mais bombou era sobre… gente."'),

    # ---------------- FINAL ----------------
    cue('C08_01', 'TITULO_EPISODIO', 950.72, 2.7, [dict(k='custom', fn='titulo')], bg=list(INK), full=True,
        why='"Qual o futuro da mensuração?" → título do episódio na tela (sobre "Esse é o tema do episódio?").'),
    cue('C09_01', 'FINAL_300_E_CONTANDO', None, OUTRO_DUR, [dict(k='custom', fn='final')], tl='END', bg=list(INK), full=True,
        why='Tela 13 do site: "300 e contando" + patrocinadores + "a sessão vai começar".'),
]
