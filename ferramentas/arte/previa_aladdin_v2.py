"""Prévia: Aladdin versão 2 ("linha B"), o mais próximo possível da LINGUAGEM do Aladdin do SNES sem o design
da Disney (regra 3).

Uso: python3 ferramentas/arte/previa_aladdin_v2.py [repo] [pasta_dos_sheets_snes]
Saída (só prévia; nada em src/): ferramentas/arte/previas/aladdin-v2/
  aladdin-v1-x-v2.png       herói de hoje × versão 2 × silhueta de referência (cinza), mesma escala, 6x
  aladdin-v2-quadros.png    todos os quadros da versão 2 (4x)
  aladdin-v2-*.gif          animações (parado com piscada, corrida, pulo completo, arremesso), 4x

O que muda em relação ao herói de hoje (gerar_jogador.py, que continua sendo a base: mesmo esqueleto, mesma luz,
mesmas poses):
- ROUPA no estilo do gênero (mil e uma noites), nas cores da escola: colete VERDE aberto com debrum dourado sobre o
  peito, calça LARGA de pano LILÁS franzida no tornozelo, faixa ROSA larga na cintura, faixa rosa na cabeça.
  Fica de fora o que é da Disney: colete roxo, calça bufante branca, fez vermelho;
- calça que ESVOAÇA (volume que vai para trás na corrida e infla no pulo), como o pano nas capturas;
- quadros novos: piscada no parado e aterrissagem (corpo amassa ao tocar o chão).
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerar_jogador as GJ  # noqa: E402
from modelo import Boneco, Material, paleta_de, ponto, mistura  # noqa: E402

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', '..'))
REF = sys.argv[2] if len(sys.argv) > 2 else os.path.join(REPO, 'references', 'estilo', 'sprites-spritedatabase',
                                                         'aladdin-snes')
SAIDA = os.path.join(REPO, 'ferramentas', 'arte', 'previas', 'aladdin-v2')
L, A = GJ.L, GJ.A

PELE, CABELO, FAIXA, COURO, OURO = GJ.PELE, GJ.CABELO, GJ.FAIXA, GJ.COURO, GJ.OURO
COLETE = Material('colete', 'GgfFE', ['#A9E482', '#6CC24A', '#3F8C3A', '#285E2E', '#173A20'], (0.80, 0.45, 0.14))
CALCA = Material('calca', 'CcbBN', ['#C8C6FF', '#9E9EFF', '#7C7AE6', '#5654C0', '#2C2A74'], (0.88, 0.55, 0.20))
MATERIAIS = [PELE, CABELO, COLETE, FAIXA, CALCA, COURO, OURO]
PALETA = paleta_de(MATERIAIS, GJ.EXTRAS)


def desenhar(p):
    b = Boneco(L, A)
    hx, hy = p['hx'], p['hy']
    incl = p['tronco']
    vento = p['vento']
    pescoco = ponto((hx, hy), GJ.COLUNA, 180 - incl)
    peito = mistura((hx, hy), pescoco, 0.68)
    cab = ponto(pescoco, 6.6, 180 - incl * 0.6 - p['cabeca'])
    cab = (cab[0] + 0.6, cab[1])
    ombro_t = (pescoco[0] + 1.8, pescoco[1] + 2.4)
    ombro_f = (pescoco[0] - 2.0, pescoco[1] + 2.8)
    quadril_t = (hx + 1.6, hy)
    quadril_f = (hx - 1.2, hy + 0.4)

    def braco(ombro, ang, dobra, esc, mao_tipo, bracelete):
        cot = ponto(ombro, GJ.BRACO, ang)
        mao = ponto(cot, GJ.ANTEBRACO, ang + dobra)
        b.capsula(ombro, cot, 2.0, 1.75, PELE, esc)
        b.capsula(cot, mao, 1.75, 1.45, PELE, esc)
        m2 = ponto(mao, 1.2, ang + dobra)
        if mao_tipo == 'punho':
            b.elipse(m2, 2.1, 2.1, PELE, esc)
        else:
            b.elipse(m2, 1.9, 2.3, PELE, esc, giro=-(ang + dobra))
        if bracelete:
            pb = mistura(cot, mao, 0.75)
            b.capsula(ponto(pb, 0.8, ang + dobra - 90), ponto(pb, 0.8, ang + dobra + 90), 1.1, 1.1, OURO, esc)

    def perna(quadril, coxa, joelho, pe_ang, esc):
        j, t, ang_pe = GJ.junta_perna(quadril, coxa, joelho, pe_ang)
        # calça larga: coxa e canela grossas, e o pano "atrasa" (vai para trás) com o vento
        atras = ponto(mistura(j, t, 0.45), 1.2 + 2.2 * vento, -90)
        b.capsula(quadril, j, 4.4, 4.0, CALCA, esc, achatar=0.9)
        b.capsula(j, atras, 4.0, 4.2, CALCA, esc, achatar=0.9)
        b.capsula(atras, t, 4.2, 2.6, CALCA, esc, achatar=0.9)
        # barra franzida no tornozelo (punho rosa)
        b.capsula(ponto(t, 0.8, coxa - joelho + 180), t, 2.6, 2.4, FAIXA, esc, pontas=False)
        # dobras do pano
        meio = mistura(j, t, 0.55)
        b.tom_em(meio[0] - 1, meio[1], CALCA, 2 + esc)
        b.tom_em(meio[0] + 1, meio[1] + 2, CALCA, 2 + esc)
        b.tom_em(j[0], j[1] + 1, CALCA, 0 if not esc else 1)
        # sandália (igual à de hoje)
        dedos = ponto(t, 5.0, ang_pe)
        sa, sb = ponto(t, 1.7, ang_pe + 90), ponto(dedos, 1.1, ang_pe + 90)
        b.capsula(ponto(sa, 1.2, ang_pe + 180), sb, 0.6, 0.6, COURO, esc + 1, separar=False)
        b.capsula(t, dedos, 1.6, 1.15, PELE, esc, achatar=0.8)
        tira = mistura(t, dedos, 0.55)
        b.capsula(ponto(tira, 1.4, ang_pe - 90), ponto(tira, 0.8, ang_pe + 90), 0.55, 0.55, COURO, esc,
                  separar=False)

    def pontas(origem, comp, larg, direcao, fase, mat, esc=0):
        pts, x, y = [origem], origem[0], origem[1]
        for i in range(4):
            a = direcao + math.sin(fase + i * 1.3) * (12 + 18 * vento) * (i + 1) / 4
            x, y = ponto((x, y), comp / 4, a)
            pts.append((x, y))
        for i in range(4):
            r0 = larg * (1 - 0.15 * i)
            b.capsula(pts[i], pts[i + 1], r0, r0 * 0.85, mat, esc)

    if p['braco_t_atras']:
        braco(ombro_t, p['ombro_t'], p['cotovelo_t'], 1, p['mao_t'], False)
    no = (hx - 4.4 - incl * 0.05, hy - 2.0)
    dirp = -8 - vento * 70
    pontas(no, 10 + vento * 3, 1.1, dirp, p['fase'], FAIXA, 1)
    pontas((no[0] + 0.5, no[1] + 0.6), 8 + vento * 2, 0.9, dirp + 12, p['fase'] + 1.7, FAIXA, 1)
    if not p['sentado']:
        perna(quadril_t, p['coxa_t'], p['joelho_t'], p['pe_t'], 1)
    perna(quadril_f, p['coxa_f'], p['joelho_f'], p['pe_f'], 0)
    if p['sentado']:
        perna(quadril_t, p['coxa_t'], p['joelho_t'], p['pe_t'], 1)
    # tronco: peito à mostra (pele) e colete verde aberto por cima
    b.capsula(peito, (hx, hy - 1.5), 4.2, 3.6, PELE, separar=False, achatar=0.92)
    b.elipse((peito[0] + 0.4, peito[1] - 0.8), 4.4, 3.2, PELE, separar=False, achatar=0.9)
    pz = pescoco
    # lado de trás do colete (mais largo, vista 3/4) e lado da frente (estreito)
    b.poligono([(pz[0] - 5.4, pz[1] + 1.2), (pz[0] - 0.2, pz[1] + 0.8), (hx - 0.6, hy - 2.6), (hx - 5.6, hy - 2.0)],
               COLETE, separar=False)
    b.poligono([(pz[0] + 2.4, pz[1] + 1.4), (pz[0] + 5.4, pz[1] + 2.6), (hx + 5.4, hy - 2.4), (hx + 3.0, hy - 3.0)],
               COLETE, separar=False)
    for a_, b_ in (((pz[0] - 0.2, pz[1] + 0.8), (hx - 0.6, hy - 2.6)), ((pz[0] + 2.4, pz[1] + 1.4), (hx + 3.0, hy - 3.0))):
        n = 10
        for i in range(n + 1):
            q = mistura(a_, b_, i / n)
            b.tom_em(q[0], q[1], OURO, 1)       # debrum dourado na abertura
    b.capsula(pescoco, (cab[0] - 0.4, cab[1] + 2.0), 2.0, 2.0, PELE, separar=False)
    # faixa larga na cintura
    fy = hy - 2.2
    b.capsula((hx - 5.0, fy + 0.4), (hx + 5.2, fy), 2.3, 2.3, FAIXA, separar=False, achatar=0.9)
    b.elipse(no, 2.0, 1.8, FAIXA, 1, separar=False)
    # cabeça (igual à de hoje: cachos, faixa rosa com pontas)
    cx, cy = cab
    for dx, dy, r in ((-3.8, -0.4, 2.7), (-4.4, 2.4, 2.4), (-3.2, 4.6, 2.0), (-1.4, -3.4, 2.5), (1.6, -3.9, 2.3),
                      (-3.8, -3.0, 2.3), (4.0, -2.8, 2.0), (-5.6, 0.8, 1.8), (-1.2, 5.4, 1.6)):
        b.elipse((cx + dx, cy + dy), r, r, CABELO, separar=False)
    b.elipse((cx + 0.8, cy + 0.6), 4.4, 4.9, PELE, separar=False, achatar=0.65)
    b.elipse((cx + 2.4, cy + 3.0), 2.6, 2.3, PELE, separar=False, achatar=0.6)
    b.elipse((cx - 1.8, cy + 1.2), 1.2, 1.7, PELE, 1, separar=False, achatar=0.8)
    for dx, dy, r in ((-0.2, -3.4, 1.9), (2.2, -3.6, 1.8), (4.2, -2.6, 1.4), (-2.4, -2.4, 1.7)):
        b.elipse((cx + dx, cy + dy), r, r * 0.9, CABELO, separar=False)
    b.capsula((cx - 0.6, cy - 1.0), (cx - 0.4, cy + 1.8), 0.8, 0.6, CABELO, separar=False)
    b.capsula((cx - 4.8, cy - 2.6), (cx + 3.4, cy - 4.4), 0.8, 0.7, FAIXA, separar=False)
    nc = (cx - 5.2, cy - 2.2)
    pontas(nc, 7 + vento * 5, 0.85, -25 - vento * 62, p['fase'] + 0.8, FAIXA, 0)
    pontas(nc, 6 + vento * 3, 0.7, -5 - vento * 60, p['fase'] + 2.4, FAIXA, 1)
    b.elipse(nc, 1.2, 1.1, FAIXA, separar=False)
    b.elipse((cx + 1.0, cy - 4.6), 1.2, 1.0, CABELO, separar=False)
    if p['braco_f_frente']:
        braco(ombro_f, p['ombro_f'], p['cotovelo_f'], 0, p['mao_f'], True)
    if not p['braco_t_atras']:
        braco(ombro_t, p['ombro_t'], p['cotovelo_t'], 0, p['mao_t'], False)
    # rosto
    if p['rosto'] == 'piscando':
        ox1, ox2, oy = cx + 1.2, cx + 4.0, cy + 0.6
        b.px(ox1, oy + 1, 'e'); b.px(ox1 + 1, oy + 1, 'e'); b.px(ox2, oy + 1, 'e')
        b.px(ox1 - 0.5, oy - 1.4, 'I'); b.px(ox1 + 0.6, oy - 1.8, 'I'); b.px(ox1 + 1.6, oy - 1.8, 'I')
        b.px(ox2, oy - 1.6, 'I'); b.px(ox2 + 1, oy - 1.4, 'I')
        b.tom_em(cx + 5.2, cy + 2.1, PELE, 2); b.tom_em(cx + 4.4, cy + 2.9, PELE, 2)
        b.px(cx + 3.0, cy + 4.4, 'q'); b.px(cx + 4.0, cy + 4.2, 'q')
        b.tom_em(cx + 0.2, cy + 5.6, PELE, 3); b.tom_em(cx + 1.2, cy + 5.9, PELE, 2)
    else:
        GJ.rosto(b, cx, cy, p['rosto'])
    b.px(cx - 1.4, cy + 3.3, 'y')
    b.tom_em(hx + 1, fy - 1, FAIXA, 0)
    return b


def aterrissagem():
    """Toca o chão: joelhos dobram, corpo baixa e inclina, braços abrem para equilibrar (amassa e estica)."""
    return GJ.pose(hy=37.0, tronco=14, cabeca=-4, coxa_f=48, joelho_f=82, pe_f=-6, coxa_t=10, joelho_t=70, pe_t=-10,
                   ombro_f=-70, cotovelo_f=30, ombro_t=70, cotovelo_t=20, vento=0.4, fase=5.0, mao_f='aberta',
                   rosto='esforco', saia=0.4)


POSES = {
    'parado1': GJ.parado(0), 'parado2': GJ.parado(1), 'parado3': GJ.parado(2), 'parado4': GJ.parado(3),
    'piscando': dict(GJ.parado(1), rosto='piscando'),
    **{f'correndo{i + 1}': GJ.correndo(i) for i in range(8)},
    'pulando1': GJ.pulando(), 'pulando2': GJ.subindo2(), 'caindo1': GJ.caindo(), 'caindo2': GJ.caindo2(),
    'aterrissando': aterrissagem(),
    'arremessando1': GJ.arremessando(0), 'arremessando2': GJ.arremessando(1), 'arremessando3': GJ.arremessando(2),
    'dano': GJ.dano(), 'sentado1': GJ.sentado(0),
}


def gerar():
    q = {n: desenhar(p).texto(GJ.CONTORNO_FIXO) for n, p in POSES.items()}

    def ultima(linhas):
        return max(y for y, l in enumerate(linhas) if any(c != '.' for c in l))
    desce = A - 1 - ultima(q['parado1'])
    for n in q:
        if desce and not n.startswith('sentado'):
            q[n] = ['.' * L] * desce + q[n][:A - desce]
    return q


def img(linhas, pal=PALETA):
    im = Image.new('RGBA', (len(linhas[0]), len(linhas)), (0, 0, 0, 0))
    for y, l in enumerate(linhas):
        for x, c in enumerate(l):
            if c != '.':
                h = pal[c].lstrip('#')
                im.putpixel((x, y), tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def fonte(t, negrito=False):
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if negrito else ''), t)


FUNDO = (158, 158, 255, 255)


def gif(nome, quadros, ms, k=4):
    fr = []
    for q in quadros:
        f = Image.new('RGBA', (L, A), FUNDO)
        f.alpha_composite(q)
        fr.append(f.resize((L * k, A * k), Image.NEAREST).convert('P', palette=Image.ADAPTIVE))
    fr[0].save(os.path.join(SAIDA, nome), save_all=True, append_images=fr[1:], duration=ms, loop=0, disposal=2)


def main():
    os.makedirs(SAIDA, exist_ok=True)
    q = {n: img(l) for n, l in gerar().items()}
    atual = {n: img(l, GJ.PALETA) for n, l in GJ.gerar().items()}
    # 1. v1 × v2 × silhueta de referência (só escala)
    k = 6
    itens = [('hoje (v1)', atual['parado1']), ('versão 2', q['parado1']),
             ('v2 correndo', q['correndo3']), ('v1 correndo', atual['correndo3'])]
    sil = None
    try:
        from previa_elenco import silhueta
        import previa_elenco as PE
        PE.REF = REF
        sil, _, _ = silhueta('Aladdin.gif', 0, 58 / 53)
    except Exception as e:  # sem os sheets, a prancha sai sem a silhueta
        print('sem silhueta de referência:', e)
    if sil is not None:
        itens.insert(0, ('referência (só silhueta)', sil))
    W = sum(max(i.width * k + 40, 260) for _, i in itens) + 40
    out = Image.new('RGBA', (W, A * k + 170), (34, 26, 48, 255))
    d = ImageDraw.Draw(out)
    d.text((20, 14), 'Aladdin: hoje × versão 2 (linha B), mesma escala (6×)', font=fonte(26, True), fill='white')
    d.text((20, 50), 'Colete verde aberto com debrum dourado, calça larga lilás franzida, faixa rosa. Sem colete roxo, '
           'calça branca ou fez (regra 3).', font=fonte(16), fill=(220, 205, 240))
    chao = 90 + A * k
    d.line([(10, chao), (W - 10, chao)], fill=(255, 176, 250), width=2)
    x = 30
    for rot, im in itens:
        im = im.crop(im.getbbox())
        g = im.resize((im.width * k, im.height * k), Image.NEAREST)
        out.alpha_composite(g, (x, chao - g.height))
        d.text((x, chao + 12), rot, font=fonte(17, True), fill=(255, 214, 251))
        d.text((x, chao + 36), f'{im.height} px', font=fonte(15), fill=(200, 190, 220))
        x += max(g.width + 40, 260)
    out.save(os.path.join(SAIDA, 'aladdin-v1-x-v2.png'))
    # 2. todos os quadros
    k = 4
    nomes = list(q)
    cols = 8
    lin = (len(nomes) + cols - 1) // cols
    out = Image.new('RGBA', (cols * (L * k + 12) + 20, lin * (A * k + 40) + 60), (34, 26, 48, 255))
    d = ImageDraw.Draw(out)
    d.text((14, 12), f'Aladdin versão 2: {len(nomes)} quadros (4×)', font=fonte(22, True), fill='white')
    for i, n in enumerate(nomes):
        X, Y = 14 + (i % cols) * (L * k + 12), 50 + (i // cols) * (A * k + 40)
        f = Image.new('RGBA', (L, A), FUNDO)
        f.alpha_composite(q[n])
        out.alpha_composite(f.resize((L * k, A * k), Image.NEAREST), (X, Y))
        d.text((X, Y + A * k + 4), n, font=fonte(15), fill=(220, 205, 240))
    out.save(os.path.join(SAIDA, 'aladdin-v2-quadros.png'))
    # 3. animações
    gif('aladdin-v2-parado.gif', [q['parado1'], q['parado2'], q['parado3'], q['parado4']] * 2 +
        [q['piscando'], q['parado1']], 250)
    gif('aladdin-v2-corrida.gif', [q[f'correndo{i + 1}'] for i in range(8)], 62)
    gif('aladdin-v2-pulo.gif', [q['parado1'], q['aterrissando'], q['pulando1'], q['pulando2'], q['caindo1'],
                                q['caindo2'], q['aterrissando'], q['parado1']], 120)
    gif('aladdin-v2-arremesso.gif', [q['parado1'], q['arremessando1'], q['arremessando2'], q['arremessando3'],
                                     q['parado1']], 90)
    print('ok', SAIDA)


if __name__ == '__main__':
    main()
