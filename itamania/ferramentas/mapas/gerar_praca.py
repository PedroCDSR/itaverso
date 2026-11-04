"""Gera a Praça Theodomiro Santiago (Centro explorável, vista de cima) no formato do Tiled.

Arte: pacote Modern Exteriors 16x16 (LimeZu, comprado pelo Pedro em 04/11/2026; licença em
referencias/licenciados/modern-exteriors-licenca.pdf: pode editar e usar em qualquer projeto, inclusive aberto no
GitHub; não pode revender nem distribuir o pacote; crédito obrigatório a https://limezu.itch.io/).
O pacote completo fica fora do Git (referencias/licenciados/modern-exteriors/, no .gitignore). Este script copia
para public/assets/limezu/ só o que a praça usa.

Disposição: satélite enviado pelo Pedro (04/11/2026). Praça retangular com 4 maciços de árvores, largo no meio com o
espelho d'água retangular e uma área redonda a nordeste dele. Em volta: ruas de asfalto e calçadas. Em cima: Hotel
Centenário e Café do Vadinho; em cima à direita, do outro lado da rua, o Cesar Burg; à esquerda, o Fórum Cível no
alto e o Clube Itajubense embaixo; à direita, o açaí e a arena esportiva.

Saída:
  public/assets/mapas/praca.tmj           mapa (abre e edita no Tiled)
  public/assets/limezu/chao.png           tiles de chão usados (calçada, grama, água, asfalto, faixa)
  public/assets/limezu/objetos/*.png      prédios, árvores, bancos, postes, fonte
  public/assets/limezu/personagens/*.png  quadros 16x32 (linha 0 parado, linha 1 andando; 6 por direção)
  src/data/pracaArte.js                   lista do que o Preload carrega
  ferramentas/arte/previas/praca-mapa.png prévia

Uso (dentro de itamania/):  python3 ferramentas/mapas/gerar_praca.py
"""
import json
import os
import random
import shutil

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACOTE = os.path.join(RAIZ, 'referencias', 'licenciados', 'modern-exteriors')
TEMAS = os.path.join(PACOTE, 'ME_Theme_Sorter_16x16')
AUTO = os.path.join(PACOTE, 'Autotiles_16x16', 'Game_Maker_Studio_Autotiles_Singles_16x16')
SAIDA_ALT = os.environ.get('PRACA_SAIDA')  # pasta para gerar uma proposta sem mexer no jogo
ASSETS = os.path.join(SAIDA_ALT, 'assets') if SAIDA_ALT else os.path.join(RAIZ, 'public', 'assets')
DEST = os.path.join(ASSETS, 'limezu')
T = 16
L, A = 80, 47
random.seed(1913)

import colorsys
from PIL import ImageEnhance


def vivo(im):
    """Cores mais claras e vivas (pedido do Pedro, 05/11/2026: priorizar chão e personagens claros)."""
    rgb, a = im.convert('RGBA').convert('RGB'), im.convert('RGBA').getchannel('A')
    rgb = ImageEnhance.Color(rgb).enhance(1.22)
    rgb = ImageEnhance.Brightness(rgb).enhance(1.08)
    out = rgb.convert('RGBA')
    out.putalpha(a)
    return out


def creme(im):
    """Paredes laranja/marrons/cinzas viram creme-claro; contorno escuro, vidro e colunas brancas ficam."""
    im = im.copy()
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a:
                continue
            h, l, sat = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            vidro = b > r + 20 and b > g
            if not vidro and 0.30 < l < 0.80:
                nl = min(0.95, 0.55 + l * 0.45)
                rr, gg, bb = colorsys.hls_to_rgb(0.11, nl, 0.45)
                px[x, y] = (int(rr * 255), int(gg * 255), int(bb * 255), a)
    return im



# ---------- chão: atlas com só os tiles usados ----------
# Autotiles do pacote no formato do GameMaker (12x4 = 47 bordas + 1 vazio): 19 calçada bege sobre asfalto,
# 5 grama (fundo transparente, vai por cima da calçada), 18 espelho d'água com borda de pedra.
AUTOTILES = {'calcada': 21, 'grama': 5, 'agua': 18}  # 21 = calçada cinza-clara (pedido do Pedro)
ATLAS_COLS = 12
atlas = Image.new('RGBA', (ATLAS_COLS * T, 17 * T), (0, 0, 0, 0))
LINHA = {}
for i, (nome, n) in enumerate(AUTOTILES.items()):
    im = Image.open(os.path.join(AUTO, f'Game_Maker_Studio_Autotiles_Singles_16x16_{n}.png')).convert('RGBA')
    atlas.alpha_composite(im, (0, i * 4 * T))
    LINHA[nome] = i * 4
# asfalto liso: só as variações sem pintura (nenhum pixel claro)
def _liso(f):
    im = Image.open(os.path.join(TEMAS, '2_City_Terrains_Singles_16x16', f)).convert('RGBA')
    return im.size == (T, T) and all(p[3] == 255 and sum(p[:3]) / 3 < 110 for p in im.getdata())


asfaltos = [f for f in sorted(os.listdir(os.path.join(TEMAS, '2_City_Terrains_Singles_16x16'))) if 'Asphalt' in f and _liso(f)][:8]
print('asfaltos lisos:', len(asfaltos))
for c, f in enumerate(asfaltos):
    atlas.alpha_composite(Image.open(os.path.join(TEMAS, '2_City_Terrains_Singles_16x16', f)).convert('RGBA'), (c * T, 12 * T))
# grama cheia (Grass_2, tiles 9 e 10) nas colunas 8 e 9 da linha 12: vai por baixo do miolo dos canteiros
for c, n in ((8, 9), (9, 10)):
    atlas.alpha_composite(Image.open(os.path.join(TEMAS, '1_Terrains_and_Fences_Singles_16x16',
                                                  f'ME_Singles_Terrains_and_Fences_16x16_Grass_2_{n}.png')).convert('RGBA'), (c * T, 12 * T))
# faixas de pedestre: bloco 4x4 da folha de terrenos da cidade (colunas 5 a 8, linhas 4 a 7)
terrenos = Image.open(os.path.join(TEMAS, '2_City_Terrains_16x16.png')).convert('RGBA')
atlas.alpha_composite(terrenos.crop((5 * T, 4 * T, 9 * T, 8 * T)), (0, 13 * T))
os.makedirs(DEST, exist_ok=True)
vivo(atlas).save(os.path.join(DEST, 'chao.png'))
atlas = Image.open(os.path.join(DEST, 'chao.png')).convert('RGBA')


def gid_chao(c, r):
    return 1 + r * ATLAS_COLS + c


# Bordas: cada tile do autotile da calçada tem um jeito único de mostrar os 8 vizinhos. Lemos um ponto perto de
# cada borda e de cada canto (calçada = claro) e guardamos qual tile corresponde a cada combinação. O arranjo é o
# mesmo nos outros autotiles do pacote, então a tabela serve para grama e água também.
PONTOS = {'n': (8, 1), 's': (8, 14), 'o': (1, 8), 'l': (14, 8), 'no': (1, 1), 'ne': (14, 1), 'so': (1, 14), 'se': (14, 14)}
ORDEM = ['n', 's', 'o', 'l', 'no', 'ne', 'so', 'se']
ref = Image.open(os.path.join(AUTO, 'Game_Maker_Studio_Autotiles_Singles_16x16_19.png')).convert('RGBA')
TABELA = {}
for r in range(4):
    for c in range(12):
        if (c, r) == (0, 0):
            continue  # vazio
        sig = tuple(sum(ref.getpixel((c * T + x, r * T + y))[:3]) / 3 > 120 for x, y in (PONTOS[k] for k in ORDEM))
        TABELA.setdefault(sig, (c, r))


def autotile(mascara, nome):
    camada = [[0] * L for _ in range(A)]

    def b(x, y):
        return not (0 <= x < L and 0 <= y < A) or mascara[y][x]

    for y in range(A):
        for x in range(L):
            if not mascara[y][x]:
                continue
            n, s, o, l = b(x, y - 1), b(x, y + 1), b(x - 1, y), b(x + 1, y)
            viz = {'n': n, 's': s, 'o': o, 'l': l,
                   'no': n and o and b(x - 1, y - 1), 'ne': n and l and b(x + 1, y - 1),
                   'so': s and o and b(x - 1, y + 1), 'se': s and l and b(x + 1, y + 1)}
            c, r = TABELA[tuple(viz[k] for k in ORDEM)]
            camada[y][x] = gid_chao(c, LINHA[nome] + r)
    return camada


# ---------- objetos (imagens soltas do pacote) ----------
ARQ = {
    # prédios
    'cafe': None,  # ferramentas/arte/montar_cafe.py
    'hotel': None,  # pecas_praca.hotel_centenario()
    'torre': None,  # pecas_praca.torre_vermelha()
    'forum': None,  # pecas_praca.forum_civel()
    'sob_nw1': None,  # pecas_praca.sobrado()
    'sob_nw2': None,  # pecas_praca.sobrado()
    'sob_nw3': None,  # pecas_praca.sobrado()
    'sob_g5': None,  # pecas_praca.sobrado()
    'sob_ne1': None,  # pecas_praca.sobrado()
    'sob_ne2': None,  # pecas_praca.sobrado()
    'sob_w1': None,  # pecas_praca.sobrado()
    'sob_w2': None,  # pecas_praca.sobrado()
    'sob_w3': None,  # pecas_praca.sobrado()
    'sob_e1': None,  # pecas_praca.sobrado()
    'sob_acai': None,  # pecas_praca.sobrado()
    'sob_e2': None,  # pecas_praca.sobrado()
    'sob_e3': None,  # pecas_praca.sobrado()
    'sob_e4': None,  # pecas_praca.sobrado()
    'sob_s0': None,  # pecas_praca.sobrado()
    'sob_s1': None,  # pecas_praca.sobrado()
    'sob_s2': None,  # pecas_praca.sobrado()
    'sob_s3': None,  # pecas_praca.sobrado()
    'sob_s4': None,  # pecas_praca.sobrado()
    'sob_s5': None,  # pecas_praca.sobrado()
    'sob_s6': None,  # pecas_praca.sobrado()
    'sob_s7': None,  # pecas_praca.sobrado()
    'sob_s8': None,  # pecas_praca.sobrado()
    'sob_s9': None,  # pecas_praca.sobrado()

    'burg': None,  # ferramentas/arte/montar_burg.py
    'concha': None,  # ferramentas/arte/pecas_praca.py
    'sob_wm1': None,  # pecas_praca.sobrado()
    'sob_wm2': None,  # pecas_praca.sobrado()
    'sob_wm3': None,  # pecas_praca.sobrado()
    'sob_em1': None,  # pecas_praca.sobrado()
    'sob_em2': None,  # pecas_praca.sobrado()
    'sob_em3': None,  # pecas_praca.sobrado()
    'fivestars': None,  # pecas_praca.five_stars()
    'jato': None,  # pecas_praca.jato()
    'jatos': None,  # pecas_praca.jatos_espelho()
    'arvore_alta1': None,  # pecas_praca.arvore_alta()
    'arvore_alta2': None,
    'palmeira_imp1': None,  # pecas_praca.palmeira_imperial()
    'palmeira_imp2': None,
    'clube': None,  # pecas_praca.clube() (girado 45°)
    'busto': None,  # pecas_praca.busto() (pedestal girado 45°)
    'palmeira1': '14_Swimming_Pool_Singles_16x16/ME_Singles_Swimming_Pool_16x16_Palm_1.png',
    'palmeira2': '14_Swimming_Pool_Singles_16x16/ME_Singles_Swimming_Pool_16x16_Palm_2.png',
    'palmeira3': '21_Beach_Singles_16x16/ME_Singles_Beach_16x16_Palm_Tree.png',
    # praça
    'arvore_grande': '7_Villas_Singles_16x16/ME_Singles_Villas_16x16_Tree_4.png',
    'arvore_media': '7_Villas_Singles_16x16/ME_Singles_Villas_16x16_Tree_3.png',
    'arvore_rua': '3_City_Props_Singles_16x16/ME_Singles_City_Props_16x16_Tree_12.png',
    'banco_h': '3_City_Props_Singles_16x16/ME_Singles_City_Props_16x16_Bench_2.png',
    'banco_v': '3_City_Props_Singles_16x16/ME_Singles_City_Props_16x16_Bench_4.png',
    'poste': '3_City_Props_Singles_16x16/ME_Singles_City_Props_16x16_Street_Lamp_1.png',
    'lixeira': '3_City_Props_Singles_16x16/ME_Singles_City_Props_16x16_Trashbin_1.png',
    'placa': '3_City_Props_Singles_16x16/ME_Singles_City_Props_16x16_Info_Sign_1.png',
    'flores': '3_City_Props_Singles_16x16/ME_Singles_City_Props_16x16_Flower_Bush_1.png',
}


def achar(rel):
    p = os.path.join(TEMAS, rel)
    if os.path.exists(p):
        return p
    # alguns nomes do pacote variam; procura pelo final do nome dentro da pasta
    pasta, nome = os.path.split(p)
    fim = nome.split('16x16_')[-1]
    for f in os.listdir(pasta):
        if f.endswith(fim):
            return os.path.join(pasta, f)
    raise FileNotFoundError(rel)


MOD = os.path.join(TEMAS, '5_Floor_Modular_Building_Singles_16x16', 'ME_Singles_Floor_Modular_Building_16x16_')
COMPLETO = os.path.join(PACOTE, 'Modern_Exteriors_Complete_Singles_16x16')


def montar_clube():
    """Club Itajubense: prédio claro com colunas (fotos do Pedro, 05/11/2026). Telhado plano, andar de cima com
    janelas altas e térreo com a colunata do palácio do pacote, tudo repintado de creme-claro."""
    abre = lambda f: Image.open(f).convert('RGBA')
    W = 224
    teto = abre(MOD + 'Roof_10.png')
    telhado = Image.new('RGBA', (W, teto.height), (0, 0, 0, 0))
    telhado.alpha_composite(teto.crop((0, 0, 40, teto.height)), (0, 0))
    for x in range(40, W - 40, 32):
        telhado.alpha_composite(teto.crop((40, 0, 72, teto.height)), (x, 0))
    telhado.alpha_composite(teto.crop((72, 0, 112, teto.height)), (W - 40, 0))
    telhado = telhado.crop((0, teto.height - 22, W, teto.height))  # só a beirada (platibanda): o prédio não fica fundo demais
    andar = Image.new('RGBA', (W, 48), (0, 0, 0, 0))
    for x in (0, 112):
        andar.alpha_composite(creme(abre(MOD + 'Middle_Floor_15.png')), (x, 0))
    lado = creme(abre(os.path.join(COMPLETO, 'ME_Singles_Garden_16x16_Palace_1_Entrance_Variant_1.png')))
    meio = creme(abre(os.path.join(COMPLETO, 'ME_Singles_Garden_16x16_Palace_1_Entrance_Variant_2.png')))
    terreo = Image.new('RGBA', (W, 64), (0, 0, 0, 0))
    terreo.alpha_composite(lado.crop((0, 0, 56, 64)), (0, 0))
    terreo.alpha_composite(meio, (56, 0))
    terreo.alpha_composite(lado.crop((56, 0, 112, 64)), (168, 0))
    img = Image.new('RGBA', (W, telhado.height + 48 + 64), (0, 0, 0, 0))
    img.alpha_composite(telhado, (0, 0))
    img.alpha_composite(andar, (0, telhado.height))
    img.alpha_composite(terreo, (0, telhado.height + 48))
    return img


def montar_busto():
    """Busto de Theodomiro Santiago (arte própria do projeto, public/assets/cenario/fonte.png) num pedestal alto,
    para ficar no meio do espelho d'água, como na foto do Pedro."""
    f = Image.open(os.path.join(RAIZ, 'public', 'assets', 'cenario', 'fonte.png')).convert('RGBA')
    topo = f.crop((58, 0, 115, 70))
    img = Image.new('RGBA', (57, 86), (0, 0, 0, 0))
    img.alpha_composite(topo, (0, 0))
    # estica o pedestal para baixo com a cor lisa da pedra (sem repetir a placa)
    base = f.crop((58, 69, 115, 70)).load()
    pedra = f.getpixel((64, 60))
    for y in range(70, 86):
        for x in range(57):
            p = base[x, 0]
            if p[3] == 0:
                continue
            escuro = sum(p[:3]) < 200
            img.putpixel((x, y), p if (escuro and (x < 8 or x > 48)) else (pedra if 7 < x < 50 else p))
    return img


os.makedirs(os.path.join(DEST, 'objetos'), exist_ok=True)
TAM = {}
import sys as _sys
_sys.path.insert(0, os.path.join(RAIZ, 'ferramentas', 'arte'))
import pecas_praca  # noqa: E402
import montar_burg  # noqa: E402
import montar_cafe  # noqa: E402

MONTADOS = {'clube': pecas_praca.clube, 'busto': pecas_praca.busto_pequeno,
            'jatos': lambda: pecas_praca.jatos_espelho(112, 48),
            'arvore_alta1': lambda: pecas_praca.arvore_alta(1), 'arvore_alta2': lambda: pecas_praca.arvore_alta(2, 40),
            'palmeira_imp1': lambda: pecas_praca.palmeira_imperial(176), 'palmeira_imp2': lambda: pecas_praca.palmeira_imperial(196), 'fivestars': pecas_praca.five_stars,
            'jato': pecas_praca.jato, 'concha': pecas_praca.concha90,
            'cafe': montar_cafe.gerar, 'burg': montar_burg.gerar, 'forum': pecas_praca.forum_civel,
            'hotel': pecas_praca.hotel_centenario, 'torre': pecas_praca.torre_vermelha}
# sobrados ecléticos (chave, semente, cor, andares, toldo): enchem as quadras no estilo do centro
SOBRADOS = [('sob_nw1', 1, 'creme', 2, True), ('sob_nw2', 2, 'rosa', 1, True), ('sob_nw3', 3, 'amarelo', 2, True), ('sob_g5', 4, 'branco', 2, True), ('sob_ne1', 5, 'azul', 2, True), ('sob_ne2', 6, 'creme', 3, False), ('sob_w1', 7, 'verde', 1, True), ('sob_w2', 8, 'pessego', 1, True), ('sob_w3', 9, 'amarelo', 2, True), ('sob_e1', 10, 'rosa', 1, True), ('sob_acai', 11, 'pessego', 1, True), ('sob_e2', 12, 'creme', 2, True), ('sob_e3', 13, 'azul', 1, True), ('sob_e4', 14, 'amarelo', 2, False), ('sob_s0', 20, None, 0, True), ('sob_s1', 21, None, 0, True), ('sob_s2', 22, None, 0, True), ('sob_s3', 23, None, 0, True), ('sob_s4', 24, None, 0, True), ('sob_s5', 25, None, 0, True), ('sob_s6', 26, None, 0, True), ('sob_s7', 27, None, 0, True), ('sob_s8', 28, None, 0, True), ('sob_s9', 29, None, 0, True), ('sob_wm1', 31, 'azul', 1, False), ('sob_wm2', 32, 'rosa', 1, False), ('sob_wm3', 33, 'creme', 1, False), ('sob_em1', 34, 'verde', 1, False), ('sob_em2', 35, 'amarelo', 1, False), ('sob_em3', 36, 'pessego', 1, False)]
for _k, _sem, _cor, _n, _t in SOBRADOS:
    MONTADOS[_k] = (lambda sem=_sem, cor=_cor, n=_n, t=_t: pecas_praca.sobrado(sem, cor, n, t))
for chave, rel in ARQ.items():
    destino = os.path.join(DEST, 'objetos', chave + '.png')
    im = MONTADOS[chave]() if chave in MONTADOS else Image.open(achar(rel)).convert('RGBA')
    vivo(im).save(destino)
    TAM[chave] = im.size

# como cada tipo de objeto bate: retângulo (x, y, largura, altura) a partir do canto de baixo à esquerda, em px
def caixa(chave):
    w, h = TAM[chave]
    if chave.startswith('palmeira'):
        return (w // 2 - 5, -10, 10, 8)  # só a base do tronco
    if chave == 'busto':
        return (2, -14, w - 4, 12)
    if chave in ('jato', 'jatos'):
        return (0, 0, 0, 0)  # fica dentro da água (a água já bate)
    if chave == 'fivestars':
        return (0, -h, w, h - 16)
    if chave == 'concha':
        return (8, -40, w - 16, 38)
    if chave in ('cafe',):
        return (0, -h, w, h - 22)  # as mesinhas da calçada não bloqueiam
    if chave == 'clube':
        return (0, -h + 52, w, h - 52)  # prédio inteiro menos o telhado
    if chave.startswith('arvore'):
        return (w // 2 - 7, -12, 14, 10)  # só o tronco
    if chave == 'fonte_redonda':
        return (4, -h + 10, w - 8, h - 12)
    if chave in ('banco_h', 'banco_v', 'lixeira', 'flores', 'placa'):
        return (0, -min(h, 12), w, min(h, 12))
    if chave == 'poste':
        return (w // 2 - 3, -6, 6, 6)
    return (0, -h, w, h)  # prédios: tudo


# ---------- desenho ----------
asfalto = [[True] * L for _ in range(A)]
calcada = [[False] * L for _ in range(A)]
grama = [[False] * L for _ in range(A)]
agua = [[False] * L for _ in range(A)]
faixas = [[0] * L for _ in range(A)]
objetos = []
pontos = []


def ret(m, x0, y0, x1, y1, v=True):
    for y in range(max(0, y0), min(A, y1 + 1)):
        for x in range(max(0, x0), min(L, x1 + 1)):
            m[y][x] = v


def obj(chave, x, y, **props):
    """x, y em tiles: canto de baixo à esquerda do objeto."""
    objetos.append(dict(chave=chave, x=x * T, y=y * T, props=props))


def ponto(tipo, x, y, **props):
    pontos.append(dict(tipo=tipo, x=x * T, y=y * T, props=props))


# Ruas pela marcação do Pedro no satélite (05/11/2026): vermelho = asfalto, amarelo = calçadão (mesmo piso da praça).
# Escala: ~18 px do satélite por tile. Praça: colunas 29 a 54, linhas 15 a 37.
ret(calcada, 0, 0, L - 1, A - 1)
VERMELHO = [
    (0, 12, 46, 14),  # rua de cima, do lado oeste, até a esquina da R. Cel. Renno
    (26, 0, 28, 11), (44, 0, 46, 11),  # as duas ruas que sobem
    (0, 0, 2, A - 1),  # avenida da esquerda (Av. Cesário Alvim)
    (0, 38, L - 1, 40),  # rua de baixo (R. Dr. Américo de Oliveira)
    (26, 41, 28, A - 1), (44, 41, 46, A - 1),  # as duas ruas que descem
]
for r in VERMELHO:
    ret(calcada, *r, False)

FX = 13  # faixas de pedestre (barras deitadas = atravessar rua horizontal; em pé = rua vertical)
for x0 in (33, 49):
    for dy, y in enumerate(range(38, 41)):
        for dx in range(2):
            faixas[y][x0 + dx] = gid_chao(2 + dx, FX + (dy % 2))
for x0 in (36,):
    for dy, y in enumerate(range(12, 15)):
        for dx in range(2):
            faixas[y][x0 + dx] = gid_chao(2 + dx, FX + (dy % 2))
for y0 in (20, 31):
    for x in range(0, 3):
        for dy in range(2):
            faixas[y0 + dy][x] = gid_chao(2 + (x % 2), FX + 2 + dy)

# praça simétrica: eixo na coluna 41,5. Quatro canteiros iguais nos cantos, espelho d'água no meio com o busto,
# concha acústica ao norte (girada 45°).
EIXO = 41.5
CANTEIROS = [(31, 17, 37, 22), (46, 17, 52, 22), (31, 31, 37, 35), (46, 31, 52, 35)]  # 2 tiles de calçada até a borda
for m in CANTEIROS:
    ret(grama, *m)
# concha acústica e fonte na faixa oeste da praça, entre os canteiros da esquerda (marcação do Pedro): a concha em
# cima e o espelho d'água com jatos embaixo; o busto fica no meio da borda leste do espelho, de perfil, olhando para
# o leste.
ret(agua, 31, 27, 37, 29)  # espelho comprido (7 x 3)
obj('concha', 31.4, 26.4, nome='Concha acústica', fala='concha')
obj('jatos', 31, 30.0)  # arcos das bordas e jatinhos no meio
obj('busto', 36.5 - TAM['busto'][0] / 32, 28.9, nome='Busto de Theodomiro Santiago', fala='placa')  # dentro da água

# árvores: uma grande no meio de cada canteiro e palmeiras nas quinas de fora (espelhadas)
for (x0, y0, x1, y1), lado in zip(CANTEIROS, ('o', 'l', 'o', 'l')):
    cx = (x0 + x1 + 1) / 2
    obj('arvore_alta1' if lado == 'o' else 'arvore_alta2', cx - 2.1, y1 + 0.2)
    canto = x0 - 2.2 if lado == 'o' else x1 - 0.8  # na beira de fora (o tronco não passa na frente da fonte)
    obj('palmeira_imp1', canto, y0 + 1.6)
    obj('palmeira_imp2', canto, y1 + 0.9)

# bancos, postes e flores, tudo espelhado no eixo
for x in (39.4, 42.6):  # bancos em volta do largo central
    obj('banco_h', x, 25.4)
    obj('banco_h', x, 31.4)
obj('banco_v', 38.2, 29.4)
obj('banco_v', 46.0, 29.4)
for x, y in [(29.2, 15.8), (53.8, 15.8), (29.2, 37.8), (53.8, 37.8), (37.2, 24.4), (45.8, 24.4), (37.2, 33.8), (45.8, 33.8)]:
    obj('poste', x, y)
for x in (38.2, 44.0):
    obj('flores', x, 24.2)
obj('placa', 37.4, 31.4, nome='Placa da praça', fala='placa')

# prédios: todas as quadras cheias, no estilo do centro (sobrados ecléticos claros com comércio embaixo)
# quadra de cima, oeste
obj('sob_nw1', 3, 11.6)
obj('sob_nw2', 10, 11.6)
obj('sob_nw3', 17, 11.6)
# quadra do Subway: a torre vermelha com lojas embaixo e o prédio do G5 na esquina
obj('torre', 29, 11.6, nome='Lojas', fala='torre')
obj('sob_g5', 36, 11.6, nome='G5', fala='g5')
# quadra de cima, leste: Hotel Centenário na esquina, Café do Vadinho, Cesar Burg e mais sobrados
obj('cafe', 47, 13.0, nome='{cafe}', fala='cafe')
obj('hotel', 54.4, 11.6, nome='Hotel Centenário', fala='hotel')
obj('burg', 61.6, 11.6, nome='{lanchonete}', fala='burg')
obj('sob_ne1', 68.8, 11.6)
obj('sob_ne2', 75.8, 11.6)
# quadra da esquerda: sobrados, o Fórum na esquina de cima e o Club Itajubense na de baixo (girado 90°)
obj('sob_w1', 3, 23.0)
obj('sob_w2', 10, 23.0)
obj('forum', 18.6, 23.0, nome='Fórum Cível', fala='forum')
obj('sob_w3', 3, 37.6)
obj('sob_wm1', 3, 30.6)
obj('sob_wm2', 10, 30.6)
obj('sob_wm3', 18.4, 30.4)
obj('clube', 11.0, 37.6, nome='Club Itajubense', fala='clube')
# quadras da direita
obj('sob_e1', 58, 23.0)
obj('sob_acai', 65, 23.0, nome='Açaí', fala='acai')
obj('fivestars', 58, 37.8, nome='Five Stars', fala='arena')
obj('sob_e2', 65, 37.6)
obj('sob_e3', 74, 23.0)
obj('sob_em1', 58, 30.6)
obj('sob_em2', 65, 30.6)
obj('sob_em3', 74, 30.6)
obj('sob_e4', 74, 37.6)
# quarteirões de baixo (sobrados térreos)
for i, x in enumerate((3, 10, 17, 29, 36, 47, 54, 61, 68, 75)):
    obj(f'sob_s{i}', x, 46.9)

# calçada de baixo: árvores de rua

# pontos: início, moradores, itacoins, saída (pela rua que desce à direita)
ponto('inicio', EIXO, 37.4)
ponto('saida', 45.5, A - 0.2)
ponto('npc', 36.0, 31.0, sprite='postman3', nome='Guia da praça', fala='guia')
ponto('npc', 39.4, 25.3, sprite='scout4', nome='Dona Cida', fala='vovo')
ponto('npc', 50.4, 13.9, sprite='postman2', nome='Barista', fala='barista')
ponto('npc', 65.4, 13.8, sprite='scout5', nome='Atendente', fala='atendente')
ponto('npc', 27.5, 26.0, sprite='scout3', nome='Estudante', fala='estudante', anda=1)
ponto('npc', 47.5, 26.5, sprite='postman1', nome='Carteiro', fala='carteiro')
for x, y in [(30, 15.6), (53, 15.6), (30, 37.6), (53, 37.6), (EIXO, 34.5), (EIXO, 21), (34, 28), (49, 28),
             (27.5, 18), (27.5, 34), (56, 18), (56, 34), (10, 13.5), (70, 13.5)]:
    ponto('itacoin', x, y)

# ---------- colisão (camada de tiles invisível) ----------
bate = [[False] * L for _ in range(A)]
for y in range(A):
    for x in range(L):
        if agua[y][x]:
            bate[y][x] = True
for o in objetos:
    cx, cy, cw, ch = caixa(o['chave'])
    x0, y0 = o['x'] + cx, o['y'] + cy
    for ty in range(int(y0 // T), int((y0 + ch - 1) // T) + 1):
        for tx in range(int(x0 // T), int((x0 + cw - 1) // T) + 1):
            if 0 <= tx < L and 0 <= ty < A:
                bate[ty][tx] = True
for y in range(A):  # bordas do mapa (menos a saída)
    bate[y][0] = bate[y][L - 1] = True
for x in range(L):
    bate[0][x] = True
    if not (44 <= x <= 46):
        bate[A - 1][x] = True

# ---------- personagens ----------
CHAR = os.path.join(PACOTE, 'Character_Generator_Addons_16x16', 'Characters_16x16')
PERSONAGENS = {
    'scout6': 'Scout_16x16_6', 'scout2': 'Scout_16x16_2',  # Geraldo e Helena (provisório)
    'scout1': 'Scout_16x16_1', 'scout3': 'Scout_16x16_3', 'scout4': 'Scout_16x16_4', 'scout5': 'Scout_16x16_5',
    'postman1': 'Postman_16x16_1', 'postman2': 'Postman_16x16_2', 'postman3': 'Postman_16x16_3',
}
os.makedirs(os.path.join(DEST, 'personagens'), exist_ok=True)
for chave, nome in PERSONAGENS.items():
    im = Image.open(os.path.join(CHAR, f'Modern_Exteriors_Characters_{nome}.png')).convert('RGBA')
    # linha 1 (y 32) = parado, linha 2 (y 64) = andando; 24 quadros de 16x32 (direita, cima, esquerda, baixo)
    im.crop((0, 32, 24 * 16, 96)).save(os.path.join(DEST, 'personagens', chave + '.png'))

# ---------- .tmj ----------
camadas_chao = {
    'asfalto': [[gid_chao(random.choice([0, 0, 0, 0, 1, 2, 3]) % max(1, len(asfaltos)), 12) for _ in range(L)] for _ in range(A)],
    'calcada': autotile(calcada, 'calcada'),
    'grama_cheia': [[gid_chao(random.choice((8, 9)), 12) if all(0 <= y + dy < A and 0 <= x + dx < L and grama[y + dy][x + dx]
                                                              for dy in (-1, 0, 1) for dx in (-1, 0, 1)) else 0
                     for x in range(L)] for y in range(A)],
    'grama': autotile(grama, 'grama'),
    'agua': autotile(agua, 'agua'),
    'faixas': faixas,
}
n_chao = ATLAS_COLS * (atlas.height // T)
GID_OBJ = 1 + n_chao
chaves = list(ARQ)
GID_BATE = gid_chao(1, LINHA['agua'])  # qualquer tile; a camada fica invisível
lid = 0


def camada(nome, dados, visivel=True):
    global lid
    lid += 1
    return {'id': lid, 'name': nome, 'type': 'tilelayer', 'x': 0, 'y': 0, 'width': L, 'height': A, 'opacity': 1,
            'visible': visivel, 'data': [v for linha in dados for v in linha]}


def props(d):
    return [{'name': k, 'type': 'int' if isinstance(v, int) else 'string', 'value': v} for k, v in d.items()]


layers = [camada(n, d) for n, d in camadas_chao.items()]
layers.append(camada('colisao', [[GID_BATE if bate[y][x] else 0 for x in range(L)] for y in range(A)], False))
oid = 0
objs = []
for o in objetos:
    oid += 1
    w, h = TAM[o['chave']]
    objs.append({'id': oid, 'name': o['props'].get('nome', o['chave']), 'type': o['chave'], 'gid': GID_OBJ + chaves.index(o['chave']),
                 'x': round(o['x'], 1), 'y': round(o['y'], 1), 'width': w, 'height': h, 'rotation': 0, 'visible': True,
                 'properties': props(o['props'])})
lid += 1
layers.append({'id': lid, 'name': 'objetos', 'type': 'objectgroup', 'x': 0, 'y': 0, 'opacity': 1, 'visible': True,
               'draworder': 'topdown', 'objects': objs})
pts = []
for p in pontos:
    oid += 1
    pts.append({'id': oid, 'name': p['props'].get('nome', p['tipo']), 'type': p['tipo'], 'point': True,
                'x': round(p['x'], 1), 'y': round(p['y'], 1), 'width': 0, 'height': 0, 'rotation': 0, 'visible': True,
                'properties': props(p['props'])})
lid += 1
layers.append({'id': lid, 'name': 'pontos', 'type': 'objectgroup', 'x': 0, 'y': 0, 'opacity': 1, 'visible': True,
               'draworder': 'topdown', 'objects': pts})

mapa = {
    'type': 'map', 'version': '1.10', 'tiledversion': '1.11.2', 'orientation': 'orthogonal', 'renderorder': 'right-down',
    'infinite': False, 'width': L, 'height': A, 'tilewidth': T, 'tileheight': T, 'nextlayerid': lid + 1,
    'nextobjectid': oid + 1,
    'properties': [{'name': 'origem', 'type': 'string',
                    'value': 'gerado por ferramentas/mapas/gerar_praca.py; arte: Modern Exteriors (LimeZu)'}],
    'tilesets': [
        {'firstgid': 1, 'name': 'chao', 'image': '../limezu/chao.png', 'imagewidth': atlas.width,
         'imageheight': atlas.height, 'tilewidth': T, 'tileheight': T, 'columns': ATLAS_COLS, 'tilecount': n_chao,
         'margin': 0, 'spacing': 0},
        {'firstgid': GID_OBJ, 'name': 'objetos', 'columns': 0, 'tilewidth': max(w for w, h in TAM.values()),
         'tileheight': max(h for w, h in TAM.values()), 'tilecount': len(chaves), 'margin': 0, 'spacing': 0,
         'grid': {'orientation': 'orthogonal', 'width': 1, 'height': 1},
         'tiles': [{'id': i, 'image': f'../limezu/objetos/{k}.png', 'imagewidth': TAM[k][0], 'imageheight': TAM[k][1],
                    'type': k} for i, k in enumerate(chaves)]},
    ],
    'layers': layers,
}
os.makedirs(os.path.join(ASSETS, 'mapas'), exist_ok=True)
with open(os.path.join(ASSETS, 'mapas', 'praca.tmj'), 'w', encoding='utf-8') as f:
    json.dump(mapa, f, ensure_ascii=False, separators=(',', ':'))

with open(os.path.join(SAIDA_ALT, 'pracaArte.js') if SAIDA_ALT else os.path.join(RAIZ, 'src', 'data', 'pracaArte.js'), 'w', encoding='utf-8') as f:
    f.write('// Gerado por ferramentas/mapas/gerar_praca.py. Arte: Modern Exteriors (LimeZu). Não editar à mão.\n')
    f.write(f'export const OBJETOS_PRACA = {json.dumps(chaves)};\n')
    f.write(f'export const PERSONAGENS_PRACA = {json.dumps(list(PERSONAGENS))};\n')

# ---------- prévia ----------
im = Image.new('RGBA', (L * T, A * T), (0, 0, 0, 255))
for nome, dados in camadas_chao.items():
    for y in range(A):
        for x in range(L):
            g = dados[y][x]
            if g:
                c, r = (g - 1) % ATLAS_COLS, (g - 1) // ATLAS_COLS
                im.alpha_composite(atlas.crop((c * T, r * T, c * T + T, r * T + T)), (x * T, y * T))
for o in sorted(objetos, key=lambda o: o['y']):
    sp = Image.open(os.path.join(DEST, 'objetos', o['chave'] + '.png')).convert('RGBA')
    x, y = int(o['x']), int(o['y']) - sp.height
    canvas = Image.new('RGBA', im.size, (0, 0, 0, 0))
    canvas.paste(sp, (x, y))
    im.alpha_composite(canvas)
for p in pontos:
    cor = {'npc': (255, 60, 200, 255), 'itacoin': (255, 220, 0, 255), 'inicio': (0, 120, 255, 255)}.get(p['tipo'], (255, 255, 255, 255))
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            im.putpixel((min(L * T - 1, max(0, int(p['x']) + dx)), min(A * T - 1, max(0, int(p['y']) + dy))), cor)
im.save(os.path.join(SAIDA_ALT, 'praca-mapa.png') if SAIDA_ALT else os.path.join(RAIZ, 'ferramentas', 'arte', 'previas', 'praca-mapa.png'))
print('ok:', f'{L}x{A} tiles,', len(objetos), 'objetos,', len(pontos), 'pontos, tabela de bordas com', len(TABELA))
