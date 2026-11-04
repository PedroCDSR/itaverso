"""Cenários e objetos novos do ITAMANIA (fases 1 a 4), com as ferramentas de cenario.py.

Linguagem visual (a mesma dos cenários de Itajubá já feitos): 4 a 5 tons por material, luz de cima e da esquerda,
contorno colorido de 1 px, sombras puxadas para o roxo, reboco com desgaste.

Saída: public/assets/cenario/*.png (prédios) e public/assets/sprites/*.png (objetos animados, quadros lado a lado).
Uso: python3 ferramentas/arte/gerar_cenarios.py   (dentro de itamania/)
"""
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cenario  # noqa: E402
from cenario import M, Tela, material  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CEN = os.path.join(RAIZ, 'public/assets/cenario')
SPR = os.path.join(RAIZ, 'public/assets/sprites')
os.makedirs(CEN, exist_ok=True)
os.makedirs(SPR, exist_ok=True)

# letras que faltavam na fonte de placas (3x5)
cenario.FONTE.update({
    'K': ['#.#', '#.#', '##.', '#.#', '#.#'],
    'Q': ['.#.', '#.#', '#.#', '##.', '.##'],
    'W': ['#...#', '#...#', '#.#.#', '##.##', '#...#'],
    'X': ['#.#', '#.#', '.#.', '#.#', '#.#'],
    'Y': ['#.#', '#.#', '.#.', '.#.', '.#.'],
    'Z': ['###', '..#', '.#.', '#..', '###'],
    'Á': ['.#.', '###', '#.#', '###', '#.#'],
    'Ó': ['.#.', '###', '#.#', '#.#', '###'],
    'Ç': ['.##', '#..', '#..', '.##', '.#.'],
    '0': ['###', '#.#', '#.#', '#.#', '###'], '1': ['.#', '##', '.#', '.#', '.#'],
    '2': ['##.', '..#', '.#.', '#..', '###'], '3': ['##.', '..#', '.#.', '..#', '##.'],
    '4': ['#.#', '#.#', '###', '..#', '..#'], '5': ['###', '#..', '##.', '..#', '##.'],
    '6': ['.##', '#..', '###', '#.#', '###'], '7': ['###', '..#', '.#.', '.#.', '.#.'],
    '8': ['###', '#.#', '###', '#.#', '###'], '9': ['###', '#.#', '###', '..#', '##.'],
    ':': ['.', '#', '.', '#', '.'], '.': ['.', '.', '.', '.', '#'], '-': ['...', '...', '###', '...', '...'],
    'b': ['#..', '#..', '##.', '#.#', '##.'], 'e': ['...', '.#.', '#.#', '##.', '.##'],
    'r': ['...', '#.#', '##.', '#..', '#..'], 's': ['...', '.##', '##.', '.##', '##.'],
    'u': ['...', '#.#', '#.#', '#.#', '.##'], 'g': ['...', '.##', '#.#', '.##', '##.'],
    'c': ['...', '.##', '#..', '#..', '.##'], 'm': ['.....', '####.', '#.#.#', '#.#.#', '#.#.#'],
    'l': ['#', '#', '#', '#', '#'], 't': ['.#.', '###', '.#.', '.#.', '.##'], 'p': ['...', '##.', '#.#', '##.', '#..'],
    'j': ['.#', '..', '.#', '.#', '##'], 'k': ['#..', '#.#', '##.', '#.#', '#.#'],
})

M['jeans'] = material('jeans', ['#C4DAFF', '#8FB6F0', '#4F7FC9', '#335AA0', '#22386E', '#121C3E'])
M['verde_trem'] = material('verde_trem', ['#B4E0A4', '#7CB878', '#4E8C58', '#336646', '#20442E', '#10241A'])
M['vinho'] = material('vinho', ['#F0A0A8', '#C8606C', '#9A3A4A', '#702634', '#481622', '#280A12'])
M['ferro'] = material('ferro', ['#9C98A8', '#6E6A7C', '#4C4858', '#363240', '#24202C', '#120E18'])
M['pao'] = material('pao', ['#FFF4C8', '#FBD98A', '#E8B45A', '#C2853A', '#8C5A24', '#4E2E10'])
M['cafe'] = material('cafe', ['#F8E2C4', '#E2BC8C', '#C08E5C', '#8E6038', '#5E3C22', '#341E0E'])
M['pena'] = material('pena', ['#F4F2FA', '#C8C6D8', '#9C9AB4', '#74728E', '#504E68', '#2C2A40'])
M['ceramica'] = material('ceramica', ['#FFFFFF', '#F6F0F0', '#DCD2D8', '#B4A8B8', '#86788E', '#4A3E58'])


def salvar(t, nome, pasta=CEN):
    t.contorno()
    img = t.imagem()
    img.save(os.path.join(pasta, nome + '.png'), optimize=True)
    return img


def folha(quadros, nome):
    """quadros: lista de Telas do mesmo tamanho -> PNG com os quadros lado a lado."""
    imgs = []
    for t in quadros:
        t.contorno()
        imgs.append(t.imagem())
    w, h = imgs[0].size
    out = Image.new('RGBA', (w * len(imgs), h), (0, 0, 0, 0))
    for i, im in enumerate(imgs):
        out.alpha_composite(im, (i * w, 0))
    out.save(os.path.join(SPR, nome + '.png'), optimize=True)
    return out


def placa_texto(t, cx, y, s, mat, tom, sombra=None, escala=1):
    w = cenario.largura_texto(s) * escala
    t.texto(int(cx - w / 2), y, s, mat, tom, sombra=sombra, escala=escala)


# =================================================================================== fase 1: rodoviária e trem

def rodoviaria():
    """Terminal rodoviário: prédio baixo e comprido de concreto, marquise ondulada, letreiro com relógio, vidraças e
    plataformas numeradas. Desenho genérico de rodoviária de cidade mineira (sem foto de referência do prédio)."""
    L, A = 400, 150
    t = Tela(L, A, semente=7)
    co, br, vd, gf = M['concreto'], M['branco'], M['vidro'], M['grafite']
    base = A - 1
    # corpo do prédio
    t.parede(10, 64, L - 11, base, co, 2)
    t.reboco(12, 66, L - 13, base - 2, co, n=30)
    # faixa de vidraças (reflete o céu da manhã)
    t.ret(18, 74, L - 19, 104, M['vidro_azul'], 2)
    for x in range(18, L - 18, 22):
        t.vlinha(x, 74, 104, br, 2)
        t.vlinha(x + 1, 74, 104, br, 3)
        t.px(x + 6, 76, M['vidro_azul'], 0); t.px(x + 7, 77, M['vidro_azul'], 0); t.px(x + 8, 78, M['vidro_azul'], 0)
    t.hlinha(18, L - 19, 89, br, 2)
    # portas de vidro e guichês
    for x in (60, 190, 320):
        t.ret(x, 112, x + 28, base, M['vidro_escuro'], 2)
        t.vlinha(x + 14, 112, base, gf, 2)
        t.relevo(t.mascara_ret(x, 112, x + 28, base))
    for i, x in enumerate((110, 140, 240, 270)):
        t.ret(x, 116, x + 22, 132, M['interior'], 2)
        t.ret(x + 2, 118, x + 20, 122, M['amarelo'], 1)
        t.ret(x - 1, 133, x + 23, 136, br, 1)
    # marquise ondulada (laje em arcos, marca das rodoviárias dos anos 70)
    for x0 in range(0, L, 40):
        m = t.mascara_elipse(x0 + 20, 58, 22, 10) & t.mascara_ret(x0, 40, x0 + 39, 58)
        t.aplicar(m, br, 1)
        t.relevo(m)
    t.ret(0, 56, L - 1, 63, br, 2)
    t.hlinha(0, L - 1, 56, br, 0)
    t.hlinha(0, L - 1, 63, br, 4)
    t.escurecer_ret(10, 64, L - 11, 68, 1, so_mat=co)
    # pilares da marquise
    for x in range(14, L - 10, 64):
        t.cilindro(x, x + 5, 64, base, br)
    # letreiro com relógio
    t.ret(140, 20, 260, 44, gf, 2)
    t.relevo(t.mascara_ret(140, 20, 260, 44))
    placa_texto(t, 192, 27, 'RODOVIÁRIA', M['amarelo'], 1, sombra=(gf, 4), escala=2)
    t.elipse(250, 32, 8, 8, br, 1)
    t.elipse(250, 32, 6, 6, br, 0)
    t.vlinha(250, 27, 32, gf, 3); t.hlinha(250, 254, 32, gf, 3)
    t.ret(198, 44, 202, 55, gf, 3)
    # números das plataformas
    for i, x in enumerate(range(30, L - 30, 64)):
        t.ret(x, 66, x + 12, 72, M['azul'], 2)
        placa_texto(t, x + 7, 67, str(i + 1), br, 0)
    # banco e lixeira
    t.ret(150, base - 8, 180, base - 6, M['madeira'], 2)
    t.vlinha(152, base - 5, base, gf, 3); t.vlinha(178, base - 5, base, gf, 3)
    t.ret(300, base - 12, 306, base, M['laranja'], 2)
    return salvar(t, 'rodoviaria')


def onibus():
    """Ônibus de viagem genérico (sem marca): branco com faixas nas cores do jogo e letreiro 'ITAJUBÁ'."""
    L, A = 168, 66
    t = Tela(L, A, semente=3)
    br, vd, gf = M['branco'], M['vidro_escuro'], M['grafite']
    corpo = t.poli([(4, 8), (156, 8), (164, 18), (164, 56), (4, 56)], br, 1)
    t.relevo(corpo)
    t.ret(4, 8, 158, 10, br, 0)
    t.ret(8, 16, 150, 34, vd, 2)                       # janelas
    for x in range(8, 150, 20):
        t.vlinha(x, 16, 34, gf, 4)
        t.px(x + 3, 18, vd, 0); t.px(x + 4, 19, vd, 0)
    t.poli([(152, 14), (160, 20), (162, 36), (152, 36)], vd, 1)   # para-brisa
    t.ret(4, 38, 164, 42, M['laranja'], 2)             # faixas
    t.ret(4, 43, 164, 45, M['rosa'], 2)
    t.ret(30, 46, 58, 54, gf, 3)                       # bagageiro
    t.ret(90, 46, 118, 54, gf, 3)
    t.ret(138, 20, 148, 54, vd, 3)                     # porta
    t.ret(108, 10, 150, 14, gf, 4)                     # letreiro
    placa_texto(t, 129, 10, 'ITAJUBÁ', M['laranja'], 1)
    for x in (30, 132):                                # rodas
        t.elipse(x, 57, 8, 8, M['preto'], 2)
        t.elipse(x, 57, 4, 4, M['ferro'], 1)
        t.px(x - 1, 55, M['ferro'], 0)
    t.ret(160, 46, 164, 50, M['amarelo'], 0)           # farol
    return salvar(t, 'onibus')


def locomotiva():
    """Locomotiva a vapor de museu (verde e preta, rodas vermelhas), virada para a esquerda. Desenho próprio de uma
    locomotiva genérica das ferrovias mineiras; a história da peça real ainda está 'a pesquisar' (DESIGN.md)."""
    L, A = 144, 96
    t = Tela(L, A, semente=11)
    pr, vm, vt, gf, dr = M['preto'], M['vermelho'], M['verde_trem'], M['grafite'], M['dourado']
    base = A - 1
    # cabine (atrás, à direita): teto em y=30, plataforma de cima do jogo
    t.ret(96, 30, 140, 74, vt, 2)
    t.relevo(t.mascara_ret(96, 30, 140, 74))
    t.ret(92, 26, 143, 31, pr, 2)                     # teto
    t.hlinha(92, 143, 26, pr, 0)
    t.ret(104, 38, 130, 54, M['vidro_escuro'], 2)     # janela
    t.vlinha(117, 38, 54, vt, 3)
    t.ret(98, 58, 138, 60, dr, 1)                     # friso dourado
    # caldeira: cilindro deitado, topo em y=44
    for y in range(44, 72):
        f = (y - 44) / 28
        tom = 1 if f < 0.18 else 0 if f < 0.32 else 2 if f < 0.7 else 3
        t.hlinha(18, 96, y, pr, tom)
    for x in (34, 56, 78):                            # cintas douradas
        t.vlinha(x, 44, 71, dr, 2)
    t.ret(10, 40, 20, 74, pr, 3)                      # frente da caldeira
    t.elipse(14, 56, 5, 12, gf, 2)
    t.elipse(14, 54, 3, 3, M['amarelo'], 0)           # farol
    # chaminé e domos
    t.ret(26, 18, 36, 44, pr, 2)
    t.ret(23, 14, 39, 19, pr, 1)
    t.relevo(t.mascara_ret(23, 14, 39, 19))
    t.elipse(58, 42, 6, 5, dr, 1)
    t.elipse(76, 42, 5, 4, pr, 1)
    # estrado e limpa-trilhos
    t.ret(6, 74, 142, 79, gf, 3)
    t.hlinha(6, 142, 74, gf, 1)
    t.poli([(0, base - 2), (12, 76), (14, base - 2)], vm, 2)
    for x in range(2, 13, 3):
        t.vlinha(x, 80, base - 3, vm, 3)
    # rodas vermelhas com biela
    for x, r in ((34, 9), (58, 9), (82, 9), (116, 7), (132, 7)):
        t.elipse(x, base - r, r, r, vm, 2)
        t.elipse(x, base - r, r - 3, r - 3, vm, 1)
        t.elipse(x, base - r, 2, 2, gf, 1)
        t.px(x - 2, base - r - 2, vm, 0)
    t.ret(32, base - 10, 84, base - 8, M['ferro'], 1)
    # placa do museu
    t.ret(100, 64, 136, 72, gf, 2)
    placa_texto(t, 118, 66, 'MUSEU', M['amarelo'], 1)
    t.reboco(20, 46, 94, 70, pr, n=10)
    return salvar(t, 'locomotiva')


def vagao(n):
    """Vagão de passageiros de madeira (vinho e creme), teto arredondado de chapa: a plataforma de cima."""
    L, A = 120, 72
    t = Tela(L, A, semente=20 + n)
    vh, cr, gf, fe = M['vinho'], M['creme'], M['grafite'], M['ferro']
    base = A - 1
    t.ret(4, 14, L - 5, 56, vh, 2)
    t.relevo(t.mascara_ret(4, 14, L - 5, 56))
    for x in range(6, L - 6, 4):                      # tábuas
        t.vlinha(x, 36, 55, vh, 3)
    t.ret(4, 18, L - 5, 34, cr, 1)                    # faixa creme das janelas
    for x in range(10, L - 14, 18):
        t.ret(x, 20, x + 11, 32, M['vidro'], 2)
        t.hlinha(x, x + 11, 20, M['vidro'], 0)
        t.relevo(t.mascara_ret(x, 20, x + 11, 32))
    # teto arredondado (topo em y=6)
    m = t.mascara_elipse(L / 2, 18, L / 2 + 4, 12) & t.mascara_ret(0, 4, L - 1, 14)
    t.aplicar(m, gf, 2)
    t.relevo(m)
    t.hlinha(2, L - 3, 14, gf, 4)
    t.ret(0, 56, L - 1, 60, fe, 3)                    # chassi
    t.hlinha(0, L - 1, 56, fe, 1)
    for x in (20, 36, L - 37, L - 21):                # truques
        t.elipse(x, base - 6, 6, 6, M['preto'], 2)
        t.elipse(x, base - 6, 2, 2, fe, 1)
    t.ret(L - 4, 46, L - 1, 52, fe, 2)                # engate
    t.ret(0, 46, 3, 52, fe, 2)
    placa_texto(t, L // 2, 40, f'0{n}', M['dourado'], 1)
    return salvar(t, f'vagao{n}')


# =================================================================================== fase 3: Rua Nova

def loja(nome_placa, semente, cor_parede, cor_placa, vitrine, L=150, A=140, real=False):
    """Fachada de loja de rua central: sobrado com platibanda, letreiro, vitrine e porta de enrolar."""
    t = Tela(L, A, semente=semente)
    pa, br, gf = M[cor_parede], M['branco'], M['grafite']
    base = A - 1
    t.parede(4, 10, L - 5, base, pa, 2)
    t.cornija(0, L - 1, 6, br, alt=4)
    t.ret(2, 0, L - 3, 5, pa, 1)
    t.relevo(t.mascara_ret(2, 0, L - 3, 5))
    for x in (20, L - 50):                            # janelas do andar de cima
        t.janela_grade(x, 18, x + 30, 52, colunas=2, linhas=3)
    t.reboco(6, 12, L - 7, 64, pa, n=14)
    # letreiro
    t.ret(8, 64, L - 9, 84, M[cor_placa], 2)
    t.relevo(t.mascara_ret(8, 64, L - 9, 84))
    esc = 2 if cenario.largura_texto(nome_placa) * 2 < L - 24 else 1
    placa_texto(t, L // 2, 70 if esc == 2 else 72, nome_placa, br, 0, sombra=(M[cor_placa], 4), escala=esc)
    # vitrine e porta
    t.ret(8, 90, L - 9, base, M['interior'], 3)
    t.ret(12, 94, L // 2 - 4, base - 4, M['vidro'], 2)
    t.relevo(t.mascara_ret(12, 94, L // 2 - 4, base - 4))
    vitrine(t, 14, 96, L // 2 - 6, base - 6)
    t.ret(L // 2 + 4, 94, L - 13, base, gf, 2)        # porta de enrolar aberta
    for y in range(94, 102, 2):
        t.hlinha(L // 2 + 4, L - 13, y, gf, 3)
    t.ret(L // 2 + 6, 102, L - 15, base, M['interior'], 2)
    return t


def vit_bones(t, x0, y0, x1, y1):
    """Vitrine com bonés (o amarelo em destaque) e camisetas."""
    for i, x in enumerate(range(x0 + 4, x1 - 6, 12)):
        cor = [M['amarelo'], M['azul'], M['vermelho'], M['folha']][i % 4]
        t.elipse(x + 4, y0 + 10, 5, 4, cor, 1)
        t.ret(x + 4, y0 + 10, x + 11, y0 + 11, cor, 2)
        t.vlinha(x + 4, y0 + 14, y0 + 18, M['grafite'], 3)
    for i, x in enumerate(range(x0 + 4, x1 - 8, 14)):
        cor = [M['rosa'], M['jeans'], M['laranja']][i % 3]
        t.poli([(x, y0 + 26), (x + 10, y0 + 26), (x + 12, y0 + 30), (x + 9, y0 + 30), (x + 9, y1 - 2), (x + 1, y1 - 2),
                (x + 1, y0 + 30), (x - 2, y0 + 30)], cor, 1)


def vit_sapatos(t, x0, y0, x1, y1):
    for fila in (y0 + 10, y0 + 24):
        t.hlinha(x0, x1, fila + 5, M['madeira'], 2)
        for x in range(x0 + 2, x1 - 6, 9):
            cor = t.rnd.choice((M['vermelho'], M['preto'], M['madeira'], M['branco']))
            t.ret(x, fila, x + 6, fila + 4, cor, 1)
            t.ret(x, fila, x + 2, fila + 2, cor, 0)


def vit_papelaria(t, x0, y0, x1, y1):
    for fila in range(y0 + 4, y1 - 4, 10):
        t.hlinha(x0, x1, fila + 8, M['madeira'], 2)
        for x in range(x0 + 2, x1 - 3, 4):
            cor = t.rnd.choice((M['azul'], M['rosa'], M['amarelo'], M['folha'], M['laranja']))
            t.ret(x, fila + t.rnd.randint(0, 2), x + 2, fila + 7, cor, 1)


def rua_nova():
    j = loja('CASA JOKA', 41, 'creme', 'vermelho', vit_bones, L=176, A=146, real=True)
    # toldo listrado amarelo e vermelho na frente (quica, como os toldos de feira)
    for x in range(4, 172, 8):
        cor = M['amarelo'] if (x // 8) % 2 == 0 else M['vermelho']
        j.poli([(x, 86), (x + 8, 86), (x + 9, 96), (x - 1, 96)], cor, 1)
    j.hlinha(3, 172, 96, M['vermelho'], 3)
    salvar(j, 'casa-joka')
    salvar(loja('SAPATARIA', 42, 'telha', 'azul', vit_sapatos), 'loja-sapatos')
    salvar(loja('PAPELARIA', 43, 'pedra_amarela', 'folha', vit_papelaria), 'loja-papelaria')


# =================================================================================== fase 4: Cesar Burg

def cesar_burg():
    """Lanchonete da praça: sobrado com letreiro 'CESAR BURG' e um hambúrguer em pixel, balcão, cardápio e a
    vitrine de pão de queijo. Letras e desenho próprios (nome autorizado pelo Pedro em 04/11/2026)."""
    L, A = 180, 150
    t = Tela(L, A, semente=55)
    pa, br, gf, vm = M['creme'], M['branco'], M['grafite'], M['vermelho']
    base = A - 1
    t.parede(4, 10, L - 5, base, pa, 2)
    t.cornija(0, L - 1, 6, br, alt=4)
    t.ret(2, 0, L - 3, 5, pa, 1)
    for x in (16, 74, 132):
        t.janela_grade(x, 18, x + 30, 50, colunas=2, linhas=3)
    t.reboco(6, 12, L - 7, 60, pa, n=14)
    # letreiro preto com letras amarelas e hambúrguer
    t.ret(6, 58, L - 7, 84, gf, 3)
    t.relevo(t.mascara_ret(6, 58, L - 7, 84))
    placa_texto(t, L // 2 + 12, 66, 'CESAR BURG', M['amarelo'], 1, sombra=(vm, 3), escala=2)
    hx, hy = 22, 71
    t.elipse(hx, hy - 3, 9, 5, M['pao'], 1)            # pão de cima
    t.px(hx - 4, hy - 5, M['pao'], 0); t.px(hx + 2, hy - 6, M['pao'], 0); t.px(hx - 1, hy - 4, M['pao'], 0)
    t.ret(hx - 9, hy + 1, hx + 9, hy + 1, M['folha'], 1)  # alface
    t.ret(hx - 9, hy + 2, hx + 9, hy + 4, M['madeira'], 3)  # carne
    t.ret(hx - 8, hy + 5, hx + 8, hy + 7, M['pao'], 2)  # pão de baixo
    # toldo vermelho com listras brancas
    for x in range(4, L - 4, 10):
        cor = vm if (x // 10) % 2 == 0 else br
        t.poli([(x, 86), (x + 10, 86), (x + 11, 98), (x - 1, 98)], cor, 1)
    t.hlinha(3, L - 4, 98, vm, 3)
    # loja: balcão com vitrine de pão de queijo, chapa, cardápio
    t.ret(8, 99, L - 9, base, M['interior'], 3)
    t.ret(8, 99, L - 9, 106, M['interior'], 4)
    t.ret(14, 120, 110, base - 6, br, 1)               # balcão
    t.hlinha(14, 110, 120, br, 0)
    t.ret(18, 110, 70, 120, M['vidro'], 1)             # vitrine de vidro
    for x in range(22, 66, 7):                         # pães de queijo dentro
        t.elipse(x, 117, 3, 2, M['pao'], 1)
        t.px(x - 1, 116, M['pao'], 0)
    t.ret(80, 112, 104, 119, gf, 2)                    # chapa
    t.ret(120, 104, 168, 136, gf, 3)                   # cardápio
    for y in range(108, 134, 4):
        t.hlinha(124, 164, y, M['amarelo'], 2 if y % 8 else 1)
    for x in (40, 96, 150):                            # luminárias
        t.vlinha(x, 99, 102, gf, 3)
        t.px(x, 103, M['amarelo'], 0)
    return salvar(t, 'cesar-burg')


# =================================================================================== objetos animados

def itacoin():
    """Itacoin: pedrinha amarela facetada que gira (a 'pedra amarela' do nome da cidade). 4 quadros 12x12."""
    qs = []
    for i, larg in enumerate((5, 4, 1.5, 4)):
        t = Tela(12, 12)
        t.elipse(6, 6, larg + 0.5, 5.5, M['amarelo'], 2)
        if larg > 2:
            t.elipse(6 - larg * 0.3, 4.5, larg * 0.5, 2.2, M['amarelo'], 0)
            t.px(6 + larg * 0.4, 8, M['amarelo'], 3)
            t.px(6 + larg * 0.2, 9, M['amarelo'], 3)
            t.px(6 - larg * 0.5, 3, M['branco'], 0)
        else:
            t.vlinha(6, 2, 9, M['amarelo'], 1)
        qs.append(t)
    folha(qs, 'itacoin')


def pao_de_queijo():
    """Pão de queijo (coletável e arremesso): 2 quadros 12x10 (girando no ar)."""
    qs = []
    for i in range(2):
        t = Tela(12, 10)
        t.elipse(6, 5.5, 5.3, 4.3, M['pao'], 2)
        t.elipse(5, 4, 3, 2, M['pao'], 1)
        for x, y in ((3, 3), (7, 2), (8, 5)) if i == 0 else ((4, 2), (8, 3), (3, 6)):
            t.px(x, y, M['pao'], 0)
        t.hlinha(3, 9, 8, M['pao'], 3)
        t.px(6, 6, M['pao'], 3); t.px(9, 6, M['pao'], 3)
        qs.append(t)
    folha(qs, 'paodequeijo')


def cafe_com_leite():
    """Copo americano de café com leite com vapor: 2 quadros 14x18."""
    qs = []
    for i in range(2):
        t = Tela(14, 18)
        t.poli([(2, 6), (11, 6), (10, 16), (3, 16)], M['vidro'], 1, sem_contorno=False)
        t.ret(3, 8, 10, 15, M['cafe'], 1)
        t.hlinha(3, 10, 8, M['cafe'], 0)
        for x in range(3, 11, 2):
            t.vlinha(x, 9, 15, M['cafe'], 2)
        t.hlinha(2, 11, 6, M['vidro'], 0)
        t.ret(3, 16, 10, 17, M['ceramica'], 2)
        for k, x in enumerate((5, 8)):
            off = (i + k) % 2
            t.px(x + off, 4, M['branco'], 1, sem_contorno=True)
            t.px(x, 3, M['branco'], 2, sem_contorno=True)
            t.px(x + 1 - off, 1, M['branco'], 2, sem_contorno=True)
        qs.append(t)
    folha(qs, 'cafecomleite')


def bone_item():
    t = Tela(18, 12)
    t.elipse(8, 7, 7, 5, M['amarelo'], 1)
    t.ret(1, 7, 15, 9, M['amarelo'], 2)
    t.ret(10, 8, 17, 9, M['amarelo'], 2)
    t.elipse(6, 5, 3, 2, M['amarelo'], 0)
    t.px(8, 2, M['amarelo'], 3)
    t.hlinha(1, 15, 10, M['amarelo'], 3)
    folha([t], 'boneitem')


def pombo():
    """Pombo da praça (fofo, cinza-azulado com pescoço furta-cor). 24x20, de lado olhando para a esquerda.
    Quadros: andar1, andar2, bicar, voar1, voar2, comendo, cochilando."""
    pe, gf = M['pena'], M['grafite']

    def corpo(t, dy=0, cabeca=(7, 7), asa='fechada', olho='aberto'):
        t.elipse(13, 12 + dy, 8, 5.5, pe, 2)                       # corpo
        t.poli([(19, 10 + dy), (23, 8 + dy), (23, 12 + dy), (20, 13 + dy)], pe, 3)   # cauda
        t.elipse(12, 10 + dy, 5, 3, pe, 1)
        cx, cy = cabeca
        t.elipse(cx + 2, cy + 3, 3, 3, M['verde_trem'], 2)          # pescoço furta-cor
        t.px(cx + 3, cy + 4, M['vinho'], 1); t.px(cx + 1, cy + 5, M['vinho'], 2)
        t.elipse(cx, cy, 3.4, 3, pe, 1)                            # cabeça
        t.ret(cx - 5, cy, cx - 3, cy + 1, M['laranja'], 3)          # bico
        if olho == 'aberto':
            t.px(cx - 1, cy - 1, M['laranja'], 1); t.px(cx - 1, cy, M['preto'], 4)
        else:
            t.hlinha(cx - 2, cx, cy, M['preto'], 3)
        if asa == 'fechada':
            t.elipse(15, 12 + dy, 5, 3, pe, 3)
            t.hlinha(13, 19, 13 + dy, pe, 4)
        elif asa == 'cima':
            t.poli([(10, 9 + dy), (18, 9 + dy), (22, 0), (14, 2)], pe, 1)
            t.hlinha(14, 21, 3, pe, 3)
        else:
            t.poli([(10, 12 + dy), (18, 12 + dy), (21, 19), (13, 18)], pe, 2)

    def pes(t, a, b):
        t.vlinha(11 + a, 17, 19, M['laranja'], 2)
        t.vlinha(15 + b, 17, 19, M['laranja'], 2)

    qs = []
    t = Tela(24, 20); corpo(t); pes(t, 0, 1); qs.append(t)
    t = Tela(24, 20); corpo(t, dy=-1); pes(t, 1, -1); qs.append(t)
    t = Tela(24, 20); corpo(t, cabeca=(5, 12)); pes(t, 0, 0); qs.append(t)
    t = Tela(24, 20); corpo(t, dy=-2, asa='cima'); qs.append(t)
    t = Tela(24, 20); corpo(t, dy=-2, asa='baixo'); qs.append(t)
    t = Tela(24, 20); corpo(t, cabeca=(6, 9)); pes(t, 0, 0)
    t.elipse(2, 12, 2.5, 2, M['pao'], 1); qs.append(t)            # comendo pão de queijo
    t = Tela(24, 20); corpo(t, dy=1, cabeca=(8, 9), olho='fechado'); pes(t, 0, 0); qs.append(t)
    folha(qs, 'pombo')


def heli_ceu():
    """Helicóptero civil genérico (azul e branco, sem marca) cruzando o céu. 2 quadros 72x30 (hélice)."""
    qs = []
    for i in range(2):
        t = Tela(72, 30, semente=5)
        az, br, vd, gf = M['azul'], M['branco'], M['vidro_azul'], M['grafite']
        t.elipse(24, 17, 16, 9, br, 1)                       # cabine/corpo
        t.ret(36, 13, 66, 17, br, 2)                         # cauda
        t.poli([(62, 8), (68, 8), (68, 17), (64, 17)], az, 2)  # deriva
        t.ret(10, 17, 40, 21, az, 2)                         # faixa
        t.elipse(14, 14, 7, 5, vd, 1)                        # vidro
        t.px(11, 12, vd, 0); t.px(12, 11, vd, 0)
        t.ret(22, 6, 30, 9, gf, 2)                           # mastro
        t.hlinha(14, 54, 27, gf, 2)                          # esqui
        t.vlinha(18, 24, 27, gf, 3); t.vlinha(34, 24, 27, gf, 3)
        if i == 0:
            t.hlinha(0, 54, 5, gf, 1)
            t.ret(64, 4, 66, 13, gf, 2)
        else:
            t.hlinha(14, 40, 5, gf, 1)
            t.ret(60, 9, 70, 10, gf, 2)
        qs.append(t)
    folha(qs, 'heliceu')


def placa_retorno():
    """Ponto de retorno: placa azul de ponto de ônibus (apagada / acesa com a estrela amarela). 2 quadros 18x44."""
    qs = []
    for aceso in (False, True):
        t = Tela(18, 44)
        t.ret(8, 14, 9, 43, M['ferro'], 1)
        t.ret(1, 1, 16, 16, M['azul'] if aceso else M['ferro'], 2)
        t.relevo(t.mascara_ret(1, 1, 16, 16))
        cor = M['amarelo'] if aceso else M['concreto']
        for x, y in ((8, 4), (7, 6), (8, 6), (9, 6), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7), (10, 7), (11, 7),
                     (6, 8), (7, 8), (8, 8), (9, 8), (10, 8), (7, 9), (8, 9), (9, 9), (6, 10), (10, 10), (5, 11),
                     (11, 11), (12, 7)):
            t.px(x, y, cor, 1)
        qs.append(t)
    folha(qs, 'placaretorno')


def placa_saida():
    """Fim da fase: placa de rua verde com seta. 26x40."""
    t = Tela(26, 40)
    t.ret(12, 16, 13, 39, M['ferro'], 1)
    t.ret(1, 2, 24, 16, M['folha'], 3)
    t.relevo(t.mascara_ret(1, 2, 24, 16))
    for i in range(7):
        t.hlinha(5, 15, 9, M['branco'], 0)
        t.vlinha(15 + i, 3 + i, 15 - i, M['branco'], 0) if i < 6 else None
    folha([t], 'placasaida')


def main():
    rodoviaria(); onibus(); locomotiva(); vagao(1); vagao(2)
    rua_nova(); cesar_burg()
    itacoin(); pao_de_queijo(); cafe_com_leite(); bone_item(); pombo(); heli_ceu(); placa_retorno(); placa_saida()
    for f in sorted(os.listdir(CEN)) + sorted(os.listdir(SPR)):
        print(f)


if __name__ == '__main__':
    main()
