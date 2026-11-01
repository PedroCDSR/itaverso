"""Gera o Aladdin do jogo (jogador) em quadros de 48x64, com o renderizador de volumes (modelo.py).

Design ORIGINAL e PROVISÓRIO (não há fotos do figurino da escola; CLAUDE.md seção 8 e 7.1):
cabelo preto cacheado com faixa rosa amarrada atrás (pontas ao vento), túnica curta verde sem mangas com gola em V,
faixa rosa na cintura com pontas, calça cor de areia justa no tornozelo com barra de couro, sandálias, bracelete e
argola dourados. Nada do design da Disney (sem colete roxo, sem chapéu fez, sem calça bufante branca: regra 3).

Medidas (references/estilo/reference-notes.md): corpo de ~58 px de altura num quadro de 48x64 (21% de 270),
cabeça ≈ 1/5,5 da altura, pernas ≈ metade do corpo, 4 tons por material, contorno colorido de 1 px.

O mesmo modelo gera o quadro "sentado", usado no tapete (fonte única, seção 7).

Saída: src/art/jogador.js e prévias PNG (folha com todos os quadros, ampliada).
Uso: python3 ferramentas/arte/gerar_jogador.py <repo> <pasta_previa>
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modelo import Boneco, Material, paleta_de, ponto, mistura  # noqa: E402
from pixel import escrever_js, imagem  # noqa: E402

L, A = 48, 64
PE_Y = 62  # linha da sola (a 63 é o contorno, que encosta no chão)

# --- materiais (4 tons: brilho, base, sombra, sombra funda; e o contorno colorido) ---
PELE = Material('pele', 'AsSzZ', ['#F6C79A', '#DB9A6B', '#B06C45', '#80452C', '#4A2216'], (0.78, 0.42, 0.10))
CABELO = Material('cabelo', 'HhiIJ', ['#6E4A52', '#45293A', '#2C1826', '#1C0E18', '#12060E'], (0.80, 0.50, 0.22))
TUNICA = Material('tunica', 'GgfFE', ['#A9E482', '#6CC24A', '#3F8C3A', '#285E2E', '#173A20'], (0.80, 0.45, 0.14))
FAIXA = Material('faixa', 'RruUV', ['#FFE2FC', '#FFB0FA', '#D17ACB', '#94489A', '#4C1E52'], (0.90, 0.52, 0.18))
CALCA = Material('calca', 'CcbBN', ['#FFF0CE', '#E8CC96', '#BE9A62', '#8A683E', '#4A321C'], (0.80, 0.46, 0.14))
COURO = Material('couro', 'LloKW', ['#C98E55', '#955F37', '#6A3D22', '#472513', '#2A1208'], (0.75, 0.40, 0.12))
OURO = Material('ouro', 'YyxXT', ['#FFF7C2', '#F2CF5A', '#C3962A', '#8A6418', '#4A3008'], (0.70, 0.40, 0.12))
MATERIAIS = [PELE, CABELO, TUNICA, FAIXA, CALCA, COURO, OURO]
EXTRAS = {'w': '#FFF6EA', 'e': '#1E1018', 'q': '#8E3A34', 'n': '#C2535A'}  # olho, pupila, boca, língua/boca aberta
PALETA = paleta_de(MATERIAIS, EXTRAS)

# --- proporções (px) ---
COXA, CANELA = 13.5, 13.0
BRACO, ANTEBRACO = 8.5, 8.0
COLUNA = 14.0  # do quadril até a base do pescoço


def pose(hx=23.0, hy=33.0, tronco=4.0, cabeca=0.0,
         coxa_f=0.0, joelho_f=0.0, pe_f=0.0, coxa_t=0.0, joelho_t=0.0, pe_t=0.0,
         ombro_f=-8.0, cotovelo_f=20.0, ombro_t=10.0, cotovelo_t=25.0,
         vento=0.0, fase=0.0, rosto='normal', mao_f='aberta', mao_t='aberta', saia=0.0, braco_t_atras=True,
         braco_f_frente=True, sentado=False):
    """Ângulos em graus. coxa: 0 = para baixo, + = para a frente. joelho: dobra para trás (+).
    ombro: 0 = braço para baixo, + = para a frente, 180 = para cima. cotovelo: dobra para a frente (+).
    tronco: inclinação para a frente. vento: quanto as pontas da faixa voam (0..1). fase: onda das pontas."""
    return dict(locals())


def junta_perna(quadril, coxa, joelho, pe):
    j = ponto(quadril, COXA, coxa)
    t = ponto(j, CANELA, coxa - joelho)
    # o pé aponta para a frente (+x), girado junto com a canela e pelo ângulo do pé
    ang_pe = coxa - joelho + 90 - pe
    return j, t, ang_pe


def desenhar(p):
    b = Boneco(L, A)
    hx, hy = p['hx'], p['hy']
    incl = p['tronco']
    pescoco = ponto((hx, hy), COLUNA, 180 - incl)  # para cima, inclinado para a frente
    peito = mistura((hx, hy), pescoco, 0.68)
    cab = ponto(pescoco, 6.6, 180 - incl * 0.6 - p['cabeca'])
    cab = (cab[0] + 0.6, cab[1])

    # ombros (vista 3/4 olhando para a direita): o de trás aparece um pouco à frente
    ombro_t = (pescoco[0] + 1.8, pescoco[1] + 2.4)
    ombro_f = (pescoco[0] - 2.0, pescoco[1] + 2.8)
    quadril_t = (hx + 1.6, hy)
    quadril_f = (hx - 1.2, hy + 0.4)

    def braco(ombro, ang, dobra, escurecer, mao_tipo, bracelete):
        cot = ponto(ombro, BRACO, ang)
        mao = ponto(cot, ANTEBRACO, ang + dobra)
        b.capsula(ombro, cot, 2.0, 1.75, PELE, escurecer)
        b.capsula(cot, mao, 1.75, 1.45, PELE, escurecer)
        # mão: um pouco maior que o pulso (lê melhor no celular)
        mao2 = ponto(mao, 1.2, ang + dobra)
        if mao_tipo == 'punho':
            b.elipse(mao2, 2.1, 2.1, PELE, escurecer)
        else:
            b.elipse(mao2, 1.9, 2.3, PELE, escurecer, giro=-(ang + dobra))
        if bracelete:
            pb = mistura(ombro, cot, 0.55)
            b.capsula(ponto(pb, 0.6, ang - 90 + 180), ponto(pb, 0.6, ang + 90 + 180), 1.0, 1.0, OURO, escurecer, pontas=True)
        return mao2

    def perna(quadril, coxa, joelho, pe_ang, escurecer):
        j, t, ang_pe = junta_perna(quadril, coxa, joelho, pe_ang)
        # calça justa no tornozelo, um pouco folgada na coxa
        b.capsula(quadril, j, 3.7, 3.1, CALCA, escurecer, achatar=0.95)
        b.capsula(j, t, 3.1, 2.4, CALCA, escurecer, achatar=0.95)
        # barra de couro no tornozelo
        tb = mistura(j, t, 0.92)
        b.capsula(tb, t, 2.5, 2.3, COURO, escurecer, pontas=False)
        # pé (pele) + sola (couro)
        dedos = ponto(t, 5.0, ang_pe)
        sola_a = ponto(t, 1.7, ang_pe + 90)
        sola_b = ponto(dedos, 1.1, ang_pe + 90)
        b.capsula(ponto(sola_a, 1.2, ang_pe + 180), sola_b, 0.6, 0.6, COURO, escurecer + 1, separar=False)
        b.capsula(t, dedos, 1.6, 1.15, PELE, escurecer, achatar=0.8)
        # tira da sandália por cima do peito do pé
        tira = mistura(t, dedos, 0.55)
        b.capsula(ponto(tira, 1.4, ang_pe - 90), ponto(tira, 0.8, ang_pe + 90), 0.55, 0.55, COURO, escurecer, separar=False)
        return j, t

    def pontas_faixa(origem, comp, larg, direcao, vento, fase, mat, escurecer=0):
        """Pontas de pano (faixa da cabeça ou da cintura) que ondulam ao vento."""
        pts = [origem]
        ang = direcao
        x, y = origem
        n = 4
        for i in range(n):
            ang_i = ang + math.sin(fase + i * 1.3) * (12 + 18 * vento) * (i + 1) / n
            x, y = ponto((x, y), comp / n, ang_i)
            pts.append((x, y))
        for i in range(n):
            r0 = larg * (1 - 0.15 * i)
            b.capsula(pts[i], pts[i + 1], r0, r0 * 0.85, mat, escurecer)

    # ---------- de trás para a frente ----------
    # 1. braço de trás
    if p['braco_t_atras']:
        braco(ombro_t, p['ombro_t'], p['cotovelo_t'], 1, p['mao_t'], False)

    # 2. pontas da faixa da cintura (atrás do corpo)
    vento = p['vento']
    no_x = hx - 4.2 - incl * 0.05
    no = (no_x, hy - 2.2)
    dir_pontas = -8 - vento * 70  # parado: caem; correndo: voam para trás
    pontas_faixa(no, 9 + vento * 2, 0.95, dir_pontas, vento, p['fase'], FAIXA, 1)
    pontas_faixa((no[0] + 0.5, no[1] + 0.6), 7 + vento * 2, 0.8, dir_pontas + 12, vento, p['fase'] + 1.7, FAIXA, 1)

    # 3. perna de trás
    if not p['sentado']:
        perna(quadril_t, p['coxa_t'], p['joelho_t'], p['pe_t'], 1)
    # 4. perna da frente
    jf, tf = perna(quadril_f, p['coxa_f'], p['joelho_f'], p['pe_f'], 0)
    if p['sentado']:
        perna(quadril_t, p['coxa_t'], p['joelho_t'], p['pe_t'], 1)

    # 5. tronco: túnica curta sem mangas
    b.capsula(peito, (hx, hy - 1.5), 4.4, 3.9, TUNICA, separar=False, achatar=0.92)
    b.elipse((peito[0] + 0.4, peito[1] - 0.8), 4.6, 3.3, TUNICA, separar=False, achatar=0.9)
    # barra da túnica (saia curta que abre um pouco e balança)
    s = p['saia']
    barra = hy + 5.5
    cintura = hy - 0.5
    b.poligono([(hx - 4.6, cintura), (hx + 4.6, cintura), (hx + 6.0 - s * 1.5, barra + s * 0.6),
                (hx - 5.8 - s * 2.0, barra - s * 1.2)], TUNICA, separar=False)
    # gola em V (pele aparecendo) e pescoço
    b.capsula(pescoco, (cab[0] - 0.4, cab[1] + 2.0), 2.0, 2.0, PELE, separar=False)
    gola_topo = (pescoco[0] + 0.8, pescoco[1] + 0.2)
    b.poligono([(gola_topo[0] - 2.4, gola_topo[1]), (gola_topo[0] + 2.8, gola_topo[1]),
                (gola_topo[0] + 0.6, gola_topo[1] + 4.6)], PELE, separar=False)

    # 6. faixa rosa na cintura (com dobras)
    faixa_y = hy - 2.6
    b.capsula((hx - 4.8, faixa_y + 0.2), (hx + 4.9, faixa_y - 0.1), 1.9, 1.9, FAIXA, separar=False, achatar=0.9)
    b.elipse(no, 1.8, 1.6, FAIXA, 1, separar=False)  # nó atrás

    # 7. cabeça
    cx, cy = cab
    # cabelo de trás: volume de cachos (cada cachinho é uma bolinha com luz própria)
    for dx, dy, r in ((-3.8, -0.4, 2.7), (-4.4, 2.4, 2.4), (-3.2, 4.6, 2.0), (-1.4, -3.4, 2.5), (1.6, -3.9, 2.3),
                      (-3.8, -3.0, 2.3), (4.0, -2.8, 2.0), (-5.6, 0.8, 1.8), (-1.2, 5.4, 1.6)):
        b.elipse((cx + dx, cy + dy), r, r, CABELO, separar=False)
    # rosto (normal "achatada": pele mais lisa, sombra só na borda)
    b.elipse((cx + 0.8, cy + 0.6), 4.4, 4.9, PELE, separar=False, achatar=0.65)
    b.elipse((cx + 2.4, cy + 3.0), 2.6, 2.3, PELE, separar=False, achatar=0.6)  # queixo e bochecha
    # orelha
    b.elipse((cx - 1.8, cy + 1.2), 1.2, 1.7, PELE, 1, separar=False, achatar=0.8)
    # franja em cachos por cima da testa
    for dx, dy, r in ((-0.2, -3.4, 1.9), (2.2, -3.6, 1.8), (4.2, -2.6, 1.4), (-2.4, -2.4, 1.7)):
        b.elipse((cx + dx, cy + dy), r, r * 0.9, CABELO, separar=False)
    # costeleta
    b.capsula((cx - 0.6, cy - 1.0), (cx - 0.4, cy + 1.8), 0.8, 0.6, CABELO, separar=False)

    # faixa rosa da cabeça, fina, na linha do cabelo (amarrada atrás, pontas ao vento)
    fa = (cx - 4.8, cy - 2.6)
    fb = (cx + 3.4, cy - 4.4)
    b.capsula(fa, fb, 0.8, 0.7, FAIXA, separar=False)
    no_cab = (cx - 5.2, cy - 2.2)
    pontas_faixa(no_cab, 7 + vento * 5, 0.85, -25 - vento * 62, vento, p['fase'] + 0.8, FAIXA, 0)
    pontas_faixa(no_cab, 6 + vento * 3, 0.7, -5 - vento * 60, vento, p['fase'] + 2.4, FAIXA, 1)
    b.elipse(no_cab, 1.2, 1.1, FAIXA, separar=False)
    # um cacho escapa por cima da faixa
    b.elipse((cx + 1.0, cy - 4.6), 1.2, 1.0, CABELO, separar=False)

    # 8. braço da frente (por cima de tudo, exceto quando a pose pede atrás)
    mao_f = None
    if p['braco_f_frente']:
        mao_f = braco(ombro_f, p['ombro_f'], p['cotovelo_f'], 0, p['mao_f'], True)
    if not p['braco_t_atras']:
        braco(ombro_t, p['ombro_t'], p['cotovelo_t'], 0, p['mao_t'], False)

    # ---------- detalhes à mão ----------
    rosto(b, cx, cy, p['rosto'])
    # argola dourada na orelha
    b.px(cx - 1.4, cy + 3.3, 'y')
    # brilho na faixa da cintura e uma dobra
    b.tom_em(hx + 1, faixa_y - 1, FAIXA, 0)
    b.tom_em(hx - 1, faixa_y + 1, FAIXA, 2)
    # costura da gola: borda em verde-escuro dos dois lados do V
    return b


def rosto(b, cx, cy, tipo):
    """Olhos, sobrancelhas, nariz e boca. Vista 3/4 olhando para a direita."""
    ox1, ox2, oy = cx + 1.2, cx + 4.0, cy + 0.6  # olho de perto (maior) e de longe
    if tipo in ('normal', 'esforco', 'sentado', 'feliz'):
        # olho de perto: branco + pupila
        b.px(ox1, oy, 'w'); b.px(ox1 + 1, oy, 'e'); b.px(ox1 + 1, oy + 1, 'e'); b.px(ox1, oy + 1, 'w')
        # olho de longe (só a pupila e um fio de branco)
        b.px(ox2, oy, 'e'); b.px(ox2, oy + 1, 'e'); b.px(ox2 - 1, oy + 1, 'w')
        # sobrancelhas
        sob = -1.4 if tipo != 'esforco' else -1.0
        b.px(ox1 - 0.5, oy + sob, 'I'); b.px(ox1 + 0.6, oy + sob - 0.4, 'I'); b.px(ox1 + 1.6, oy + sob - 0.4, 'I')
        b.px(ox2, oy + sob - 0.2, 'I'); b.px(ox2 + 1, oy + sob + (0.5 if tipo == 'esforco' else 0), 'I')
    elif tipo == 'dano':
        # olhos apertados (> <) e sobrancelhas para cima
        b.px(ox1, oy - 0.4, 'e'); b.px(ox1 + 1, oy + 0.5, 'e'); b.px(ox1, oy + 1.4, 'e')
        b.px(ox2 + 0.4, oy - 0.4, 'e'); b.px(ox2 - 0.6, oy + 0.5, 'e'); b.px(ox2 + 0.4, oy + 1.4, 'e')
        b.px(ox1 - 0.4, oy - 1.6, 'I'); b.px(ox2 + 0.6, oy - 1.8, 'I')
    # nariz: um pixel de sombra marcando a ponta
    b.tom_em(cx + 5.2, cy + 2.1, PELE, 2)
    b.tom_em(cx + 4.4, cy + 2.9, PELE, 2)
    # boca
    if tipo == 'feliz':
        b.px(cx + 2.6, cy + 4.2, 'q'); b.px(cx + 3.6, cy + 4.6, 'n'); b.px(cx + 4.4, cy + 4.0, 'q')
    elif tipo == 'esforco':
        b.px(cx + 3.0, cy + 4.4, 'q'); b.px(cx + 4.0, cy + 4.4, 'q')
    elif tipo == 'dano':
        b.px(cx + 3.0, cy + 4.2, 'q'); b.px(cx + 3.0, cy + 5.0, 'n'); b.px(cx + 4.0, cy + 4.6, 'q')
    else:
        b.px(cx + 3.0, cy + 4.4, 'q'); b.px(cx + 4.0, cy + 4.2, 'q')
    # sombra embaixo do queixo
    b.tom_em(cx + 0.2, cy + 5.6, PELE, 3)
    b.tom_em(cx + 1.2, cy + 5.9, PELE, 2)


# ---------------------------------------------------------------------------------------------
# Poses
# ---------------------------------------------------------------------------------------------

def parado(i):
    """Respiração: 4 quadros (sobe, segura, desce, segura). Peso na perna de trás, mão na cintura."""
    resp = [0.0, 0.5, 1.0, 0.5][i]
    return pose(hy=33.0 + resp * 0.4, tronco=2.0 - resp * 0.8, cabeca=-1.0 + resp,
                coxa_f=6, joelho_f=8, pe_f=-4, coxa_t=-5, joelho_t=0, pe_t=0,
                ombro_f=-22 + resp * 2, cotovelo_f=112, ombro_t=10, cotovelo_t=18,
                vento=0.05, fase=i * 0.9, mao_f='punho', saia=0.0)


def correndo(i, n=8):
    """Ciclo de corrida de 8 quadros. Corpo inclinado, braços opostos às pernas, pontas da faixa voando."""
    f = i / n * 2 * math.pi
    # perna da frente (f) e de trás (t) em oposição
    def perna_ang(fase):
        coxa = 34 * math.sin(fase)  # avanço/recuo da coxa
        if coxa < 0:
            coxa *= 0.7  # para trás a coxa vai menos (senão parece um chute)
        # joelho dobra muito quando a perna volta (recolhe) e pouco quando apoia
        dobra = 18 + 52 * max(0.0, math.sin(fase - 1.7)) ** 1.2 + 10 * max(0.0, -math.sin(fase))
        pe = -10 * math.cos(fase)
        return coxa, dobra, pe
    cf, jf, pf = perna_ang(f)
    ct, jt, pt = perna_ang(f + math.pi)
    sobe = -1.6 * abs(math.cos(f))  # o corpo sobe no meio do passo
    return pose(hy=34.2 + sobe, tronco=12, cabeca=-6,
                coxa_f=cf, joelho_f=jf, pe_f=pf, coxa_t=ct, joelho_t=jt, pe_t=pt,
                ombro_f=-40 * math.sin(f) + 5, cotovelo_f=70, ombro_t=40 * math.sin(f) + 5, cotovelo_t=70,
                vento=1.0, fase=f * 1.0, rosto='normal', mao_f='punho', mao_t='punho', saia=0.8)


def pulando():
    """Subida: perna da frente encolhida, de trás esticada, braço da frente para cima."""
    return pose(hy=30.0, tronco=6, cabeca=-4, coxa_f=70, joelho_f=95, pe_f=10, coxa_t=-22, joelho_t=30, pe_t=-30,
                ombro_f=-55, cotovelo_f=50, ombro_t=140, cotovelo_t=25, vento=0.7, fase=1.0, mao_t='aberta',
                saia=1.0, rosto='esforco')


def subindo2():
    return pose(hy=30.5, tronco=4, cabeca=-2, coxa_f=50, joelho_f=70, pe_f=0, coxa_t=10, joelho_t=60, pe_t=-20,
                ombro_f=-35, cotovelo_f=60, ombro_t=140, cotovelo_t=30, vento=0.6, fase=2.0, saia=0.6)


def caindo():
    """Descida: pernas abertas se preparando para pousar, braços abertos para equilíbrio."""
    return pose(hy=30.0, tronco=0, cabeca=2, coxa_f=30, joelho_f=40, pe_f=-10, coxa_t=-14, joelho_t=35, pe_t=-25,
                ombro_f=-110, cotovelo_f=-25, ombro_t=118, cotovelo_t=-20, vento=0.5, fase=3.5, saia=-0.8,
                rosto='normal')


def caindo2():
    return pose(hy=30.0, tronco=-2, cabeca=3, coxa_f=24, joelho_f=34, pe_f=-12, coxa_t=-10, joelho_t=40, pe_t=-28,
                ombro_f=-122, cotovelo_f=-30, ombro_t=130, cotovelo_t=-24, vento=0.5, fase=4.6, saia=-1.0)


def arremessando(i):
    """0 antecipação (braço lá atrás, corpo recua), 1 soltar (braço esticado à frente), 2 acompanhamento."""
    if i == 0:
        return pose(hy=33.4, tronco=-6, cabeca=2, coxa_f=16, joelho_f=12, pe_f=-6, coxa_t=-14, joelho_t=6, pe_t=0,
                    ombro_f=-120, cotovelo_f=-60, ombro_t=30, cotovelo_t=50, vento=0.3, fase=0.5, mao_f='punho',
                    rosto='esforco', saia=-0.4)
    if i == 1:
        return pose(hy=34.2, tronco=14, cabeca=-6, coxa_f=24, joelho_f=24, pe_f=-6, coxa_t=-18, joelho_t=14, pe_t=0,
                    ombro_f=96, cotovelo_f=4, ombro_t=-30, cotovelo_t=30, vento=0.5, fase=1.5, mao_f='aberta',
                    rosto='esforco', saia=0.8)
    return pose(hy=34.0, tronco=10, cabeca=-3, coxa_f=20, joelho_f=20, pe_f=-6, coxa_t=-16, joelho_t=10, pe_t=0,
                ombro_f=60, cotovelo_f=20, ombro_t=-16, cotovelo_t=40, vento=0.3, fase=2.5, mao_f='aberta',
                rosto='normal', saia=0.4)


def dano():
    """Leva um susto e é jogado para trás: corpo arqueado, braços para cima, olhos apertados."""
    return pose(hx=24.5, hy=32.0, tronco=-16, cabeca=12, coxa_f=24, joelho_f=40, pe_f=-20, coxa_t=-6, joelho_t=30,
                pe_t=-20, ombro_f=-150, cotovelo_f=-30, ombro_t=150, cotovelo_t=-20, vento=0.6, fase=4.0,
                rosto='dano', saia=-1.0)


def sentado(i):
    """No tapete (vista de lado), pernas cruzadas para a frente, mão no joelho; faixa da cabeça voando."""
    return pose(hx=20.0, hy=56.0, tronco=4, cabeca=-2, coxa_f=84, joelho_f=150, pe_f=40, coxa_t=80, joelho_t=140,
                pe_t=40, ombro_f=20, cotovelo_f=60, ombro_t=-10, cotovelo_t=30, vento=1.0, fase=i * 2.1,
                rosto='feliz', saia=0.6, sentado=True)


QUADROS_POSES = {
    'parado1': parado(0), 'parado2': parado(1), 'parado3': parado(2), 'parado4': parado(3),
    **{f'correndo{i + 1}': correndo(i) for i in range(8)},
    'pulando1': pulando(), 'pulando2': subindo2(),
    'caindo1': caindo(), 'caindo2': caindo2(),
    'arremessando1': arremessando(0), 'arremessando2': arremessando(1), 'arremessando3': arremessando(2),
    'dano': dano(),
    'sentado1': sentado(0), 'sentado2': sentado(1), 'sentado3': sentado(2),
}
ORDEM = list(QUADROS_POSES.keys())

# Animações (nome: quadros, quadros por segundo, repetição). O Preload lê isto direto.
ANIMACOES = {
    'parado': (['parado1', 'parado2', 'parado3', 'parado4'], 4, -1),
    'correndo': ([f'correndo{i + 1}' for i in range(8)], 16, -1),
    'pulando': (['pulando1', 'pulando2'], 8, 0),
    'caindo': (['caindo1', 'caindo2'], 6, -1),
    'arremessando': (['arremessando1', 'arremessando2', 'arremessando3'], 16, 0),
    'dano': (['dano'], 1, 0),
    'sentado': (['sentado1', 'sentado2', 'sentado3'], 8, -1),
}

CONTORNO_FIXO = {'w': 'Z', 'e': 'Z', 'q': 'Z', 'n': 'Z'}


def gerar():
    quadros = {}
    for nome, p in QUADROS_POSES.items():
        quadros[nome] = desenhar(p).texto(CONTORNO_FIXO)
    # encosta o contorno de baixo do pé na última linha (63) usando o quadro parado como régua; todos os quadros
    # de pé ou no ar descem juntos, para o corpo não "pular" ao trocar de animação
    def ultima(linhas):
        return max(y for y, l in enumerate(linhas) if any(c != '.' for c in l))
    desce = A - 1 - ultima(quadros['parado1'])
    for nome in quadros:
        if desce and not nome.startswith('sentado'):
            vazio = '.' * L
            quadros[nome] = [vazio] * desce + quadros[nome][:A - desce]
    return quadros


def main():
    repo = sys.argv[1] if len(sys.argv) > 1 else '.'
    previa = sys.argv[2] if len(sys.argv) > 2 else None
    quadros = gerar()
    # confere a altura do corpo no quadro parado (alvo: 56 a 60 px)
    linhas = quadros['parado1']
    ocup = [y for y, l in enumerate(linhas) if any(c != '.' for c in l)]
    print(f'parado1: linhas {ocup[0]}..{ocup[-1]} -> altura com contorno {ocup[-1] - ocup[0] + 1} px')
    cab = [
        'Aladdin do jogo (jogador): design ORIGINAL e PROVISÓRIO, gerado por ferramentas/arte/gerar_jogador.py.',
        'Quadros de 48x64 (corpo de ~58 px). Cabelo cacheado preto, faixa rosa na cabeça e na cintura, túnica verde',
        'sem mangas, calça areia com barra de couro, sandálias, argola e bracelete dourados. Sem nada do design da',
        'Disney (regra 3). Será ajustado quando chegarem as fotos do figurino (references/figurinos/).',
        'O quadro "sentado" é o mesmo personagem no tapete (fonte única, CLAUDE.md seção 7).',
    ]
    escrever_js(os.path.join(repo, 'src/art/jogador.js'), cab, PALETA, L, A, ORDEM, quadros, ANIMACOES)
    if previa:
        os.makedirs(previa, exist_ok=True)
        img = imagem([(quadros[n], PALETA) for n in ORDEM], escala=4)
        img.save(os.path.join(previa, 'jogador-quadros.png'))
        print('prévia:', os.path.join(previa, 'jogador-quadros.png'))


if __name__ == '__main__':
    main()
