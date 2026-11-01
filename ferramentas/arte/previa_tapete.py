"""Prévia do voo do tapete sobre Itajubá (Fase 4): Hotel Coroados no alto do morro, UNIFEI, prédios da cidade,
Serra da Mantiqueira ao fundo, tucanos e maritacas.

Uso: python3 ferramentas/arte/previa_tapete.py [repo]
Saída (só prévia; nada em src/): ferramentas/arte/previas/tapete/
  tapete-panorama.png   trecho do voo em sequência (2x)
  tapete-telas.png      4 telas de 480x270 do jogo (2x)
  aves.png              tucano e maritaca, 2 quadros de asa cada (6x)
  nativo/*.png          cada peça em 1x

Escala da fase (src/scenes/Tapete.js): telhados mais próximos em y = 228, tapete entre y = 44 e 196,
câmera a 96 px/s. Camadas: céu, serra (0,15), morro do Coroados e cidade (0,35), telhados e UNIFEI (1).
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerar_lugares as GL  # noqa: E402
from cenario import M, MATERIAIS, Tela, largura_texto  # noqa: E402
from previa_elenco import carregar_sprites  # noqa: E402

REPO = GL.REPO
SAIDA = os.path.join(REPO, 'ferramentas', 'arte', 'previas', 'tapete')
NATIVO = os.path.join(SAIDA, 'nativo')
L_TELA, A_TELA = 480, 270
TELHADOS_Y = 228
AR = '#B89AD8'   # cor do ar para as camadas de longe


def palmeira(t, x, yb, h, mat_folha=None):
    """Palmeira imperial: tronco fino claro e leque de folhas no alto."""
    mf = mat_folha or M['folha']
    tr = M['concreto']
    t.ret(x, yb - h, x + 1, yb, tr, 2)
    t.vlinha(x, yb - h, yb, tr, 1)
    t.ret(x - 1, yb - h + 2, x + 2, yb - h + 5, M['folha'], 3)        # capitel verde
    for ang, comp in ((-160, 9), (-130, 10), (-95, 7), (-60, 10), (-25, 9), (-200, 6), (20, 6)):
        a = math.radians(ang)
        for k in range(comp):
            xx = x + 0.5 + math.cos(a) * k
            yy = yb - h + math.sin(a) * k + (k * k) / (comp * 1.6)  # folha caindo na ponta
            t.px(xx, yy, mf, 1 if k < comp // 2 else 2)
            t.px(xx, yy + 1, mf, 3)


# ---------------------------------------------------------------------------------------------------------------
# Hotel Coroados: prédio comprido de 2 andares, branco com faixas e pilares vermelhos, telhado de barro com
# placas escuras, bloco do meio com o letreiro HOTEL COROADOS, palmeiras na frente. Fica no alto de um morro.
# ---------------------------------------------------------------------------------------------------------------

def hotel():
    L, A = 220, 52
    t = Tela(L, A, semente=101)
    br, vm, tl = M['branco'], M['vermelho'], M['telha']
    base = A - 1
    for x0, x1, topo in ((2, 70, 22), (150, 217, 22), (70, 150, 12)):
        t.parede(x0, topo, x1, base - 2, br, 1)
        # telhado de barro em águas baixas, com placas solares escuras
        t.poli([(x0 - 2, topo), (x0 + 4, topo - 5), (x1 - 4, topo - 5), (x1 + 2, topo)], tl, 2)
        t.hlinha(x0 + 4, x1 - 4, topo - 5, tl, 1)
        for y in range(topo - 4, topo):
            for x in range(x0, x1):
                if t.mat[y, x] == tl and (x + y) % 4 == 0:
                    t.px(x, y, tl, 3)
        for px_ in range(x0 + 8, x1 - 8, 22):
            t.ret(px_, topo - 4, px_ + 5, topo - 2, M['preto'], 2)
            t.hlinha(px_, px_ + 5, topo - 4, M['preto'], 0)
        # faixas vermelhas nas lajes e no beiral
        t.ret(x0, topo, x1, topo + 1, vm, 2)
        t.hlinha(x0, x1, topo, vm, 1)
        for yf in range(topo + 11, base - 2, 11):
            t.ret(x0, yf, x1, yf + 1, vm, 2)
            t.hlinha(x0, x1, yf, vm, 1)
        # janelas em fita
        for yj in range(topo + 4, base - 4, 11):
            for xj in range(x0 + 3, x1 - 4, 7):
                t.ret(xj, yj, xj + 4, yj + 3, M['vidro_escuro'], 2)
                t.hlinha(xj, xj + 4, yj, M['vidro_escuro'], 0)
        # pilares vermelhos
        for xp in range(x0, x1 + 1, 20):
            t.ret(xp, topo, xp + 2, base, vm, 2)
            t.vlinha(xp, topo, base, vm, 1)
            t.vlinha(xp + 2, topo, base, vm, 3)
    # letreiro do bloco do meio
    t.ret(76, 13, 144, 21, br, 0)
    t.hlinha(76, 144, 21, br, 2)
    txt = 'HOTEL COROADOS'
    t.texto(int(110 - largura_texto(txt) / 2), 15, txt, vm, 2)
    # sombra da varanda / garagem embaixo
    t.ret(2, base - 2, 217, base, M['interior'], 3)
    for x in range(10, 212, 23):
        t.ret(x, base - 2, x + 6, base, M['grafite'], t.rnd.choice((1, 2)))  # carros estacionados
    for x in (36, 60, 160, 178, 196, 206):
        palmeira(t, x, base, 26)
    t.contorno()
    return t.imagem()


def morro_coroados(w=420, h=230):
    """Morro alto e verde com mata no topo, encosta de pasto e um barranco de terra vermelha; o hotel em cima."""
    a = np.zeros((h, w, 4), np.uint8)
    rnd = np.random.RandomState(31)
    cx = w / 2
    topo_y = 56

    plato = 122   # meia largura do topo plano: o hotel (220 px) fica todo apoiado no morro, sem flutuar

    def perfil(x):
        d = max(0, abs(x - cx) - plato) / (w / 2 - plato)
        return topo_y + (h - topo_y) * min(1, d ** 1.25) + 2 * math.sin(x / 9)

    pasto = ['#C6E08E', '#A8CC78', '#8CB466', '#729A58']
    for x in range(w):
        y = int(perfil(x))
        a[y:, x, :3] = GL.hex_rgb(pasto[1] if x < cx else pasto[2])
        a[y:, x, 3] = 255
    mata = ['#9CC88A', '#6FA460', '#4F8650', '#3A6844']
    # mata atrás do hotel e nas laterais
    for _ in range(260):
        x = rnd.uniform(0, w)
        y = perfil(x) + rnd.uniform(-2, 30) if abs(x - cx) > plato - 10 else perfil(x) + rnd.uniform(-14, 4)
        GL._copinha(a, x, y, rnd.uniform(3.5, 6), mata)
    for _ in range(70):  # arbustos no pasto
        x = rnd.uniform(40, w - 40)
        y = rnd.uniform(perfil(x) + 40, h)
        GL._copinha(a, x, y, rnd.uniform(2, 3.5), mata)
    # barranco de terra vermelha
    terra = [GL.hex_rgb(c) for c in ('#E89A70', '#C8684A', '#A04A38')]
    for y in range(topo_y - 6, topo_y + 6):
        for x in range(int(cx + 30), int(cx + 66)):
            if a[y, x, 3] and rnd.rand() < 0.9:
                a[y, x, :3] = terra[(x + y) % 3 if y > topo_y - 3 else 0]
    img = Image.fromarray(a, 'RGBA')
    ho = hotel()
    img.alpha_composite(ho, (int(cx - ho.width / 2), topo_y + 16 - ho.height))
    return img


# ---------------------------------------------------------------------------------------------------------------
# UNIFEI: dois blocos brancos com janelas em fita, torre de vidro azul curva no meio coroada pela faixa azul com
# UNIFEI em branco; na frente, as letras grandes UNIFEI no gramado e palmeiras.
# ---------------------------------------------------------------------------------------------------------------

def unifei():
    L, A = 196, 150
    t = Tela(L, A, semente=202)
    br, va = M['branco'], M['vidro_azul']
    base = A - 1
    gram = base - 10
    # blocos brancos
    for x0, x1, lado in ((14, 74, -1), (122, 182, 1)):
        t.parede(x0, 30, x1, gram, br, 1)
        if lado > 0:
            t.ret(x1 - 14, 30, x1, gram, br, 2)
        else:
            t.ret(x0, 30, x0 + 10, gram, br, 0)
        t.ret(x0 - 1, 28, x1 + 1, 30, br, 0)
        t.hlinha(x0 - 1, x1 + 1, 30, br, 3)
        for andar, y in enumerate(range(38, gram - 8, 14)):
            for xj in range(x0 + 4, x1 - 6, 11):
                t.ret(xj, y, xj + 7, y + 5, M['vidro_escuro'], 2)
                t.hlinha(xj, xj + 7, y, M['vidro_escuro'], 0)
                t.px(xj + 1, y + 1, M['vidro_escuro'], 1)
        t.manchas(x0, 32, x1, gram, br, 10, tam=(3, 8))
    # torre de vidro curva (cilindro azul com caixilhos)
    g0, g1 = 66, 130
    t.cilindro(g0, g1, 18, gram, va)
    for x in range(g0 + 2, g1, 4):
        t.vlinha(x, 18, gram, va, min(4, t.tom[40, x] + 1))
    for y in range(26, gram, 9):
        t.hlinha(g0, g1, y, va, 4)
    for k in range(0, 60):  # reflexo do céu em diagonal
        x = g0 + 12 + k // 3
        y = 30 + k
        if y < gram and x < g1:
            t.px(x, y, va, 0)
            t.px(x + 1, y, va, 1)
    # coroa azul curva com o nome
    t.elipse((g0 + g1) / 2, 18, (g1 - g0) / 2 + 4, 6, M['azul'], 2)
    t.ret(g0 - 4, 10, g1 + 4, 20, M['azul'], 2)
    t.aplicar(t.mascara_elipse((g0 + g1) / 2, 10, (g1 - g0) / 2 + 4, 4), M['azul'], 1)
    t.hlinha(g0 - 4, g1 + 4, 20, M['azul'], 4)
    txt = 'UNIFEI'
    t.texto(int((g0 + g1) / 2 - largura_texto(txt)), 11, txt, br, 0, escala=2)
    # gramado e letras grandes UNIFEI na frente
    t.ret(0, gram + 1, L - 1, base, M['grama'], 2)
    t.hlinha(0, L - 1, gram + 1, M['grama'], 1)
    t.manchas(0, gram + 2, L - 1, base, M['grama'], 30, tam=(2, 5))
    xx = 34
    for ch in 'UNIFEI':   # letras de concreto com volume: lado de trás 2 px à direita, na sombra
        t.texto(xx + 2, base - 18, ch, br, 3, escala=3)
        t.texto(xx, base - 19, ch, br, 1, escala=3)
        xx += (len(GL_fonte(ch)[0]) + 1) * 3 + 3
    for xp in (6, 186):
        palmeira(t, xp, gram + 2, 40)
    t.contorno()
    return t.imagem()


def GL_fonte(ch):
    from cenario import FONTE
    return FONTE[ch]


def predio(semente, w, h):
    """Prédio de apartamentos do centro de Itajubá (camada da cidade, ao longe)."""
    from cenario import material, rampa
    rnd = np.random.RandomState(semente)
    cor = ['#F2EAD8', '#E8D8C0', '#D8DCE4', '#EFD6C8'][semente % 4]
    pm = material('predio' + cor, rampa(cor))
    t = Tela(w + 2, h + 2, semente=semente)
    t.parede(1, 4, w, h, pm, 1)
    t.ret(w - 5, 4, w, h, pm, 2)
    t.ret(0, 1, w + 1, 4, pm, 0)
    for y in range(8, h - 2, 6):
        for x in range(4, w - 3, 5):
            t.ret(x, y, x + 2, y + 2, M['vidro_escuro'], 2 if rnd.rand() < 0.8 else 0)
        if rnd.rand() < 0.5:
            t.hlinha(2, w - 1, y + 4, pm, 3)                       # sacadas
    t.contorno()
    return t.imagem()


def cidade(w, semente=4):
    """Itajubá vista do alto, ao longe: casario e prédios, pé escondido atrás dos telhados de perto."""
    img = Image.new('RGBA', (w, A_TELA), (0, 0, 0, 0))
    rnd = np.random.RandomState(semente)
    x = 0
    base = 236
    while x < w:
        if rnd.rand() < 0.35:
            p = predio(int(rnd.randint(0, 999)), int(rnd.choice([14, 18, 22])), int(rnd.randint(40, 80)))
        else:
            p = GL.casa(int(rnd.randint(0, 999)), int(rnd.choice([32, 40])), int(rnd.choice([40, 48])))
        img.alpha_composite(p, (x, base - p.height))
        x += p.width - 2 + int(rnd.randint(0, 8))
    return img


# ---------------------------------------------------------------------------------------------------------------
# Aves: tucano-toco e maritaca, 2 quadros (asa para cima / para baixo), voando para a esquerda (contra o tapete)
# ---------------------------------------------------------------------------------------------------------------

def tucano(asa_cima):
    t = Tela(36, 24, semente=5)
    pr, bc = M['preto'], M['branco']
    t.poli([(25, 8), (32, 9), (32, 14), (25, 15)], pr, 3)             # cauda curta e larga
    t.elipse(19, 11.5, 7.5, 5.5, pr, 2)                                # corpo
    t.aplicar(t.mascara_elipse(19, 9, 7, 2.5) & (t.mat == pr), pr, 1)
    t.ret(24, 14, 26, 15, M['vermelho'], 2); t.px(24, 14, M['vermelho'], 1)     # vermelho sob a cauda
    t.elipse(12, 8, 4.5, 4.5, pr, 2)                                   # cabeça
    t.elipse(11.5, 11.5, 3.5, 3, bc, 1)                                # papo branco
    t.aplicar(t.mascara_elipse(12, 13, 3, 1.5) & (t.mat == bc), M['amarelo'], 1)
    t.elipse(11, 7, 1.8, 1.8, M['azul'], 1)                            # pele azul em volta do olho
    t.px(11, 7, pr, 4)
    # bico enorme: amarelo em cima, laranja embaixo, ponta preta
    t.poli([(9, 4.5), (3, 5.5), (0, 8), (2, 10), (9, 10.5)], M['laranja'], 2)
    t.aplicar(t.mascara_ret(0, 4, 9, 6) & (t.mat == M['laranja']), M['laranja'], 1)
    t.aplicar(t.mascara_ret(0, 8, 9, 10) & (t.mat == M['laranja']), M['laranja'], 3)
    t.aplicar(t.mascara_ret(0, 4, 2, 11) & (t.mat == M['laranja']), pr, 2)
    t.hlinha(3, 8, 8, M['laranja'], 4)
    if asa_cima:
        t.poli([(15, 8), (20, 0), (25, 1), (23, 9)], pr, 1)
        t.linha(17, 7, 21, 1, pr, 0)
    else:
        t.poli([(15, 12), (18, 21), (23, 20), (23, 12)], pr, 3)
        t.linha(17, 13, 19, 20, pr, 2)
    t.contorno()
    return t.imagem()


def maritaca(asa_cima):
    t = Tela(30, 16, semente=6)
    vd = M['folha']
    t.poli([(15, 6.5), (25, 8.5), (25, 9.5), (15, 10)], vd, 2)          # cauda pontuda
    t.elipse(11, 8, 6, 3.6, vd, 1)                                     # corpo
    t.elipse(6, 6.5, 3.2, 3, vd, 1)                                    # cabeça
    t.aplicar(t.mascara_elipse(11, 10, 5, 1.6) & (t.mat == vd), vd, 2)
    t.px(5, 6, M['branco'], 0); t.px(5, 5, M['branco'], 1)             # anel branco do olho
    t.px(4, 6, M['preto'], 4)
    t.poli([(3, 5), (0.5, 6.5), (2, 8.5), (3.5, 8)], M['granito'], 1)  # bico claro
    if asa_cima:
        t.poli([(9, 6), (13, 0), (17, 1), (14, 7)], vd, 0)
        t.linha(13, 1, 15, 6, vd, 2)
    else:
        t.poli([(9, 9), (12, 15), (16, 14), (15, 9)], vd, 2)
        t.px(12, 10, M['vermelho'], 2); t.px(13, 11, M['vermelho'], 1)  # vermelho sob a asa
    t.contorno()
    return t.imagem()


# ---------------------------------------------------------------------------------------------------------------
# Tapete com o Aladdin e a Tia Paula (sprites atuais do jogo; a Tia Paula do tapete ainda é provisória)
# ---------------------------------------------------------------------------------------------------------------

def tapete_com_passageiros():
    d = carregar_sprites()
    tp = d['tapete']['SPRITES']['voo']
    voo = Image.new('RGBA', (tp['largura'], tp['altura']))
    for y, l in enumerate(tp['quadros'][0]):
        for x, c in enumerate(l):
            if c != '.':
                h = d['tapete']['PALETA'][c].lstrip('#')
                voo.putpixel((x, y), tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    j = d['jogador']
    al = Image.new('RGBA', (48, 64))
    for y, l in enumerate(j['QUADROS']['sentado1']):
        for x, c in enumerate(l):
            if c != '.':
                h = j['PALETA'][c].lstrip('#')
                al.putpixel((x, y), tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    out = Image.new('RGBA', (80, 90))
    cx, cy = 40, 60   # centro do container
    out.alpha_composite(voo, (cx - 32, cy - 24))
    out.alpha_composite(al, (cx + 12 - 24, cy + 15 - 64))
    return out, (cx, cy)


def sol(img, x, y, r=26):
    d = ImageDraw.Draw(img)
    for rr, c in ((r + 10, '#FBD6C8'), (r + 5, '#FCE2C0'), (r, '#FFF2B0'), (r - 6, '#FFF8D0')):
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=c)


CEU_CREPUSCULO = ['#2E2A66', '#383274', '#443A84', '#544292', '#6A4A9E', '#8652A4', '#A65AA4', '#C8649C',
                  '#E2748E', '#F2887E', '#F9A070']
LUZ_JANELA = ['#FFF2B0', '#FFD878', '#F2B050']


def ceu_crepusculo(w):
    """Crepúsculo: o sol já se pôs atrás da serra; brilho laranja no horizonte, azul-violeta em cima, estrelas."""
    a = np.zeros((A_TELA, w, 4), np.uint8)
    c = CEU_CREPUSCULO
    for y in range(A_TELA):
        for xb in range(0, w, 8):
            f = y / 200 + (0.012 if (xb // 8) % 2 else 0)
            a[y, xb:xb + 8, :3] = GL.hex_rgb(c[min(len(c) - 1, int(f * len(c)))])
    a[:, :, 3] = 255
    img = Image.fromarray(a, 'RGBA')
    d = ImageDraw.Draw(img)
    rnd = np.random.RandomState(8)
    for _ in range(w // 12):
        x, y = rnd.randint(0, w), rnd.randint(2, 80)
        d.point((x, y), fill='#FFF6D8' if rnd.rand() < 0.4 else '#B8A8F0')
    for _ in range(w // 160):
        x, y = rnd.randint(0, w), rnd.randint(6, 60)
        d.line([(x - 2, y), (x + 2, y)], fill='#FFF6D8'); d.line([(x, y - 2), (x, y + 2)], fill='#FFF6D8')
    for _ in range(max(2, w // 300)):   # nuvens finas com a barriga laranja (última luz do sol)
        x, y = rnd.randint(-40, w), rnd.randint(70, 130)
        cw = rnd.randint(60, 120)
        d.rectangle([x, y, x + cw, y + 1], fill='#8A5AA8')
        d.rectangle([x + 6, y + 2, x + cw - 8, y + 3], fill='#F2A07A')
    return img


def acender_janelas(img, cor_ar, forca, chance=0.55, semente=1):
    """Crepúsculo: puxa a camada para a cor do ar e acende parte das janelas de vidro (amarelo quente, sem o
    tingido). A escolha é por janela (bloco de 6x7 px), para a janela acender inteira."""
    a0 = np.array(img)
    alvo = set()
    for nome in ('vidro', 'vidro_escuro'):
        for cor in MATERIAIS[nome][1][:5]:
            alvo.add(GL.hex_rgb(cor))
    a = np.array(GL.tingir(img, cor_ar, forca))
    rnd = np.random.RandomState(semente)
    liga = {}
    ys, xs = np.nonzero(a0[:, :, 3])
    for y, x in zip(ys, xs):
        if tuple(a0[y, x, :3]) in alvo:
            k = (x // 6, y // 7)
            if k not in liga:
                liga[k] = rnd.rand() < chance
            if liga[k]:
                tom = 0 if (y % 7) < 2 else 1 if (x % 6) < 3 else 2
                a[y, x, :3] = GL.hex_rgb(LUZ_JANELA[tom])
    return Image.fromarray(a, 'RGBA')


def panorama(W=3000):
    img = ceu_crepusculo(W)
    img.alpha_composite(GL.tingir(GL.morros(W), '#3A3070', 0.40))
    meio = Image.new('RGBA', (W, A_TELA), (0, 0, 0, 0))
    mc = morro_coroados()
    meio.alpha_composite(mc, (790, A_TELA - mc.height + 30))
    img.alpha_composite(acender_janelas(meio, '#4A3A80', 0.32, 0.7, 2))
    img.alpha_composite(acender_janelas(cidade(W), '#4A3A80', 0.38, 0.5, 3))
    perto = Image.new('RGBA', (W, A_TELA), (0, 0, 0, 0))
    perto.alpha_composite(GL.casario(W, semente=9, base=312))
    un = unifei()
    perto.alpha_composite(un, (1900, A_TELA - un.height))
    img.alpha_composite(acender_janelas(perto, '#4A3A80', 0.22, 0.45, 4))
    # aves: bandos de maritacas e tucanos em alturas diferentes
    tc = [tucano(True), tucano(False)]
    mt = [maritaca(True), maritaca(False)]
    for x, y, k in ((420, 70, 0), (1240, 120, 1), (2240, 60, 0), (2700, 140, 1)):
        img.alpha_composite(tc[k], (x, y))
    for x0, y0 in ((700, 140), (1600, 80), (2550, 100)):
        for i in range(5):
            img.alpha_composite(mt[i % 2], (x0 + i * 22 + (i % 2) * 6, y0 + (i % 3) * 9 - i * 2))
    tap, _ = tapete_com_passageiros()
    marcas = {}
    for nome, x, y in (('inicio', 80, 90), ('coroados', 880, 150), ('unifei', 1780, 50), ('aves', 2480, 80)):
        img.alpha_composite(tap, (x, y))
        marcas[nome] = x + 40
    return img, marcas


def telas(pan, marcas):
    k, gap, topo = 2, 16, 40
    ordem = [('inicio', 'Saindo do Espaço: telhados de Itajubá e a serra'),
             ('coroados', 'Hotel Coroados no alto do morro'),
             ('unifei', 'Passando pela UNIFEI'), ('aves', 'Tucanos e maritacas no caminho')]
    W = 2 * L_TELA * k + 3 * gap
    H = 2 * (A_TELA * k + topo + gap) + 60
    out = Image.new('RGBA', (W, H), (34, 26, 48, 255))
    d = ImageDraw.Draw(out)
    GL.rotulo(d, (gap, 14), 'Fase 4 · voo do tapete sobre Itajubá (480×270, ampliado 2×)', 24)
    for i, (nome, titulo) in enumerate(ordem):
        x0 = max(0, min(pan.width - L_TELA, marcas[nome] - 120))   # o tapete fica no x 120 da tela
        crop = pan.crop((x0, 0, x0 + L_TELA, A_TELA)).resize((L_TELA * k, A_TELA * k), Image.NEAREST)
        X = gap + (i % 2) * (L_TELA * k + gap)
        Y = 60 + (i // 2) * (A_TELA * k + topo + gap)
        GL.rotulo(d, (X, Y + 4), f'{i + 1}. {titulo}', 22, (255, 214, 251))
        out.alpha_composite(crop, (X, Y + topo))
    return out


def prancha_aves():
    k = 6
    ims = [tucano(True), tucano(False), maritaca(True), maritaca(False)]
    W = sum(i.width * k + 30 for i in ims) + 30
    out = Image.new('RGBA', (W, 24 * k + 110), (34, 26, 48, 255))
    d = ImageDraw.Draw(out)
    GL.rotulo(d, (20, 14), 'Aves do voo: tucano-toco e maritaca (2 quadros de asa cada, ampliado 6×)', 22)
    x = 30
    for im, nome in zip(ims, ['tucano · asa em cima', 'tucano · asa embaixo', 'maritaca · asa em cima',
                              'maritaca · asa embaixo']):
        fundo = Image.new('RGBA', (im.width * k, im.height * k), (158, 158, 255, 255))
        fundo.alpha_composite(im.resize((im.width * k, im.height * k), Image.NEAREST))
        out.alpha_composite(fundo, (x, 56))
        GL.rotulo(d, (x, 56 + im.height * k + 8), nome, 16, (220, 205, 240), False)
        x += im.width * k + 30
    return out


if __name__ == '__main__':
    os.makedirs(NATIVO, exist_ok=True)
    for nome, f in (('hotel-coroados', hotel), ('morro-coroados', morro_coroados), ('unifei', unifei),
                    ('tucano', lambda: tucano(True)), ('maritaca', lambda: maritaca(True))):
        f().save(os.path.join(NATIVO, nome + '.png'))
    pan, marcas = panorama()
    pan.resize((pan.width * 2, pan.height * 2), Image.NEAREST).save(os.path.join(SAIDA, 'tapete-panorama.png'))
    telas(pan, marcas).save(os.path.join(SAIDA, 'tapete-telas.png'))
    prancha_aves().save(os.path.join(SAIDA, 'aves.png'))
    print('ok', SAIDA)
