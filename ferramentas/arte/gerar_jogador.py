"""Gera o Aladdin do jogo (jogador) em quadros de 48x64, com o renderizador de volumes (modelo.py).

Design ORIGINAL e PROVISÓRIO, versão 2 (aprovada pelo Pedro em 01/11/2026; sem fotos do figurino da escola):
corpo esguio, rosto fino (queixo estreito, olhos grandes com brilho, sobrancelha marcada, sorriso de canto), cabelo
preto cacheado com faixa rosa amarrada atrás (pontas ao vento), colete VERDE aberto com debrum dourado sobre o peito,
faixa rosa larga na cintura, calça LARGA LILÁS franzida no tornozelo (esvoaça na corrida), sandálias, bracelete e
argola dourados. Linguagem do Aladdin do SNES (silhueta, pano que esvoaça), mas nada do design da Disney: sem colete
roxo, sem fez, sem calça bufante branca (regra 3).

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
COLETE = Material('colete', 'GgfFE', ['#A9E482', '#6CC24A', '#3F8C3A', '#285E2E', '#173A20'], (0.80, 0.45, 0.14))
FAIXA = Material('faixa', 'RruUV', ['#FFE2FC', '#FFB0FA', '#D17ACB', '#94489A', '#4C1E52'], (0.90, 0.52, 0.18))
CALCA = Material('calca', 'CcbBN', ['#C8C6FF', '#9E9EFF', '#7C7AE6', '#5654C0', '#2C2A74'], (0.88, 0.55, 0.20))
COURO = Material('couro', 'LloKW', ['#C98E55', '#955F37', '#6A3D22', '#472513', '#2A1208'], (0.75, 0.40, 0.12))
OURO = Material('ouro', 'YyxXT', ['#FFF7C2', '#F2CF5A', '#C3962A', '#8A6418', '#4A3008'], (0.70, 0.40, 0.12))
MATERIAIS = [PELE, CABELO, COLETE, FAIXA, CALCA, COURO, OURO]
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
    vento = p['vento']
    pescoco = ponto((hx, hy), COLUNA, 180 - incl)
    peito = mistura((hx, hy), pescoco, 0.68)
    cab = ponto(pescoco, 6.6, 180 - incl * 0.6 - p['cabeca'])
    cab = (cab[0] + 0.6, cab[1])
    ombro_t = (pescoco[0] + 1.8, pescoco[1] + 2.4)
    ombro_f = (pescoco[0] - 2.0, pescoco[1] + 2.8)
    quadril_t = (hx + 1.6, hy)
    quadril_f = (hx - 1.2, hy + 0.4)

    def braco(ombro, ang, dobra, esc, mao_tipo, bracelete):
        cot = ponto(ombro, BRACO, ang)
        mao = ponto(cot, ANTEBRACO, ang + dobra)
        b.capsula(ombro, cot, 1.7, 1.5, PELE, esc)      # braço mais fino (corpo esguio)
        b.capsula(cot, mao, 1.5, 1.25, PELE, esc)
        m2 = ponto(mao, 1.2, ang + dobra)
        if mao_tipo == 'punho':
            b.elipse(m2, 2.1, 2.1, PELE, esc)
        else:
            b.elipse(m2, 1.9, 2.3, PELE, esc, giro=-(ang + dobra))
        if bracelete:
            pb = mistura(cot, mao, 0.75)
            b.capsula(ponto(pb, 0.8, ang + dobra - 90), ponto(pb, 0.8, ang + dobra + 90), 1.1, 1.1, OURO, esc)

    def perna(quadril, coxa, joelho, pe_ang, esc):
        j, t, ang_pe = junta_perna(quadril, coxa, joelho, pe_ang)
        # calça larga: coxa e canela grossas, e o pano "atrasa" (vai para trás) com o vento
        atras = ponto(mistura(j, t, 0.45), 1.2 + 2.2 * vento, -90)
        b.capsula(quadril, j, 4.0, 3.8, CALCA, esc, achatar=0.9)
        b.capsula(j, atras, 4.0, 4.2, CALCA, esc, achatar=0.9)
        b.capsula(atras, t, 4.2, 2.6, CALCA, esc, achatar=0.9)
        # barra franzida no tornozelo (punho rosa)
        b.capsula(ponto(t, 0.8, coxa - joelho + 180), t, 2.6, 2.4, FAIXA, esc, pontas=False)
        # dobras do pano
        meio = mistura(j, t, 0.55)
        b.tom_em(meio[0] - 1, meio[1], CALCA, 2 + esc)
        b.tom_em(meio[0] + 1, meio[1] + 2, CALCA, 2 + esc)
        b.tom_em(j[0], j[1] + 1, CALCA, 0 if not esc else 1)
        # sandália (igual à de hoje)
        dedos = ponto(t, 5.0, ang_pe)
        sa, sb = ponto(t, 1.7, ang_pe + 90), ponto(dedos, 1.1, ang_pe + 90)
        b.capsula(ponto(sa, 1.2, ang_pe + 180), sb, 0.6, 0.6, COURO, esc + 1, separar=False)
        b.capsula(t, dedos, 1.6, 1.15, PELE, esc, achatar=0.8)
        tira = mistura(t, dedos, 0.55)
        b.capsula(ponto(tira, 1.4, ang_pe - 90), ponto(tira, 0.8, ang_pe + 90), 0.55, 0.55, COURO, esc,
                  separar=False)

    def pontas(origem, comp, larg, direcao, fase, mat, esc=0):
        pts, x, y = [origem], origem[0], origem[1]
        for i in range(4):
            a = direcao + math.sin(fase + i * 1.3) * (12 + 18 * vento) * (i + 1) / 4
            x, y = ponto((x, y), comp / 4, a)
            pts.append((x, y))
        for i in range(4):
            r0 = larg * (1 - 0.15 * i)
            b.capsula(pts[i], pts[i + 1], r0, r0 * 0.85, mat, esc)

    if p['braco_t_atras']:
        braco(ombro_t, p['ombro_t'], p['cotovelo_t'], 1, p['mao_t'], False)
    no = (hx - 4.4 - incl * 0.05, hy - 2.0)
    dirp = -8 - vento * 70
    pontas(no, 10 + vento * 3, 1.1, dirp, p['fase'], FAIXA, 1)
    pontas((no[0] + 0.5, no[1] + 0.6), 8 + vento * 2, 0.9, dirp + 12, p['fase'] + 1.7, FAIXA, 1)
    if not p['sentado']:
        perna(quadril_t, p['coxa_t'], p['joelho_t'], p['pe_t'], 1)
    perna(quadril_f, p['coxa_f'], p['joelho_f'], p['pe_f'], 0)
    if p['sentado']:
        perna(quadril_t, p['coxa_t'], p['joelho_t'], p['pe_t'], 1)
    # tronco: peito à mostra (pele) e colete verde aberto por cima
    b.capsula(peito, (hx, hy - 1.5), 3.7, 2.9, PELE, separar=False, achatar=0.92)   # tronco esguio, cintura fina
    b.elipse((peito[0] + 0.4, peito[1] - 0.8), 3.9, 3.0, PELE, separar=False, achatar=0.9)
    pz = pescoco
    # lado de trás do colete (mais largo, vista 3/4) e lado da frente (estreito)
    b.poligono([(pz[0] - 4.8, pz[1] + 1.2), (pz[0] - 0.2, pz[1] + 0.8), (hx - 0.6, hy - 2.6), (hx - 4.4, hy - 2.0)],
               COLETE, separar=False)
    b.poligono([(pz[0] + 2.4, pz[1] + 1.4), (pz[0] + 4.8, pz[1] + 2.6), (hx + 4.2, hy - 2.4), (hx + 2.6, hy - 3.0)],
               COLETE, separar=False)
    for a_, b_ in (((pz[0] - 0.2, pz[1] + 0.8), (hx - 0.6, hy - 2.6)), ((pz[0] + 2.4, pz[1] + 1.4), (hx + 3.0, hy - 3.0))):
        n = 10
        for i in range(n + 1):
            q = mistura(a_, b_, i / n)
            b.tom_em(q[0], q[1], OURO, 1)       # debrum dourado na abertura
    b.capsula(pescoco, (cab[0] - 0.4, cab[1] + 2.0), 2.0, 2.0, PELE, separar=False)
    # faixa larga na cintura
    fy = hy - 2.2
    b.capsula((hx - 4.4, fy + 0.4), (hx + 4.6, fy), 2.1, 2.1, FAIXA, separar=False, achatar=0.9)
    b.elipse(no, 2.0, 1.8, FAIXA, 1, separar=False)
    # cabeça (igual à de hoje: cachos, faixa rosa com pontas)
    cx, cy = cab
    for dx, dy, r in ((-3.8, -0.4, 2.7), (-4.4, 2.4, 2.4), (-3.2, 4.6, 2.0), (-1.4, -3.4, 2.5), (1.6, -3.9, 2.3),
                      (-3.8, -3.0, 2.3), (4.0, -2.8, 2.0), (-5.6, 0.8, 1.8), (-1.2, 5.4, 1.6)):
        b.elipse((cx + dx, cy + dy), r, r, CABELO, separar=False)
    b.elipse((cx + 0.8, cy + 0.4), 4.0, 5.0, PELE, separar=False, achatar=0.65)     # rosto mais fino
    b.elipse((cx + 2.6, cy + 3.4), 2.0, 2.1, PELE, separar=False, achatar=0.6)      # queixo estreito
    b.elipse((cx - 1.8, cy + 1.2), 1.2, 1.7, PELE, 1, separar=False, achatar=0.8)
    for dx, dy, r in ((-0.2, -3.6, 2.1), (2.2, -3.9, 2.0), (4.2, -2.8, 1.5), (-2.4, -2.6, 1.8), (0.9, -5.0, 1.6)):
        b.elipse((cx + dx, cy + dy), r, r * 0.9, CABELO, separar=False)
    b.capsula((cx - 0.6, cy - 1.0), (cx - 0.4, cy + 1.8), 0.8, 0.6, CABELO, separar=False)
    b.capsula((cx - 4.8, cy - 2.6), (cx + 3.4, cy - 4.4), 0.8, 0.7, FAIXA, separar=False)
    nc = (cx - 5.2, cy - 2.2)
    pontas(nc, 7 + vento * 5, 0.85, -25 - vento * 62, p['fase'] + 0.8, FAIXA, 0)
    pontas(nc, 6 + vento * 3, 0.7, -5 - vento * 60, p['fase'] + 2.4, FAIXA, 1)
    b.elipse(nc, 1.2, 1.1, FAIXA, separar=False)
    b.elipse((cx + 1.0, cy - 4.6), 1.2, 1.0, CABELO, separar=False)
    if p['braco_f_frente']:
        braco(ombro_f, p['ombro_f'], p['cotovelo_f'], 0, p['mao_f'], True)
    if not p['braco_t_atras']:
        braco(ombro_t, p['ombro_t'], p['cotovelo_t'], 0, p['mao_t'], False)
    # rosto (versão 2): olhos maiores (2x2 com brilho), sobrancelha grossa e reta, nariz marcado, sorriso de canto.
    rosto2(b, cx, cy, p['rosto'])
    b.px(cx - 1.4, cy + 3.3, 'y')
    b.tom_em(hx + 1, fy - 1, FAIXA, 0)
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


def rosto2(b, cx, cy, tipo):
    if tipo in ('dano', 'esforco'):
        rosto(b, cx, cy, tipo)
        return
    ox1, ox2, oy = cx + 0.6, cx + 3.4, cy + 0.4
    if tipo == 'piscando':
        b.px(ox1, oy + 1, 'e'); b.px(ox1 + 1, oy + 1, 'e'); b.px(ox2, oy + 1, 'e')
    else:
        # olho de perto: 2x2 (branco + pupila grande) com brilho; olho de longe: pupila e fio de branco
        b.px(ox1, oy, 'w'); b.px(ox1, oy + 1, 'w'); b.px(ox1 + 1, oy, 'e'); b.px(ox1 + 1, oy + 1, 'e')
        b.px(ox1 + 1, oy + 2, 'e'); b.px(ox1 + 2, oy + 1, 'e')
        b.px(ox1 + 1, oy, 'w')                     # brilho no olho
        b.px(ox2, oy, 'e'); b.px(ox2, oy + 1, 'e'); b.px(ox2, oy + 2, 'e'); b.px(ox2 - 1, oy + 1, 'w')
    # sobrancelhas grossas, um pouco arqueadas (expressão confiante)
    for x, y in ((ox1 - 0.6, oy - 1.4), (ox1 + 0.4, oy - 1.9), (ox1 + 1.4, oy - 1.9), (ox2 - 0.2, oy - 1.9),
                 (ox2 + 0.8, oy - 1.4)):
        b.px(x, y, 'I')
    # nariz: ponta e sombra embaixo
    b.tom_em(cx + 4.4, cy + 2.2, PELE, 2)
    b.tom_em(cx + 3.8, cy + 3.0, PELE, 3)
    # boca: sorriso de canto (sobe para o lado de trás do rosto)
    if tipo == 'feliz':
        b.px(cx + 1.8, cy + 4.0, 'q'); b.px(cx + 2.8, cy + 4.6, 'n'); b.px(cx + 3.8, cy + 4.2, 'q')
    else:
        b.px(cx + 1.8, cy + 4.0, 'q'); b.px(cx + 2.8, cy + 4.6, 'q'); b.px(cx + 3.8, cy + 4.6, 'q')
    b.tom_em(cx + 0.4, cy + 5.4, PELE, 3)       # sombra do queixo
    b.tom_em(cx + 1.4, cy + 6.0, PELE, 2)
    b.tom_em(cx - 0.4, cy + 2.6, PELE, 2)       # maçã do rosto (rosto mais anguloso)


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


def aterrissagem():
    """Toca o chão: joelhos dobram, corpo baixa e inclina, braços abrem para equilibrar (amassa e estica)."""
    return pose(hy=37.0, tronco=14, cabeca=-4, coxa_f=48, joelho_f=82, pe_f=-6, coxa_t=10, joelho_t=70, pe_t=-10,
                   ombro_f=-70, cotovelo_f=30, ombro_t=70, cotovelo_t=20, vento=0.4, fase=5.0, mao_f='aberta',
                   rosto='esforco', saia=0.4)


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
    'piscando': dict(parado(1), rosto='piscando'), 'aterrissando': aterrissagem(),
}
ORDEM = list(QUADROS_POSES.keys())

# Animações (nome: quadros, quadros por segundo, repetição). O Preload lê isto direto.
ANIMACOES = {
    # parado: respira 2 vezes e pisca
    'parado': (['parado1', 'parado2', 'parado3', 'parado4', 'parado1', 'parado2', 'parado3', 'parado4', 'piscando'], 4, -1),
    'correndo': ([f'correndo{i + 1}' for i in range(8)], 16, -1),
    'pulando': (['pulando1', 'pulando2'], 8, 0),
    'caindo': (['caindo1', 'caindo2'], 6, -1),
    'arremessando': (['arremessando1', 'arremessando2', 'arremessando3'], 16, 0),
    'dano': (['dano'], 1, 0),
    'sentado': (['sentado1', 'sentado2', 'sentado3'], 8, -1),
    # aterrissagem: o corpo amassa ao tocar o chão (Jogador.js toca por um instante ao pousar)
    'aterrissando': (['aterrissando'], 10, 0),
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
        'Quadros de 48x64 (corpo de ~58 px). Versão 2: corpo esguio, colete verde aberto, calça larga lilás que',
        'esvoaça, faixa rosa na cabeça e na cintura, sandálias, piscada no parado e quadro de aterrissagem. Sem nada do',
        'design da Disney (regra 3). Será ajustado quando chegarem as fotos do figurino (references/figurinos/).',
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
