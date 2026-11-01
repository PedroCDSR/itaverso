"""Gera as folhas PNG do elenco (Etapa 8A, propostas aprovadas pelo Pedro em 01/11/2026) e das aves do tapete.

Uso: python3 ferramentas/arte/gerar_elenco.py [repo]

Os desenhos vêm de elenco_proposta.py (personagens), previa_chefe.py (gaiola) e previa_tapete.py (aves): mesmo
renderizador e mesma luz do herói. Saída em public/assets/sprites/<nome>.png, uma faixa de quadros do mesmo tamanho,
na ORDEM abaixo (é a ordem que as animações do Preload usam). Os tamanhos ficam em SPRITES_PNG (src/art/index.js).

A capivara continua a de src/art/objetos.js (decisão do Pedro).
"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import elenco_proposta as EP  # noqa: E402
import previa_chefe as PC  # noqa: E402
import previa_tapete as PT  # noqa: E402

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', '..'))
SAIDA = os.path.join(REPO, 'public', 'assets', 'sprites')


def folha(nome, quadros):
    w = max(q.width for q in quadros)
    h = max(q.height for q in quadros)
    img = Image.new('RGBA', (w * len(quadros), h), (0, 0, 0, 0))
    for i, q in enumerate(quadros):
        # centraliza na largura e encosta embaixo (pé no fundo do quadro)
        img.alpha_composite(q, (i * w + (w - q.width) // 2, h - q.height))
    img.save(os.path.join(SAIDA, nome + '.png'), optimize=True)
    return nome, w, h, len(quadros)


def main():
    os.makedirs(SAIDA, exist_ok=True)
    tp, tc, ja, su, jf, ge, ab = (EP.TiaPaula(), EP.TiaClaudia(), EP.Jasmine(), EP.Sultao(), EP.Jafar(), EP.Genio(),
                                  EP.Abu())
    R, P = EP.respirar, EP.pose
    feitos = [
        # Tia Paula: 0-1 socorro (presa), 2-3 feliz, 4 sentada (tapete), 5-6 microfone (Final)
        folha('tiaPaula', [
            tp.img(R(1, ombro_f=85, cotovelo_f=20, ombro_t=75, cotovelo_t=25, rosto='socorro', mao_f='punho',
                     mao_t='punho')),
            tp.img(R(3, ombro_f=95, cotovelo_f=15, ombro_t=85, cotovelo_t=20, rosto='socorro', mao_f='punho',
                     mao_t='punho', fase=1.6)),
            tp.img(R(2, ombro_f=150, cotovelo_f=10, ombro_t=145, cotovelo_t=15, rosto='feliz', braco_t_atras=False)),
            tp.img(R(0, ombro_f=135, cotovelo_f=25, ombro_t=155, cotovelo_t=5, rosto='feliz', braco_t_atras=False,
                     fase=1.2, extra={'rabo': 15})),
            tp.img(P(sentado=True, hy=44, coxa_f=80, joelho_f=90, pe_f=0, coxa_t=75, joelho_t=85, ombro_f=60,
                     cotovelo_f=20, rosto='feliz', extra={'rabo': -25})),
            tp.img(R(0, ombro_f=60, cotovelo_f=95, rosto='fala', extra={'microfone': True})),
            tp.img(R(2, ombro_f=60, cotovelo_f=95, ombro_t=40, cotovelo_t=60, rosto='feliz', fase=1.4,
                     extra={'microfone': True})),
        ]),
        # Tia Claudia: 0 parada, 1 entregando os ingressos, 2 parada (respiração)
        folha('claudia', [tc.img(R(0)), tc.img(R(0, ombro_f=75, cotovelo_f=10, rosto='feliz',
                                                 extra={'ingressos': True})), tc.img(R(2))]),
        # Jasmine: 0 parada, 1-2 pirueta
        folha('jasmine', [
            ja.img(R(0, ombro_f=-20, cotovelo_f=60)),
            ja.img(P(ombro_f=160, cotovelo_f=-40, ombro_t=165, cotovelo_t=-40, coxa_f=0, joelho_f=0, coxa_t=-30,
                     joelho_t=80, ponta=True, rosto='feliz', braco_t_atras=False, extra={'giro': 0.6}, fase=1.5)),
            ja.img(P(ombro_f=95, cotovelo_f=0, ombro_t=-95, cotovelo_t=0, coxa_f=0, joelho_f=0, coxa_t=25,
                     joelho_t=70, ponta=True, rosto='fechado', extra={'giro': 1.0}, fase=3.0)),
        ]),
        # Sultão: 0 parado, 1 palmas
        folha('sultao', [su.img(R(0, ombro_f=-10, cotovelo_f=30)),
                         su.img(R(1, ombro_f=55, cotovelo_f=60, ombro_t=50, cotovelo_t=70, rosto='feliz',
                                  braco_t_atras=False))]),
        # Gênio: 0 flutuando, 1 tchan!
        folha('genio', [ge.img(P(ombro_f=-20, cotovelo_f=100, ombro_t=-10, cotovelo_t=90, rosto='feliz')),
                        ge.img(P(ombro_f=115, cotovelo_f=-35, ombro_t=165, cotovelo_t=-10, rosto='fala',
                                 fase=1.6))]),
        # Abu: 0 parado, 1-2 correndo, 3 aflito
        folha('abu', [ab.img('parado'), ab.img('correndo'), ab.img('correndo2'), ab.img('aflito')]),
        # Jafar: 0-1 flutuando, 2 lançando, 3 cansado/tonto
        folha('jafar', [
            jf.img(P(ombro_f=20, cotovelo_f=70, ombro_t=10, cotovelo_t=20, rosto='bravo', extra={'varinha': 160})),
            jf.img(P(ombro_f=25, cotovelo_f=65, ombro_t=12, cotovelo_t=24, rosto='bravo', fase=1.6,
                     extra={'varinha': 165})),
            jf.img(P(ombro_f=120, cotovelo_f=-30, ombro_t=-30, cotovelo_t=20, rosto='bravo', fase=1.2,
                     extra={'varinha': 170, 'brilho': 1.4})),
            jf.img(P(tronco=14, cabeca=8, ombro_f=-10, cotovelo_f=10, rosto='tonto', fase=2.4,
                     extra={'varinha': 230, 'sobe': -6})),
        ]),
        # Gaiola em 2 camadas (a Tia Paula fica entre elas): 0 fechada, 1 aberta
        folha('gaiola', [_frente(False), _frente(True)]),
        folha('gaiolaFundo', [_fundo(True), _fundo(False)]),
        # Aves do tapete (voam para a esquerda): 0 asa em cima, 1 asa embaixo
        folha('tucano', [PT.tucano(True), PT.tucano(False)]),
        folha('maritaca', [PT.maritaca(True), PT.maritaca(False)]),
    ]
    for nome, w, h, n in feitos:
        print(f"  {nome}: {{ largura: {w}, altura: {h} }},  // {n} quadros")


def _frente(aberta):
    im = Image.new('RGBA', (PC.GL_ + 10, PC.GA), (0, 0, 0, 0))
    im.alpha_composite(PC.gaiola('frente', aberta), (10, 0))
    return im


def _fundo(brilho):
    im = Image.new('RGBA', (PC.GL_ + 10, PC.GA), (0, 0, 0, 0))
    if brilho:
        im.alpha_composite(PC.brilho(), (10, 0))
    im.alpha_composite(PC.gaiola('tras'), (10, 0))
    return im


if __name__ == '__main__':
    main()
