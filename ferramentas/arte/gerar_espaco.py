"""Gera a arte provisória (original) da Fase 2, Espaço Paula De Marco, como matrizes de texto.

Tiles do estúdio (piso de madeira, tablado) e personagens: Jasmine, Gênio, Sultão, Tia Claudia e Abu,
além do ingresso e do balãozinho de "tem conversa aqui".
Os figurinos do espetáculo ainda não chegaram (references/figurinos/ só tem capturas de jogo, que valem
só como clima): todos os designs são originais e provisórios, nas cores da escola, e nunca copiam o filme.

Saída: src/art/espaco.js (matrizes) e uma prévia PNG ampliada para conferir.
Uso: python3 ferramentas/arte/gerar_espaco.py <repo> <pasta_previa>
"""
import sys

PALETA = {
    'k': '#2E1A33',  # contorno
    'w': '#FFFFFF',
    'e': '#2A1A1C',  # olho / cabelo preto
    'E': '#4A3540',  # brilho do cabelo
    'm': '#9A4040',  # boca
    # peles
    's': '#D9956A',
    'S': '#B06E46',
    'z': '#F0C29A',  # pele clara
    'Z': '#D29C74',
    'j': '#B4A6F5',  # pele do Gênio (lilás, para não lembrar nenhuma versão conhecida)
    'J': '#8C7CDB',
    # cores da escola
    'r': '#FFB0FA',
    'R': '#D57FCF',
    'l': '#9E9EFF',
    'L': '#6D6BD9',
    'v': '#F9FCBB',
    'V': '#D9D59A',
    'g': '#6CC24A',
    'G': '#47913A',
    # ouro, roupa branca, calça escura, madeira
    'o': '#F2C14E',
    'O': '#C08A2A',
    'b': '#F4F0F8',
    'B': '#CFC6DE',
    'n': '#3B3F66',  # calça escura da Tia Claudia
    'N': '#2A2D4D',
    'c': '#C98B52',  # madeira clara
    'C': '#A86A38',
    'd': '#7E4D25',  # madeira escura
    'D': '#5E3618',
    'f': '#8A5A3A',  # pelo do Abu
    'F': '#6A4028',
    'q': '#E6B98C',  # cara do Abu
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
        for y in range(int(y0), int(y1) + 1):
            for x in range(int(x0), int(x1) + 1):
                self.px(x, y, c)

    def elipse(self, cx, cy, rx, ry, c, so_se=None):
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                    if so_se is None or so_se(x, y):
                        self.px(x, y, c)

    def linha(self, x0, y0, x1, y1, larg, c):
        """Segmento grosso (braços e pernas)."""
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




# ------------------------------------------------------------------ personagens (32x48, olhando para a DIREITA)
# Pé no fundo do quadro (y = 46/47), como o Aladdin. No jogo o NPC vira para o lado do jogador.






def ingresso():
    """Ingresso do espetáculo: papel amarelo-claro com picote e faixa rosa."""
    q = Quadro(16, 10)
    q.ret(1, 1, 14, 8, 'v')
    q.ret(1, 1, 3, 8, 'r')
    for y in (2, 4, 6):
        q.px(4, y, 'V')
    q.ret(6, 3, 12, 3, 'L')
    q.ret(6, 5, 10, 5, 'l')
    q.px(14, 4, '.'); q.px(14, 5, '.')  # picote
    return q.contorno().texto()


def balao(pontos):
    """Balãozinho com "..." em cima de quem ainda tem algo a dizer."""
    q = Quadro(16, 12)
    q.elipse(7.5, 4.5, 6.5, 3.8, 'w')
    q.ret(4, 8, 6, 8, 'w'); q.px(4, 9, 'w')
    for i in range(3):
        q.px(4 + i * 3, 4, 'L' if i < pontos else 'B')
        q.px(5 + i * 3, 4, 'L' if i < pontos else 'B')
    return q.contorno().texto()


# ------------------------------------------------------------------ tiles 16x16 do estúdio
# Mesmos nomes de tiles.js (a ORDEM é a mesma), para o leitor de mapas servir para as duas fases.

def tile_piso_topo():
    """Piso de madeira do estúdio: tábuas compridas com emendas, vistas de frente, e rodapé escuro em cima."""
    linhas = [
        'kkkkkkkkkkkkkkkk',
        'cccccccccccccccc',
        'cccwcccccccccwcc',
        'CCCCCCCCCCCCCCCC',
        'ddddddddddddddDd',
        'cccccccDcccccccc',
        'cccccccDcccccccc',
        'CCCCCCCDCCCCCCCC',
        'dddddddddddddddd',
        'cccDcccccccccccc',
        'cccDcccccccccccc',
        'CCCDCCCCCCCCCCCC',
        'dddddddddddddddd',
        'CCCCCCCCCCCDCCCC',
        'CCCCCCCCCCCDCCCC',
        'DDDDDDDDDDDDDDDD',
    ]
    return linhas


def tile_piso():
    return [
        'dddddddDdddddddd',
        'DDDDDDDDDDDDDDDD',
        'dddDdddddddddddd',
        'dddDdddddddddddd',
        'DDDDDDDDDDDDDDDD',
        'ddddddddddDddddd',
        'ddddddddddDddddd',
        'DDDDDDDDDDDDDDDD',
        'ddddDddddddddddd',
        'ddddDddddddddddd',
        'DDDDDDDDDDDDDDDD',
        'dddddddddddDdddd',
        'dddddddddddDdddd',
        'DDDDDDDDDDDDDDDD',
        'ddddddDddddddddd',
        'DDDDDDDDDDDDDDDD',
    ]


def tile_tablado():
    """Tablado de ensaio (plataforma que se atravessa por baixo): tampo lilás e pés de madeira."""
    return [
        'kkkkkkkkkkkkkkkk',
        'Llllllllllllllll',
        'LlllvlllllllvllL',
        'LLLLLLLLLLLLLLLL',
        'kkkkkkkkkkkkkkkk',
        '..d..........d..',
        '..d..........d..',
        '..d..........d..',
        '..k..........k..',
        '................',
        '................',
        '................',
        '................',
        '................',
        '................',
        '................',
    ]


SPRITES = {
    # Jasmine, Gênio, Sultão, Tia Claudia e Abu: PNG em public/assets/sprites/ (gerar_elenco.py, Etapa 8A)
    'ingresso': (16, 10, [ingresso()]),
    'balao': (16, 12, [balao(1), balao(2), balao(3)]),
}

TILES = {
    'chaoTopo': tile_piso_topo(),
    'chao': tile_piso(),
    'plataforma': tile_tablado(),
}


def escrever_js(caminho):
    linhas = [
        '// Arte da Fase 2 (Espaço Paula De Marco) em matriz de texto: tiles do estúdio, ingresso e balãozinho.',
        '// Os personagens são PNG em public/assets/sprites/ (gerar_elenco.py). Gerado por ferramentas/arte/gerar_espaco.py;',
        '// dá para editar à mão (cada caractere é uma cor da PALETA).',
        '',
        'export const PALETA = {',
    ]
    linhas += [f"  '{k}': '{v}'," for k, v in PALETA.items()]
    linhas += ['};', '', '// Mesmos nomes da ORDEM de tiles.js (o toldo não existe no estúdio).', 'export const TILES = {']
    for nome, qd in TILES.items():
        assert len(qd) == 16 and all(len(l) == 16 for l in qd), nome
        linhas.append(f'  {nome}: [')
        linhas += [f"    '{l}'," for l in qd]
        linhas.append('  ],')
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
    itens = [(w, h, qs) for w, h, qs in SPRITES.values()] + [(16, 16, [t]) for t in TILES.values()]
    larg = sum(w * len(qs) + 4 * len(qs) for w, h, qs in itens)
    alt = max(h for _, h, _ in itens)
    img = Image.new('RGBA', (larg * esc, alt * esc), (243, 217, 240, 255))
    x0 = 0
    for w, h, qs in itens:
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
    escrever_js(f'{sys.argv[1]}/src/art/espaco.js')
    previa(f'{sys.argv[2]}/espaco.png')
