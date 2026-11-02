"""Gera os tiles 16x16 (chão de paralelepípedo com meio-fio, plataforma de madeira, toldo listrado) como matrizes.
O chão é a rua de paralelepípedo de Itajubá (prévia aprovada pelo Pedro em 01/11/2026).
Uso: python3 ferramentas/arte/gerar_tiles.py <repo> <pasta_previa>
"""
import sys, random

T = 16
PALETA = {
    'k': '#2E1A33',  # contorno
    '1': '#F4CF95',  # pedra clara (topo iluminado)
    '2': '#E0A86A',  # pedra média
    '3': '#C9824B',  # pedra (terracota)
    '4': '#9A5532',  # pedra escura
    '5': '#7C4128',  # rejunte
    'l': '#DDA46A',  # madeira clara
    'w': '#B7793F',  # madeira
    'W': '#7E4D25',  # madeira escura
    'r': '#FFB0FA',  # toldo rosa (escola)
    'R': '#D57FCF',  # toldo rosa sombra
    'v': '#F9FCBB',  # toldo amarelo claro (escola)
    'V': '#D9D59A',  # toldo amarelo sombra
    # rua de paralelepípedo (granito cinza aquecido pelo entardecer) e meio-fio claro
    'm': '#FBF2E0', 'n': '#EADBC0', 'o': '#AE9878', 'p': '#6E5E58',
    'A': '#DCD2D6', 'B': '#B6AAB4', 'C': '#8E8292',   # pedra fria: luz, base, sombra
    'D': '#E2CDBE', 'E': '#BCA294', 'F': '#937A74',   # pedra quente
    'G': '#B8ACB6', 'H': '#968A98', 'I': '#766A7E',   # pedra escura
    'J': '#5E5268',                                   # junta
}


def vazio(c='.'):
    return [[c] * T for _ in range(T)]


def paralelepipedos(m, y0, semente, deslocar=0):
    """Pedras de 7x3 em fiadas desencontradas (juntas de 1 px), cada pedra com luz em cima e sombra embaixo e à
    direita, cantos arredondados e um pontinho de desgaste. As fiadas têm 4 px (16 é múltiplo: emenda sem costura)."""
    rnd = random.Random(semente)
    tons = [('A', 'B', 'C'), ('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'H', 'I')]
    for y in range(T):
        for x in range(T):
            m[y][x] = 'J'
    for fiada in range((T - y0) // 4 + 1):
        ya = y0 + fiada * 4
        desloc = 4 if (fiada + deslocar) % 2 else 0
        for xa in range(-8 + desloc, T, 8):
            luz, base, sombra = rnd.choice(tons)
            for y in range(ya, min(T, ya + 3)):
                for x in range(xa, xa + 7):
                    if not 0 <= x < T:
                        continue
                    if (x == xa and y == ya) or (x == xa + 6 and y == ya + 2):
                        continue
                    if y == ya and x < xa + 6:
                        m[y][x] = luz
                    elif x == xa + 6 or y == ya + 2:
                        m[y][x] = sombra
                    else:
                        m[y][x] = base
            if rnd.random() < 0.4:
                xx = xa + rnd.randint(1, 5)
                if 0 <= xx < T and ya + 1 < T:
                    m[ya + 1][xx] = sombra


def chao_topo():
    m = vazio()
    paralelepipedos(m, 5, semente=3)
    # meio-fio de granito claro no alto (o jogador pisa nele)
    for x in range(T):
        m[0][x] = 'k'
        m[1][x] = 'm'
        m[2][x] = 'n'
        m[3][x] = 'n' if x % 8 else 'o'
        m[4][x] = 'p'
    return m


def chao():
    m = vazio()
    paralelepipedos(m, 1, semente=7, deslocar=1)   # linha 0 = junta (continua a fiada do tile de cima)
    return m


def plataforma():
    m = vazio()
    for x in range(T):
        m[0][x] = 'k'
        m[1][x] = 'l'
        for y in (2, 3, 4):
            m[y][x] = 'w'
        m[5][x] = 'W'
        m[6][x] = 'k'
        if x in (0, 15):
            for y in range(1, 6):
                m[y][x] = 'W'
    # pregos e veio da madeira
    for x in (3, 12):
        m[3][x] = 'W'
    for x in range(5, 10):
        m[2][x] = 'l'
    # suportes embaixo
    for x in (2, 13):
        for y in range(7, 10):
            m[y][x] = 'W'
        m[10][x] = 'k'
    return m


def toldo():
    m = vazio()
    for y in range(0, 11):
        for x in range(T):
            listra = (x // 4) % 2
            m[y][x] = ('r', 'v')[listra]
            if y >= 8:
                m[y][x] = ('R', 'V')[listra]
    for x in range(T):
        m[0][x] = 'k'
        # borda de baixo em ondas (gomos)
        fundo = 11 + (1 if x % 4 in (1, 2) else 0)
        for y in range(11, fundo):
            m[y][x] = ('R', 'V')[(x // 4) % 2]
        m[fundo][x] = 'k'
    return m


TILES = {'chaoTopo': chao_topo(), 'chao': chao(), 'plataforma': plataforma(), 'toldo': toldo()}
ORDEM = ['vazio', 'chaoTopo', 'chao', 'plataforma', 'toldo']


def escrever_js(caminho):
    linhas = [
        '// Tiles 16x16 em matriz de texto (CLAUDE.md, seção 7). Cada caractere é uma cor da PALETA.',
        "// A ORDEM define o número de cada tile no mapa (0 = vazio).",
        '',
        'export const PALETA = {',
    ]
    linhas += [f"  '{k}': '{v}'," for k, v in PALETA.items()]
    linhas += ['};', '', f'export const TAMANHO = {T};', '', 'export const ORDEM = ' + repr(ORDEM) + ';', '', 'export const TILES = {']
    for nome in ORDEM[1:]:
        linhas.append(f'  {nome}: [')
        linhas += [f"    '{''.join(l)}'," for l in TILES[nome]]
        linhas.append('  ],')
    linhas.append('};')
    open(caminho, 'w').write('\n'.join(linhas) + '\n')


def previa(caminho, esc=6):
    try:
        from PIL import Image
    except ImportError:
        print('Pillow não instalado: sem prévia')
        return
    nomes = ORDEM[1:]
    img = Image.new('RGBA', (len(nomes) * (T + 4) * esc, T * 2 * esc), (158, 158, 255, 255))
    for i, n in enumerate(nomes):
        for rep in range(2):
            m = TILES[n] if not (n == 'chaoTopo' and rep == 1) else TILES['chao']
            for y, l in enumerate(m):
                for x, c in enumerate(l):
                    if c == '.':
                        continue
                    rgb = tuple(int(PALETA[c][j:j + 2], 16) for j in (1, 3, 5))
                    for yy in range(esc):
                        for xx in range(esc):
                            img.putpixel(((i * (T + 4) + x) * esc + xx, (rep * T + y) * esc + yy), rgb + (255,))
    img.save(caminho)


if __name__ == '__main__':
    escrever_js(f'{sys.argv[1]}/src/art/tiles.js')
    previa(f'{sys.argv[2]}/tiles.png')
