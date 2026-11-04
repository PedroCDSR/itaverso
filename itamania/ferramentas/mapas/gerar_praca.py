"""Gera o mapa da Praça (Centro explorável, vista de cima) no formato do Tiled: public/assets/mapas/praca.tmj.

Arte: só tiles do pacote Ninja Adventure (Pixel-boy e AAA, CC0), em public/assets/ninja/tilesets/. Nada desenhado
do zero. O arquivo .tmj abre no Tiled (https://www.mapeditor.org) para o Pedro editar à mão.

Referência da praça (Praça Theodomiro Santiago): o mapa-múndi do Pedro (moldura de caminho, 4 gramados, caminhos
em cruz, fonte redonda no meio com o busto, árvores nos cantos) e as notas em referencias/mapa (satélite).

Camadas (de baixo para cima):
  chao      grama + caminhos de terra (bordas escolhidas automaticamente)
  agua      espelho d'água da fonte
  objetos   casas, troncos, bancos, placas, base da estátua (abaixo do herói)
  cima      copas e topo da estátua (por cima do herói)
  colisao   onde não se anda (camada invisível no jogo)
  pontos    camada de objetos: início, moradores, placas, itacoins, saída

Uso (dentro de itamania/):  python3 ferramentas/mapas/gerar_praca.py
"""
import json
import os
import random

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TS_DIR = os.path.join(RAIZ, 'public', 'assets', 'ninja', 'tilesets')
SAIDA = os.path.join(RAIZ, 'public', 'assets', 'mapas', 'praca.tmj')
T = 16
L, A = 36, 28  # tamanho do mapa em tiles
random.seed(1913)  # ano da fundação do IEMI: o mapa sai sempre igual

TILESETS = ['TilesetFloor', 'TilesetWater', 'TilesetNature', 'TilesetHouse', 'TilesetElement', 'TilesetLogic']
IMGS = {n: Image.open(os.path.join(TS_DIR, n + '.png')).convert('RGBA') for n in TILESETS}
FIRST = {}
_g = 1
for n in TILESETS:
    FIRST[n] = _g
    w, h = IMGS[n].size
    _g += (w // T) * (h // T)


def gid(ts, c, r):
    return FIRST[ts] + r * (IMGS[ts].width // T) + c


# ---------- bordas ----------
# Cada bloco de terreno do pacote traz um terreno B (terra ou água) sobre a grama, sempre no mesmo arranjo:
# um 3x3 com as bordas e os cantos de fora (canto de cima à esquerda em c0, r0) e, no bloco de terra, os 4 cantos
# de dentro num 2x2. As posições foram conferidas na grade (ferramentas/arte/previas, grade dos tilesets).
# Por isso os caminhos do mapa têm sempre 2 tiles de largura ou mais (faixas de 1 tile pediriam outros tiles).
TERRA = dict(c0=0, r0=7, dentro={'no': (6, 9), 'ne': (5, 9), 'so': (6, 8), 'se': (5, 8)},
             cheio=[(1, 8), (8, 8), (8, 9)])
AGUA = dict(c0=0, r0=6, dentro=None, cheio=[(1, 7)])
GRAMA_LISA = [(0, 12), (1, 12), (2, 12), (3, 11), (3, 12), (4, 12)]


def autotile(mascara, bl, ts):
    """mascara[y][x] = True onde é o terreno B. Devolve a camada de gids (0 = vazio)."""
    camada = [[0] * L for _ in range(A)]

    def b(x, y):
        return not (0 <= x < L and 0 <= y < A) or mascara[y][x]

    for y in range(A):
        for x in range(L):
            if not mascara[y][x]:
                continue
            n, s, o, l = b(x, y - 1), b(x, y + 1), b(x - 1, y), b(x + 1, y)
            dc = 0 if not o else 2 if not l else 1  # coluna dentro do 3x3
            dr = 0 if not n else 2 if not s else 1  # linha dentro do 3x3
            pos = (bl['c0'] + dc, bl['r0'] + dr)
            if (dc, dr) == (1, 1):
                pos = random.choice(bl['cheio'])
                if bl['dentro']:
                    for canto, (vx, vy) in (('no', (-1, -1)), ('ne', (1, -1)), ('so', (-1, 1)), ('se', (1, 1))):
                        if not b(x + vx, y + vy):
                            pos = bl['dentro'][canto]
                            break
            camada[y][x] = gid(ts, *pos)
    return camada


# ---------- desenho da praça ----------
terra = [[False] * L for _ in range(A)]
agua = [[False] * L for _ in range(A)]
objetos = [[0] * L for _ in range(A)]
cima = [[0] * L for _ in range(A)]
colisao = [[False] * L for _ in range(A)]
pontos = []


def retangulo(m, x0, y0, x1, y1, v=True):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            m[y][x] = v


def colocar(camada, ts, c0, r0, w, h, x, y, bate=True):
    """Copia um pedaço w×h do tileset (a partir de c0, r0) para o mapa na posição x, y."""
    for dy in range(h):
        for dx in range(w):
            camada[y + dy][x + dx] = gid(ts, c0 + dx, r0 + dy)
            if bate:
                colisao[y + dy][x + dx] = True


def ponto(tipo, x, y, **props):
    pontos.append(dict(tipo=tipo, x=x, y=y, props=props))


# ruas de terra em volta da praça
PX0, PY0, PX1, PY1 = 7, 9, 28, 23  # praça (gramado + caminhos)
retangulo(terra, 1, 5, L - 2, 7)  # rua de cima, na frente das lojas
retangulo(terra, 3, 5, 5, A - 3)  # rua da esquerda
retangulo(terra, L - 6, 5, L - 4, A - 3)  # rua da direita
retangulo(terra, 3, A - 4, L - 4, A - 3)  # rua de baixo
retangulo(terra, 17, A - 3, 18, A - 1)  # saída para a Rua Nova (embaixo, no meio)

# caminhos da praça: moldura e cruz
for x0, y0, x1, y1 in [
    (PX0, PY0, PX1, PY0 + 1), (PX0, PY1 - 1, PX1, PY1), (PX0, PY0, PX0 + 1, PY1), (PX1 - 1, PY0, PX1, PY1),  # moldura
    (17, PY0, 18, PY1), (PX0, 15, PX1, 16),  # cruz
    (17, 8, 18, 8), (17, PY1 + 1, 18, PY1 + 1), (6, 15, 6, 16), (PX1 + 1, 15, PX1 + 1, 16),  # entradas
]:
    retangulo(terra, x0, y0, x1, y1)
# canteiro de grama em volta da fonte (no mapa do Pedro, a fonte fica no meio, onde a cruz se encontra)
retangulo(terra, 15, 13, 20, 18, False)

# fonte: espelho d'água 4x4 no meio, estátua no centro (lugar do busto de Theodomiro Santiago)
retangulo(agua, 16, 14, 19, 17)
retangulo(colisao, 16, 14, 19, 17)
colocar(objetos, 'TilesetHouse', 7, 20, 1, 2, 17, 15, bate=False)  # corpo e pedestal da estátua
colocar(cima, 'TilesetHouse', 7, 19, 1, 1, 17, 14, bate=False)  # cabeça (por cima do herói)
ponto('fonte', 17.5, 17.6, nome='Fonte', fala='fonte')

# lojas e casas na rua de cima (frente para a praça)
colocar(objetos, 'TilesetHouse', 0, 0, 4, 3, 1, 2)  # casa
colocar(objetos, 'TilesetHouse', 4, 0, 4, 3, 6, 2)  # Club Itajubense (casarão creme)
colocar(objetos, 'TilesetHouse', 19, 0, 4, 3, 12, 2)  # Café do Vadinho
colocar(objetos, 'TilesetHouse', 16, 0, 3, 3, 19, 2)  # Cesar Burg (placa de lanche no telhado)
colocar(objetos, 'TilesetHouse', 12, 0, 4, 3, 24, 2)  # casa vermelha
colocar(objetos, 'TilesetHouse', 8, 0, 4, 3, 30, 2)  # casa
for x, nome, fala in [(10, 'Club Itajubense', 'clube'), (16, 'Café do Vadinho', 'cafe'), (22, 'Cesar Burg', 'burg')]:
    colocar(objetos, 'TilesetElement', 6, 3, 1, 1, x, 4, bate=True)  # placa (topo)
    ponto('placa', x + 0.5, 5, nome=nome, fala=fala)
# telhados de trás (fileira de cima do mapa): árvores, para fechar a borda
for x in range(0, L, 2):
    colocar(cima, 'TilesetNature', 0, 0, 2, 1, x, 0, bate=False)
    colocar(objetos, 'TilesetNature', 0, 1, 2, 1, x, 1, bate=False)
retangulo(colisao, 0, 0, L - 1, 1)

# laterais: fileira de árvores e casas
for y in range(9, A - 4, 3):
    colocar(cima, 'TilesetNature', 2, 0, 2, 1, 0, y, bate=False)
    colocar(objetos, 'TilesetNature', 2, 1, 2, 1, 0, y + 1)
    colocar(cima, 'TilesetNature', 2, 0, 2, 1, L - 2, y, bate=False)
    colocar(objetos, 'TilesetNature', 2, 1, 2, 1, L - 2, y + 1)
retangulo(colisao, 0, 2, 0, A - 1)
retangulo(colisao, L - 1, 2, L - 1, A - 1)
# fundo (embaixo): árvores dos dois lados da saída
for x in list(range(0, 16, 2)) + list(range(20, L, 2)):
    colocar(cima, 'TilesetNature', 0, 0, 2, 1, x, A - 2, bate=False)
    colocar(objetos, 'TilesetNature', 0, 1, 2, 1, x, A - 1)
ponto('saida', 17.9, A - 0.5, nome='Saída', fala='saida')
colocar(objetos, 'TilesetElement', 6, 3, 1, 2, 19, A - 4, bate=False)  # placa da saída
colisao[A - 3][19] = True
ponto('placa', 19.5, A - 2, nome='Placa', fala='placaSaida')

# gramados: árvores grandes nos 4 cantos (no mapa do Pedro, palmeiras)
for x, y in [(9, 10), (25, 10), (9, 20), (25, 20)]:
    colocar(cima, 'TilesetNature', 6, 8, 2, 1, x, y, bate=False)
    colocar(objetos, 'TilesetNature', 6, 9, 2, 1, x, y + 1)
# arbustos e flores nos gramados
for x, y in [(12, 11), (14, 10), (22, 11), (20, 10), (12, 20), (14, 21), (22, 20), (20, 21), (10, 13), (26, 13),
             (10, 18), (26, 18)]:
    colocar(objetos, 'TilesetNature', random.choice([0, 1, 2, 6]), 10, 1, 1, x, y, bate=False)
# bancos nos caminhos, de frente para a fonte
for x, y in [(11, 14), (22, 14), (11, 17), (22, 17)]:
    colocar(objetos, 'TilesetElement', 11, 1, 3, 1, x, y)

# pontos: início, moradores (sprite do pacote), itacoins
ponto('inicio', 17.9, 25.5)
ponto('npc', 15, 18.6, sprite='OldMan', nome='Guia da praça', fala='guia')
ponto('npc', 12.5, 13.6, sprite='OldWoman', nome='Dona Cida', fala='vovo')
ponto('npc', 14, 6.4, sprite='Woman', nome='{barista}', fala='barista')
ponto('npc', 21, 6.4, sprite='Villager4', nome='{atendente}', fala='atendente')
ponto('npc', 24, 16.5, sprite='Villager3', nome='Estudante', fala='estudante', anda=1)
ponto('gato', 27, 21.5)
for x, y in [(8, 9.5), (28, 9.5), (8, 23.5), (28, 23.5), (13, 15.5), (23, 15.5), (17.9, 11), (17.9, 21), (4, 12),
             (32, 12), (4, 20), (32, 20), (9.5, 6.5), (27.5, 6.5)]:
    ponto('itacoin', x, y)

# ---------- montagem do .tmj ----------
grama = [[gid('TilesetFloor', *random.choice(GRAMA_LISA[:1] if random.random() < 0.6 else GRAMA_LISA))
          for _ in range(L)] for _ in range(A)]
camada_terra = autotile(terra, TERRA, 'TilesetFloor')
chao = [[camada_terra[y][x] or grama[y][x] for x in range(L)] for y in range(A)]
camada_agua = autotile(agua, AGUA, 'TilesetWater')
marca = gid('TilesetLogic', 0, 0)
camada_colisao = [[marca if colisao[y][x] else 0 for x in range(L)] for y in range(A)]


def tile_layer(lid, nome, dados, visivel=True):
    return {
        'id': lid, 'name': nome, 'type': 'tilelayer', 'x': 0, 'y': 0, 'width': L, 'height': A,
        'opacity': 1, 'visible': visivel, 'data': [v for linha in dados for v in linha],
    }


objs = []
for i, p in enumerate(pontos, start=1):
    props = [{'name': k, 'type': 'int' if isinstance(v, int) else 'string', 'value': v} for k, v in p['props'].items()]
    objs.append({
        'id': i, 'name': p['props'].get('nome', p['tipo']), 'type': p['tipo'], 'point': True,
        'x': round(p['x'] * T, 1), 'y': round(p['y'] * T, 1), 'width': 0, 'height': 0, 'rotation': 0,
        'visible': True, 'properties': props,
    })

mapa = {
    'type': 'map', 'version': '1.10', 'tiledversion': '1.11.2', 'orientation': 'orthogonal',
    'renderorder': 'right-down', 'infinite': False, 'width': L, 'height': A, 'tilewidth': T, 'tileheight': T,
    'nextlayerid': 7, 'nextobjectid': len(objs) + 1,
    'properties': [{'name': 'origem', 'type': 'string',
                    'value': 'gerado por ferramentas/mapas/gerar_praca.py; arte: Ninja Adventure (CC0)'}],
    'tilesets': [
        {
            'firstgid': FIRST[n], 'name': n, 'image': f'../ninja/tilesets/{n}.png',
            'imagewidth': IMGS[n].width, 'imageheight': IMGS[n].height, 'tilewidth': T, 'tileheight': T,
            'columns': IMGS[n].width // T, 'tilecount': (IMGS[n].width // T) * (IMGS[n].height // T),
            'margin': 0, 'spacing': 0,
        }
        for n in TILESETS
    ],
    'layers': [
        tile_layer(1, 'chao', chao),
        tile_layer(2, 'agua', camada_agua),
        tile_layer(3, 'objetos', objetos),
        tile_layer(4, 'cima', cima),
        tile_layer(5, 'colisao', camada_colisao, visivel=False),
        {'id': 6, 'name': 'pontos', 'type': 'objectgroup', 'x': 0, 'y': 0, 'opacity': 1, 'visible': True,
         'draworder': 'topdown', 'objects': objs},
    ],
}
os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
with open(SAIDA, 'w', encoding='utf-8') as f:
    json.dump(mapa, f, ensure_ascii=False, separators=(',', ':'))


# prévia em PNG (só para conferir; não vai para o jogo)
def previa():
    im = Image.new('RGBA', (L * T, A * T), (0, 0, 0, 255))
    porgid = {}
    for n in TILESETS:
        cols = IMGS[n].width // T
        for i in range((IMGS[n].width // T) * (IMGS[n].height // T)):
            porgid[FIRST[n] + i] = (n, i % cols, i // cols)
    for dados in (chao, camada_agua, objetos, cima):
        for y in range(A):
            for x in range(L):
                g = dados[y][x]
                if g:
                    n, c, r = porgid[g]
                    im.alpha_composite(IMGS[n].crop((c * T, r * T, c * T + T, r * T + T)), (x * T, y * T))
    for p in pontos:
        cor = {'npc': (255, 60, 200, 255), 'itacoin': (255, 220, 0, 255), 'inicio': (0, 120, 255, 255)}.get(
            p['tipo'], (255, 255, 255, 255))
        x, y = int(p['x'] * T), int(p['y'] * T)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                im.putpixel((min(L * T - 1, max(0, x + dx)), min(A * T - 1, max(0, y + dy))), cor)
    destino = os.path.join(RAIZ, 'ferramentas', 'arte', 'previas', 'praca-mapa.png')
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    im.resize((im.width * 2, im.height * 2), Image.NEAREST).save(destino)


previa()
print('ok:', os.path.relpath(SAIDA, RAIZ), f'{L}x{A} tiles,', len(pontos), 'pontos')
