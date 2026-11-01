"""Monta o mapa da Fase 1 (Itajubá) por trechos e escreve src/levels/itajuba.js.
Uso: python3 ferramentas/mapas/gerar_itajuba.py > src/levels/itajuba.js
Referência de alcance (config.js): pulo alto ~4,5 tiles de altura e ~6 tiles de distância; quique no toldo ~9 tiles.
Rodar sobrescreve edições feitas à mão no itajuba.js.
"""
W, H = 320, 17
g = [['.'] * W for _ in range(H)]
def put(x, y, c): g[y][x] = c
def chao(x0, x1, topo=15):
    for x in range(x0, x1 + 1):
        for y in range(topo, H): g[y][x] = '#'
def buraco(x0, x1):
    for x in range(x0, x1 + 1):
        for y in range(H): 
            if g[y][x] == '#': g[y][x] = '.'
def linha(x0, x1, y, c):
    for x in range(x0, x1 + 1): g[y][x] = c
def bloco(x0, x1, y0):  # bloco sólido do y0 até o chão
    for x in range(x0, x1 + 1):
        for y in range(y0, H): g[y][x] = '#'

chao(0, W - 1)
# 1. rua de saída: começo calmo
put(3, 14, 'P')
for x in (10, 12, 14): put(x, 11, 's')
put(18, 14, 'a')
# primeira capivara, sozinha, no plano
put(30, 14, 'C')
for x in (28, 30, 32): put(x, 9, 's')
# degrauzinho
bloco(38, 40, 13)
put(39, 12, 'a')
# 2. feira: barracas com toldos (quicar!)
linha(46, 49, 11, 'T'); put(53, 14, 'C')
for y in (5, 3): put(47, y, 's')
put(48, 1, 's')
linha(58, 61, 11, 'T')
linha(63, 67, 6, '=')
for x in (64, 66): put(x, 5, 's')
put(65, 14, 'a')
linha(72, 75, 11, 'T'); put(78, 14, 'C')
put(73, 3, 'h')
# buraco pequeno no fim da feira
buraco(86, 87)
for x in (85, 86, 87, 88): put(x, 10, 's')
# 3. praça com a fonte
put(96, 14, 'a')
put(104, 14, 'C')
put(112, 14, 'F')   # ocupa 112..114
for x, y in ((110, 9), (113, 7), (116, 9)): put(x, y, 's')
put(122, 14, 'C')
linha(126, 129, 11, '=')
put(127, 10, 'h'); put(128, 10, 'a')
# checkpoint no meio
put(136, 14, 'K')
# 4. segunda metade: buracos com plataformas
buraco(144, 147)
linha(145, 146, 11, '=')
put(145, 10, 's'); put(146, 10, 's')
put(152, 14, 'C')
bloco(158, 160, 13)
bloco(161, 163, 11)
put(162, 10, 'a')
buraco(164, 168)
linha(170, 172, 11, '=') 
put(166, 8, 's')
# toldo que lança para cima de um muro alto
linha(178, 181, 11, 'T')
bloco(185, 188, 9)
for x in (185, 186, 187, 188): put(x, 8, 's')
put(186, 4, 'h')
put(193, 14, 'C')
put(199, 14, 'C')
buraco(204, 206)
linha(208, 211, 11, '=')
put(209, 10, 'a'); put(210, 10, 'a')
# escadinha + buraco largo atravessado pelo alto
bloco(214, 215, 13)
bloco(216, 217, 11)
buraco(218, 223)
linha(220, 221, 9, '=')
for x in (219, 220, 221, 222): put(x, 7, 's')
put(230, 14, 'C')
linha(236, 239, 11, 'T')
linha(242, 246, 5, '=')
for x in (242, 244, 246): put(x, 4, 's')
put(250, 14, 'C')
put(256, 14, 'a')
put(262, 14, 'C')
linha(266, 269, 11, 'T')
for y in (6, 4): put(267, y, 's')
put(272, 14, 'C')
# 5. rua final até o Espaço
for x in (280, 283, 286, 289): put(x, 12, 's')
put(305, 14, 'E')
# muro do fim
bloco(W - 2, W - 1, 0)
print('// Fase 1, Itajubá (CLAUDE.md, seção 11): rua de saída, feira com toldos, praça com a fonte, checkpoint,')
print('// segunda metade com buracos e plataformas, e a rua final até a porta do Espaço Paula De Marco (E).')
print('// Legenda em leitor.js e no CLAUDE.md (seção 10). Todas as linhas precisam ter o mesmo tamanho.')
print('// Gerado por ferramentas/mapas/gerar_itajuba.py; dá para editar à mão.')
print('export const ITAJUBA = [')
for l in g: print(f"  '{''.join(l)}',")
print('];')
