"""(Herói antigo, substituído por gerar_heroi16.py; este arquivo hoje gera só os NPCs.)
Gera o herói do ITAMANIA (Geraldo e Helena, criança) com o renderizador de volumes (modelo.py).

Design próprio (DESIGN.md, "Personagens"): criança recém-chegada a Itajubá, com mochila e tênis. Mesmo corpo e
mesmas animações para os dois; mudam o cabelo e as cores da roupa. O boné amarelo só aparece da fase 3 em diante,
então cada quadro sai em duas versões: sem boné e com boné.

Dois tamanhos (mesmo desenho, proporções escaladas):
- normal: corpo de ~46 px (17% da tela de 270);
- turbinado (café com leite): corpo de ~58 px (21%), aguenta um toque a mais.

Saída: public/assets/sprites/heroi-<nome>-<tamanho>.png (quadros de 48x64 lado a lado; a ordem e as animações ficam em
src/art/heroi.js) e prévia em ferramentas/arte/previas/heroi.png.
Uso: python3 ferramentas/arte/gerar_heroi.py   (rodar dentro de itamania/)
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modelo import Boneco, Material, paleta_de, ponto, mistura  # noqa: E402
from pixel import rgb  # noqa: E402

L, A = 48, 64

PELE = Material('pele', 'AsSzZ', ['#F8D2AE', '#E3A982', '#BC7A56', '#8A4E34', '#4E2818'], (0.78, 0.42, 0.10))
BRANCO = Material('branco', 'WwvVQ', ['#FFFFFF', '#E9ECF6', '#BCC2DA', '#8A90B0', '#4A4E6C'], (0.85, 0.5, 0.15))
OURO = Material('bone', 'YyxXT', ['#FFF6A8', '#FFD43A', '#E09A12', '#A86408', '#5A3204'], (0.72, 0.40, 0.12))
JEANS = Material('jeans', 'JjiIK', ['#8FB6F0', '#4F7FC9', '#335AA0', '#22386E', '#121C3E'], (0.86, 0.50, 0.16))

# Cada herói: cabelo, camiseta, mochila, tênis. Cores escolhidas para ler bem sobre o céu e o casario.
HEROIS = {
    'geraldo': dict(
        cabelo=['#7A5A48', '#4A3226', '#2E1E16', '#1C110C', '#10080A'],
        camiseta=['#B6F0A0', '#5CC24A', '#3A8E34', '#235E26', '#123818'],   # verde
        mochila=['#FFC08A', '#F2803A', '#C2541E', '#86340E', '#4A1A06'],     # laranja
        tenis=['#FF9AA0', '#E2444E', '#AE2432', '#741420', '#40080E'],       # vermelho
        estilo='curto'),
    'helena': dict(
        cabelo=['#9A6A4E', '#5E3A28', '#3E2418', '#28140C', '#160A06'],
        camiseta=['#FFC6E4', '#F07AB4', '#C44C8C', '#8C2C62', '#4C1234'],   # rosa
        mochila=['#B8E8FF', '#4AB0E8', '#2A7CBC', '#1A5084', '#0C2A48'],     # azul
        tenis=['#E0D2FF', '#9A7EF0', '#6E52C8', '#46308E', '#22144C'],       # lilás
        estilo='rabo'),
}

TAMANHOS = {'normal': 0.90, 'turbinado': 1.10}


def materiais(h):
    cab = Material('cabelo', 'HhgGE', h['cabelo'], (0.80, 0.50, 0.22))
    cam = Material('camiseta', 'CcbBN', h['camiseta'], (0.86, 0.50, 0.16))
    moc = Material('mochila', 'MmnRU', h['mochila'], (0.80, 0.46, 0.14))
    ten = Material('tenis', 'FfdDO', h['tenis'], (0.80, 0.46, 0.14))
    return cab, cam, moc, ten


EXTRAS = {'o': '#FFFFFF', 'e': '#1E1018', 'q': '#8E3A34', 'r': '#F08A8A'}


def pose(hx=23.0, hy=33.0, tronco=4.0, cabeca=0.0,
         coxa_f=0.0, joelho_f=0.0, pe_f=0.0, coxa_t=0.0, joelho_t=0.0, pe_t=0.0,
         ombro_f=-8.0, cotovelo_f=20.0, ombro_t=10.0, cotovelo_t=25.0,
         vento=0.0, fase=0.0, rosto='normal', mao_f='aberta', mao_t='aberta'):
    return dict(locals())


def desenhar(p, h, s, bone):
    """p = pose, h = herói, s = escala, bone = com boné."""
    CAB, CAM, MOC, TEN = materiais(h)
    b = Boneco(L, A)
    COXA, CANELA = 10.0 * s, 9.5 * s
    BRACO, ANTEBRACO = 7.0 * s, 6.6 * s
    COLUNA = 11.5 * s
    hx, hy = p['hx'], 36.0 + (p['hy'] - 33.0) * s
    incl = p['tronco']
    vento = p['vento']
    pescoco = ponto((hx, hy), COLUNA, 180 - incl)
    cab = ponto(pescoco, 6.4 * s, 180 - incl * 0.6 - p['cabeca'])
    ombro_t = (pescoco[0] + 1.6 * s, pescoco[1] + 2.0 * s)
    ombro_f = (pescoco[0] - 1.6 * s, pescoco[1] + 2.4 * s)
    quadril_t = (hx + 1.4 * s, hy)
    quadril_f = (hx - 1.0 * s, hy + 0.4 * s)

    def braco(ombro, ang, dobra, esc, mao_tipo):
        cot = ponto(ombro, BRACO, ang)
        mao = ponto(cot, ANTEBRACO, ang + dobra)
        b.capsula(ombro, cot, 1.8 * s, 1.6 * s, PELE, esc)
        b.capsula(cot, mao, 1.6 * s, 1.4 * s, PELE, esc)
        # manga curta da camiseta
        b.capsula(ombro, mistura(ombro, cot, 0.55), 2.5 * s, 2.3 * s, CAM, esc)
        m2 = ponto(mao, 1.0 * s, ang + dobra)
        b.elipse(m2, 1.9 * s, 2.0 * s, PELE, esc)

    def perna(quadril, coxa, joelho, pe_ang, esc):
        j = ponto(quadril, COXA, coxa)
        t = ponto(j, CANELA, coxa - joelho)
        ang_pe = coxa - joelho + 90 - pe_ang
        b.capsula(j, t, 2.0 * s, 1.7 * s, JEANS if h.get('calca') == 'longa' else PELE, esc)   # canela
        b.capsula(quadril, j, 3.3 * s, 3.0 * s, JEANS, esc, achatar=0.9)              # bermuda
        b.capsula(mistura(quadril, j, 0.6), mistura(j, t, 0.12), 3.2 * s, 3.0 * s, JEANS, esc, achatar=0.9)
        b.capsula(ponto(t, 1.6 * s, coxa - joelho + 180), t, 1.8 * s, 1.8 * s, BRANCO, esc, pontas=False)  # meia
        # tênis: corpo colorido e sola branca, maior que o pé (tênis de criança)
        ponta = ponto(t, 4.6 * s, ang_pe)
        b.capsula(ponto(t, 1.0 * s, ang_pe + 180), ponta, 2.4 * s, 2.0 * s, TEN, esc, achatar=0.85)
        sola_a = ponto(ponto(t, 1.6 * s, ang_pe + 180), 2.1 * s, ang_pe + 90)
        sola_b = ponto(ponta, 1.6 * s, ang_pe + 90)
        b.capsula(sola_a, sola_b, 0.9 * s, 0.9 * s, BRANCO, esc, separar=False)
        b.tom_em(*mistura(t, ponta, 0.5), BRANCO, 0)                                  # cadarço

    # ---- de trás para a frente ----
    braco(ombro_t, p['ombro_t'], p['cotovelo_t'], 1, p['mao_t'])
    # mochila (nas costas, lado -x)
    costas = ponto(mistura((hx, hy), pescoco, 0.55), 3.4 * s, 180 - incl - 90)
    if h.get('usa_mochila', True):
        b.elipse((costas[0] - 1.2 * s, costas[1]), 3.8 * s, 5.4 * s, MOC, 1, giro=-incl)
        b.elipse((costas[0] - 2.4 * s, costas[1] + 2.4 * s), 2.2 * s, 2.2 * s, MOC, 0, giro=-incl)  # bolso
    perna(quadril_t, p['coxa_t'], p['joelho_t'], p['pe_t'], 1)
    perna(quadril_f, p['coxa_f'], p['joelho_f'], p['pe_f'], 0)
    # tronco (camiseta)
    peito = mistura((hx, hy), pescoco, 0.62)
    b.capsula(peito, (hx, hy - 1.0 * s), 4.1 * s, 3.7 * s, CAM, separar=False, achatar=0.92)
    b.elipse((peito[0] + 0.2 * s, peito[1] - 0.6 * s), 4.2 * s, 3.4 * s, CAM, separar=False, achatar=0.9)
    # barra da camiseta sobre a bermuda
    b.capsula((hx - 3.8 * s, hy - 0.4 * s), (hx + 3.8 * s, hy - 0.8 * s), 1.4 * s, 1.4 * s, CAM, 1, separar=False)
    # alça da mochila passando no ombro da frente
    alca_a = (pescoco[0] - 0.6 * s, pescoco[1] + 1.6 * s)
    alca_b = ponto(alca_a, 7.0 * s, 180 - incl + 180 - 8)
    if h.get('usa_mochila', True):
        b.capsula(alca_a, alca_b, 0.8 * s, 0.8 * s, MOC, 1, separar=False)
    elif h.get('avental'):
        # avental na frente do tronco (cor da mochila)
        b.poligono([(peito[0] + 0.5 * s, peito[1] - 1.5 * s), (peito[0] + 4.2 * s, peito[1] - 1.0 * s),
                    (hx + 4.8 * s, hy + 6.0 * s), (hx + 0.2 * s, hy + 6.0 * s)], MOC, separar=False)
    b.capsula(pescoco, (cab[0] - 0.4, cab[1] + 2.0 * s), 1.9 * s, 1.9 * s, PELE, separar=False)

    # ---- cabeça (criança: cabeça grande) ----
    cx, cy = cab
    sh = s * h.get('cabeca', 1.14)  # cabeça de criança, maior
    cx, cy = cx + 0.4 * sh, cy - 0.8 * sh
    # cabelo de trás
    if h['estilo'] == 'careca':
        for dx, dy, r in ((-3.8, 0.6, 2.4), (-2.6, 2.8, 2.0)):
            b.elipse((cx + dx * sh, cy + dy * sh), r * sh, r * sh, CAB, separar=False)
    elif h['estilo'] == 'coque':
        b.elipse((cx - 3.6 * sh, cy - 4.4 * sh), 2.8 * sh, 2.6 * sh, CAB, 1, separar=False)
        for dx, dy, r in ((-3.4, -0.4, 3.2), (-1.0, -3.4, 3.4), (2.0, -3.8, 2.8), (-4.0, 2.4, 2.4)):
            b.elipse((cx + dx * sh, cy + dy * sh), r * sh, r * sh, CAB, separar=False)
    elif h['estilo'] == 'curto':
        for dx, dy, r in ((-3.4, -0.6, 3.2), (-1.0, -3.4, 3.4), (2.0, -3.8, 2.8), (-4.0, 2.0, 2.4)):
            b.elipse((cx + dx * sh, cy + dy * sh), r * sh, r * sh, CAB, separar=False)
    else:
        # rabo de cavalo que balança atrás (com o vento)
        base = (cx - 4.6 * sh, cy - 2.4 * sh)
        pts, x, y = [base], base[0], base[1]
        for i in range(4):
            a = -30 - vento * 55 + math.sin(p['fase'] + i * 1.1) * (10 + 16 * vento) * (i + 1) / 4
            x, y = ponto((x, y), 2.6 * sh, a)
            pts.append((x, y))
        for i in range(4):
            r = (2.4 - 0.4 * i) * sh
            b.capsula(pts[i], pts[i + 1], r, r * 0.85, CAB, 1)
        for dx, dy, r in ((-3.4, -0.4, 3.4), (-1.0, -3.4, 3.5), (2.0, -3.8, 2.9), (-4.2, 2.6, 2.6)):
            b.elipse((cx + dx * sh, cy + dy * sh), r * sh, r * sh, CAB, separar=False)
    b.elipse((cx + 1.0 * sh, cy + 0.6 * sh), 5.0 * sh, 5.4 * sh, PELE, separar=False, achatar=0.7)   # rosto
    b.elipse((cx - 2.0 * sh, cy + 1.2 * sh), 1.3 * sh, 1.8 * sh, PELE, 1, separar=False, achatar=0.8)  # orelha
    # franja / topo
    if h['estilo'] == 'careca':
        b.tom_em(cx + 1.0 * sh, cy - 3.6 * sh, PELE, 0)
    elif h['estilo'] in ('curto', 'coque'):
        for dx, dy, r in ((0.0, -4.0, 2.6), (2.6, -4.2, 2.3), (4.6, -3.0, 1.5), (-2.4, -3.0, 2.0)):
            b.elipse((cx + dx * sh, cy + dy * sh), r * sh, r * 0.85 * sh, CAB, separar=False)
    else:
        for dx, dy, r in ((0.0, -4.0, 2.7), (2.8, -4.0, 2.5), (4.8, -2.4, 1.7), (-2.4, -3.0, 2.1), (5.0, -0.6, 1.0)):
            b.elipse((cx + dx * sh, cy + dy * sh), r * sh, r * 0.85 * sh, CAB, separar=False)
        b.elipse((cx - 4.6 * sh, cy - 2.4 * sh), 1.2 * sh, 1.2 * sh, CAM, separar=False)  # xuxinha
    if bone:
        # boné amarelo: copa arredondada e aba para a frente
        b.elipse((cx + 0.6 * sh, cy - 3.2 * sh), 5.6 * sh, 3.4 * sh, OURO, separar=False)
        b.capsula((cx + 3.0 * sh, cy - 1.6 * sh), (cx + 8.2 * sh, cy - 1.2 * sh), 1.0 * sh, 0.8 * sh, OURO, 1, separar=False)
        b.tom_em(cx + 0.6 * sh, cy - 6.0 * sh, OURO, 2)   # botão do topo
        b.tom_em(cx - 2.0 * sh, cy - 2.2 * sh, OURO, 2)   # costura
    braco(ombro_f, p['ombro_f'], p['cotovelo_f'], 0, p['mao_f'])
    rosto(b, cx, cy, sh, p['rosto'])
    if h.get('bigode'):
        for dx in (2.0, 3.0, 4.0, 5.0):
            b.px(cx + dx * sh, cy + 3.6 * sh, 'G')
    if h.get('oculos'):
        ox1, ox2, oy = cx + 1.0 * sh, cx + 4.0 * sh, cy + 0.6 * sh
        for x in range(int(round(ox1)) - 1, int(round(ox2)) + 2):
            b.px(x, oy - 1, 'e')
        b.px(ox1 - 1, oy, 'e'); b.px(ox1 - 1, oy + 1, 'e'); b.px(ox1 + 2, oy + 1, 'e')
        b.px(ox1, oy + 2, 'e'); b.px(ox1 + 1, oy + 2, 'e'); b.px(ox2 + 1, oy, 'e'); b.px(ox2 + 1, oy + 1, 'e')
    return b


def rosto(b, cx, cy, s, tipo):
    ox1, ox2, oy = cx + 1.0 * s, cx + 4.0 * s, cy + 0.6 * s
    if tipo == 'dano':
        b.px(ox1, oy - 0.5, 'e'); b.px(ox1 + 1, oy + 0.5, 'e'); b.px(ox1, oy + 1.5, 'e')
        b.px(ox2 + 0.5, oy - 0.5, 'e'); b.px(ox2 - 0.5, oy + 0.5, 'e'); b.px(ox2 + 0.5, oy + 1.5, 'e')
    elif tipo == 'piscando':
        b.px(ox1, oy + 1, 'e'); b.px(ox1 + 1, oy + 1, 'e'); b.px(ox2, oy + 1, 'e')
    else:
        # olhos grandes de criança: 2x3 com brilho
        for dy in (0, 1, 2):
            b.px(ox1, oy + dy, 'o' if dy < 2 else 'e')
            b.px(ox1 + 1, oy + dy, 'e')
        b.px(ox1 + 1, oy, 'o')
        for dy in (0, 1, 2):
            b.px(ox2, oy + dy, 'e')
        b.px(ox2, oy, 'o')
    # bochecha rosada
    b.px(cx + 0.4 * s, cy + 3.4 * s, 'r')
    b.tom_em(cx + 5.6 * s, cy + 2.6 * s, PELE, 2)   # nariz
    if tipo in ('feliz', 'vitoria'):
        b.px(cx + 2.4 * s, cy + 4.4 * s, 'q'); b.px(cx + 3.4 * s, cy + 5.0 * s, 'q'); b.px(cx + 4.4 * s, cy + 4.4 * s, 'q')
    elif tipo == 'esforco':
        b.px(cx + 3.0 * s, cy + 4.6 * s, 'q'); b.px(cx + 4.0 * s, cy + 4.6 * s, 'q')
    elif tipo == 'dano':
        b.px(cx + 3.2 * s, cy + 4.4 * s, 'q'); b.px(cx + 3.2 * s, cy + 5.4 * s, 'q')
    else:
        b.px(cx + 2.6 * s, cy + 4.4 * s, 'q'); b.px(cx + 3.6 * s, cy + 4.8 * s, 'q'); b.px(cx + 4.4 * s, cy + 4.4 * s, 'q')


# ----------------------------------------------------------------------------- poses

def parado(i):
    resp = [0.0, 0.5, 1.0, 0.5][i]
    return pose(hy=33.0 + resp * 0.4, tronco=1.0, cabeca=-1.0 + resp, coxa_f=4, joelho_f=4, coxa_t=-4,
                ombro_f=-6 + resp * 2, cotovelo_f=16, ombro_t=8, cotovelo_t=14, vento=0.05, fase=i * 0.9,
                rosto='feliz')


def correndo(i, n=8):
    f = i / n * 2 * math.pi

    def perna_ang(fase):
        coxa = 38 * math.sin(fase)
        if coxa < 0:
            coxa *= 0.7
        dobra = 16 + 56 * max(0.0, math.sin(fase - 1.7)) ** 1.2 + 10 * max(0.0, -math.sin(fase))
        return coxa, dobra, -10 * math.cos(fase)
    cf, jf, pf = perna_ang(f)
    ct, jt, pt = perna_ang(f + math.pi)
    return pose(hy=34.0 - 1.6 * abs(math.cos(f)), tronco=10, cabeca=-5, coxa_f=cf, joelho_f=jf, pe_f=pf,
                coxa_t=ct, joelho_t=jt, pe_t=pt, ombro_f=-46 * math.sin(f) + 5, cotovelo_f=80,
                ombro_t=46 * math.sin(f) + 5, cotovelo_t=80, vento=1.0, fase=f, rosto='feliz')


def pulando(i):
    if i == 0:
        return pose(hy=30.0, tronco=6, cabeca=-4, coxa_f=72, joelho_f=100, pe_f=10, coxa_t=-20, joelho_t=34, pe_t=-30,
                    ombro_f=-50, cotovelo_f=50, ombro_t=150, cotovelo_t=20, vento=0.7, fase=1.0, rosto='esforco')
    return pose(hy=30.5, tronco=4, cabeca=-2, coxa_f=52, joelho_f=74, coxa_t=10, joelho_t=62, pe_t=-20,
                ombro_f=-36, cotovelo_f=60, ombro_t=150, cotovelo_t=26, vento=0.6, fase=2.0, rosto='feliz')


def caindo(i):
    return pose(hy=30.0, tronco=-1 * i, cabeca=2 + i, coxa_f=30 - 5 * i, joelho_f=40, pe_f=-10, coxa_t=-14,
                joelho_t=36 + 4 * i, pe_t=-25, ombro_f=-112 - 10 * i, cotovelo_f=-25, ombro_t=120 + 10 * i,
                cotovelo_t=-20, vento=0.5, fase=3.5 + i, rosto='normal')


def arremessando(i):
    if i == 0:
        return pose(hy=33.4, tronco=-6, cabeca=2, coxa_f=16, joelho_f=12, coxa_t=-14, joelho_t=6,
                    ombro_f=-120, cotovelo_f=-60, ombro_t=30, cotovelo_t=50, vento=0.3, rosto='esforco')
    if i == 1:
        return pose(hy=34.0, tronco=12, cabeca=-6, coxa_f=24, joelho_f=24, coxa_t=-18, joelho_t=14,
                    ombro_f=96, cotovelo_f=4, ombro_t=-30, cotovelo_t=30, vento=0.5, fase=1.5, rosto='esforco')
    return pose(hy=34.0, tronco=8, cabeca=-3, coxa_f=20, joelho_f=20, coxa_t=-16, joelho_t=10,
                ombro_f=60, cotovelo_f=20, ombro_t=-16, cotovelo_t=40, vento=0.3, fase=2.5, rosto='feliz')


def aterrissagem():
    return pose(hy=36.5, tronco=14, cabeca=-4, coxa_f=50, joelho_f=84, pe_f=-6, coxa_t=10, joelho_t=70, pe_t=-10,
                ombro_f=-70, cotovelo_f=30, ombro_t=70, cotovelo_t=20, vento=0.4, fase=5.0, rosto='esforco')


def dano():
    return pose(hx=24.5, hy=32.0, tronco=-16, cabeca=12, coxa_f=24, joelho_f=40, pe_f=-20, coxa_t=-6, joelho_t=30,
                pe_t=-20, ombro_f=-150, cotovelo_f=-30, ombro_t=150, cotovelo_t=-20, vento=0.6, fase=4.0, rosto='dano')


def vitoria(i):
    return pose(hy=32.0 - i, tronco=-2, cabeca=4, coxa_f=8, joelho_f=10, coxa_t=-8, joelho_t=10,
                ombro_f=-160 + 10 * i, cotovelo_f=-10, ombro_t=165 - 10 * i, cotovelo_t=-10, vento=0.4, fase=i,
                rosto='vitoria')


POSES = {
    'parado1': parado(0), 'parado2': parado(1), 'parado3': parado(2), 'parado4': parado(3),
    'piscando': dict(parado(1), rosto='piscando'),
    **{f'correndo{i + 1}': correndo(i) for i in range(8)},
    'pulando1': pulando(0), 'pulando2': pulando(1), 'caindo1': caindo(0), 'caindo2': caindo(1),
    'arremessando1': arremessando(0), 'arremessando2': arremessando(1), 'arremessando3': arremessando(2),
    'aterrissando': aterrissagem(), 'dano': dano(), 'vitoria1': vitoria(0), 'vitoria2': vitoria(1),
}
NOMES = list(POSES.keys())
ANIMACOES = {
    'parado': (['parado1', 'parado2', 'parado3', 'parado4', 'parado1', 'parado2', 'parado3', 'parado4', 'piscando'], 4, -1),
    'correndo': ([f'correndo{i + 1}' for i in range(8)], 16, -1),
    'pulando': (['pulando1', 'pulando2'], 8, 0),
    'caindo': (['caindo1', 'caindo2'], 6, -1),
    'arremessando': (['arremessando1', 'arremessando2', 'arremessando3'], 16, 0),
    'aterrissando': (['aterrissando'], 10, 0),
    'dano': (['dano'], 1, 0),
    'vitoria': (['vitoria1', 'vitoria2'], 4, -1),
}
CONTORNO_FIXO = {'o': 'Z', 'e': 'Z', 'q': 'Z', 'r': 'Z'}


def gerar_folha(h, s):
    """Devolve a lista de quadros (linhas) e a paleta: primeiro todos sem boné, depois todos com boné."""
    CAB, CAM, MOC, TEN = materiais(h)
    pal = paleta_de([PELE, BRANCO, OURO, JEANS, CAB, CAM, MOC, TEN], EXTRAS)
    quadros = []
    for bone in (False, True):
        qs = {n: desenhar(p, h, s, bone).texto(CONTORNO_FIXO) for n, p in POSES.items()}

        def ultima(linhas):
            return max(y for y, l in enumerate(linhas) if any(c != '.' for c in l))
        desce = A - 1 - ultima(qs['parado1'])
        for n in qs:
            if desce > 0:
                qs[n] = ['.' * L] * desce + qs[n][:A - desce]
        quadros += [qs[n] for n in NOMES]
    return quadros, pal


def png(quadros, pal, caminho):
    from PIL import Image
    img = Image.new('RGBA', (L * len(quadros), A), (0, 0, 0, 0))
    for i, linhas in enumerate(quadros):
        for y, l in enumerate(linhas):
            for x, c in enumerate(l):
                if c != '.':
                    img.putpixel((i * L + x, y), rgb(pal[c]) + (255,))
    img.save(caminho, optimize=True)
    return img


# NPCs adultos (genéricos, sem pessoa real): mesmo renderizador, cabeça proporcional de adulto, sem mochila.
NPCS = {
    'motorista': dict(cabelo=['#5A5A6A', '#36364A', '#24243A', '#18182A', '#0C0C18'],
                      camiseta=['#C6DCFF', '#7AA6F0', '#4C78C8', '#30509A', '#182C5C'],
                      mochila=['#C6DCFF', '#7AA6F0', '#4C78C8', '#30509A', '#182C5C'],
                      tenis=['#7C7888', '#545060', '#3A3644', '#28242F', '#1A1720'],
                      estilo='curto', mochila_=False, calca='longa', cabeca=0.98, bigode=True),
    'guia': dict(cabelo=['#FFFFFF', '#D8D8E4', '#A8A8BC', '#7C7C94', '#4A4A60'],
                 camiseta=['#F6E4B8', '#D8B878', '#B08C4E', '#7E6034', '#46341A'],
                 mochila=['#C8A070', '#A07440', '#784E24', '#503014', '#2C1808'],
                 tenis=['#C98E55', '#955F37', '#6A3D22', '#472513', '#2A1208'],
                 estilo='careca', mochila_=False, calca='longa', cabeca=0.98, oculos=True),
    'vovo': dict(cabelo=['#FFFFFF', '#E4E0EC', '#B8B2C8', '#8A84A0', '#565070'],
                 camiseta=['#E8D0FF', '#B48AF0', '#8460C8', '#5A3C98', '#2E1C58'],
                 mochila=['#E8D0FF', '#B48AF0', '#8460C8', '#5A3C98', '#2E1C58'],
                 tenis=['#F6F0F0', '#DCD2D8', '#B4A8B8', '#86788E', '#4A3E58'],
                 estilo='coque', mochila_=False, calca='longa', cabeca=0.98, oculos=True),
    'vendedora': dict(cabelo=['#3A2A2A', '#24161A', '#160C10', '#0C0608', '#060204'],
                      camiseta=['#FFFFFF', '#E9ECF6', '#BCC2DA', '#8A90B0', '#4A4E6C'],
                      mochila=['#FF9C8C', '#F05A4A', '#CC3530', '#9A2228', '#66161E'],
                      tenis=['#7C7888', '#545060', '#3A3644', '#28242F', '#1A1720'],
                      estilo='rabo', mochila_=False, avental=True, calca='longa', cabeca=0.98),
    'tecnico': dict(cabelo=['#6A4E3A', '#46301E', '#2C1C10', '#1A1008', '#0C0604'],
                    camiseta=['#A8C8FF', '#5A8AE8', '#3460C0', '#244490', '#182C62'],
                    mochila=['#A8C8FF', '#5A8AE8', '#3460C0', '#244490', '#182C62'],
                    tenis=['#C98E55', '#955F37', '#6A3D22', '#472513', '#2A1208'],
                    estilo='curto', mochila_=False, calca='longa', cabeca=0.98),
    'atendente': dict(cabelo=['#8A5A3A', '#5E3A22', '#3E2414', '#28160A', '#140A04'],
                      camiseta=['#FFF0A0', '#FFC845', '#F8941E', '#D0601A', '#963A14'],
                      mochila=['#E0A86C', '#C08A55', '#955F37', '#6A3D22', '#472513'],
                      tenis=['#7C7888', '#545060', '#3A3644', '#28242F', '#1A1720'],
                      estilo='curto', mochila_=False, avental=True, calca='longa', cabeca=0.98),
    'barista': dict(cabelo=['#2E2A3A', '#1C1826', '#100E18', '#08060E', '#040208'],
                    camiseta=['#F4F0EA', '#DCD4D2', '#B4A8B4', '#857792', '#4A3E5A'],
                    mochila=['#B08A6E', '#8A6650', '#664838', '#4A3028', '#30201C'],
                    tenis=['#7C7888', '#545060', '#3A3644', '#28242F', '#1A1720'],
                    estilo='coque', mochila_=False, avental=True, calca='longa', cabeca=0.98),
    'estudante': dict(cabelo=['#3A2418', '#24140C', '#160A06', '#0C0402', '#060200'],
                      camiseta=['#C2EE8E', '#86CC58', '#55A23E', '#3A7634', '#26502C'],
                      mochila=['#7C7888', '#545060', '#3A3644', '#28242F', '#1A1720'],
                      tenis=['#FFFFFF', '#E9ECF6', '#BCC2DA', '#8A90B0', '#4A4E6C'],
                      estilo='curto', calca='longa', cabeca=1.02, oculos=True),
}


def gerar_npcs(pasta):
    """Cada NPC: 2 quadros (parado, falando com a mão levantada), escala de adulto."""
    for nome, h in NPCS.items():
        h = dict(h)
        h['usa_mochila'] = h.pop('mochila_', True)
        CAB, CAM, MOC, TEN = materiais(h)
        pal = paleta_de([PELE, BRANCO, OURO, JEANS, CAB, CAM, MOC, TEN], EXTRAS)
        p1 = dict(parado(0), rosto='normal')
        p2 = dict(parado(2), rosto='feliz', ombro_f=40, cotovelo_f=80)
        qs = [desenhar(p1, h, 1.14, False).texto(CONTORNO_FIXO), desenhar(p2, h, 1.14, False).texto(CONTORNO_FIXO)]
        ultima = max(y for y, l in enumerate(qs[0]) if any(c != '.' for c in l))
        desce = A - 1 - ultima
        qs = [(['.' * L] * desce + q[:A - desce]) if desce > 0 else q for q in qs]
        png(qs, pal, os.path.join(pasta, f'npc-{nome}.png'))


def main():
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    pasta = os.path.join(raiz, 'public/assets/sprites')
    os.makedirs(pasta, exist_ok=True)
    gerar_npcs(pasta)
    # o herói agora vem do desenho do Pedro: ver gerar_heroi16.py


if __name__ == '__main__':
    main()
