"""Proposta do mapa-múndi do Itamania (Itajubá em pixel art, linguagem de mapa de mundo de plataforma de 16 bits).

Gera ferramentas/arte/previas/mapa-mundi-proposta.png (360x640 nativo, em pé, ampliado 3x).
Posições seguem o 2º esboço do Pedro (references/mapa/esboco-pedro-2.jpg), com o norte para cima: a cidade
num vale cercado de montanhas, com a Av. BPS (e o rio no meio dela) como eixo central até o lago.
Tudo é desenhado aqui, com formas próprias: nenhum tile ou sprite de outro jogo.

Uso: python3 ferramentas/mapa-mundi/gerar_mapa.py
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw

W, H = 360, 640
ESCALA = 3
random.seed(7)
np.random.seed(7)

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, '..', 'arte', 'previas', 'mapa-mundi-proposta.png')

# ---------------------------------------------------------------- paleta
C = {
    'g0': (36, 124, 52), 'g1': (60, 164, 60), 'g2': (100, 200, 68), 'g3': (156, 224, 84), 'g4': (212, 244, 132),
    'gl': (16, 72, 32),
    'm0': (44, 60, 72), 'm1': (70, 102, 104), 'm2': (100, 140, 120), 'm3': (140, 178, 136), 'm4': (190, 214, 168),
    'a0': (24, 40, 96), 'a1': (40, 88, 176), 'a2': (72, 136, 224), 'a3': (136, 192, 248), 'a4': (232, 248, 255),
    'areia': (224, 196, 140),
    'c0': (96, 56, 28), 'c1': (176, 120, 64), 'c2': (224, 176, 104), 'c3': (248, 216, 152),
    'ru': (208, 88, 56), 'ru2': (160, 56, 40), 'ru3': (240, 136, 88),
    'pa': (244, 236, 216), 'pa2': (204, 192, 168),
    'ci0': (80, 84, 100), 'ci1': (132, 140, 156), 'ci2': (180, 188, 200), 'ci3': (228, 232, 240),
    'am': (248, 208, 56), 'am2': (196, 140, 24), 'am3': (255, 244, 168),
    'vm': (216, 56, 40), 'vm2': (144, 32, 24), 'vm3': (255, 144, 120),
    'roxo': (96, 72, 160), 'preto': (32, 28, 40), 'br': (255, 255, 255),
    'mad0': (72, 40, 24), 'mad1': (128, 80, 40), 'mad2': (176, 120, 64), 'mad3': (216, 168, 104),
}


def rgba(c, a=255):
    return (c[0], c[1], c[2], a)


def camada(w=W, h=H):
    return Image.new('RGBA', (w, h), (0, 0, 0, 0))


def contorno(img, cor):
    """Contorno de 1 px (4 vizinhos) em volta de tudo que é opaco."""
    a = np.array(img)
    m = a[:, :, 3] > 0
    d = np.zeros_like(m)
    d[1:, :] |= m[:-1, :]
    d[:-1, :] |= m[1:, :]
    d[:, 1:] |= m[:, :-1]
    d[:, :-1] |= m[:, 1:]
    novo = d & ~m
    a[novo] = rgba(cor)
    return Image.fromarray(a)


def colar(base, spr, x, y, cor_contorno=None):
    """Cola o sprite com a base (centro inferior) em x, y."""
    if cor_contorno:
        g = camada(spr.width + 2, spr.height + 2)
        g.paste(spr, (1, 1))
        spr = contorno(g, cor_contorno)
        x0, y0 = x - spr.width // 2, y - spr.height + 1
    else:
        x0, y0 = x - spr.width // 2, y - spr.height
    base.alpha_composite(spr, (int(x0), int(y0)))


def px(d, x, y, c):
    d.point((x, y), fill=rgba(c))


def ret(d, x0, y0, x1, y1, c):
    d.rectangle([x0, y0, x1, y1], fill=rgba(c))


# ---------------------------------------------------------------- fonte 5x7 própria
F = {
    'A': '.###.|#...#|#...#|#####|#...#|#...#|#...#', 'B': '####.|#...#|#...#|####.|#...#|#...#|####.',
    'C': '.###.|#...#|#....|#....|#....|#...#|.###.', 'D': '####.|#...#|#...#|#...#|#...#|#...#|####.',
    'E': '#####|#....|#....|####.|#....|#....|#####', 'F': '#####|#....|#....|####.|#....|#....|#....',
    'G': '.###.|#...#|#....|#.###|#...#|#...#|.###.', 'H': '#...#|#...#|#...#|#####|#...#|#...#|#...#',
    'I': '.###.|..#..|..#..|..#..|..#..|..#..|.###.', 'J': '..###|...#.|...#.|...#.|#..#.|#..#.|.##..',
    'K': '#...#|#..#.|#.#..|##...|#.#..|#..#.|#...#', 'L': '#....|#....|#....|#....|#....|#....|#####',
    'M': '#...#|##.##|#.#.#|#.#.#|#...#|#...#|#...#', 'N': '#...#|##..#|#.#.#|#..##|#...#|#...#|#...#',
    'O': '.###.|#...#|#...#|#...#|#...#|#...#|.###.', 'P': '####.|#...#|#...#|####.|#....|#....|#....',
    'R': '####.|#...#|#...#|####.|#.#..|#..#.|#...#', 'S': '.####|#....|#....|.###.|....#|....#|####.',
    'T': '#####|..#..|..#..|..#..|..#..|..#..|..#..', 'U': '#...#|#...#|#...#|#...#|#...#|#...#|.###.',
    'V': '#...#|#...#|#...#|#...#|#...#|.#.#.|..#..', 'W': '#...#|#...#|#...#|#.#.#|#.#.#|##.##|#...#',
    'X': '#...#|#...#|.#.#.|..#..|.#.#.|#...#|#...#', 'Y': '#...#|#...#|.#.#.|..#..|..#..|..#..|..#..',
    'Z': '#####|....#|...#.|..#..|.#...|#....|#####', ' ': '.....|.....|.....|.....|.....|.....|.....',
    '0': '.###.|#..##|#.#.#|#.#.#|##..#|#...#|.###.', '1': '..#..|.##..|..#..|..#..|..#..|..#..|.###.',
    '2': '.###.|#...#|....#|...#.|..#..|.#...|#####', '3': '####.|....#|....#|.###.|....#|....#|####.',
    '4': '...#.|..##.|.#.#.|#..#.|#####|...#.|...#.', '5': '#####|#....|####.|....#|....#|#...#|.###.',
    '6': '.###.|#....|#....|####.|#...#|#...#|.###.', '7': '#####|....#|...#.|..#..|..#..|..#..|..#..',
    '8': '.###.|#...#|#...#|.###.|#...#|#...#|.###.', '9': '.###.|#...#|#...#|.####|....#|....#|.###.',
    '-': '.....|.....|.....|.###.|.....|.....|.....', '.': '.....|.....|.....|.....|.....|.##..|.##..',
    '?': '.###.|#...#|....#|...#.|..#..|.....|..#..',
}
ACENTO = {'Á': ('A', 'agudo'), 'É': ('E', 'agudo'), 'Í': ('I', 'agudo'), 'Ó': ('O', 'agudo'), 'Ú': ('U', 'agudo'),
          'Ã': ('A', 'til'), 'Õ': ('O', 'til'), 'Â': ('A', 'circ'), 'Ê': ('E', 'circ'), 'Ô': ('O', 'circ'),
          'Ç': ('C', 'cedilha')}
MARCA = {'agudo': ['...#.', '..#..'], 'til': ['.##.#', '#.##.'], 'circ': ['..#..', '.#.#.']}


def texto_img(txt, cor, sombra, esc=1):
    """Texto em pixel com sombra de 1 px. Altura fixa 11 (2 de acento, 7 de letra, 2 de cedilha)."""
    w = len(txt) * 6 * esc + esc
    im = camada(w + esc, 11 * esc + esc)
    d = ImageDraw.Draw(im)

    def bloco(linhas, x0, y0, c):
        for j, lin in enumerate(linhas):
            for i, ch in enumerate(lin):
                if ch == '#':
                    d.rectangle([x0 + i * esc, y0 + j * esc, x0 + (i + 1) * esc - 1, y0 + (j + 1) * esc - 1],
                                fill=rgba(c))

    for passo, (dx, c) in enumerate([(esc, sombra), (0, cor)]):
        for k, ch in enumerate(txt):
            x0 = k * 6 * esc + dx
            y0 = dx
            base, marca = ACENTO.get(ch, (ch, None))
            bloco(F[base].split('|'), x0, y0 + 2 * esc, c)
            if marca == 'cedilha':
                bloco(['..#..', '.##..'], x0, y0 + 9 * esc, c)
            elif marca:
                bloco(MARCA[marca], x0, y0, c)
    return im


def placa(base, txt, x, y, esc=1, cor=None):
    """Plaquinha de madeira com o nome do lugar, centrada em x, topo em y."""
    t = texto_img(txt, cor or C['c3'], C['mad0'], esc)
    w, h = t.width + 6, 11 * esc + 4
    p = camada(w + 2, h + 2)
    d = ImageDraw.Draw(p)
    d.rectangle([0, 0, w + 1, h + 1], fill=rgba(C['mad0']))
    d.rectangle([1, 1, w, h], fill=rgba(C['mad1']))
    d.line([2, 1, w - 1, 1], fill=rgba(C['mad2']))
    d.line([1, h, w, h], fill=rgba(C['mad0']))
    p.alpha_composite(t, (4, 2))
    base.alpha_composite(p, (int(x - p.width / 2), int(y)))
    return p.width, p.height


# ---------------------------------------------------------------- terreno
def ruido(escala, oitavas=3):
    tot = np.zeros((H, W))
    amp, soma = 1.0, 0
    for o in range(oitavas):
        s = max(2, int(escala / (2 ** o)))
        gh, gw = H // s + 2, W // s + 2
        g = np.random.rand(gh, gw)
        ys = np.arange(H) / s
        xs = np.arange(W) / s
        y0 = ys.astype(int)
        x0 = xs.astype(int)
        fy = (ys - y0)[:, None]
        fx = (xs - x0)[None, :]
        fy = fy * fy * (3 - 2 * fy)
        fx = fx * fx * (3 - 2 * fx)
        a = g[y0][:, x0]
        b = g[y0][:, x0 + 1]
        c = g[y0 + 1][:, x0]
        d = g[y0 + 1][:, x0 + 1]
        v = a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy
        tot += v * amp
        soma += amp
        amp *= 0.5
    return tot / soma


def terreno():
    n = ruido(40)
    img = np.zeros((H, W, 4), np.uint8)
    img[:, :, 3] = 255
    cores = [C['g1'], C['g2'], C['g3']]
    lim = [0.44, 0.6]
    yy, xx = np.mgrid[0:H, 0:W]
    xadrez = (xx + yy) % 2 == 0
    idx = np.where(n < lim[0], 0, np.where(n < lim[1], 1, 2))
    # faixa pontilhada nas bordas entre tons (pontilhado de 16 bits)
    perto0 = np.abs(n - lim[0]) < 0.012
    perto1 = np.abs(n - lim[1]) < 0.012
    idx = np.where(perto0 & xadrez, 1, np.where(perto0, 0, idx))
    idx = np.where(perto1 & xadrez, 2, np.where(perto1, 1, idx))
    for i, c in enumerate(cores):
        img[idx == i, :3] = c
    # tufos de grama
    im = Image.fromarray(img)
    d = ImageDraw.Draw(im)
    for _ in range(900):
        x, y = random.randrange(W), random.randrange(H)
        c = C['g1'] if idx[y, x] > 0 else C['g0']
        d.point((x, y), fill=rgba(c))
        d.point((x + 2, y), fill=rgba(c))
        d.point((x + 1, y + 1), fill=rgba(c))
    for _ in range(250):
        x, y = random.randrange(W), random.randrange(H)
        d.point((x, y), fill=rgba(C['g4']))
    return im


def catmull(pts, passos=12):
    out = []
    p = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for k in range(passos):
            t = k / passos
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                       (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                       (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(pts[-1])
    return out


def linha_grossa(d, pts, larg, cor):
    d.line(pts, fill=rgba(cor), width=larg, joint='curve')
    r = larg / 2
    for x, y in (pts[0], pts[-1]):
        d.ellipse([x - r + 0.5, y - r + 0.5, x + r - 0.5, y + r - 0.5], fill=rgba(cor))


# ---------------------------------------------------------------- montanhas e morros
def montanha(base, cx, by, w, h, tons=('m0', 'm1', 'm2', 'm3', 'm4')):
    l = camada()
    d = ImageDraw.Draw(l)
    o, t1, t2, t3, t4 = (C[k] for k in tons)
    topo = (cx + random.randint(-3, 3), by - h)
    esq, dir_ = (cx - w // 2, by), (cx + w // 2, by)
    # crista irregular
    pe = [esq]
    for k in range(1, 4):
        f = k / 4
        pe.append((esq[0] + (topo[0] - esq[0]) * f + random.randint(-2, 1), by - h * f + random.randint(-2, 2)))
    pe.append(topo)
    for k in range(1, 4):
        f = k / 4
        pe.append((topo[0] + (dir_[0] - topo[0]) * f + random.randint(-1, 2), by - h + h * f + random.randint(-2, 2)))
    pe.append(dir_)
    d.polygon(pe, fill=rgba(t2))
    # face da sombra (direita)
    d.polygon([topo] + pe[5:] + [(cx + w // 8, by)], fill=rgba(t1))
    # face da luz (esquerda, perto do topo)
    d.polygon([topo, pe[3], pe[2], (topo[0] - w // 10, by - h // 3)], fill=rgba(t3))
    d.polygon([topo, pe[3], (topo[0] - 2, by - h * 2 // 3)], fill=rgba(t4))
    # sulcos
    for k in range(3):
        x = topo[0] + 3 + k * (w // 8)
        d.line([(x, by - h + 6 + k * 5), (x + 2, by - h + 14 + k * 6)], fill=rgba(o))
    a = np.array(l)
    a[:, :, 3] = np.where(a[:, :, 3] > 0, 255, 0)
    l = contorno(Image.fromarray(a), o)
    base.alpha_composite(l)


def morro(base, cx, by, w, h):
    """Morro verde arredondado, luz de cima e da esquerda."""
    l = camada()
    d = ImageDraw.Draw(l)
    d.ellipse([cx - w / 2, by - h, cx + w / 2, by + h], fill=rgba(C['g1']))
    d.ellipse([cx - w / 2 + 2, by - h + 1, cx + w / 2 - w * 0.25, by + h * 0.4], fill=rgba(C['g2']))
    d.ellipse([cx - w / 2 + w * 0.15, by - h + 2, cx - w * 0.05, by - h * 0.45], fill=rgba(C['g3']))
    d.ellipse([cx - w * 0.28, by - h + 3, cx - w * 0.16, by - h * 0.78], fill=rgba(C['g4']))
    a = np.array(l)
    a[by + 1:, :, 3] = 0
    l = contorno(Image.fromarray(a), C['gl'])
    a = np.array(l)
    a[by + 1:, :, 3] = 0
    base.alpha_composite(Image.fromarray(a))


# ---------------------------------------------------------------- árvores, casas
def arvore(base, x, y, tipo=0):
    s = camada(9, 11)
    d = ImageDraw.Draw(s)
    ret(d, 4, 7, 4, 10, C['mad1'])
    if tipo == 0:
        d.ellipse([0, 0, 8, 8], fill=rgba(C['g0']))
        d.ellipse([1, 0, 6, 6], fill=rgba(C['g1']))
        d.ellipse([2, 1, 5, 4], fill=rgba(C['g2']))
        px(d, 3, 2, C['g3'])
    else:  # ipê amarelo (árvore típica das ruas)
        d.ellipse([0, 0, 8, 8], fill=rgba(C['am2']))
        d.ellipse([1, 0, 6, 6], fill=rgba(C['am']))
        d.ellipse([2, 1, 5, 4], fill=rgba(C['am3']))
    colar(base, s, x, y, C['gl'] if tipo == 0 else C['c0'])


def casa(base, x, y, var):
    w = 7 + var % 2 * 2
    s = camada(w, 7)
    d = ImageDraw.Draw(s)
    teto = [C['ru'], C['ru3'], (196, 120, 72)][var % 3]
    ret(d, 0, 3, w - 1, 6, C['pa'] if var % 4 else (236, 212, 160))
    ret(d, 0, 6, w - 1, 6, C['pa2'])
    ret(d, 0, 0, w - 1, 2, teto)
    ret(d, 0, 2, w - 1, 2, C['ru2'])
    ret(d, 1, 0, w - 2, 0, C['ru3'] if teto != C['ru3'] else (255, 180, 130))
    px(d, w // 2, 5, C['mad0'])
    px(d, w // 2, 4, C['mad0'])
    if w > 7:
        px(d, 1, 4, C['a1'])
    colar(base, s, x, y, C['c0'])


# ---------------------------------------------------------------- marcos (lugares)
class _Desloc:
    """ImageDraw que soma um deslocamento em y (para desenhar acima do topo do sprite)."""
    def __init__(self, d, dy):
        self.d, self.dy = d, dy

    def _xy(self, xy):
        if len(xy) and isinstance(xy[0], (tuple, list)):
            return [(x, y + self.dy) for x, y in xy]
        return [v + (self.dy if k % 2 else 0) for k, v in enumerate(xy)]

    def rectangle(self, xy, **k):
        self.d.rectangle(self._xy(xy), **k)

    def ellipse(self, xy, **k):
        self.d.ellipse(self._xy(xy), **k)

    def polygon(self, xy, **k):
        self.d.polygon(self._xy(xy), **k)

    def line(self, xy, **k):
        self.d.line(self._xy(xy), **k)

    def point(self, xy, **k):
        self.d.point((xy[0], xy[1] + self.dy), **k)


def spr(w, h, dy=0):
    s = camada(w, h + dy)
    d = ImageDraw.Draw(s)
    return s, (_Desloc(d, dy) if dy else d)


def m_trem():
    s, d = spr(40, 20)
    # estação: casinha comprida, telhado de beiral
    ret(d, 0, 6, 17, 19, C['pa'])
    ret(d, 0, 4, 17, 6, C['ru'])
    ret(d, 0, 3, 17, 3, C['ru3'])
    ret(d, 0, 7, 17, 7, C['ru2'])
    for x in (2, 7, 12):
        ret(d, x, 10, x + 2, 15, C['a1'])
        px(d, x, 10, C['a3'])
    ret(d, 0, 18, 17, 19, C['pa2'])
    # locomotiva
    ret(d, 22, 9, 35, 16, C['vm'])
    ret(d, 22, 9, 35, 9, C['vm3'])
    ret(d, 31, 5, 37, 16, C['vm2'])
    ret(d, 32, 7, 35, 10, C['a3'])
    ret(d, 24, 5, 26, 8, C['preto'])
    ret(d, 23, 4, 27, 4, C['preto'])
    ret(d, 20, 15, 39, 16, C['preto'])
    for x in (24, 30, 36):
        d.ellipse([x - 2, 15, x + 2, 19], fill=rgba(C['preto']))
        px(d, x, 17, C['ci2'])
    # fumaça
    for i, (x, y) in enumerate([(25, 2), (22, 0), (19, 1)]):
        d.ellipse([x - 1, y - 1 + i % 2, x + 1, y + 1], fill=rgba(C['ci3']))
    return s


def m_soldado():
    s, d = spr(36, 24)
    # pedestal branco com o soldado apontando
    ret(d, 2, 12, 9, 23, C['pa'])
    ret(d, 7, 12, 9, 23, C['pa2'])
    ret(d, 1, 21, 10, 23, C['pa2'])
    ret(d, 4, 4, 7, 11, (120, 104, 72))
    ret(d, 4, 2, 7, 4, (92, 80, 56))
    ret(d, 8, 6, 11, 6, (120, 104, 72))
    px(d, 5, 5, (168, 150, 100))
    # helicóptero
    ret(d, 15, 12, 29, 19, C['ci1'])
    ret(d, 15, 12, 29, 13, C['ci2'])
    ret(d, 26, 13, 29, 16, C['a3'])
    ret(d, 11, 13, 15, 14, C['ci1'])
    ret(d, 10, 11, 11, 15, C['ci0'])
    ret(d, 17, 15, 21, 17, C['g1'])  # bandeira do Brasil na lateral
    px(d, 19, 16, C['am'])
    px(d, 19, 16, C['a1'])
    ret(d, 21, 9, 22, 11, C['ci0'])
    ret(d, 12, 8, 35, 8, C['ci0'])
    ret(d, 16, 21, 30, 21, C['ci0'])
    ret(d, 18, 20, 18, 20, C['ci0'])
    ret(d, 27, 20, 27, 20, C['ci0'])
    ret(d, 14, 22, 32, 23, C['pa2'])
    return s


def m_ruanova():
    s, d = spr(34, 18)
    # comércio com toldos coloridos
    cores = [(C['vm'], C['br']), (C['a1'], C['br']), (C['g1'], C['am3'])]
    for i in range(3):
        x0 = i * 11
        ret(d, x0, 3, x0 + 10, 17, C['pa'] if i != 1 else (240, 220, 176))
        ret(d, x0, 2, x0 + 10, 3, C['ru2'])
        ret(d, x0 + 3, 12, x0 + 7, 17, C['mad1'])
        a, b = cores[i]
        for k in range(11):
            c = a if (k // 2) % 2 == 0 else b
            ret(d, x0 + k, 8, x0 + k, 10, c)
        ret(d, x0, 11, x0 + 10, 11, cores[i][0])
        ret(d, x0 + 2, 5, x0 + 8, 6, C['a1'])
    return s


def m_alameda():
    s, d = spr(30, 14)
    for i, x in enumerate(range(3, 30, 6)):
        ret(d, x, 9, x, 13, C['mad1'])
        d.ellipse([x - 3, 1 + i % 2, x + 3, 9], fill=rgba(C['g0'] if i % 2 else C['am2']))
        d.ellipse([x - 2, 1 + i % 2, x + 1, 6], fill=rgba(C['g2'] if i % 2 else C['am']))
        px(d, x - 1, 3, C['g4'] if i % 2 else C['am3'])
    return s


def m_hotel():
    s, d = spr(22, 30)
    # Hotel Coroados: prédio alto claro no morro
    ret(d, 2, 4, 19, 29, C['pa'])
    ret(d, 15, 4, 19, 29, C['pa2'])
    ret(d, 1, 2, 20, 4, C['ci1'])
    ret(d, 1, 2, 20, 2, C['ci2'])
    for y in range(7, 26, 4):
        for x in range(4, 18, 4):
            ret(d, x, y, x + 1, y + 1, C['a1'] if (x + y) % 3 else C['am'])
    ret(d, 8, 25, 12, 29, C['mad0'])
    ret(d, 9, 0, 11, 1, C['vm'])
    return s


def m_unifei():
    s, d = spr(44, 24)
    # blocos do campus e uma roda-d'água (energia)
    ret(d, 0, 8, 27, 23, (232, 228, 216))
    ret(d, 0, 6, 27, 8, C['ci1'])
    ret(d, 22, 8, 27, 23, C['pa2'])
    for y in (11, 16):
        ret(d, 2, y, 20, y + 2, C['a1'])
        for x in range(2, 21, 3):
            px(d, x, y, C['a3'])
    ret(d, 10, 19, 14, 23, C['mad0'])
    ret(d, 6, 0, 7, 6, C['ci0'])
    ret(d, 5, 0, 8, 0, C['vm'])
    # roda
    cx, cy = 36, 15
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], outline=rgba(C['mad1']))
    for k in range(8):
        a = k * math.pi / 4
        d.line([(cx, cy), (cx + 6 * math.cos(a), cy + 6 * math.sin(a))], fill=rgba(C['mad2']))
    d.ellipse([cx - 1, cy - 1, cx + 1, cy + 1], fill=rgba(C['ci0']))
    ret(d, 29, 21, 43, 23, C['a2'])
    px(d, 31, 21, C['a4'])
    px(d, 40, 22, C['a4'])
    return s


def m_praca_coreto():
    s, d = spr(26, 20)
    # "Praçona": praça grande com coreto (a confirmar)
    d.ellipse([0, 12, 25, 19], fill=rgba((200, 196, 184)))
    d.ellipse([2, 13, 23, 18], fill=rgba((224, 220, 208)))
    ret(d, 6, 6, 19, 14, C['pa'])
    for x in (7, 12, 18):
        ret(d, x, 7, x, 14, C['pa2'])
    d.polygon([(4, 7), (13, 0), (21, 7)], fill=rgba(C['vm']))
    d.polygon([(13, 0), (21, 7), (13, 7)], fill=rgba(C['vm2']))
    ret(d, 5, 14, 20, 15, C['pa2'])
    return s


def m_praca_matriz():
    s, d = spr(40, 34, 4)
    # Igreja Matriz: torre central com relógio, duas torres menores, rosácea, 3 portas
    cr, cr2, br = (240, 224, 184), (208, 184, 140), C['pa']
    ret(d, 6, 14, 29, 33, cr)
    ret(d, 24, 14, 29, 33, cr2)
    ret(d, 13, 2, 22, 14, cr)
    ret(d, 20, 2, 22, 14, cr2)
    d.polygon([(12, 3), (17, -3), (23, 3)], fill=rgba(C['ci1']))
    ret(d, 17, -1, 17, 1, C['am'])
    d.ellipse([15, 5, 20, 10], fill=rgba(C['br']))
    px(d, 17, 6, C['preto'])
    px(d, 17, 7, C['preto'])
    px(d, 18, 7, C['preto'])
    for x0 in (4, 26):
        ret(d, x0, 9, x0 + 5, 18, cr if x0 == 4 else cr2)
        d.polygon([(x0 - 1, 10), (x0 + 2, 5), (x0 + 6, 10)], fill=rgba(C['ci1']))
    d.ellipse([15, 17, 20, 22], fill=rgba(C['a2']))
    px(d, 17, 19, C['am'])
    for x0 in (8, 16, 24):
        ret(d, x0, 26, x0 + 3, 33, C['mad0'])
        px(d, x0, 26, cr)
        px(d, x0 + 3, 26, cr)
    ret(d, 6, 14, 29, 14, br)
    ret(d, 6, 24, 29, 24, br)
    # fonte com o busto, ao lado
    d.ellipse([30, 27, 39, 33], fill=rgba(C['pa2']))
    d.ellipse([31, 28, 38, 32], fill=rgba(C['a2']))
    ret(d, 34, 23, 35, 29, (100, 112, 96))
    px(d, 32, 26, C['a4'])
    px(d, 37, 26, C['a4'])
    return s


def m_cemiterio():
    s, d = spr(30, 20)
    # muro baixo, portão e lápides; ciprestes. Tom calmo, nada assustador.
    ret(d, 0, 12, 29, 19, (176, 168, 156))
    ret(d, 0, 12, 29, 12, (212, 204, 192))
    ret(d, 12, 8, 17, 19, C['ci0'])
    for x in range(13, 17):
        ret(d, x, 9, x, 19, C['ci2'] if x % 2 else C['ci0'])
    for x in (3, 7, 21, 25):
        ret(d, x, 7, x + 2, 11, C['ci2'])
        px(d, x + 1, 6, C['ci2'])
    for x in (1, 28):
        d.ellipse([x - 2, 0, x + 2, 12], fill=rgba(C['g0']))
        ret(d, x - 1, 2, x - 1, 9, C['g1'])
    return s


def m_lago():
    s, d = spr(56, 34)
    # lago do Parque Municipal com pedalinho
    d.ellipse([0, 4, 55, 33], fill=rgba(C['areia']))
    d.ellipse([2, 5, 53, 31], fill=rgba(C['a1']))
    d.ellipse([4, 7, 50, 28], fill=rgba(C['a2']))
    d.ellipse([10, 10, 30, 20], fill=rgba(C['a3']))
    for x, y in [(14, 22), (38, 12), (30, 25), (44, 20)]:
        ret(d, x, y, x + 2, y, C['a4'])
    # pedalinho de cisne, desenho próprio
    ret(d, 33, 16, 40, 19, C['br'])
    ret(d, 33, 19, 40, 19, C['ci2'])
    ret(d, 39, 12, 40, 16, C['br'])
    px(d, 41, 12, C['am'])
    ret(d, 34, 15, 36, 16, C['vm'])
    return s


def m_kart():
    s, d = spr(48, 24)
    # pista de kart: oval de asfalto com zebra e bandeira quadriculada
    d.ellipse([0, 2, 47, 23], fill=rgba(C['ci0']))
    d.ellipse([1, 3, 46, 22], fill=rgba((88, 92, 104)))
    d.ellipse([9, 8, 38, 17], fill=rgba(C['g2']))
    d.ellipse([11, 9, 30, 14], fill=rgba(C['g3']))
    for k in range(0, 46, 4):
        px(d, k + 1, 12, C['vm'])
        px(d, k + 2, 12, C['br'])
    ret(d, 22, 2, 22, 7, C['br'])
    for i in range(4):
        for j in range(3):
            ret(d, 23 + i, 2 + j, 23 + i, 2 + j, C['preto'] if (i + j) % 2 else C['br'])
    ret(d, 5, 13, 8, 15, C['vm'])
    px(d, 6, 12, C['am'])
    ret(d, 40, 9, 43, 11, C['a2'])
    px(d, 41, 8, C['am'])
    return s


def m_agonia():
    s, d = spr(26, 30, 6)
    # Santuário no alto do morro: capela branca de torre única e cruz
    ret(d, 4, 14, 21, 29, C['pa'])
    ret(d, 17, 14, 21, 29, C['pa2'])
    d.polygon([(2, 15), (12, 8), (23, 15)], fill=rgba(C['ru']))
    d.polygon([(12, 8), (23, 15), (12, 15)], fill=rgba(C['ru2']))
    ret(d, 9, 3, 15, 14, C['pa'])
    ret(d, 13, 3, 15, 14, C['pa2'])
    d.polygon([(8, 4), (12, -1), (16, 4)], fill=rgba(C['a1']))
    ret(d, 12, -5, 12, -1, C['am'])
    ret(d, 11, -4, 13, -4, C['am'])
    ret(d, 11, 6, 13, 9, C['mad0'])
    d.ellipse([10, 16, 14, 20], fill=rgba(C['a2']))
    ret(d, 10, 22, 14, 29, C['a1'])
    px(d, 11, 22, C['a3'])
    return s


def m_piranguinho():
    s, d = spr(30, 22)
    # placa de saída da cidade + pé de moleque gigante (doce típico de Piranguinho)
    ret(d, 2, 4, 3, 21, C['mad0'])
    d.polygon([(0, 2), (17, 2), (21, 6), (17, 10), (0, 10)], fill=rgba(C['g1']))
    ret(d, 2, 5, 14, 5, C['br'])
    ret(d, 2, 7, 11, 7, C['br'])
    ret(d, 12, 13, 29, 20, C['c1'])
    ret(d, 12, 13, 29, 14, C['c2'])
    ret(d, 12, 20, 29, 21, C['c0'])
    for x, y in [(14, 16), (18, 18), (21, 15), (25, 17), (27, 15), (16, 19), (23, 19)]:
        ret(d, x, y, x + 1, y, C['c3'])
    return s


def m_inicio():
    s, d = spr(14, 14)
    # casinha do herói com bandeira
    ret(d, 1, 6, 12, 13, C['pa'])
    d.polygon([(0, 7), (6, 1), (13, 7)], fill=rgba(C['vm']))
    ret(d, 5, 9, 7, 13, C['mad1'])
    ret(d, 9, 9, 10, 10, C['a1'])
    return s




# ---------------------------------------------------------------- marcos novos (versão em pé)
def m_hotel_grande():
    """Hotel Coroados: prédio enorme no alto do morro."""
    s, d = spr(30, 50)
    ret(d, 2, 6, 27, 49, C['pa'])
    ret(d, 21, 6, 27, 49, C['pa2'])
    ret(d, 0, 3, 29, 6, C['ci1'])
    ret(d, 0, 3, 29, 3, C['ci2'])
    for y in range(9, 44, 4):
        for x in range(4, 26, 4):
            c = C['am'] if (x * 7 + y * 3) % 5 == 0 else (C['a1'] if x < 21 else C['a0'])
            ret(d, x, y, x + 1, y + 1, c)
            px(d, x, y, C['a3'] if c == C['a1'] else c)
    ret(d, 10, 44, 18, 49, C['mad0'])
    ret(d, 8, 43, 20, 43, C['vm'])
    ret(d, 12, 0, 16, 2, C['vm'])
    ret(d, 13, 0, 15, 0, C['vm3'])
    return s


def m_unifei_campus():
    """Campus grande: três blocos, gramado e a roda-d'água (energia)."""
    s, d = spr(96, 46)
    d.rounded_rectangle([0, 6, 95, 45], radius=6, fill=rgba(C['g3']))
    d.rounded_rectangle([2, 8, 93, 43], radius=5, fill=rgba(C['g2']))
    for x in range(6, 92, 9):
        px(d, x, 40, C['g1'])

    def bloco(x0, y0, w, h):
        ret(d, x0, y0, x0 + w, y0 + h, (232, 228, 216))
        ret(d, x0 + w - 4, y0, x0 + w, y0 + h, C['pa2'])
        ret(d, x0 - 1, y0 - 2, x0 + w + 1, y0, C['ci1'])
        ret(d, x0 - 1, y0 - 2, x0 + w + 1, y0 - 2, C['ci2'])
        for y in range(y0 + 3, y0 + h - 3, 4):
            ret(d, x0 + 2, y, x0 + w - 6, y + 1, C['a1'])
            for x in range(x0 + 2, x0 + w - 5, 3):
                px(d, x, y, C['a3'])
        ret(d, x0 + w // 2 - 2, y0 + h - 4, x0 + w // 2 + 1, y0 + h, C['mad0'])

    bloco(6, 12, 30, 24)
    bloco(42, 6, 24, 20)
    bloco(44, 30, 22, 12)
    ret(d, 50, 0, 51, 5, C['ci0'])
    ret(d, 49, 0, 52, 0, C['vm'])
    cx, cy = 82, 26
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], outline=rgba(C['mad1']))
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=rgba(C['mad2']))
    for k in range(8):
        a = k * math.pi / 4 + 0.2
        d.line([(cx, cy), (cx + 8 * math.cos(a), cy + 8 * math.sin(a))], fill=rgba(C['mad2']))
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=rgba(C['ci0']))
    ret(d, 72, 35, 92, 39, C['a1'])
    ret(d, 73, 36, 91, 37, C['a2'])
    px(d, 76, 36, C['a4'])
    px(d, 86, 37, C['a4'])
    return s


def m_prefeitura():
    """Prefeitura: prédio cívico com colunas e as bandeiras."""
    s, d = spr(40, 34)
    ret(d, 2, 14, 37, 33, (236, 228, 208))
    ret(d, 30, 14, 37, 33, (204, 192, 168))
    d.polygon([(0, 15), (20, 6), (39, 15)], fill=rgba(C['ci1']))
    d.polygon([(20, 6), (39, 15), (20, 15)], fill=rgba(C['ci0']))
    d.polygon([(6, 14), (20, 8), (33, 14)], fill=rgba(C['ci2']))
    ret(d, 1, 15, 38, 16, C['pa'])
    for x in (5, 11, 17, 23, 29):
        ret(d, x, 17, x + 2, 30, C['br'])
        px(d, x + 2, 17, C['pa2'])
        ret(d, x + 2, 18, x + 2, 30, C['pa2'])
    ret(d, 15, 24, 24, 30, C['mad0'])
    ret(d, 0, 31, 39, 33, C['pa2'])
    # mastros com bandeiras (Brasil e Minas)
    ret(d, 3, 0, 3, 13, C['ci0'])
    ret(d, 4, 0, 10, 4, C['g1'])
    d.polygon([(5, 2), (7, 0), (9, 2), (7, 4)], fill=rgba(C['am']))
    px(d, 7, 2, C['a1'])
    ret(d, 36, 0, 36, 13, C['ci0'])
    ret(d, 29, 0, 35, 4, C['br'])
    d.polygon([(31, 3), (32, 1), (33, 3)], fill=rgba(C['vm']))
    return s


def m_capela_gotica():
    """Capelinha gótica do cemitério: torre pontuda, janela ogival e vitral roxo."""
    s, d = spr(24, 36)
    p0, p1, p2, p3 = (52, 44, 72), (84, 72, 108), (120, 104, 148), (164, 148, 188)
    ret(d, 3, 18, 20, 35, p1)
    ret(d, 15, 18, 20, 35, p0)
    d.polygon([(1, 19), (11, 10), (22, 19)], fill=rgba(p0))
    ret(d, 8, 4, 14, 18, p2)
    ret(d, 12, 4, 14, 18, p1)
    d.polygon([(7, 5), (11, -6), (15, 5)], fill=rgba(p1))
    d.polygon([(11, -6), (15, 5), (11, 5)], fill=rgba(p0))
    ret(d, 11, -10, 11, -6, p3)
    ret(d, 10, -9, 12, -9, p3)
    # janelas ogivais com luz roxa
    d.polygon([(10, 12), (11, 9), (12, 12)], fill=rgba((216, 160, 255)))
    ret(d, 10, 12, 12, 15, (216, 160, 255))
    for x in (5, 16):
        ret(d, x, 23, x + 1, 28, (176, 112, 232))
        px(d, x, 22, (176, 112, 232))
    d.polygon([(8, 35), (8, 29), (11, 26), (15, 29), (15, 35)], fill=rgba((28, 20, 40)))
    # pináculos
    for x in (2, 20):
        ret(d, x, 15, x + 1, 19, p2)
        px(d, x, 14, p3)
    return s


def morcego(base, x, y, abre):
    s, d = spr(9, 5)
    c = (40, 28, 56)
    ret(d, 3, 1, 5, 3, c)
    px(d, 3, 0, c)
    px(d, 5, 0, c)
    px(d, 3, 2, (255, 220, 96))
    px(d, 5, 2, (255, 220, 96))
    if abre:
        ret(d, 0, 0, 2, 1, c)
        ret(d, 6, 0, 8, 1, c)
        px(d, 0, 2, c)
        px(d, 8, 2, c)
    else:
        ret(d, 0, 2, 2, 3, c)
        ret(d, 6, 2, 8, 3, c)
        px(d, 1, 4, c)
        px(d, 7, 4, c)
    base.alpha_composite(s, (x - 4, y - 2))


def cruz(base, x, y, var):
    s, d = spr(5, 8)
    c1, c2 = ((176, 168, 192), (120, 112, 140)) if var % 2 else ((148, 140, 164), (96, 88, 116))
    ret(d, 2, 0, 2, 7, c1)
    ret(d, 0, 2, 4, 2, c1)
    px(d, 3, 3, c2)
    ret(d, 2, 4, 2, 7, c2)
    colar(base, s, x, y, (28, 20, 40))


def lapide(base, x, y):
    s, d = spr(5, 6)
    d.rounded_rectangle([0, 0, 4, 5], radius=2, fill=rgba((150, 144, 164)))
    ret(d, 3, 1, 4, 5, (108, 100, 128))
    px(d, 1, 1, (196, 190, 210))
    colar(base, s, x, y, (28, 20, 40))


def m_coreto():
    s, d = spr(22, 18)
    ret(d, 4, 7, 17, 15, C['pa'])
    for x in (5, 10, 16):
        ret(d, x, 8, x, 15, C['pa2'])
    d.polygon([(2, 8), (11, 1), (19, 8)], fill=rgba(C['vm']))
    d.polygon([(11, 1), (19, 8), (11, 8)], fill=rgba(C['vm2']))
    ret(d, 11, 0, 11, 1, C['am'])
    ret(d, 2, 15, 19, 17, C['pa2'])
    ret(d, 2, 15, 19, 15, C['pa'])
    return s


def m_estatua_soldado():
    s, d = spr(12, 26)
    bz, bz2, bz3 = (120, 104, 72), (84, 72, 52), (168, 150, 100)
    ret(d, 1, 12, 10, 25, C['pa'])
    ret(d, 8, 12, 10, 25, C['pa2'])
    ret(d, 0, 23, 11, 25, C['pa2'])
    ret(d, 3, 17, 7, 19, (200, 180, 120))
    ret(d, 4, 3, 7, 11, bz)
    ret(d, 6, 3, 7, 11, bz2)
    ret(d, 3, 1, 7, 3, bz2)
    px(d, 4, 1, bz3)
    ret(d, 8, 4, 11, 5, bz)
    ret(d, 2, 4, 2, 11, bz2)
    px(d, 5, 5, bz3)
    return s


def m_helicoptero():
    s, d = spr(30, 16)
    ret(d, 8, 5, 22, 11, C['ci1'])
    ret(d, 8, 5, 22, 6, C['ci2'])
    ret(d, 18, 6, 22, 9, C['a3'])
    px(d, 19, 6, C['a4'])
    ret(d, 0, 6, 8, 7, C['ci1'])
    ret(d, 0, 4, 1, 8, C['ci0'])
    ret(d, 10, 7, 14, 9, C['g1'])
    d.polygon([(11, 8), (12, 7), (13, 8), (12, 9)], fill=rgba(C['am']))
    ret(d, 14, 2, 15, 4, C['ci0'])
    ret(d, 2, 1, 29, 1, C['ci0'])
    ret(d, 8, 13, 23, 13, C['ci0'])
    px(d, 10, 12, C['ci0'])
    px(d, 20, 12, C['ci0'])
    ret(d, 6, 14, 25, 15, C['pa2'])
    return s


def m_locomotiva():
    s, d = spr(48, 18)
    # vagão
    ret(d, 0, 6, 15, 14, C['am2'])
    ret(d, 0, 6, 15, 7, C['am'])
    for x in (2, 7, 12):
        ret(d, x, 9, x + 2, 11, C['a3'])
    # locomotiva a vapor (desenho próprio)
    ret(d, 18, 8, 37, 14, C['vm'])
    ret(d, 18, 8, 37, 8, C['vm3'])
    ret(d, 33, 3, 41, 14, C['vm2'])
    ret(d, 34, 5, 39, 8, C['a3'])
    ret(d, 22, 3, 24, 7, C['preto'])
    ret(d, 21, 2, 25, 2, C['preto'])
    ret(d, 16, 13, 43, 14, C['preto'])
    d.polygon([(42, 14), (47, 17), (42, 17)], fill=rgba(C['ci0']))
    for x in (4, 12, 22, 29, 38):
        d.ellipse([x - 2, 13, x + 2, 17], fill=rgba(C['preto']))
        px(d, x, 15, C['ci2'])
    for i, (x, y) in enumerate([(23, 0), (19, 0), (15, 1)]):
        d.ellipse([x - 1, y, x + 1, y + 1], fill=rgba(C['ci3']))
    return s


def m_estacao():
    s, d = spr(30, 20)
    ret(d, 1, 7, 28, 19, (236, 216, 176))
    ret(d, 22, 7, 28, 19, (204, 180, 140))
    ret(d, 0, 4, 29, 7, C['ru'])
    ret(d, 0, 3, 29, 3, C['ru3'])
    ret(d, 0, 7, 29, 7, C['ru2'])
    for x in (3, 10, 17):
        ret(d, x, 10, x + 3, 17, C['a1'])
        px(d, x, 10, C['a3'])
        d.point((x + 1, 9), fill=rgba(C['pa']))
    ret(d, 12, 0, 17, 3, C['pa'])
    d.ellipse([13, 0, 16, 3], fill=rgba(C['br']))
    px(d, 14, 1, C['preto'])
    ret(d, 0, 18, 29, 19, C['pa2'])
    return s


def m_lago_retrato():
    s, d = spr(46, 62)
    d.ellipse([0, 0, 45, 61], fill=rgba(C['areia']))
    d.ellipse([2, 1, 43, 59], fill=rgba(C['a0']))
    d.ellipse([3, 2, 42, 58], fill=rgba(C['a1']))
    d.ellipse([6, 5, 39, 54], fill=rgba(C['a2']))
    d.ellipse([10, 9, 26, 28], fill=rgba(C['a3']))
    for x, y in [(12, 36), (30, 18), (24, 46), (33, 40), (16, 22)]:
        ret(d, x, y, x + 2, y, C['a4'])
    # pedalinho de cisne
    ret(d, 26, 30, 33, 33, C['br'])
    ret(d, 26, 33, 33, 33, C['ci2'])
    ret(d, 32, 26, 33, 30, C['br'])
    px(d, 34, 26, C['am'])
    ret(d, 27, 29, 29, 30, C['vm'])
    return s



# ---------------------------------------------------------------- linguagem do mapa (v3)
# Referência de estilo: mapa de mundo de plataforma de 16 bits (planaltos com paredão, morros arredondados,
# nuvens, cachoeira, flores, título colorido). Só a linguagem do gênero: nenhum personagem, item ou objeto
# característico de outro jogo (nada de canos, blocos "?", cogumelos, morros ou nuvens com olhos).
def morro_pilula(lay, cx, by, w, h, tom=1):
    """Morro arredondado alto (forma de cápsula), luz da esquerda."""
    if tom:
        base_, sombra_, luz_, brilho = (64, 176, 72), (40, 136, 56), (128, 216, 96), (196, 244, 148)
    else:
        base_, sombra_, luz_, brilho = (44, 140, 76), (28, 108, 60), (80, 172, 96), (128, 204, 120)
    s, d = spr(w, h)
    d.ellipse([0, 0, w - 1, w - 1], fill=rgba(base_))
    ret(d, 0, w // 2, w - 1, h - 1, base_)
    d.ellipse([w * 0.62, 2, w - 1, w - 2], fill=rgba(sombra_))
    ret(d, round(w * 0.62), w // 2, w - 1, h - 1, sombra_)
    d.ellipse([w * 0.18, 4, w * 0.4, w * 0.6], fill=rgba(luz_))
    ret(d, round(w * 0.18), round(w * 0.3), round(w * 0.4), round(h * 0.7), luz_)
    d.ellipse([w * 0.22, 6, w * 0.32, 6 + w * 0.16], fill=rgba(brilho))
    colar(lay, s, cx, by, C['gl'])


def planalto(lay, x0, y0, x1, y1, falesia, escuro=False, raio=14):
    """Planalto: topo de grama arredondado e paredão de pedra em camadas embaixo."""
    topo = Image.new('L', (W, H), 0)
    ImageDraw.Draw(topo).rounded_rectangle([x0, y0, x1, y1], radius=raio, fill=255)
    t = np.array(topo) > 0
    dep = np.zeros(t.shape, int)
    for k in range(1, falesia + 1):
        m = np.zeros_like(t)
        m[k:, :] = t[:-k, :]
        dep[(dep == 0) & m & ~t] = k
    cl = dep > 0
    if escuro:
        pedra = [(156, 136, 168), (116, 100, 136), (84, 70, 104), (52, 42, 72)]
        grama = [(70, 56, 100), (96, 78, 128), (128, 108, 160), (164, 144, 192)]
        borda = (22, 14, 34)
    else:
        pedra = [(236, 192, 120), (204, 148, 80), (164, 104, 52), (112, 66, 34)]
        grama = [C['g1'], C['g2'], C['g3'], C['g4']]
        borda = (56, 30, 14)
    a = np.zeros((H, W, 4), np.uint8)
    cx = (x0 + x1) / 2
    w = x1 - x0
    xx = np.arange(W)[None, :].repeat(H, 0)
    idx = np.where(dep <= 1, 3, np.where(dep == falesia, 3, 1 + ((dep - 2) // 3) % 2))
    idx = np.where(xx < cx - w * 0.3, idx - 1, idx)
    idx = np.where(xx > cx + w * 0.3, np.minimum(idx + 1, 3), idx)
    rach = np.zeros(W, bool)
    rach[random.sample(range(W), W // 7)] = True
    idx = np.where(rach[None, :] & (dep > 3) & (dep < falesia - 1) & ((dep + xx) % 5 != 0), 3, idx)
    idx = np.clip(idx, 0, 3)
    for i, c in enumerate(pedra):
        a[cl & (idx == i)] = rgba(c)
    # topo com chanfro de luz em cima e à esquerda
    im = Image.fromarray(a)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x0, y0, x1, y1], radius=raio, fill=rgba(grama[0]))
    d.rounded_rectangle([x0 + 1, y0, x1 - 1, y1 - 2], radius=max(2, raio - 1), fill=rgba(grama[2]))
    d.rounded_rectangle([x0 + 3, y0 + 2, x1 - 2, y1 - 3], radius=max(2, raio - 3), fill=rgba(grama[1]))
    for _ in range(int(w * (y1 - y0) / 40)):
        x, y = random.randint(x0 + 4, x1 - 4), random.randint(y0 + 4, y1 - 4)
        if t[y, x]:
            d.point((x, y), fill=rgba(grama[3]))
            d.point((x + 1, y + 1), fill=rgba(grama[0]))
    lay.alpha_composite(contorno(im, borda))


def nuvem(base, cx, cy, w):
    s, d = spr(w, w // 2 + 2)
    h = w // 2
    for (ex, ey, r) in [(0.28, 0.6, 0.26), (0.5, 0.45, 0.32), (0.74, 0.62, 0.24), (0.5, 0.75, 0.3)]:
        d.ellipse([w * (ex - r), h * ey - w * r * 0.7, w * (ex + r), h * ey + w * r * 0.7], fill=rgba((255, 255, 255)))
    a = np.array(s)
    yy = np.arange(a.shape[0])[:, None]
    som = (a[:, :, 3] > 0) & (yy > h * 0.72)
    a[som, :3] = (200, 228, 255)
    colar(base, Image.fromarray(a), cx, cy + h // 2, (88, 136, 200))


def cachoeira(base, x0, y0, x1, y1):
    d = ImageDraw.Draw(base)
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            fase = (x * 3 + y) % 7
            c = C['a4'] if fase < 2 else (C['a3'] if fase < 5 else C['a2'])
            d.point((x, y), fill=rgba(c))
    d.line([(x0 - 1, y0), (x0 - 1, y1)], fill=rgba(C['a0']))
    d.line([(x1 + 1, y0), (x1 + 1, y1)], fill=rgba(C['a0']))
    for k in range(5):
        d.ellipse([x0 - 4 + k * 3, y1 - 2, x0 + k * 3 + 1, y1 + 3], fill=rgba(C['br']))


def titulo_colorido(txt, esc=3):
    cores = [C['vm'], C['am'], (72, 184, 72), (56, 120, 232)]
    letras = []
    for k, ch in enumerate(txt):
        letras.append(texto_img(ch, cores[k % 4], cores[k % 4], esc))
    passo = 6 * esc + 3
    w = passo * len(txt) + 8
    im = camada(w, 9 * esc + 8)
    for k, l in enumerate(letras):
        im.alpha_composite(l, (4 + k * passo, 4 - 2 * esc))
    a = np.array(im)
    m = a[:, :, 3] > 0
    # brilho na metade de cima de cada letra
    yy = np.arange(a.shape[0])[:, None]
    claro = m & (yy < 4 + 3 * esc)
    a[claro, :3] = np.minimum(255, a[claro, :3].astype(int) + 60)
    im = Image.fromarray(a)
    im = contorno(im, (24, 20, 32))
    out = camada(im.width + 2, im.height + 2)
    sombra = np.array(im)
    sombra[sombra[:, :, 3] > 0] = (24, 20, 32, 160)
    out.alpha_composite(Image.fromarray(sombra), (2, 2))
    out.alpha_composite(im, (0, 0))
    return out


def flor(base, x, y, cor):
    d = ImageDraw.Draw(base)
    for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
        d.point((x + dx, y + dy), fill=rgba(cor))
    d.point((x, y), fill=rgba((255, 208, 48)))


def m_hotel_coroados():
    """Hotel Coroados (fotos e satélite de 03/11/2026): prédio comprido de 2 andares, branco com faixas
    vermelho-terracota e telhado escalonado, ao longo da Rua São Judas Tadeu. A rua passa por baixo de uma
    marquise apoiada em pilares. Piscina na ponta norte. Aqui o prédio fica a oeste da rua (à esquerda)."""
    br, br2 = (244, 240, 232), (208, 200, 192)
    vm, vm2, vm3 = (204, 88, 64), (150, 56, 44), (232, 128, 100)
    s, d = spr(46, 92)
    # piscina (ponta norte)
    ret(d, 4, 0, 24, 8, (232, 228, 216))
    ret(d, 6, 2, 22, 6, C['a2'])
    ret(d, 7, 2, 12, 3, C['a4'])
    # módulos escalonados descendo o morro
    for i in range(6):
        y = 10 + i * 13
        x0 = 2 + (i % 2) * 2
        ret(d, x0, y, x0 + 26, y + 3, vm)
        ret(d, x0, y, x0 + 26, y, vm3)
        for k in range(x0, x0 + 27, 3):
            px(d, k, y + 2, vm2)
        ret(d, x0, y + 4, x0 + 26, y + 10, br)
        ret(d, x0 + 20, y + 4, x0 + 26, y + 10, br2)
        for wx in range(x0 + 2, x0 + 20, 5):
            ret(d, wx, y + 5, wx + 2, y + 7, (48, 52, 64))
            px(d, wx, y + 5, (120, 136, 160))
        ret(d, x0, y + 11, x0 + 26, y + 12, vm)
    # marquise sobre a rua, com pilares do outro lado (a rua passa por baixo)
    ret(d, 26, 46, 45, 50, vm)
    ret(d, 26, 46, 45, 46, vm3)
    ret(d, 26, 51, 45, 51, vm2)
    for x in (41, 44):
        ret(d, x, 52, x + 1, 58, br)
        ret(d, x, 56, x + 1, 58, vm)
    return s


def m_agonia_santuario():
    """Santuário N. Sra. da Agonia (fotos do Pedro, 03/11/2026): pirâmide de vidro azul em degraus, nervuras
    brancas nos cantos, cúpula prateada com cruz, anexos brancos e azuis na base e a torre-agulha azul na frente."""
    s, d = spr(44, 44)
    vid, vid2, vid3, vid4 = (64, 164, 224), (32, 104, 176), (144, 216, 248), (24, 64, 128)
    br, br2 = (236, 242, 250), (176, 196, 220)
    # anexos na base
    ret(d, 0, 34, 43, 43, br)
    ret(d, 0, 34, 43, 35, br2)
    ret(d, 32, 34, 43, 43, br2)
    for x in range(2, 42, 4):
        ret(d, x, 38, x + 1, 40, vid2)
    ret(d, 3, 36, 9, 42, (96, 128, 200))  # painel azul com a imagem
    ret(d, 5, 37, 7, 41, br)
    # degraus da pirâmide (de baixo para cima)
    for i, (w_, y_) in enumerate([(34, 29), (28, 24), (22, 19), (16, 14)]):
        x0 = 22 - w_ // 2
        ret(d, x0, y_, x0 + w_ - 1, y_ + 5, vid)
        ret(d, x0, y_ + 3, x0 + w_ - 1, y_ + 5, vid2)
        ret(d, 22, y_ + 1, x0 + w_ - 1, y_ + 5, vid2)
        ret(d, x0, y_ + 1, 21, y_ + 2, vid3)
        ret(d, x0 - 1, y_, x0 + w_, y_, br)
        for x in range(x0 + 2, x0 + w_ - 1, 3):
            px(d, x, y_ + 4, vid4)
    # nervuras diagonais dos cantos até a cúpula
    for x0_, x1_ in ((5, 16), (38, 27)):
        d.line([(x0_, 34), (x1_, 13)], fill=rgba(br), width=2)
    d.line([(22, 34), (22, 13)], fill=rgba(br2), width=1)
    # cúpula prateada
    d.ellipse([14, 3, 30, 19], fill=rgba((200, 206, 216)))
    ret(d, 14, 11, 30, 14, (200, 206, 216))
    d.ellipse([16, 4, 23, 12], fill=rgba((240, 244, 248)))
    d.ellipse([25, 6, 30, 14], fill=rgba((144, 152, 168)))
    for x in (18, 22, 26):
        d.line([(x, 5), (x, 14)], fill=rgba((160, 168, 184)))
    ret(d, 14, 13, 30, 14, (120, 128, 148))
    ret(d, 22, 0, 22, 3, C['am'])
    ret(d, 21, 1, 23, 1, C['am'])
    # torre-agulha azul na frente
    d.polygon([(38, 43), (40, 22), (42, 43)], fill=rgba(vid))
    d.line([(40, 22), (40, 43)], fill=rgba(vid3))
    return s


def m_prefeitura_itajuba():
    """Prefeitura (foto do Pedro, 03/11/2026): duas alas compridas branco-azuladas com faixas cinza, bloco central
    amarelo com placa azul e entrada de vidro, torrinha em cima, escadaria larga até a avenida, palmeiras."""
    s, d = spr(52, 38)
    pa, pa2, faixa, jan = (224, 234, 246), (184, 198, 218), (150, 162, 182), (48, 72, 128)
    for x0, x1 in ((0, 18), (33, 51)):
        ret(d, x0, 10, x1, 25, pa)
        ret(d, x0, 9, x1, 9, (112, 124, 144))
        for y in (13, 18, 23):
            ret(d, x0, y, x1, y, faixa)
            for x in range(x0 + 1, x1, 2):
                px(d, x, y - 1, jan)
        ret(d, x1 - 3 if x0 else x1 - 3, 10, x1, 25, pa2)
    # bloco central
    ret(d, 18, 5, 33, 26, (232, 200, 72))
    ret(d, 18, 5, 19, 26, (248, 224, 120))
    ret(d, 31, 5, 33, 26, (196, 160, 48))
    ret(d, 20, 6, 31, 8, (40, 72, 176))
    for x in range(21, 31, 2):
        px(d, x, 7, C['br'])
    ret(d, 21, 10, 30, 25, (56, 104, 184))
    for y in range(11, 25, 3):
        ret(d, 21, y, 30, y, (136, 184, 232))
    for x in (23, 26, 29):
        ret(d, x, 10, x, 25, (32, 64, 128))
    ret(d, 23, 1, 28, 4, C['br'])
    ret(d, 23, 1, 28, 1, pa2)
    # escadaria
    for k, y in enumerate(range(27, 37)):
        ret(d, 20 - k // 3, y, 31 + k // 3, y, (200, 200, 196) if y % 2 else (160, 160, 156))
    # palmeiras
    for x in (8, 44):
        ret(d, x, 26, x, 35, C['mad1'])
        for dx, dy in ((-3, -1), (3, -1), (-2, -2), (2, -2), (0, -3)):
            d.line([(x, 26), (x + dx, 26 + dy)], fill=rgba(C['g1']))
        px(d, x, 25, C['g3'])
    return s


def m_kart_pista():
    """Kartódromo (satélite de 03/11/2026): pista sinuosa e comprida de norte a sul, com grama no meio,
    zebras nas curvas, e boxes, arquibancada e estacionamento na ponta sul, de frente para o lago."""
    s, d = spr(50, 58)
    d.rounded_rectangle([0, 0, 49, 44], radius=10, fill=rgba(C['g1']))
    d.rounded_rectangle([1, 1, 48, 42], radius=9, fill=rgba(C['g2']))
    pista = [(12, 6), (22, 4), (26, 12), (20, 18), (28, 22), (36, 8), (44, 14), (42, 26), (34, 30), (40, 38),
             (30, 41), (22, 34), (14, 40), (6, 34), (12, 26), (5, 18), (8, 9), (12, 6)]
    d.line(pista, fill=rgba(C['br']), width=7, joint='curve')
    d.line(pista, fill=rgba((84, 88, 100)), width=5, joint='curve')
    d.line(pista, fill=rgba((104, 108, 120)), width=1, joint='curve')
    for x, y in pista[1:-1:2]:
        px(d, x, y - 3, C['vm'])
        px(d, x + 1, y - 3, C['br'])
        px(d, x + 2, y - 3, C['vm'])
    # largada quadriculada
    for i in range(4):
        for j in range(2):
            px(d, 15 + i, 3 + j * 2 + i % 2, C['preto'] if (i + j) % 2 else C['br'])
    ret(d, 19, 0, 19, 5, C['ci0'])
    # boxes, arquibancada e estacionamento
    ret(d, 2, 45, 47, 57, (156, 156, 160))
    for x in range(4, 46, 6):
        ret(d, x, 52, x, 56, C['br'])
    ret(d, 4, 44, 20, 49, (236, 232, 224))
    ret(d, 4, 44, 20, 44, C['vm'])
    for x in range(6, 20, 3):
        px(d, x, 47, (72, 80, 96))
    ret(d, 26, 44, 44, 48, (120, 128, 144))
    for y in (45, 47):
        ret(d, 27, y, 43, y, (180, 188, 200))
    for x, c in [(8, C['vm']), (14, C['a1']), (32, C['am']), (38, C['br'])]:
        ret(d, x, 53, x + 2, 54, c)
    return s


def lago_parque(base, dl):
    """Lago do Parque Municipal (satélite): comprido de norte a sul, mais largo em cima, água esverdeada,
    calçada em volta e chafariz no meio da parte de cima."""
    pts = [(252, 108), (286, 106), (292, 116), (290, 140), (284, 160), (280, 184), (272, 200), (260, 200),
           (254, 186), (252, 160), (248, 132)]
    d = ImageDraw.Draw(base)
    d.polygon(pts, fill=rgba((200, 196, 184)))
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    a = np.array(m) > 0
    for k, c in enumerate([(36, 104, 92), (56, 140, 116), (84, 168, 136)]):
        e = a.copy()
        for _ in range(2 + k * 2):
            e2 = e.copy()
            e2[1:, :] &= e[:-1, :]
            e2[:-1, :] &= e[1:, :]
            e2[:, 1:] &= e[:, :-1]
            e2[:, :-1] &= e[:, 1:]
            e = e2
        ba = np.array(base)
        ba[e, :3] = c
        base.paste(Image.fromarray(ba))
    d = ImageDraw.Draw(base)
    d.polygon(pts, outline=rgba((120, 116, 104)))
    d.ellipse([258, 116, 272, 130], fill=rgba((112, 192, 160)))
    for x, y in [(262, 150), (274, 140), (266, 176), (276, 160), (258, 136)]:
        ret(d, x, y, x + 2, y, (168, 224, 196))
    # chafariz
    for dx, dy in ((0, -4), (-1, -3), (1, -3), (-2, -1), (2, -1), (0, -2)):
        px(d, 268 + dx, 126 + dy, C['br'])
    d.ellipse([265, 125, 271, 128], fill=rgba(C['a4']))
    dl.polygon(pts, fill=255)
    dl.rectangle([246, 104, 294, 202], fill=255)


def m_unifei_v2():
    """UNIFEI (fotos e satélite do Pedro, 04/11/2026): prédio principal branco com a fachada de vidro escuro
    no centro e a faixa azul curva com o nome; letras brancas gigantes no gramado da frente; prédios baixos
    brancos do campus, laguinho a oeste e campo de esportes."""
    s, d = spr(92, 60)
    d.rounded_rectangle([0, 4, 91, 59], radius=6, fill=rgba(C['g3']))
    d.rounded_rectangle([2, 6, 89, 57], radius=5, fill=rgba(C['g2']))
    # laguinho do campus (oeste)
    d.ellipse([4, 10, 18, 30], fill=rgba((56, 140, 116)))
    d.ellipse([6, 12, 14, 22], fill=rgba((84, 168, 136)))
    # prédios baixos do campus (telhado cinza claro)
    for x0, y0, w, h in [(22, 8, 16, 7), (22, 18, 16, 7), (72, 8, 16, 8), (72, 20, 9, 7), (83, 20, 6, 7)]:
        ret(d, x0, y0, x0 + w, y0 + h, (236, 236, 232))
        ret(d, x0, y0, x0 + w, y0 + 2, (200, 204, 208))
        ret(d, x0, y0 + h, x0 + w, y0 + h, (168, 172, 180))
        for x in range(x0 + 2, x0 + w - 1, 3):
            px(d, x, y0 + 4, (72, 88, 120))
    # campo de esportes
    ret(d, 72, 31, 89, 43, (72, 168, 72))
    d.rectangle([73, 32, 88, 42], outline=rgba(C['br']))
    ret(d, 80, 32, 80, 42, C['br'])
    # prédio principal: alas brancas e centro de vidro com a faixa azul
    ret(d, 40, 6, 70, 40, (246, 246, 244))
    ret(d, 64, 6, 70, 40, (210, 212, 216))
    for y in range(10, 38, 5):
        for x in (42, 45, 61, 64, 67):
            ret(d, x, y, x + 1, y + 1, (40, 48, 64))
    ret(d, 49, 6, 59, 40, (40, 56, 80))
    for y in range(9, 40, 3):
        ret(d, 49, y, 59, y, (72, 96, 132))
    for x in (51, 54, 57):
        ret(d, x, 9, x, 40, (28, 40, 60))
    ret(d, 50, 10, 53, 20, (96, 128, 168))
    d.rounded_rectangle([47, 2, 61, 8], radius=2, fill=rgba((40, 80, 200)))
    ret(d, 48, 2, 60, 3, (88, 128, 232))
    for x in range(49, 60, 2):
        px(d, x, 5, C['br'])
    # letras gigantes brancas no gramado
    t = texto_img('UNIFEI', (250, 250, 250), (150, 156, 164))
    s.alpha_composite(t, (27, 43))
    return s


def m_mansao(v):
    """Mansão do Pinheirinho: casa grande, piscina, gramado e muro."""
    s, d = spr(20, 16)
    ret(d, 0, 3, 19, 15, (176, 168, 152))
    ret(d, 1, 4, 18, 14, C['g2'])
    teto = [(196, 92, 60), (120, 124, 136), (176, 72, 52), (88, 92, 104)][v % 4]
    parede = [(246, 238, 220), (236, 236, 232), (240, 224, 196), (224, 228, 236)][v % 4]
    x0 = 1 if v % 2 else 7
    ret(d, x0, 1, x0 + 11, 9, parede)
    ret(d, x0, 0, x0 + 11, 3, teto)
    ret(d, x0, 0, x0 + 11, 0, tuple(min(255, c + 40) for c in teto))
    ret(d, x0 + 6, 0, x0 + 6, 3, tuple(max(0, c - 40) for c in teto))
    for x in range(x0 + 1, x0 + 11, 3):
        ret(d, x, 5, x + 1, 6, (64, 96, 140))
    ret(d, x0 + 5, 7, x0 + 6, 9, C['mad0'])
    px_ = 13 if v % 2 else 1
    ret(d, px_, 10, px_ + 5, 13, C['br'])
    ret(d, px_ + 1, 11, px_ + 4, 12, (72, 184, 232))
    px(d, px_ + 1, 11, (200, 240, 255))
    return s


def m_santa_casa():
    """Santa Casa de Itajubá (foto do Pedro, 04/11/2026): prédio alto branco com o letreiro vertical e a cruz de
    hospital, casarão antigo creme com cúpulas e telhado de barro à esquerda, torre fina da capela e o
    estacionamento na frente."""
    s, d = spr(66, 46)
    # estacionamento
    ret(d, 0, 38, 65, 45, (150, 150, 156))
    for x in range(2, 64, 5):
        ret(d, x, 39, x, 44, (220, 220, 220))
    for x, c in [(4, C['br']), (14, C['br']), (24, (60, 64, 80)), (40, C['br']), (50, C['vm']), (60, C['br'])]:
        ret(d, x - 1, 41, x + 2, 43, c)
        px(d, x, 41, (120, 160, 200))
    # torre fina da capela (esquerda)
    d.polygon([(2, 37), (5, 6), (8, 37)], fill=rgba((236, 230, 214)))
    d.line([(6, 8), (8, 37)], fill=rgba((200, 192, 172)))
    ret(d, 5, 2, 5, 6, C['ci0'])
    ret(d, 4, 3, 6, 3, C['ci0'])
    # casarão antigo creme com cúpulas
    ret(d, 9, 20, 38, 37, (236, 216, 164))
    ret(d, 32, 20, 38, 37, (212, 188, 136))
    ret(d, 9, 17, 38, 20, (168, 84, 60))
    ret(d, 9, 17, 38, 17, (200, 112, 84))
    for x0 in (11, 30):
        d.ellipse([x0, 11, x0 + 7, 19], fill=rgba((112, 128, 140)))
        ret(d, x0, 15, x0 + 7, 19, (112, 128, 140))
        px(d, x0 + 2, 13, (160, 176, 188))
        ret(d, x0 + 3, 9, x0 + 4, 11, (112, 128, 140))
    for y in (23, 30):
        for x in range(11, 37, 4):
            ret(d, x, y, x + 1, y + 3, (64, 104, 140))
            px(d, x, y, (236, 236, 240))
    ret(d, 9, 35, 38, 37, (120, 168, 196))
    # prédio alto branco do hospital
    ret(d, 40, 2, 63, 37, (246, 246, 244))
    ret(d, 58, 2, 63, 37, (208, 210, 214))
    ret(d, 39, 0, 64, 2, (176, 180, 188))
    for y in range(6, 34, 4):
        for x in range(48, 63, 3):
            ret(d, x, y, x + 1, y + 1, (56, 64, 84))
    for y in range(6, 32, 3):  # letreiro vertical
        ret(d, 42, y, 43, y + 1, (40, 40, 48))
    ret(d, 46, 32, 56, 37, (64, 168, 140))
    # cruz de hospital
    ret(d, 49, -1 + 1, 54, 0 + 1, C['br'])
    d.rectangle([47, -6 + 6, 56, 3 + 6], fill=rgba(C['br']))
    ret(d, 51, 1, 52, 8, C['vm'])
    ret(d, 48, 3, 55, 5, C['vm'])
    return s


def m_camara():
    """Câmara Municipal (foto do Pedro, 04/11/2026): prédio quadrado antigo, branco acinzentado, 2 andares,
    janelas em arco em cima, balaustrada no alto, escadaria na frente e palmeiras."""
    s, d = spr(36, 30)
    br, br2, br3 = (232, 234, 236), (196, 200, 206), (150, 156, 166)
    ret(d, 4, 4, 31, 25, br)
    ret(d, 26, 4, 31, 25, br2)
    ret(d, 3, 2, 32, 4, br2)
    for x in range(4, 32, 2):
        px(d, x, 1, br3)
    ret(d, 3, 1, 32, 1, br3)
    ret(d, 4, 14, 31, 15, br3)
    for x in (7, 12, 17, 22, 27):
        d.ellipse([x - 1, 6, x + 1, 9], fill=rgba((72, 80, 96)))
        ret(d, x - 1, 8, x + 1, 12, (72, 80, 96))
        ret(d, x - 1, 17, x + 1, 22, (72, 80, 96))
        px(d, x, 18, (140, 156, 176))
    ret(d, 14, 19, 20, 25, (88, 76, 64))
    for k, y in enumerate(range(25, 30)):
        ret(d, 12 - k, y, 22 + k, y, (176, 172, 164) if y % 2 else (140, 136, 128))
    for x in (1, 34):
        ret(d, x, 18, x, 29, C['mad1'])
        for dx, dy in ((-2, -1), (2, -1), (-1, -2), (1, -2)):
            d.line([(x, 18), (x + dx, 18 + dy)], fill=rgba(C['g1']))
    return s


def m_predio(v):
    """Prediozinho de apartamentos (como os da BPS e do centro)."""
    h = [16, 20, 24, 18][v % 4]
    s, d = spr(10, h)
    cor, cor2 = [((244, 244, 240), (204, 206, 210)), ((240, 228, 176), (206, 190, 136)),
                 ((236, 236, 240), (196, 198, 208)), ((248, 240, 228), (210, 200, 186))][v % 4]
    ret(d, 0, 1, 9, h - 1, cor)
    ret(d, 7, 1, 9, h - 1, cor2)
    ret(d, 0, 0, 9, 1, (150, 156, 166))
    for y in range(3, h - 3, 3):
        for x in (1, 4):
            ret(d, x, y, x + 1, y, (64, 80, 108))
    ret(d, 3, h - 3, 5, h - 1, (88, 76, 64))
    return s


# ---------------------------------------------------------------- mapa (em pé)
def main():
    base = terreno()
    d = ImageDraw.Draw(base)
    relevo_mask = Image.new('L', (W, H), 0)

    # ----- céu no alto, atrás dos morros
    ba = np.array(base)
    yy, xx = np.mgrid[0:H, 0:W]
    ceu = [(112, 184, 248), (136, 200, 252), (160, 214, 255), (184, 228, 255)]
    for k, c in enumerate(ceu):
        faixa = (yy >= k * 14) & (yy < (k + 1) * 14 + ((xx + yy) % 2) * 2)
        ba[faixa & (yy < 64), :3] = c
    base = Image.fromarray(ba)
    d = ImageDraw.Draw(base)
    nuvem(base, 36, 16, 44)
    nuvem(base, 318, 12, 52)
    nuvem(base, 330, 40, 30)

    # ----- morros arredondados em volta da cidade (o vale de Itajubá)
    serra = camada()
    for k in range(13):  # fileira de trás
        x = k * 30 + random.randint(-4, 4)
        morro_pilula(serra, x, 74, 26 + random.randint(0, 10), 34 + random.randint(0, 14), 0)
    for k in range(7):   # fileira da frente, nos cantos
        for x in (6 + k * 3, 354 - k * 3):
            pass
    for x, by_, w_, h_ in [(10, 88, 30, 52), (34, 86, 24, 36), (350, 100, 30, 56), (328, 92, 22, 34)]:
        morro_pilula(serra, x, by_, w_, h_, 1)
    for y in range(120, 640, 26):  # laterais
        morro_pilula(serra, 4 + random.randint(-3, 3), y + 30, 22 + random.randint(0, 6), 40 + random.randint(0, 10), 1)
        if y > 180:
            morro_pilula(serra, 356 + random.randint(-3, 3), y + 30, 22 + random.randint(0, 6), 40 + random.randint(0, 10), 1)
    base.alpha_composite(serra)

    # ----- planaltos: Coroados (morro comprido a oeste da BPS), Alameda, Agonia e cemitério
    morros = camada()
    planalto(morros, 14, 232, 92, 494, 12, raio=16)   # Coroados: crista comprida norte-sul
    planalto(morros, 20, 500, 98, 540, 10, raio=12)   # Alameda: morro com a rua
    planalto(morros, 178, 74, 242, 110, 12, raio=14)   # Agonia
    planalto(morros, 222, 250, 346, 424, 14, raio=18)  # Cruzeiro: bairro alto, no morro
    base.alpha_composite(morros)
    esc = camada()
    planalto(esc, 236, 252, 340, 320, 8, escuro=True, raio=14)   # cemitério, no alto do Cruzeiro
    base.alpha_composite(esc)

    relevo = np.maximum(np.array(serra)[:, :, 3], np.maximum(np.array(morros)[:, :, 3], np.array(esc)[:, :, 3]))

    livre = Image.new('L', (W, H), 0)
    dl = ImageDraw.Draw(livre)

    # ----- Av. BPS: eixo central da cidade, com o rio correndo no meio, até o lago
    # Av. Dr. Jerson Dias: corre de norte a sul a leste do lago e do kart e encontra a BPS
    jerson = [(298, 30), (298, 220), (288, 232), (262, 232)]
    linha_grossa(d, jerson, 13, C['ci0'])
    linha_grossa(d, jerson, 11, (112, 116, 128))
    for y in range(34, 220, 8):
        ret(d, 298, y, 298, y + 2, (236, 228, 200))
    dl.line(jerson, fill=255, width=15)
    eixo = [(124, H + 10), (124, 520), (124, 236), (128, 230), (262, 230), (268, 224), (268, 196)]
    linha_grossa(d, eixo, 24, C['ci0'])
    linha_grossa(d, eixo, 22, (112, 116, 128))
    linha_grossa(d, eixo, 12, C['g1'])  # canteiro gramado na beira do rio
    linha_grossa(d, eixo, 9, C['a0'])
    linha_grossa(d, eixo, 7, C['a1'])
    linha_grossa(d, eixo, 3, C['a2'])
    dl.line(eixo, fill=255, width=26)
    rio_mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(rio_mask).line(eixo, fill=255, width=9)
    rio_a = np.array(rio_mask) > 0
    # faixas da pista e brilhos na água
    for (x0, y0), (x1, y1) in zip(eixo, eixo[1:]):
        seg = int(math.hypot(x1 - x0, y1 - y0))
        for k in range(0, seg, 1):
            t = k / max(1, seg)
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            nx, ny = (-(y1 - y0) / max(1, seg), (x1 - x0) / max(1, seg))
            if k % 8 < 3:
                for lado in (-8.5, 8.5):
                    d.point((round(x + nx * lado), round(y + ny * lado)), fill=rgba((236, 228, 200)))
            if random.random() < 0.08:
                d.point((round(x + nx * random.choice((-2, 1))), round(y + ny * random.choice((-2, 1)))),
                        fill=rgba(C['a3']))
            if random.random() < 0.02:
                d.point((round(x), round(y)), fill=rgba(C['a4']))

    # ----- marcos fixos
    lago_parque(base, dl)

    # ----- cidade: ruas em grade e casario (a parte de baixo é a mais densa)
    zona = Image.new('L', (W, H), 0)
    dz = ImageDraw.Draw(zona)
    dz.polygon([(98, 250), (150, 236), (232, 248), (236, 300), (222, 380), (346, 380), (346, 632), (14, 632),
                (14, 560), (40, 556), (100, 520)], fill=255)
    dz.polygon([(98, 236), (98, 182), (154, 182), (240, 210), (240, 240)], fill=255)
    dz.ellipse([70, 80, 190, 168], fill=255)      # Pinheirinho (bairro das mansões)
    dz.rectangle([304, 196, 346, 230], fill=255)  # bairro da Prefeitura
    zona_a = (np.array(zona) > 0) & (relevo == 0)
    # casas também no alto do Cruzeiro (abaixo do cemitério)
    cruz_m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(cruz_m).rounded_rectangle([228, 334, 340, 420], radius=12, fill=255)
    zona_a |= np.array(cruz_m) > 0
    # Varginha: bairro baixo, com mais árvores entre as casas
    varginha = np.zeros((H, W), bool)
    varginha[442:600, 288:348] = True
    varginha[442:512, 232:348] = True
    # morros pequenos podem ter casas no Pinheirinho
    zona_a |= (np.array(zona) > 0) & (np.arange(H)[:, None] < 150) & (np.arange(H)[:, None] > 84)

    # ----- marcos (sprites), registrados na máscara
    praca = (226, 516, 284, 574)   # Praça: um quadrado
    ruanova = (138, 560, 214, 576)  # Rua Nova: rua larga
    MARCOS = [
        ('hotel', m_hotel_coroados(), (49, 418)),
        ('unifei', m_unifei_v2(), (194, 222)),
        ('prefeitura', m_prefeitura_itajuba(), (328, 170)),
        ('kart', m_kart_pista(), (270, 104)),
        ('agonia', m_agonia_santuario(), (210, 98)),
        ('capela', m_capela_gotica(), (294, 290)),
        ('coreto', m_coreto(), (196, 392)),
        ('santacasa', m_santa_casa(), (280, 486)),
        ('camara', m_camara(), (214, 500)),
        ('estacao', m_estacao(), (36, 584)),
        ('trem', m_locomotiva(), (40, 606)),
        ('soldado', m_estatua_soldado(), (98, 624)),
        ('heli', m_helicoptero(), (132, 628)),
    ]
    for _, s, (x, y) in MARCOS:
        dl.rectangle([x - s.width // 2 - 2, y - s.height - 2, x + s.width // 2 + 2, y + 3], fill=255)
    dl.rectangle([praca[0] - 3, praca[1] - 3, praca[2] + 3, praca[3] + 3], fill=255)
    dl.rectangle([ruanova[0] - 8, ruanova[1] - 9, ruanova[2] + 4, ruanova[3] + 3], fill=255)
    dl.rectangle([234, 248, 342, 330], fill=255)  # cemitério
    dl.rectangle([164, 364, 228, 404], fill=255)  # Praçonha
    dl.rectangle([70, 596, 160, 632], fill=255)   # Praça do Soldado
    dl.rectangle([0, 598, 70, 612], fill=255)     # trilho

    # ----- rota das fases
    N = {
        'trem': (54, 578), 'soldado': (114, 604), 'ruanova': (176, 568), 'praca': (255, 545),
        'alameda': (66, 522), 'coroados': (82, 376), 'pracona': (196, 404), 'cemiterio': (276, 300),
        'unifei': (194, 246), 'pinheirinho': (132, 118), 'agonia': (226, 102), 'kart': (284, 104),
        'lago': (298, 150), 'prefeitura': (328, 182),
        'j1': (144, 522), 'j2': (144, 360), 'j3': (144, 246), 'j4': (226, 404),
    }
    ROTAS = [
        [N['trem'], (54, 604), N['soldado']],
        [N['soldado'], (144, 604), (144, 568), N['ruanova']],
        [N['ruanova'], (226, 568), (226, 545), N['praca']],
        [N['praca'], (255, 522), N['j1']],
        [N['j1'], (102, 522), N['alameda']],
        [N['alameda'], (64, 500), (64, 376), N['coroados']],
        [N['coroados'], (110, 376), (110, 360), N['j2']],
        [N['j2'], (144, 404), N['pracona']],
        [N['pracona'], N['j4'], (226, 330), (252, 312), N['cemiterio']],
        [N['cemiterio'], (276, 262), (226, 262), (226, 246), N['unifei']],
        [N['unifei'], N['j3']],
        [N['j2'], N['j3']],
        [N['j3'], (144, 168), (132, 160), N['pinheirinho']],
        [N['pinheirinho'], (166, 118), (182, 102), N['agonia']],
        [N['agonia'], (244, 102), (244, 106), (284, 106), N['kart']],
        [N['kart'], (298, 104), N['lago']],
        [N['lago'], (298, 182), N['prefeitura']],
    ]
    for r in ROTAS:
        dl.line(r, fill=255, width=11)
    livre_a = (np.array(livre) > 0) | (relevo > 0) & ~zona_a

    # ruas em grade (como no satélite) e casario em lotes: 2 x 2 casas por quarteirão
    PX, PY, OX, OY = 20, 18, 4, 176
    livre_np0 = np.array(livre) > 0
    ba = np.array(base)
    rua_px = np.zeros((H, W), bool)
    for y in range(OY, H, PY):
        rua_px[y:y + 2, :] = True
    for x in range(OX, W, PX):
        rua_px[OY:, x:x + 2] = True
    rua_px &= zona_a & ~livre_np0
    rua_px[:OY, :] = False
    ba[rua_px, :3] = (184, 178, 164)
    sombra = np.zeros_like(rua_px)
    sombra[1:, :] = rua_px[:-1, :] & ~rua_px[1:, :]
    ba[sombra & zona_a & ~livre_np0, :3] = (150, 146, 136)
    base = Image.fromarray(ba)
    d = ImageDraw.Draw(base)

    ocup = livre_np0.copy()
    casas = []
    for by_ in range(OY, H, PY):
        for bx_ in range(OX, W, PX):
            for cx_, cy_ in ((bx_ + 6, by_ + 9), (bx_ + 15, by_ + 9), (bx_ + 6, by_ + 18), (bx_ + 15, by_ + 18)):
                x, y = cx_ + random.randint(-1, 0), cy_ - 1
                if not (8 < x < W - 8 and y < H - 6) or not zona_a[y - 6:y + 1, x - 4:x + 5].all():
                    continue
                if ocup[y - 6:y + 1, x - 4:x + 5].any() or random.random() < (0.55 if varginha[y, x] else 0.06):
                    continue
                ocup[y - 6:y + 1, x - 4:x + 5] = True
                casas.append((x, y))
    # bairro BPS também do lado oeste da avenida: uma fileira de casas entre o morro e a pista
    for y in range(252, 512, 9):
        x = 104
        if ocup[y - 6:y + 1, x - 4:x + 5].any() or relevo[y - 6:y + 1, x - 4:x + 5].any():
            continue
        ocup[y - 6:y + 1, x - 4:x + 5] = True
        casas.append((x, y))

    # Pinheirinho: bairro das mansões (as maiores casas da cidade), com piscina
    mansoes = []
    for _ in range(4000):
        x, y = random.randrange(80, 186), random.randrange(94, 168)
        if not zona_a[y - 8, x] or ocup[y - 15:y + 1, x - 10:x + 11].any():
            continue
        ocup[y - 15:y + 1, x - 10:x + 11] = True
        mansoes.append((x, y))

    arvores = []
    livre_np = np.array(livre) > 0
    serra_a = np.array(serra)[:, :, 3]
    esc_a = np.array(esc)[:, :, 3]
    morros_a = np.array(morros)[:, :, 3]
    for _ in range(5000):
        x, y = random.randrange(8, W - 8), random.randrange(60, H - 4)
        if zona_a[y, x] and random.random() < (0.35 if varginha[y, x] else 0.97):
            continue
        if livre_np[max(0, y - 9):y + 1, x - 4:x + 5].any() or ocup[y - 9:y + 1, x - 4:x + 5].any():
            continue
        if serra_a[y, x] > 0 and random.random() < 0.7:
            continue
        if esc_a[y, x] > 0:
            continue
        if morros_a[y, x] > 0 and (y > 500 or y < 130 or random.random() < 0.35):
            continue
        ocup[y - 9:y + 1, x - 4:x + 5] = True
        arvores.append((x, y))

    # ----- caminhos
    rua_coroados = [(66, 548), (64, 500), (64, 240), (70, 224), (96, 214), (118, 226)]
    linha_grossa(d, rua_coroados, 13, C['ci0'])
    linha_grossa(d, rua_coroados, 11, (112, 116, 128))
    for (x0, y0), (x1, y1) in zip(rua_coroados, rua_coroados[1:]):
        seg = int(math.hypot(x1 - x0, y1 - y0))
        for k in range(0, seg, 8):
            t = k / max(1, seg)
            ret(d, round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t), round(x0 + (x1 - x0) * t),
                round(y0 + (y1 - y0) * t) + 2, (236, 228, 200))
    for r in ROTAS:
        linha_grossa(d, r, 9, C['c0'])
    for r in ROTAS:
        linha_grossa(d, r, 7, C['c1'])
        linha_grossa(d, r, 5, C['c2'])
    for r in ROTAS:
        tot = 0
        for (x0, y0), (x1, y1) in zip(r, r[1:]):
            seg = math.hypot(x1 - x0, y1 - y0)
            k = 0
            while k < seg:
                if int(tot + k) % 6 < 2:
                    t = k / seg
                    d.point((round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t)), fill=rgba(C['c3']))
                k += 1
            tot += seg
    # pontes de madeira onde a rota cruza o rio
    feitas = []
    for r in ROTAS:
        for (x0, y0), (x1, y1) in zip(r, r[1:]):
            seg = int(math.hypot(x1 - x0, y1 - y0))
            for k in range(seg + 1):
                t = k / max(1, seg)
                x, y = round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t)
                if 0 <= y < H and 0 <= x < W and rio_a[y, x] and all(math.hypot(x - a, y - b) > 10 for a, b in feitas):
                    feitas.append((x, y))
                    horiz = abs(x1 - x0) > abs(y1 - y0)
                    if horiz:
                        ret(d, x - 7, y - 5, x + 7, y + 5, C['mad0'])
                        for xx in range(x - 6, x + 7):
                            ret(d, xx, y - 3, xx, y + 3, C['mad2'] if xx % 3 else C['mad1'])
                        ret(d, x - 7, y - 5, x + 7, y - 4, C['mad3'])
                        ret(d, x - 7, y + 4, x + 7, y + 5, C['mad1'])
                    else:
                        ret(d, x - 5, y - 7, x + 5, y + 7, C['mad0'])
                        for yy in range(y - 6, y + 7):
                            ret(d, x - 3, yy, x + 3, yy, C['mad2'] if yy % 3 else C['mad1'])

    # ----- Praçonha: a praça no meio do bairro BPS, bem verde, cheia de plantas, bancos e o coreto
    x0, y0, x1, y1 = 166, 366, 226, 402
    ret(d, x0 - 1, y0 - 1, x1 + 1, y1 + 1, C['ci0'])
    ret(d, x0, y0, x1, y1, (216, 208, 192))
    ret(d, x0 + 3, y0 + 3, x1 - 3, y1 - 3, C['g1'])
    ret(d, x0 + 4, y0 + 4, x1 - 4, y0 + 4, C['g3'])
    ret(d, (x0 + x1) // 2 - 1, y0 + 3, (x0 + x1) // 2 + 1, y1 - 3, (216, 208, 192))
    ret(d, x0 + 3, (y0 + y1) // 2 + 4, x1 - 3, (y0 + y1) // 2 + 6, (216, 208, 192))
    folha = [(40, 132, 56), (72, 176, 64), (120, 208, 80)]
    for bx, by_ in [(171, 372), (180, 371), (212, 372), (221, 373), (171, 396), (221, 396), (184, 398), (208, 398)]:
        d.ellipse([bx - 4, by_ - 3, bx + 4, by_ + 3], fill=rgba(C['gl']))
        d.ellipse([bx - 3, by_ - 3, bx + 3, by_ + 2], fill=rgba(folha[0]))
        d.ellipse([bx - 2, by_ - 3, bx + 1, by_], fill=rgba(folha[1]))
        px(d, bx - 1, by_ - 2, folha[2])
    for bx, by_ in [(176, 380), (216, 380)]:  # plantas altas de folhas compridas
        for dx, dy in ((-4, -6), (4, -6), (-5, -2), (5, -2), (0, -8), (-2, -7), (2, -7)):
            d.line([(bx, by_), (bx + dx, by_ + dy)], fill=rgba(folha[1]))
        px(d, bx, by_ - 8, folha[2])
    for fx, fy in [(186, 376), (205, 377), (189, 393), (203, 394)]:
        flor(base, fx, fy, random.choice([(255, 120, 160), C['br'], (255, 236, 96)]))
    for bx, by_ in [(181, 386), (209, 386)]:  # bancos
        ret(d, bx - 3, by_, bx + 3, by_ + 1, C['mad2'])
        px(d, bx - 3, by_ + 2, C['mad0'])
        px(d, bx + 3, by_ + 2, C['mad0'])

    # ----- Praça (quadrado) e Rua Nova (rua larga)
    x0, y0, x1, y1 = praca
    ret(d, x0 - 1, y0 - 1, x1 + 1, y1 + 1, C['ci0'])
    ret(d, x0, y0, x1, y1, (216, 208, 192))
    for yy in range(y0, y1 + 1, 4):
        for xx in range(x0 + (yy // 4) % 2 * 2, x1 + 1, 4):
            px(d, xx, yy, (196, 188, 172))
    ret(d, x0 + 6, y0 + 6, x1 - 6, y1 - 6, C['g2'])
    ret(d, x0 + 6, y0 + 6, x1 - 6, y0 + 6, C['g3'])
    mx, my = (x0 + x1) // 2, (y0 + y1) // 2
    ret(d, mx - 1, y0 + 6, mx + 1, y1 - 6, (216, 208, 192))
    ret(d, x0 + 6, my - 1, x1 - 6, my + 1, (216, 208, 192))
    d.ellipse([mx - 9, my - 7, mx + 9, my + 7], fill=rgba(C['pa2']))
    d.ellipse([mx - 8, my - 6, mx + 8, my + 6], fill=rgba(C['a1']))
    d.ellipse([mx - 6, my - 5, mx + 6, my + 4], fill=rgba(C['a2']))
    for ddx, ddy in [(-5, -3), (5, -3), (-6, 2), (6, 2)]:
        px(d, mx + ddx, my + ddy, C['a4'])
    ret(d, mx - 1, my - 7, mx + 1, my, (100, 112, 96))  # busto
    ret(d, mx - 1, my - 9, mx + 1, my - 8, (84, 96, 80))
    for ax, ay in [(x0 + 4, y0 + 10), (x1 - 4, y0 + 10), (x0 + 4, y1 - 1), (x1 - 4, y1 - 1),
                   (mx - 14, y0 + 10), (mx + 14, y0 + 10), (mx - 14, y1 - 1), (mx + 14, y1 - 1)]:
        arvore(base, ax, ay, 0)

    x0, y0, x1, y1 = ruanova
    ret(d, x0 - 2, y0 - 1, x1 + 2, y1 + 1, C['ci0'])
    ret(d, x0 - 2, y0, x1 + 2, y1, (104, 108, 120))
    ret(d, x0 - 2, y0, x1 + 2, y0 + 1, (200, 196, 184))
    ret(d, x0 - 2, y1 - 1, x1 + 2, y1, (200, 196, 184))
    for xx in range(x0, x1, 8):
        ret(d, xx, (y0 + y1) // 2, xx + 3, (y0 + y1) // 2, (240, 232, 200))
    # lojas de toldo listrado dos dois lados da Rua Nova
    toldos = [(C['vm'], C['br']), (C['a1'], C['br']), (C['g1'], C['am3']), (C['roxo'], C['am3'])]
    for i, xx in enumerate(range(x0, x1 - 8, 12)):
        for lado, yb in ((0, y0 - 2), (1, y1 + 10)):
            s, ds = spr(11, 10)
            ret(ds, 0, 0, 10, 9, C['pa'] if (i + lado) % 2 else (240, 220, 176))
            ret(ds, 0, 0, 10, 0, C['ru2'])
            ret(ds, 3, 6, 6, 9, C['mad1'])
            a1, b1 = toldos[(i + lado) % 4]
            for k in range(11):
                ret(ds, k, 3, k, 4, a1 if (k // 2) % 2 == 0 else b1)
            ret(ds, 0, 5, 10, 5, a1)
            colar(base, s, xx + 6, yb, C['c0'])

    # ----- trilho do trem
    ret(d, 0, 603, 72, 608, (120, 96, 72))
    for xx in range(0, 72, 3):
        ret(d, xx, 603, xx, 608, C['mad0'])
    ret(d, 0, 604, 72, 604, C['ci2'])
    ret(d, 0, 607, 72, 607, C['ci2'])
    # piso da Praça do Soldado
    d.rectangle([80, 606, 156, 632], fill=rgba((216, 208, 192)))
    d.rectangle([80, 606, 156, 606], fill=rgba(C['ci1']))

    # ----- objetos em ordem de profundidade
    obj = [(y, 'c', x) for x, y in casas] + [(y, 'a', x) for x, y in arvores] + [(y, 'm', x) for x, y in mansoes]
    for y, t, x in sorted(obj):
        if t == 'm':
            colar(base, m_mansao(random.randrange(4)), x, y, C['c0'])
        elif t == 'c':
            perto_bps = 100 < x < 172 and 236 < y < 520
            centro = y > 440 and x < 290
            if (perto_bps and random.random() < 0.3) or (centro and random.random() < 0.18):
                colar(base, m_predio(random.randrange(4)), x, y, C['c0'])
            else:
                casa(base, x, y, random.randrange(12))
        else:
            arvore(base, x, y, 0)

    # flores espalhadas na grama (fora da cidade, das ruas e dos planaltos escuros)
    cores_flor = [C['br'], (255, 120, 160), C['vm'], (255, 236, 96), (176, 140, 255)]
    for _ in range(4000):
        x, y = random.randrange(10, W - 10), random.randrange(70, H - 8)
        if ocup[y - 2:y + 3, x - 2:x + 3].any() or zona_a[y, x] or esc_a[y, x] or serra_a[y, x]:
            continue
        ocup[y - 2:y + 3, x - 2:x + 3] = True
        flor(base, x, y, random.choice(cores_flor))

    # cemitério: cruzes, lápides, cerca, capela e morcegos
    dd = ImageDraw.Draw(base)
    for k in range(240, 336, 3):
        if abs(k - 276) > 6:
            ret(dd, k, 314, k, 318, (60, 48, 84))
    ret(dd, 238, 315, 336, 315, (60, 48, 84))
    for i, (x, y) in enumerate([(248, 296), (258, 304), (240, 306), (318, 300), (326, 308), (310, 310), (264, 290),
                                (252, 284), (330, 292)]):
        if i % 3:
            cruz(base, x, y, i)
        else:
            lapide(base, x, y)
    for i, (x, y) in enumerate([(244, 250), (330, 262), (262, 236), (312, 230), (222, 276)]):
        morcego(base, x, y, i % 2)
    # árvores secas
    for tx, ty in [(244, 300), (332, 304)]:
        dd.line([(tx, ty), (tx, ty - 12)], fill=rgba((40, 28, 52)), width=2)
        dd.line([(tx, ty - 8), (tx - 4, ty - 13)], fill=rgba((40, 28, 52)))
        dd.line([(tx, ty - 10), (tx + 4, ty - 15)], fill=rgba((40, 28, 52)))

    # pinheiros (araucárias) no Pinheirinho
    for tx, ty in [(96, 100), (170, 96), (110, 140), (162, 138)]:
        s, ds = spr(11, 16)
        ret(ds, 5, 6, 5, 15, C['mad1'])
        for j, w_ in enumerate([3, 5, 7, 9, 11]):
            yb = 2 + j * 2
            ret(ds, 5 - w_ // 2, yb, 5 + w_ // 2, yb, C['g0'])
            px(ds, 5 - w_ // 2, yb - 1, C['g1'])
            px(ds, 5 + w_ // 2, yb - 1, C['g1'])
        ret(ds, 4, 0, 6, 1, C['g1'])
        colar(base, s, tx, ty, C['gl'])

    for _, s, (x, y) in sorted(MARCOS, key=lambda m: m[2][1]):
        colar(base, s, x, y, C['preto'])
    # lua minguante sobre a capela
    lua, dlua = spr(15, 15)
    dlua.ellipse([0, 0, 14, 14], fill=rgba((248, 240, 200)))
    dlua.ellipse([2, 1, 9, 9], fill=rgba((255, 252, 230)))
    la = np.array(lua)
    yy_, xx_ = np.mgrid[0:15, 0:15]
    la[((xx_ - 10) ** 2 + (yy_ - 5) ** 2) < 36, 3] = 0
    colar(base, Image.fromarray(la), 326, 248)

    # ----- pontos de fase
    ORDEM = ['trem', 'soldado', 'ruanova', 'praca', 'alameda', 'coroados', 'pracona', 'cemiterio', 'unifei',
             'pinheirinho', 'agonia', 'kart', 'lago', 'prefeitura']
    d = ImageDraw.Draw(base)
    for nome, (x, y) in N.items():
        if nome.startswith('j'):
            d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=rgba(C['c0']))
            d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=rgba(C['c3']))
            continue
        cor, cor2, cor3 = (C['vm'], C['vm2'], C['vm3']) if nome in ('prefeitura', 'cemiterio') else \
            (C['am'], C['am2'], C['am3'])
        d.ellipse([x - 6, y - 4, x + 6, y + 5], fill=rgba(C['mad0']))
        d.ellipse([x - 5, y - 4, x + 5, y + 3], fill=rgba(cor2))
        d.ellipse([x - 5, y - 4, x + 5, y + 2], fill=rgba(cor))
        d.rectangle([x - 2, y - 3, x, y - 2], fill=rgba(cor3))

    PLACAS = [
        ('TREM', 26, 618), ('PRAÇA DO SOLDADO', 208, 618), ('RUA NOVA', 176, 529), ('PRAÇA', 255, 578),
        ('ALAMEDA', 40, 536), ('COROADOS', 54, 428), ('PRAÇONHA', 196, 410), ('CEMITÉRIO', 288, 322),
        ('UNIFEI', 194, 252), ('PINHEIRINHO', 132, 124), ('AGONIA', 206, 124), ('KART', 242, 56),
        ('LAGO', 230, 160), ('PREFEITURA', 314, 190), ('AV. BPS', 160, 436), ('CÂMARA', 214, 456), ('SANTA CASA', 282, 488),
    ]
    for txt, x, y in PLACAS:
        w = len(txt) * 6 + 10
        x = min(max(x, w // 2 + 7), W - w // 2 - 7)
        placa(base, txt, x, min(y, H - 22))

    for k, nome in enumerate(ORDEM):
        x, y = N[nome]
        t = texto_img(str(k + 1), C['br'], C['preto']).crop((0, 2, 6 * len(str(k + 1)) + 1, 10))
        bx0, by0 = (x - 22, y - 6) if nome == 'lago' else (x + 5, y - 13)
        ret(d, bx0, by0, bx0 + t.width + 2, by0 + t.height + 1, C['preto'])
        ret(d, bx0 + 1, by0 + 1, bx0 + t.width + 1, by0 + t.height, C['vm2'])
        base.alpha_composite(t, (bx0 + 2, by0 + 1))

    for txt, bx, by_ in [('BAIRRO BPS', 190, 300), ('CENTRO', 172, 506), ('CRUZEIRO', 288, 392), ('VARGINHA', 318, 504)]:
        t = contorno(texto_img(txt, C['br'], C['preto']), C['preto'])
        base.alpha_composite(t, (bx - t.width // 2, by_))

    t = texto_img('RIO SAPUCAÍ', C['a4'], C['a0'])
    tv = t.rotate(90, expand=True)
    base.alpha_composite(tv, (119, 410))

    tit = titulo_colorido('ITAMANIA', 3)
    base.alpha_composite(tit, (W // 2 - tit.width // 2, 6))
    placa(base, 'MUNDO DE ITAJUBÁ', W // 2, 6 + tit.height - 2)

    fr = camada()
    df = ImageDraw.Draw(fr)
    for i, c in enumerate([C['mad0'], C['mad1'], C['mad2'], C['mad1'], C['mad0']]):
        df.rectangle([i, i, W - 1 - i, H - 1 - i], outline=rgba(c))
    base.alpha_composite(fr)

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    out = base.convert('RGB').resize((W * ESCALA, H * ESCALA), Image.NEAREST)
    out.save(SAIDA, optimize=True)
    print('ok', SAIDA, len(casas), 'casas', len(arvores), 'árvores')


if __name__ == '__main__':
    main()
