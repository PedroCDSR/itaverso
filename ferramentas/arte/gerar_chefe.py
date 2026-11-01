"""Gera a arte provisória (original) da Fase 3, Resgate, como matrizes de texto.

Jafar (chefe), projétil mágico, gaiola e Tia Paula.
- Jafar: design ORIGINAL e provisório (mago de capuz roxo, bigodão enrolado, medalhão de lua, varinha de estrela).
  Não segue nenhum filme nem jogo; deve ser redesenhado quando chegarem as fotos do figurino do espetáculo.
- Tia Paula: aparência A DEFINIR (CLAUDE.md, seção 8). Desenho NEUTRO de professora de dança (coque, blusa rosa,
  saia lilás), num sprite separado ('tiaPaula', quadros 32x48) para trocar fácil por PNG ou por um novo gerador.

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
    # Tia Paula
    'h': '#4A2E22',  # cabelo
    'H': '#6B4434',  # cabelo brilho
    'r': '#FFB0FA',  # blusa rosa (cor da escola)
    'R': '#D57FCF',  # blusa sombra
    'v': '#9E9EFF',  # saia lilás
    'V': '#7C7CE0',  # saia sombra
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


def jafar(pose):
    """pose: 'flutuar1', 'flutuar2', 'lancar', 'tonto'."""
    q = Quadro(JW, JH)
    onda = {'flutuar1': 0, 'flutuar2': 1, 'lancar': 0, 'tonto': 1}[pose]
    caido = 2 if pose == 'tonto' else 0  # capuz e corpo um pouco caídos quando tonto

    # cauda de fumaça do manto (flutua, sem pernas)
    cauda = [(12, 38), (28, 38), (26 + onda, 46), (22 - onda, 52), (17 + onda, 54), (19 - onda, 48), (14, 44)]
    q.poligono(cauda, 'P')
    q.poligono([(15, 38), (24, 38), (22 + onda, 45), (19, 49), (16, 43)], 'p')

    # manto (corpo), mais largo embaixo
    q.poligono([(13, 20 + caido), (27, 20 + caido), (31, 40), (9, 40)], 'p')
    q.poligono([(24, 20 + caido), (27, 20 + caido), (31, 40), (26, 40)], 'P')
    # forro magenta aparecendo na abertura do manto e barra lilás
    q.poligono([(18, 26 + caido), (22, 26 + caido), (24, 40), (16, 40)], 'm')
    q.poligono([(21, 28 + caido), (22, 26 + caido), (24, 40), (22, 40)], 'M')
    q.ret(9, 39, 31, 40, 'l')

    # capuz pontudo com a ponta caindo para trás (direita)
    cy = 6 + caido
    q.poligono([(11, cy + 16), (12, cy + 5), (17, cy), (25, cy), (31, cy + 4), (35, cy + 9 + onda),
                (30, cy + 8), (29, cy + 16)], 'p')
    q.poligono([(26, cy + 1), (31, cy + 4), (35, cy + 9 + onda), (30, cy + 8), (28, cy + 6)], 'P')
    # beirada lilás do capuz em volta do rosto
    q.elipse(18, cy + 10, 6.5, 7, 'l')
    # rosto
    q.elipse(18, cy + 10.5, 5, 5.5, 's')
    q.ret(20, cy + 6, 22, cy + 15, 'S')
    q.elipse(17.5, cy + 10.5, 4, 5, 's')
    if pose == 'tonto':
        # olhos em X (tonto)
        for ox in (15, 20):
            q.px(ox - 1, cy + 8, 'e'); q.px(ox + 1, cy + 8, 'e'); q.px(ox, cy + 9, 'e')
            q.px(ox - 1, cy + 10, 'e'); q.px(ox + 1, cy + 10, 'e')
        q.ret(16, cy + 14, 19, cy + 15, 'n')
    else:
        # sobrancelhas bravas e olhos
        q.linha(13, cy + 6, 16, cy + 7, 1, 'e')
        q.linha(19, cy + 7, 22, cy + 6, 1, 'e')
        q.ret(14, cy + 8, 15, cy + 9, 'w'); q.px(14, cy + 9, 'e')
        q.ret(19, cy + 8, 20, cy + 9, 'w'); q.px(19, cy + 9, 'e')
    # nariz e bigodão enrolado (marca do personagem)
    q.ret(17, cy + 10, 17, cy + 11, 'S')
    q.ret(13, cy + 12, 22, cy + 13, 'e')
    q.px(11, cy + 11, 'e'); q.px(12, cy + 12, 'e'); q.px(11, cy + 10, 'e')
    q.px(24, cy + 11, 'e'); q.px(23, cy + 12, 'e'); q.px(24, cy + 10, 'e')
    # cavanhaque pontudo
    q.poligono([(16, cy + 15), (20, cy + 15), (18, cy + 19)], 'e')

    # medalhão de lua dourado no peito
    q.elipse(19, 27 + caido, 3, 3, 'o')
    q.elipse(20, 26 + caido, 2.2, 2.2, 'p')
    q.px(18, 28 + caido, 'y')

    # braços (mangas largas) e varinha
    if pose == 'lancar':
        # os dois braços para cima, varinha erguida
        q.poligono([(12, 24), (16, 22), (10, 10), (7, 12)], 'p')
        q.poligono([(25, 22), (29, 24), (33, 12), (30, 10)], 'p')
        q.elipse(8, 10, 2, 2, 's')
        q.elipse(31, 10, 2, 2, 's')
        q.linha(8, 9, 6, 3, 1.5, 'b')
        estrela(q, 6, 3)
        for (sx, sy) in ((2, 8), (12, 2), (36, 5)):
            q.px(sx, sy, 'y')
    else:
        q.poligono([(12, 23 + caido), (16, 24 + caido), (12, 33), (7, 32)], 'p')
        q.poligono([(12, 29 + caido), (8, 32), (11, 33)], 'm')
        q.elipse(8, 32, 2, 2, 's')
        if pose != 'tonto':
            q.linha(7, 31, 4, 23, 1.5, 'b')
            estrela(q, 4, 22)
        else:
            # varinha caída, pendurada
            q.linha(8, 33, 6, 39, 1.5, 'b')
            q.px(6, 40, 'y')
        q.poligono([(25, 23 + caido), (29, 24 + caido), (31, 33), (27, 33)], 'P')
        q.elipse(29, 33, 2, 2, 'S')
    return q.contorno().texto()


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
def gaiola(aberta):
    q = Quadro(40, 56)
    # gancho em cima
    q.elipse(20, 3, 2.5, 2.5, 'O')
    q.elipse(20, 3, 1, 1, '.')
    q.ret(19, 5, 20, 8, 'O')
    # cúpula
    q.elipse(20, 16, 16, 8, 'o', so_se=lambda x, y: y <= 16)
    q.elipse(20, 16, 14, 6.5, '.', so_se=lambda x, y: y <= 16)
    q.ret(3, 15, 36, 17, 'o')
    q.ret(3, 17, 36, 17, 'O')
    # base
    q.ret(2, 50, 37, 54, 'o')
    q.ret(2, 53, 37, 54, 'O')
    # barras verticais
    for x in range(5, 36, 5):
        porta = 14 <= x <= 25
        if aberta and porta:
            continue
        q.ret(x, 10 if 10 <= x <= 30 else 13, x, 50, 'o')
        q.px(x, 49, 'O')
    # faixa do meio
    if aberta:
        q.ret(3, 33, 12, 34, 'o'); q.ret(27, 33, 36, 34, 'o')
        # porta aberta, girada para a esquerda (vista de lado = estreita)
        q.ret(0, 19, 3, 49, 'O')
        q.ret(1, 20, 2, 48, '.')
        for y in (25, 33, 41):
            q.ret(0, y, 3, y, 'O')
    else:
        q.ret(3, 33, 36, 34, 'o')
        # cadeado
        q.ret(18, 31, 22, 36, 'O')
        q.ret(19, 29, 21, 30, 'O')
        q.px(20, 34, 'k')
    return q.contorno().texto()


# ------------------------------------------------------------------ Tia Paula (32x48, olhando para a ESQUERDA)
def tia_paula(pose):
    """pose: 'presa1', 'presa2' (pedindo ajuda), 'feliz' (braços para cima), 'parada'."""
    q = Quadro(32, 48)
    # saia longa lilás (rodada)
    q.poligono([(11, 28), (21, 28), (25, 44), (7, 44)], 'v')
    q.poligono([(18, 28), (21, 28), (25, 44), (21, 44)], 'V')
    # sapatilhas
    q.ret(10, 45, 14, 46, 'r'); q.ret(18, 45, 22, 46, 'r')
    q.ret(11, 44, 13, 44, 's'); q.ret(19, 44, 21, 44, 's')
    # blusa rosa
    q.poligono([(11, 18), (21, 18), (22, 29), (10, 29)], 'r')
    q.ret(19, 18, 21, 29, 'R')
    # pescoço e cabeça
    q.ret(15, 15, 17, 18, 'S')
    q.elipse(16, 10, 5, 6, 's')
    q.ret(19, 7, 21, 13, 'S')
    q.elipse(15.5, 10, 4.5, 5.5, 's')
    # cabelo preso em coque alto (professora de dança)
    q.elipse(16, 6, 5.5, 3.5, 'h', so_se=lambda x, y: y <= 7)
    q.ret(19, 5, 21, 11, 'h')
    q.elipse(18, 1.8, 3, 2.2, 'h')
    q.px(17, 1, 'H'); q.px(14, 5, 'H')
    # olhos e boca
    q.ret(13, 9, 13, 10, 'e'); q.ret(17, 9, 17, 10, 'e')
    if pose == 'feliz':
        q.ret(13, 13, 17, 13, 'n'); q.px(12, 12, 'n'); q.px(18, 12, 'n')
    elif pose == 'parada':
        q.ret(14, 13, 16, 13, 'n')
    else:
        q.elipse(15, 13.5, 1.2, 1.2, 'n')  # "socorro!"
    # braços
    if pose in ('presa1', 'feliz'):
        q.linha(11, 19, 7, 8, 2.5, 'r'); q.elipse(7, 7, 1.6, 1.6, 's')
        q.linha(21, 19, 25, 8, 2.5, 'R'); q.elipse(25, 7, 1.6, 1.6, 's')
    elif pose == 'presa2':
        q.linha(11, 19, 6, 11, 2.5, 'r'); q.elipse(6, 10, 1.6, 1.6, 's')
        q.linha(21, 19, 24, 27, 2.5, 'R'); q.elipse(24, 28, 1.6, 1.6, 's')
    else:
        q.linha(11, 19, 9, 28, 2.5, 'r'); q.elipse(9, 29, 1.6, 1.6, 's')
        q.linha(21, 19, 23, 28, 2.5, 'R'); q.elipse(23, 29, 1.6, 1.6, 's')
    return q.contorno().texto()


SPRITES = {
    'jafar': (JW, JH, [jafar('flutuar1'), jafar('flutuar2'), jafar('lancar'), jafar('tonto')]),
    'projetil': (12, 12, [projetil(0), projetil(1)]),
    'gaiola': (40, 56, [gaiola(False), gaiola(True)]),
    'tiaPaula': (32, 48, [tia_paula('presa1'), tia_paula('presa2'), tia_paula('feliz'), tia_paula('parada')]),
}


def escrever_js(caminho):
    linhas = [
        '// Arte da Fase 3 (Resgate) em matriz de texto: Jafar, projétil, gaiola e Tia Paula.',
        '// Arte original e provisória. Gerado por ferramentas/arte/gerar_chefe.py; dá para editar à mão.',
        '// Tia Paula: aparência A DEFINIR (CLAUDE.md, seção 8). Para trocar, basta um PNG 32x48 com os mesmos 4 quadros',
        "// em public/assets/sprites/tiaPaula.png (registrado em SPRITES_PNG) ou mudar tia_paula() no gerador.",
        '// Quadros: jafar = flutuar1, flutuar2, lancar, tonto | gaiola = fechada, aberta |',
        '//          tiaPaula = presa1, presa2, feliz, parada | projetil = 2 quadros girando.',
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
