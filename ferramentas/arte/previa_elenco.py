"""Prancha de estudo: elenco atual do jogo × escala medida nas referências (sheets do SNES).

Uso: python3 ferramentas/arte/previa_elenco.py [repo] [pasta_dos_sheets]

Os sheets do Sprite Database ficam em references/estilo/sprites-spritedatabase/aladdin-snes/ (branch do PR 22).
Deles a prancha usa só a SILHUETA chapada em cinza e a altura (regra 3: nada dos pixels originais entra no jogo nem
nas prévias). Saída: ferramentas/arte/previas/personagens/elenco-atual-x-escala.png
"""
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comps import componentes  # noqa: E402

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', '..'))
REF = sys.argv[2] if len(sys.argv) > 2 else os.path.join(REPO, 'references', 'estilo', 'sprites-spritedatabase',
                                                         'aladdin-snes')
SAIDA = os.path.join(REPO, 'ferramentas', 'arte', 'previas', 'personagens')
ALADDIN_SNES = 53   # altura do Aladdin parado no sheet (px do SNES)
HEROI = 58          # altura do nosso herói (px do jogo)
K = 4               # ampliação da prancha


def carregar_sprites():
    js = ("const b=process.argv[1];const o={};for(const m of ['jogador','espaco','chefe','tapete','objetos'])"
          "o[m]=await import(b+'/src/art/'+m+'.js');console.log(JSON.stringify(o));")
    out = subprocess.run(['node', '--input-type=module', '-e', js, REPO], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def quadro_img(linhas, pal):
    img = Image.new('RGBA', (len(linhas[0]), len(linhas)), (0, 0, 0, 0))
    for y, l in enumerate(linhas):
        for x, c in enumerate(l):
            if c != '.':
                h = pal[c].lstrip('#')
                img.putpixel((x, y), tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return img.crop(img.getbbox())


def silhueta(arquivo, indice, escala):
    """Silhueta chapada (cinza) de um sprite do sheet, redimensionada para a escala do nosso jogo."""
    cs, lab = componentes(os.path.join(REF, arquivo))
    cs.sort(key=lambda t: (t['y'] // 20, t['x']))
    c = cs[indice]
    m = lab[c['y']:c['y'] + c['alt'], c['x']:c['x'] + c['larg']] == c['n']
    a = np.zeros(m.shape + (4,), np.uint8)
    a[m] = (150, 140, 170, 255)
    img = Image.fromarray(a, 'RGBA')
    w, h = round(img.width * escala), round(img.height * escala)
    return img.resize((w, h), Image.NEAREST), c['alt'], c['cores']


def fonte(t, negrito=False):
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if negrito else ''), t)


def main():
    d = carregar_sprites()
    esc = HEROI / ALADDIN_SNES
    j = d['jogador']
    sp = lambda m, k, i=0: quadro_img(d[m]['SPRITES'][k]['quadros'][i], d[m]['PALETA'])  # noqa: E731
    # (nome, sprite atual, quadros atuais, ref (arquivo, índice) ou None, alvo em px, observação curta)
    elenco = [
        ('Aladdin', quadro_img(j['QUADROS']['parado1'], j['PALETA']), len(j['ORDEM']), ('Aladdin.gif', 0), '56-60',
         'OK (8.0): escala e acabamento no padrão'),
        ('Jasmine', sp('espaco', 'jasmine'), 2, ('Jasmine.gif', 3), '50-54', 'pequena e chapada; 2 quadros'),
        ('Gênio', sp('espaco', 'genio'), 2, ('Genie.gif', 0), '80-90', 'muito pequeno: devia ser o maior'),
        ('Sultão', sp('espaco', 'sultao'), 2, ('FruitVendor.png', 0), '62-66', 'pequeno; NPC adulto robusto'),
        ('Tia Claudia', sp('espaco', 'claudia'), 2, None, '56-58', 'menor que o herói; 2 quadros'),
        ('Tia Paula', sp('chefe', 'tiaPaula'), 4, None, '56-58', 'coque castanho e vestido roxo: errado'),
        ('Abu', sp('espaco', 'abu'), 4, ('Abu.gif', 0), '24-30', 'tamanho ok; 9 cores, sem volume'),
        ('Jafar', sp('chefe', 'jafar'), 4, ('Jafar.gif', 0), '64-74', 'chefe menor que o herói'),
        ('Capivara', sp('objetos', 'capivara'), 6, ('SNES_Aladdin_Lv2Enemies.png', 6), '24-28',
         'ok no tamanho; 8 cores, 2 tons'),
    ]
    col = 230
    base_y = 520
    W = col * len(elenco) + 40
    H = 820
    out = Image.new('RGBA', (W, H), (34, 26, 48, 255))
    dr = ImageDraw.Draw(out)
    dr.text((20, 16), 'Elenco atual × escala medida nas referências (tudo ampliado 4×; herói = 58 px)',
            font=fonte(26, True), fill=(255, 255, 255))
    dr.text((20, 52), 'Colorido = sprite atual do jogo · cinza = silhueta de referência (SNES) convertida para a nossa '
            'escala (58/53), só para medir altura · faixa rosa = altura-alvo proposta', font=fonte(17),
            fill=(220, 205, 240))
    dr.line([(10, base_y), (W - 10, base_y)], fill=(255, 176, 250), width=2)
    for y in range(base_y - HEROI * K, base_y, 4 * K * 4):
        pass
    dr.line([(10, base_y - HEROI * K), (W - 10, base_y - HEROI * K)], fill=(110, 100, 140), width=1)
    dr.text((W - 210, base_y - HEROI * K - 22), 'altura do herói (58 px)', font=fonte(15), fill=(180, 170, 210))
    for i, (nome, img, nq, ref, alvo, obs) in enumerate(elenco):
        x0 = 30 + i * col
        lo, hi = (int(v) for v in alvo.split('-'))
        dr.rectangle([x0, base_y - hi * K, x0 + 8, base_y - lo * K], fill=(255, 176, 250))
        if ref:
            s, alt_ref, cores_ref = silhueta(ref[0], ref[1], esc)
            s = s.resize((s.width * K, s.height * K), Image.NEAREST)
            out.alpha_composite(s, (x0 + 14, base_y - s.height))
            xs = x0 + 14 + s.width + 6
        else:
            alt_ref = None
            xs = x0 + 20
        g = img.resize((img.width * K, img.height * K), Image.NEAREST)
        if xs + g.width > x0 + col - 4:
            xs = x0 + col - 4 - g.width
        out.alpha_composite(g, (xs, base_y - g.height))
        cores = len({p for p in img.get_flattened_data() if p[3]})
        y = base_y + 14
        dr.text((x0, y), nome, font=fonte(19, True), fill=(255, 255, 255))
        linhas = [f'hoje: {img.height} px · {nq} quadros', f'{cores} cores',
                  f'ref.: {round(alt_ref * esc)} px' if alt_ref else 'ref.: sem foto', f'alvo: {alvo} px']
        for k, t in enumerate(linhas):
            dr.text((x0, y + 28 + k * 22), t, font=fonte(15), fill=(220, 205, 240))
        # observação em até 2 linhas
        palavras, l1, l2 = obs.split(), '', ''
        for p in palavras:
            if len(l1) + len(p) < 26 and not l2:
                l1 += (' ' if l1 else '') + p
            else:
                l2 += (' ' if l2 else '') + p
        dr.text((x0, y + 124), l1, font=fonte(15, True), fill=(255, 214, 160))
        dr.text((x0, y + 144), l2, font=fonte(15, True), fill=(255, 214, 160))
    os.makedirs(SAIDA, exist_ok=True)
    out.save(os.path.join(SAIDA, 'elenco-atual-x-escala.png'))
    print('ok')


if __name__ == '__main__':
    main()
