"""Gera os PNGs de cenário do jogo (Etapa 8B, prévias aprovadas pelo Pedro em 01/11/2026).

Uso: python3 ferramentas/arte/gerar_cenarios.py [repo]

Saída em public/assets/cenario/ (o Preload carrega; ver CENARIO_PNG em src/art/index.js):
  Fase 1 (fim de tarde):  ceu.png (480x270, parado), morros.png e casas.png (960x270, repetem na horizontal),
                          clube, fonte, cafe, igreja, posto, estatua, helicoptero, arvore, arvore2 (lugares reais)
  Fase 3 (pôr do sol):    arena.png (480x270: céu, sol na serra, terraço; chão e plataformas são tiles)
  Fase 4 (crepúsculo):    ceu-crepusculo.png (parado), serra-crepusculo, cidade-crepusculo, telhados-crepusculo
                          (960x270, repetem), coroados.png (morro com o hotel), unifei.png

As faixas que repetem são feitas para emendar sem costura: a serra usa ondas com número inteiro de ciclos na
largura, e as casas e copas que passam da borda direita são desenhadas de novo na esquerda.
"""
import math
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerar_lugares as GL  # noqa: E402
import previa_chefe as PC  # noqa: E402
import previa_tapete as PT  # noqa: E402

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', '..'))
SAIDA = os.path.join(REPO, 'public', 'assets', 'cenario')
W, H = 960, 270


def salvar(img, nome):
    img.save(os.path.join(SAIDA, nome + '.png'), optimize=True)
    print(f'  {nome}.png {img.size[0]}x{img.size[1]} {os.path.getsize(os.path.join(SAIDA, nome + ".png")) // 1024} KB')


def morros_repetem(w=W, h=H):
    """Serra da Mantiqueira (3 camadas verdes de mata) que emenda nas bordas."""
    a = np.zeros((h, w, 4), np.uint8)
    rnd = np.random.RandomState(12)
    for rampa, base, amp, freqs, r in GL.SERRA:
        fq = [(max(1, round(f * w / 960)), k, fa) for f, k, fa in freqs]

        def crista(x):
            return base - sum(amp * k * math.sin(2 * math.pi * f * x / w + fa) for f, k, fa in fq)
        cores = [GL.hex_rgb(c) for c in rampa]
        for x in range(w):
            y = int(crista(x))
            a[y:, x, :3] = cores[2]
            a[y:, x, 3] = 255
        clara = [rampa[0], rampa[0], rampa[1], rampa[2]]

        def tons(xx):
            return clara if crista(xx + 6) < crista(xx - 6) else rampa

        def copa(xx, yy, rr):
            for dx in (-w, 0, w):   # repete nas bordas
                GL._copinha(a, xx + dx, yy, rr, tons(xx % w))
        passo = max(2, int(r * 1.3))
        for x in range(0, w, passo):
            xx = x + rnd.uniform(-1, 1)
            copa(xx, crista(xx) + rnd.uniform(-0.5, 1.5), r * rnd.uniform(0.8, 1.2))
        for _ in range(int(w * (h - base + amp) / (r * r * 4))):
            xx = rnd.uniform(0, w)
            yy = crista(xx) + rnd.uniform(2, h - base + amp)
            if yy < h:
                copa(xx, yy, r * rnd.uniform(0.7, 1.15))
    return Image.fromarray(a, 'RGBA')


def faixa_repete(pecas, w=W, h=H, base=246, sobrepor=2, semente=1):
    """Monta prédios lado a lado numa faixa que emenda (o que passa da borda volta pela esquerda)."""
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    x, i = 0, 0
    while x < w:
        p = pecas(i)
        for dx in (0, -w):
            img.alpha_composite(p, (x + dx, base - p.height)) if x + dx + p.width > 0 else None
        x += p.width - sobrepor
        i += 1
    return img


def casario_repete(semente, base, w=W):
    def casa(i):
        larg = [56, 72, 48, 64, 80][(semente + i) % 5]
        alt = [58, 74, 50, 66, 82][((semente + i) * 3) % 5]
        return GL.casa(semente * 31 + i, larg, alt)
    return faixa_repete(casa, w=w, base=base, sobrepor=2 - 0)


def cidade_repete(w=W):
    rnd = np.random.RandomState(4)

    def peca(i):
        if rnd.rand() < 0.35:
            return PT.predio(int(rnd.randint(0, 999)), int(rnd.choice([14, 18, 22])), int(rnd.randint(40, 80)))
        return GL.casa(int(rnd.randint(0, 999)), int(rnd.choice([32, 40])), int(rnd.choice([40, 48])))
    return faixa_repete(peca, w=w, base=236, sobrepor=-2)


def main():
    os.makedirs(SAIDA, exist_ok=True)
    print('Fase 1')
    salvar(GL.ceu(480), 'ceu')
    serra = morros_repetem()
    salvar(serra, 'morros')
    salvar(GL.tingir(casario_repete(3, 246), '#B89AD8', 0.16), 'casas')
    salvar(GL.tingir(GL.clube(), '#B89AD8', 0.16), 'clube')
    for nome, f in (('fonte', GL.fonte), ('cafe', GL.cafe), ('igreja', GL.igreja), ('posto', GL.posto),
                    ('estatua', GL.estatua), ('helicoptero', GL.helicoptero)):
        salvar(f(), nome)
    salvar(GL.tingir(GL.arvore(), '#B89AD8', 0.08), 'arvore')
    salvar(GL.tingir(GL.arvore(semente=89, L=110, A=128), '#B89AD8', 0.08), 'arvore2')
    print('Fase 3')
    salvar(PC.arena(completa=False).convert('RGB'), 'arena')
    print('Fase 4')
    salvar(PT.ceu_crepusculo(480).convert('RGB'), 'ceu-crepusculo')
    salvar(GL.tingir(serra, '#3A3070', 0.40), 'serra-crepusculo')
    salvar(PT.acender_janelas(cidade_repete(), '#4A3A80', 0.38, 0.5, 3), 'cidade-crepusculo')
    salvar(PT.acender_janelas(casario_repete(9, 312), '#4A3A80', 0.22, 0.45, 4), 'telhados-crepusculo')
    salvar(PT.acender_janelas(PT.morro_coroados(), '#4A3A80', 0.32, 0.7, 2), 'coroados')
    salvar(PT.acender_janelas(PT.unifei(), '#4A3A80', 0.22, 0.45, 5), 'unifei')


if __name__ == '__main__':
    main()
