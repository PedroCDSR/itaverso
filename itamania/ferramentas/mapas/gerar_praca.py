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
ASSETS = os.path.join(RAIZ, 'public', 'assets')
DEST = os.path.join(ASSETS, 'limezu')
T = 16
L, A = 70, 45
random.seed(1913)

# ---------- chão: atlas com só os tiles usados ----------
# Autotiles do pacote no formato do GameMaker (12x4 = 47 bordas + 1 vazio): 19 calçada bege sobre asfalto,
# 5 grama (fundo transparente, vai por cima da calçada), 18 espelho d'água com borda de pedra.
AUTOTILES = {'calcada': 19, 'grama': 5, 'agua': 18}
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


asfaltos = [f for f in sorted(os.listdir(os.path.join(TEMAS, '2_City_Terrains_Singles_16x16'))) if 'Asphalt' in f and _liso(f)][:ATLAS_COLS]
print('asfaltos lisos:', len(asfaltos))
for c, f in enumerate(asfaltos):
    atlas.alpha_composite(Image.open(os.path.join(TEMAS, '2_City_Terrains_Singles_16x16', f)).convert('RGBA'), (c * T, 12 * T))
# faixas de pedestre: bloco 4x4 da folha de terrenos da cidade (colunas 5 a 8, linhas 4 a 7)
terrenos = Image.open(os.path.join(TEMAS, '2_City_Terrains_16x16.png')).convert('RGBA')
atlas.alpha_composite(terrenos.crop((5 * T, 4 * T, 9 * T, 8 * T)), (0, 13 * T))
os.makedirs(DEST, exist_ok=True)
atlas.save(os.path.join(DEST, 'chao.png'))


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
    'hotel': '12_Hotel_and_Hospital_Singles_16x16/ME_Singles_Hotel_and_Hospital_16x16_Hotel_1.png',
    'cafe': '9_Shopping_Center_and_Markets_Singles_16x16/ME_Singles_Shopping_Center_and_Markets_16x16_Market_Small_5.png',
    'burg': '9_Shopping_Center_and_Markets_Singles_16x16/ME_Singles_Shopping_Center_and_Markets_16x16_Market_Small_1.png',
    'subway': '9_Shopping_Center_and_Markets_Singles_16x16/ME_Singles_Shopping_Center_and_Markets_16x16_Market_Small_3.png',
    'acai': '9_Shopping_Center_and_Markets_Singles_16x16/ME_Singles_Shopping_Center_and_Markets_16x16_Market_Small_8.png',
    'arena': '9_Shopping_Center_and_Markets_Singles_16x16/ME_Singles_Shopping_Center_and_Markets_16x16_Market_Medium_9.png',
    'clube': '24_Additional_Houses_Singles_16x16/24_Additional_Houses_Victorian_House_5_16x16.png',
    'forum': '4_Generic_Building_Singles_16x16/ME_Singles_Generic_Building_16x16_Condo_4_17.png',
    'sobrado1': '24_Additional_Houses_Singles_16x16/24_Additional_Houses_Terraced_House_1_16x16.png',
    'sobrado4': '24_Additional_Houses_Singles_16x16/24_Additional_Houses_Terraced_House_4_16x16.png',
    'predio9': '4_Generic_Building_Singles_16x16/ME_Singles_Generic_Building_16x16_Condo_9_Example.png',
    # praça
    'arvore_grande': '7_Villas_Singles_16x16/ME_Singles_Villas_16x16_Tree_4.png',
    'arvore_media': '7_Villas_Singles_16x16/ME_Singles_Villas_16x16_Tree_3.png',
    'arvore_rua': '3_City_Props_Singles_16x16/ME_Singles_City_Props_16x16_Tree_12.png',
    'fonte_redonda': '17_Garden_Singles_16x16/ME_Singles_Garden_16x16_Fountain_3_4.png',
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


os.makedirs(os.path.join(DEST, 'objetos'), exist_ok=True)
TAM = {}
for chave, rel in ARQ.items():
    destino = os.path.join(DEST, 'objetos', chave + '.png')
    shutil.copyfile(achar(rel), destino)
    TAM[chave] = Image.open(destino).size

# como cada tipo de objeto bate: retângulo (x, y, largura, altura) a partir do canto de baixo à esquerda, em px
def caixa(chave):
    w, h = TAM[chave]
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


# ruas (o resto é calçada): duas horizontais e duas verticais em volta da praça
RUA_N, RUA_S = (13, 15), (38, 40)
RUA_O, RUA_L = (18, 20), (55, 57)
ret(calcada, 0, 0, L - 1, A - 1)
ret(calcada, 0, RUA_N[0], L - 1, RUA_N[1], False)
ret(calcada, 0, RUA_S[0], L - 1, RUA_S[1], False)
ret(calcada, RUA_O[0], 0, RUA_O[1], A - 1, False)
ret(calcada, RUA_L[0], 0, RUA_L[1], A - 1, False)

# faixas de pedestre nas entradas da praça. No atlas: colunas 2 e 3 = faixa sem borda; linhas FX e FX+1 = barras
# deitadas (para atravessar uma rua horizontal), FX+2 e FX+3 = barras em pé (rua vertical).
FX = 13
for x0 in (30, 44):
    for dy, y in enumerate(range(RUA_N[0], RUA_N[1] + 1)):
        for dx in range(2):
            faixas[y][x0 + dx] = gid_chao(2 + dx, FX + (dy % 2))
for xs, y0s in ((RUA_O, (22, 31)), (RUA_L, (27,))):
    for y0 in y0s:
        for x in range(xs[0], xs[1] + 1):
            for dy in range(2):
                faixas[y0 + dy][x] = gid_chao(2 + (x % 2), FX + 2 + dy)

# praça: x 21..54, y 16..37. Maciços de árvores (grama) como no satélite
PX0, PX1, PY0, PY1 = 21, 54, 16, 37
MACICOS = [
    (22, 17, 32, 25),  # noroeste
    (41, 17, 50, 22),  # nordeste
    (22, 32, 34, 36),  # sudoeste
    (41, 25, 53, 36),  # leste e sudeste
]
for m in MACICOS:
    ret(grama, *m)
# espelho d'água retangular no largo e área redonda (fonte) a nordeste dele
ret(agua, 25, 27, 32, 30)
obj('fonte_redonda', 36, 25.6, nome='Fonte', fala='fonte')

# árvores nos maciços: copas grandes e sobrepostas
for (x0, y0, x1, y1) in MACICOS:
    y = y0 + 3
    linha = 0
    while y <= y1 + 1:
        x = x0 + (0 if linha % 2 == 0 else 2)
        while x + 5 <= x1 + 2:
            chave = 'arvore_grande' if (x + y) % 3 else 'arvore_media'
            obj(chave, x + random.uniform(-0.4, 0.4), y + random.uniform(-0.2, 0.2))
            x += 5
        y += 3
        linha += 1

# bancos e postes em volta do largo
for x in (25, 29):
    obj('banco_h', x, 26.2)
    obj('banco_h', x, 32.6)
obj('banco_v', 23.4, 30.2)
obj('banco_v', 34.2, 30.2)
for x, y in [(21.2, 16.8), (54.2, 16.8), (21.2, 37.6), (54.2, 37.6), (36.5, 31.5), (38.5, 18.5), (38.5, 36.5)]:
    obj('poste', x, y)
obj('lixeira', 33.4, 26.5)
obj('placa', 33.5, 31.6, nome='Placa da praça', fala='placa')
for x in (37, 39):
    obj('flores', x, 23.4)

# prédios: quadra de cima (base na linha 11, a calçada fica embaixo)
obj('sobrado1', 0, 11.6)
obj('subway', 13, 11.6)
obj('sobrado4', 21, 11.6)
obj('hotel', 33, 11.6, nome='Hotel Centenário', fala='hotel')
obj('cafe', 50, 11.6, nome='{cafe}', fala='cafe')
obj('burg', 58, 11.6, nome='{lanchonete}', fala='burg')
obj('predio9', 63.5, 11.6)
# quadra da esquerda
obj('forum', 8, 21.6, nome='Fórum Cível', fala='forum')
obj('clube', -1, 37.6, nome='Club Itajubense', fala='clube')
# quadra da direita
obj('acai', 59, 24.6, nome='Açaí', fala='acai')
obj('arena', 60, 36.6, nome='Arena', fala='arena')
# calçada de baixo: árvores de rua
for x in range(1, L, 6):
    obj('arvore_rua', x, A - 1.2)

# pontos: início, moradores, itacoins, saída
ponto('inicio', 37.5, 43.5)
ponto('saida', 37.5, A - 0.2)
ponto('npc', 30, 33.8, sprite='postman3', nome='Guia da praça', fala='guia')
ponto('npc', 26, 26.0, sprite='scout4', nome='Dona Cida', fala='vovo')
ponto('npc', 52.5, 12.8, sprite='postman2', nome='Barista', fala='barista')
ponto('npc', 60.5, 12.8, sprite='scout5', nome='Atendente', fala='atendente')
ponto('npc', 37, 21.5, sprite='scout3', nome='Estudante', fala='estudante', anda=1)
ponto('npc', 45, 24.0, sprite='postman1', nome='Carteiro', fala='carteiro')
for x, y in [(22, 16.6), (53.5, 16.6), (22, 37.2), (53.5, 37.2), (36, 34), (39.5, 28), (24, 28.5), (47, 23.6),
             (10, 12.6), (65, 12.6), (19, 27), (56, 20), (30, 42), (46, 42)]:
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
    if not (35 <= x <= 40):
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
with open(os.path.join(ASSETS, 'mapas', 'praca.tmj'), 'w', encoding='utf-8') as f:
    json.dump(mapa, f, ensure_ascii=False, separators=(',', ':'))

with open(os.path.join(RAIZ, 'src', 'data', 'pracaArte.js'), 'w', encoding='utf-8') as f:
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
im.save(os.path.join(RAIZ, 'ferramentas', 'arte', 'previas', 'praca-mapa.png'))
print('ok:', f'{L}x{A} tiles,', len(objetos), 'objetos,', len(pontos), 'pontos, tabela de bordas com', len(TABELA))
