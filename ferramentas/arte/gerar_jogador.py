"""Gera os quadros do Aladdin do jogo (design original e provisório) como matrizes de texto 32x48.

Saída: src/art/jogador.js (matrizes) e uma prévia PNG ampliada para conferir.
Uso: python3 ferramentas/arte/gerar_jogador.py <repo> <pasta_previa>
"""
import sys, math

L, A = 32, 48

# Paleta (um caractere por cor). '.' = transparente, 'k' = contorno (aplicado automaticamente).
PALETA = {
    'k': '#2E1A33',  # contorno
    's': '#D9956A',  # pele
    'S': '#B06E46',  # pele sombra
    'h': '#2A1A1C',  # cabelo
    'H': '#4A3030',  # cabelo brilho
    'g': '#6CC24A',  # túnica (verde da escola)
    'G': '#47913A',  # túnica sombra
    'r': '#FFB0FA',  # faixa (rosa da escola)
    'R': '#D57FCF',  # faixa sombra
    'c': '#F2DEB0',  # calça areia
    'C': '#CDB386',  # calça sombra
    'b': '#7A4A2A',  # sandália
    'w': '#FFFFFF',  # olho (branco)
    'e': '#2A1A1C',  # pupila
    'm': '#9A4040',  # boca
}


class Quadro:
    def __init__(self):
        self.p = [['.'] * L for _ in range(A)]

    def px(self, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < L and 0 <= y < A:
            self.p[y][x] = c

    def ret(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def elipse(self, cx, cy, rx, ry, c):
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                    self.px(x, y, c)

    def linha(self, x0, y0, x1, y1, larg, c):
        """Segmento grosso (membros)."""
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
        r = larg / 2
        for i in range(n + 1):
            t = i / n
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            for yy in range(int(y - r) - 1, int(y + r) + 2):
                for xx in range(int(x - r) - 1, int(x + r) + 2):
                    if (xx + 0.5 - x - 0.5) ** 2 + (yy + 0.5 - y - 0.5) ** 2 <= r * r:
                        self.px(xx, yy, c)

    def contorno(self):
        novo = [linha[:] for linha in self.p]
        for y in range(A):
            for x in range(L):
                if self.p[y][x] != '.':
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < L and 0 <= yy < A and self.p[yy][xx] not in '.k':
                        novo[y][x] = 'k'
                        break
        self.p = novo

    def texto(self):
        return [''.join(l) for l in self.p]


# ---------- partes (personagem olhando para a DIREITA) ----------

def perna(q, quadril, joelho, pe, frente):
    """Calça até o meio da canela, tornozelo de pele e sandália apontando para a frente."""
    cor, sombra = ('c', 'C') if frente else ('C', 'C')
    q.linha(*quadril, *joelho, 5, cor)
    # canela: 65% calça, resto pele
    mx = joelho[0] + (pe[0] - joelho[0]) * 0.6
    my = joelho[1] + (pe[1] - joelho[1]) * 0.6
    q.linha(*joelho, mx, my, 5, cor)
    q.linha(mx, my, pe[0], pe[1] - 1, 3, 's' if frente else 'S')
    # barra da calça (dobrada)
    q.linha(mx - 0.5, my, mx + 0.5, my, 5, sombra)
    # sandália
    q.ret(int(pe[0]) - 1, int(pe[1]), int(pe[0]) + 3, int(pe[1]) + 1, 'b')


def braco(q, ombro, cotovelo, mao, frente):
    cor = 's' if frente else 'S'
    q.linha(*ombro, *cotovelo, 3, cor)
    q.linha(*cotovelo, *mao, 3, cor)
    q.elipse(mao[0], mao[1], 1.6, 1.6, cor)


def corpo(q, dy=0, inclina=0):
    """Túnica + faixa. dy desce o tronco (respiração/agacho); inclina desloca o topo."""
    for y in range(19 + dy, 33 + dy):
        t = (y - 19 - dy) / 13
        desloc = int(round(inclina * (1 - t)))
        meia = 5 if y < 31 + dy else 6  # barra abre um pouco
        x0, x1 = 16 - meia + desloc, 16 + meia + desloc
        q.ret(x0, y, x1, y, 'g')
        q.ret(x0, y, x0 + 1, y, 'G')  # sombra nas costas
    # gola em V
    q.px(19 + inclina, 19 + dy, 's')
    q.px(19 + inclina, 20 + dy, 's')
    q.px(18 + inclina, 19 + dy, 's')
    # faixa rosa na cintura + ponta solta nas costas
    q.ret(11 + inclina // 2, 27 + dy, 21 + inclina // 2, 28 + dy, 'r')
    q.ret(11 + inclina // 2, 28 + dy, 21 + inclina // 2, 28 + dy, 'R')
    q.ret(10 + inclina // 2, 29 + dy, 11 + inclina // 2, 32 + dy, 'r')


def cabeca(q, dy=0, dx=0, olho='normal'):
    cx, cy = 17 + dx, 11 + dy
    # cabelo (volume cacheado atrás e em cima)
    q.elipse(cx - 1, cy - 1, 6.2, 5.5, 'h')
    for bx, by in ((-6, -2), (-5, 2), (-3, -5), (1, -6), (4, -5)):
        q.elipse(cx + bx, cy + by, 1.8, 1.8, 'h')
    # rosto
    q.elipse(cx + 2, cy + 2, 4.2, 4.6, 's')
    q.ret(cx + 1, cy + 5, cx + 4, cy + 6, 's')  # queixo
    q.ret(cx - 1, cy + 5, cx, cy + 6, 'S')  # mandíbula na sombra
    # orelha
    q.px(cx - 1, cy + 2, 'S')
    q.px(cx - 1, cy + 3, 'S')
    # faixa rosa na cabeça + pontas esvoaçantes atrás
    q.ret(cx - 6, cy - 3, cx + 5, cy - 2, 'r')
    q.ret(cx - 6, cy - 2, cx + 5, cy - 2, 'R')
    q.linha(cx - 7, cy - 2, cx - 10, cy + 1, 2, 'r')
    q.linha(cx - 7, cy - 1, cx - 9, cy + 3, 2, 'R')
    # brilho no cabelo
    q.px(cx - 2, cy - 5, 'H')
    q.px(cx - 1, cy - 5, 'H')
    # olho
    if olho == 'dano':
        q.px(cx + 3, cy + 1, 'e'); q.px(cx + 4, cy + 2, 'e'); q.px(cx + 4, cy + 1, 'e'); q.px(cx + 3, cy + 2, 'e')
    elif olho == 'fechado':
        q.px(cx + 3, cy + 2, 'e'); q.px(cx + 4, cy + 2, 'e')
    else:
        q.px(cx + 3, cy + 1, 'w'); q.px(cx + 3, cy + 2, 'w')
        q.px(cx + 4, cy + 1, 'e'); q.px(cx + 4, cy + 2, 'e')
    # sobrancelha e boca
    q.px(cx + 3, cy, 'h'); q.px(cx + 4, cy, 'h')
    q.px(cx + 4, cy + 4, 'm')
    if olho != 'dano':
        q.px(cx + 5, cy + 4, 'm')
    # pescoço
    q.ret(cx - 1, cy + 7, cx + 1, cy + 8, 'S')


# ---------- poses ----------

def pose(pernas, bracos, dy=0, inclina=0, olho='normal'):
    """pernas = ((joelho_tras, pe_tras), (joelho_frente, pe_frente)); bracos = ((cot_tras, mao_tras), (cot_fr, mao_fr))."""
    q = Quadro()
    quadril_t, quadril_f = (14, 33 + dy), (18, 33 + dy)
    ombro_t, ombro_f = (13 + inclina, 21 + dy), (19 + inclina, 21 + dy)
    # ordem de desenho: membros de trás, corpo, cabeça, membros da frente
    braco(q, ombro_t, *bracos[0], frente=False)
    perna(q, quadril_t, *pernas[0], frente=False)
    perna(q, quadril_f, *pernas[1], frente=True)
    corpo(q, dy, inclina)
    cabeca(q, dy, inclina, olho)
    braco(q, ombro_f, *bracos[1], frente=True)
    q.contorno()
    return q.texto()


QUADROS = {}

# parado (2): respiração = tronco 1 px para baixo
for i, d in enumerate((0, 1)):
    QUADROS[f'parado{i + 1}'] = pose(
        (((14, 39), (13, 45)), ((19, 39), (19, 45))),
        (((12, 26 + d), (12, 30 + d)), ((20, 26 + d), (21, 30 + d))),
        dy=d,
    )

# correndo (6): ciclo de pernas com braços alternados
CICLO = [
    # (joelho_t, pe_t, joelho_f, pe_f, mao_t, mao_f, dy)
    ((10, 38), (6, 42), (21, 38), (24, 45), (23, 27), (9, 29), 0),
    ((11, 39), (8, 44), (20, 38), (22, 45), (21, 28), (11, 29), 1),
    ((14, 39), (12, 45), (18, 37), (16, 41), (17, 29), (17, 29), 0),
    ((21, 38), (24, 45), (10, 38), (6, 42), (9, 29), (23, 27), 0),
    ((20, 38), (22, 45), (11, 39), (8, 44), (11, 29), (21, 28), 1),
    ((18, 37), (16, 41), (14, 39), (12, 45), (17, 29), (17, 29), 0),
]
for i, (jt, pt, jf, pf, mt, mf, d) in enumerate(CICLO):
    cot_t = ((13 + mt[0]) // 2, 25 + d)
    cot_f = ((19 + mf[0]) // 2, 25 + d)
    QUADROS[f'correndo{i + 1}'] = pose(((jt, pt), (jf, pf)), ((cot_t, mt), (cot_f, mf)), dy=d, inclina=1)

# pulando: joelhos encolhidos, braço da frente para cima
QUADROS['pulando'] = pose(
    (((19, 36), (14, 40)), ((23, 35), (19, 40))),
    (((10, 19), (9, 15)), ((22, 17), (23, 12))),
)
# caindo: pernas esticadas e abertas, braços abertos
QUADROS['caindo'] = pose(
    (((13, 40), (11, 45)), ((21, 39), (23, 44))),
    (((9, 21), (6, 18)), ((24, 21), (27, 18))),
)
# arremessando (2): braço da frente para trás e depois esticado
QUADROS['arremessando1'] = pose(
    (((14, 39), (12, 45)), ((20, 39), (21, 45))),
    (((12, 26), (12, 30)), ((15, 18), (11, 14))),
    inclina=-1,
)
QUADROS['arremessando2'] = pose(
    (((13, 39), (11, 45)), ((21, 39), (23, 45))),
    (((12, 26), (11, 30)), ((24, 20), (29, 19))),
    inclina=1,
)
# dano: inclinado para trás, braços abertos, olhos em X
QUADROS['dano'] = pose(
    (((15, 39), (17, 45)), ((19, 39), (22, 44))),
    (((9, 20), (7, 16)), ((23, 20), (26, 16))),
    inclina=-2,
    olho='dano',
)

ORDEM = ['parado1', 'parado2'] + [f'correndo{i}' for i in range(1, 7)] + ['pulando', 'caindo', 'arremessando1', 'arremessando2', 'dano']


def escrever_js(caminho):
    linhas = [
        '// Aladdin do jogo: design ORIGINAL e provisório (cabelo cacheado, faixa rosa, túnica verde, calça areia).',
        '// Será redesenhado com base nos figurinos do espetáculo (references/figurinos/).',
        '// Cada quadro tem 32x48 caracteres; cada caractere é uma cor da PALETA (\'.\' = transparente).',
        '// Pode editar à mão: troque um caractere para mudar a cor daquele pixel.',
        '',
        'export const PALETA = {',
    ]
    for k, v in PALETA.items():
        linhas.append(f"  {k}: '{v}',")
    linhas += ['};', '', f'export const LARGURA = {L};', f'export const ALTURA = {A};', '',
               '// Ordem dos quadros na textura (o índice de cada um é a posição nesta lista).',
               'export const ORDEM = ' + repr(ORDEM).replace("'", "'") + ';', '', 'export const QUADROS = {']
    for nome in ORDEM:
        linhas.append(f'  {nome}: [')
        for l in QUADROS[nome]:
            linhas.append(f"    '{l}',")
        linhas.append('  ],')
    linhas.append('};')
    open(caminho, 'w').write('\n'.join(linhas) + '\n')


def previa(caminho, escala=4):
    try:
        from PIL import Image
    except ImportError:
        print('Pillow não instalado: sem prévia')
        return
    img = Image.new('RGBA', (len(ORDEM) * (L + 2) * escala, A * escala), (158, 158, 255, 255))
    for i, nome in enumerate(ORDEM):
        for y, l in enumerate(QUADROS[nome]):
            for x, c in enumerate(l):
                if c == '.':
                    continue
                cor = PALETA[c]
                rgb = tuple(int(cor[j:j + 2], 16) for j in (1, 3, 5))
                for yy in range(escala):
                    for xx in range(escala):
                        img.putpixel(((i * (L + 2) + x) * escala + xx, y * escala + yy), rgb + (255,))
    img.save(caminho)


if __name__ == '__main__':
    repo, pasta = sys.argv[1], sys.argv[2]
    escrever_js(f'{repo}/src/art/jogador.js')
    previa(f'{pasta}/jogador.png')
    print('quadros:', len(ORDEM))
