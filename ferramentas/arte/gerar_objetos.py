"""Gera a arte provisória (original) dos objetos da Fase 1 como matrizes de texto.

Capivara, maçã, sapatilha, coração e bandeira de checkpoint (a fonte da praça agora é PNG: gerar_cenarios.py).
Saída: src/art/objetos.js (matrizes) e uma prévia PNG ampliada para conferir.
Uso: python3 ferramentas/arte/gerar_objetos.py <repo> <pasta_previa>
"""
import sys

PALETA = {
    'k': '#2E1A33',  # contorno
    'w': '#FFFFFF',  # brilho
    'e': '#2A1A1C',  # olho
    # capivara
    'p': '#B07A48',  # pelo
    'P': '#8A5532',  # pelo sombra
    'q': '#CF9C68',  # pelo luz
    'n': '#5A3524',  # focinho
    'b': '#F2A3B5',  # bochecha
    # maçã
    'a': '#E0453A',
    'A': '#A82C2A',
    'g': '#6CC24A',  # folha (verde da escola)
    'G': '#47913A',
    'm': '#7A4A2A',  # cabinho / madeira
    'M': '#55311C',
    # sapatilha e coração
    'r': '#FFB0FA',  # rosa da escola
    'R': '#D57FCF',
    'x': '#FF5A7A',  # coração
    'X': '#C23A5A',
    'v': '#F9FCBB',  # amarelo claro da escola
    'V': '#D9D59A',
    # fonte (pedra e água)
    's': '#E6DCCB',
    'S': '#BBAE98',
    'T': '#8E8270',
    'u': '#BFE8F7',
    'U': '#6FB6DE',
    # bandeira
    'l': '#9E9EFF',  # lilás
    'L': '#6D6BD9',  # roxo
}


class Quadro:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.p = [['.'] * w for _ in range(h)]

    def px(self, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.w and 0 <= y < self.h:
            self.p[y][x] = c

    def ret(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def elipse(self, cx, cy, rx, ry, c, so_se=None):
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                    if so_se is None or so_se(x, y):
                        self.px(x, y, c)

    def contorno(self):
        novo = [l[:] for l in self.p]
        for y in range(self.h):
            for x in range(self.w):
                if self.p[y][x] != '.':
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < self.w and 0 <= yy < self.h and self.p[yy][xx] not in '.k':
                        novo[y][x] = 'k'
                        break
        self.p = novo
        return self

    def texto(self):
        return [''.join(l) for l in self.p]


# ---------------- capivara 32x24, olhando para a DIREITA ----------------
# Corpo de barril, cabeça quadradona com focinho reto, orelhinha, perninhas curtas. Fofa, nunca assustadora.

def capivara(pose='andar', passo=0, respira=0):
    q = Quadro(32, 24)
    dy = {'andar': 0, 'comer': 1, 'dormir': 4}[pose]
    if pose == 'dormir':
        dy -= respira
    # pernas (atrás do corpo)
    if pose != 'dormir':
        alt = [0, 1] if passo == 0 else [1, 0]
        for i, x in enumerate((7, 11, 18, 22)):
            sobe = alt[i % 2] if pose == 'andar' else 0
            q.ret(x, 18 + dy - sobe, x + 2, 21 - sobe, 'P')
    # corpo
    q.elipse(14, 13 + dy, 11, 6.5, 'p')
    q.elipse(14, 16 + dy, 9, 3, 'P', so_se=lambda x, y: y >= 15 + dy)
    q.elipse(13, 10 + dy, 7, 2.2, 'q')
    # cabeça
    hx, hy = 20, 5 + dy
    q.ret(hx, hy + 1, hx + 8, hy + 9, 'p')
    q.ret(hx + 1, hy, hx + 7, hy, 'p')
    q.ret(hx + 9, hy + 3, hx + 9, hy + 8, 'p')
    q.ret(hx + 1, hy + 1, hx + 6, hy + 2, 'q')
    q.ret(hx + 9, hy + 3, hx + 9, hy + 5, 'n')  # focinho
    q.px(hx + 8, hy + 4, 'n')
    q.ret(hx + 1, hy - 1, hx + 2, hy - 1, 'P')  # orelha
    q.px(hx + 6, hy + 7, 'b')  # bochecha
    q.px(hx + 7, hy + 7, 'b')
    # olho
    if pose == 'andar':
        q.ret(hx + 5, hy + 3, hx + 6, hy + 4, 'e')
        q.px(hx + 5, hy + 3, 'w')
    elif pose == 'comer':
        # olhinhos felizes ^
        q.px(hx + 4, hy + 4, 'e')
        q.px(hx + 5, hy + 3, 'e')
        q.px(hx + 6, hy + 4, 'e')
    else:
        q.ret(hx + 4, hy + 4, hx + 6, hy + 4, 'e')
    # maçã na boca
    if pose == 'comer':
        mx, my = hx + 10, hy + 8 - passo
        q.elipse(mx, my, 2.6 - passo * 0.6, 2.6 - passo * 0.6, 'a')
        q.px(mx - 1, my - 1, 'w')
        q.px(mx, my - 3 + passo, 'm')
    # rabinho
    q.px(3, 11 + dy, 'P')
    return q.contorno().texto()


def maca():
    q = Quadro(10, 10)
    q.elipse(4.5, 5.5, 3.6, 3.4, 'a')
    q.elipse(5.5, 7, 2.5, 1.6, 'A', so_se=lambda x, y: y >= 7)
    q.px(3, 4, 'w')
    q.px(3, 5, 'w')
    q.px(5, 1, 'm')
    q.px(5, 2, 'm')
    q.px(6, 1, 'g')
    q.px(7, 1, 'g')
    q.px(7, 0, 'G')
    return q.contorno().texto()


def sapatilha(brilho=0):
    # sapatilha de ponta vista de lado, com fitas cruzadas
    q = Quadro(16, 12)
    q.elipse(8, 7.5, 6, 2.6, 'r')
    q.ret(2, 8, 13, 9, 'R')  # sola
    q.ret(3, 5, 6, 6, 'r')
    q.px(13, 7, 'R')
    # boca da sapatilha
    q.ret(5, 5, 9, 5, 'R')
    # fitas
    for (x, y) in ((4, 4), (5, 3), (6, 2), (7, 1), (3, 3), (2, 2), (6, 4), (8, 3), (9, 2)):
        q.px(x, y, 'R')
    q.px(10, 6, 'w')
    if brilho:
        q.px(12, 2, 'v')
        q.px(13, 1, 'w')
        q.px(14, 2, 'v')
        q.px(13, 3, 'v')
    return q.contorno().texto()


def coracao(cheio=True):
    q = Quadro(11, 10)
    forma = [
        '.XX...XX.',
        'XxxX.XxxX',
        'XxwxXxxxX',
        'XxxxxxxxX',
        '.XxxxxxX.',
        '..XxxxX..',
        '...XxX...',
        '....X....',
    ]
    for y, l in enumerate(forma):
        for x, c in enumerate(l):
            if c == '.':
                continue
            if not cheio:
                c = {'X': 'L', 'x': 'l', 'w': 'l'}[c]
            q.px(x + 1, y + 1, c)
    return q.contorno().texto()


def bandeira(ativa=False):
    q = Quadro(16, 40)
    q.ret(3, 2, 4, 39, 'm')
    q.ret(4, 2, 4, 39, 'M')
    q.ret(2, 37, 6, 39, 'M')
    q.elipse(3.5, 1.5, 1.6, 1.4, 'v')
    if ativa:
        q.ret(5, 3, 14, 11, 'r')
        q.ret(5, 10, 14, 11, 'R')
        # quadradinhos concêntricos do logo
        q.ret(8, 5, 11, 8, 'v')
        q.ret(9, 6, 10, 7, 'r')
    else:
        q.ret(5, 26, 12, 32, 'l')
        q.ret(5, 31, 12, 32, 'L')
    return q.contorno().texto()


SPRITES = {
    'capivara': (32, 24, [
        capivara('andar', 0), capivara('andar', 1),
        capivara('comer', 0), capivara('comer', 1),
        capivara('dormir', respira=0), capivara('dormir', respira=1),
    ]),
    'maca': (10, 10, [maca()]),
    'sapatilha': (16, 12, [sapatilha(0), sapatilha(1)]),
    'coracao': (11, 10, [coracao(True), coracao(False)]),
    'bandeira': (16, 40, [bandeira(False), bandeira(True)]),
}


def escrever_js(caminho):
    linhas = [
        '// Objetos da Fase 1 em matriz de texto (arte original e provisória). Gerado por',
        '// ferramentas/arte/gerar_objetos.py; dá para editar à mão (cada caractere é uma cor da PALETA).',
        '// Cada sprite: largura, altura e a lista de quadros (numerados 0, 1, 2... na textura).',
        '',
        'export const PALETA = {',
    ]
    linhas += [f"  '{k}': '{v}'," for k, v in PALETA.items()]
    linhas += ['};', '', 'export const SPRITES = {']
    for nome, (w, h, quadros) in SPRITES.items():
        linhas.append(f'  {nome}: {{')
        linhas.append(f'    largura: {w},')
        linhas.append(f'    altura: {h},')
        linhas.append('    quadros: [')
        for qd in quadros:
            linhas.append('      [')
            linhas += [f"        '{l}'," for l in qd]
            linhas.append('      ],')
        linhas.append('    ],')
        linhas.append('  },')
    linhas.append('};')
    open(caminho, 'w').write('\n'.join(linhas) + '\n')


def previa(caminho, esc=5):
    try:
        from PIL import Image
    except ImportError:
        print('Pillow não instalado: sem prévia')
        return
    larg = sum(w * len(qs) + 4 * len(qs) for w, h, qs in SPRITES.values())
    alt = max(h for _, h, _ in SPRITES.values())
    img = Image.new('RGBA', (larg * esc, alt * esc), (158, 158, 255, 255))
    x0 = 0
    for w, h, qs in SPRITES.values():
        for qd in qs:
            for y, l in enumerate(qd):
                for x, c in enumerate(l):
                    if c == '.':
                        continue
                    rgb = tuple(int(PALETA[c][j:j + 2], 16) for j in (1, 3, 5)) + (255,)
                    for yy in range(esc):
                        for xx in range(esc):
                            img.putpixel(((x0 + x) * esc + xx, (alt - h + y) * esc + yy), rgb)
            x0 += w + 4
    img.save(caminho)


if __name__ == '__main__':
    escrever_js(f'{sys.argv[1]}/src/art/objetos.js')
    previa(f'{sys.argv[2]}/objetos.png')
