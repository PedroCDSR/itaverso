"""Proposta do mapa-múndi do Itamania (Itajubá em pixel art, linguagem de mapa de mundo de plataforma de 16 bits).

Gera ferramentas/arte/previas/mapa-mundi-proposta.png (640x360 nativo, ampliado 3x).
Posições seguem o esboço do Pedro (references/mapa/esboco-pedro.jpg), com o norte para cima.
Tudo é desenhado aqui, com formas próprias: nenhum tile ou sprite de outro jogo.

Uso: python3 ferramentas/mapa-mundi/gerar_mapa.py
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw

W, H = 640, 360
ESCALA = 3
random.seed(7)
np.random.seed(7)

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, '..', 'arte', 'previas', 'mapa-mundi-proposta.png')

# ---------------------------------------------------------------- paleta
C = {
    'g0': (40, 96, 56), 'g1': (64, 136, 64), 'g2': (100, 172, 72), 'g3': (148, 204, 88), 'g4': (196, 228, 120),
    'gl': (24, 64, 40),
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


# ---------------------------------------------------------------- mapa
def main():
    base = terreno()
    d = ImageDraw.Draw(base)

    # ----- serra no fundo (norte e laterais): Itajubá fica num vale
    for k in range(-1, 18):
        cx = k * 40 + random.randint(-8, 8)
        if 120 < cx < 300 and False:
            continue
        montanha(base, cx, 30 + random.randint(-4, 4), 70 + random.randint(-10, 20), 34 + random.randint(-6, 10),
                 ('m0', 'm1', 'm2', 'm3', 'm4'))
    for y in range(40, 350, 34):
        montanha(base, 6 + random.randint(-6, 4), y + 30, 50, 34 + random.randint(-4, 8))
        montanha(base, 636 + random.randint(-4, 6), y + 30, 50, 34 + random.randint(-4, 8))

    # ----- morros verdes da parte de cima (Agonia, Piranguinho, Kart)
    for cx, by, w, h in [(95, 92, 110, 34), (190, 80, 90, 26), (345, 84, 120, 46), (460, 70, 90, 24),
                         (590, 82, 80, 30), (40, 210, 50, 22), (105, 238, 70, 36)]:
        morro(base, cx, by, w, h)

    # ----- máscara de onde não pode ter casa nem árvore
    livre = Image.new('L', (W, H), 0)
    dl = ImageDraw.Draw(livre)

    # ----- rio Sapucaí: atravessa a cidade de leste para oeste, abaixo do centro (como no satélite)
    rio = catmull([(650, 286), (600, 290), (560, 272), (520, 282), (470, 300), (420, 290), (380, 268), (330, 270),
                   (290, 290), (250, 300), (205, 296), (160, 280), (110, 292), (60, 280), (-10, 286)], 10)
    linha_grossa(d, rio, 15, C['areia'])
    linha_grossa(d, rio, 13, C['a0'])
    linha_grossa(d, rio, 11, C['a1'])
    linha_grossa(d, rio, 5, C['a2'])
    linha_grossa(dl, rio, 19, 255) if False else dl.line(rio, fill=255, width=21)
    for i in range(0, len(rio), 3):
        x, y = rio[i]
        if random.random() < 0.5:
            dx = random.randint(-3, 3)
            d.line([(x + dx, y + random.randint(-2, 2)), (x + dx + 2, y)], fill=rgba(C['a3']))
        if random.random() < 0.15:
            d.point((x + random.randint(-3, 3), y + random.randint(-2, 2)), fill=rgba(C['a4']))

    # ----- nós e caminhos (rota de fases)
    N = {
        'trem': (48, 312), 'soldado': (128, 329), 'ruanova': (232, 328), 'alameda': (190, 252),
        'j1': (196, 204), 'coroados': (112, 196), 'j2': (206, 140), 'j3': (322, 140), 'unifei': (322, 112),
        'pracona': (334, 196), 'praca': (436, 248), 'cemiterio': (520, 206), 'j4': (512, 140),
        'lago': (530, 112), 'kart': (572, 58), 'agonia': (354, 52), 'piranguinho': (98, 56),
    }
    ROTAS = [
        ('trem', 'soldado'), ('soldado', 'ruanova'), ('ruanova', 'alameda'),
        ('alameda', 'j1'), ('j1', 'coroados'), ('j1', 'j2'), ('j2', 'j3'), ('j3', 'unifei'), ('j3', 'pracona'),
        ('pracona', 'praca'), ('praca', 'cemiterio'), ('cemiterio', 'j4'), ('j3', 'j4'), ('j4', 'lago'),
        ('lago', 'kart'), ('kart', 'agonia'),
    ]
    SECRETA = [('agonia', 'piranguinho')]

    def trajeto(a, b):
        (x0, y0), (x1, y1) = N[a], N[b]
        # caminhos em "L" suaves, como estradas de mapa
        if abs(x1 - x0) > 8 and abs(y1 - y0) > 8:
            meio = (x1, y0) if a in ('j3', 'j4', 'kart', 'lago') else (x0, y1)
            return catmull([(x0, y0), ((x0 + meio[0]) / 2, (y0 + meio[1]) / 2), meio,
                            ((meio[0] + x1) / 2, (meio[1] + y1) / 2), (x1, y1)], 6)
        return [(x0, y0), (x1, y1)]

    caminhos = [trajeto(a, b) for a, b in ROTAS]
    secretos = [trajeto(a, b) for a, b in SECRETA]
    for c in caminhos + secretos:
        dl.line(c, fill=255, width=13)

    # ----- marcos (posições e sprites)
    MARCOS = [
        ('trem', m_trem(), (40, 300)), ('soldado', m_soldado(), (124, 326)), ('ruanova', m_ruanova(), (232, 318)),
        ('alameda', m_alameda(), (168, 246)), ('coroados', m_hotel(), (96, 192)), ('unifei', m_unifei(), (300, 106)),
        ('pracona', m_praca_coreto(), (360, 196)), ('praca', m_praca_matriz(), (466, 246)),
        ('cemiterio', m_cemiterio(), (552, 204)), ('lago', m_lago(), (576, 132)), ('kart', m_kart(), (596, 50)),
        ('agonia', m_agonia(), (354, 46)), ('piranguinho', m_piranguinho(), (68, 54)),
    ]
    for _, s, (x, y) in MARCOS:
        dl.rectangle([x - s.width // 2 - 3, y - s.height - 3, x + s.width // 2 + 3, y + 3], fill=255)
    for nome in N:
        x, y = N[nome]
        dl.rectangle([x - 8, y - 8, x + 8, y + 8], fill=255)

    livre_a = np.array(livre)

    def pode(x, y, r=4):
        if not (8 <= x < W - 8 and 8 <= y < H - 8):
            return False
        return livre_a[max(0, y - r):y + 2, max(0, x - r):x + r].max() == 0

    # ----- cidade: casario no vale (entre os morros de cima e o rio), mais denso no centro
    pontos = []
    for _ in range(9000):
        x, y = random.randrange(150, 600), random.randrange(96, 340)
        cx, cy = 340, 220
        dist = ((x - cx) / 260) ** 2 + ((y - cy) / 130) ** 2
        if dist > 1 or random.random() < dist * 0.7:
            continue
        pontos.append((x, y))
    pontos += [(random.randrange(20, 150), random.randrange(250, 345)) for _ in range(700)]
    ocup = np.zeros((H, W), bool)
    casas = []
    for x, y in pontos:
        if not pode(x, y, 5):
            continue
        if ocup[y - 7:y + 2, x - 6:x + 6].any():
            continue
        ocup[y - 7:y + 2, x - 6:x + 6] = True
        casas.append((x, y))

    # ----- árvores: matas nos morros e ipês nas ruas
    arvores = []
    for _ in range(1400):
        x, y = random.randrange(10, W - 10), random.randrange(40, H - 6)
        perto_cidade = ((x - 340) / 260) ** 2 + ((y - 220) / 130) ** 2 < 1
        if perto_cidade and random.random() < 0.85:
            continue
        if not pode(x, y, 4) or ocup[y - 9:y + 1, x - 4:x + 5].any():
            continue
        ocup[y - 9:y + 1, x - 4:x + 5] = True
        arvores.append((x, y, 0))

    obj = sorted([(y, 'c', x, i) for i, (x, y) in enumerate(casas)] +
                 [(y, 'a', x, t) for (x, y, t) in arvores])

    # caminhos por baixo dos objetos
    for c in secretos:
        linha_grossa(d, c, 7, C['c0'])
        for i in range(0, len(c) - 1):
            pass
    for c in caminhos:
        linha_grossa(d, c, 9, C['c0'])
    for c in caminhos:
        linha_grossa(d, c, 7, C['c1'])
        linha_grossa(d, c, 5, C['c2'])
    # pontilhado no meio da estrada
    for c in caminhos:
        tot = 0
        for (x0, y0), (x1, y1) in zip(c, c[1:]):
            seg = math.hypot(x1 - x0, y1 - y0)
            k = 0
            while k < seg:
                if int(tot + k) % 6 < 2:
                    t = k / seg
                    d.point((round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t)), fill=rgba(C['c3']))
                k += 1
            tot += seg
    # caminho secreto: só pegadas (aparece quando a fase secreta é vencida)
    for c in secretos:
        tot = 0
        for (x0, y0), (x1, y1) in zip(c, c[1:]):
            seg = math.hypot(x1 - x0, y1 - y0)
            k = 0
            while k < seg:
                if int(tot + k) % 8 < 3:
                    t = k / seg
                    x, y = round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t)
                    d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=rgba(C['c2']))
                k += 1
            tot += seg

    # ponte de madeira onde a estrada da Rua Nova cruza o rio
    bx = N['ruanova'][0]
    ys = [y for x, y in rio if abs(x - bx) < 1.5]
    by = round(sum(ys) / len(ys)) if ys else 298
    ret(d, bx - 7, by - 10, bx + 7, by + 10, C['mad0'])
    for y in range(by - 9, by + 10):
        ret(d, bx - 5, y, bx + 5, y, C['mad2'] if y % 3 else C['mad1'])
    for x in (bx - 6, bx + 6):
        ret(d, x, by - 10, x, by + 10, C['mad3'])
        for y in (by - 10, by - 3, by + 4, by + 10):
            px(d, x, y, C['mad0'])

    for y, tipo, x, v in obj:
        if tipo == 'c':
            casa(base, x, y, v)
        else:
            arvore(base, x, y, v)

    # marcos
    for _, s, (x, y) in sorted(MARCOS, key=lambda m: m[2][1]):
        colar(base, s, x, y, C['preto'])

    # ----- pontos de fase: amarelo = fase, vermelho = fase com saída secreta, pequeno = cruzamento
    ORDEM = ['trem', 'soldado', 'ruanova', 'alameda', 'coroados', 'unifei', 'pracona', 'praca', 'cemiterio',
             'lago', 'kart', 'agonia']
    for nome, (x, y) in N.items():
        if nome.startswith('j'):
            d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=rgba(C['c0']))
            d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=rgba(C['c3']))
            continue
        cor, cor2, cor3 = (C['vm'], C['vm2'], C['vm3']) if nome == 'agonia' else \
            (C['am'], C['am2'], C['am3'])
        if nome == 'piranguinho':
            cor, cor2, cor3 = C['roxo'], (56, 40, 104), (176, 160, 240)
        d.ellipse([x - 6, y - 4, x + 6, y + 5], fill=rgba(C['mad0']))
        d.ellipse([x - 5, y - 4, x + 5, y + 3], fill=rgba(cor2))
        d.ellipse([x - 5, y - 4, x + 5, y + 2], fill=rgba(cor))
        d.rectangle([x - 2, y - 3, x, y - 2], fill=rgba(cor3))
    # ----- placas com os nomes
    PLACAS = [
        ('ESTAÇÃO', 40, 321), ('PRAÇA DO SOLDADO', 128, 344 - 4), ('RUA NOVA', 238, 336),
        ('ALAMEDA', 150, 254), ('COROADOS', 96, 202), ('UNIFEI', 284, 116), ('PRAÇONA?', 368, 204),
        ('PRAÇA E MATRIZ', 462, 256), ('CEMITÉRIO', 552, 214), ('LAGO', 572, 142), ('KART', 590, 66),
        ('AGONIA', 400, 40), ('PIRANGUINHO', 70, 64), ('AV. BPS', 262, 144),
    ]
    for txt, x, y in PLACAS:
        w = len(txt) * 6 + 10
        x = min(max(x, w // 2 + 8), W - w // 2 - 8)
        y = min(y, H - 24)
        placa(base, txt, x, y)

    # número de cada fase num selinho ao lado do ponto (ordem sugerida)
    for k, nome in enumerate(ORDEM):
        x, y = N[nome]
        t = texto_img(str(k + 1), C['br'], C['preto']).crop((0, 2, 6 * len(str(k + 1)) + 1, 10))
        bx0, by0 = x + 5, y - 13
        ret(d, bx0, by0, bx0 + t.width + 2, by0 + t.height + 1, C['preto'])
        ret(d, bx0 + 1, by0 + 1, bx0 + t.width + 1, by0 + t.height, C['vm2'])
        base.alpha_composite(t, (bx0 + 2, by0 + 1))

    # nome do rio, escrito na água
    t = texto_img('RIO SAPUCAÍ', C['a4'], C['a0'])
    base.alpha_composite(t, (560, 268))

    # ----- título
    placa(base, 'ITAMANIA', 222, 9, esc=2, cor=C['am'])

    # ----- rosa dos ventos simples
    rx, ry = 612, 318
    d.polygon([(rx, ry - 12), (rx + 3, ry), (rx - 3, ry)], fill=rgba(C['vm']))
    d.polygon([(rx, ry + 10), (rx + 3, ry), (rx - 3, ry)], fill=rgba(C['pa']))
    d.polygon([(rx - 10, ry), (rx, ry - 3), (rx, ry + 3)], fill=rgba(C['pa2']))
    d.polygon([(rx + 10, ry), (rx, ry - 3), (rx, ry + 3)], fill=rgba(C['pa2']))
    t = texto_img('N', C['br'], C['preto'])
    base.alpha_composite(t, (rx - 3, ry - 24))

    # ----- moldura
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
