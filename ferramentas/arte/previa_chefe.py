"""Prévia da Fase 3 (Resgate): a Tia Paula precisa ser VISTA dentro da gaiola.

Uso: python3 ferramentas/arte/previa_chefe.py [repo]
Saída (só prévia; nada em src/): ferramentas/arte/previas/chefe/
  gaiola-atual-x-nova.png   gaiola de hoje × gaiola nova (fechada, com a Tia Paula; aberta), 5x
  chefe-telas.png           2 telas do jogo (480x270, 2x): durante a luta e na vitória

Por que a de hoje não funciona: a gaiola tem 40x56 com grades douradas grossas e juntas (a cada 3 px), e a Tia
Paula provisória (48 px) fica atrás delas, quase toda coberta, contra o céu escuro.

Proposta:
- gaiola maior (64x96) para a Tia Paula nova (57 px) caber inteira, de pé;
- grades em 2 camadas: as de TRÁS escuras e finas, as da FRENTE só 5, finas, com 9 px de vão entre elas;
- a Tia Paula fica ENTRE as duas camadas e na frente de um brilho lilás (o feitiço do Jafar), que a destaca
  do céu da noite;
- pose "socorro" (mãos nas grades, boca aberta) + balão "Socorro!" já existente;
- pendurada no alto à direita (como hoje), abaixo do HUD e longe dos botões PULAR e MAÇÃ;
- na vitória, a portinha abre para o lado e o brilho some.
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerar_lugares as GL  # noqa: E402
from cenario import M, Tela  # noqa: E402
import elenco_proposta as EP  # noqa: E402
from previa_elenco import carregar_sprites, quadro_img  # noqa: E402

REPO = GL.REPO
SAIDA = os.path.join(REPO, 'ferramentas', 'arte', 'previas', 'chefe')
L_T, A_T = 480, 270
GL_, GA = 64, 96          # quadro da gaiola nova
BASE_G = 88               # linha do piso da gaiola dentro do quadro


def recortar(im):
    return im.crop(im.getbbox())


def brilho():
    """Brilho do feitiço atrás da Tia Paula: elipse em 3 faixas de lilás (sem degradê)."""
    im = Image.new('RGBA', (GL_, GA), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = GL_ // 2, 58
    for rx, ry, cor in ((24, 31, '#4E4290'), (20, 27, '#6A5AB4'), (15, 22, '#8C7AD6'), (9, 15, '#AE9EEC')):
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=cor)
    return im


def gaiola(parte, aberta=False):
    """parte='tras' (grades de trás, cúpula) ou 'frente' (grades da frente, anéis, piso, cadeado)."""
    t = Tela(GL_, GA, semente=9)
    ou = M['dourado']
    cx = GL_ / 2
    x0, x1 = 7, GL_ - 8
    topo = 26
    if parte == 'tras':
        # cúpula (metade de trás) e argola
        t.elipse(cx, 6, 3, 3, ou, 2)
        t.elipse(cx, 6, 1.4, 1.4, ou, 4)
        t.vlinha(int(cx), 9, 12, ou, 3)
        for k in range(-3, 4):   # costelas da cúpula
            xa = cx + k * 7.5
            for i in range(15):
                s = i / 14
                x = cx + (xa - cx) * math.sin(s * math.pi / 2)
                y = 12 + (topo - 12) * s ** 1.6
                t.px(x, y, ou, 3)
        # grades de trás (escuras, finas, a cada 6 px)
        for x in range(x0 + 3, x1 - 1, 6):
            t.vlinha(x, topo, BASE_G - 1, ou, 4)
        t.hlinha(x0, x1, topo + 1, ou, 4)
        t.hlinha(x0, x1, 58, ou, 4)
        t.contorno()
        return t.imagem()
    # --- frente ---
    # anel de cima (aro grosso), anel do meio fino, piso
    t.ret(x0 - 1, topo - 1, x1 + 1, topo + 1, ou, 1)
    t.hlinha(x0 - 1, x1 + 1, topo - 1, ou, 0)
    t.hlinha(x0 - 1, x1 + 1, topo + 1, ou, 3)
    t.ret(x0 - 3, BASE_G, x1 + 3, BASE_G + 4, ou, 2)
    t.hlinha(x0 - 3, x1 + 3, BASE_G, ou, 0)
    t.hlinha(x0 - 3, x1 + 3, BASE_G + 4, ou, 4)
    for x in range(x0, x1 + 1, 6):
        t.px(x, BASE_G + 2, ou, 3)            # rebites do piso
    t.poli([(cx - 6, BASE_G + 5), (cx + 6, BASE_G + 5), (cx + 2, BASE_G + 8), (cx - 2, BASE_G + 8)], ou, 3)  # ponteira
    # grades da frente: só nas bordas e 3 no meio, finas (1 px) com brilho
    porta_x0, porta_x1 = int(cx - 12), int(cx + 12)   # vão de 23 px: o rosto e o corpo dela ficam livres
    grades = [x0, x0 + 6, x1 - 6, x1]
    if not aberta:
        grades += [porta_x0, porta_x1]
    for x in grades:
        t.vlinha(x, topo + 2, BASE_G - 1, ou, 2)
        t.vlinha(x - 1 if x > x0 else x + 1, topo + 2, BASE_G - 1, ou, 0 if x < cx else 3)
    if not aberta:
        # porta fechada: 2 barras finas (1 px) no vão da frente, para a gaiola não parecer aberta durante a luta;
        # entre elas (7 px) o rosto e o corpo da Tia Paula continuam à vista
        for x in (int(cx - 4), int(cx + 4)):
            t.vlinha(x, topo + 2, BASE_G - 1, ou, 1)
    if not aberta:
        # anel do meio só nas laterais (não passa na frente do rosto)
        t.hlinha(x0, x0 + 10, 58, ou, 1)
        t.hlinha(x1 - 10, x1, 58, ou, 1)
        # cadeado
        t.ret(porta_x1 - 2, 60, porta_x1 + 3, 66, ou, 2)
        t.relevo(t.mascara_ret(porta_x1 - 2, 60, porta_x1 + 3, 66))
        t.px(porta_x1, 63, ou, 4)
        t.linha(porta_x1 - 1, 60, porta_x1 + 2, 57, ou, 1)
    else:
        # portinha aberta, girada para a esquerda (vista de lado: grades curtas em perspectiva)
        for k, x in enumerate(range(x0 - 9, x0 - 1, 3)):
            t.vlinha(x, topo + 6 + k, BASE_G - 3 - k, ou, 2 if k % 2 else 1)
        t.linha(x0 - 9, topo + 6, x0, topo + 2, ou, 1)
        t.linha(x0 - 9, BASE_G - 3, x0, BASE_G - 1, ou, 2)
        t.hlinha(x0, x0 + 10, 58, ou, 1)
        t.hlinha(x1 - 10, x1, 58, ou, 1)
    t.contorno()
    return t.imagem()


def gaiola_com(ocupante, aberta=False):
    im = Image.new('RGBA', (GL_ + 10, GA), (0, 0, 0, 0))
    if not aberta:
        im.alpha_composite(brilho(), (10, 0))
    im.alpha_composite(gaiola('tras'), (10, 0))
    if ocupante is not None:
        o = recortar(ocupante)
        im.alpha_composite(o, (10 + GL_ // 2 - o.width // 2 + 1, BASE_G - o.height))
    im.alpha_composite(gaiola('frente', aberta), (10, 0))
    return im


def paula(pose_nome):
    tp = EP.TiaPaula()
    if pose_nome == 'socorro':
        # mãos para a frente, segurando as grades
        return tp.img(EP.respirar(1, ombro_f=85, cotovelo_f=20, ombro_t=75, cotovelo_t=25, rosto='socorro',
                                  mao_f='punho', mao_t='punho'))
    return tp.img(EP.respirar(2, ombro_f=150, cotovelo_f=10, ombro_t=145, cotovelo_t=15, rosto='feliz',
                              braco_t_atras=False))


# ---------------------------------------------------------------------------------------------------------------
# Arena (noite caindo): céu escuro, serra, terraço com arcos, chão de paralelepípedo, 2 plataformas
# ---------------------------------------------------------------------------------------------------------------

# Pôr do sol (a luta acontece quando o sol encosta na serra; em seguida o voo é no crepúsculo)
CEU_POR_DO_SOL = ['#6C64CC', '#7E72D6', '#9480DA', '#AE8AD6', '#C892CC', '#E09CBC', '#F2A8A6', '#FBB88C', '#FFC878']


def arena(completa=True):
    """completa=False: só o fundo (céu, sol, serra e terraço), sem plataformas e chão (o jogo desenha esses com tiles)."""
    a = np.zeros((A_T, L_T, 4), np.uint8)
    ceu = CEU_POR_DO_SOL
    for y in range(A_T):
        for xb in range(0, L_T, 8):
            f = y / 190 + (0.015 if (xb // 8) % 2 else 0)
            a[y, xb:xb + 8, :3] = GL.hex_rgb(ceu[min(len(ceu) - 1, int(f * len(ceu)))])
    a[:, :, 3] = 255
    img = Image.fromarray(a, 'RGBA')
    d = ImageDraw.Draw(img)
    # sol grande e baixo, encostando na serra (em faixas, sem degradê)
    sx, sy = 150, 122
    for r, cor in ((44, '#FFC890'), (36, '#FFD49A'), (28, '#FFE2A0'), (22, '#FFF0B0'), (17, '#FFF8D0')):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=cor)
    for y, x0, x1 in ((40, 300, 400), (56, 340, 460), (30, 20, 90)):   # nuvens compridas iluminadas por baixo
        d.rectangle([x0, y, x1, y + 2], fill='#F6C2C8')
        d.rectangle([x0 + 8, y + 3, x1 - 10, y + 4], fill='#FFD8A8')
    img.alpha_composite(GL.tingir(GL.morros(L_T), '#B0607A', 0.22))
    # terraço: colunas com arcos ao fundo
    t = Tela(L_T, A_T, semente=4)
    cr = M['creme']
    for i, x in enumerate(range(10, L_T, 96)):
        t.ret(x, 150, x + 12, 239, cr, 2)
        t.vlinha(x, 150, 239, cr, 1)
        t.vlinha(x + 12, 150, 239, cr, 3)
        t.ret(x - 3, 144, x + 15, 149, cr, 1)
        t.hlinha(x - 3, x + 15, 149, cr, 3)
        if x + 96 < L_T + 20:
            for k in range(84):
                s = k / 83
                yy = 146 - math.sin(s * math.pi) * 34
                t.ret(x + 12 + k, yy - 4, x + 12 + k, yy, cr, 2 if s < 0.5 else 3)
    t.ret(0, 228, L_T - 1, 239, cr, 3)   # mureta
    t.hlinha(0, L_T - 1, 228, cr, 1)
    t.reboco(0, 150, L_T - 1, 239, cr, n=12)
    t.contorno()
    img.alpha_composite(GL.tingir(t.imagem(), '#E8906A', 0.12))   # luz quente do sol baixo
    if not completa:
        return img
    # plataformas de madeira (mapa: colunas 4-8 e 20-24 na linha 11)
    p = Tela(L_T, A_T, semente=5)
    for c0 in (4, 20):
        x0, x1, y = c0 * 16, (c0 + 5) * 16 - 1, 11 * 16
        p.ret(x0, y, x1, y + 5, M['madeira'], 2)
        p.hlinha(x0, x1, y, M['madeira'], 0)
        p.hlinha(x0, x1, y + 5, M['madeira'], 4)
        for x in range(x0, x1, 8):
            p.vlinha(x, y + 1, y + 4, M['madeira'], 4)
        for x in (x0 + 4, x1 - 4):
            p.linha(x, y + 6, x + (6 if x < (x0 + x1) / 2 else -6), y + 12, M['madeira'], 3)
    p.contorno()
    img.alpha_composite(p.imagem())
    img.alpha_composite(GL.chao(L_T))
    return img


def corrente(img, x, y0, y1):
    d = ImageDraw.Draw(img)
    for y in range(y0, y1, 6):
        d.rectangle([x - 2, y, x + 1, y + 4], fill='#2E1A33')
        d.rectangle([x - 1, y + 1, x, y + 3], fill='#E0B440')


def estrela(img, x, y):
    d = ImageDraw.Draw(img)
    pts = []
    for k in range(10):
        r = 6 if k % 2 == 0 else 2.6
        a = -math.pi / 2 + k * math.pi / 5
        pts.append((x + r * math.cos(a), y + r * math.sin(a)))
    d.polygon(pts, fill='#FF7AD0', outline='#7A1E5E')
    d.point((x, y), fill='#FFFFFF')


def botoes(img):
    """Marca onde ficam os botões de toque (semitransparentes), para conferir que não cobrem a gaiola."""
    cam = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(cam)
    for cx, cy, r, txt in ((40, 232, 22, '<'), (96, 232, 22, '>'), (440, 226, 28, 'PULAR'), (380, 238, 18, 'MAÇÃ')):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 60), outline=(255, 255, 255, 140))
    img.alpha_composite(cam)


def tela(vitoria=False):
    img = arena()
    gx, gtopo = 404, 30   # gaiola pendurada no alto à direita, abaixo do HUD
    corrente(img, gx + 10 + GL_ // 2, 0, gtopo + 4)
    if vitoria:
        img.alpha_composite(gaiola_com(None, aberta=True), (gx, gtopo))
        img.alpha_composite(recortar(paula('feliz')), (372, 240 - recortar(paula('feliz')).height))
    else:
        img.alpha_composite(gaiola_com(paula('socorro')), (gx, gtopo))
        d = ImageDraw.Draw(img)   # balão "Socorro!"
        d.rounded_rectangle([360, 34, 404, 48], 4, fill='#FFFFFF', outline='#6D6BD9')
        d.polygon([(398, 48), (406, 52), (400, 46)], fill='#FFFFFF')
        GL.rotulo(d, (364, 36), 'Socorro!', 9, (109, 107, 217), True)
    jf = EP.Jafar()
    if vitoria:
        d = ImageDraw.Draw(img)
        for k, (x, y, r) in enumerate(((230, 110, 16), (214, 120, 11), (248, 122, 12), (232, 96, 9))):
            d.ellipse([x - r, y - r, x + r, y + r], fill=['#E8D8FF', '#C0A8F0', '#C0A8F0', '#FFFFFF'][k])
    else:
        j = recortar(jf.img(EP.pose(ombro_f=150, cotovelo_f=10, ombro_t=-30, cotovelo_t=20, rosto='bravo', fase=1.2,
                                    extra={'varinha': 170, 'brilho': 1.4})))
        img.alpha_composite(j, (200, 70))
        for dx, dy in ((-30, 66), (-44, 52), (-50, 34)):
            estrela(img, 200 + dx + 30, 70 + dy + 40)
    d = carregar_sprites()
    h = quadro_img(d['jogador']['QUADROS']['parado1'], d['jogador']['PALETA'])
    img.alpha_composite(h, (70, 240 - h.height))
    # faixa do HUD (onde ficam corações, maçãs e a barra do Jafar)
    hud = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(hud).rectangle([0, 0, L_T, 22], fill=(158, 158, 255, 70))
    img.alpha_composite(hud)
    botoes(img)
    return img


def gaiola_atual():
    d = carregar_sprites()
    ch = d['chefe']
    g = quadro_img(ch['SPRITES']['gaiola']['quadros'][0], ch['PALETA'])
    p = quadro_img(ch['SPRITES']['tiaPaula']['quadros'][0], ch['PALETA'])
    im = Image.new('RGBA', (g.width + 4, max(g.height, p.height) + 2), (0, 0, 0, 0))
    im.alpha_composite(p, ((im.width - p.width) // 2, im.height - p.height - 6))
    im.alpha_composite(g, (2, im.height - g.height))
    return im


def main():
    os.makedirs(SAIDA, exist_ok=True)
    k = 5
    fundo_cor = (232, 156, 188, 255)
    itens = [('hoje no jogo', gaiola_atual()), ('nova: fechada (luta)', gaiola_com(paula('socorro'))),
             ('nova: aberta (vitória)', gaiola_com(None, aberta=True))]
    W = sum(i.width * k + 40 for _, i in itens) + 40
    H = max(i.height for _, i in itens) * k + 150
    out = Image.new('RGBA', (W, H), (34, 26, 48, 255))
    dr = ImageDraw.Draw(out)
    GL.rotulo(dr, (20, 14), 'Gaiola da Tia Paula: hoje × proposta (ampliado 5×, sobre o céu do pôr do sol)', 24)
    x = 30
    for rot, im in itens:
        f = Image.new('RGBA', im.size, fundo_cor)
        f.alpha_composite(im)
        g = f.resize((im.width * k, im.height * k), Image.NEAREST)
        out.alpha_composite(g, (x, 60))
        GL.rotulo(dr, (x, 70 + g.height), rot, 18, (255, 214, 251))
        x += g.width + 40
    out.save(os.path.join(SAIDA, 'gaiola-atual-x-nova.png'))
    # telas
    k = 2
    t1, t2 = tela(False), tela(True)
    W = 2 * L_T * k + 48
    out = Image.new('RGBA', (W, A_T * k + 110), (34, 26, 48, 255))
    dr = ImageDraw.Draw(out)
    GL.rotulo(dr, (16, 14), 'Fase 3 · Resgate (480×270, ampliado 2×). Faixa lilás = HUD; círculos = botões de toque',
              22)
    for i, (rot, im) in enumerate((('Durante a luta: Tia Paula visível na gaiola', t1),
                                   ('Vitória: a portinha abre e ela desce', t2))):
        X = 16 + i * (L_T * k + 16)
        GL.rotulo(dr, (X, 52), rot, 20, (255, 214, 251))
        out.alpha_composite(im.resize((L_T * k, A_T * k), Image.NEAREST), (X, 90))
    out.save(os.path.join(SAIDA, 'chefe-telas.png'))
    print('ok', SAIDA)


if __name__ == '__main__':
    main()
