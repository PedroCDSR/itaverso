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


def braco(q, ombro, cotovelo, mao, pele, larg=3):
    q.linha(*ombro, *cotovelo, larg, pele)
    q.linha(*cotovelo, *mao, larg, pele)
    q.elipse(mao[0], mao[1], 1.6, 1.6, pele)


def olho(q, x, y, feliz=False):
    if feliz:
        q.px(x - 1, y + 1, 'e'); q.px(x, y, 'e'); q.px(x + 1, y + 1, 'e')
    else:
        q.px(x, y, 'w'); q.px(x, y + 1, 'w')
        q.px(x + 1, y, 'e'); q.px(x + 1, y + 1, 'e')


# ------------------------------------------------------------------ personagens (32x48, olhando para a DIREITA)
# Pé no fundo do quadro (y = 46/47), como o Aladdin. No jogo o NPC vira para o lado do jogador.

def jasmine(q_idx):
    """Bailarina do espetáculo: trança longa preta com fita rosa, tiara dourada, top lilás e calça bufante rosa.
    Quadro 0: braços em coroa (5ª posição), pés juntos. Quadro 1: braços abertos e perna em passé."""
    q = Quadro(32, 48)
    # trança nas costas (atrás de tudo)
    for i in range(9):
        q.elipse(11 - (i % 2) * 0.6, 14 + i * 2.2, 1.9, 1.5, 'e')
    q.ret(10, 33, 12, 34, 'r')  # fita na ponta
    # pernas (calça bufante rosa até o tornozelo, sapatilha rosa)
    if q_idx == 0:
        q.elipse(14, 39, 3.2, 6, 'R')
        q.elipse(18, 39, 3.2, 6, 'r')
        q.ret(13, 44, 14, 45, 'z'); q.ret(17, 44, 18, 45, 'z')
        q.ret(12, 46, 15, 47, 'R'); q.ret(17, 46, 20, 47, 'r')
    else:
        q.elipse(14, 39, 3.2, 6, 'R')
        q.ret(13, 44, 14, 45, 'z')
        q.ret(12, 46, 15, 47, 'R')
        # perna da frente em passé: joelho para a frente, pé encostado no joelho de trás
        q.elipse(19, 35, 4, 2.6, 'r')
        q.linha(22, 36, 16, 39, 4, 'r')
        q.ret(15, 39, 17, 40, 'z')
    # quadril com faixa dourada
    q.ret(11, 31, 21, 33, 'r')
    q.ret(11, 31, 21, 31, 'o')
    # barriga e top lilás
    q.ret(13, 26, 19, 30, 'z')
    q.ret(13, 26, 13, 30, 'Z')
    q.ret(12, 20, 20, 25, 'l')
    q.ret(12, 20, 13, 25, 'L')
    q.ret(14, 25, 19, 25, 'o')
    # braços
    if q_idx == 0:
        braco(q, (13, 21), (9, 13), (14, 6), 'Z', 2)
        braco(q, (19, 21), (23, 13), (18, 6), 'z', 2)
    else:
        braco(q, (13, 21), (7, 22), (3, 20), 'Z', 2)
        braco(q, (19, 21), (25, 22), (29, 20), 'z', 2)
    # cabeça
    cx, cy = 17, 12
    q.elipse(cx - 1, cy - 1, 5.5, 5, 'e')
    q.elipse(cx + 1.5, cy + 1.5, 4, 4.4, 'z')
    q.ret(cx - 1, cy + 3, cx, cy + 5, 'Z')
    q.ret(cx - 4, cy - 5, cx + 3, cy - 4, 'e')  # franja penteada
    q.ret(cx - 2, cy - 6, cx + 2, cy - 6, 'o')  # tiara
    q.px(cx, cy - 7, 'r')
    q.px(cx - 3, cy - 3, 'E')
    olho(q, cx + 2, cy, feliz=(q_idx == 1))
    q.px(cx + 4, cy + 4, 'm')
    q.px(cx + 1, cy + 6, 'Z'); q.px(cx + 2, cy + 6, 'Z')  # pescoço
    q.px(cx - 2, cy + 3, 'o')  # brinco
    return q.contorno().texto()


def genio(q_idx):
    """Gênio do espetáculo: pele lilás, cabeça raspada com rabo de cavalo preto, colete rosa, braceletes de ouro.
    Da cintura para baixo é fumaça amarelo-clara. Quadro 0: braços cruzados. Quadro 1: acenando."""
    q = Quadro(32, 48)
    # fumaça (cauda em espiral)
    voltas = [(16, 34, 6, 3), (14, 38, 5, 2.6), (17, 41, 4, 2.2), (14, 44, 3, 1.8), (16, 46, 2, 1.3)]
    for i, (x, y, rx, ry) in enumerate(voltas):
        dx = (1 if q_idx else -1) * (i % 2)
        q.elipse(x + dx, y, rx, ry, 'v')
        q.elipse(x + dx + 1, y + 1, rx - 1.5, ry - 1, 'V')
    # tronco largo
    q.elipse(16, 26, 8, 7, 'j')
    q.elipse(13, 27, 4, 6, 'J', so_se=lambda x, y: x <= 12)
    # colete rosa aberto
    q.ret(9, 20, 12, 31, 'r'); q.ret(20, 20, 23, 31, 'r')
    q.ret(9, 20, 10, 31, 'R')
    # faixa de ouro na cintura
    q.ret(9, 31, 23, 33, 'o')
    q.ret(9, 33, 23, 33, 'O')
    # braços fortes
    if q_idx == 0:
        q.linha(10, 22, 13, 27, 4, 'J')
        q.linha(22, 22, 19, 27, 4, 'j')
        q.ret(11, 26, 21, 28, 'j')
        q.ret(11, 26, 12, 28, 'o'); q.ret(20, 26, 21, 28, 'o')
    else:
        q.linha(10, 22, 8, 29, 4, 'J')
        q.ret(7, 27, 10, 28, 'o')
        q.linha(22, 22, 27, 16, 4, 'j')
        q.linha(27, 16, 28, 9, 4, 'j')
        q.ret(26, 14, 29, 15, 'o')
        q.elipse(28, 7, 2.2, 2.2, 'j')
    # cabeça
    cx, cy = 17, 12
    q.elipse(cx, cy, 5, 5.5, 'j')
    q.ret(cx - 4, cy + 1, cx - 2, cy + 5, 'J')
    q.ret(cx - 1, cy - 7, cx + 1, cy - 5, 'e')  # coque
    q.linha(cx - 1, cy - 6, cx - 6, cy - 2, 2, 'e')  # rabo de cavalo
    q.px(cx - 4, cy + 1, 'o')  # brinco
    olho(q, cx + 2, cy - 1, feliz=(q_idx == 1))
    q.px(cx + 1, cy - 3, 'e'); q.px(cx + 2, cy - 3, 'e')  # sobrancelha
    # sorrisão e cavanhaque
    q.ret(cx + 1, cy + 3, cx + 4, cy + 3, 'm')
    q.px(cx + 2, cy + 4, 'w'); q.px(cx + 3, cy + 4, 'w')
    q.ret(cx + 1, cy + 5, cx + 2, cy + 6, 'e')
    return q.contorno().texto()


def sultao(q_idx):
    """Sultão do espetáculo: baixinho e redondo, barba branca, turbante enorme rosa com pena e joia verde,
    túnica branca com capa roxa. Quadro 0: mãos separadas. Quadro 1: batendo palmas."""
    q = Quadro(32, 48)
    # capa roxa atrás
    q.ret(8, 22, 13, 45, 'L')
    # pernas curtas e sapatos dourados de bico
    q.ret(13, 41, 15, 44, 'B'); q.ret(18, 41, 20, 44, 'b')
    q.ret(12, 45, 16, 46, 'O'); q.ret(17, 45, 22, 46, 'o')
    q.px(22, 44, 'o')
    # barriga
    q.elipse(17, 33, 8, 8.5, 'b')
    q.elipse(13, 34, 4, 7, 'B', so_se=lambda x, y: x <= 12)
    q.ret(10, 34, 24, 35, 'l')  # faixa lilás
    q.px(17, 35, 'g')
    # braços curtinhos
    if q_idx == 0:
        braco(q, (12, 27), (10, 31), (11, 34), 'Z', 3)
        braco(q, (22, 27), (25, 30), (25, 33), 'z', 3)
    else:
        braco(q, (12, 27), (16, 28), (21, 27), 'Z', 3)
        braco(q, (22, 27), (24, 28), (23, 26), 'z', 3)
    # cabeça redonda com barba
    cx, cy = 17, 19
    q.elipse(cx, cy, 5, 4.5, 'z')
    q.elipse(cx + 1, cy + 5, 5, 3.5, 'b')  # barba
    q.ret(cx - 1, cy + 2, cx + 4, cy + 2, 'b')  # bigode
    q.px(cx + 2, cy + 4, 'm')
    olho(q, cx + 2, cy - 1, feliz=(q_idx == 1))
    q.px(cx - 4, cy + 1, 'Z')
    # turbante grande
    q.elipse(cx, cy - 7, 7.5, 5.5, 'r')
    q.elipse(cx - 2, cy - 6, 4, 3, 'R', so_se=lambda x, y: y >= cy - 5)
    q.ret(cx - 6, cy - 3, cx + 6, cy - 3, 'R')
    q.elipse(cx + 2, cy - 7, 1.6, 1.6, 'g')  # joia
    q.px(cx + 2, cy - 8, 'w')
    # pena
    q.linha(cx + 3, cy - 10, cx + 7, cy - 17, 2, 'v')
    q.px(cx + 7, cy - 17, 'V')
    return q.contorno().texto()


def claudia(q_idx):
    """Tia Claudia (staff do Espaço): cabelo preto na altura do ombro, óculos, camiseta rosa da escola com os
    quadradinhos do logo, calça escura e tênis branco. Quadro 0: parada sorrindo.
    Quadro 1: braço esticado entregando os ingressos."""
    q = Quadro(32, 48)
    # cabelo de trás (até o ombro)
    q.elipse(15, 15, 6, 7.5, 'e')
    # pernas e tênis
    q.ret(13, 33, 15, 44, 'N'); q.ret(17, 33, 19, 44, 'n')
    q.ret(12, 45, 16, 46, 'B'); q.ret(17, 45, 21, 46, 'b')
    # camiseta rosa
    q.ret(11, 21, 21, 33, 'r')
    q.ret(11, 21, 12, 33, 'R')
    # quadradinhos do logo na camiseta
    q.ret(16, 24, 19, 27, 'l')
    q.ret(17, 25, 18, 26, 'v')
    # braços
    braco(q, (12, 22), (11, 27), (12, 31), 'Z', 3)
    q.ret(11, 22, 13, 24, 'R')  # manga
    if q_idx == 0:
        braco(q, (20, 22), (21, 27), (21, 31), 'z', 3)
        q.ret(19, 22, 21, 24, 'r')
    else:
        q.linha(20, 23, 28, 24, 3, 'z')
        q.ret(19, 22, 22, 24, 'r')
        q.elipse(28, 24, 1.6, 1.6, 'z')
        # ingressos na mão
        q.ret(26, 20, 31, 23, 'v')
        q.ret(26, 20, 26, 23, 'L')
    # cabeça
    cx, cy = 17, 13
    q.elipse(cx + 1, cy + 1, 4.3, 4.7, 'z')
    q.ret(cx - 1, cy + 4, cx, cy + 6, 'Z')
    # franja e topo do cabelo
    q.elipse(cx, cy - 3, 5.5, 3, 'e')
    q.ret(cx - 5, cy - 3, cx - 3, cy + 6, 'e')
    q.px(cx - 2, cy - 5, 'E'); q.px(cx - 1, cy - 5, 'E')
    # óculos (armação roxa, lente clara e olho dentro)
    q.ret(cx + 2, cy - 1, cx + 5, cy + 2, 'L')
    q.ret(cx + 3, cy, cx + 4, cy + 1, 'b')
    q.px(cx + 4, cy + 1, 'e')
    q.ret(cx - 1, cy, cx + 1, cy, 'L')  # haste até a orelha
    # sorriso
    q.ret(cx + 3, cy + 4, cx + 4, cy + 4, 'm')
    q.px(cx + 1, cy + 7, 'Z'); q.px(cx + 2, cy + 7, 'Z')
    return q.contorno().texto()


def abu(pose, passo=0):
    """Macaquinho do espetáculo: pelo marrom, colete rosa e chapeuzinho roxo. Pequeno, no pé do quadro."""
    q = Quadro(32, 48)
    base = 46
    pula = 3 if pose == 'feliz' else 0
    yb = base - pula
    # rabo enrolado
    q.linha(9, yb - 6, 5, yb - 12, 2, 'F')
    q.elipse(5, yb - 14, 2, 2, 'F')
    # pernas
    if pose == 'correr':
        if passo == 0:
            q.linha(13, yb - 6, 9, yb, 3, 'F'); q.linha(17, yb - 6, 21, yb, 3, 'f')
        else:
            q.linha(13, yb - 6, 14, yb, 3, 'F'); q.linha(17, yb - 6, 17, yb - 1, 3, 'f')
    else:
        q.linha(13, yb - 6, 12, yb, 3, 'F'); q.linha(17, yb - 6, 18, yb, 3, 'f')
    # corpo + colete
    q.elipse(15, yb - 10, 5, 5.5, 'f')
    q.ret(11, yb - 14, 13, yb - 6, 'r'); q.ret(17, yb - 14, 19, yb - 6, 'r')
    # braços
    if pose == 'feliz':
        q.linha(12, yb - 13, 9, yb - 20, 2, 'F'); q.linha(18, yb - 13, 22, yb - 20, 2, 'f')
    elif pose == 'correr':
        q.linha(18, yb - 12, 23, yb - 9 - passo * 3, 2, 'f')
    else:
        q.linha(18, yb - 12, 20, yb - 7, 2, 'f')
    # cabeça
    cx, cy = 18, yb - 20
    q.elipse(cx, cy, 5, 4.5, 'f')
    q.elipse(cx - 5, cy - 1, 2, 2, 'f')  # orelha
    q.px(cx - 5, cy - 1, 'q')
    q.elipse(cx + 2, cy + 1, 3, 2.8, 'q')  # cara
    olho(q, cx + 2, cy - 1, feliz=(pose == 'feliz'))
    q.px(cx + 4, cy + 2, 'm')
    # chapeuzinho roxo com pompom
    q.ret(cx - 3, cy - 7, cx + 2, cy - 4, 'L')
    q.px(cx, cy - 8, 'r')
    return q.contorno().texto()


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
    'jasmine': (32, 48, [jasmine(0), jasmine(1)]),
    'genio': (32, 48, [genio(0), genio(1)]),
    'sultao': (32, 48, [sultao(0), sultao(1)]),
    'claudia': (32, 48, [claudia(0), claudia(1)]),
    'abu': (32, 48, [abu('parado'), abu('correr', 0), abu('correr', 1), abu('feliz')]),
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
        '// Arte da Fase 2 (Espaço Paula De Marco) em matriz de texto: tiles do estúdio e personagens.',
        '// Arte original e provisória (os figurinos ainda não chegaram). Gerado por ferramentas/arte/gerar_espaco.py;',
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
