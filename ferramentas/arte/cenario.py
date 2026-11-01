"""Ferramentas de pixel art para CENÁRIOS (prédios, monumentos, objetos grandes).

Complementa o modelo.py (que é para personagens). Cada pixel guarda um MATERIAL e um TOM:

    tom 0 = brilho, 1 = luz, 2 = base, 3 = sombra, 4 = sombra funda, 5 = contorno do material

Regras do guia (references/estilo/reference-notes.md) aplicadas aqui:
- 4 a 5 tons por material, sem degradê nem pontilhado: cada face recebe um tom chapado;
- luz de cima e da frente (um pouco da esquerda): bordas de cima e da esquerda 1 tom mais claras, de baixo e da
  direita 1 tom mais escuras, e embaixo de cada cornija uma faixa de sombra projetada;
- contorno de 1 px na cor de contorno do material vizinho (colorido, nunca preto puro);
- sombras puxadas para o roxo (ligação com a paleta da escola).

O resultado sai como imagem RGBA (Pillow) e pode virar matriz de caracteres para src/art/ (ver para_matriz).
"""
import random

import numpy as np
from PIL import Image, ImageDraw


# ---------------------------------------------------------------------------------------------------------------
# Cores e rampas
# ---------------------------------------------------------------------------------------------------------------

def hex_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_hex(c):
    return '#%02X%02X%02X' % tuple(int(round(max(0, min(255, v)))) for v in c)


def mistura(a, b, t):
    a, b = hex_rgb(a), hex_rgb(b)
    return rgb_hex(tuple(a[i] + (b[i] - a[i]) * t for i in range(3)))


def rampa(base, luz='#FFF6D8', sombra='#5A3A78', funda='#2E1A33'):
    """Rampa de 5 tons + contorno a partir da cor base (tom 2). A luz puxa para o amarelo claro da escola e a
    sombra para o roxo, como no guia."""
    return [
        mistura(base, luz, 0.55),
        mistura(base, luz, 0.25),
        base,
        mistura(base, sombra, 0.30),
        mistura(base, sombra, 0.58),
        mistura(base, funda, 0.78),
    ]


MATERIAIS = {}  # nome -> (id, [6 cores])
_POR_ID = [None]


def material(nome, cores):
    assert len(cores) == 6, nome
    if nome in MATERIAIS:
        return MATERIAIS[nome][0]
    i = len(_POR_ID)
    _POR_ID.append((nome, [hex_rgb(c) for c in cores]))
    MATERIAIS[nome] = (i, cores)
    return i


# Paleta de cenário do guia (arenito, terracota, madeira...) + materiais dos lugares de Itajubá.
M = {}
M['creme'] = material('creme', ['#FFF6DC', '#F7E6BE', '#E6CC98', '#C5A672', '#987B5A', '#5E3F2E'])     # reboco creme
M['branco'] = material('branco', ['#FFFFFF', '#F4F0EA', '#DCD4D2', '#B4A8B4', '#857792', '#4A3E5A'])    # frisos, molduras
M['marmore'] = material('marmore', ['#C8B8AE', '#A89488', '#877468', '#665458', '#463844', '#2C2030'])   # pedra escura do clube
M['vidro'] = material('vidro', ['#FBE4F2', '#C8B4EC', '#8F8CD4', '#6462AA', '#45407E', '#272350'])  # reflete o entardecer
M['vidro_escuro'] = material('vidro_escuro', ['#8C8AB8', '#5E5C8E', '#46446E', '#33315A', '#242244', '#16142C'])
M['madeira'] = material('madeira', ['#E0A86C', '#C08A55', '#955F37', '#6A3D22', '#472513', '#2A1208'])
M['madeira_clara'] = material('madeira_clara', ['#F6D29A', '#E2B477', '#C8925A', '#9C6A3E', '#6E4528', '#40240F'])
M['telha'] = material('telha', ['#F09A6E', '#E8875E', '#C9623E', '#A0472C', '#73301F', '#4A1E18'])
M['bronze'] = material('bronze', ['#F0C27E', '#C48C4E', '#8E5E34', '#5E3A20', '#3C2414', '#22130A'])
M['agua'] = material('agua', ['#FFFFFF', '#CDEEFF', '#8FD0F2', '#5C9ED8', '#3D6CB4', '#2A4A8A'])
M['bloquete'] = material('bloquete', ['#E4DEE0', '#C9C1C8', '#ABA1AE', '#877C8E', '#62586C', '#3E3448'])
M['granito'] = material('granito', ['#FBF2E0', '#EADBC0', '#D2BE9E', '#AE9878', '#80705E', '#4E4038'])  # borda da fonte
M['lona'] = material('lona', ['#ECE4D8', '#CEC4BA', '#A69C9C', '#7C7282', '#565068', '#2E2A3C'])        # toldo do café
M['grafite'] = material('grafite', ['#8A8494', '#625C6E', '#46404F', '#312C38', '#211D27', '#120F16'])   # ferro, placa preta
M['interior'] = material('interior', ['#7A5A50', '#5A4040', '#432E34', '#30222A', '#21161E', '#140C12'])  # loja à sombra
M['vermelho'] = material('vermelho', ['#FF9C8C', '#F05A4A', '#CC3530', '#9A2228', '#66161E', '#3E0C14'])
M['azul'] = material('azul', ['#A8C8FF', '#5A8AE8', '#3460C0', '#244490', '#182C62', '#0E1A40'])
M['amarelo'] = material('amarelo', ['#FFF9C8', '#FBE878', '#F2CF4A', '#C89A2A', '#8E6618', '#4A3008'])
M['dourado'] = material('dourado', ['#FFF7C2', '#F7DC74', '#E0B440', '#AC8024', '#76541A', '#3E2A0A'])
M['folha'] = material('folha', ['#C2EE8E', '#86CC58', '#55A23E', '#3A7634', '#26502C', '#14301C'])
M['tronco'] = material('tronco', ['#B08A6E', '#8A6650', '#664838', '#4A3028', '#30201C', '#1C1010'])
M['heli'] = material('heli', ['#FAFAFC', '#E2E4EA', '#BCC0CA', '#9096A8', '#666C84', '#3C4058'])         # cinza do helicóptero
M['preto'] = material('preto', ['#7C7888', '#545060', '#3A3644', '#28242F', '#1A1720', '#0E0C12'])
M['grama'] = material('grama', ['#C6E88A', '#93CC5E', '#68A848', '#4A803C', '#30582E', '#1A3420'])
M['concreto'] = material('concreto', ['#F2EEE8', '#DAD4D0', '#BAB2B4', '#948A96', '#6C6274', '#40384A'])
M['azulejo'] = material('azulejo', ['#FFFFFF', '#F2F2F6', '#D8DAE4', '#B0B4C8', '#8288A4', '#4C5070'])
M['pedra_amarela'] = material('pedra_amarela', ['#F4D898', '#D8B26C', '#B88C4E', '#8C6638', '#5E4226', '#36240E'])
M['laranja'] = material('laranja', ['#FFF0A0', '#FFC845', '#F8941E', '#D0601A', '#963A14', '#4E1A08'])
M['vidro_azul'] = material('vidro_azul', ['#D6ECFF', '#8EC2F4', '#5288D4', '#335CA8', '#223C78', '#14204A'])
M['rosa'] = material('rosa', ['#FFE2FC', '#FFC4FA', '#FFB0FA', '#D17ACB', '#94489A', '#4C1E52'])


def cor(mat, tom):
    return _POR_ID[mat][1][tom]


# ---------------------------------------------------------------------------------------------------------------
# Fonte em pixel (3x5, com algumas letras mais largas) para placas e inscrições
# ---------------------------------------------------------------------------------------------------------------

FONTE = {
    'A': ['.#.', '#.#', '###', '#.#', '#.#'],
    'B': ['##.', '#.#', '##.', '#.#', '##.'],
    'C': ['.##', '#..', '#..', '#..', '.##'],
    'D': ['##.', '#.#', '#.#', '#.#', '##.'],
    'E': ['###', '#..', '##.', '#..', '###'],
    'F': ['###', '#..', '##.', '#..', '#..'],
    'H': ['#.#', '#.#', '###', '#.#', '#.#'],
    'R': ['##.', '#.#', '##.', '#.#', '#.#'],
    'I': ['###', '.#.', '.#.', '.#.', '###'],
    'J': ['..#', '..#', '..#', '#.#', '.#.'],
    'L': ['#..', '#..', '#..', '#..', '###'],
    'N': ['#..#', '##.#', '#.##', '#..#', '#..#'],
    'O': ['.#.', '#.#', '#.#', '#.#', '.#.'],
    'P': ['##.', '#.#', '##.', '#..', '#..'],
    'S': ['.##', '#..', '.#.', '..#', '##.'],
    'T': ['###', '.#.', '.#.', '.#.', '.#.'],
    'U': ['#.#', '#.#', '#.#', '#.#', '###'],
    'V': ['#.#', '#.#', '#.#', '#.#', '.#.'],
    ' ': ['..', '..', '..', '..', '..'],
    'a': ['...', '.##', '#.#', '#.#', '.##'],
    'd': ['..#', '.##', '#.#', '#.#', '.##'],
    'f': ['.##', '.#.', '###', '.#.', '.#.'],
    'é': ['..#', '.#.', '#.#', '##.', '.##'],
    'h': ['#..', '#..', '##.', '#.#', '#.#'],
    'i': ['#', '.', '#', '#', '#'],
    'n': ['...', '##.', '#.#', '#.#', '#.#'],
    'o': ['...', '.#.', '#.#', '#.#', '.#.'],
}


def largura_texto(s):
    return sum(len(FONTE[c][0]) + 1 for c in s) - 1


# ---------------------------------------------------------------------------------------------------------------
# Tela
# ---------------------------------------------------------------------------------------------------------------

class Tela:
    def __init__(self, largura, altura, semente=1):
        self.L, self.A = largura, altura
        self.mat = np.zeros((altura, largura), np.int16)
        self.tom = np.zeros((altura, largura), np.int8)
        self.sem_contorno = np.zeros((altura, largura), bool)  # pixels que não geram contorno (água, brilho)
        self.rnd = random.Random(semente)

    # --- básico ---
    def dentro(self, x, y):
        return 0 <= x < self.L and 0 <= y < self.A

    def px(self, x, y, mat, tom, sem_contorno=False):
        x, y = int(round(x)), int(round(y))
        if self.dentro(x, y):
            self.mat[y, x] = mat
            self.tom[y, x] = tom
            self.sem_contorno[y, x] = sem_contorno

    def ret(self, x0, y0, x1, y1, mat, tom, sem_contorno=False):
        """Retângulo cheio, cantos inclusivos."""
        x0, x1 = sorted((int(round(x0)), int(round(x1))))
        y0, y1 = sorted((int(round(y0)), int(round(y1))))
        xa, xb = max(0, x0), min(self.L - 1, x1)
        ya, yb = max(0, y0), min(self.A - 1, y1)
        if xa > xb or ya > yb:
            return
        self.mat[ya:yb + 1, xa:xb + 1] = mat
        self.tom[ya:yb + 1, xa:xb + 1] = tom
        self.sem_contorno[ya:yb + 1, xa:xb + 1] = sem_contorno

    def hlinha(self, x0, x1, y, mat, tom):
        self.ret(x0, y, x1, y, mat, tom)

    def vlinha(self, x, y0, y1, mat, tom):
        self.ret(x, y0, x, y1, mat, tom)

    def linha(self, x0, y0, x1, y1, mat, tom, larg=1):
        n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for i in range(n + 1):
            t = i / n
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            if larg <= 1:
                self.px(x, y, mat, tom)
            else:
                self.ret(round(x - (larg - 1) / 2), round(y), round(x - (larg - 1) / 2) + larg - 1, round(y), mat, tom)

    def _mascara(self, desenhar):
        img = Image.new('1', (self.L, self.A), 0)
        desenhar(ImageDraw.Draw(img))
        return np.array(img, bool)

    def aplicar(self, mascara, mat, tom, sem_contorno=False):
        self.mat[mascara] = mat
        self.tom[mascara] = tom
        self.sem_contorno[mascara] = sem_contorno

    def poli(self, pts, mat, tom, sem_contorno=False):
        m = self._mascara(lambda d: d.polygon([(round(x), round(y)) for x, y in pts], fill=1))
        self.aplicar(m, mat, tom, sem_contorno)
        return m

    def elipse(self, cx, cy, rx, ry, mat, tom, sem_contorno=False):
        yy, xx = np.mgrid[0:self.A, 0:self.L]
        m = ((xx + 0.5 - cx) / rx) ** 2 + ((yy + 0.5 - cy) / ry) ** 2 <= 1.0
        self.aplicar(m, mat, tom, sem_contorno)
        return m

    def mascara_elipse(self, cx, cy, rx, ry):
        yy, xx = np.mgrid[0:self.A, 0:self.L]
        return ((xx + 0.5 - cx) / rx) ** 2 + ((yy + 0.5 - cy) / ry) ** 2 <= 1.0

    def mascara_ret(self, x0, y0, x1, y1):
        m = np.zeros((self.A, self.L), bool)
        m[max(0, y0):max(0, y1 + 1), max(0, x0):max(0, x1 + 1)] = True
        return m

    def mascara_arco(self, x0, x1, ytopo, ybase):
        """Vão em arco pleno: retângulo com meio círculo em cima (x0..x1 inclusivos)."""
        larg = x1 - x0 + 1
        r = larg / 2
        cx = x0 + r
        cy = ytopo + r
        yy, xx = np.mgrid[0:self.A, 0:self.L]
        dentro_x = (xx >= x0) & (xx <= x1)
        corpo = dentro_x & (yy >= cy) & (yy <= ybase)
        topo = ((xx + 0.5 - cx) ** 2 + (yy + 0.5 - cy) ** 2 <= r * r) & (yy >= ytopo)
        return corpo | topo

    def arco(self, x0, x1, ytopo, ybase, mat, tom):
        m = self.mascara_arco(x0, x1, ytopo, ybase)
        self.aplicar(m, mat, tom)
        return m

    def borda_de(self, m, lado):
        """Pixels da máscara que encostam no lado de fora: 'cima', 'baixo', 'esq', 'dir'."""
        f = np.zeros_like(m)
        if lado == 'cima':
            f[1:] = m[1:] & ~m[:-1]
            f[0] = m[0]
        elif lado == 'baixo':
            f[:-1] = m[:-1] & ~m[1:]
            f[-1] = m[-1]
        elif lado == 'esq':
            f[:, 1:] = m[:, 1:] & ~m[:, :-1]
            f[:, 0] = m[:, 0]
        else:
            f[:, :-1] = m[:, :-1] & ~m[:, 1:]
            f[:, -1] = m[:, -1]
        return f

    def moldura(self, m, mat, tom_luz, tom_sombra):
        """Moldura de 1 px em volta (por fora) de uma máscara: em cima e à esquerda clara, embaixo e à direita
        escura (relevo saliente com luz de cima-esquerda)."""
        fora = np.zeros_like(m)
        fora[:-1] |= m[1:]
        fora[1:] |= m[:-1]
        fora[:, :-1] |= m[:, 1:]
        fora[:, 1:] |= m[:, :-1]
        fora &= ~m
        yy, xx = np.nonzero(fora)
        for y, x in zip(yy, xx):
            baixo_ou_dir = (y > 0 and m[y - 1, x]) or (x > 0 and m[y, x - 1])
            self.px(x, y, mat, tom_sombra if baixo_ou_dir else tom_luz)

    def relevo(self, m, tom_luz=None, tom_sombra=None, delta=1):
        """Clareia a borda de cima/esquerda e escurece a de baixo/direita de uma região já pintada."""
        for lado, d in (('cima', -delta), ('esq', -delta), ('baixo', delta), ('dir', delta)):
            b = self.borda_de(m, lado)
            self.tom[b] = np.clip(self.tom[b] + d, 0, 4)

    def escurecer(self, m, n=1, so_mat=None):
        mm = m & (self.mat > 0)
        if so_mat is not None:
            mm &= self.mat == so_mat
        self.tom[mm] = np.clip(self.tom[mm] + n, 0, 4)

    def escurecer_ret(self, x0, y0, x1, y1, n=1, so_mat=None):
        self.escurecer(self.mascara_ret(x0, y0, x1, y1), n, so_mat)

    # --- peças de arquitetura ---
    def parede(self, x0, y0, x1, y1, mat, tom=2):
        """Parede lisa com relevo nas bordas."""
        self.ret(x0, y0, x1, y1, mat, tom)
        self.relevo(self.mascara_ret(x0, y0, x1, y1))

    def cornija(self, x0, x1, y, mat, alt=4, sombra_proj=2):
        """Cornija saliente: linha de brilho, faixa de luz, faixa base e sombra funda embaixo, e a sombra que ela
        projeta na parede (sombra_proj linhas)."""
        if sombra_proj:
            self.escurecer_ret(x0 + 1, y + alt, x1 - 1, y + alt + sombra_proj - 1, 1)
        tons = {1: [1], 2: [0, 3], 3: [0, 2, 3], 4: [0, 1, 2, 4], 5: [0, 1, 2, 3, 4], 6: [0, 1, 1, 2, 3, 4]}[alt]
        for i, t in enumerate(tons):
            self.hlinha(x0, x1, y + i, mat, t)
        self.vlinha(x1, y, y + alt - 1, mat, 4)

    def dentilhado(self, x0, x1, y, mat, passo=3, alt=2):
        """Fileira de dentículos (ou arquinhos) embaixo de uma cornija."""
        for x in range(x0, x1 + 1):
            if (x - x0) % passo == passo - 1:
                self.vlinha(x, y, y + alt - 1, mat, 4)
            else:
                self.vlinha(x, y, y + alt - 1, mat, 1 if (x - x0) % passo == 0 else 2)

    def cilindro(self, x0, x1, y0, y1, mat, desloc=0, caneluras=False):
        """Fuste de coluna: tons por faixa vertical (luz na frente-esquerda, sombra à direita)."""
        w = x1 - x0 + 1
        for x in range(x0, x1 + 1):
            f = (x - x0 + 0.5) / w
            t = 2 if f < 0.15 else 0 if f < 0.38 else 1 if f < 0.62 else 2 if f < 0.84 else 3
            t = min(4, t + desloc)
            if caneluras and w >= 8 and (x - x0) % 3 == 2 and 0 < x - x0 < w - 1:
                t = min(4, t + 1)
            self.vlinha(x, y0, y1, mat, t)

    def janela_grade(self, x0, y0, x1, y1, moldura='branco', vidro='vidro', colunas=2, linhas=3, aberta=False):
        """Janela de vidraça quadriculada com moldura branca saliente."""
        self.ret(x0, y0, x1, y1, M[moldura], 1)
        self.relevo(self.mascara_ret(x0, y0, x1, y1))
        xi0, yi0, xi1, yi1 = x0 + 2, y0 + 2, x1 - 2, y1 - 2
        self.ret(xi0, yi0, xi1, yi1, M[vidro], 3 if aberta else 2)
        # reflexo do céu em cima e sombra da verga
        self.hlinha(xi0, xi1, yi0, M[vidro], 4)
        for k in range(1, max(2, (yi1 - yi0) // 3)):
            xx = xi0 + 1 + k
            yy = yi1 - k
            if xi0 <= xx <= xi1 and yi0 < yy:
                self.px(xx, yy, M[vidro], 1)
        # caixilhos
        for c in range(1, colunas):
            xx = xi0 + round(c * (xi1 - xi0 + 1) / colunas) - (0 if colunas > 2 else 0)
            self.vlinha(xx, yi0, yi1, M[moldura], 1)
        for l in range(1, linhas):
            yy = yi0 + round(l * (yi1 - yi0 + 1) / linhas)
            self.hlinha(xi0, xi1, yy, M[moldura], 1)

    def veneziana(self, x0, y0, x1, y1, mat='branco'):
        """Janela com folhas de veneziana (ripas horizontais)."""
        self.ret(x0, y0, x1, y1, M[mat], 1)
        self.relevo(self.mascara_ret(x0, y0, x1, y1))
        meio = (x0 + x1) // 2
        for y in range(y0 + 2, y1 - 1):
            t = 1 if (y - y0) % 2 == 0 else 3
            self.hlinha(x0 + 2, meio - 1, y, M[mat], t)
            self.hlinha(meio + 1, x1 - 2, y, M[mat], t)
        self.vlinha(meio, y0 + 1, y1 - 1, M[mat], 3)

    def volume_h(self, m, mat, cortes=(0.10, 0.30, 0.66, 0.86)):
        """Sombreia uma máscara como um cilindro deitado (fuselagem, toldo): por coluna, do alto (brilho) ao
        pé (sombra funda)."""
        ys, xs = np.nonzero(m)
        for x in np.unique(xs):
            col = ys[xs == x]
            y0, y1 = col.min(), col.max()
            h = max(1, y1 - y0 + 1)
            for y in col:
                f = (y - y0 + 0.5) / h
                tom = 0 if f < cortes[0] else 1 if f < cortes[1] else 2 if f < cortes[2] else 3 if f < cortes[3] else 4
                self.mat[y, x] = mat
                self.tom[y, x] = tom

    def copa(self, cx, cy, rx, ry, mat, n=14):
        """Copa de árvore: vários tufos (elipses) com luz de cima-esquerda; cada tufo tem brilho, base e sombra,
        e a parte de baixo da copa fica na sombra funda."""
        tufos = []
        for _ in range(n):
            a = self.rnd.uniform(0, 2 * np.pi)
            d = self.rnd.uniform(0, 0.72)
            tufos.append((cx + np.cos(a) * rx * d, cy + np.sin(a) * ry * d, self.rnd.uniform(0.24, 0.38) * rx))
        tufos.sort(key=lambda t: t[1])  # de cima para baixo: os de baixo ficam na frente
        yy, xx = np.mgrid[0:self.A, 0:self.L]
        for tx, ty, r in tufos:
            ry2 = r * 0.8
            dx, dy = (xx + 0.5 - tx) / r, (yy + 0.5 - ty) / ry2
            dentro = dx ** 2 + dy ** 2 <= 1
            luz = -dx * 0.55 - dy * 0.8
            base_y = (ty - (cy - ry)) / (2 * ry)  # tufos de baixo mais escuros
            tom = np.where(luz > 0.62, 0, np.where(luz > 0.22, 1, np.where(luz > -0.35, 2, 3)))
            tom = np.clip(tom + (base_y > 0.62), 0, 4)
            self.mat[dentro] = mat
            self.tom[dentro] = tom[dentro]
            borda = dentro & (dx ** 2 + dy ** 2 > 0.72) & (luz < -0.2)
            self.tom[borda] = np.clip(self.tom[borda] + 1, 0, 4)
        # textura de folhas: pequenos 'v' de sombra espalhados por dentro da copa
        for _ in range(int(rx * ry / 6)):
            x = int(cx + self.rnd.uniform(-rx, rx))
            y = int(cy + self.rnd.uniform(-ry, ry))
            if self.dentro(x + 1, y + 1) and self.dentro(x - 1, y) and (self.mat[y, x - 1:x + 2] == mat).all():
                tm = min(4, self.tom[y, x] + 1)
                self.tom[y, x - 1] = tm
                self.tom[y + 1, x] = tm
                self.tom[y, x + 1] = tm
        # folhinhas soltas na borda de cima
        for _ in range(n * 3):
            x = int(cx + self.rnd.uniform(-rx, rx))
            y = int(cy + self.rnd.uniform(-ry, ry))
            if self.dentro(x, y) and self.mat[y, x] == mat and self.dentro(x, y - 1) and self.mat[y - 1, x] == 0:
                self.px(x, y - 1, mat, 1)

    def texto(self, x, y, s, mat, tom, sombra=None, escala=1):
        """Escreve com a FONTE. sombra = (mat, tom) para uma sombra 1 px abaixo-direita (letra em relevo).
        escala=2 desenha cada pixel da letra como um bloco 2x2 (placas grandes)."""
        cx = x
        e = escala
        for ch in s:
            g = FONTE[ch]
            for j, linha in enumerate(g):
                for i, c in enumerate(linha):
                    if c == '#':
                        if sombra:
                            self.ret(cx + i * e + 1, y + j * e + 1, cx + i * e + e, y + j * e + e, *sombra)
                        self.ret(cx + i * e, y + j * e, cx + i * e + e - 1, y + j * e + e - 1, mat, tom)
            cx += (len(g[0]) + 1) * e
        return cx

    def manchas(self, x0, y0, x1, y1, mat, n, tam=(1, 3), delta=1, so_tom=None):
        """Manchas de umidade/desgaste: borrões irregulares (elipses com borda roída) 1 tom mais escuros, só onde
        já é o material."""
        for _ in range(n):
            cx = self.rnd.uniform(x0, x1)
            cy = self.rnd.uniform(y0, y1)
            rx = self.rnd.uniform(tam[0], tam[1]) / 2 + 0.3
            ry = max(0.6, rx * self.rnd.uniform(0.4, 0.8))
            for yy in range(int(cy - ry) - 1, int(cy + ry) + 2):
                for xx in range(int(cx - rx) - 1, int(cx + rx) + 2):
                    d = ((xx + 0.5 - cx) / rx) ** 2 + ((yy + 0.5 - cy) / ry) ** 2
                    if d > 1 or (d > 0.55 and self.rnd.random() < 0.45):
                        continue
                    if self.dentro(xx, yy) and self.mat[yy, xx] == mat:
                        if so_tom is None or self.tom[yy, xx] == so_tom:
                            self.tom[yy, xx] = min(4, self.tom[yy, xx] + delta)

    def reboco(self, x0, y0, x1, y1, mat, n=None, tijolos=0, tijolo_mat=None):
        """Textura de parede rebocada: borrões grandes de 1 tom (desgaste), pontinhos e, se pedido, pedaços de
        reboco caído mostrando tijolo (como as paredes das capturas do guia)."""
        area = (x1 - x0 + 1) * (y1 - y0 + 1)
        n = n if n is not None else max(4, area // 420)
        self.manchas(x0, y0, x1, y1, mat, n, tam=(5, 12))
        self.manchas(x0, y0, x1, y1, mat, n, tam=(1, 3))
        for _ in range(n):  # pontinhos de luz (grão do reboco)
            x, y = self.rnd.randint(x0, x1), self.rnd.randint(y0, y1)
            if self.dentro(x, y) and self.mat[y, x] == mat and self.tom[y, x] > 0:
                self.tom[y, x] -= 1
        tm = tijolo_mat if tijolo_mat is not None else M['telha']
        for _ in range(tijolos):
            for _tent in range(30):
                cx, cy = self.rnd.randint(x0 + 4, x1 - 10), self.rnd.randint(y0 + 3, y1 - 7)
                w, h = self.rnd.randint(8, 12), self.rnd.randint(5, 7)
                if (self.mat[cy:cy + h, cx:cx + w] == mat).all():
                    break
            else:
                continue
            for yy in range(cy, cy + h):
                corte = abs(yy - (cy + h / 2)) / (h / 2)
                xa = cx + int(corte * 3) + self.rnd.randint(0, 1)
                xb = cx + w - int(corte * 3) - self.rnd.randint(0, 1)
                for xx in range(xa, xb):
                    fiada = (yy - cy) // 2
                    junta = (yy - cy) % 2 == 1 or (xx + (fiada % 2) * 2) % 4 == 0
                    self.px(xx, yy, tm, 4 if junta else 2)
                self.px(xa - 1, yy, mat, 4)   # borda quebrada do reboco
                self.px(xb, yy, mat, 0)

    def escorrido(self, x, y, comp, mat):
        """Marca de chuva escorrendo (linha vertical irregular 1 tom mais escura)."""
        for i in range(comp):
            if self.rnd.random() < 0.85 and self.dentro(x, y + i) and self.mat[y + i, x] == mat:
                self.tom[y + i, x] = min(4, self.tom[y + i, x] + 1)
            if self.rnd.random() < 0.12:
                x += self.rnd.choice((-1, 1))

    def rachadura(self, x, y, comp, mat):
        """Rachadura: linha escura em zigue-zague com 1 px de brilho embaixo-direita (borda quebrada)."""
        for _ in range(comp):
            if self.dentro(x, y) and self.mat[y, x] == mat:
                self.tom[y, x] = 4
                if self.dentro(x + 1, y + 1) and self.mat[y + 1, x + 1] == mat and self.tom[y + 1, x + 1] < 4:
                    self.tom[y + 1, x + 1] = max(0, self.tom[y + 1, x + 1] - 1)
            y += 1
            x += self.rnd.choice((-1, 0, 0, 1))
            if self.rnd.random() < 0.18:
                self.rachadura(x, y, comp // 3, mat) if comp > 6 else None

    # --- finalização ---
    def contorno(self, ignorar=()):
        """Contorno colorido por fora de tudo o que foi pintado (4 vizinhos)."""
        cheio = self.mat > 0
        fonte = cheio & ~self.sem_contorno
        for m in ignorar:
            fonte &= self.mat != m
        novo_m = self.mat.copy()
        novo_t = self.tom.copy()
        alvo = ~cheio
        for dy, dx in ((-1, 0), (0, -1), (0, 1), (1, 0)):
            viz = np.zeros_like(fonte)
            vm = np.zeros_like(self.mat)
            ys = slice(max(0, dy), self.A + min(0, dy))
            yd = slice(max(0, -dy), self.A + min(0, -dy))
            xs = slice(max(0, dx), self.L + min(0, dx))
            xd = slice(max(0, -dx), self.L + min(0, -dx))
            viz[yd, xd] = fonte[ys, xs]
            vm[yd, xd] = self.mat[ys, xs]
            sel = alvo & viz & (novo_m == 0)
            novo_m[sel] = vm[sel]
            novo_t[sel] = 5
        self.mat, self.tom = novo_m, novo_t
        self.sem_contorno = np.zeros_like(self.sem_contorno)

    def imagem(self):
        img = np.zeros((self.A, self.L, 4), np.uint8)
        for i in range(1, len(_POR_ID)):
            sel = self.mat == i
            if not sel.any():
                continue
            cores = _POR_ID[i][1]
            for t in range(6):
                s2 = sel & (self.tom == t)
                img[s2, :3] = cores[t]
                img[s2, 3] = 255
        return Image.fromarray(img, 'RGBA')


def colar_tela(destino, img, x, y):
    """Cola uma imagem RGBA sobre outra (cópia), na posição (x, y)."""
    destino.alpha_composite(img, (int(x), int(y)))


def contar_cores(img):
    a = np.array(img)
    a = a[a[:, :, 3] > 0][:, :3]
    return len({tuple(c) for c in a})


def para_matriz(img, chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&*+-:;<=>?@^_~'):
    """Converte uma imagem RGBA em (linhas, paleta) no formato de src/art/ ('.' = transparente).
    Serve para levar a arte para o jogo depois da aprovação."""
    a = np.array(img)
    pal = {}
    linhas = []
    for y in range(a.shape[0]):
        l = []
        for x in range(a.shape[1]):
            r, g, b, al = a[y, x]
            if al < 128:
                l.append('.')
                continue
            h = rgb_hex((r, g, b))
            if h not in pal:
                pal[h] = chars[len(pal)]
            l.append(pal[h])
        linhas.append(''.join(l))
    return linhas, {v: k for k, v in pal.items()}
