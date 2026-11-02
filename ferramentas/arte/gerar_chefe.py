"""Gera a arte provisória (original) da Fase 3, Resgate, como matrizes de texto.

Jafar (chefe), projétil mágico, gaiola e Tia Paula.
- Jafar: design ORIGINAL e provisório (mago de capuz roxo, bigodão enrolado, medalhão de lua, varinha de estrela).
  Não segue nenhum filme nem jogo; deve ser redesenhado quando chegarem as fotos do figurino do espetáculo.
- Tia Paula: aparência A DEFINIR (CLAUDE.md, seção 8). Desenho NEUTRO de professora de dança (coque, vestido roxo
  com faixa amarela, igual à Tia Paula do tapete), num sprite separado ('tiaPaula', quadros 32x48) para trocar fácil por PNG ou por um novo gerador.

Saída: src/art/chefe.js (matrizes) e uma prévia PNG ampliada para conferir.
Uso: python3 ferramentas/arte/gerar_chefe.py <repo> <pasta_previa>
"""
import sys

PALETA = {
    'k': '#2E1A33',  # contorno
    'w': '#FFFFFF',  # branco / brilho
    'e': '#2A1A1C',  # olho, bigode
    's': '#D9956A',  # pele
    'S': '#B06E46',  # pele sombra
    # Jafar
    'p': '#5A3A8C',  # capuz e manto (roxo escuro)
    'P': '#3B2560',  # manto sombra
    'l': '#9E9EFF',  # acabamento lilás (cor da escola)
    'm': '#C2457F',  # forro magenta
    'M': '#8E2E5E',  # forro sombra
    'o': '#F2C94C',  # dourado (medalhão, gaiola)
    'O': '#B98A2A',  # dourado sombra
    'y': '#F9FCBB',  # amarelo claro (estrela, brilho)
    'b': '#6E4A2A',  # varinha
    # Tia Paula (mesmas cores da Tia Paula do tapete, em gerar_tapete.py)
    'h': '#E8C25A',  # cabelo loiro (Pedro, 01/11/2026)
    'H': '#B88A32',  # cabelo sombra
    'q': '#E8B48A',  # pele
    'Q': '#C48C64',  # pele sombra
    'v': '#6D6BD9',  # vestido roxo (cor da escola)
    'V': '#4F4DB0',  # vestido sombra
    'r': '#FFB0FA',  # sapatilha rosa
    'n': '#9A4040',  # boca
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

    def poligono(self, pts, c):
        """Preenche um polígono (regra par-ímpar, amostrando o centro de cada pixel)."""
        ys = [p[1] for p in pts]
        for y in range(int(min(ys)), int(max(ys)) + 1):
            cy = y + 0.5
            xs = []
            for i in range(len(pts)):
                (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
                if (y0 <= cy < y1) or (y1 <= cy < y0):
                    xs.append(x0 + (cy - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for a, b in zip(xs[::2], xs[1::2]):
                for x in range(int(round(a)), int(round(b))):
                    self.px(x, y, c)

    def linha(self, x0, y0, x1, y1, larg, c):
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
        r = larg / 2
        for i in range(n + 1):
            t = i / n
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            for yy in range(int(y - r) - 1, int(y + r) + 2):
                for xx in range(int(x - r) - 1, int(x + r) + 2):
                    if (xx - x) ** 2 + (yy - y) ** 2 <= r * r:
                        self.px(xx, yy, c)

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


# ------------------------------------------------------------------ Jafar (40x56, olhando para a ESQUERDA)
JW, JH = 40, 56


def estrela(q, cx, cy, c='y', borda='o'):
    q.ret(cx - 1, cy - 3, cx + 1, cy + 3, c)
    q.ret(cx - 3, cy - 1, cx + 3, cy + 1, c)
    q.px(cx, cy, borda)



# ------------------------------------------------------------------ projétil (12x12)
def projetil(fase):
    q = Quadro(12, 12)
    if fase == 0:
        q.poligono([(6, 0), (7.5, 4.5), (12, 6), (7.5, 7.5), (6, 12), (4.5, 7.5), (0, 6), (4.5, 4.5)], 'm')
    else:
        q.poligono([(1.5, 1.5), (6, 4), (10.5, 1.5), (8, 6), (10.5, 10.5), (6, 8), (1.5, 10.5), (4, 6)], 'm')
    q.elipse(6, 6, 2.2, 2.2, 'r')
    q.ret(5, 5, 6, 6, 'y')
    return q.contorno().texto()


# ------------------------------------------------------------------ gaiola (40x56)

# ------------------------------------------------------------------ Tia Paula (32x48, olhando para a ESQUERDA)

SPRITES = {
    # Jafar, gaiola e Tia Paula: PNG em public/assets/sprites/ (gerar_elenco.py, Etapa 8A)
    'projetil': (12, 12, [projetil(0), projetil(1)]),
}


def escrever_js(caminho):
    linhas = [
        '// Arte da Fase 3 (Resgate) em matriz de texto: o projétil do Jafar (estrela girando, 2 quadros).',
        '// Gerado por ferramentas/arte/gerar_chefe.py; dá para editar à mão.',
        '// Jafar, gaiola e Tia Paula são PNG em public/assets/sprites/ (ferramentas/arte/gerar_elenco.py, Etapa 8A).',
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
    escrever_js(f'{sys.argv[1]}/src/art/chefe.js')
    previa(f'{sys.argv[2]}/chefe.png')
