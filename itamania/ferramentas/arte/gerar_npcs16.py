"""Gera os 8 NPCs adultos no estilo dos heróis desenhados pelo Pedro (heroi_base.py).

Mesmo jeito do herói grande (16x32): cabeça grande, contorno escuro de 1 px, olho com brilho, bochecha rosada,
poucas cores chapadas, sapato com sola. Os NPCs não têm mochila (só o estudante, uma pequena e cinza) nem o boné
amarelo, que é a marca do herói. Todos olham para a direita.

Cada NPC tem 2 quadros: 0 = parado, 1 = falando (antebraço levantado com a mão aberta e boca aberta). O quadro 1
sai do quadro 0 por código (falando()), para a roupa e as cores ficarem idênticas.

Saída (ampliada 2x, fundo transparente):
- public/assets/sprites/npc-<nome>.png   quadros de 32x64, folha de 64x64
- ferramentas/arte/previas/npcs16.png    prancha com os heróis grandes ao lado dos NPCs, mesma escala
Uso: python3 ferramentas/arte/gerar_npcs16.py   (dentro de itamania/)
"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import heroi_base as B  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
L, A = 16, 32
ESCALA = 2

# Paleta do herói + cores novas dos NPCs (as letras do herói acabaram; as novas usam símbolos).
PALETA = dict(B.PALETA)
PALETA.update({
    '1': '#4A4650',  # cabelo grisalho escuro
    '2': '#7D7884',  # brilho do grisalho
    '3': '#8DBBEA',  # camisa azul-clara do uniforme
    '4': '#5E8DC4',  # sombra da camisa do uniforme
    '5': '#2F3A5C',  # azul-marinho (calça, gravata)
    '6': '#E2C38D',  # colete bege
    '7': '#B4955F',  # sombra do colete
    '8': '#9ED0BD',  # camisa verde-água do guia
    '9': '#73AC97',  # sombra da camisa do guia
    '!': '#F1EEF4',  # cabelo branco
    '@': '#C2BCCD',  # sombra do cabelo branco
    '#': '#B98ADB',  # blusa lilás
    '$': '#8E64B9',  # sombra da blusa lilás
    '%': '#5C4A7C',  # saia
    '&': '#7D4FA6',  # armação lilás dos óculos
    '*': '#E2AA82',  # pele média
    '+': '#BE8963',  # sombra da pele média
    '=': '#2C2430',  # cabelo preto
    '-': '#4E4258',  # brilho do cabelo preto
    ';': '#D2D0DC',  # sombra da camiseta branca
    ':': '#4C76B6',  # macacão
    '<': '#365890',  # sombra do macacão
    '>': '#CDD1D8',  # camiseta cinza-clara
    '?': '#8A5634',  # avental marrom
    '/': '#6A3F25',  # sombra do avental marrom
    '(': '#D9443A',  # touca vermelha da lanchonete
    ')': '#A3312C',  # aba da touca
    '[': '#2F2A33',  # camiseta preta da barista
    ']': '#463F4C',  # sombra/brilho da camiseta preta
    '{': '#9C4A2C',  # cabelo ruivo-castanho
    '}': '#C26A3E',  # brilho do cabelo ruivo
    '^': '#52B054',  # camiseta verde
    '~': '#3A8A41',  # sombra da camiseta verde
    '|': '#9A9DA8',  # mochila cinza
    '_': '#6E717E',  # sombra da mochila
    ',': '#5C3A26',  # sapato marrom
    '`': '#3A3A44',  # sapato preto
    "'": '#E8E6EE',  # cadarço/brilho claro
})

# Cada NPC: matriz 16x32 do quadro parado + o que muda no quadro falando.
#   manga: cor do antebraço levantado (manga comprida) ou None (manga curta: antebraço de pele)
#   sombra: cor da parte de cima do braço; pele: cor da mão; boca: pixels da boca aberta (linha, coluna, cor)
NPCS = {}

# Motorista: camisa azul de uniforme com gravata, bigode, cabelo grisalho escuro, sapato preto.
NPCS['motorista'] = dict(manga=None, sombra='4', pele='p', boca=[(11, 10, 'k'), (11, 11, 'm')], m=[
    '................',
    '....kkkkkkk.....',
    '...k1122111kk...',
    '..k1111111111k..',
    '.k111111111111k.',
    '.k1111pp1ppp1pk.',
    '.k11pppppp11ppk.',
    '.k11pqppppewppk.',
    '.k11pqppppeeppk.',
    '..k1ppppprrpppk.',
    '..kpppppp1111pk.',
    '...kkpppppppkk..',
    '..kkkkk3p3kk....',
    '.....k335333k...',
    '.....k335344k...',
    '.....k335344k...',
    '.....k344344k...',
    '.....k335344k...',
    '.....k3353ppk...',
    '.....k3353ppk...',
    '.....k335333k...',
    '.....k333333k...',
    '.....kkkkZkkk...',
    '.....k555555k...',
    '.....k555555k...',
    '.....k555k55k...',
    '.....k555k55k...',
    '.....k555k55k...',
    '.....k555k55k...',
    '....k````k````k.',
    "....k`'``k``'``k",
    '....kkkkkkkkkkkk',
])

# Guia turístico: senhor careca de óculos de armação âmbar, cabelo branco dos lados, colete bege sobre camisa verde-água.
NPCS['guia'] = dict(manga='9', sombra='9', pele='*', boca=[(10, 12, 'k'), (10, 11, 'm')], m=[
    '................',
    '....kkkkkk......',
    '...k******kk....',
    '..k*******'+"'"+'**k..',
    '.k!!**********k.',
    '.k!@!*********k.',
    '.k!@*****NNNN*k.',
    '.k!@*+**NNHwN*k.',
    '.k!@*+***NHHN*k.',
    '..k!*****rr***k.',
    '..k*********m*k.',
    '...kk*******kk..',
    '..kkkkk8*8kk....',
    '.....k668866k...',
    '.....k666699k...',
    '.....k666699k...',
    '.....k677699k...',
    '.....k666699k...',
    '.....k666699k...',
    '.....k6666**k...',
    '.....k666666k...',
    '.....k666666k...',
    '.....kkkkZkkk...',
    '.....kJJJJJJk...',
    '.....kJJJJJJk...',
    '.....kJJJkJJk...',
    '.....kJJJkJJk...',
    '.....kJJJkJJk...',
    '.....kJJJkJJk...',
    '....k,,,,k,,,,k.',
    '....k,Q,,k,,Q,,k',
    '....kooookoooook',
])

# Vovó: coque branco no alto, óculos de armação lilás, blusa lilás, saia roxa, sapatilha.
NPCS['vovo'] = dict(manga='$', sombra='$', pele='p', boca=[(10, 12, 'k'), (10, 11, 'm')], m=[
    '..kkkk..........',
    '.k!!@!k.........',
    '.k!@@!kkkkkk....',
    '..kkk!!!!!!!kk..',
    '.k!!!!!!!!!!!!k.',
    '.k!@!!!pp!ppppk.',
    '.k!@!pppp&&&&pk.',
    '.k!@!qpp&&ew&pk.',
    '.k!@!qppp&ee&pk.',
    '..k@ppppprrpppk.',
    '..kpppppppppmpk.',
    '...kkpppppppkk..',
    '..kkkkk#p#kk....',
    '.....k######k...',
    '.....k####$$k...',
    '.....k####$$k...',
    '.....k####$$k...',
    '.....k####$$k...',
    '.....k####$$k...',
    '.....k####ppk...',
    '.....k######k...',
    '.....k######k...',
    '.....k%%%%%%k...',
    '.....k%%%%%%k...',
    '....k%%%%%%%k...',
    '....k%%%%%%%k...',
    '....k%%%%%%%%k..',
    '....kkkkkkkkkk..',
    '......kpk.kpk...',
    '.....k&&&kk&&&k.',
    '.....k&&&kk&&&&k',
    '.....kkkkkkkkkkk',
])

# Vendedora: rabo de cavalo preto, avental vermelho sobre camiseta branca, calça jeans, tênis.
NPCS['vendedora'] = dict(manga=None, sombra=';', pele='P', boca=[(10, 12, 'k'), (10, 11, 'm')], m=[
    '................',
    '....kkkkkkk.....',
    '...k===--=kk....',
    '..k==========k..',
    '.k============k.',
    'k-kk===PP=PPPPk.',
    'k=k=PPPPPPPPPPk.',
    'k=k=PQPPPPkwPPk.',
    'k=-kPQPPPPkkPPk.',
    '.k=kPPPPPRRPPPk.',
    '.k=kPPPPPPPPmPk.',
    '..kkkPPPPPPPkk..',
    '..kkkkkwPwkk....',
    '.....kwwwwwvk...',
    '.....kwww;;vk...',
    '.....kwww;;vk...',
    '.....kwwwPPvk...',
    '.....kvvvPPvk...',
    '.....kwvvPPvk...',
    '.....kwvvPPvk...',
    '.....kwvvvvvk...',
    '.....kwvvvDvk...',
    '.....kkvvvvvk...',
    '.....kSvvvvvk...',
    '.....kSvvvvvk...',
    '.....kSSkDDDk...',
    '.....kSSSkSSk...',
    '.....kSSSkSSk...',
    '.....kSSSkSSk...',
    '....kwwwwkwwwwk.',
    '....kwvwwkwwvwwk',
    '....kooookoooook',
])

# Técnico da fábrica: macacão azul com bolso e zíper, camiseta cinza por baixo, cabelo curto castanho, bota.
NPCS['tecnico'] = dict(manga='<', sombra='<', pele='*', boca=[(10, 12, 'k'), (10, 11, 'm')], m=[
    '................',
    '....kkkkkkk.....',
    '...khhhiihhkk...',
    '..khhhhhhhhhhk..',
    '.khhhhhhhhhhhhk.',
    '.khhhh**h*****k.',
    '.khh**********k.',
    '.khh*+****Hw**k.',
    '.khh*+****HH**k.',
    '..kh*****rr***k.',
    '..k*********m*k.',
    '...kk*******kk..',
    '..kkkkk>*>kk....',
    '.....k::>>::k...',
    '.....k:::<<:k...',
    '.....k:::<<:k...',
    '.....k<<:<<:k...',
    '.....k<<:<<:k...',
    '.....k:::<<:k...',
    '.....k:::**:k...',
    '.....k::::::k...',
    '.....k<<<<<<k...',
    '.....k::::::k...',
    '.....k::::::k...',
    '.....k::::::k...',
    '.....k:::k::k...',
    '.....k:::k::k...',
    '.....k:::k::k...',
    '.....k<<<k<<k...',
    '....k````k````k.',
    "....k````k```'`k",
    '....kooookoooook',
])

# Atendente da lanchonete: touca vermelha com aba, camiseta laranja, avental marrom, calça escura.
NPCS['atendente'] = dict(manga=None, sombra='N', pele='P', boca=[(10, 12, 'k'), (10, 11, 'm')], m=[
    '................',
    '....kkkkkkk.....',
    '...k(((((((k....',
    '..k((((ww((((k..',
    '.k((((((((((((kk',
    '.k)))))))))))))k',
    '.kHHkPPPPPPPPPk.',
    '.kHHPQPPPPkwPPk.',
    '.kHHPQPPPPkkPPk.',
    '..kHPPPPPRRPPPk.',
    '..kPPPPPPPPPmPk.',
    '...kkPPPPPPPkk..',
    '..kkkkkMPMkk....',
    '.....kMMMMM?k...',
    '.....kMMMNN?k...',
    '.....kMMMNN?k...',
    '.....kMMMPP?k...',
    '.....k???PP?k...',
    '.....kM??PP?k...',
    '.....kM??PP?k...',
    '.....kM?????k...',
    '.....kM???/?k...',
    '.....kk?????k...',
    '.....k5?????k...',
    '.....k5?????k...',
    '.....k55k///k...',
    '.....k555k55k...',
    '.....k555k55k...',
    '.....k555k55k...',
    '....kwwwwkwwwwk.',
    '....kw(wwkww(wwk',
    '....kooookoooook',
])

# Barista: cabelo ruivo-castanho preso em coque baixo, camiseta preta, avental marrom comprido.
NPCS['barista'] = dict(manga=None, sombra=']', pele='p', boca=[(10, 12, 'k'), (10, 11, 'm')], m=[
    '................',
    '....kkkkkkk.....',
    '...k{{}}{{{kk...',
    '..k{{{{{{{{{{k..',
    '.k{{{{{{{{{{{{k.',
    '.k{{{{{pp{ppppk.',
    'kkk{{pppppppppk.',
    'k}{k{qppppewppk.',
    'k{{k{qppppeeppk.',
    '.kkk{pppprrpppk.',
    '..kpppppppppmpk.',
    '...kkpppppppkk..',
    '..kkkkk[p[kk....',
    '.....k[[[[[?k...',
    '.....k[[[]]?k...',
    '.....k[[[]]?k...',
    '.....k[[[pp?k...',
    '.....k???pp?k...',
    '.....k[??pp?k...',
    '.....k[??pp?k...',
    '.....k[?????k...',
    '.....k[???/?k...',
    '.....kk?????k...',
    '.....k[?????k...',
    '.....k[?????k...',
    '.....k[?????k...',
    '.....k[[k///k...',
    '.....k[[[k[[k...',
    '.....k[[[k[[k...',
    '....k,,,,k,,,,k.',
    "....k,Q,,k,,Q,,k",
    '....kooookoooook',
])

# Estudante da UNIFEI: jovem de óculos vermelhos, cabelo castanho bagunçado, camiseta verde, mochila cinza pequena.
NPCS['estudante'] = dict(manga=None, sombra='~', pele='*', boca=[(10, 12, 'k'), (10, 11, 'm')], m=[
    '.....k.kk.......',
    '....kHkJHkk.....',
    '...kHHJHHHHkk...',
    '..kHHHHHJHHHHk..',
    '.kHJHHHHHHHJHHk.',
    '.kHHHH**H**H**k.',
    '.kHH*****vvvv*k.',
    '.kHH*+**vvHwv*k.',
    '.kHH*+***vHHv*k.',
    '..kH*****rr***k.',
    '..k*********m*k.',
    '...kk*******kk..',
    '..kkkkk^*^kk....',
    '..kkkk^^^^^^k...',
    '.k||_k^^^~~^k...',
    '.k|||k^^^~~^k...',
    '.k|_|k^^^**^k...',
    '.k|||k^^^**^k...',
    '..kkkk^^^**^k...',
    '.....k^^^**^k...',
    '.....k^^^^^^k...',
    '.....k^^^^^^k...',
    '.....kkkkZkkk...',
    '.....kSSSSSSk...',
    '.....kSSSSSSk...',
    '.....kSSSkSSk...',
    '.....kSSSkSSk...',
    '.....kSSSkSSk...',
    '.....kSSSkSSk...',
    '....kwwwwkwwwwk.',
    '....kw^wwkww^wwk',
    '....kooookoooook',
])


def falando(m, cfg):
    """Quadro 1: o braço da frente dobra e a mão sobe até o queixo, aberta; a boca abre."""
    q = [list(r) for r in m]
    # descobre a coluna do braço (onde está a mão parada) e a cor do tronco atrás dele
    pele = cfg['pele']
    linha_mao = max(r for r in range(13, 22) if q[r][9] == pele or q[r][10] == pele)
    for r in range(14, linha_mao + 1):
        for c in (9, 10):
            q[r][c] = q[r][8]
    # braço de cima junto do corpo, cotovelo dobrado, antebraço para a frente e mão aberta levantada
    s = cfg['sombra']
    ante = cfg['manga'] or pele
    for r, c, ch in [
        (14, 9, s), (14, 10, s), (15, 9, s), (15, 10, s), (16, 9, s), (16, 10, s), (17, 9, s), (17, 10, ante),
        (15, 11, 'k'), (15, 12, 'k'), (16, 11, ante), (16, 12, ante), (17, 11, ante), (17, 12, ante),
        (18, 9, 'k'), (18, 10, 'k'), (18, 11, 'k'), (18, 12, 'k'),
        (14, 13, pele), (15, 13, pele), (16, 13, pele), (14, 14, pele), (15, 14, pele),
        (13, 13, 'k'), (13, 14, 'k'), (14, 15, 'k'), (15, 15, 'k'), (16, 14, 'k'), (17, 13, 'k'),
    ]:
        q[r][c] = ch
    for r, c, ch in cfg['boca']:
        q[r][c] = ch
    return [''.join(r) for r in q]


def alargar(m):
    """Os troncos foram escritos com 6 px; o herói grande tem 7. Duplica a coluna 11 nas linhas 13 a 28."""
    out = list(m)
    for r in range(13, 29):
        linha = m[r][:12] + m[r][11:]
        assert linha[-1] == '.', (r, m[r])
        out[r] = linha[:L]
    return out


def conferir(nome, m):
    assert len(m) == A, (nome, len(m))
    for i, r in enumerate(m):
        assert len(r) == L, (nome, i, r, len(r))
        for ch in r:
            assert ch == '.' or ch in PALETA, (nome, i, ch)


def imagem(m, escala=ESCALA):
    im = Image.new('RGBA', (len(m[0]) * escala, len(m) * escala), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for y, r in enumerate(m):
        for x, ch in enumerate(r):
            if ch != '.':
                d.rectangle([x * escala, y * escala, x * escala + escala - 1, y * escala + escala - 1], fill=PALETA[ch])
    return im


def main():
    quadros = {}
    for nome, cfg in NPCS.items():
        conferir(nome, cfg['m'])
        cfg['m'] = alargar(cfg['m'])
        f1 = falando(cfg['m'], cfg)
        conferir(nome + ' (falando)', f1)
        quadros[nome] = (cfg['m'], f1)
        folha = Image.new('RGBA', (L * ESCALA * 2, A * ESCALA), (0, 0, 0, 0))
        for i, q in enumerate((cfg['m'], f1)):
            folha.paste(imagem(q), (i * L * ESCALA, 0))
        folha.save(os.path.join(RAIZ, 'public', 'assets', 'sprites', f'npc-{nome}.png'))

    # Prancha: heróis grandes e os 8 NPCs (parado em cima, falando embaixo), mesma escala, ampliada 4x.
    esc = 4
    herois = [B.GERALDO_GRANDE, B.HELENA_GRANDE]
    colunas = len(herois) + len(quadros)
    passo = (L + 4) * esc
    prancha = Image.new('RGBA', (colunas * passo + 4 * esc, (A * 2 + 12) * esc), '#A8DCF5')
    d = ImageDraw.Draw(prancha)
    chao = (A + 4) * esc
    for i, h in enumerate(herois):
        prancha.alpha_composite(imagem(h, esc), (4 * esc + i * passo, 2 * esc))
    for j, (nome, (f0, f1)) in enumerate(quadros.items()):
        x = 4 * esc + (len(herois) + j) * passo
        prancha.alpha_composite(imagem(f0, esc), (x, 2 * esc))
        prancha.alpha_composite(imagem(f1, esc), (x, chao + 4 * esc))
        d.text((x, chao - 2 * esc + 2), nome, fill='#2B1E2E')
    d.line([(0, chao), (prancha.width, chao)], fill='#5DB04A', width=2)
    destino = os.path.join(RAIZ, 'ferramentas', 'arte', 'previas', 'npcs16.png')
    prancha.save(destino)
    print('ok:', ', '.join(quadros), '->', destino)


if __name__ == '__main__':
    main()
