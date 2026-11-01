"""Gera a pixel art dos 6 lugares reais da Fase 1 (Itajubá) e as pranchas de prévia.

Uso:  python3 ferramentas/arte/gerar_lugares.py [repo]

Saída (só prévia; nada em src/):
  ferramentas/arte/previas/lugares/nativo/<lugar>.png   arte na resolução do jogo (1 px = 1 px da tela 480x270)
  ferramentas/arte/previas/lugares/<n>-<lugar>.png      prancha: foto de referência × pixel art × Aladdin
  ferramentas/arte/previas/lugares/fase1-panorama.png   tira com os 6 lugares em sequência (2x)
  ferramentas/arte/previas/lugares/fase1-telas.png      6 telas de 480x270 do jogo, uma por lugar (2x)

Fotos em references/lugares/ (ver reference-notes.md). Escala: o herói tem 58 px; chão em y = 240.
Os prédios são comprimidos na altura (convenção do gênero), mas portas e janelas ficam do tamanho do herói ou
maiores, e a igreja e o clube ficam bem mais altos que ele.
"""
import os
import re
import sys
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cenario import M, Tela, largura_texto, mistura, hex_rgb, contar_cores  # noqa: E402
import modelo  # noqa: E402

REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SAIDA = os.path.join(REPO, 'ferramentas', 'arte', 'previas', 'lugares')
NATIVO = os.path.join(SAIDA, 'nativo')
CHAO_Y = 240
TELA_L, TELA_A = 480, 270


# ===============================================================================================================
# 1. Clube Itajubense (camada do fundo, logo no começo da fase)
# ===============================================================================================================

def clube():
    L, A = 264, 178
    t = Tela(L, A, semente=11)
    # Decisão do Pedro (01/11/2026): o clube é todo branco. O rodapé e os pedestais, que na foto são de pedra
    # escura, usam o mesmo branco das molduras (juntas claras, sem veios).
    cr, br, mm = M['creme'], M['branco'], M['branco']
    base = A - 1
    rod = A - 24          # topo do rodapé
    # --- corpo principal ---
    t.parede(4, 40, L - 5, base, cr, 1)
    # sombra na metade direita de cada ala (leve volume) e alas laterais um pouco recuadas
    t.escurecer_ret(L - 12, 40, L - 5, base, 1)
    # --- platibanda (ático) com painéis vazados ---
    t.parede(6, 8, L - 7, 26, cr, 1)
    t.cornija(4, L - 5, 6, br, alt=3, sombra_proj=1)
    for x0 in range(12, L - 16, 22):
        if 92 <= x0 <= 160:
            continue
        t.ret(x0, 13, x0 + 15, 21, cr, 4)          # vão escuro do painel
        t.hlinha(x0, x0 + 15, 13, cr, 4)
        for bx in range(x0 + 2, x0 + 15, 3):       # balaústres
            t.vlinha(bx, 14, 21, br, 2)
            t.px(bx, 14, br, 1)
        t.hlinha(x0, x0 + 15, 22, br, 3)
    # ático central mais alto e liso, com frontão reto
    t.parede(90, 2, 174, 26, cr, 1)
    t.cornija(88, 176, 0, br, alt=3, sombra_proj=1)
    for x0 in (98, 134):
        t.ret(x0, 10, x0 + 31, 20, cr, 3)
        t.relevo(t.mascara_ret(x0, 10, x0 + 31, 20), delta=-1)
    # --- cornija principal com dentículos ---
    t.cornija(0, L - 1, 27, br, alt=5, sombra_proj=0)
    t.dentilhado(2, L - 3, 32, br, passo=3, alt=2)
    t.escurecer_ret(4, 34, L - 5, 35, 1)
    # --- friso com a inscrição ---
    t.ret(4, 36, L - 5, 45, cr, 1)
    t.hlinha(4, L - 5, 36, cr, 3)
    texto = 'CLUB ITAJUBENSE'
    tx = (L - largura_texto(texto)) // 2
    t.texto(tx, 39, texto, cr, 4, sombra=(cr, 0))
    t.cornija(4, L - 5, 46, br, alt=3, sombra_proj=2)   # arquitrave
    # --- bloco central recuado (atrás das colunas) ---
    cx0, cx1 = 92, 172
    t.ret(cx0, 49, cx1, rod - 1, cr, 3)
    t.escurecer_ret(cx0, 49, cx1, 54, 1)
    # --- alas: janelas de cima (quadradas) e de baixo (altas, com bandeira) ---
    alas = [(14, 50), (40, 76), (188, 224), (214, 250)]
    jan_cima = [16, 50, 192, 226]
    for x in jan_cima:
        t.ret(x - 2, 58, x + 21, 60, br, 1)          # verga
        t.relevo(t.mascara_ret(x - 2, 58, x + 21, 60))
        t.janela_grade(x, 61, x + 19, 80, colunas=3, linhas=2)
        t.ret(x - 2, 81, x + 21, 82, br, 2)          # peitoril
        t.escurecer_ret(x - 1, 83, x + 20, 83, 1, so_mat=cr)
    for x in jan_cima:
        t.ret(x - 3, 92, x + 22, 95, br, 1)          # cornija da janela de baixo
        t.relevo(t.mascara_ret(x - 3, 92, x + 22, 95))
        t.escurecer_ret(x - 2, 96, x + 21, 96, 1, so_mat=cr)
        t.janela_grade(x, 97, x + 19, 105, colunas=3, linhas=1)          # bandeira
        t.janela_grade(x, 105, x + 19, rod - 3, colunas=3, linhas=5)     # folhas
        t.ret(x - 1, rod - 2, x + 20, rod - 1, br, 3)
    # pilastras nas pontas e entre as janelas (faixas brancas)
    for x in (4, 80, 176, L - 13):
        t.ret(x, 49, x + 8, rod - 1, cr, 1)
        t.vlinha(x, 49, rod - 1, cr, 0)
        t.vlinha(x + 8, 49, rod - 1, cr, 3)
    # frisos horizontais entre os andares
    t.ret(4, 86, cx0 - 1, 88, br, 1)
    t.ret(cx1 + 1, 86, L - 5, 88, br, 1)
    t.hlinha(4, cx0 - 1, 88, br, 3)
    t.hlinha(cx1 + 1, 88, L - 5, br, 3)
    # --- bloco central: 3 janelas em cima e 3 portas embaixo ---
    vaos = [100, 124, 148]
    for i, x in enumerate(vaos):
        t.ret(x - 1, 58, x + 16, 60, br, 1)
        t.janela_grade(x, 61, x + 15, 79, colunas=2, linhas=2)
        t.ret(x - 1, 80, x + 16, 81, br, 2)
        t.ret(x - 2, 96, x + 17, 98, br, 1)
        t.relevo(t.mascara_ret(x - 2, 96, x + 17, 98))
        t.janela_grade(x, 99, x + 15, 108, colunas=3, linhas=1)
        if i == 2:   # porta aberta (como na foto): vão escuro com a folha recolhida
            t.ret(x, 109, x + 15, rod + 6, M['interior'], 3)
            t.ret(x, 109, x + 15, 112, M['interior'], 4)
            t.ret(x + 11, 109, x + 15, rod + 6, br, 2)
            t.vlinha(x + 11, 109, rod + 6, br, 1)
            t.ret(x + 3, 118, x + 6, 124, M['vidro_escuro'], 1)  # cartaz lá dentro
        else:
            t.ret(x, 109, x + 15, rod + 6, br, 1)
            t.relevo(t.mascara_ret(x, 109, x + 15, rod + 6))
            t.vlinha(x + 7, 109, rod + 6, br, 3)
            for xx in (x + 2, x + 9):
                t.ret(xx, 112, xx + 4, 138, M['vidro'], 2)
                t.hlinha(xx, xx + 4, 112, M['vidro'], 4)
                for yy in range(117, 138, 5):
                    t.hlinha(xx, xx + 4, yy, br, 2)
                t.ret(xx, 142, xx + 4, rod + 3, br, 2)
                t.relevo(t.mascara_ret(xx, 142, xx + 4, rod + 3))
    # --- rodapé branco (blocos com juntas claras) ---
    t.ret(4, rod, L - 5, base, mm, 1)
    t.hlinha(4, L - 5, rod, mm, 0)
    t.hlinha(4, L - 5, rod + 1, mm, 0)
    for y in range(rod + 2, base + 1, 8):
        t.hlinha(4, L - 5, y + 7, mm, 2)
        off = 0 if (y // 8) % 2 else 12
        for x in range(4 + off, L - 5, 24):
            t.vlinha(x, y, min(base, y + 7), mm, 2)
            t.vlinha(x + 1, y, min(base, y + 7), mm, 0)
    # escada: degraus diante das portas
    for i, y in enumerate(range(rod + 6, base + 1, 3)):
        t.ret(cx0 + 4 - i * 2, y, cx1 - 4 + i * 2, y + 2, M['concreto'], 2)
        t.hlinha(cx0 + 4 - i * 2, cx1 - 4 + i * 2, y, M['concreto'], 0)
        t.hlinha(cx0 + 4 - i * 2, cx1 - 4 + i * 2, y + 2, M['concreto'], 3)
    t.escurecer_ret(cx0, rod + 6, cx1, rod + 8, 1, so_mat=M['concreto'])
    # --- 4 colunas jônicas sobre pedestais de pedra escura ---
    for cx in (96, 122, 146, 170):
        cx -= 3
        x0, x1 = cx - 5, cx + 5
        # pedestal
        t.ret(x0 - 3, rod - 14, x1 + 3, base, mm, 1)
        t.relevo(t.mascara_ret(x0 - 3, rod - 14, x1 + 3, base))
        t.ret(x0 - 4, rod - 16, x1 + 4, rod - 14, mm, 0)
        t.hlinha(x0 - 4, x1 + 4, rod - 16, mm, 0)
        t.vlinha(x1 + 3, rod - 13, base, mm, 3)
        t.vlinha(x0 - 3, rod - 13, base, mm, 0)
        # base da coluna (toro)
        t.ret(x0 - 1, rod - 20, x1 + 1, rod - 17, br, 1)
        t.hlinha(x0 - 1, x1 + 1, rod - 17, br, 3)
        # fuste
        t.cilindro(x0, x1, 55, rod - 21, br, caneluras=True)
        # capitel jônico (volutas)
        t.ret(x0 - 3, 50, x1 + 3, 54, br, 1)
        t.hlinha(x0 - 3, x1 + 3, 54, br, 3)
        for vx in (x0 - 2, x1 + 2):
            t.px(vx, 52, br, 4)
            t.px(vx - 1 if vx < cx else vx + 1, 52, br, 2)
        # sombra que a coluna projeta no fundo recuado (para a direita)
        t.escurecer_ret(x1 + 1, 55, x1 + 3, rod - 21, 1, so_mat=cr)
    # --- desgaste: manchas, escorridos e uma rachadura ---
    t.reboco(6, 50, L - 8, rod - 2, cr)
    for x in (12, 37, 61, 70, 185, 210, 233, 246):
        t.escorrido(x, 83, t.rnd.randint(4, 9), cr)
        t.escorrido(x + 2, rod - 1 - 8, 8, cr)
    t.rachadura(68, 60, 9, cr)
    t.rachadura(240, 100, 8, cr)
    t.manchas(8, 9, L - 9, 25, cr, 12, tam=(2, 3))
    t.contorno()
    return t.imagem()


# ===============================================================================================================
# Estátuas em bronze (busto e soldado): volumes do modelo.py com material de bronze
# ===============================================================================================================

BRONZE = modelo.Material('bronze', 'ABCDE', ['#E8B878', '#B07A44', '#7A4E2C', '#4A2E1A', '#26150A'],
                         limiares=(0.78, 0.48, 0.18))


def boneco_para_img(b):
    linhas = b.texto()
    pal = modelo.paleta_de([BRONZE])
    return matriz_para_img(linhas, pal)


def busto():
    """Busto (bronze) do Teodomiro Santiago: homem de paletó, cabeça e ombros. Sem traços inventados de rosto
    (a foto não mostra o rosto de perto): só cabelo curto, orelhas, sombra dos olhos, nariz e bigode."""
    b = modelo.Boneco(30, 30)
    b.elipse((15, 26), 12.5, 5.5, BRONZE, achatar=0.7)                 # ombros
    b.capsula((15, 20), (15, 27), 7, 9, mat=BRONZE, achatar=0.8)       # peito (paletó)
    b.capsula((15, 13), (15, 19), 2.6, mat=BRONZE, escurecer=1)        # pescoço
    b.elipse((10.6, 9.5), 1.2, 1.8, BRONZE, escurecer=1)               # orelhas
    b.elipse((19.4, 9.5), 1.2, 1.8, BRONZE, escurecer=1)
    b.elipse((15, 9), 4.4, 5.4, BRONZE)                                # cabeça
    for x in range(11, 20):                                            # cabelo curto: calota de cima
        for y in range(3, 6):
            if b.material_em(x, y):
                b.tom_em(x, y, BRONZE, 2 if y == 5 else 3)
    b.tom_em(13, 9, BRONZE, 3); b.tom_em(17, 9, BRONZE, 3)            # sombra dos olhos
    b.tom_em(15, 10, BRONZE, 1); b.tom_em(16, 11, BRONZE, 2)          # nariz
    for x in (13, 14, 15, 16, 17):                                     # bigode
        b.tom_em(x, 12, BRONZE, 3)
    b.tom_em(13, 7, BRONZE, 0); b.tom_em(14, 7, BRONZE, 0)            # brilho da testa
    for y in range(20, 30):                                            # lapelas
        d = (30 - y) // 3
        b.tom_em(15 - d - 1, y, BRONZE, 3)
        b.tom_em(15 + d + 1, y, BRONZE, 3)
    for y in range(20, 24):
        b.tom_em(15, y, BRONZE, 2)                                     # gravata
    b.tom_em(14, 20, BRONZE, 0); b.tom_em(16, 20, BRONZE, 0)          # colarinho
    return boneco_para_img(b)


def soldado():
    """Soldado de bronze: capacete, camisa com bolsos, cinto com cartucheiras, calça para dentro das botas, braço
    direito esticado apontando, fuzil em pé ao lado (como na Praça do Soldado)."""
    b = modelo.Boneco(70, 72)
    # fuzil (atrás da mão esquerda)
    b.capsula((15, 12), (16, 52), 1.0, mat=BRONZE, escurecer=1)        # cano
    b.capsula((16, 48), (17, 69), 2.2, 2.8, mat=BRONZE)               # coronha
    b.capsula((15, 26), (15, 34), 1.2, mat=BRONZE, escurecer=1)       # bandoleira
    # pernas e botas
    b.capsula((28, 42), (26, 62), 4.2, 3.6, mat=BRONZE, escurecer=1)
    b.capsula((36, 42), (38, 62), 4.2, 3.6, mat=BRONZE)
    b.capsula((25.5, 61), (25, 68), 3.6, 3.4, mat=BRONZE, escurecer=1)
    b.capsula((38.5, 61), (39, 68), 3.6, 3.4, mat=BRONZE)
    b.elipse((24.5, 68.5), 4.2, 1.8, BRONZE, escurecer=1)
    b.elipse((40, 68.5), 4.2, 1.8, BRONZE)
    # tronco
    b.capsula((32, 22), (32, 40), 8.0, 6.6, mat=BRONZE, achatar=0.85)
    # braço esquerdo para baixo segurando o fuzil
    b.capsula((24.5, 22), (21, 32), 3.0, 2.6, mat=BRONZE, escurecer=1)
    b.capsula((21, 32), (18, 40), 2.6, 2.2, mat=BRONZE, escurecer=1)
    b.elipse((17, 41), 2.4, 2.6, BRONZE)
    # braço direito esticado apontando (para a frente da fase)
    b.capsula((39, 21), (50, 17), 3.0, 2.6, mat=BRONZE)
    b.capsula((50, 17), (60, 13), 2.6, 2.2, mat=BRONZE)
    b.elipse((62, 12.5), 2.4, 2.0, BRONZE)
    # pescoço, cabeça e capacete
    b.capsula((32, 15), (32, 19), 2.6, mat=BRONZE)
    b.elipse((32, 12), 4.0, 4.8, BRONZE)
    b.elipse((32, 8), 6.4, 4.4, BRONZE)
    b.capsula((25.5, 10), (38.5, 10), 0.9, mat=BRONZE, escurecer=1)    # aba do capacete
    # detalhes: bolsos, cinto, cartucheiras, dedo apontando
    for x0 in (27, 34):
        for x in range(x0, x0 + 4):
            b.tom_em(x, 25, BRONZE, 3)
        b.tom_em(x0, 26, BRONZE, 3); b.tom_em(x0 + 3, 26, BRONZE, 3)
        for x in range(x0, x0 + 4):
            b.tom_em(x, 29, BRONZE, 2)
    for x in range(25, 40):
        b.tom_em(x, 38, BRONZE, 3)
        b.tom_em(x, 39, BRONZE, 1 if x % 4 else 3)
    for x0 in (26, 35):
        for y in range(36, 41):
            b.tom_em(x0, y, BRONZE, 3)
            b.tom_em(x0 + 3, y, BRONZE, 3)
    b.px(65, 11, 'B'); b.px(66, 11, 'B'); b.px(65, 12, 'C')
    b.tom_em(30, 12, BRONZE, 3); b.tom_em(34, 12, BRONZE, 3)       # sombra dos olhos sob o capacete
    for y in range(44, 60, 5):                                      # dobras da calça
        b.tom_em(29, y, BRONZE, 3); b.tom_em(37, y + 2, BRONZE, 2)
    return boneco_para_img(b)


# ===============================================================================================================
# 2. Fonte da praça com o busto do Teodomiro Santiago
# ===============================================================================================================

def fonte():
    L, A = 172, 108
    t = Tela(L, A, semente=22)
    gr, ag = M['granito'], M['agua']
    cx = L / 2
    cy = A - 15           # centro da elipse da borda
    rx, ry = 82, 11
    # parede da frente da borda (curva): da linha da elipse para baixo 12 px, mais clara à esquerda
    for x in range(int(cx - rx), int(cx + rx) + 1):
        d = (x + 0.5 - cx) / rx
        if abs(d) > 1:
            continue
        ye = cy + ry * math.sqrt(1 - d * d)
        f = (d + 1) / 2
        tom = 1 if f < 0.18 else 2 if f < 0.62 else 3 if f < 0.9 else 4
        for y in range(int(ye) - 1, min(A, int(ye) + 13)):
            t.px(x, y, gr, tom)
        t.px(x, int(ye) + 12, gr, 4)
    # tampo da borda (anel claro) e espelho d'água
    t.elipse(cx, cy, rx, ry, gr, 0)
    t.elipse(cx, cy - 0.5, rx - 4, ry - 2.5, gr, 3)
    t.elipse(cx, cy, rx - 5, ry - 3, ag, 2)
    # água: faixa de reflexo do céu ao fundo e ondinhas
    m_agua = t.mascara_elipse(cx, cy, rx - 5, ry - 3)
    yy, xx = np.mgrid[0:A, 0:L]
    t.tom[m_agua & (yy < cy - 4)] = 1
    for _ in range(40):
        x = t.rnd.randint(int(cx - rx + 10), int(cx + rx - 14))
        y = t.rnd.randint(int(cy - 5), int(cy + 6))
        for k in range(t.rnd.randint(2, 5)):
            if t.dentro(x + k, y) and t.mat[y, x + k] == ag:
                t.tom[y, x + k] = t.rnd.choice((0, 1, 3))
    # juntas das placas da borda
    for k in range(-7, 8):
        x = int(cx + k * rx / 8)
        d = (x - cx) / rx
        ye = cy + ry * math.sqrt(max(0, 1 - d * d))
        t.vlinha(x, int(ye) + 1, int(ye) + 11, gr, 4)
        t.px(x + 1, int(ye) + 1, gr, 1)
    t.manchas(int(cx - rx), int(cy), int(cx + rx), A - 1, gr, 30, tam=(2, 4))

    # jatos: arcos que saem da borda e caem perto do pedestal (os de trás primeiro)
    def jato(x0, y0, x1, y1, alt, frente):
        n = int(abs(x1 - x0) * 2) + 8
        ultimo = None
        for i in range(n + 1):
            s = i / n
            x = x0 + (x1 - x0) * s
            y = y0 + (y1 - y0) * s - alt * 4 * s * (1 - s)
            p = (int(round(x)), int(round(y)))
            if p == ultimo:
                continue
            ultimo = p
            t.px(p[0], p[1], ag, 0 if frente else 1, sem_contorno=True)
            t.px(p[0], p[1] + 1, ag, 2 if frente else 3, sem_contorno=True)
        # respingo onde cai
        for dx, dy, tm in ((-1, -1, 0), (1, -2, 1), (0, -2, 0), (2, 0, 1), (-2, 0, 1)):
            t.px(x1 + dx, y1 + dy, ag, tm, sem_contorno=True)

    angulos = [i * 360 / 14 + 8 for i in range(14)]
    jatos = []
    for a in angulos:
        r = math.radians(a)
        x0 = cx + (rx - 6) * math.cos(r)
        y0 = cy + (ry - 3) * math.sin(r)
        x1 = cx + 14 * math.cos(r)
        y1 = cy + 3 * math.sin(r)
        jatos.append((y0, x0, x1, y1, 26 + 8 * abs(math.cos(r))))
    for y0, x0, x1, y1, alt in sorted(jatos):
        if y0 < cy:
            jato(x0, y0 - 1, x1, y1, alt, False)
    # pedestal de pedra clara com placa de bronze
    px0, px1 = int(cx - 9), int(cx + 8)
    t.ret(px0 - 3, cy - 8, px1 + 3, cy + 1, gr, 2)                 # base
    t.relevo(t.mascara_ret(px0 - 3, cy - 8, px1 + 3, cy + 1))
    t.hlinha(px0 - 3, px1 + 3, cy - 8, gr, 0)
    t.ret(px0, cy - 50, px1, cy - 9, gr, 1)                         # fuste
    t.vlinha(px0, cy - 50, cy - 9, gr, 0)
    t.ret(px1 - 4, cy - 50, px1, cy - 9, gr, 2)
    t.vlinha(px1, cy - 50, cy - 9, gr, 3)
    t.ret(px0 - 3, cy - 56, px1 + 3, cy - 51, gr, 1)               # capitel
    t.hlinha(px0 - 3, px1 + 3, cy - 56, gr, 0)
    t.hlinha(px0 - 3, px1 + 3, cy - 52, gr, 3)
    t.hlinha(px0 - 2, px1 + 2, cy - 51, gr, 4)
    t.ret(px0 + 3, cy - 36, px1 - 3, cy - 24, M['bronze'], 3)       # placa
    t.relevo(t.mascara_ret(px0 + 3, cy - 36, px1 - 3, cy - 24))
    for y in range(int(cy - 33), int(cy - 26), 2):
        t.hlinha(px0 + 5, px1 - 5, y, M['bronze'], 1)
    t.manchas(px0, int(cy - 50), px1, int(cy - 10), gr, 8, tam=(1, 3))
    t.escorrido(px0 + 4, int(cy - 23), 12, gr)
    for y0, x0, x1, y1, alt in sorted(jatos):
        if y0 >= cy:
            jato(x0, y0 - 1, x1, y1, alt - 6, True)
    t.contorno(ignorar=(ag,))
    img = t.imagem()
    bb = busto()
    img.alpha_composite(bb, (int(cx - 15) - 1, int(cy - 56 - 29)))
    return img


# ===============================================================================================================
# 3. Café do Vadinho
# ===============================================================================================================

def cafe():
    L, A = 188, 174
    t = Tela(L, A, semente=33)
    cr, br, ln, gf = M['creme'], M['branco'], M['lona'], M['grafite']
    base = A - 1
    # --- fachada de cima ---
    t.parede(2, 6, L - 3, 94, cr, 1)
    t.cornija(0, L - 1, 2, br, alt=4, sombra_proj=2)
    t.ret(2, 0, L - 3, 1, br, 2)
    for x in (2, 62, 124, L - 9):                                   # pilastras brancas
        t.ret(x, 8, x + 6, 90, br, 1)
        t.vlinha(x, 8, 90, br, 0)
        t.vlinha(x + 6, 8, 90, br, 3)
    for x in (16, 78, 140):                                         # janelas de veneziana
        t.ret(x - 3, 20, x + 30, 22, br, 1)
        t.relevo(t.mascara_ret(x - 3, 20, x + 30, 22))
        t.escurecer_ret(x - 2, 23, x + 29, 24, 1, so_mat=cr)
        t.veneziana(x, 23, x + 27, 62)
        t.ret(x - 3, 63, x + 30, 65, br, 2)
        t.hlinha(x - 3, x + 30, 63, br, 0)
        t.escurecer_ret(x - 2, 66, x + 29, 67, 1, so_mat=cr)
    t.reboco(8, 8, L - 10, 88, cr, n=22)
    for x in (30, 95, 150, 170):
        t.escorrido(x, 66, t.rnd.randint(5, 12), cr)
    t.ret(0, 86, L - 1, 94, br, 2)                                  # marquise (laje)
    t.hlinha(0, L - 1, 86, br, 0)
    t.hlinha(0, L - 1, 87, br, 1)
    t.hlinha(0, L - 1, 94, br, 4)
    # --- loja à sombra embaixo do toldo ---
    lo = M['interior']
    t.ret(2, 95, L - 3, base, lo, 3)
    t.ret(2, 95, L - 3, 104, lo, 4)
    # balcão, máquina de café, prateleiras e luminárias
    t.ret(14, 140, 70, base - 12, M['madeira'], 3)
    t.hlinha(14, 70, 140, M['madeira'], 1)
    t.hlinha(14, 70, 141, M['madeira'], 2)
    for x in range(18, 70, 8):
        t.vlinha(x, 143, base - 13, M['madeira'], 4)
    t.ret(24, 128, 36, 139, gf, 1)                                  # máquina de espresso
    t.relevo(t.mascara_ret(24, 128, 36, 139))
    t.ret(26, 131, 34, 133, gf, 3)
    t.px(27, 130, M['dourado'], 0); t.px(31, 130, M['dourado'], 1)
    for y in (112, 122):                                            # prateleiras com garrafas e xícaras
        t.hlinha(10, 72, y + 6, M['madeira'], 2)
        for x in range(12, 70, 3):
            t.vlinha(x, y + 1, y + 5, t.rnd.choice((M['vidro'], M['vermelho'], M['folha'], M['dourado'])),
                     t.rnd.choice((1, 2, 3)))
    for x in (40, 104, 150):                                        # luminárias acesas
        t.vlinha(x, 105, 108, gf, 3)
        t.ret(x - 2, 109, x + 2, 110, M['dourado'], 1)
        t.px(x, 111, M['amarelo'], 0)
    t.ret(84, 104, 96, base - 8, br, 1)                             # pilar branco com cardápio
    t.vlinha(84, 104, base - 8, br, 0)
    t.vlinha(96, 104, base - 8, br, 3)
    t.ret(86, 118, 94, 132, M['concreto'], 1)
    for y in range(120, 131, 2):
        t.hlinha(87, 93, y, gf, 2)
    t.ret(112, 116, 140, 150, M['vidro_escuro'], 2)                 # vitrine ao fundo
    t.hlinha(112, 140, 116, M['vidro_escuro'], 0)
    t.ret(150, 108, 176, 128, M['concreto'], 1)                     # placa clara ao fundo (sem marca)
    t.relevo(t.mascara_ret(150, 108, 176, 128))
    for y in range(112, 126, 3):
        t.hlinha(153, 173, y, M['azul'], 2)
    # --- toldo curvo (lona) com armação escura ---
    m = t.mascara_ret(0, 90, L - 1, 118)
    yy, xx = np.mgrid[0:A, 0:L]
    # pontas arredondadas descendo
    for lado in (0, 1):
        x0 = 0 if lado == 0 else L - 12
        for y in range(90, 119):
            for x in range(x0, x0 + 12):
                dxn = (x - (x0 + 11 if lado == 0 else x0)) / 12
                dyn = (y - 118) / 28
                if dxn * dxn + dyn * dyn > 1:
                    m[y, x] = False
    t.volume_h(m, ln, cortes=(0.12, 0.34, 0.66, 0.86))
    for x in range(14, L - 12, 26):                                 # costelas da armação
        t.vlinha(x, 91, 116, gf, 3)
        t.vlinha(x + 1, 91, 116, ln, 0 if x < L // 2 else 1)
    t.ret(6, 117, L - 7, 119, gf, 2)                                # barra da frente
    t.hlinha(6, L - 7, 117, gf, 0)
    t.hlinha(6, L - 7, 119, gf, 4)
    for x in (4, L - 6):                                            # postes
        t.ret(x, 117, x + 2, base, gf, 2)
        t.vlinha(x, 117, base, gf, 1)
        t.vlinha(x + 2, 117, base, gf, 4)
    # placa oval preta "Café do Vadinho"
    ox, oy = L / 2, 102
    t.elipse(ox, oy, 38, 10.5, gf, 3)
    t.elipse(ox, oy, 36, 8.5, gf, 4)
    m_o = t.mascara_elipse(ox, oy, 38, 10.5) & ~t.mascara_elipse(ox, oy, 36.6, 9.2)
    t.aplicar(m_o, M['granito'], 1)
    t.aplicar(m_o & (yy > oy), M['granito'], 3)
    txt = 'Café do Vadinho'
    tx0 = int(ox - largura_texto(txt) / 2)
    t.texto(tx0, int(oy) - 3, txt, M['granito'], 0)
    t.hlinha(int(ox) - 3, int(ox) + 3, int(oy) + 4, M['granito'], 2)    # risquinho (como na placa)
    # --- mesinhas e cadeiras de madeira dobráveis na calçada ---
    md = M['madeira_clara']

    def cadeira(x, vira):
        s = 1 if vira else -1
        t.linha(x, base, x + 6 * s, base - 14, md, 3)
        t.linha(x + 6 * s, base, x, base - 14, md, 2)
        t.ret(min(x, x + 6 * s) - 1, base - 13, max(x, x + 6 * s) + 1, base - 12, md, 1)   # assento
        t.linha(x, base - 13, x - 2 * s, base - 26, md, 2, larg=1)                         # encosto
        for yb in (base - 24, base - 21, base - 18):
            t.hlinha(min(x - 2 * s, x + 3 * s), max(x - 2 * s, x + 3 * s), yb, md, 1)

    def mesa(x):
        t.ret(x - 9, base - 20, x + 9, base - 18, md, 1)
        t.hlinha(x - 9, x + 9, base - 20, md, 0)
        t.hlinha(x - 9, x + 9, base - 18, md, 3)
        t.linha(x - 6, base - 17, x + 6, base, md, 2)
        t.linha(x + 6, base - 17, x - 6, base, md, 3)
        t.px(x - 3, base - 21, M['branco'], 0); t.px(x - 2, base - 21, M['branco'], 1)  # xícara
        t.px(x + 3, base - 22, M['vidro'], 1); t.px(x + 3, base - 21, M['vidro'], 2)    # copo

    for x in (30, 92, 150):
        cadeira(x - 16, False)
        mesa(x)
        cadeira(x + 16, True)
    # cavalete com o quadro-negro do cardápio
    qx = 120
    t.linha(qx - 7, base, qx - 3, base - 26, md, 2)
    t.linha(qx + 7, base, qx + 3, base - 26, md, 3)
    t.ret(qx - 6, base - 24, qx + 6, base - 8, gf, 4)
    t.relevo(t.mascara_ret(qx - 6, base - 24, qx + 6, base - 8), delta=-1)
    for y in range(base - 21, base - 9, 3):
        t.hlinha(qx - 4, qx - 4 + t.rnd.randint(4, 8), y, M['concreto'], 1)
    # vaso com planta à esquerda
    t.ret(3, base - 8, 11, base, M['telha'], 2)
    t.relevo(t.mascara_ret(3, base - 8, 11, base))
    t.copa(7, base - 15, 7, 8, M['folha'], n=6)
    t.contorno()
    return t.imagem()

# ===============================================================================================================
# 4. Igreja Matriz
# ===============================================================================================================

def igreja():
    L, A = 204, 244
    t = Tela(L, A, semente=44)
    cr, br, gf = M['creme'], M['branco'], M['grafite']
    yb = A - 15                      # pé da fachada (a escadaria fica embaixo)
    cxm = L // 2                     # eixo central
    madeira = M['madeira']

    def pilastra(x0, x1, y0, y1):
        t.ret(x0, y0, x1, y1, br, 1)
        t.vlinha(x0, y0, y1, br, 0)
        t.vlinha(x1, y0, y1, br, 3)
        t.vlinha(x1 + 1, y0, y1, cr, 3)

    def arquinhos(x0, x1, y, mat=br):
        """Friso de arquinhos (arcatura) embaixo das cornijas, como na foto."""
        for x in range(x0, x1 + 1):
            k = (x - x0) % 6
            if k in (0, 5):
                t.vlinha(x, y, y + 3, mat, 2)
            elif k in (1, 4):
                t.px(x, y, mat, 1); t.px(x, y + 1, mat, 2)
            else:
                t.px(x, y, mat, 1)
        t.escurecer_ret(x0, y + 1, x1, y + 3, 1, so_mat=cr)

    def janela_arco(x0, x1, y0, y1, cega=False, persiana=False):
        m = t.mascara_arco(x0 - 2, x1 + 2, y0 - 2, y1)
        t.aplicar(m, br, 1)
        t.relevo(m)
        mi = t.mascara_arco(x0, x1, y0, y1)
        if cega:
            t.aplicar(mi, cr, 3)
            t.aplicar(t.borda_de(mi, 'cima') | t.borda_de(mi, 'esq'), cr, 4)
        elif persiana:
            t.aplicar(mi, gf, 2)
            ys = np.nonzero(mi.any(axis=1))[0]
            for y in ys:
                if (y - ys[0]) % 2 == 1:
                    t.aplicar(mi & t.mascara_ret(0, y, L, y), gf, 4)
                else:
                    t.aplicar(mi & t.mascara_ret(0, y, L, y), gf, 1)
        else:
            t.aplicar(mi, M['vidro'], 2)
            t.aplicar(t.borda_de(mi, 'cima'), M['vidro'], 4)
            t.vlinha((x0 + x1) // 2, y0, y1, br, 2)
        t.ret(x0 - 3, y1 + 1, x1 + 3, y1 + 2, br, 2)
        t.hlinha(x0 - 3, x1 + 3, y1 + 1, br, 0)

    def porta(x0, x1, y0, rica=False):
        m = t.mascara_arco(x0 - 3, x1 + 3, y0 - 3, yb)
        t.aplicar(m, br, 1)
        t.relevo(m)
        if rica:   # arquivolta dupla com bandeira trabalhada
            m2 = t.mascara_arco(x0 - 1, x1 + 1, y0 - 1, yb)
            t.aplicar(m2, br, 2)
        mi = t.mascara_arco(x0, x1, y0, yb)
        t.aplicar(mi, madeira, 3)
        r = (x1 - x0 + 1) / 2
        ybd = int(y0 + r)                       # linha da bandeira (tímpano)
        tim = mi & t.mascara_ret(0, 0, L, ybd + 2)
        t.aplicar(tim, M['dourado'] if rica else M['vidro'], 2)
        t.aplicar(t.borda_de(tim, 'cima'), M['dourado'] if rica else M['vidro'], 4)
        if rica:
            cxp = (x0 + x1) // 2
            for k in range(-3, 4):
                t.linha(cxp, ybd + 1, cxp + k * 3, y0 + 1, M['dourado'], 0 if k % 2 else 3)
            t.ret(cxp - 2, ybd - 3, cxp + 2, ybd + 1, M['dourado'], 1)
        t.hlinha(x0, x1, ybd + 2, br, 1)
        t.hlinha(x0, x1, ybd + 3, br, 3)
        # folhas de madeira com almofadas
        meio = (x0 + x1) // 2
        t.vlinha(meio, ybd + 4, yb, madeira, 4)
        for xa, xb_ in ((x0 + 2, meio - 2), (meio + 2, x1 - 2)):
            for ya, yb_ in ((ybd + 7, ybd + 20), (ybd + 24, yb - 4)):
                if yb_ - ya < 4 or xb_ - xa < 2:
                    continue
                mm = t.mascara_ret(xa, ya, xb_, yb_)
                t.aplicar(mm, madeira, 2)
                t.relevo(mm)
        t.ret(x0, ybd + 4, x1, ybd + 5, madeira, 4)              # sombra da verga

    # ---------- alas de fora (mais baixas) ----------
    for x0, x1 in ((4, 21), (L - 22, L - 5)):
        t.parede(x0, 150, x1, yb, cr, 2)
        t.cornija(x0 - 2, x1 + 2, 146, br, alt=4)
        janela_arco(x0 + 5, x0 + 12, 172, 196)
        t.reboco(x0 + 1, 152, x1 - 1, yb - 8, cr, n=6)
    # ---------- corpo das torres laterais e paredes laterais ----------
    lat = ((22, 67), (L - 68, L - 23))
    for x0, x1 in lat:
        t.parede(x0, 136, x1, yb, cr, 1)
        t.cornija(x0 - 2, x1 + 2, 131, br, alt=5)
        arquinhos(x0, x1, 136)
        pilastra(x0, x0 + 4, 140, yb)
        pilastra(x1 - 4, x1, 140, yb)
        cxl = (x0 + x1) // 2
        janela_arco(cxl - 6, cxl + 6, 146, 172, cega=True)
        porta(cxl - 10, cxl + 10, 176)
        t.reboco(x0 + 5, 140, x1 - 5, yb - 8, cr)
        # torre lateral
        tx0, tx1 = cxl - 17, cxl + 17
        t.parede(tx0, 92, tx1, 130, cr, 1)
        t.escurecer_ret(tx1 - 6, 92, tx1, 130, 1, so_mat=cr)
        pilastra(tx0, tx0 + 3, 94, 130)
        pilastra(tx1 - 3, tx1, 94, 130)
        janela_arco(cxl - 5, cxl + 5, 100, 124, persiana=True)
        t.cornija(tx0 - 2, tx1 + 2, 88, br, alt=4)
        arquinhos(tx0, tx1, 92)
        # frontão triangular com friso de dentes
        gm = t.poli([(tx0 - 2, 88), (cxl, 72), (tx1 + 2, 88)], cr, 2)
        t.poli([(tx0 + 4, 87), (cxl, 77), (tx1 - 4, 87)], cr, 3)
        t.linha(tx0 - 2, 88, cxl, 72, br, 0, larg=2)
        t.linha(cxl, 72, tx1 + 2, 88, br, 2, larg=2)
        t.px(cxl, 81, br, 1); t.px(cxl, 82, br, 1)                # óculo pequeno
        # coruchéu com cruz
        t.ret(cxl - 3, 66, cxl + 3, 72, br, 1)
        t.relevo(t.mascara_ret(cxl - 3, 66, cxl + 3, 72))
        t.poli([(cxl - 2, 66), (cxl, 58), (cxl + 2, 66)], br, 1)
        t.vlinha(cxl + 1, 60, 66, br, 3)
        t.vlinha(cxl, 50, 57, M['dourado'], 2)
        t.hlinha(cxl - 2, cxl + 2, 52, M['dourado'], 2)
        t.px(cxl, 50, M['dourado'], 0)
    # ---------- corpo central ----------
    c0, c1 = cxm - 32, cxm + 31
    t.parede(c0, 120, c1, yb, cr, 1)
    pilastra(c0, c0 + 5, 124, yb)
    pilastra(c1 - 5, c1, 124, yb)
    t.cornija(c0 - 2, c1 + 2, 116, br, alt=4)
    arquinhos(c0 + 6, c1 - 6, 140)
    t.cornija(c0 + 6, c1 - 6, 136, br, alt=3, sombra_proj=0)
    # rosácea
    rx, ry = cxm, 156
    t.elipse(rx, ry, 11.5, 11.5, br, 1)
    t.relevo(t.mascara_elipse(rx, ry, 11.5, 11.5))
    t.elipse(rx, ry, 9.5, 9.5, M['vidro'], 3)
    t.elipse(rx, ry, 3, 3, M['dourado'], 1)
    for k in range(8):
        a = k * math.pi / 4
        t.linha(rx + 3 * math.cos(a), ry + 3 * math.sin(a), rx + 9 * math.cos(a), ry + 9 * math.sin(a), br, 2)
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        t.px(rx + 6 * math.cos(a), ry + 6 * math.sin(a), M['vidro'], 0)
    porta(cxm - 15, cxm + 14, 172, rica=True)
    t.reboco(c0 + 7, 124, c1 - 7, 166, cr, n=5)
    # ---------- torre central ----------
    t0, t1 = cxm - 24, cxm + 23            # bloco com nichos
    t.parede(t0, 78, t1, 115, cr, 1)
    pilastra(t0, t0 + 3, 80, 115)
    pilastra(t1 - 3, t1, 80, 115)
    for k in range(4):
        x = t0 + 7 + k * 10
        janela_arco(x, x + 5, 88, 110, cega=True)
    t.cornija(t0 - 2, t1 + 2, 74, br, alt=4)
    arquinhos(t0, t1, 78)
    k0, k1 = cxm - 19, cxm + 18            # andar do relógio
    t.parede(k0, 46, k1, 73, cr, 1)
    t.escurecer_ret(k1 - 5, 46, k1, 73, 1, so_mat=cr)
    pilastra(k0, k0 + 3, 48, 73)
    pilastra(k1 - 3, k1, 48, 73)
    for x in (cxm - 10, cxm + 5):
        janela_arco(x, x + 4, 63, 72, persiana=True)
    t.cornija(k0 - 2, k1 + 2, 42, br, alt=4)
    # frontão com o relógio
    t.poli([(k0 - 2, 42), (cxm, 32), (k1 + 2, 42)], cr, 2)
    t.linha(k0 - 2, 42, cxm, 32, br, 0, larg=2)
    t.linha(cxm, 32, k1 + 2, 42, br, 2, larg=2)
    t.elipse(cxm, 51, 8, 8, br, 1)
    t.relevo(t.mascara_elipse(cxm, 51, 8, 8))
    t.elipse(cxm, 51, 6.5, 6.5, gf, 2)
    t.elipse(cxm, 51, 5.5, 5.5, br, 0)
    t.aplicar(t.mascara_elipse(cxm, 51, 5.5, 5.5) & ~t.mascara_elipse(cxm - 1, 50, 5.5, 5.5), br, 2)
    for a in range(0, 360, 30):
        r = 4.5 if a % 90 == 0 else 4.8
        t.px(cxm - 0.5 + r * math.cos(math.radians(a)), 50.5 + r * math.sin(math.radians(a)), gf,
             3 if a % 90 == 0 else 1)
    t.vlinha(cxm, 47, 51, gf, 4)                                    # ponteiros (10 para as 7, entardecer)
    t.linha(cxm, 51, cxm - 2, 53, gf, 4)
    b0, b1 = cxm - 14, cxm + 13            # campanário
    t.parede(b0, 18, b1, 31, cr, 1)
    t.escurecer_ret(b1 - 4, 18, b1, 31, 1, so_mat=cr)
    janela_arco(cxm - 4, cxm + 3, 20, 30, persiana=True)
    t.cornija(b0 - 2, b1 + 2, 14, br, alt=4)
    t.poli([(b0 + 1, 14), (cxm - 4, 9), (cxm + 3, 9), (b1 - 1, 14)], cr, 2)   # cúpula baixa
    t.hlinha(b0 + 3, b1 - 3, 13, cr, 3)
    t.ret(cxm - 3, 7, cxm + 2, 9, br, 1)
    # imagem no alto (vulto claro de braços abertos)
    t.ret(cxm - 1, 1, cxm, 6, br, 0)
    t.px(cxm - 1, 0, br, 1); t.px(cxm, 0, br, 1)
    t.hlinha(cxm - 3, cxm + 2, 2, br, 1)
    # ---------- base: rodapé com almofadas ----------
    for x0, x1 in ((4, L - 5),):
        t.ret(x0, yb - 6, x1, yb, cr, 3)
        t.hlinha(x0, x1, yb - 6, br, 1)
        for x in range(x0 + 3, x1 - 6, 10):
            if t.mat[yb - 3, x + 3] == cr:
                t.ret(x, yb - 4, x + 6, yb - 1, M['marmore'], 1)
    # vasos com planta junto da porta principal
    for x in (cxm - 24, cxm + 20):
        t.ret(x, yb - 9, x + 5, yb, M['concreto'], 1)
        t.relevo(t.mascara_ret(x, yb - 9, x + 5, yb))
        t.copa(x + 3, yb - 14, 5, 6, M['folha'], n=5)
    # ---------- escadaria ----------
    for i in range(7):
        y = yb + 1 + i * 2
        x0, x1 = 6 - i, L - 7 + i
        t.ret(x0, y, x1, y + 1, M['concreto'], 2)
        t.hlinha(x0, x1, y, M['concreto'], 0 if i % 2 == 0 else 1)
        t.hlinha(x0, x1, y + 1, M['concreto'], 3)
    t.escurecer_ret(4, yb + 1, L - 5, yb + 2, 1, so_mat=M['concreto'])
    # corrimãos de metal
    for xr in (cxm - 46, cxm + 45):
        for xp, yp in ((xr, yb + 1), (xr, A - 3)):
            t.vlinha(xp, yp - 9, yp, gf, 1)
        t.vlinha(xr + 1, yb - 8, A - 12, gf, 3)
        t.hlinha(xr - 1, xr + 1, yb - 8, gf, 0)
        t.linha(xr, yb - 8, xr, A - 12, gf, 1)
    t.contorno()
    return t.imagem()


# ===============================================================================================================
# 5. Posto Esso, "o menor posto de gasolina do mundo"
# ===============================================================================================================

def posto():
    L, A = 116, 156
    t = Tela(L, A, semente=55)
    az, vm, bc = M['azulejo'], M['vermelho'], M['branco']
    base = A - 1
    # --- poste e placa oval (atrás da cabine) ---
    px = 36
    t.ret(px - 1, 30, px + 1, base - 10, M['concreto'], 2)
    t.vlinha(px - 1, 30, base - 10, M['concreto'], 1)
    t.vlinha(px + 1, 30, base - 10, M['concreto'], 3)
    # treliça com a plaquinha de baixo
    for y in range(36, 60, 6):
        t.linha(px - 14, y, px + 14, y + 6, M['concreto'], 3)
        t.linha(px + 14, y, px - 14, y + 6, M['concreto'], 3)
    t.vlinha(px - 14, 36, 62, M['concreto'], 2)
    t.vlinha(px + 14, 36, 62, M['concreto'], 2)
    t.ret(px - 18, 40, px + 18, 50, bc, 1)
    t.relevo(t.mascara_ret(px - 18, 40, px + 18, 50))
    for y in (43, 46):
        t.hlinha(px - 15, px + 15, y, M['azul'], 3)
    # oval: aro azul, aro branco e campo branco com ESSO em vermelho (decisão do Pedro, 01/11/2026).
    # Letras de pixel nossas (fonte do cenario.py ampliada 2x), sem decalcar o logotipo.
    oy = 18
    t.elipse(px, oy, 23, 15, M['azul'], 2)
    t.aplicar(t.mascara_elipse(px, oy, 23, 15) & ~t.mascara_elipse(px - 1, oy + 1, 22, 14), M['azul'], 1)
    t.elipse(px, oy, 20, 12, bc, 1)
    t.elipse(px, oy, 19, 11, bc, 0)
    t.aplicar(t.mascara_elipse(px, oy, 19, 11) & ~t.mascara_elipse(px - 1, oy - 1, 19, 11), bc, 2)
    yy, xx = np.mgrid[0:A, 0:L]
    txt = 'ESSO'
    larg2 = largura_texto(txt) * 2
    tx = int(px - larg2 / 2) + 1
    t.texto(tx + 1, oy - 4, txt, vm, 4, escala=2)      # sombra das letras
    t.texto(tx, oy - 5, txt, vm, 2, escala=2)
    for y in (oy - 5,):                                 # luz no alto das letras
        sel = (t.mat[y] == vm) & (t.tom[y] == 2)
        t.tom[y][sel] = 1
    t.px(px - 12, oy - 9, bc, 0); t.px(px - 11, oy - 10, bc, 0)        # brilho do acrílico
    # --- plataforma com meio-fio amarelo ---
    t.ret(2, base - 7, L - 3, base, M['concreto'], 2)
    t.hlinha(2, L - 3, base - 7, M['concreto'], 0)
    t.ret(2, base - 3, L - 3, base, M['amarelo'], 2)
    t.hlinha(2, L - 3, base - 3, M['amarelo'], 1)
    t.hlinha(2, L - 3, base, M['amarelo'], 4)
    for x in range(10, L - 3, 14):
        t.vlinha(x, base - 3, base, M['amarelo'], 4)
    # --- cabine ---
    c0, c1 = 26, 100
    ct, cb = 74, base - 8
    t.ret(c0, ct, c1, cb, az, 1)
    for y in range(ct, cb + 1):                                     # azulejos 5x5
        for x in range(c0, c1 + 1):
            if (y - ct) % 5 == 4 or (x - c0) % 5 == 4:
                t.px(x, y, az, 2)
    t.relevo(t.mascara_ret(c0, ct, c1, cb))
    t.escurecer_ret(c1 - 10, ct, c1, cb, 1, so_mat=az)              # lado na sombra
    # janela grande com caixilho branco (3x3) e porta
    t.janela_grade(34, 82, 60, 112, colunas=3, linhas=3)
    t.ret(34, 114, 60, cb, bc, 1)                                   # porta branca (parte de baixo)
    t.relevo(t.mascara_ret(34, 114, 60, cb))
    t.vlinha(47, 114, cb, bc, 3)
    t.px(45, 124, M['grafite'], 1)
    t.janela_grade(68, 82, 92, 106, colunas=3, linhas=3)
    # painel de pedra amarelada com moldura vermelha (embaixo à direita)
    t.ret(64, 110, 96, cb, vm, 2)
    t.hlinha(64, 96, 110, vm, 0)
    t.vlinha(96, 110, cb, vm, 3)
    pa = M['pedra_amarela']
    t.ret(66, 112, 94, cb, pa, 2)
    for y in range(112, cb + 1):
        for x in range(66, 95):
            if (y - 112) % 5 == 4 or (x + ((y - 112) // 5) * 3) % 7 == 0:
                t.px(x, y, pa, 4)
            elif t.rnd.random() < 0.18:
                t.px(x, y, pa, t.rnd.choice((1, 3)))
    t.ret(84, 116, 88, 121, bc, 1)                                  # tomadinha / caixa de luz
    t.relevo(t.mascara_ret(84, 116, 88, 121))
    # --- telhado: laje com beiral vermelho e platibanda de azulejo em losango ---
    t.ret(16, 62, 110, 67, bc, 1)
    for x in range(16, 111):
        for y in range(62, 68):
            if (x + y) % 6 == 0 or (x - y) % 6 == 0:
                t.px(x, y, az, 3)
    t.hlinha(16, 110, 62, bc, 0)
    t.ret(14, 68, 112, 72, vm, 2)
    t.hlinha(14, 112, 68, vm, 0)
    t.hlinha(14, 112, 69, vm, 1)
    t.hlinha(14, 112, 72, vm, 4)
    t.escurecer_ret(c0, ct, c1, ct + 2, 2, so_mat=az)
    # --- duas colunas inclinadas listradas de vermelho e branco ---
    for (xa, ya), (xb, yb) in (((19, base - 8), (12, 73)), ((24, base - 8), (34, 73))):
        n = int(math.hypot(xb - xa, yb - ya))
        for i in range(n + 1):
            s = i / n
            x = xa + (xb - xa) * s
            y = ya + (yb - ya) * s
            m_ = vm if (i // 5) % 2 == 0 else bc
            t.px(x - 1, y, m_, 1)
            t.px(x, y, m_, 2)
            t.px(x + 1, y, m_, 3)
    t.contorno()
    return t.imagem()


# ===============================================================================================================
# 6. Praça do Soldado: estátua no pedestal branco e o helicóptero com a bandeira do Brasil
# ===============================================================================================================

def estatua():
    L, A = 74, 156
    t = Tela(L, A, semente=66)
    cc = M['concreto']
    base = A - 1
    p0, p1 = 14, 59
    t.ret(p0, 74, p1, base, cc, 1)
    t.vlinha(p0, 74, base, cc, 0)
    t.ret(p1 - 9, 74, p1, base, cc, 2)
    t.vlinha(p1, 74, base, cc, 3)
    t.hlinha(p0, p1, 74, cc, 0)
    t.ret(p0 - 1, base - 4, p1 + 1, base, cc, 3)                    # sujeira de terra no pé
    t.hlinha(p0 - 1, p1 + 1, base - 4, cc, 2)
    t.manchas(p0 + 1, 76, p1 - 1, base - 4, cc, 8, tam=(3, 7))
    for x in range(p0 + 2, p1 - 1, 3):
        t.escorrido(x, 75, t.rnd.randint(4, 40), cc)
    t.manchas(p0 + 1, base - 16, p1 - 1, base - 5, cc, 10, tam=(2, 5))
    t.rachadura(p0 + 8, 120, 10, cc)
    t.rachadura(p1 - 6, 96, 7, cc)
    # placa de bronze
    t.ret(28, 84, 45, 95, M['bronze'], 3)
    t.relevo(t.mascara_ret(28, 84, 45, 95))
    for y in range(87, 94, 2):
        t.hlinha(30, 43, y, M['bronze'], 1)
    # base escura da estátua
    t.ret(p0 + 4, 69, p1 - 4, 73, M['bronze'], 3)
    t.hlinha(p0 + 4, p1 - 4, 69, M['bronze'], 2)
    t.hlinha(p0 + 4, p1 - 4, 73, M['bronze'], 4)
    t.contorno()
    img = t.imagem()
    img.alpha_composite(soldado(), (2, 0))
    return img


def helicoptero():
    L, A = 248, 112
    t = Tela(L, A, semente=77)
    hc, pr, gf = M['heli'], M['preto'], M['grafite']
    base = A - 1
    # --- base de concreto com faixa amarela ---
    t.ret(30, base - 9, 226, base, M['concreto'], 2)
    t.hlinha(30, 226, base - 9, M['concreto'], 0)
    t.hlinha(30, 226, base - 8, M['concreto'], 1)
    t.ret(30, base - 6, 226, base - 5, M['amarelo'], 1)
    t.hlinha(30, 226, base, M['concreto'], 4)
    # --- cone de cauda e deriva ---
    t.poli([(84, 48), (20, 52), (16, 60), (84, 72)], hc, 2)
    cauda = t.mascara_ret(10, 46, 86, 74) & (t.mat == hc)
    t.volume_h(cauda, hc)
    t.poli([(10, 20), (22, 22), (28, 54), (14, 60), (8, 56)], hc, 2)          # deriva
    t.vlinha(9, 22, 56, hc, 1)
    t.linha(22, 22, 28, 54, hc, 3)
    t.ret(26, 58, 44, 61, hc, 3)                                               # estabilizador
    t.hlinha(26, 44, 58, hc, 1)
    # rotor de cauda
    t.elipse(13, 30, 2.5, 2.5, gf, 2)
    t.linha(13, 16, 13, 44, gf, 3)
    t.linha(5, 30, 21, 30, gf, 3)
    # --- fuselagem ---
    corpo = t.poli([(70, 46), (96, 36), (196, 36), (214, 48), (226, 60), (228, 74), (220, 84),
                    (196, 90), (84, 90), (72, 80)], hc, 2)
    t.volume_h(corpo, hc, cortes=(0.08, 0.30, 0.62, 0.86))
    # nariz preto (radome)
    nariz = t.mascara_elipse(226, 70, 10, 13) & (xx_ := np.mgrid[0:A, 0:L][1]) >= 220
    t.aplicar(t.mascara_elipse(225, 70, 10, 12.5) & (np.mgrid[0:A, 0:L][1] >= 219), pr, 2)
    t.aplicar(t.mascara_elipse(223, 66, 5, 5) & (t.mat == pr), pr, 1)
    t.px(222, 63, pr, 0)
    # cabine de comando (vidros grandes)
    vid = t.poli([(186, 42), (206, 44), (218, 58), (216, 66), (190, 66)], M['vidro_escuro'], 2)
    t.aplicar(t.borda_de(vid, 'cima'), M['vidro_escuro'], 0)
    t.linha(200, 44, 202, 66, hc, 3, larg=2)
    t.linha(190, 46, 214, 62, M['vidro_escuro'], 1)
    t.linha(206, 48, 208, 52, M['vidro_escuro'], 0)
    # porta de correr e janelas da cabine
    t.ret(112, 46, 140, 84, hc, 2)
    t.vlinha(112, 46, 84, hc, 4)
    t.vlinha(140, 46, 84, hc, 4)
    t.hlinha(112, 140, 46, hc, 4)
    t.vlinha(113, 47, 84, hc, 1)
    for x0 in (118, 150, 166):
        t.ret(x0, 50, x0 + 11, 60, M['vidro_escuro'], 2)
        t.hlinha(x0, x0 + 11, 50, M['vidro_escuro'], 4)
        t.px(x0 + 2, 52, M['vidro_escuro'], 0); t.px(x0 + 3, 52, M['vidro_escuro'], 1)
        t.moldura(t.mascara_ret(x0, 50, x0 + 11, 60), hc, 4, 1)
    t.ret(178, 52, 186, 74, hc, 3)                                             # portinha do piloto
    t.vlinha(178, 52, 74, hc, 4)
    t.ret(180, 56, 185, 64, M['vidro_escuro'], 2)
    # linhas de painel e rebites
    for x in (96, 150, 176):
        t.vlinha(x, 40, 86, hc, 3)
    t.hlinha(84, 220, 76, hc, 3)
    for x in range(88, 210, 6):
        t.px(x, 78, hc, 1)
    # bandeira do Brasil na lateral
    fx, fy = 146, 64
    t.ret(fx, fy, fx + 17, fy + 11, M['folha'], 2)
    t.relevo(t.mascara_ret(fx, fy, fx + 17, fy + 11))
    t.poli([(fx + 2, fy + 5.5), (fx + 8.5, fy + 1.5), (fx + 15, fy + 5.5), (fx + 8.5, fy + 9.5)], M['amarelo'], 2)
    t.elipse(fx + 8.5, fy + 5.5, 3.2, 3.2, M['azul'], 2)
    t.hlinha(fx + 6, fx + 11, fy + 5, M['branco'], 0)
    # sponson (carenagem do trem) e rodas
    sp = t.poli([(118, 80), (176, 80), (184, 88), (180, 94), (124, 94), (116, 88)], hc, 2)
    t.volume_h(sp, hc, cortes=(0.15, 0.4, 0.7, 0.9))
    for wx, wy in ((136, 98), (168, 98), (204, 96)):
        t.elipse(wx, wy, 5, 5, pr, 2)
        t.elipse(wx - 1, wy - 1, 2.5, 2.5, pr, 1)
        t.px(wx - 1, wy - 1, gf, 0)
    t.vlinha(204, 88, 92, gf, 2)
    # --- motores, mastro e pás ---
    mot = t.poli([(104, 36), (110, 24), (178, 24), (188, 30), (188, 36)], hc, 2)
    t.volume_h(mot, hc, cortes=(0.15, 0.4, 0.7, 0.9))
    for ex in (176, 184):                                                      # saídas dos motores
        t.elipse(ex, 31, 3.5, 4, hc, 3)
        t.elipse(ex + 1, 31, 2, 2.5, pr, 3)
    t.ret(108, 28, 114, 33, gf, 3)                                             # grade de ar
    for y in range(28, 34, 2):
        t.hlinha(108, 114, y, gf, 1)
    t.ret(138, 14, 143, 24, gf, 2)                                             # mastro
    t.vlinha(138, 14, 24, gf, 1)
    t.ret(133, 12, 148, 16, gf, 2)                                             # cubo
    t.hlinha(133, 148, 12, gf, 0)
    # pás: duas compridas caindo (como paradas no chão) e uma encurtada
    t.linha(134, 14, 0, 26, pr, 2, larg=2)
    t.linha(134, 13, 0, 25, pr, 1)
    t.linha(148, 14, L - 1, 22, pr, 2, larg=2)
    t.linha(148, 13, L - 1, 21, pr, 1)
    t.linha(140, 12, 152, 4, pr, 2, larg=2)
    t.linha(138, 16, 118, 22, pr, 3, larg=2)
    t.contorno()
    return t.imagem()


def arvore(semente=88, L=128, A=150):
    t = Tela(L, A, semente=semente)
    tr = M['tronco']
    cx = L // 2
    # tronco com galhos
    t.ret(cx - 4, A - 60, cx + 4, A - 1, tr, 2)
    t.vlinha(cx - 4, A - 60, A - 1, tr, 1)
    t.ret(cx + 2, A - 60, cx + 4, A - 1, tr, 3)
    for (xa, ya, xb, yb) in ((cx, A - 50, cx - 26, A - 90), (cx, A - 56, cx + 24, A - 96), (cx, A - 60, cx + 2, A - 104)):
        t.linha(xa, ya, xb, yb, tr, 2, larg=3)
    t.ret(cx - 7, A - 3, cx + 7, A - 1, tr, 3)                                 # raízes
    t.manchas(cx - 4, A - 60, cx + 4, A - 1, tr, 8, tam=(1, 2))
    t.copa(cx, A - 100, L // 2 - 6, 46, M["folha"], n=40)
    t.contorno()
    return t.imagem()


# ===============================================================================================================
# Utilidades: Aladdin, tiles, céu, morros, casario
# ===============================================================================================================

def ler_matriz_js(caminho, nome_quadro):
    with open(caminho, encoding='utf-8') as f:
        s = f.read()
    pal = dict(re.findall(r"'(.)': '(#[0-9A-Fa-f]{6})'", s.split('export const PALETA')[1].split('};')[0]))
    bloco = re.search(nome_quadro + r': \[(.*?)\]', s, re.S).group(1)
    linhas = re.findall(r"'([^']*)'", bloco)
    return linhas, pal


def matriz_para_img(linhas, pal):
    img = Image.new('RGBA', (len(linhas[0]), len(linhas)), (0, 0, 0, 0))
    for y, l in enumerate(linhas):
        for x, c in enumerate(l):
            if c != '.':
                img.putpixel((x, y), hex_rgb(pal[c]) + (255,))
    return img


def aladdin():
    return matriz_para_img(*ler_matriz_js(os.path.join(REPO, 'src', 'art', 'jogador.js'), 'parado1'))


def tile(nome):
    return matriz_para_img(*ler_matriz_js(os.path.join(REPO, 'src', 'art', 'tiles.js'), nome))


def pe_do_heroi(img):
    """Linha do último pixel visível (pé) do quadro do herói."""
    a = np.array(img)[:, :, 3]
    return int(np.nonzero(a.any(axis=1))[0].max())


# ---------------------------------------------------------------------------------------------------------------
# Fundo: céu de entardecer em faixas, nuvens, Serra da Mantiqueira, casario e chão do jogo
# ---------------------------------------------------------------------------------------------------------------

CEU = ['#7C7CE0', '#8C8CF0', '#9E9EFF', '#B4A0F8', '#C8A2F0', '#DCA8E6', '#EDAFDC', '#F7B6D8', '#F9C4CC', '#F9D2BE']


def ceu(w, h=TELA_A):
    """Céu em faixas (sem degradê), com a borda de cada faixa em degraus de 2 px, como no guia."""
    a = np.zeros((h, w, 4), np.uint8)
    n = len(CEU)
    alto = 205  # o céu termina atrás dos morros e do casario
    for y in range(h):
        for xb in range(0, w, 8):
            f = y / alto + (0.012 if (xb // 8) % 2 else 0)
            i = min(n - 1, int(f * n))
            a[y, xb:xb + 8, :3] = hex_rgb(CEU[i])
    a[:, :, 3] = 255
    img = Image.fromarray(a, 'RGBA')
    d = ImageDraw.Draw(img)
    rnd = np.random.RandomState(5)
    for _ in range(max(2, w // 160)):  # nuvens compridas em faixas, como em snes-voo-pano-portao
        x, y = rnd.randint(-40, w), rnd.randint(18, 110)
        cw = rnd.randint(50, 110)
        for k, (dy, enc, c) in enumerate(((0, 0, '#F6D6F2'), (3, 8, '#E2C0EC'), (6, 18, '#C9A8E4'))):
            d.rectangle([x + enc - k * 6, y + dy, x + cw - enc + k * 4, y + dy + 2], fill=c)
        d.rectangle([x + 10, y - 2, x + cw - 30, y - 1], fill='#FBE6F6')
    return img


# Serra da Mantiqueira: 3 camadas verdes cobertas de mata. Quanto mais longe, mais azulada/lilás e com menos
# contraste (perspectiva atmosférica, guia: fundo com 2 a 3 tons). Cada rampa: luz, base, sombra, funda.
SERRA = [
    # (rampa, base da crista, amplitude, frequências, raio das copas)
    (['#B2CEBE', '#94B4A8', '#7E9C98', '#6E8890'], 132, 34, ((1.1, 1, 0.3), (2.7, 0.5, 1.2), (6.1, 0.15, 2)), 2.5),
    (['#9CC08C', '#7FA676', '#668C66', '#527458'], 160, 24, ((1.7, 1, 2.1), (4.3, 0.4, 0.7), (9.7, 0.12, 1)), 3.5),
    (['#86BA62', '#62994E', '#4A7C44', '#355E3A'], 188, 16, ((2.6, 1, 0.9), (6.2, 0.35, 2.4), (13, 0.1, 0.4)), 4.5),
]


def _copinha(a, cx, cy, r, rampa):
    """Copa de árvore redonda vista de longe: luz em cima à esquerda, sombra embaixo à direita."""
    h, w = a.shape[:2]
    x0, x1 = max(0, int(cx - r - 1)), min(w, int(cx + r + 2))
    y0, y1 = max(0, int(cy - r - 1)), min(h, int(cy + r + 2))
    if x0 >= x1 or y0 >= y1:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1]
    dx, dy = (xx + 0.5 - cx) / r, (yy + 0.5 - cy) / (r * 0.85)
    dentro = dx * dx + dy * dy <= 1
    luz = -dx * 0.6 - dy * 0.8
    tom = np.where(luz > 0.45, 0, np.where(luz > -0.15, 1, np.where(luz > -0.6, 2, 3)))
    cores = np.array([hex_rgb(c) for c in rampa], np.uint8)
    reg = a[y0:y1, x0:x1]
    reg[dentro, :3] = cores[tom[dentro]]
    reg[dentro, 3] = 255


def morros(w, h=TELA_A):
    """Serra da Mantiqueira ao fundo (Itajubá fica no pé dela): morros verdes cobertos de mata."""
    a = np.zeros((h, w, 4), np.uint8)
    rnd = np.random.RandomState(12)
    for rampa, base, amp, freqs, r in SERRA:
        def crista(x):
            return base - sum(amp * k * math.sin(x / 480 * math.pi * f + fa) for f, k, fa in freqs)
        cores = [hex_rgb(c) for c in rampa]
        # massa do morro: encosta virada para a luz (esquerda) mais clara, a outra na base
        for x in range(w):
            y = int(crista(x))
            a[y:, x, :3] = cores[2]
            a[y:, x, 3] = 255
        # encosta virada para a luz (morro subindo para a direita): copas um tom mais claras
        clara = [rampa[0], rampa[0], rampa[1], rampa[2]]

        def tons(xx):
            return clara if crista(xx + 6) < crista(xx - 6) else rampa
        # mata: copas encostadas umas nas outras na crista e espalhadas pela encosta
        passo = max(2, int(r * 1.3))
        for x in range(-4, w + 4, passo):
            xx = x + rnd.uniform(-1, 1)
            _copinha(a, xx, crista(xx) + rnd.uniform(-0.5, 1.5), r * rnd.uniform(0.8, 1.2), tons(xx))
        n = int(w * (h - base + amp) / (r * r * 4))
        for _ in range(n):
            xx = rnd.uniform(0, w)
            yy = crista(xx) + rnd.uniform(2, h - base + amp)
            if yy < h:
                _copinha(a, xx, yy, r * rnd.uniform(0.7, 1.15), tons(xx))
        # clareiras de pasto (manchas mais claras e lisas), só na camada do meio
        if r == 3.5:
            for _ in range(w // 220):
                cx, cy = rnd.uniform(0, w), 0
                cy = crista(cx) + rnd.uniform(10, 22)
                for yy in range(int(cy - 3), int(cy + 4)):
                    meia = int(14 * math.sqrt(max(0, 1 - ((yy - cy) / 4) ** 2)))
                    for xx in range(int(cx - meia), int(cx + meia)):
                        if 0 <= xx < w and 0 <= yy < h and a[yy, xx, 3]:
                            a[yy, xx, :3] = hex_rgb('#B6CC8A')
    return Image.fromarray(a, 'RGBA')


PAREDES = ['#F3E3C3', '#F6D7A8', '#EFC2C9', '#CFE0E8', '#E8B48A', '#F2EAD8', '#D8C8F0', '#C8E2C0']


def casa(semente, larg, alt):
    """Sobrado do casario de Itajubá (camada do meio), no mesmo padrão de tons e contorno dos lugares."""
    from cenario import material, rampa
    rnd = np.random.RandomState(semente)
    base_cor = PAREDES[semente % len(PAREDES)]
    pm = material('parede' + base_cor, rampa(base_cor))
    L, A = larg + 8, alt + 16
    t = Tela(L, A, semente=semente)
    br, tl = M['branco'], M['telha']
    topo = A - alt
    t.parede(4, topo, L - 5, A - 1, pm, 1)
    t.escurecer_ret(L - 9, topo, L - 5, A - 1, 1, so_mat=pm)
    t.ret(4, A - 12, L - 5, A - 1, pm, 3)                            # barra de baixo
    t.hlinha(4, L - 5, A - 12, br, 1)
    platibanda = rnd.rand() < 0.35
    if platibanda:
        t.ret(2, topo - 6, L - 3, topo, br, 1)
        t.relevo(t.mascara_ret(2, topo - 6, L - 3, topo))
        t.escurecer_ret(4, topo + 1, L - 5, topo + 2, 1)
    else:
        t.poli([(0, topo + 1), (8, topo - 13), (L - 9, topo - 13), (L - 1, topo + 1)], tl, 2)
        for y in range(topo - 12, topo + 1):
            for x in range(L):
                if t.mat[y, x] == tl:
                    if (y - topo) % 3 == 0:
                        t.tom[y, x] = 3
                    elif (x + (y // 3) * 2) % 5 == 0:
                        t.tom[y, x] = 1
        t.hlinha(1, L - 2, topo - 13, tl, 1)
        t.ret(0, topo + 1, L - 1, topo + 2, tl, 4)
        t.escurecer_ret(4, topo + 3, L - 5, topo + 4, 1)
    andares = 2 if alt > 64 else 1
    cols = max(2, larg // 24)
    for a in range(andares):
        for c in range(cols):
            jx = int(4 + (c + 0.5) * (L - 8) / cols - 6)
            jy = topo + 10 + a * 30
            if a == andares - 1 and c == cols // 2:
                continue  # porta no lugar
            if rnd.rand() < 0.5:
                t.veneziana(jx, jy, jx + 11, jy + 17, 'branco' if rnd.rand() < 0.6 else 'madeira')
            else:
                t.janela_grade(jx, jy, jx + 11, jy + 17, colunas=2, linhas=2)
            t.ret(jx - 1, jy + 18, jx + 12, jy + 19, br, 2)
    dx = int(4 + (cols // 2 + 0.5) * (L - 8) / cols - 7)
    t.ret(dx - 2, A - 30, dx + 15, A - 1, br, 1)
    t.relevo(t.mascara_ret(dx - 2, A - 30, dx + 15, A - 1))
    t.ret(dx, A - 28, dx + 13, A - 1, M['madeira'], 2)
    t.vlinha(dx + 6, A - 26, A - 1, M['madeira'], 4)
    t.relevo(t.mascara_ret(dx, A - 28, dx + 13, A - 1))
    t.reboco(5, topo + 1, L - 6, A - 13, pm, n=3)
    t.contorno()
    return t.imagem()


def casario(w, semente=1, base=246):
    img = Image.new('RGBA', (w, TELA_A), (0, 0, 0, 0))
    x, i = -10, 0
    while x < w:
        larg = [56, 72, 48, 64, 80][(semente + i) % 5]
        alt = [58, 74, 50, 66, 82][((semente + i) * 3) % 5]
        c = casa(semente * 31 + i, larg, alt)
        img.alpha_composite(c, (x, base - c.height))
        x += c.width - 2 + ((i * 7) % 3) * 6
        i += 1
    return img


def tingir(img, cor, t):
    """Puxa a camada para a cor do ar (profundidade: fundo menos contrastado e mais lilás)."""
    a = np.array(img).astype(float)
    c = np.array(hex_rgb(cor), float)
    a[:, :, :3] = a[:, :, :3] * (1 - t) + c * t
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), 'RGBA')


# Chão de paralelepípedo (rua de Itajubá): meio-fio de granito no alto e pedras em fiadas desencontradas.
# Tiles de 16x16 como os do jogo, em 3 variações para a repetição não aparecer.
PEDRA = {   # granito cinza aquecido pelo entardecer: luz, base, sombra, junta, contorno
    'fria': ['#DCD2D6', '#B6AAB4', '#8E8292', '#5E5268', '#3A3044'],
    'quente': ['#E2CDBE', '#BCA294', '#937A74', '#5E5268', '#3A3044'],
    'escura': ['#B8ACB6', '#968A98', '#766A7E', '#5E5268', '#3A3044'],
}


def tiles_paralelepipedo(semente):
    rnd = np.random.RandomState(semente)
    topo = np.zeros((16, 16, 4), np.uint8)
    meio = np.zeros((16, 16, 4), np.uint8)
    for t_, y_ini in ((topo, 5), (meio, 0)):
        t_[:, :, 3] = 255
        t_[:, :, :3] = hex_rgb(PEDRA['fria'][3])          # junta
        for fiada in range((16 - y_ini) // 4 + 1):
            y0 = y_ini + fiada * 4
            desloc = 4 if (fiada + (0 if t_ is topo else 1)) % 2 else 0
            for x0 in range(-8 + desloc, 16, 8):
                c = PEDRA[rnd.choice(['fria', 'fria', 'quente', 'escura'])]
                for y in range(y0, min(16, y0 + 3)):
                    for x in range(x0, x0 + 7):
                        if not 0 <= x < 16:
                            continue
                        if y == y0 and x < x0 + 6:
                            tom = 0                          # aresta de cima pega luz
                        elif x == x0 + 6 or y == y0 + 2:
                            tom = 2                          # lado e pé na sombra
                        else:
                            tom = 1
                        if (x == x0 and y == y0) or (x == x0 + 6 and y == y0 + 2):
                            continue                         # cantos arredondados
                        t_[y, x, :3] = hex_rgb(c[tom])
                if rnd.rand() < 0.4:                         # desgaste: um pontinho escuro na pedra
                    xx, yy = x0 + rnd.randint(1, 5), y0 + 1
                    if 0 <= xx < 16 and yy < 16:
                        t_[yy, xx, :3] = hex_rgb(c[2])
    # meio-fio de granito claro no alto do tile de cima
    gr = ['#3A3044', '#FBF2E0', '#EADBC0', '#AE9878', '#6E5E58']
    for y, c in enumerate(gr):
        topo[y, :, :3] = hex_rgb(c)
    for x in range(0, 16, 8):                                # juntas do meio-fio
        topo[1:4, x, :3] = hex_rgb('#AE9878')
    return Image.fromarray(topo, 'RGBA'), Image.fromarray(meio, 'RGBA')


TILES_RUA = [tiles_paralelepipedo(s) for s in (1, 2, 3)]


def chao(w):
    img = Image.new('RGBA', (w, TELA_A), (0, 0, 0, 0))
    rnd = np.random.RandomState(7)
    for x in range(0, w, 16):
        topo, _ = TILES_RUA[rnd.randint(3)]
        _, meio = TILES_RUA[rnd.randint(3)]
        img.alpha_composite(topo, (x, CHAO_Y))
        img.alpha_composite(meio, (x, CHAO_Y + 16))
    return img


def heroi_em(img, x):
    h = aladdin()
    img.alpha_composite(h, (int(x), CHAO_Y - pe_do_heroi(h) - 1))


# ---------------------------------------------------------------------------------------------------------------
# Tira panorâmica e telas
# ---------------------------------------------------------------------------------------------------------------

def panorama():
    W = 2800
    img = ceu(W)
    img.alpha_composite(morros(W))
    fundo = Image.new('RGBA', (W, TELA_A), (0, 0, 0, 0))
    fundo.alpha_composite(casario(W, semente=3), (0, 0))
    # 1. Clube Itajubense no fundo (camada do meio, atrás do casario da frente)
    cl = clube()
    fundo.alpha_composite(cl, (110, 246 - cl.height + 4))
    img.alpha_composite(tingir(fundo, '#B89AD8', 0.16))
    frente = Image.new('RGBA', (W, TELA_A), (0, 0, 0, 0))
    lugares = {}

    def por(nome, im, x, y=None):
        frente.alpha_composite(im, (x, CHAO_Y - im.height if y is None else y))
        lugares[nome] = x + im.width // 2

    lugares['clube'] = 110 + cl.width // 2
    por('fonte', fonte(), 640)
    por('cafe', cafe(), 1060)
    por('igreja', igreja(), 1500)
    por('posto', posto(), 1960)
    arv = arvore()
    frente.alpha_composite(tingir(arv, '#B89AD8', 0.08), (2470, CHAO_Y - arv.height))
    frente.alpha_composite(tingir(arvore(semente=89, L=110, A=128), '#B89AD8', 0.08), (2600, CHAO_Y - 128))
    por('soldado', estatua(), 2330)
    por('helicoptero', helicoptero(), 2440)
    lugares['soldado'] = 2330 + 130
    img.alpha_composite(frente)
    img.alpha_composite(chao(W))
    for x in (60, 590, 1010, 1440, 1920, 2290):
        heroi_em(img, x)
    return img, lugares


def rotulo(d, xy, texto, tam=22, cor=(255, 255, 255), negrito=True):
    f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if negrito else ''), tam)
    d.text(xy, texto, font=f, fill=cor)


def telas(pan, lugares):
    """6 telas de 480x270 (o que o jogador vê), uma por lugar, ampliadas 2x."""
    ordem = [('clube', '1. Clube Itajubense (fundo)'), ('fonte', '2. Fonte da praça e busto'),
             ('cafe', '3. Café do Vadinho'), ('igreja', '4. Igreja Matriz'),
             ('posto', '5. Posto Esso, o menor do mundo'), ('soldado', '6. Praça do Soldado')]
    k, gap, topo = 2, 16, 40
    W = 2 * TELA_L * k + 3 * gap
    H = 3 * (TELA_A * k + topo) + 2 * gap + 60
    out = Image.new('RGBA', (W, H), (34, 26, 48, 255))
    d = ImageDraw.Draw(out)
    rotulo(d, (gap, 14), 'Fase 1 · os 6 lugares na tela do jogo (480×270, ampliado 2×; herói = 58 px)', 24)
    for i, (nome, titulo) in enumerate(ordem):
        cx = lugares[nome]
        x0 = max(0, min(pan.width - TELA_L, cx - TELA_L // 2))
        crop = pan.crop((x0, 0, x0 + TELA_L, TELA_A)).resize((TELA_L * k, TELA_A * k), Image.NEAREST)
        col, lin = i % 2, i // 2
        X = gap + col * (TELA_L * k + gap)
        Y = 60 + lin * (TELA_A * k + topo + gap)
        rotulo(d, (X, Y + 4), titulo, 22, (255, 214, 251))
        out.alpha_composite(crop, (X, Y + topo))
    return out


# ---------------------------------------------------------------------------------------------------------------
# Pranchas: foto × pixel art (mesma altura) × Aladdin
# ---------------------------------------------------------------------------------------------------------------

def cena(objetos, larg, heroi_x, alt=None):
    """Cena curta na resolução do jogo: céu, chão do jogo, os objetos e o herói. objetos: [(img, x)]."""
    topo_obj = min(CHAO_Y - im.height for im, _ in objetos)
    y0 = max(0, topo_obj - 10)
    img = ceu(larg)
    img.alpha_composite(morros(larg))
    for im, x in objetos:
        img.alpha_composite(im, (x, CHAO_Y - im.height))
    img.alpha_composite(chao(larg))
    heroi_em(img, heroi_x)
    return img.crop((0, y0, larg, TELA_A))


def prancha(arquivo, titulo, fotos, cena_img, notas, alvo=780):
    k = max(2, round(alvo / cena_img.height))
    pix = cena_img.resize((cena_img.width * k, cena_img.height * k), Image.NEAREST)
    H = pix.height
    fts = []
    for f in fotos:
        im = Image.open(os.path.join(REPO, 'references', 'lugares', f)).convert('RGBA')
        fts.append(im.resize((round(im.width * H / im.height), H), Image.LANCZOS))
    gap, topo = 20, 64
    W = sum(f.width for f in fts) + pix.width + gap * (len(fts) + 2)
    alt_notas = 34 * len(notas) + 30
    out = Image.new('RGBA', (W, H + topo + alt_notas + gap), (34, 26, 48, 255))
    d = ImageDraw.Draw(out)
    rotulo(d, (gap, 18), titulo, 26)
    x = gap
    for f, nome in zip(fts, fotos):
        out.alpha_composite(f, (x, topo))
        rotulo(d, (x + 8, topo + H - 30), 'foto: ' + nome, 16, (255, 255, 255), False)
        x += f.width + gap
    out.alpha_composite(pix, (x + gap, topo))
    rotulo(d, (x + gap + 8, topo + 8), f'pixel art do jogo, ampliada {k}× (Aladdin com 58 px para escala)', 16,
           (46, 26, 51), True)
    y = topo + H + 16
    for n in notas:
        rotulo(d, (gap, y), n, 20, (240, 230, 255), False)
        y += 34
    out.save(os.path.join(SAIDA, arquivo))
    return out


NOTAS = {
    'clube': [
        'Fiel: prédio creme de 2 andares, 4 colunas jônicas sobre pedestais de pedra escura, 3 portas (uma aberta), janelas brancas',
        'quadriculadas, platibanda com balaústres e o ático central, inscrição CLUB ITAJUBENSE no friso, rodapé de mármore com veios.',
        'Simplificado: menos janelas por ala (2+2), escala reduzida por ser camada de fundo; prédio vizinho, postes e fios ficaram de fora.'],
    'fonte': [
        'Fiel: fonte grande e baixa com borda clara, 14 jatos em arco caindo para o centro, pedestal claro com placa de bronze e o busto',
        'de bronze no alto. Simplificado: vista de lado (elipse achatada); o rosto do busto não tem traços (a foto não mostra de perto).',
        'No jogo, a borda vira plataforma e os jatos podem ter 2 quadros de animação.'],
    'cafe': [
        'Fiel: fachada creme com 3 janelas de veneziana branca e pilastras, toldo curvo cinza com armação escura e a placa oval preta',
        '"Café do Vadinho", loja à sombra com balcão, mesinhas e cadeiras dobráveis de madeira, cavalete com o cardápio, planta no vaso.',
        'Simplificado: a lotérica vizinha virou só uma placa clara sem nome; pessoas ficaram de fora. O toldo pode ser um toldo que quica.'],
    'igreja': [
        'Fiel: torre central alta com relógio e imagem no topo, duas torres laterais com frontão e cruz, rosácea, 3 portas em arco',
        '(a do meio com bandeira dourada), frisos e pilastras brancas, arcatura sob as cornijas, escadaria larga com corrimãos.',
        'Simplificado: altura comprimida para caber na tela (portas do tamanho do herói); ornamentos finos viraram 1 a 2 px.'],
    'posto': [
        'Fiel: cabine minúscula branca de azulejos, beiral vermelho com platibanda de losangos, 2 colunas inclinadas listradas, painel de',
        'pedra com moldura vermelha, janelas quadriculadas, plataforma com meio-fio amarelo, placa oval alta no poste com a treliça.',
        'Placa: oval com aro azul e ESSO em vermelho no campo branco (decisão do Pedro), com letras de pixel nossas, sem decalcar o logotipo.'],
    'soldado': [
        'Fiel: soldado de bronze de capacete apontando com o braço direito, fuzil em pé ao lado, cinto com cartucheiras, pedestal branco',
        'alto e manchado com placa; helicóptero cinza-claro com nariz preto, cabine envidraçada, motores, pás caídas e a bandeira do Brasil.',
        'Simplificado: helicóptero comprimido (cerca de 4 alturas do herói) e de perfil; árvores do fundo genéricas; sem inscrições.'],
}

if __name__ == '__main__':
    os.makedirs(NATIVO, exist_ok=True)
    for nome, f in (('clube', clube), ('fonte', fonte), ('cafe', cafe), ('igreja', igreja), ('posto', posto),
                    ('estatua', estatua), ('helicoptero', helicoptero), ('arvore', arvore)):
        img = f()
        img.save(os.path.join(NATIVO, nome + '.png'))
        print(nome, img.size, contar_cores(img), 'cores')
    folha = Image.new('RGBA', (16 * 3, 32))
    for i, (tp, md) in enumerate(TILES_RUA):
        folha.alpha_composite(tp, (16 * i, 0))
        folha.alpha_composite(md, (16 * i, 16))
    folha.save(os.path.join(NATIVO, 'tiles-paralelepipedo.png'))
    pan, lugares = panorama()
    pan.resize((pan.width * 2, pan.height * 2), Image.NEAREST).save(os.path.join(SAIDA, 'fase1-panorama.png'))
    telas(pan, lugares).save(os.path.join(SAIDA, 'fase1-telas.png'))
    larg = lambda *ims: sum(im.width for im in ims)
    cl, fo, ca, ig, po = clube(), fonte(), cafe(), igreja(), posto()
    prancha('1-clube-itajubense.png', '1 · Clube Itajubense (fundo do começo da fase)', ['1-clube-itajubense.jpg'],
            cena([(cl, 70)], cl.width + 90, 8), NOTAS['clube'])
    prancha('2-fonte-busto.png', '2 · Fonte da praça com o busto do Teodomiro Santiago',
            ['2-fonte-praca-busto-teodomiro-santiago.jpg'], cena([(fo, 70)], fo.width + 90, 10), NOTAS['fonte'])
    prancha('3-cafe-do-vadinho.png', '3 · Café do Vadinho', ['3-cafe-do-vadinho.jpg'],
            cena([(ca, 70)], ca.width + 90, 10), NOTAS['cafe'])
    prancha('4-igreja-matriz.png', '4 · Igreja Matriz', ['4-igreja-matriz-1.jpg', '4-igreja-matriz-2.jpg'],
            cena([(ig, 70)], ig.width + 90, 10), NOTAS['igreja'])
    prancha('5-posto-menor-do-mundo.png', '5 · Posto Esso, "o menor posto de gasolina do mundo"',
            ['5-posto-esso-menor-do-mundo.jpg'], cena([(po, 70)], po.width + 90, 10), NOTAS['posto'])
    es, he, ar = estatua(), helicoptero(), arvore()
    prancha('6-praca-do-soldado.png', '6 · Praça do Soldado: estátua e helicóptero',
            ['6-praca-do-soldado-estatua-1.jpg', '6-praca-do-soldado-estatua-2.jpg', '6-praca-do-soldado-helicoptero.jpg'],
            cena([(tingir(ar, '#B89AD8', 0.08), 200), (es, 70), (he, 150)], 410, 10), NOTAS['soldado'], alvo=640)
    print('pranchas prontas em', SAIDA)
