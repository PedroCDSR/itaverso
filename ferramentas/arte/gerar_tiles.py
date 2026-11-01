"""Gera os tiles 16x16 (chão de pedra quente, plataforma de madeira, toldo listrado) como matrizes de texto.
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
}


def vazio(c='.'):
    return [[c] * T for _ in range(T)]


def tijolos(m, y0, linhas_por_fiada=4, semente=1):
    """Fiadas de pedra com rejunte e manchas, deslocadas a cada fiada."""
    rnd = random.Random(semente)
    for y in range(y0, T):
        fiada = (y - y0) // linhas_por_fiada
        borda = (y - y0) % linhas_por_fiada == linhas_por_fiada - 1
        desloc = 0 if fiada % 2 == 0 else 4
        for x in range(T):
            if borda or (x + desloc) % 8 == 7:
                m[y][x] = '5'
            else:
                m[y][x] = '3'
                if (y - y0) % linhas_por_fiada == 0:
                    m[y][x] = '2'  # luz no alto de cada pedra
                if rnd.random() < 0.08:
                    m[y][x] = '4'


def chao_topo():
    m = vazio()
    tijolos(m, 4, semente=3)
    for x in range(T):
        m[0][x] = 'k'
        m[1][x] = '1'
        m[2][x] = '1' if x % 5 else '2'
        m[3][x] = '2'
    return m


def chao():
    m = vazio()
    tijolos(m, 0, semente=7)
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
