"""Peças da praça montadas a partir do Modern Exteriors (LimeZu) e da arte própria do projeto.

- girar45(): mostra um prédio girado 45° (a quina virada para a câmera): as duas fachadas do pacote são entortadas
  na diagonal 2:1 (degraus limpos de pixel art) e o telhado vira um losango.
- clube(), busto(), concha(), cafe(), burg(): peças da Praça Theodomiro Santiago (fotos do Pedro, 05/11/2026).
Usado por ferramentas/mapas/gerar_praca.py.
"""
import colorsys
import os

from PIL import Image, ImageDraw

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACOTE = os.path.join(RAIZ, 'referencias', 'licenciados', 'modern-exteriors')
MOD = os.path.join(PACOTE, 'ME_Theme_Sorter_16x16', '5_Floor_Modular_Building_Singles_16x16',
                   'ME_Singles_Floor_Modular_Building_16x16_')
COMPLETO = os.path.join(PACOTE, 'Modern_Exteriors_Complete_Singles_16x16')


def abre(f):
    return Image.open(f).convert('RGBA')


def creme(im, matiz=0.11, sat=0.40):
    """Paredes viram creme-claro; contorno escuro e vidro ficam."""
    im = im.copy()
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a:
                continue
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            vidro = b > r + 20 and b > g and l > 0.58  # vidro é azul-claro; parede azul é mais escura
            if not vidro and 0.30 < l < 0.82:
                nl = min(0.95, 0.56 + l * 0.44)
                rr, gg, bb = colorsys.hls_to_rgb(matiz, nl, sat)
                px[x, y] = (int(rr * 255), int(gg * 255), int(bb * 255), a)
    return im


def escurecer(im, f=0.82):
    """Lado na sombra (a luz vem da direita/frente)."""
    im = im.copy()
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a:
                px[x, y] = (int(r * f), int(g * f), int(b * f), a)
    return im


def claro(im, tom=(232, 226, 212)):
    """Pinta tudo num tom claro só, mantendo luz e sombra (para lajes e telhados)."""
    im = im.copy()
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a:
                l = (r * 0.3 + g * 0.59 + b * 0.11) / 255
                k = 0.55 + 0.6 * l if l > 0.22 else 0.35
                px[x, y] = tuple(min(255, int(c * k)) for c in tom) + (a,)
    return im


def coluna_alta(pilar, altura):
    """Alonga uma coluna do pacote repetindo o fuste (sem esticar a imagem): capitel, fuste e base."""
    w, h = pilar.size
    cap, base = pilar.crop((0, 0, w, 16)), pilar.crop((0, h - 14, w, h))
    fuste = pilar.crop((0, h // 2, w, h // 2 + 1))
    out = Image.new('RGBA', (w, altura), (0, 0, 0, 0))
    for y in range(16, altura - 14):
        out.alpha_composite(fuste, (0, y))
    out.alpha_composite(cap, (0, 0))
    out.alpha_composite(base, (0, altura - 14))
    return out


def girar45(direita, esquerda, cor_teto, beirada, altura_extra=0):
    """direita: fachada que fica à direita da quina (sobe para a direita); esquerda: a outra (sobe para a esquerda).
    As duas com a mesma altura. Devolve a imagem do prédio girado 45°."""
    w1, w2, h = direita.width, esquerda.width, direita.height
    topo = (w1 + w2) // 2 + 4 + altura_extra
    img = Image.new('RGBA', (w1 + w2, h + topo), (0, 0, 0, 0))
    # parede da esquerda: a ponta de longe (u = 0) fica mais alta
    for u in range(w2):
        dy = (w2 - u) // 2
        col = esquerda.crop((u, 0, u + 1, h))
        img.alpha_composite(col, (u, topo - dy))
    # parede da direita: a ponta de longe (u = w1) fica mais alta
    for u in range(w1):
        dy = u // 2
        col = direita.crop((u, 0, u + 1, h))
        img.alpha_composite(col, (w2 + u, topo - dy))
    # telhado em losango (laje com platibanda)
    d = ImageDraw.Draw(img)
    frente = (w2, topo)
    esq = (0, topo - w2 // 2)
    dir_ = (w1 + w2 - 1, topo - w1 // 2)
    fundo = (w1 - 1, topo - (w1 + w2) // 2)
    d.polygon([frente, dir_, fundo, esq], fill=cor_teto)
    # platibanda: faixa clara nas duas bordas da frente e contorno escuro
    for k in range(3):
        d.line([(frente[0], frente[1] - k), (dir_[0], dir_[1] - k)], fill=beirada)
        d.line([(frente[0], frente[1] - k), (esq[0], esq[1] - k)], fill=beirada)
    contorno = (60, 58, 74, 255)
    d.line([esq, fundo, dir_], fill=contorno)
    d.line([(frente[0], frente[1] - 3), (dir_[0], dir_[1] - 3)], fill=(200, 194, 178, 255))
    d.line([(frente[0], frente[1] - 3), (esq[0], esq[1] - 3)], fill=(200, 194, 178, 255))
    # quina: linha vertical
    d.line([(w2, topo), (w2, topo + h - 1)], fill=(150, 140, 120, 255))
    return img.crop(img.getbbox())


def clube():
    """Club Itajubense girado 90° (pedido do Pedro, 05/11/2026): o pórtico de colunas fica virado para a praça (leste,
    à direita) e de frente para a câmera aparece a lateral sul, a da rua de baixo, com pilastras e janelas altas, como
    nas fotos. O pórtico aparece de perfil na ponta direita: laje do telhado avançando e as colunas.
    Peças do pacote (andar com janelas altas, colunata e janelas do palácio, laje, pilar) repintadas de creme."""
    W, fundo = 192, 52  # largura da lateral e profundidade do telhado visto de cima
    andar1 = creme(abre(MOD + 'Middle_Floor_15.png'))
    colunas = creme(abre(os.path.join(COMPLETO, 'ME_Singles_Garden_16x16_Palace_1_Entrance_Variant_2.png')))
    janelas = creme(abre(os.path.join(COMPLETO, 'ME_Singles_Garden_16x16_Palace_1_Entrance_Variant_1.png')))
    andar = Image.new('RGBA', (W, 48), (0, 0, 0, 0))
    andar.alpha_composite(andar1, (0, 0))
    andar.alpha_composite(andar1.crop((32, 0, 112, 48)), (112, 0))
    # térreo da lateral: só janelas altas, como o andar de cima (as "colunas" da foto são pilastras da parede),
    # com a base de pedra (granito) embaixo
    terreo = Image.new('RGBA', (W, 58), (0, 0, 0, 0))
    terreo.alpha_composite(andar, (0, 0))
    dd = ImageDraw.Draw(terreo)
    dd.rectangle((0, 48, W - 1, 57), fill=(176, 162, 156, 255))
    dd.line((0, 48, W - 1, 48), fill=(214, 204, 196, 255))
    dd.line((0, 57, W - 1, 57), fill=(84, 80, 92, 255))
    for x in range(0, W, 24):
        dd.line((x, 49, x, 56), fill=(150, 138, 132, 255))
    # telhado (laje com platibanda), da folha de telhados do pacote, esticado na largura
    teto = abre(MOD + 'Roof_10.png')
    telhado = Image.new('RGBA', (W, teto.height), (0, 0, 0, 0))
    telhado.alpha_composite(teto.crop((0, 0, 40, teto.height)), (0, 0))
    for x in range(40, W - 40, 32):
        telhado.alpha_composite(teto.crop((40, 0, 72, teto.height)), (x, 0))
    telhado.alpha_composite(teto.crop((72, 0, 112, teto.height)), (W - 40, 0))
    telhado = claro(telhado.crop((0, teto.height - fundo, W, teto.height)))
    # pórtico do lado da praça (à direita), visto de perfil: colunas gigantes que vão do chão à platibanda, com a laje
    # do pórtico avançando por cima
    av = 30
    pilar = creme(abre(os.path.join(COMPLETO, 'ME_Singles_Garden_16x16_Pillar_Modular_10.png')), 0.11, 0.22)
    pilar = pilar.crop(pilar.getbbox())
    alt = fundo + 48 + 58
    img = Image.new('RGBA', (W + av, alt), (0, 0, 0, 0))
    img.alpha_composite(telhado, (0, 0))
    img.alpha_composite(andar, (0, fundo))
    img.alpha_composite(terreo, (0, fundo + 48))
    d = ImageDraw.Draw(img)
    laje = claro(telhado.crop((W - av - 8, 0, W - 8, fundo)))
    img.alpha_composite(laje, (W, 0))
    d.rectangle((W, fundo - 2, W + av - 1, fundo + 6), fill=(244, 238, 222, 255))  # entablamento de perfil
    d.line((W, fundo + 7, W + av - 1, fundo + 7), fill=(84, 80, 92, 255))
    d.line((W + av - 1, 0, W + av - 1, fundo + 7), fill=(84, 80, 92, 255))
    hcol = alt - (fundo + 8)
    d.rectangle((W, fundo + 8, W + av - 1, alt - 1), fill=(200, 190, 168, 255))  # fundo do pórtico, na sombra
    d.rectangle((W, alt - 6, W + av - 1, alt - 1), fill=(224, 216, 196, 255))  # degrau
    for x, f in ((W + 1, 0.86), (W + av - pilar.width - 1, 1.0)):
        col = coluna_alta(pilar, hcol)
        img.alpha_composite(escurecer(col, f) if f < 1 else col, (x, fundo + 8))
    return img.crop(img.getbbox())


def busto():
    """Busto de Theodomiro Santiago (arte própria, public/assets/cenario/fonte.png) sobre um pedestal girado 45°."""
    f = abre(os.path.join(RAIZ, 'public', 'assets', 'cenario', 'fonte.png'))
    cabeca = f.crop((68, 0, 104, 44))
    ped = f.crop((60, 44, 113, 70))  # topo do pedestal e a placa
    # pedestal alto e estreito de pedra clara: frente com a placa de bronze (à direita da quina), lateral lisa
    pedra = f.getpixel((63, 52))
    claro = tuple(min(255, int(c * 1.08)) for c in pedra[:3]) + (255,)
    escuro = (96, 86, 74, 255)
    bronze, bronze2 = f.getpixel((80, 62)), f.getpixel((76, 58))
    frente = Image.new('RGBA', (24, 40), pedra)
    dd = ImageDraw.Draw(frente)
    dd.rectangle((0, 0, 23, 3), fill=claro)  # capitel
    dd.rectangle((0, 36, 23, 39), fill=claro)  # base
    dd.rectangle((5, 12, 18, 24), fill=bronze2)  # placa
    dd.rectangle((6, 13, 17, 23), fill=bronze)
    for yy in (16, 19):
        dd.line((8, yy, 15, yy), fill=bronze2)
    dd.line((0, 0, 0, 39), fill=escuro)
    lado = Image.new('RGBA', (16, 40), pedra)
    ImageDraw.Draw(lado).rectangle((0, 0, 15, 3), fill=claro)
    ImageDraw.Draw(lado).rectangle((0, 36, 15, 39), fill=claro)
    ImageDraw.Draw(lado).line((0, 0, 0, 39), fill=escuro)
    base = girar45(frente, escurecer(lado, 0.84), claro, claro)
    # a cabeça fica no centro do losango do topo (centro em x = 20, y = 10 na base recortada)
    pe = 10 + 8  # onde fica a base do busto dentro da imagem do pedestal
    sobe = max(0, cabeca.height - pe)
    img = Image.new('RGBA', (max(base.width, 20 + cabeca.width // 2) + 2, base.height + sobe), (0, 0, 0, 0))
    dx = max(0, cabeca.width // 2 - 20)
    img.alpha_composite(base, (dx, sobe))
    img.alpha_composite(cabeca, (dx + 20 - cabeca.width // 2, sobe + pe - cabeca.height))
    return img


def contorno(img, cor=(84, 80, 92, 255)):
    """Contorno de 1 px em volta da forma, como nas peças do pacote."""
    src = img.copy()
    sp, dp = src.load(), img.load()
    for y in range(img.height):
        for x in range(img.width):
            if sp[x, y][3]:
                continue
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < img.width and 0 <= ny < img.height and sp[nx, ny][3]:
                    dp[x, y] = cor
                    break
    return img


def concha():
    """Concha acústica da praça (foto do Pedro): quarto de cúpula de concreto claro sobre uma plataforma baixa, alta
    na abertura e baixando para trás, girada 45° (a abertura fica virada para a direita/baixo). Desenho próprio (o
    pacote não tem): fatias em arco de trás para a frente, na mesma projeção 2:1 de girar45()."""
    a0, H0, D, esp = 30, 38, 30, 4  # meia largura e altura na abertura, profundidade, espessura
    W, Ht = 2 * a0 + D + 40, H0 + a0 + D + 40
    img = Image.new('RGBA', (W, Ht), (0, 0, 0, 0))
    px = img.load()
    cx, cy = D + 20, Ht - 20

    def ponto(u, v, h):
        return int(round(cx + u - v)), int(round(cy - u * 0.5 - h - v * 0.5))

    def pinta(x, y, cor):
        if 0 <= x < W and 0 <= y < Ht:
            px[x, y] = cor

    def perfil(v):
        k = max(0.0, 1 - (v / D) ** 2) ** 0.5  # a cúpula baixa e estreita para trás
        return max(1.0, a0 * (0.55 + 0.45 * k)), H0 * k

    # plataforma
    for v in range(-6, D + 4):
        for u in range(-a0 - 6, a0 + 7):
            for h in (0, 1, 2):
                cor = (226, 222, 212, 255) if h == 2 else (184, 178, 168, 255)
                x, y = ponto(u, v, h)
                pinta(x, y, cor)
                pinta(x + 1, y, cor)
    # interior (sombra) e casca, fatia por fatia, de trás para a frente
    for v in range(D, -1, -1):
        a, H = perfil(v)
        if H < 1:
            continue
        frente = v == 0
        for u10 in range(int(-a * 2), int(a * 2) + 1):
            u = u10 / 2
            fora = H * max(0.0, 1 - (u / a) ** 2) ** 0.5
            ai, hi = a - esp, H - esp
            dentro = hi * max(0.0, 1 - (u / ai) ** 2) ** 0.5 if abs(u) < ai and hi > 0 else 0
            for h10 in range(0, int(fora * 2) + 1):
                h = h10 / 2
                if h < dentro:
                    if frente:
                        continue
                    c = int(176 - 50 * v / D)  # interior: mais escuro lá no fundo
                    cor = (c, c - 3, c - 8, 255)
                elif frente:
                    cor = (250, 248, 242, 255)  # borda da abertura
                else:
                    luz = 0.84 + 0.16 * (h / H0)
                    c = int(238 * luz)
                    cor = (c, c - 3, c - 9, 255)
                x, y = ponto(u, v, h + 2)
                pinta(x, y, cor)
    img = img.crop(img.getbbox())
    pad = Image.new('RGBA', (img.width + 2, img.height + 2), (0, 0, 0, 0))
    pad.alpha_composite(img, (1, 1))
    return contorno(pad)


def _peca(rel):
    return abre(os.path.join(PACOTE, 'ME_Theme_Sorter_16x16', rel))


def forum():
    """Fórum Cível: prédio do pacote repintado de branco (o prédio real é branco)."""
    return creme(_peca('4_Generic_Building_Singles_16x16/ME_Singles_Generic_Building_16x16_Condo_4_17.png'), 0.6, 0.06)


def predio_meio():
    """Prédio entre o Fórum e o Clube: peça do pacote repintada de amarelo-claro."""
    return creme(_peca('4_Generic_Building_Singles_16x16/ME_Singles_Generic_Building_16x16_Condo_4_15.png'), 0.13, 0.55)


# ---------- prédios do centro (estilo das fotos do Pedro: sobrados ecléticos claros com comércio embaixo) ----------
CORES = {  # matiz, saturação para creme()
    'creme': (0.11, 0.40), 'rosa': (0.02, 0.42), 'amarelo': (0.14, 0.62), 'azul': (0.56, 0.32),
    'verde': (0.30, 0.28), 'branco': (0.60, 0.05), 'pessego': (0.07, 0.55),
}
ANDARES = [1, 2, 3, 5, 7, 8, 9, 11, 15, 16, 17]  # Middle_Floor do pacote que combinam com sobrado
TERREOS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Ground_Floor_Condo (portas e vitrines, sem letreiro)
TETOS = [1, 3, 5, 7, 10]


def veneziana(im):
    """Vidro azul vira veneziana branca (listras), como nas janelas dos prédios antigos do centro."""
    im = im.copy()
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a and b > r + 25 and b > g + 5:
                v = 240 if y % 2 == 0 else 218
                px[x, y] = (v, v, v - 4, a)
    return im


def _telhado(n, fundo, largura=112):
    teto = abre(MOD + f'Roof_{n}.png')
    t = teto.crop((0, teto.height - fundo, 112, teto.height))
    if largura != 112:
        out = Image.new('RGBA', (largura, fundo), (0, 0, 0, 0))
        out.alpha_composite(t.crop((0, 0, 40, fundo)), (0, 0))
        for x in range(40, largura - 40, 32):
            out.alpha_composite(t.crop((40, 0, 72, fundo)), (x, 0))
        out.alpha_composite(t.crop((72, 0, 112, fundo)), (largura - 40, 0))
        t = out
    return claro(t)


def sobrado(semente, cor=None, andares=None, toldo=True, venez=None, fundo=26):
    """Sobrado eclético: telhado claro, 1 a 3 andares com janelas e o térreo com porta/vitrine e toldo colorido.
    Tudo do pacote (Floor_Modular e Shop_Tent), repintado em tons claros."""
    import random as _r
    r = _r.Random(semente)
    cor = cor or r.choice(list(CORES))
    n = andares if andares is not None else r.choice((1, 2, 2, 3))
    venez = r.random() < 0.6 if venez is None else venez
    m, s = CORES[cor]
    andar = creme(abre(MOD + f'Middle_Floor_{r.choice(ANDARES)}.png'), m, s)
    if venez:
        andar = veneziana(andar)
    terreo = creme(abre(MOD + f'Ground_Floor_Condo_{r.choice(TERREOS)}.png'), m, s)
    teto = _telhado(r.choice(TETOS), fundo)
    img = Image.new('RGBA', (112, fundo + 48 * n + 48), (0, 0, 0, 0))
    img.alpha_composite(teto, (0, 0))
    for k in range(n):
        img.alpha_composite(andar, (0, fundo + 48 * k))
    img.alpha_composite(terreo, (0, fundo + 48 * n))
    if toldo:
        t = abre(os.path.join(PACOTE, 'ME_Theme_Sorter_16x16', '4_Generic_Building_Singles_16x16',
                              f'ME_Singles_Generic_Building_16x16_Shop_Tent_{r.choice((1, 2, 3, 4))}.png'))
        img.alpha_composite(t, (r.choice((4, 16, 28)), fundo + 48 * n + 2))
    return img


def torre_vermelha():
    """Condomínio Edifício Eulálio Pinto (quarteirão do Subway): torre alta vermelha e bege com várias lojas no térreo,
    marquise de granito. Andares do pacote empilhados e repintados de vermelho-terracota."""
    andar = creme(abre(MOD + 'Middle_Floor_10.png'), 0.02, 0.50)
    andar2 = creme(abre(MOD + 'Middle_Floor_10.png'), 0.09, 0.30)
    lojas = creme(abre(MOD + 'Ground_Floor_Condo_9.png'), 0.08, 0.20)
    teto = _telhado(10, 24)
    n = 7
    img = Image.new('RGBA', (112, 24 + 48 * n + 10 + 48), (0, 0, 0, 0))
    img.alpha_composite(teto, (0, 0))
    for k in range(n):
        faixa = Image.new('RGBA', (112, 48), (0, 0, 0, 0))
        faixa.alpha_composite(andar.crop((0, 0, 72, 48)), (0, 0))
        faixa.alpha_composite(andar2.crop((72, 0, 112, 48)), (72, 0))  # parte bege do lado
        img.alpha_composite(faixa, (0, 24 + 48 * k))
    d = ImageDraw.Draw(img)
    y = 24 + 48 * n
    d.rectangle((0, y, 111, y + 9), fill=(150, 136, 122, 255))  # marquise de granito
    d.line((0, y + 9, 111, y + 9), fill=(84, 80, 92, 255))
    img.alpha_composite(lojas, (0, y + 10))
    for x0, cor in ((6, (60, 150, 70, 255)), (44, (230, 200, 40, 255)), (80, (200, 60, 60, 255))):  # lojinhas
        d.rectangle((x0, y + 12, x0 + 24, y + 16), fill=cor)
    return img


def hotel_centenario():
    """Hotel Centenário (foto do Pedro): prédio antigo rosado de 3 andares com venezianas brancas, beirais brancos e
    comércio no térreo, na esquina antes do Café do Vadinho."""
    andar = veneziana(creme(abre(MOD + 'Middle_Floor_2.png'), 0.03, 0.40))
    terreo = creme(abre(MOD + 'Ground_Floor_Condo_6.png'), 0.75, 0.30)  # térreo lilás (o mural da esquina)
    teto = _telhado(5, 24)
    img = Image.new('RGBA', (112, 24 + 48 * 3 + 48), (0, 0, 0, 0))
    img.alpha_composite(teto, (0, 0))
    d = ImageDraw.Draw(img)
    for k in range(3):
        img.alpha_composite(andar, (0, 24 + 48 * k))
        d.line((0, 24 + 48 * k + 47, 111, 24 + 48 * k + 47), fill=(246, 244, 240, 255))  # beiral branco
    img.alpha_composite(terreo, (0, 24 + 48 * 3))
    return img


def forum_civel():
    """Fórum Cível (foto do Pedro): prédio moderno branco, vidraças e a faixa azul com o nome."""
    andar = creme(abre(MOD + 'Middle_Floor_13.png'), 0.60, 0.04)
    terreo = creme(abre(MOD + 'Ground_Floor_Condo_5.png'), 0.60, 0.04)
    teto = _telhado(10, 22)
    img = Image.new('RGBA', (112, 22 + 48 + 8 + 48), (0, 0, 0, 0))
    img.alpha_composite(teto, (0, 0))
    img.alpha_composite(andar, (0, 22))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 70, 111, 77), fill=(52, 110, 220, 255))  # faixa azul
    d.line((0, 77, 111, 77), fill=(30, 60, 140, 255))
    d.rectangle((44, 72, 67, 75), fill=(240, 240, 240, 255))  # plaquinha "Fórum Cível"
    img.alpha_composite(terreo, (0, 78))
    return img


def concha90():
    """Concha acústica girada 90° (a abertura virada para o leste, à direita): vista do sul, aparece o perfil da
    cúpula, alta na abertura e baixando para trás (oeste), sobre a plataforma. Desenho próprio, em fatias de norte
    para sul."""
    a0, H0, D, esp = 22, 36, 64, 4
    K = 0.5  # quanto o norte-sul "sobe" na tela (vista de cima em 3/4)
    W, Ht = D + 30, int(H0 + 2 * a0 * K + 30)
    img = Image.new('RGBA', (W, Ht), (0, 0, 0, 0))
    px = img.load()
    cx, cy = D + 14, Ht - 6 - int(a0 * K)

    def pinta(x, y, cor):
        if 0 <= x < W and 0 <= y < Ht:
            px[x, y] = cor

    def perfil(v):
        k = max(0.0, 1 - (v / D) ** 2) ** 0.5
        return max(1.0, a0 * (0.6 + 0.4 * k)), H0 * k

    # plataforma (laje de concreto)
    for u in range(-a0 - 6, a0 + 7):
        for v in range(-6, D + 4):
            x, y = cx - v, int(cy + u * K)
            for h in (0, 1, 2):
                pinta(x, y - h, (204, 202, 196, 255) if h == 2 else (164, 160, 152, 255))
    # cúpula: fatias de norte (u negativo, longe) para sul (perto)
    for u10 in range(-a0 * 2, a0 * 2 + 1):
        u = u10 / 2
        for v in range(D, -1, -1):
            a, H = perfil(v)
            if abs(u) > a:
                continue
            fora = H * max(0.0, 1 - (u / a) ** 2) ** 0.5
            for h in range(0, int(fora) + 1):
                luz = 0.80 + 0.20 * (h / H0) + (0.06 if u > 0 else 0)
                c = min(250, int(236 * luz))
                pinta(cx - v, int(cy + u * K) - h - 2, (c, c - 3, c - 9, 255))
    # borda da abertura (vista de lado: uma faixa clara) e um pouco do interior em sombra
    for u10 in range(-a0 * 2, a0 * 2 + 1):
        u = u10 / 2
        fora = H0 * max(0.0, 1 - (u / a0) ** 2) ** 0.5
        dentro = (H0 - esp) * max(0.0, 1 - (u / (a0 - esp)) ** 2) ** 0.5 if abs(u) < a0 - esp else 0
        for h in range(int(dentro), int(fora) + 1):
            for dx in (0, 1):
                pinta(cx + dx, int(cy + u * K) - h - 2, (252, 250, 244, 255))
        if u > 0:
            for h in range(2, int(dentro)):
                pinta(cx + 1, int(cy + u * K) - h - 2, (150, 146, 138, 255))
    img = img.crop(img.getbbox())
    pad = Image.new('RGBA', (img.width + 2, img.height + 2), (0, 0, 0, 0))
    pad.alpha_composite(img, (1, 1))
    return contorno(pad)


def busto90():
    """Busto de Theodomiro Santiago sobre pedestal alto de pedra clara (a placa fica do lado da praça). O rosto é o
    desenho próprio do projeto, de frente (para virar de perfil precisa de um desenho novo)."""
    f = abre(os.path.join(RAIZ, 'public', 'assets', 'cenario', 'fonte.png'))
    cabeca = f.crop((68, 0, 104, 44))
    pedra = f.getpixel((63, 52))
    clara = tuple(min(255, int(c * 1.08)) for c in pedra[:3]) + (255,)
    ped = Image.new('RGBA', (28, 44), pedra)
    d = ImageDraw.Draw(ped)
    d.rectangle((0, 0, 27, 4), fill=clara)
    d.rectangle((0, 39, 27, 43), fill=clara)
    d.rectangle((22, 5, 27, 38), fill=escurecer(Image.new('RGBA', (1, 1), pedra), 0.88).getpixel((0, 0)))
    img = Image.new('RGBA', (cabeca.width, cabeca.height + ped.height - 8), (0, 0, 0, 0))
    img.alpha_composite(ped, ((cabeca.width - ped.width) // 2, img.height - ped.height))
    img.alpha_composite(cabeca, (0, 0))
    return contorno(img)


def _fonte():
    return abre(os.path.join(RAIZ, 'public', 'assets', 'cenario', 'fonte.png'))


def jato():
    """Jato d'água em arco, recortado da fonte da praça (arte própria do projeto): só os pixels de água."""
    f = _fonte()
    reg = f.crop((10, 60, 64, 96))
    px = reg.load()
    for y in range(reg.height):
        for x in range(reg.width):
            r, g, b, a = px[x, y]
            agua = a and (b > r + 25 or (r > 225 and g > 225 and b > 225))
            if not agua:
                px[x, y] = (0, 0, 0, 0)
    reg = reg.crop(reg.getbbox())
    out = Image.new('RGBA', (reg.width * 2, reg.height), (0, 0, 0, 0))
    out.alpha_composite(reg, (0, 0))
    out.alpha_composite(reg.transpose(Image.FLIP_LEFT_RIGHT), (reg.width, 0))
    return out


def busto_perfil():
    """Busto de Theodomiro Santiago de perfil, virado para o leste (direita), sobre pedestal de pedra clara. Desenho
    próprio, com as cores de bronze do busto original (public/assets/cenario/fonte.png)."""
    f = _fonte()
    esc, med, cla, luz = f.getpixel((80, 30)), f.getpixel((86, 20)), f.getpixel((84, 12)), f.getpixel((90, 10))
    pedra = f.getpixel((63, 52))
    pclara = tuple(min(255, int(c * 1.08)) for c in pedra[:3]) + (255,)
    W, H = 30, 46
    img = Image.new('RGBA', (W, H + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # ombros e peito (de lado: mais estreitos), peito avança para a direita
    d.polygon([(5, 30), (8, 25), (19, 24), (25, 28), (26, 40), (4, 40)], fill=med)
    d.polygon([(19, 24), (25, 28), (26, 40), (20, 40)], fill=cla)  # frente iluminada
    d.line((12, 28, 13, 40), fill=esc)  # dobra do paletó
    # pescoço
    d.rectangle((12, 19, 18, 25), fill=med)
    # cabeça: oval, nuca à esquerda, rosto à direita
    d.ellipse((7, 2, 24, 22), fill=med)
    d.ellipse((13, 4, 24, 21), fill=cla)  # lado do rosto com luz
    d.polygon([(23, 10), (27, 13), (23, 15)], fill=cla)  # nariz
    d.point((26, 13), fill=luz)
    d.line((21, 18, 23, 19), fill=esc)  # boca/queixo
    d.polygon([(19, 20), (23, 19), (21, 22)], fill=med)  # queixo
    d.point((20, 9), fill=esc)  # olho
    d.line((19, 8, 21, 8), fill=esc)  # sobrancelha
    d.ellipse((11, 9, 14, 14), fill=esc)  # orelha
    d.point((12, 11), fill=med)
    # cabelo ondulado em cima e na nuca
    d.chord((7, 1, 23, 12), 180, 360, fill=esc)
    for x in (9, 12, 15, 18, 21):
        d.point((x, 3), fill=med)
    d.polygon([(7, 8), (10, 6), (10, 17), (8, 16)], fill=esc)
    img = contorno(img, (34, 40, 36, 255))
    # pedestal alto (a placa fica no lado leste, de frente para a praça)
    ped = Image.new('RGBA', (24, 40), pedra)
    dp = ImageDraw.Draw(ped)
    dp.rectangle((0, 0, 23, 4), fill=pclara)
    dp.rectangle((0, 35, 23, 39), fill=pclara)
    dp.rectangle((18, 5, 23, 34), fill=tuple(int(c * 0.9) for c in pedra[:3]) + (255,))
    dp.rectangle((21, 12, 23, 24), fill=f.getpixel((80, 62)))  # beirada da placa de bronze, do lado da praça
    out = Image.new('RGBA', (W + 2, H + 38), (0, 0, 0, 0))
    out.alpha_composite(ped, (3, H - 4))
    out.alpha_composite(img.crop((0, 0, W, H)), (1, 0))
    return contorno(out.crop(out.getbbox()))


def five_stars():
    """Five Stars, bar com telão (a "arena esportiva"), fotos do Pedro: sobrado antigo amarelo, térreo branco com a
    parte de baixo vermelha, toldo vinho com o letreiro amarelo e mesinhas com cadeiras amarelas na calçada."""
    andar = creme(abre(MOD + 'Middle_Floor_16.png'), 0.14, 0.62)
    terreo = creme(abre(MOD + 'Ground_Floor_Condo_12.png'), 0.60, 0.04)
    teto = _telhado(7, 22)
    W = 112
    img = Image.new('RGBA', (W, 22 + 48 + 48 + 22), (0, 0, 0, 0))
    img.alpha_composite(teto, (0, 0))
    img.alpha_composite(andar, (0, 22))
    img.alpha_composite(terreo, (0, 70))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 102, W - 1, 117), fill=(196, 40, 56, 255))  # parte de baixo vermelha
    d.line((0, 102, W - 1, 102), fill=(232, 226, 214, 255))
    for x in range(0, W, 16):
        d.line((x, 103, x, 117), fill=(170, 30, 46, 255))
    # toldo vinho com o letreiro amarelo
    d.rectangle((0, 70, W - 1, 82), fill=(138, 30, 52, 255))
    d.line((0, 83, W - 1, 83), fill=(96, 20, 36, 255))
    LET = {'F': ['111', '100', '110', '100', '100'], 'I': ['1', '1', '1', '1', '1'], 'V': ['101', '101', '101', '101', '010'],
           'E': ['111', '100', '110', '100', '111'], 'S': ['111', '100', '111', '001', '111'], 'T': ['111', '010', '010', '010', '010'],
           'A': ['010', '101', '111', '101', '101'], 'R': ['110', '101', '110', '101', '101'], ' ': ['00', '00', '00', '00', '00']}
    txt = 'FIVE STARS'
    larg = sum(len(LET[c][0]) + 1 for c in txt) - 1
    x = W // 2 - larg // 2
    for c in txt:
        for j, lin in enumerate(LET[c]):
            for i, v in enumerate(lin):
                if v == '1':
                    img.putpixel((x + i, 74 + j), (250, 200, 40, 255))
        x += len(LET[c][0]) + 1
    # telão (TV grande) aparecendo pela porta
    d.rectangle((70, 88, 92, 100), fill=(30, 34, 44, 255))
    d.rectangle((72, 90, 90, 98), fill=(70, 160, 90, 255))  # campo de futebol na tela
    d.line((81, 90, 81, 98), fill=(230, 240, 230, 255))
    # mesinhas e cadeiras amarelas na calçada
    for mx in (10, 40):
        d.rectangle((mx, 124, mx + 14, 128), fill=(176, 120, 64, 255))
        d.line((mx + 2, 129, mx + 2, 133), fill=(120, 80, 40, 255))
        d.line((mx + 12, 129, mx + 12, 133), fill=(120, 80, 40, 255))
        for cx in (mx - 5, mx + 16):
            d.rectangle((cx, 125, cx + 3, 133), fill=(250, 204, 40, 255))
    return img


def _tema(rel):
    return abre(os.path.join(PACOTE, 'ME_Theme_Sorter_16x16', rel))


def palmeira_imperial(altura=176, semente=0):
    """Palmeira-imperial (fotos do Pedro): tronco reto e bem alto, com anéis discretos e o lado da sombra
    mais escuro, nos tons de marrom do tronco da palmeira do pacote; logo abaixo da copa, o trecho verde liso
    (palmito). Copa da palmeira do pacote; tronco desenhado."""
    p = _tema('14_Swimming_Pool_Singles_16x16/ME_Singles_Swimming_Pool_16x16_Palm_1.png')
    copa = p.crop((0, 0, 64, 46))
    # tira o pedacinho laranja do tronco original que aparece por baixo da copa
    cp = copa.load()
    for y in range(30, 46):
        for x in range(64):
            r, g, b, a = cp[x, y]
            if a and r > g + 25:
                cp[x, y] = (0, 0, 0, 0)
    img = Image.new('RGBA', (64, altura), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x0, x1 = 28, 35  # tronco de 8 px
    CONTORNO = (58, 58, 80, 255)  # contorno do pacote
    for y in range(36, altura - 4):
        palmito = y < 54
        if palmito:
            cores = [(96, 140, 70), (122, 168, 86), (140, 184, 98), (122, 168, 86), (110, 156, 78), (96, 140, 70)]
        elif (y % 9) == 0:  # anel: tons um passo mais escuros
            cores = [(107, 80, 82), (126, 97, 81), (168, 95, 70), (181, 117, 77), (168, 95, 70), (107, 80, 82)]
        else:  # marrom do próprio tronco da palmeira do pacote (sombra à esquerda, luz à direita do meio)
            cores = [(126, 97, 81), (168, 95, 70), (181, 117, 77), (199, 140, 89), (181, 117, 77), (126, 97, 81)]
        for i, c in enumerate(cores):
            img.putpixel((x0 + 1 + i, y), c + (255,))
        img.putpixel((x0, y), CONTORNO)
        img.putpixel((x1, y), CONTORNO)
    d.line((x0 + 1, 54, x1 - 1, 54), fill=(86, 120, 62, 255))  # fim do palmito
    # pé do tronco um pouco mais largo e escuro, com a sombra no chão
    d.ellipse((22, altura - 7, 42, altura - 1), fill=(0, 0, 0, 60))
    d.rectangle((x0 - 1, altura - 8, x1 + 1, altura - 3), fill=(126, 97, 81, 255))
    d.line((x0 - 1, altura - 8, x0 - 1, altura - 3), fill=CONTORNO)
    d.line((x1 + 1, altura - 8, x1 + 1, altura - 3), fill=CONTORNO)
    img.alpha_composite(copa, (0, 0))
    return img


def arvore_alta(semente=0, extra=34):
    """Árvore de praça alta e rala (como as da praça real): copa da árvore do pacote com falhas entre as folhas e
    tronco bem mais comprido, para a copa ficar lá no alto."""
    import random as _r
    r = _r.Random(semente)
    t = _tema('7_Villas_Singles_16x16/ME_Singles_Villas_16x16_Tree_3.png')
    copa = t.crop((0, 0, 80, 46)).copy()
    px = copa.load()
    # falhas na copa: tira manchas de folhas por dentro, sem mexer na borda (fica mais rala)
    for _ in range(9):
        cx, cy, rr = r.randint(16, 62), r.randint(10, 34), r.randint(3, 5)
        for y in range(cy - rr, cy + rr + 1):
            for x in range(cx - rr, cx + rr + 1):
                if 0 <= x < 80 and 0 <= y < 46 and (x - cx) ** 2 + (y - cy) ** 2 <= rr * rr:
                    viz = [px[min(79, max(0, x + dx)), min(45, max(0, y + dy))][3] for dx in (-3, 3) for dy in (-3, 3)]
                    if all(viz):
                        px[x, y] = (0, 0, 0, 0)
    tronco = t.crop((37, 47, 46, 48))  # só o tronco (sem as folhas que caem do lado)
    base = t.crop((30, 53, 53, 64))  # pé do tronco com a gramínea
    img = Image.new('RGBA', (80, 46 + extra + base.height), (0, 0, 0, 0))
    for y in range(40, img.height - base.height + 1):
        img.alpha_composite(tronco, (37, y))
    img.alpha_composite(base, (30, img.height - base.height))
    img.alpha_composite(copa, (0, 0))
    return img.crop(img.getbbox())


def busto_pequeno():
    """Busto de Theodomiro Santiago, pequeno, de perfil (olhando para o leste), num pedestal fino: fica dentro do
    espelho d'água, como na foto. Cores de bronze do busto original."""
    f = _fonte()
    esc, med, cla = f.getpixel((80, 30)), f.getpixel((86, 20)), f.getpixel((84, 12))
    pedra = f.getpixel((63, 52))
    img = Image.new('RGBA', (14, 34), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(2, 14), (4, 11), (10, 11), (12, 14), (12, 17), (2, 17)], fill=med)  # ombros
    d.rectangle((9, 11, 12, 17), fill=cla)
    d.rectangle((6, 8, 9, 11), fill=med)  # pescoço
    d.ellipse((3, 1, 11, 10), fill=med)  # cabeça
    d.ellipse((6, 2, 11, 9), fill=cla)
    d.point((12, 5), fill=cla)  # nariz
    d.chord((3, 0, 11, 6), 180, 360, fill=esc)  # cabelo
    d.point((5, 5), fill=esc)  # orelha
    d.rectangle((4, 17, 10, 33), fill=pedra)  # pedestal fino
    d.rectangle((3, 17, 11, 19), fill=tuple(min(255, int(c * 1.08)) for c in pedra[:3]) + (255,))
    d.rectangle((9, 20, 10, 33), fill=tuple(int(c * 0.88) for c in pedra[:3]) + (255,))
    pad = Image.new('RGBA', (16, 36), (0, 0, 0, 0))
    pad.alpha_composite(img, (1, 1))
    return contorno(pad, (34, 40, 36, 255))


def jatos_espelho(largura, profundidade):
    """Jatos da fonte (foto do Pedro): arcos d'água das duas bordas em direção ao meio (os arcos da fonte original do
    projeto, que se leem bem vistos de lado) e uma fileira de jatinhos retos no centro."""
    arco = jato()
    pico = arco.height
    img = Image.new('RGBA', (largura, profundidade + pico), (0, 0, 0, 0))
    meio = pico + profundidade // 2
    img.alpha_composite(arco, ((largura - arco.width) // 2, meio - arco.height + 4))
    px = img.load()
    for x in range((largura - arco.width) // 2 + 30, (largura + arco.width) // 2 - 30, 7):  # jatinhos retos
        for h in range(0, 10):
            px[x, meio - h] = (250, 252, 255, 240) if h % 3 else (196, 226, 255, 230)
        for dx in (-1, 1):
            px[x + dx, meio] = (196, 226, 255, 230)
    return img
