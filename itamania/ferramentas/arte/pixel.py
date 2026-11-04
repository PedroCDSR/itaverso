"""Ferramentas comuns dos geradores de arte: quadro de pixels, formas, contorno, saída em JS e prévia PNG.

Cada quadro é uma grade de caracteres; cada caractere é uma cor da paleta ('.' = transparente).
O contorno escuro ('k') é aplicado no fim, em volta de tudo o que foi pintado.
"""


class Quadro:
    def __init__(self, largura=32, altura=48):
        self.L, self.A = largura, altura
        self.p = [['.'] * largura for _ in range(altura)]

    def px(self, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.L and 0 <= y < self.A:
            self.p[y][x] = c

    def get(self, x, y):
        if 0 <= x < self.L and 0 <= y < self.A:
            return self.p[y][x]
        return '.'

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
        """Segmento grosso (membros). larg=1 desenha uma linha fina."""
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

    def trapezio(self, y0, y1, cx0, meia0, cx1, meia1, c, sombra=None):
        """Faixa horizontal que vai de (centro cx0, meia-largura meia0) no topo a (cx1, meia1) embaixo.
        sombra: pinta a primeira coluna à esquerda com essa cor (lado das costas)."""
        for y in range(y0, y1 + 1):
            t = 0 if y1 == y0 else (y - y0) / (y1 - y0)
            cx = cx0 + (cx1 - cx0) * t
            m = meia0 + (meia1 - meia0) * t
            x0, x1 = int(round(cx - m)), int(round(cx + m))
            self.ret(x0, y, x1, y, c)
            if sombra:
                self.ret(x0, y, x0 + 1, y, sombra)

    def trocar(self, de, para):
        for l in self.p:
            for i, c in enumerate(l):
                if c == de:
                    l[i] = para

    def contorno(self, cor='k'):
        novo = [l[:] for l in self.p]
        for y in range(self.A):
            for x in range(self.L):
                if self.p[y][x] != '.':
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    v = self.get(x + dx, y + dy)
                    if v not in '.k':
                        novo[y][x] = cor
                        break
        self.p = novo

    def texto(self):
        return [''.join(l) for l in self.p]


def escrever_js(caminho, cabecalho, paleta, largura, altura, ordem, quadros, animacoes):
    """Escreve um módulo JS com PALETA, LARGURA, ALTURA, ORDEM, QUADROS e ANIMACOES.
    animacoes: {nome: (lista_de_quadros, quadros_por_segundo, repetir)}; repetir=-1 é sem fim."""
    linhas = [f'// {l}' if l else '//' for l in cabecalho]
    linhas += [
        "// Cada quadro é uma lista de strings; cada caractere é uma cor da PALETA ('.' = transparente).",
        '// Arquivo gerado por ferramentas/arte/. Pode editar à mão, mas rodar o gerador de novo sobrescreve.',
        '',
        'export const PALETA = {',
    ]
    for k, v in paleta.items():
        linhas.append(f"  '{k}': '{v}',")
    linhas += ['};', '', f'export const LARGURA = {largura};', f'export const ALTURA = {altura};', '',
               '// Ordem dos quadros na textura (o índice de cada um é a posição nesta lista).',
               'export const ORDEM = [' + ', '.join(f"'{n}'" for n in ordem) + '];', '',
               '// Animações: quadros, quadros por segundo e repetição (-1 = sem fim, 0 = toca uma vez).',
               'export const ANIMACOES = {']
    for nome, (qs, fps, rep) in animacoes.items():
        linhas.append(f"  {nome}: {{ quadros: [{', '.join(repr(q) for q in qs)}], fps: {fps}, repetir: {rep} }},")
    linhas += ['};', '', 'export const QUADROS = {']
    for nome in ordem:
        linhas.append(f'  {nome}: [')
        for l in quadros[nome]:
            linhas.append(f"    '{l}',")
        linhas.append('  ],')
    linhas.append('};')
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write('\n'.join(linhas) + '\n')


def rgb(cor):
    return tuple(int(cor[j:j + 2], 16) for j in (1, 3, 5))


def imagem(quadros_e_paletas, escala=4, fundo=(158, 158, 255), espaco=2):
    """Monta uma faixa PNG com os quadros lado a lado. quadros_e_paletas: [(linhas, paleta), ...]."""
    from PIL import Image
    alt = max(len(l) for l, _ in quadros_e_paletas)
    larg = sum(len(l[0]) + espaco for l, _ in quadros_e_paletas)
    img = Image.new('RGBA', (larg * escala, alt * escala), fundo + (255,))
    x0 = 0
    for linhas, pal in quadros_e_paletas:
        for y, l in enumerate(linhas):
            for x, c in enumerate(l):
                if c == '.':
                    continue
                cor = rgb(pal[c]) + (255,)
                for yy in range(escala):
                    for xx in range(escala):
                        img.putpixel(((x0 + x) * escala + xx, (alt - len(linhas) + y) * escala + yy), cor)
        x0 += len(linhas[0]) + espaco
    return img
