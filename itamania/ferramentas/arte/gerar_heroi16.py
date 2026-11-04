"""Gera as folhas do herói (Geraldo e Helena) a partir dos sprites 16x24 desenhados pelo Pedro (heroi_base.py).

O desenho enviado tem só a pose parada (sem e com boné). As animações saem dele mexendo apenas nas pernas, no
braço e nos olhos; cabeça, roupa e cores ficam idênticas ao desenho.

Saída (pixels já ampliados, para o Phaser não precisar escalar):
- public/assets/sprites/heroi-<geraldo|helena>-normal.png     quadros de 32x48 (2x)
- public/assets/sprites/heroi-<geraldo|helena>-turbinado.png  quadros de 48x72 (3x, café com leite)
- src/art/heroi.js (ordem dos quadros e animações) e prévia em ferramentas/arte/previas/heroi.png
Primeira metade da folha: sem boné. Segunda metade: os mesmos quadros com boné.
Uso: python3 ferramentas/arte/gerar_heroi16.py   (dentro de itamania/)
"""
import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import heroi_base as B  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
L, A = 16, 24
ESCALAS = {'normal': 2}  # forma grande (café com leite) fica para depois do MVP

# caracteres de cada herói: camiseta, sombra da camiseta (braço), pele, bermuda
HEROIS = {
    'geraldo': dict(bases=(B.GERALDO, B.GERALDO_BONE), c='c', d='d', p='p', s='s'),
    'helena': dict(bases=(B.HELENA, B.HELENA_BONE), c='C', d='D', p='P', s='S'),
}

# Pernas (linhas 19 a 23). Letras: s bermuda, p pele, w tênis, v detalhe do tênis, o sola, k contorno.
PERNAS = {
    'corrida1': ['....kssk.kssk...', '...kppk...kppk..', '..kwwwk...kwwwwk', '..kwvwk...kwvwwk', '..koook...kooook'],
    'corrida2': ['.....ksssssk....', '....kwwwkppk....', '....koookppk....', '........kwvwwk..', '........koooook.'],
    'corrida3': ['.....kssksssk...', '....kppk.kppk...', '...kwwwk.kwwwwk.', '...kwvwk.kwvwwwk', '...koook.koooook'],
    'corrida4': ['.....ksssssk....', '.....kppkwwwwk..', '.....kppkoooook.', '....kwvwk.......', '....koook.......'],
    'pulo': ['.....ksssssk....', '....kppk.kppk...', '....kwwwkkwwwwk.', '....koookkoooook', '................'],
    'queda': ['.....ksssssk....', '....kppk..kppk..', '...kwwwk..kwwwwk', '...koook..kooook', '................'],
}


def copia(m):
    return [list(r) for r in m]


def trocar(m, r, c, ch):
    m[r][c] = ch


def pernas(m, nome, h):
    for i, linha in enumerate(PERNAS[nome]):
        assert len(linha) == L, (nome, linha)
        m[19 + i] = [h['s'] if ch == 's' else h['p'] if ch == 'p' else ch for ch in linha]


def braco_frente(m, h):
    """Braço esticado para a frente (arremesso, equilíbrio): some o braço do lado do corpo."""
    for r in (14, 15, 16, 17):
        for c in (9, 10):
            m[r][c] = h['c']
    for c in (13, 14):
        m[13][c] = 'k'
        m[15][c] = 'k'
    m[14][12] = h['d']
    m[14][13] = h['d']
    m[14][14] = h['p']
    m[14][15] = 'k'
    m[13][15] = '.'
    m[15][15] = '.'


def piscar(m, h):
    m[7][10] = h['p']
    m[7][11] = h['p']
    m[8][10] = 'k'
    m[8][11] = 'k'


def olhos_dano(m, h):
    m[7][10] = 'k'
    m[7][11] = h['p']
    m[8][10] = h['p']
    m[8][11] = 'k'


def quadros(base, h):
    q = {}
    q['parado'] = copia(base)
    q['piscando'] = copia(base)
    piscar(q['piscando'], h)
    for i in range(4):
        m = copia(base)
        pernas(m, f'corrida{i + 1}', h)
        q[f'correndo{i + 1}'] = m
    m = copia(base)
    pernas(m, 'pulo', h)
    q['pulando'] = m
    m = copia(base)
    pernas(m, 'queda', h)
    braco_frente(m, h)
    q['caindo'] = m
    q['arremessando1'] = copia(base)
    m = copia(base)
    braco_frente(m, h)
    q['arremessando2'] = m
    vazio = ['.'] * L
    q['aterrissando'] = [vazio[:]] + copia(base[0:19]) + copia(base[20:24])
    m = copia(base)
    pernas(m, 'queda', h)
    olhos_dano(m, h)
    q['dano'] = m
    m = copia(base)
    braco_frente(m, h)
    q['vitoria1'] = m
    m = copia(base)
    pernas(m, 'pulo', h)
    braco_frente(m, h)
    piscar(m, h)
    q['vitoria2'] = m
    for nome, m in q.items():
        assert len(m) == A and all(len(r) == L for r in m), nome
    return q


NOMES = ['parado', 'piscando', 'correndo1', 'correndo2', 'correndo3', 'correndo4', 'pulando', 'caindo',
         'arremessando1', 'arremessando2', 'aterrissando', 'dano', 'vitoria1', 'vitoria2']
ANIMACOES = {
    'parado': (['parado'] * 7 + ['piscando'], 4, -1),
    'correndo': (['correndo1', 'correndo2', 'correndo3', 'correndo4'], 10, -1),
    'pulando': (['pulando'], 1, 0),
    'caindo': (['caindo'], 1, 0),
    'arremessando': (['arremessando1', 'arremessando2', 'arremessando2'], 16, 0),
    'aterrissando': (['aterrissando'], 10, 0),
    'dano': (['dano'], 1, 0),
    'vitoria': (['vitoria1', 'vitoria2'], 4, -1),
}


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def imagem(m, esc):
    img = Image.new('RGBA', (L * esc, A * esc), (0, 0, 0, 0))
    px = img.load()
    for y, r in enumerate(m):
        for x, ch in enumerate(r):
            if ch == '.':
                continue
            cor = rgb(B.PALETA[ch]) + (255,)
            for yy in range(esc):
                for xx in range(esc):
                    px[x * esc + xx, y * esc + yy] = cor
    return img


def main():
    pasta = os.path.join(RAIZ, 'public/assets/sprites')
    folhas = []
    for nome, h in HEROIS.items():
        lista = []
        for base in h['bases']:
            q = quadros(base, h)
            lista += [q[n] for n in NOMES]
        for forma, esc in ESCALAS.items():
            folha = Image.new('RGBA', (L * esc * len(lista), A * esc), (0, 0, 0, 0))
            for i, m in enumerate(lista):
                folha.alpha_composite(imagem(m, esc), (i * L * esc, 0))
            folha.save(os.path.join(pasta, f'heroi-{nome}-{forma}.png'), optimize=True)
            if forma == 'normal':
                folhas.append(folha)
    js = ['// Herói do ITAMANIA: gerado por ferramentas/arte/gerar_heroi16.py a partir do desenho do Pedro (16x24).',
          '// Folhas em public/assets/sprites/heroi-<geraldo|helena>-<normal|turbinado>.png (já ampliadas 2x e 3x).',
          '// Os primeiros NOMES.length quadros são sem boné; os seguintes, os mesmos com o boné amarelo.',
          f'export const TAMANHOS = {json.dumps({f: [L * e, A * e] for f, e in ESCALAS.items()})};',
          'export const NOMES = ' + json.dumps(NOMES) + ';',
          'export const ANIMACOES = {']
    for n, (qs, fps, rep) in ANIMACOES.items():
        js.append(f'  {n}: {{ quadros: {json.dumps(qs)}, fps: {fps}, repetir: {rep} }},')
    js.append('};')
    with open(os.path.join(RAIZ, 'src/art/heroi.js'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(js) + '\n')
    prev = os.path.join(RAIZ, 'ferramentas/arte/previas')
    os.makedirs(prev, exist_ok=True)
    larg = max(f.width for f in folhas)
    tela = Image.new('RGBA', (larg, 48 * len(folhas)), (168, 220, 245, 255))
    for i, f in enumerate(folhas):
        tela.alpha_composite(f, (0, i * 48))
    tela.resize((tela.width * 2, tela.height * 2), Image.NEAREST).save(os.path.join(prev, 'heroi.png'))
    print('ok:', len(NOMES) * 2, 'quadros por folha')


if __name__ == '__main__':
    main()
