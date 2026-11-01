"""Gera a arte da Fase 4 (Tapete) como matrizes de texto: design ORIGINAL.

- voo (64x48, 3 quadros): tapete mágico com a estampa dos quadrados arredondados concêntricos do logo,
  ondulando, com o Aladdin (provisório, igual ao do jogador) e a Tia Paula (provisória: aparência A DEFINIR).
- passaro (18x14, 2 quadros): sabiá-laranjeira, voando para a esquerda.
- pipa (18x28, 2 quadros): pipa de papel nas cores da escola, com rabiola balançando.
- sapatilha (14x12, 1 quadro): sapatilha de ponta rosa, coletável do céu.

Saída: src/art/tapete.js e uma prévia PNG ampliada.
Uso: python3 ferramentas/arte/gerar_tapete.py <repo> <pasta_previa>
"""
import sys, math

PALETA = {
    'k': '#2E1A33',  # contorno
    # pele, cabelo e roupa do Aladdin (iguais ao jogador)
    's': '#D9956A', 'S': '#B06E46', 'h': '#2A1A1C', 'H': '#4A3030',
    'g': '#6CC24A', 'G': '#47913A', 'c': '#F2DEB0', 'C': '#CDB386',
    'w': '#FFFFFF', 'e': '#2A1A1C', 'm': '#9A4040',
    # cores da escola
    'r': '#FFB0FA', 'R': '#D57FCF', 'l': '#9E9EFF', 'L': '#7C7CE0', 'y': '#F9FCBB', 'Y': '#D9D59A',
    'v': '#6D6BD9', 'V': '#4F4DB0', 'x': '#6CC24A',
    # Tia Paula (provisória)
    'p': '#5A3A2A', 'P': '#3E2619', 'q': '#E8B48A', 'Q': '#C48C64',
    # sabiá
    'b': '#8A6A4A', 'B': '#6A4E36', 'o': '#E8873A', 'O': '#C66A24', 'a': '#F2C14E',
    # varetas da pipa
    'n': '#7A4A2A',
}


class Quadro:
    def __init__(self, larg, alt):
        self.L, self.A = larg, alt
        self.p = [['.'] * larg for _ in range(alt)]

    def px(self, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.L and 0 <= y < self.A:
            self.p[y][x] = c

    def ret(self, x0, y0, x1, y1, c):
        for y in range(int(y0), int(y1) + 1):
            for x in range(int(x0), int(x1) + 1):
                self.px(x, y, c)

    def elipse(self, cx, cy, rx, ry, c):
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                    self.px(x, y, c)

    def linha(self, x0, y0, x1, y1, larg, c):
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
        r = larg / 2
        for i in range(n + 1):
            t = i / n
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            if larg <= 1:
                self.px(x, y, c)
                continue
            for yy in range(int(y - r) - 1, int(y + r) + 2):
                for xx in range(int(x - r) - 1, int(x + r) + 2):
                    if (xx - x) ** 2 + (yy - y) ** 2 <= r * r:
                        self.px(xx, yy, c)

    def colar(self, outro, dx, dy):
        for y in range(outro.A):
            for x in range(outro.L):
                if outro.p[y][x] != '.':
                    self.px(x + dx, y + dy, outro.p[y][x])

    def contorno(self):
        novo = [linha[:] for linha in self.p]
        for y in range(self.A):
            for x in range(self.L):
                if self.p[y][x] != '.':
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < self.L and 0 <= yy < self.A and self.p[yy][xx] not in '.k':
                        novo[y][x] = 'k'
                        break
        self.p = novo

    def texto(self):
        return [''.join(l) for l in self.p]


# ---------- tapete ----------
# Estampa: quadrados arredondados concêntricos (como no logo), em módulos de 8 px de largura.
MODULO = [
    '.rrrrr.',
    'rryyyrr',
    'ryxxxyr',
    'ryxvxyr',
    'ryxxxyr',
    'rryyyrr',
    '.rrrrr.',
]
TAP_X0, TAP_X1, TAP_Y0 = 5, 58, 35  # tapete ocupa x 5..58, y 35..43 (9 linhas: borda + 7 + borda)


def onda(x, fase):
    """Deslocamento vertical do tapete em cada coluna (a ondulação anda da frente para trás)."""
    return int(round(1.3 * math.sin(x / 7.0 + fase)))


def tapete(fase):
    q = Quadro(64, 48)
    for x in range(TAP_X0, TAP_X1 + 1):
        dy = onda(x, fase)
        y0 = TAP_Y0 + dy
        q.px(x, y0, 'v')  # borda de cima
        q.px(x, y0 + 8, 'V')  # borda de baixo
        for i in range(7):
            q.px(x, y0 + 1 + i, 'l')  # fundo lilás
        mx = (x - TAP_X0 - 1) % 8
        if x > TAP_X0 and x < TAP_X1 and mx < 7:
            for i in range(7):
                c = MODULO[i][mx]
                if c != '.':
                    q.px(x, y0 + 1 + i, c)
    # franjas amarelas nas pontas, balançando
    for lado, x0, sentido in (('tras', TAP_X0, -1), ('frente', TAP_X1, 1)):
        dy = onda(x0, fase)
        for i in range(0, 9, 2):
            balanco = int(round(math.sin(fase + i) * 0.8))
            q.px(x0 + sentido, TAP_Y0 + dy + i + balanco, 'y')
            q.px(x0 + 2 * sentido, TAP_Y0 + dy + i + balanco, 'Y')
    return q


# ---------- Aladdin sentado (mesmo visual provisório do jogador) ----------

def aladdin(q, ox, oy):
    cx, cy = 17 + ox, 11 + oy
    # pernas dobradas para a frente (calça areia), pé no tapete
    q.linha(14 + ox, 31 + oy, 23 + ox, 30 + oy, 5, 'C')
    q.linha(23 + ox, 30 + oy, 25 + ox, 34 + oy, 4, 'c')
    q.ret(24 + ox, 34 + oy, 27 + ox, 34 + oy, 's')
    # túnica
    for y in range(19 + oy, 32 + oy):
        q.ret(11 + ox, y, 21 + ox, y, 'g')
        q.ret(11 + ox, y, 12 + ox, y, 'G')
    q.px(19 + ox, 19 + oy, 's'); q.px(19 + ox, 20 + oy, 's'); q.px(18 + ox, 19 + oy, 's')
    q.ret(11 + ox, 27 + oy, 21 + ox, 28 + oy, 'r')
    q.ret(11 + ox, 28 + oy, 21 + ox, 28 + oy, 'R')
    # cabeça
    q.elipse(cx - 1, cy - 1, 6.2, 5.5, 'h')
    for bx, by in ((-6, -2), (-5, 2), (-3, -5), (1, -6), (4, -5)):
        q.elipse(cx + bx, cy + by, 1.8, 1.8, 'h')
    q.elipse(cx + 2, cy + 2, 4.2, 4.6, 's')
    q.ret(cx + 1, cy + 5, cx + 4, cy + 6, 's')
    q.ret(cx - 1, cy + 5, cx, cy + 6, 'S')
    q.px(cx - 1, cy + 2, 'S'); q.px(cx - 1, cy + 3, 'S')
    q.ret(cx - 6, cy - 3, cx + 5, cy - 2, 'r')
    q.ret(cx - 6, cy - 2, cx + 5, cy - 2, 'R')
    # pontas da faixa ao vento (voando: bem esticadas para trás)
    q.linha(cx - 7, cy - 2, cx - 12, cy - 1, 2, 'r')
    q.linha(cx - 7, cy - 1, cx - 11, cy + 1, 2, 'R')
    q.px(cx - 2, cy - 5, 'H'); q.px(cx - 1, cy - 5, 'H')
    q.px(cx + 3, cy + 1, 'w'); q.px(cx + 3, cy + 2, 'w')
    q.px(cx + 4, cy + 1, 'e'); q.px(cx + 4, cy + 2, 'e')
    q.px(cx + 3, cy, 'h'); q.px(cx + 4, cy, 'h')
    q.px(cx + 4, cy + 4, 'm'); q.px(cx + 5, cy + 4, 'm')
    # braço da frente apoiado no joelho
    q.linha(19 + ox, 21 + oy, 22 + ox, 26 + oy, 3, 's')
    q.linha(22 + ox, 26 + oy, 25 + ox, 28 + oy, 3, 's')


# ---------- Tia Paula sentada (PROVISÓRIA: aparência A DEFINIR, ver CLAUDE.md seção 8) ----------

def paula(q, ox, oy):
    cx, cy = 17 + ox, 13 + oy
    # pernas dobradas (meia-calça lilás) e sapatilha rosa
    q.linha(14 + ox, 32 + oy, 22 + ox, 31 + oy, 5, 'L')
    q.linha(22 + ox, 31 + oy, 23 + ox, 34 + oy, 4, 'l')
    q.ret(22 + ox, 34 + oy, 25 + ox, 34 + oy, 'r')
    # vestido roxo com saia rodada
    for y in range(21 + oy, 33 + oy):
        t = (y - 21 - oy) / 11
        meia = 4 + int(round(t * 3))
        q.ret(16 + ox - meia, y, 16 + ox + meia, y, 'v')
        q.ret(16 + ox - meia, y, 16 + ox - meia + 1, y, 'V')
    q.ret(13 + ox, 26 + oy, 20 + ox, 26 + oy, 'y')  # faixa amarela na cintura
    q.px(18 + ox, 21 + oy, 'q'); q.px(19 + ox, 21 + oy, 'q')
    # cabeça: cabelo castanho escuro preso num coque alto (de bailarina)
    q.elipse(cx - 1, cy - 1, 5.5, 5.0, 'p')
    q.elipse(cx - 4, cy - 6, 2.6, 2.4, 'p')  # coque
    q.px(cx - 4, cy - 7, 'P'); q.px(cx - 3, cy - 6, 'P')
    q.elipse(cx + 2, cy + 2, 3.8, 4.2, 'q')
    q.ret(cx + 1, cy + 5, cx + 3, cy + 6, 'q')
    q.ret(cx - 1, cy + 4, cx, cy + 6, 'Q')
    q.px(cx - 1, cy + 2, 'Q')
    q.ret(cx - 5, cy - 2, cx + 1, cy - 1, 'p')  # franja penteada para trás
    q.px(cx + 3, cy + 1, 'w'); q.px(cx + 4, cy + 1, 'e'); q.px(cx + 4, cy + 2, 'e'); q.px(cx + 3, cy + 2, 'w')
    q.px(cx + 3, cy, 'P'); q.px(cx + 4, cy, 'P')
    q.px(cx + 4, cy + 4, 'm'); q.px(cx + 5, cy + 4, 'm')
    q.px(cx - 1, cy + 4, 'y')  # brinco
    q.ret(cx, cy + 7, cx + 1, cy + 8, 'Q')  # pescoço
    # braço esticado para a frente, segurando no ombro do Aladdin
    q.linha(19 + ox, 23 + oy, 24 + ox, 23 + oy, 3, 'q')
    q.linha(24 + ox, 23 + oy, 27 + ox, 21 + oy, 3, 'q')


def voo(fase):
    q = tapete(fase)
    pas = Quadro(64, 48)
    paula(pas, 0, 1)
    ala = Quadro(64, 48)
    aladdin(ala, 19, 0)
    # cada passageiro sobe e desce junto com o pedaço de tapete em que está sentado
    q.colar(pas, 0, onda(17, fase))
    q.colar(ala, 0, onda(37, fase))
    q.contorno()
    return q.texto()


# ---------- sabiá-laranjeira (olha para a ESQUERDA, voando contra o tapete) ----------

def passaro(asa_cima):
    q = Quadro(18, 14)
    q.elipse(9, 8, 5.5, 3.6, 'b')  # corpo
    q.elipse(8, 9.5, 3.8, 2.2, 'o')  # peito laranja
    q.ret(7, 11, 10, 11, 'O')
    q.elipse(4.5, 6.5, 2.8, 2.6, 'b')  # cabeça
    q.ret(0, 7, 2, 7, 'a')  # bico
    q.px(1, 6, 'a')
    q.px(4, 6, 'w'); q.px(3, 6, 'e')
    q.ret(14, 7, 16, 8, 'B')  # cauda
    q.px(17, 7, 'B')
    if asa_cima:
        q.linha(9, 6, 12, 1, 3, 'B')
        q.linha(10, 6, 14, 2, 2, 'b')
    else:
        q.linha(9, 8, 12, 12, 3, 'B')
        q.linha(10, 8, 14, 12, 2, 'b')
    q.contorno()
    return q.texto()


# ---------- pipa (cores da escola) ----------

def pipa(balanco):
    q = Quadro(18, 28)
    cx, topo, meio, base = 9, 1, 7, 16
    for y in range(topo, base + 1):
        if y <= meio:
            meia = int(round((y - topo) / (meio - topo) * 7))
        else:
            meia = int(round((base - y) / (base - meio) * 7))
        for x in range(cx - meia, cx + meia + 1):
            cima = y <= meio
            esq = x < cx
            q.px(x, y, ('r' if esq else 'y') if cima else ('l' if esq else 'x'))
    q.linha(cx, topo, cx, base, 1, 'n')  # vareta
    q.linha(cx - 7, meio, cx + 7, meio, 1, 'n')
    # rabiola: fitinhas que balançam
    for i, y in enumerate(range(18, 28, 3)):
        dx = int(round(math.sin(balanco + i * 1.2) * 1.5))
        q.px(cx + dx, y - 1, 'n')
        q.ret(cx + dx - 1, y, cx + dx + 1, y, 'r' if i % 2 == 0 else 'y')
    q.contorno()
    return q.texto()


# ---------- sapatilha de ponta ----------

def sapatilha():
    """Sapatilha de ponta vista de lado, com as fitas cruzadas soltas."""
    q = Quadro(14, 12)
    q.elipse(7, 8, 5.6, 2.6, 'r')  # corpo
    q.elipse(11, 8.5, 2.2, 2.0, 'r')  # ponta
    q.ret(3, 6, 8, 6, 'R')  # abertura (forro)
    q.ret(4, 7, 7, 7, 'R')
    q.ret(5, 10, 11, 10, 'R')  # sola
    q.linha(4, 6, 2, 1, 1, 'y')  # fitas
    q.linha(7, 6, 9, 1, 1, 'y')
    q.px(1, 2, 'y'); q.px(10, 2, 'y')
    q.contorno()
    return q.texto()


SPRITES = {
    'voo': (64, 48, [voo(f) for f in (0, 2 * math.pi / 3, 4 * math.pi / 3)]),
    'passaro': (18, 14, [passaro(True), passaro(False)]),
    'pipa': (18, 28, [pipa(0), pipa(math.pi)]),
    'sapatilhaCeu': (14, 12, [sapatilha()]),
}


def escrever_js(caminho):
    linhas = [
        '// Arte da Fase 4 (Tapete): design ORIGINAL, gerado por ferramentas/arte/gerar_tapete.py.',
        '// Tapete com a estampa dos quadrados arredondados concêntricos do logo; Aladdin provisório (igual ao jogador);',
        '// Tia Paula PROVISÓRIA (aparência A DEFINIR); sabiá-laranjeira; pipa nas cores da escola; sapatilha.',
        "// Cada caractere é uma cor da PALETA ('.' = transparente). Pode editar à mão.",
        '',
        'export const PALETA = {',
    ]
    for k, v in PALETA.items():
        linhas.append(f"  {k}: '{v}',")
    linhas += ['};', '', '// nome: { largura, altura, quadros: [matriz, matriz, ...] }', 'export const SPRITES = {']
    for nome, (l, a, quadros) in SPRITES.items():
        linhas.append(f'  {nome}: {{')
        linhas.append(f'    largura: {l},')
        linhas.append(f'    altura: {a},')
        linhas.append('    quadros: [')
        for quadro in quadros:
            linhas.append('      [')
            for linha in quadro:
                linhas.append(f"        '{linha}',")
            linhas.append('      ],')
        linhas.append('    ],')
        linhas.append('  },')
    linhas.append('};')
    open(caminho, 'w').write('\n'.join(linhas) + '\n')


def previa(caminho, esc=6):
    try:
        from PIL import Image
    except ImportError:
        print('Pillow não instalado: sem prévia')
        return
    larg = sum((l + 2) * len(q) for l, a, q in SPRITES.values())
    img = Image.new('RGBA', (larg * esc, 48 * esc), (158, 158, 255, 255))
    x0 = 0
    for l, a, quadros in SPRITES.values():
        for quadro in quadros:
            for y, linha in enumerate(quadro):
                for x, c in enumerate(linha):
                    if c == '.':
                        continue
                    rgb = tuple(int(PALETA[c][j:j + 2], 16) for j in (1, 3, 5))
                    for yy in range(esc):
                        for xx in range(esc):
                            img.putpixel(((x0 + x) * esc + xx, y * esc + yy), rgb + (255,))
            x0 += l + 2
    img.save(caminho)


if __name__ == '__main__':
    repo, pasta = sys.argv[1], sys.argv[2]
    escrever_js(f'{repo}/src/art/tapete.js')
    previa(f'{pasta}/tapete.png')
    print('sprites:', ', '.join(f'{n} ({len(q)})' for n, (l, a, q) in SPRITES.items()))
