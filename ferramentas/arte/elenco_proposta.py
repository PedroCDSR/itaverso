"""Proposta de substituição do elenco (Etapa 8A; a capivara fica como está, decisão do Pedro), no padrão do herói da 8.0.

Uso: python3 ferramentas/arte/elenco_proposta.py [repo]
Saída (só prévia; nada em src/): ferramentas/arte/previas/personagens/
  proposta-elenco.png        todos lado a lado, na escala do jogo, com o Aladdin (4x)
  proposta-<nome>.png        cada personagem: sprite atual × poses novas (5x)
  nativo/<nome>-<pose>.png   cada quadro em 1x

Mesmo renderizador do Aladdin (modelo.py): volumes com luz de cima e da frente, 4 tons por material, linha de
separação e contorno colorido. Mesmo esqueleto (proporções do gerar_jogador.py), com escala por personagem:
adultos com a altura do herói, Sultão maior, Jasmine um pouco menor, Jafar e Gênio bem maiores (chefe e "gigante").

Designs PROVISÓRIOS (sem fotos dos figurinos). Nada do design da Disney (regra 3). Tia Paula segue a seção 8
(loira, rabo de cavalo, camiseta preta do espetáculo); Tia Claudia, só cabelo preto e óculos + roupa neutra.
"""
import math
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modelo import Boneco, Material, paleta_de, ponto, mistura  # noqa: E402

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', '..'))
SAIDA = os.path.join(REPO, 'ferramentas', 'arte', 'previas', 'personagens')
NATIVO = os.path.join(SAIDA, 'nativo')

EXTRAS = {'w': '#FFF6EA', 'e': '#1E1018', 'q': '#8E3A34', 'n': '#C2535A', 'c': '#F29A9A'}
POOL = [ch for ch in 'ABCDFGHIJKLMNOPRSTUVXYZabdfghijklmoprstuvxyz0123456789!#$%&*+-:;<=>?@^_~/|' if ch not in EXTRAS]


class Paleta:
    """Distribui caracteres únicos para os materiais de UM personagem."""

    def __init__(self):
        self.i = 0
        self.mats = []

    def __call__(self, nome, cores, limiares=(0.80, 0.45, 0.14)):
        chars = ''.join(POOL[self.i:self.i + 5])
        self.i += 5
        m = Material(nome, chars, cores, limiares)
        self.mats.append(m)
        return m

    def paleta(self):
        return paleta_de(self.mats, EXTRAS)


# rampas (brilho, base, sombra, funda, contorno)
R = {
    'pele_branca': ['#FFF2E6', '#F9DCC6', '#E8B898', '#BC8468', '#6E3E2C'],
    'pele_clara': ['#FCE0C4', '#EDB892', '#C98962', '#97583D', '#55291C'],
    'pele_morena': ['#F6C79A', '#DB9A6B', '#B06C45', '#80452C', '#4A2216'],
    'pele_lilas': ['#E8DCFF', '#C2B0F2', '#9886D6', '#6C5CAE', '#3A2E6E'],
    'loiro': ['#FFF4B8', '#F4D46A', '#D2A63E', '#9C7228', '#5A3E12'],
    'preto_cab': ['#6E5A6E', '#3E2E40', '#2A1C2C', '#1A101C', '#0E060E'],
    'camiseta_preta': ['#5E5470', '#3A3248', '#262034', '#181424', '#0C0A14'],
    'jeans': ['#9CB4DC', '#6E88BC', '#4E6498', '#36466E', '#1E2640'],
    'tenis': ['#FFFFFF', '#E8E4EE', '#C2BCCC', '#8E86A0', '#4A4258'],
    'sola': ['#F4EEF6', '#C8C0D0', '#9890A4', '#6A6278', '#3A3446'],
    'ouro': ['#FFF7C2', '#F2CF5A', '#C3962A', '#8A6418', '#4A3008'],
    'rosa': ['#FFE2FC', '#FFB0FA', '#D17ACB', '#94489A', '#4C1E52'],
    'lilas': ['#E6E6FF', '#B8B8FF', '#9E9EFF', '#6D6BD9', '#36347E'],
    'roxo': ['#B6A8F0', '#7E6CD0', '#5A48A8', '#3E2F7C', '#22184A'],
    'magenta': ['#FFB4E4', '#E25CB4', '#B03488', '#7A1E5E', '#420C32'],
    'verde': ['#A9E482', '#6CC24A', '#3F8C3A', '#285E2E', '#173A20'],
    'branco': ['#FFFFFF', '#F4F0EA', '#DCD4D2', '#B4A8B4', '#5A4E66'],
    'creme': ['#FFF6DC', '#F2E2BC', '#D8C090', '#A88C64', '#5E4630'],
    'pelo': ['#D8A070', '#A86C40', '#7C4A28', '#54301A', '#2C180C'],
    'pelo_claro': ['#FBE2BE', '#EEC394', '#CC9A68', '#9A6E46', '#5A3E24'],
    'capivara': ['#E0B080', '#C08A58', '#956440', '#6A442C', '#3A2418'],
    'fumaca': ['#FFFBE0', '#FFF0A8', '#F2D872', '#C8A84A', '#7A6428'],
    'fumaca_roxa': ['#E8D8FF', '#C0A8F0', '#9A80DA', '#6E58B0', '#3A2C70'],
    'marrom': ['#C98E55', '#955F37', '#6A3D22', '#472513', '#2A1208'],
    'cinza_barba': ['#FFFFFF', '#ECE8F0', '#C8C2D2', '#9890A8', '#5A5268'],
    'azul': ['#A8C8FF', '#5A8AE8', '#3460C0', '#244490', '#0E1A40'],
    'vermelho': ['#FF9C8C', '#F05A4A', '#CC3530', '#9A2228', '#3E0C14'],
}

PE_Y = 62


# ===============================================================================================================
# Figura humana genérica (mesmo esqueleto do herói, com escala)
# ===============================================================================================================

def pose(**kw):
    p = dict(hx=23.0, tronco=1.0, cabeca=0.0, coxa_f=5, joelho_f=6, pe_f=-4, coxa_t=-4, joelho_t=2, pe_t=0,
             ombro_f=-6, cotovelo_f=24, ombro_t=8, cotovelo_t=20, mao_f='aberta', mao_t='aberta', fase=0.0,
             rosto='normal', sentado=False, braco_t_atras=True, ponta=False, extra={})
    p.update(kw)
    return p


def respirar(i, **kw):
    r = [0.0, 0.5, 1.0, 0.5][i % 4]
    d = dict(tronco=1.0 - r * 0.6, cabeca=-1.0 + r, ombro_f=-6 + r * 2, fase=i * 0.9, resp=r)
    d.update(kw)
    return pose(**d)


class Humano:
    S = 1.0            # escala do corpo (1 = herói)
    LARG = 1.0         # largura do tronco
    BARRIGA = 0.0      # 0..1 (Sultão)
    L, A = 48, 64
    RB, RP = 2.0, 3.4  # raio do braço e da perna

    def __init__(self):
        self.pal = Paleta()
        self.mat()

    def mat(self):
        raise NotImplementedError

    # --- esqueleto ---
    def juntas(self, p):
        S = self.S
        c = dict(p)
        perna = (13.5 + 13.0) * S
        hy = (self.A - 2) - perna - 2.6 * S + p.get('resp', 0) * 0.4
        if p['sentado']:
            hy = p.get('hy', hy)
        hx = p['hx'] if 'hx' in p else self.L / 2 - 1
        c['hx'], c['hy'] = hx, hy
        incl = p['tronco']
        c['pescoco'] = ponto((hx, hy), 14.0 * S, 180 - incl)
        c['peito'] = mistura((hx, hy), c['pescoco'], 0.68)
        cab = ponto(c['pescoco'], 6.6 * S, 180 - incl * 0.6 - p['cabeca'])
        c['cab'] = (cab[0] + 0.6, cab[1])
        pz = c['pescoco']
        c['ombro_t'] = (pz[0] + 1.8 * self.LARG, pz[1] + 2.4 * S)
        c['ombro_f'] = (pz[0] - 2.0 * self.LARG, pz[1] + 2.8 * S)
        c['quadril_t'] = (hx + 1.6 * self.LARG, hy)
        c['quadril_f'] = (hx - 1.2 * self.LARG, hy + 0.4)
        return c

    def desenhar(self, p):
        b = Boneco(self.L, self.A)
        c = self.juntas(p)
        self.b, self.c, self.p = b, c, p
        self.fundo(b, c)
        if p['braco_t_atras']:
            c['mao_t_pt'] = self.braco(b, c, 't', 1)
        if not p['sentado']:
            self.perna(b, c, 't', 1)
        self.perna(b, c, 'f', 0)
        if p['sentado']:
            self.perna(b, c, 't', 1)
        self.roupa_baixo(b, c)
        self.tronco(b, c)
        self.cintura(b, c)
        b.capsula(c['pescoco'], (c['cab'][0] - 0.4, c['cab'][1] + 2.0), 2.0, 2.0, self.PELE, separar=False)
        self.gola(b, c)
        self.cabeca(b, c)
        c['mao_f_pt'] = self.braco(b, c, 'f', 0)
        if not p['braco_t_atras']:
            c['mao_t_pt'] = self.braco(b, c, 't', 0)
        self.na_mao(b, c)
        self.rosto(b, c)
        self.detalhes(b, c)
        return b

    def quadro(self, p):
        b = self.desenhar(p)
        linhas = b.texto({k: self.CONTORNO_ROSTO for k in EXTRAS})
        return linhas

    def img(self, p):
        linhas = self.quadro(p)
        pal = self.pal.paleta()
        im = Image.new('RGBA', (self.L, self.A), (0, 0, 0, 0))
        for y, l in enumerate(linhas):
            for x, ch in enumerate(l):
                if ch != '.':
                    h = pal[ch].lstrip('#')
                    im.putpixel((x, y), tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
        return im

    # --- peças padrão ---
    def fundo(self, b, c):
        pass

    def roupa_baixo(self, b, c):
        pass

    def cintura(self, b, c):
        pass

    def gola(self, b, c):
        pass

    def na_mao(self, b, c):
        pass

    def detalhes(self, b, c):
        pass

    def material_braco(self):
        return self.PELE

    def manga(self, b, ombro, cot, ang, esc):
        pass

    def braco(self, b, c, lado, esc):
        S = self.S
        ombro = c['ombro_' + lado]
        ang, dobra = self.p['ombro_' + lado], self.p['cotovelo_' + lado]
        cot = ponto(ombro, 8.5 * S, ang)
        mao = ponto(cot, 8.0 * S, ang + dobra)
        mb = self.material_braco()
        b.capsula(ombro, cot, self.RB, self.RB * 0.88, mb, esc)
        b.capsula(cot, mao, self.RB * 0.88, self.RB * 0.72, self.PELE if mb is not self.PELE else mb, esc)
        self.manga(b, ombro, cot, ang, esc)
        m2 = ponto(mao, 1.2, ang + dobra)
        if self.p['mao_' + lado] == 'punho':
            b.elipse(m2, 2.1, 2.1, self.PELE, esc)
        else:
            b.elipse(m2, 1.9, 2.3, self.PELE, esc, giro=-(ang + dobra))
        c['cot_' + lado] = cot
        c['ang_' + lado] = ang + dobra
        return m2

    def perna(self, b, c, lado, esc):
        S = self.S
        quadril = c['quadril_' + lado]
        coxa, joelho, pe = self.p['coxa_' + lado], self.p['joelho_' + lado], self.p['pe_' + lado]
        j = ponto(quadril, 13.5 * S, coxa)
        t = ponto(j, 13.0 * S, coxa - joelho)
        ang_pe = coxa - joelho + 90 - pe
        if self.p['ponta'] and lado == 'f':
            ang_pe = coxa - joelho + 20      # na ponta do pé (balé)
        r = self.RP
        b.capsula(quadril, j, r, r * 0.86, self.CALCA, esc, achatar=0.95)
        b.capsula(j, t, r * 0.86, r * 0.66, self.CALCA, esc, achatar=0.95)
        self.sapato(b, t, ang_pe, esc)
        c['tornozelo_' + lado] = t
        c['joelho_' + lado] = j

    def sapato(self, b, t, ang_pe, esc):
        dedos = ponto(t, 5.0, ang_pe)
        b.capsula(t, dedos, 2.0, 1.5, self.SAPATO, esc, achatar=0.85)
        sa = ponto(t, 1.9, ang_pe + 90)
        sb = ponto(dedos, 1.3, ang_pe + 90)
        b.capsula(ponto(sa, 1.0, ang_pe + 180), sb, 0.6, 0.6, self.SOLA, esc, separar=False)

    def tronco(self, b, c):
        hx, hy, lt = c['hx'], c['hy'], self.LARG
        b.capsula(c['peito'], (hx, hy - 1.5), 4.4 * lt, 3.9 * lt + self.BARRIGA * 2, self.ROUPA, separar=False,
                  achatar=0.92)
        b.elipse((c['peito'][0] + 0.4, c['peito'][1] - 0.8), 4.6 * lt, 3.3 * self.S, self.ROUPA, separar=False,
                 achatar=0.9)
        if self.BARRIGA:
            b.elipse((hx + 2.2, hy - 4), 4.2 * lt * self.BARRIGA + 2, 5.2, self.ROUPA, separar=False, achatar=0.9)

    def cabeca(self, b, c):
        cx, cy = c['cab']
        self.cabelo_tras(b, c)
        b.elipse((cx + 0.8, cy + 0.6), 4.4, 4.9, self.PELE, separar=False, achatar=0.65)
        b.elipse((cx + 2.4, cy + 3.0), 2.6, 2.3, self.PELE, separar=False, achatar=0.6)
        b.elipse((cx - 1.8, cy + 1.2), 1.2, 1.7, self.PELE, 1, separar=False, achatar=0.8)
        self.cabelo_frente(b, c)

    def cabelo_tras(self, b, c):
        pass

    def cabelo_frente(self, b, c):
        pass

    SOB = 'e'
    BOCHECHA = False
    CONTORNO_ROSTO = None

    def rosto(self, b, c):
        cx, cy = c['cab']
        tipo = self.p['rosto']
        ox1, ox2, oy = cx + 1.2, cx + 4.0, cy + 0.6
        s = self.SOB
        if tipo in ('normal', 'feliz', 'fala', 'socorro', 'bravo'):
            b.px(ox1, oy, 'w'); b.px(ox1 + 1, oy, 'e'); b.px(ox1 + 1, oy + 1, 'e'); b.px(ox1, oy + 1, 'w')
            b.px(ox2, oy, 'e'); b.px(ox2, oy + 1, 'e'); b.px(ox2 - 1, oy + 1, 'w')
            if tipo == 'socorro':
                b.px(ox1 - 0.5, oy - 1.0, s); b.px(ox1 + 0.6, oy - 1.8, s); b.px(ox2 + 0.6, oy - 1.8, s)
            elif tipo == 'bravo':
                b.px(ox1 - 0.5, oy - 2.0, s); b.px(ox1 + 0.6, oy - 1.4, s); b.px(ox1 + 1.6, oy - 1.0, s)
                b.px(ox2, oy - 1.0, s); b.px(ox2 + 1, oy - 1.6, s)
            else:
                b.px(ox1 - 0.5, oy - 1.4, s); b.px(ox1 + 0.6, oy - 1.8, s); b.px(ox1 + 1.6, oy - 1.8, s)
                b.px(ox2, oy - 1.6, s); b.px(ox2 + 1, oy - 1.4, s)
        elif tipo in ('fechado', 'dorme'):
            b.px(ox1 - 0.2, oy + 0.8, 'e'); b.px(ox1 + 0.8, oy + 0.2, 'e'); b.px(ox1 + 1.8, oy + 0.8, 'e')
            b.px(ox2 - 0.4, oy + 0.2, 'e'); b.px(ox2 + 0.6, oy + 0.8, 'e')
        elif tipo == 'tonto':
            for dx, dy in ((0, -0.4), (1, 0.5), (0, 1.4)):
                b.px(ox1 + dx, oy + dy, 'e')
            for dx, dy in ((0.4, -0.4), (-0.6, 0.5), (0.4, 1.4)):
                b.px(ox2 + dx, oy + dy, 'e')
        if self.BOCHECHA:
            b.px(cx + 2.2, cy + 3.2, 'c')
        b.tom_em(cx + 5.2, cy + 2.1, self.PELE, 2)
        b.tom_em(cx + 4.4, cy + 2.9, self.PELE, 2)
        if tipo in ('feliz', 'fechado'):
            b.px(cx + 2.6, cy + 4.2, 'q'); b.px(cx + 3.6, cy + 4.6, 'n'); b.px(cx + 4.4, cy + 4.0, 'q')
        elif tipo in ('fala', 'socorro', 'tonto'):
            b.px(cx + 3.0, cy + 4.2, 'q'); b.px(cx + 3.0, cy + 5.0, 'n'); b.px(cx + 4.0, cy + 4.4, 'q')
            b.px(cx + 4.0, cy + 5.0, 'q')
        elif tipo == 'bravo':
            b.px(cx + 3.0, cy + 4.4, 'q'); b.px(cx + 4.0, cy + 4.4, 'q')
        else:
            b.px(cx + 3.0, cy + 4.4, 'q'); b.px(cx + 4.0, cy + 4.2, 'q')
        b.tom_em(cx + 0.2, cy + 5.6, self.PELE, 3)
        b.tom_em(cx + 1.2, cy + 5.9, self.PELE, 2)


def corrente(b, origem, comp, larg, direcao, fase, mat, esc=0, n=4, afinar=0.15, amplitude=12, separar=True):
    pts = [origem]
    x, y = origem
    for i in range(n):
        a = direcao + math.sin(fase + i * 1.3) * amplitude * (i + 1) / n
        x, y = ponto((x, y), comp / n, a)
        pts.append((x, y))
    for i in range(n):
        r0 = larg * (1 - afinar * i)
        b.capsula(pts[i], pts[i + 1], r0, r0 * (1 - afinar), mat, esc, separar=separar)
    return pts


# ===============================================================================================================
# Tia Paula: loira, rabo de cavalo, camiseta preta do espetáculo ("Aladdin" dourado com fumaça azul e roxa e a
# lâmpada). Resto neutro: calça jeans e tênis brancos. Um sprite só para Chefe, Tapete e Final.
# ===============================================================================================================

class TiaPaula(Humano):
    BOCHECHA = True

    def mat(self):
        P = self.pal
        self.PELE = P('pele', R['pele_branca'], (0.78, 0.42, 0.10))   # pele branca (Pedro, 01/11/2026)
        self.CABELO = P('cabelo', R['loiro'], (0.78, 0.46, 0.18))
        self.ROUPA = P('camiseta', R['camiseta_preta'], (0.74, 0.40, 0.12))
        self.CALCA = P('jeans', R['jeans'])
        self.SAPATO = P('tenis', R['tenis'])
        self.SOLA = P('sola', R['sola'])
        self.OURO = P('ouro', R['ouro'], (0.70, 0.40, 0.12))
        self.AZUL = P('fumaca_azul', ['#C8E8FF', '#62B8F0', '#3A86D0', '#2A5A9A', '#16305A'])
        self.ROXO = P('fumaca_roxa', R['roxo'])
        self.MIC = P('mic', ['#E8E8F0', '#A8A8B8', '#6E6E80', '#45455A', '#22222E'])
        self.SOB = self.CABELO.chars[3]
        self.CONTORNO_ROSTO = self.PELE.contorno

    def manga(self, b, ombro, cot, ang, esc):
        b.capsula(ombro, mistura(ombro, cot, 0.55), 2.6, 2.4, self.ROUPA, esc)   # manga curta da camiseta

    def cabelo_tras(self, b, c):
        cx, cy = c['cab']
        b.elipse((cx - 0.4, cy - 0.6), 5.4, 5.0, self.CABELO, separar=False)
        # rabo de cavalo alto, balançando
        corrente(b, (cx - 4.6, cy - 2.4), 13, 2.2, -20 + self.p['extra'].get('rabo', 0), self.p['fase'],
                 self.CABELO, 0, n=4, afinar=0.18, amplitude=10)
        b.elipse((cx - 4.4, cy - 2.6), 1.4, 1.3, self.ROXO, separar=False)       # prendedor

    def cabelo_frente(self, b, c):
        cx, cy = c['cab']
        b.elipse((cx + 0.8, cy - 3.4), 4.6, 2.2, self.CABELO, separar=False)     # cabelo puxado para trás
        b.elipse((cx + 4.2, cy - 1.8), 1.6, 1.4, self.CABELO, separar=False)     # franjinha de lado
        b.capsula((cx - 0.4, cy - 1.6), (cx - 0.6, cy + 1.6), 0.8, 0.6, self.CABELO, separar=False)

    def detalhes(self, b, c):
        # estampa da camiseta: "Aladdin" (linha dourada ondulada) com fumaça azul e roxa e a lâmpada embaixo
        px, py = c['peito']
        for dx in range(-3, 4):
            b.tom_em(px + dx, py - 0.5 + (0.6 if dx % 2 else 0), self.OURO, 1 if dx % 3 else 0)
        for dx, dy in ((-4, -1.5), (-4, 0.5)):
            b.tom_em(px + dx, py + dy, self.AZUL, 1)
        for dx, dy in ((4, -1.5), (4, 0.5)):
            b.tom_em(px + dx, py + dy, self.ROXO, 1)
        b.tom_em(px + 0, py + 2, self.OURO, 2); b.tom_em(px + 1, py + 2, self.OURO, 1)   # lâmpada

    def na_mao(self, b, c):
        if self.p['extra'].get('microfone'):
            m = c['mao_f_pt']
            b.capsula(m, ponto(m, 4, c['ang_f'] + 150), 0.8, 0.8, self.MIC)
            b.elipse(ponto(m, 4.6, c['ang_f'] + 150), 1.5, 1.5, self.MIC)


# ===============================================================================================================
# Tia Claudia: cabelo preto na altura do ombro e óculos (seção 8). Roupa neutra da escola: camiseta rosa com os
# quadradinhos do logo, calça escura e sapatilha.
# ===============================================================================================================

class TiaClaudia(Humano):
    BOCHECHA = True

    def mat(self):
        P = self.pal
        self.PELE = P('pele', R['pele_branca'], (0.78, 0.42, 0.10))   # pele branca (Pedro, 01/11/2026)
        self.CABELO = P('cabelo', R['preto_cab'], (0.82, 0.52, 0.22))
        self.ROUPA = P('camiseta', R['rosa'], (0.86, 0.50, 0.16))
        self.CALCA = P('calca', ['#8A86A8', '#5C5880', '#424062', '#2E2C48', '#18162A'])
        self.SAPATO = P('sapatilha', R['lilas'])
        self.SOLA = P('sola', R['roxo'])
        self.OCULOS = P('oculos', R['roxo'])
        self.LOGO = P('logo', R['verde'])
        self.AMAR = P('amarelo', R['ouro'])
        self.ING = P('ingresso', ['#FFFFFF', '#F9FCBB', '#E0D890', '#B0A060', '#6A5A2A'])
        self.SOB = self.CABELO.chars[3]
        self.CONTORNO_ROSTO = self.PELE.contorno

    def manga(self, b, ombro, cot, ang, esc):
        b.capsula(ombro, mistura(ombro, cot, 0.5), 2.6, 2.4, self.ROUPA, esc)

    def cabelo_tras(self, b, c):
        cx, cy = c['cab']
        b.elipse((cx - 0.8, cy - 0.4), 5.6, 5.2, self.CABELO, separar=False)
        b.capsula((cx - 3.4, cy), (cx - 3.0, cy + 6.6), 3.0, 2.6, self.CABELO, separar=False)   # até o ombro
        b.capsula((cx + 4.2, cy - 1), (cx + 4.6, cy + 4.4), 1.4, 1.2, self.CABELO, separar=False)

    def cabelo_frente(self, b, c):
        cx, cy = c['cab']
        b.elipse((cx + 1.2, cy - 3.6), 4.8, 2.2, self.CABELO, separar=False)
        b.elipse((cx + 4.0, cy - 2.4), 2.0, 1.6, self.CABELO, separar=False)

    def detalhes(self, b, c):
        cx, cy = c['cab']
        oy = cy + 0.6
        # óculos de armação roxa (duas lentes e a ponte)
        for x in (cx + 0.4, cx + 1.4, cx + 2.4):
            b.px(x, oy - 1, self.OCULOS.chars[2])
            b.px(x, oy + 2, self.OCULOS.chars[2])
        b.px(cx + 0.2, oy, self.OCULOS.chars[2]); b.px(cx + 0.2, oy + 1, self.OCULOS.chars[2])
        b.px(cx + 3.0, oy, self.OCULOS.chars[2])
        b.px(cx + 3.6, oy - 1, self.OCULOS.chars[2]); b.px(cx + 4.6, oy - 1, self.OCULOS.chars[2])
        b.px(cx + 5.2, oy, self.OCULOS.chars[2]); b.px(cx + 4.6, oy + 2, self.OCULOS.chars[2])
        b.px(cx - 0.8, oy, self.OCULOS.chars[3])   # haste
        # quadradinhos do logo no peito
        px, py = c['peito']
        for dx, dy, m in ((-1, -1, self.LOGO), (0, -1, self.LOGO), (-1, 0, self.LOGO), (0, 0, self.AMAR)):
            b.tom_em(px + dx, py + dy, m, 1)

    def na_mao(self, b, c):
        if self.p['extra'].get('ingressos'):
            m = c['mao_f_pt']
            for k in range(3):
                b.capsula((m[0] + 1 + k * 0.6, m[1] - 2 - k * 1.2), (m[0] + 5 + k * 0.6, m[1] - 3 - k * 1.2), 1.0,
                          1.0, self.ING, separar=False)


# ===============================================================================================================
# Jasmine (versão da escola, bailarina): trança comprida, tiara dourada, blusa lilás de manga bufante curta,
# saia longa de dança rosa com cinto de moedas dourado, sapatilhas. Sem o top e a calça do filme.
# ===============================================================================================================

class Jasmine(Humano):
    S = 0.92
    BOCHECHA = True

    def mat(self):
        P = self.pal
        self.PELE = P('pele', R['pele_morena'], (0.78, 0.42, 0.10))
        self.CABELO = P('cabelo', R['preto_cab'], (0.82, 0.52, 0.22))
        self.ROUPA = P('blusa', R['lilas'], (0.86, 0.50, 0.16))
        self.SAIA = P('saia', R['rosa'], (0.86, 0.50, 0.16))
        self.CALCA = self.PELE
        self.SAPATO = P('sapatilha', R['rosa'])
        self.SOLA = self.SAPATO
        self.OURO = P('ouro', R['ouro'], (0.70, 0.40, 0.12))
        self.SOB = self.CABELO.chars[3]
        self.CONTORNO_ROSTO = self.PELE.contorno

    def manga(self, b, ombro, cot, ang, esc):
        b.elipse(mistura(ombro, cot, 0.3), 2.8, 2.6, self.ROUPA, esc)          # manga bufante curta

    def tronco(self, b, c):
        hx, hy = c['hx'], c['hy']
        b.capsula(c['peito'], (hx, hy - 1.5), 3.9, 3.0, self.PELE, separar=False, achatar=0.92)   # cintura à mostra
        b.elipse((c['peito'][0] + 0.4, c['peito'][1] - 0.6), 4.2, 3.0, self.ROUPA, separar=False, achatar=0.9)

    def roupa_baixo(self, b, c):
        hx, hy = c['hx'], c['hy']
        ab = self.p['extra'].get('giro', 0)
        tf, tt = c['tornozelo_f'], c['tornozelo_t']
        base = max(tf[1], tt[1]) - 3
        # saia longa que abre em sino (mais aberta na pirueta)
        b.poligono([(hx - 4.4, hy - 2.5), (hx + 4.6, hy - 2.5), (hx + 8 + ab * 6, base - ab * 3),
                    (hx - 8 - ab * 6, base - ab * 3)], self.SAIA, separar=False)
        for k in (-3, 0, 3):   # pregas
            for y in range(int(hy + 2), int(base - ab * 3)):
                t = (y - hy) / max(1, base - hy)
                b.tom_em(hx + k * (1 + t * (1 + ab)), y, self.SAIA, 2)

    def cintura(self, b, c):
        hx, hy = c['hx'], c['hy']
        b.capsula((hx - 4.6, hy - 2.6), (hx + 4.8, hy - 2.8), 1.2, 1.2, self.OURO, separar=False)
        for k in range(-4, 5, 2):
            b.elipse((hx + k, hy - 0.8), 0.7, 0.9, self.OURO, separar=False)   # moedinhas

    def cabelo_tras(self, b, c):
        cx, cy = c['cab']
        b.elipse((cx - 0.6, cy - 0.4), 5.4, 5.2, self.CABELO, separar=False)
        pts = corrente(b, (cx - 4.2, cy + 1.0), 22 * self.S, 1.9, -6, self.p['fase'], self.CABELO, 0, n=5,
                       afinar=0.1, amplitude=8)
        for p_ in pts[1:-1]:
            b.tom_em(p_[0], p_[1], self.CABELO, 0)               # gomos da trança
        b.elipse(pts[-1], 1.2, 1.2, self.OURO, separar=False)

    def cabelo_frente(self, b, c):
        cx, cy = c['cab']
        b.elipse((cx + 1.0, cy - 3.4), 4.8, 2.3, self.CABELO, separar=False)
        b.capsula((cx - 3.0, cy - 3.6), (cx + 4.0, cy - 5.0), 0.8, 0.7, self.OURO, separar=False)   # tiara
        b.elipse((cx + 1.8, cy - 5.0), 1.0, 1.2, self.OURO, separar=False)


# ===============================================================================================================
# Sultão (versão da escola): robusto, turbante rosa com pena e joia, barba branca, túnica creme, faixa dourada,
# capa roxa nas costas. Maior que o herói.
# ===============================================================================================================

class Sultao(Humano):
    S = 1.06
    LARG = 1.35
    BARRIGA = 0.9
    L, A = 56, 72
    RB, RP = 2.4, 3.8

    def mat(self):
        P = self.pal
        self.PELE = P('pele', R['pele_branca'], (0.78, 0.42, 0.10))   # pele branca (Pedro, 01/11/2026)
        self.ROUPA = P('tunica', R['creme'])
        self.CALCA = P('calca', R['creme'])
        self.CAPA = P('capa', R['roxo'])
        self.TURB = P('turbante', R['rosa'], (0.86, 0.50, 0.16))
        self.BARBA = P('barba', R['cinza_barba'])
        self.OURO = P('ouro', R['ouro'], (0.70, 0.40, 0.12))
        self.SAPATO = P('sapato', R['magenta'])
        self.SOLA = self.OURO
        self.PENA = P('pena', R['verde'])
        self.SOB = self.BARBA.chars[3]
        self.CONTORNO_ROSTO = self.PELE.contorno

    def juntas(self, p):
        p = dict(p)
        p.setdefault('hx', self.L / 2 - 1)
        return super().juntas(p)

    def manga(self, b, ombro, cot, ang, esc):
        b.capsula(ombro, cot, 2.9, 2.7, self.ROUPA, esc)

    def fundo(self, b, c):
        pz = c['pescoco']
        hy = c['hy']
        b.poligono([(pz[0] - 6, pz[1] + 1), (pz[0] + 3, pz[1] + 1), (pz[0] + 1, hy + 22), (pz[0] - 13, hy + 22)],
                   self.CAPA, 1, separar=False)

    def roupa_baixo(self, b, c):
        hx, hy = c['hx'], c['hy']
        base = c['tornozelo_f'][1] - 6
        b.poligono([(hx - 6, hy - 2), (hx + 7, hy - 2), (hx + 9, base), (hx - 8, base)], self.ROUPA,
                   separar=False)

    def cintura(self, b, c):
        hx, hy = c['hx'], c['hy']
        b.capsula((hx - 6.5, hy - 2.5), (hx + 8.5, hy - 3.2), 1.8, 1.8, self.OURO, separar=False)
        b.elipse((hx + 3, hy - 3), 1.6, 1.6, self.TURB, separar=False)

    def cabeca(self, b, c):
        super().cabeca(b, c)
        cx, cy = c['cab']
        # barba branca cheia
        b.elipse((cx + 2.8, cy + 6.6), 3.2, 3.0, self.BARBA, separar=False)      # barba só no queixo
        b.capsula((cx + 0.2, cy + 3.0), (cx + 1.6, cy + 6.0), 0.9, 1.2, self.BARBA, separar=False)
        # turbante rosa com joia e pena
        b.elipse((cx + 0.6, cy - 3.6), 6.2, 4.4, self.TURB, separar=False)
        b.capsula((cx - 4.6, cy - 2.4), (cx + 5.4, cy - 3.4), 1.0, 1.0, self.TURB, 1, separar=False)
        corrente(b, (cx + 1.6, cy - 6.6), 8, 1.1, 165, 0.4, self.PENA, n=3, amplitude=8)
        b.elipse((cx + 2.0, cy - 4.2), 1.2, 1.4, self.OURO, separar=False)

    def rosto(self, b, c):
        super().rosto(b, c)
        cx, cy = c['cab']
        b.px(cx + 3.2, cy + 3.6, self.BARBA.chars[2]); b.px(cx + 4.4, cy + 3.6, self.BARBA.chars[2])   # bigode

    def na_mao(self, b, c):
        pass


# ===============================================================================================================
# Jafar (chefe, design próprio do jogo): capuz roxo pontudo com beirada lilás, rosto fino, bigode enrolado,
# cavanhaque, manto roxo com forro magenta, medalhão de lua dourado, varinha de estrela, cauda de fumaça no
# lugar das pernas (flutua). Bem maior que o herói.
# ===============================================================================================================

class Jafar(Humano):
    S = 1.18
    LARG = 1.25
    L, A = 64, 84
    RB = 2.3

    def mat(self):
        P = self.pal
        self.PELE = P('pele', ['#F2CFA8', '#D8A882', '#B07E5C', '#7E523A', '#44281A'], (0.78, 0.42, 0.10))
        self.ROUPA = P('manto', R['roxo'], (0.80, 0.44, 0.14))
        self.FORRO = P('forro', R['magenta'], (0.80, 0.44, 0.14))
        self.BORDA = P('borda', R['lilas'], (0.86, 0.50, 0.16))
        self.CALCA = self.ROUPA
        self.SAPATO = self.ROUPA
        self.SOLA = self.ROUPA
        self.FUMACA = P('fumaca', R['fumaca_roxa'], (0.70, 0.40, 0.12))
        self.OURO = P('ouro', R['ouro'], (0.70, 0.40, 0.12))
        self.BIG = P('bigode', R['preto_cab'], (0.82, 0.52, 0.22))
        self.ESTRELA = P('estrela', ['#FFFFFF', '#FFF6A0', '#FFD84A', '#E0A020', '#7A5010'])
        self.SOB = self.BIG.chars[2]
        self.CONTORNO_ROSTO = self.PELE.contorno

    def juntas(self, p):
        c = super().juntas(dict(p, hx=p.get('hx', 30)))
        sobe = p['extra'].get('sobe', 10)
        for k in list(c):
            if isinstance(c[k], tuple):
                c[k] = (c[k][0], c[k][1] - sobe)
        c['hy'] -= sobe
        return c

    def manga(self, b, ombro, cot, ang, esc):
        b.capsula(ombro, cot, 3.0, 3.4, self.ROUPA, esc)
        b.elipse(ponto(cot, 1.6, ang), 3.2, 2.4, self.FORRO, esc, giro=-ang)   # boca larga da manga

    def perna(self, b, c, lado, esc):
        pass   # flutua: sem pernas

    def fundo(self, b, c):
        hx, hy = c['hx'], c['hy']
        f = self.p['fase']
        # manto/capa abrindo atrás com forro magenta
        b.poligono([(hx - 4, hy - 16), (hx - 14 - 2 * math.sin(f), hy + 10), (hx - 6, hy + 6), (hx + 2, hy - 14)],
                   self.FORRO, 1, separar=False)
        # cauda de fumaça
        pts = corrente(b, (hx + 1, hy + 6), 26, 5.6, -40, f, self.FUMACA, n=5, afinar=0.2, amplitude=10)
        for p_ in pts[2:]:
            b.elipse((p_[0] - 1, p_[1] - 1.5), 1.8, 1.4, self.FUMACA, separar=False)

    def roupa_baixo(self, b, c):
        hx, hy = c['hx'], c['hy']
        b.poligono([(hx - 6, hy - 4), (hx + 6, hy - 4), (hx + 7, hy + 9), (hx + 1, hy + 12), (hx - 7, hy + 8)],
                   self.ROUPA, separar=False)
        b.capsula((hx - 6.5, hy + 8), (hx + 6.5, hy + 9), 1.0, 1.0, self.BORDA, separar=False)

    def tronco(self, b, c):
        super().tronco(b, c)
        pz = c['pescoco']
        hy = c['hy']
        # abertura do manto (forro magenta no meio) e gola alta
        b.poligono([(pz[0], pz[1] + 1), (pz[0] + 2.4, pz[1] + 1), (c['hx'] + 2, hy - 2), (c['hx'] - 0.5, hy - 2)],
                   self.FORRO, separar=False)
        b.elipse((pz[0] - 0.5, pz[1] - 0.5), 4.6, 2.6, self.BORDA, separar=False)

    def cabeca(self, b, c):
        cx, cy = c['cab']
        # capuz pontudo (atrás e em volta do rosto)
        b.poligono([(cx - 6, cy + 4), (cx - 5.5, cy - 4), (cx - 1, cy - 8), (cx - 10, cy - 15), (cx + 3, cy - 8),
                    (cx + 6.5, cy - 2), (cx + 5.5, cy + 2)], self.ROUPA, separar=False)
        b.capsula((cx - 5, cy - 4.8), (cx + 5.4, cy - 3.6), 1.0, 1.0, self.BORDA, separar=False)
        b.elipse((cx + 1.4, cy + 1.0), 4.0, 5.0, self.PELE, separar=False, achatar=0.65)   # rosto fino
        b.elipse((cx + 2.6, cy + 3.8), 2.2, 2.4, self.PELE, separar=False, achatar=0.6)

    def rosto(self, b, c):
        super().rosto(b, c)
        cx, cy = c['cab']
        bc = self.BIG.chars
        # bigode enrolado e cavanhaque pontudo
        for x, y in ((cx + 1.4, cy + 3.6), (cx + 2.4, cy + 3.4), (cx + 4.6, cy + 3.4), (cx + 5.6, cy + 3.6),
                     (cx + 0.6, cy + 3.0), (cx + 6.4, cy + 3.0), (cx + 0.4, cy + 2.2)):
            b.px(x, y, bc[1])
        for y in range(0, 4):
            b.px(cx + 3.4, cy + 6.0 + y, bc[1] if y < 3 else bc[2])

    def detalhes(self, b, c):
        px, py = c['peito']
        b.elipse((px + 1.0, py + 1.6), 1.8, 1.8, self.OURO, separar=False)    # medalhão de lua
        b.px(px + 1.6, py + 1.2, self.ROUPA.chars[2])

    def na_mao(self, b, c):
        m = c['mao_f_pt']
        ang = self.p['extra'].get('varinha', 170)
        topo = ponto(m, 12, ang)
        b.capsula(ponto(m, 3, ang + 180), topo, 0.8, 0.8, self.OURO, separar=False)
        brilho = self.p['extra'].get('brilho', 1.0)
        for k in range(5):   # estrela de 5 pontas
            a = k * 72 + 180
            b.capsula(topo, ponto(topo, 3.6 * brilho, a), 1.2, 0.5, self.ESTRELA, separar=False)
        b.elipse(topo, 1.6, 1.6, self.ESTRELA, separar=False)


# ===============================================================================================================
# Gênio (versão da escola): grande, flutuando, pele lilás, turbante rosa com joia, cavanhaque, brinco de argola,
# colete rosa aberto, faixa amarela, braceletes dourados e cauda de fumaça amarela. Nada do Gênio do filme.
# ===============================================================================================================

class Genio(Humano):
    S = 1.5
    LARG = 1.9
    L, A = 88, 104
    RB = 3.6

    def mat(self):
        P = self.pal
        self.PELE = P('pele', R['pele_lilas'], (0.78, 0.42, 0.10))
        self.ROUPA = P('colete', R['rosa'], (0.86, 0.50, 0.16))
        self.TURB = P('turbante', R['magenta'], (0.80, 0.44, 0.14))
        self.CALCA = self.PELE
        self.SAPATO = self.PELE
        self.SOLA = self.PELE
        self.FAIXA = P('faixa', R['ouro'], (0.70, 0.40, 0.12))
        self.FUMACA = P('fumaca', R['fumaca'], (0.70, 0.40, 0.12))
        self.BARBA = P('barba', R['preto_cab'], (0.82, 0.52, 0.22))
        self.JOIA = P('joia', R['verde'])
        self.SOB = self.BARBA.chars[2]
        self.CONTORNO_ROSTO = self.PELE.contorno

    def juntas(self, p):
        c = super().juntas(dict(p, hx=p.get('hx', 40)))
        for k in list(c):
            if isinstance(c[k], tuple):
                c[k] = (c[k][0], c[k][1] - 12)
        c['hy'] -= 12
        return c

    def perna(self, b, c, lado, esc):
        pass

    def fundo(self, b, c):
        hx, hy = c['hx'], c['hy']
        pts = corrente(b, (hx + 1, hy + 2), 44, 10, -20, self.p['fase'], self.FUMACA, n=6, afinar=0.15,
                       amplitude=16)
        for p_ in pts[2:]:
            b.elipse((p_[0] + 3, p_[1] - 2), 3.0, 2.4, self.FUMACA, separar=False)

    def tronco(self, b, c):
        hx, hy, lt = c['hx'], c['hy'], self.LARG
        # peito largo à mostra, colete aberto por cima
        b.capsula(c['peito'], (hx, hy - 2), 4.6 * lt, 3.6 * lt, self.PELE, separar=False, achatar=0.92)
        b.elipse((c['peito'][0] + 0.4, c['peito'][1] - 1.5), 4.8 * lt, 4.0, self.PELE, separar=False, achatar=0.9)
        pz = c['pescoco']
        b.poligono([(pz[0] - 9, pz[1] + 2), (pz[0] - 2, pz[1] + 2), (hx - 3, hy - 2), (hx - 9, hy - 2)],
                   self.ROUPA, separar=False)
        b.poligono([(pz[0] + 4, pz[1] + 2), (pz[0] + 9, pz[1] + 3), (hx + 8, hy - 2), (hx + 5, hy - 2)],
                   self.ROUPA, 1, separar=False)

    def cintura(self, b, c):
        hx, hy = c['hx'], c['hy']
        b.capsula((hx - 8, hy - 2.5), (hx + 8, hy - 3), 2.6, 2.6, self.FAIXA, separar=False)

    def manga(self, b, ombro, cot, ang, esc):
        pass

    def braco(self, b, c, lado, esc):
        m = super().braco(b, c, lado, esc)
        cot = c['cot_' + lado]
        pulso = mistura(cot, m, 0.75)
        b.elipse(pulso, 2.6, 2.6, self.FAIXA, esc, separar=False)            # bracelete
        return m

    def cabeca(self, b, c):
        cx, cy = c['cab']
        k = 1.5
        b.elipse((cx + 0.8, cy + 0.6), 4.4 * k, 4.9 * k, self.PELE, separar=False, achatar=0.65)
        b.elipse((cx + 2.8, cy + 3.6), 3.0 * k, 2.6 * k, self.PELE, separar=False, achatar=0.6)
        b.elipse((cx - 2.4, cy + 1.2), 1.5, 2.1, self.PELE, 1, separar=False, achatar=0.8)
        b.elipse((cx + 0.6, cy - 5.6), 8.4, 5.6, self.TURB, separar=False)             # turbante
        b.capsula((cx - 7, cy - 3.2), (cx + 7.4, cy - 4.4), 1.4, 1.4, self.TURB, 1, separar=False)
        b.elipse((cx + 3.4, cy - 6.0), 1.8, 2.0, self.JOIA, separar=False)
        b.elipse((cx - 2.8, cy + 4.4), 1.4, 1.4, self.FAIXA, separar=False)            # brinco de argola
        b.capsula((cx + 4.0, cy + 7.6), (cx + 5.0, cy + 11), 1.6, 0.6, self.BARBA, separar=False)   # cavanhaque

    def rosto(self, b, c):
        cx, cy = c['cab']
        # escala do rosto maior: reposiciona e reaproveita
        super().rosto(b, c | {'cab': (cx + 1.2, cy + 1.4)})


# ===============================================================================================================
# Abu (versão da escola): macaco-prego (o macaquinho brasileiro), pelo marrom, rosto e barriga claros, boné/topete
# escuro do macaco-prego e lenço rosa da escola no pescoço. Sem colete e chapéu do filme.
# ===============================================================================================================

class Abu:
    L, A = 36, 40

    def __init__(self):
        self.pal = Paleta()
        P = self.pal
        self.PELO = P('pelo', R['pelo'], (0.78, 0.44, 0.14))
        self.CLARO = P('claro', R['pelo_claro'], (0.78, 0.42, 0.12))
        self.TOPETE = P('topete', R['preto_cab'], (0.82, 0.52, 0.22))
        self.LENCO = P('lenco', R['rosa'], (0.86, 0.50, 0.16))
        self.CHAPEU = P('chapeu', R['azul'], (0.80, 0.46, 0.14))

    def desenhar(self, pose_):
        b = Boneco(self.L, self.A)
        P, C = self.PELO, self.CLARO
        if pose_ == 'parado':
            hx, hy = 15, 26
            corrente(b, (hx - 4, hy + 4), 16, 1.2, -60, 0.5, P, 1, n=5, afinar=0.08, amplitude=30)  # rabo em espiral
            b.capsula((hx - 1, hy + 4), (hx - 3, hy + 11), 2.2, 2.0, P, 1)                  # perna de trás
            b.capsula((hx + 2, hy + 4), (hx + 3, hy + 11), 2.2, 2.0, P)
            b.elipse((hx - 3.5, hy + 12), 2.2, 1.2, C, 1); b.elipse((hx + 4, hy + 12), 2.2, 1.2, C)
            b.capsula((hx, hy - 4), (hx + 0.5, hy + 4), 4.2, 4.6, P, achatar=0.9)            # corpo
            b.elipse((hx + 1.6, hy + 1.5), 2.4, 3.6, C, separar=False)                       # barriga
            b.capsula((hx - 2, hy - 3), (hx - 4, hy + 5), 1.4, 1.2, P, 1)                    # braço de trás
            b.capsula((hx + 2.5, hy - 3), (hx + 5, hy + 4), 1.4, 1.2, P)                     # braço da frente
            cab = (hx + 1, hy - 9)
        elif pose_ == 'correndo':
            hx, hy = 15, 29
            corrente(b, (hx - 6, hy), 16, 1.2, -110, 1.5, P, 1, n=5, afinar=0.08, amplitude=20)
            b.capsula((hx - 4, hy + 2), (hx - 9, hy + 8), 2.0, 1.8, P, 1)
            b.capsula((hx + 3, hy + 2), (hx + 8, hy + 8), 2.0, 1.8, P)
            b.capsula((hx - 6, hy - 1), (hx + 4, hy - 3), 4.0, 4.2, P, achatar=0.9)            # corpo deitado
            b.capsula((hx + 3, hy - 3), (hx + 9, hy + 4), 1.4, 1.2, P)
            b.capsula((hx + 1, hy - 3), (hx - 3, hy + 5), 1.4, 1.2, P, 1)
            cab = (hx + 7, hy - 8)
        else:  # aflito: pulando, braços para cima
            hx, hy = 15, 24
            corrente(b, (hx - 4, hy + 4), 16, 1.2, -40, 2.5, P, 1, n=5, afinar=0.08, amplitude=30)
            b.capsula((hx - 1, hy + 4), (hx - 4, hy + 9), 2.2, 2.0, P, 1)
            b.capsula((hx + 2, hy + 4), (hx + 5, hy + 9), 2.2, 2.0, P)
            b.capsula((hx, hy - 4), (hx + 0.5, hy + 4), 4.2, 4.6, P, achatar=0.9)
            b.elipse((hx + 1.6, hy + 1.5), 2.4, 3.6, C, separar=False)
            b.capsula((hx - 2, hy - 3), (hx - 6, hy - 12), 1.4, 1.2, P, 1)
            b.capsula((hx + 2.5, hy - 3), (hx + 6, hy - 12), 1.4, 1.2, P)
            cab = (hx + 1, hy - 9)
        cx, cy = cab
        b.elipse((cx - 3.6, cy - 0.4), 1.8, 2.0, C, 1)                                        # orelha
        b.elipse((cx, cy), 4.6, 4.4, P)                                                     # cabeça
        b.elipse((cx + 1.6, cy + 1.2), 3.0, 2.8, C, separar=False)                         # rosto claro
        b.elipse((cx + 0.2, cy - 3.6), 3.6, 1.6, self.TOPETE, separar=False)               # topete do macaco-prego
        # chapeuzinho azul (boina redonda inclinada com bolinha; pedido do Pedro, 01/11/2026)
        b.elipse((cx + 0.6, cy - 4.6), 4.2, 2.6, self.CHAPEU, separar=False)
        b.capsula((cx - 3.4, cy - 3.2), (cx + 4.4, cy - 4.0), 0.8, 0.8, self.CHAPEU, 1, separar=False)
        b.elipse((cx + 1.4, cy - 7.4), 1.2, 1.2, self.CHAPEU, separar=False)
        b.capsula((cx - 3, cy + 4.5), (cx + 3, cy + 5.2), 1.3, 1.3, self.LENCO, separar=False)   # lenço
        b.poligono([(cx - 3, cy + 4), (cx - 6, cy + 8), (cx - 2, cy + 6)], self.LENCO, separar=False)
        olho = 'e'
        if pose_ == 'aflito':
            b.px(cx + 1, cy - 0.4, 'w'); b.px(cx + 1, cy + 0.6, olho); b.px(cx + 3, cy - 0.4, 'w'); b.px(cx + 3, cy + 0.6, olho)
            b.px(cx + 2, cy + 3, 'q'); b.px(cx + 2, cy + 4, 'n')
        else:
            b.px(cx + 1, cy, olho); b.px(cx + 3, cy, olho); b.px(cx + 1, cy - 1, 'w')
            b.px(cx + 2, cy + 2.6, 'q'); b.px(cx + 3, cy + 2.4, 'q')
        return b

    def img(self, pose_):
        linhas = self.desenhar(pose_).texto({k: self.PELO.contorno for k in EXTRAS})
        pal = self.pal.paleta()
        im = Image.new('RGBA', (self.L, self.A), (0, 0, 0, 0))
        for y, l in enumerate(linhas):
            for x, ch in enumerate(l):
                if ch != '.':
                    h = pal[ch].lstrip('#')
                    im.putpixel((x, y), tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
        return im


# ===============================================================================================================
# Pranchas
# ===============================================================================================================

def fonte(t, negrito=False):
    from PIL import ImageFont
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if negrito else ''), t)


def recortar(im):
    return im.crop(im.getbbox())


def poses():
    """{nome: (titulo, [(rotulo, imagem)], design)}"""
    tp, tc, ja, su, jf, ge, ab = TiaPaula(), TiaClaudia(), Jasmine(), Sultao(), Jafar(), Genio(), Abu()
    return {
        'tia-paula': ('Tia Paula', [
            ('parada', tp.img(respirar(0))),
            ('socorro (gaiola)', tp.img(respirar(1, ombro_f=115, cotovelo_f=25, ombro_t=100, cotovelo_t=30,
                                                  rosto='socorro'))),
            ('feliz', tp.img(respirar(2, ombro_f=45, cotovelo_f=105, ombro_t=40, cotovelo_t=100, rosto='feliz',
                                      extra={'rabo': 15}))),
            ('microfone (Final)', tp.img(respirar(0, ombro_f=60, cotovelo_f=95, rosto='fala',
                                                  extra={'microfone': True}))),
            ('sentada (tapete)', tp.img(pose(sentado=True, hy=44, coxa_f=80, joelho_f=90, pe_f=0, coxa_t=75,
                                             joelho_t=85, ombro_f=30, cotovelo_f=40, rosto='feliz'))),
        ], 'loira de rabo de cavalo, camiseta preta do espetáculo (Aladdin dourado, fumaça azul e roxa, lâmpada); '
           'jeans e tênis brancos (neutros até a foto)'),
        'tia-claudia': ('Tia Claudia', [
            ('parada', tc.img(respirar(0))),
            ('fala', tc.img(respirar(1, rosto='fala', ombro_f=20, cotovelo_f=60))),
            ('entrega os ingressos', tc.img(respirar(0, ombro_f=75, cotovelo_f=10, rosto='feliz',
                                                     extra={'ingressos': True}))),
        ], 'cabelo preto no ombro e óculos (seção 8); camiseta rosa da escola com os quadradinhos do logo, '
           'calça escura e sapatilha (neutros até a foto)'),
        'jasmine': ('Jasmine', [
            ('parada', ja.img(respirar(0, ombro_f=-20, cotovelo_f=60))),
            ('pirueta 1', ja.img(pose(ombro_f=160, cotovelo_f=-40, ombro_t=165, cotovelo_t=-40, coxa_f=0,
                                      joelho_f=0, coxa_t=-30, joelho_t=80, ponta=True, rosto='feliz',
                                      braco_t_atras=False, extra={'giro': 0.6}, fase=1.5))),
            ('pirueta 2', ja.img(pose(ombro_f=95, cotovelo_f=0, ombro_t=-95, cotovelo_t=0, coxa_f=0, joelho_f=0,
                                      coxa_t=25, joelho_t=70, ponta=True, rosto='fechado', extra={'giro': 1.0},
                                      fase=3.0))),
        ], 'bailarina da escola: trança, tiara, blusa lilás de manga bufante, saia longa rosa com cinto de '
           'moedas, sapatilhas (sem o top e a calça do filme)'),
        'sultao': ('Sultão', [
            ('parado', su.img(respirar(0, ombro_f=-10, cotovelo_f=30))),
            ('palmas', su.img(respirar(1, ombro_f=55, cotovelo_f=60, ombro_t=50, cotovelo_t=70, rosto='feliz',
                                       braco_t_atras=False))),
        ], 'robusto, turbante rosa com pena e joia, barba branca, túnica creme, faixa dourada, capa roxa'),
        'jafar': ('Jafar', [
            ('flutuando', jf.img(pose(ombro_f=20, cotovelo_f=70, ombro_t=10, cotovelo_t=20, rosto='bravo',
                                      extra={'varinha': 160}))),
            ('lançando', jf.img(pose(ombro_f=120, cotovelo_f=-30, ombro_t=-30, cotovelo_t=20, rosto='bravo',
                                     fase=1.2, extra={'varinha': 170, 'brilho': 1.4}))),
            ('cansado / tonto', jf.img(pose(tronco=14, cabeca=8, ombro_f=-10, cotovelo_f=10, rosto='tonto',
                                            fase=2.4, extra={'varinha': 230, 'sobe': 2}))),
        ], 'design próprio mantido: capuz roxo pontudo com beirada lilás, bigode enrolado, cavanhaque, forro '
           'magenta, medalhão de lua, varinha de estrela, cauda de fumaça'),
        'genio': ('Gênio', [
            ('flutuando', ge.img(pose(ombro_f=-20, cotovelo_f=100, ombro_t=-10, cotovelo_t=90, rosto='feliz'))),
            ('tchan!', ge.img(pose(ombro_f=150, cotovelo_f=10, ombro_t=160, cotovelo_t=0, braco_t_atras=False,
                                   rosto='fala', fase=1.6))),
        ], 'pele lilás, turbante magenta com joia verde, cavanhaque, brinco de argola, colete rosa aberto, faixa '
           'e braceletes dourados, cauda de fumaça amarela'),
        'abu': ('Abu', [('parado', ab.img('parado')), ('correndo', ab.img('correndo')), ('aflito', ab.img('aflito'))],
                'macaco-prego (o macaquinho brasileiro), chapeuzinho azul (boina com bolinha), rosto e barriga claros, '
                'lenço rosa da escola'),
    }


ATUAL = {'tia-paula': ('chefe', 'tiaPaula'), 'tia-claudia': ('espaco', 'claudia'), 'jasmine': ('espaco', 'jasmine'),
         'sultao': ('espaco', 'sultao'), 'jafar': ('chefe', 'jafar'), 'genio': ('espaco', 'genio'),
         'abu': ('espaco', 'abu')}


def heroi():
    from previa_elenco import carregar_sprites, quadro_img
    d = carregar_sprites()
    j = d['jogador']
    return quadro_img(j['QUADROS']['parado1'], j['PALETA']), d


def prancha_personagem(nome, titulo, lista, design, atual, k=5):
    itens = [('atual (hoje no jogo)', atual)] + lista
    base = max(im.height for _, im in itens)
    W = sum(max(im.width * k + 30, 190) for _, im in itens) + 40
    H = base * k + 190
    out = Image.new('RGBA', (W, H), (34, 26, 48, 255))
    d = ImageDraw.Draw(out)
    d.text((20, 14), f'{titulo} · proposta (ampliado {k}×)', font=fonte(26, True), fill=(255, 255, 255))
    d.text((20, 50), design, font=fonte(16), fill=(220, 205, 240))
    y0 = 90
    chao = y0 + base * k
    d.line([(10, chao), (W - 10, chao)], fill=(255, 176, 250), width=2)
    x = 30
    for i, (rot, im) in enumerate(itens):
        g = im.resize((im.width * k, im.height * k), Image.NEAREST)
        out.alpha_composite(g, (x, chao - g.height))
        cor = (255, 214, 160) if i == 0 else (255, 214, 251)
        d.text((x, chao + 10), rot, font=fonte(16, True), fill=cor)
        d.text((x, chao + 32), f'{im.height} px', font=fonte(15), fill=(200, 190, 220))
        x += max(g.width + 30, 190)
        if i == 0:
            d.line([(x - 15, y0), (x - 15, chao + 50)], fill=(90, 80, 120), width=2)
    return out


def main():
    os.makedirs(NATIVO, exist_ok=True)
    h, dados = heroi()
    ps = poses()
    for nome, (titulo, lista, design) in ps.items():
        m, k = ATUAL[nome]
        sp = dados[m]['SPRITES'][k]
        from previa_elenco import quadro_img
        atual = quadro_img(sp['quadros'][0], dados[m]['PALETA'])
        lista = [(r, recortar(im)) for r, im in lista]
        for r, im in lista:
            im.save(os.path.join(NATIVO, f"{nome}-{r.split(' ')[0]}.png"))
        prancha_personagem(nome, titulo, lista, design, atual).save(os.path.join(SAIDA, f'proposta-{nome}.png'))
    # elenco lado a lado, na escala do jogo
    k = 4
    elenco = [('Aladdin', h)] + [(t, recortar(l[0][1])) for _, (t, l, _) in ps.items()]
    W = sum(max(im.width * k + 36, 150) for _, im in elenco) + 40
    base = max(im.height for _, im in elenco)
    H = base * k + 170
    out = Image.new('RGBA', (W, H), (34, 26, 48, 255))
    d = ImageDraw.Draw(out)
    d.text((20, 14), 'Proposta: elenco novo na escala do jogo (ampliado 4×; herói = 58 px)', font=fonte(26, True),
           fill=(255, 255, 255))
    d.text((20, 50), 'Mesmo renderizador e mesma luz do herói: 4 tons por material e contorno colorido. '
           'Designs provisórios até as fotos dos figurinos.', font=fonte(16), fill=(220, 205, 240))
    chao = 90 + base * k
    d.line([(10, chao), (W - 10, chao)], fill=(255, 176, 250), width=2)
    d.line([(10, chao - 58 * k), (W - 10, chao - 58 * k)], fill=(110, 100, 140), width=1)
    x = 30
    for nome, im in elenco:
        g = im.resize((im.width * k, im.height * k), Image.NEAREST)
        # Gênio e Jafar flutuam: sobem um pouco
        sobe = 6 * k if nome == 'Gênio' else 4 * k if nome == 'Jafar' else 0
        out.alpha_composite(g, (x, chao - g.height - sobe))
        d.text((x, chao + 10), nome, font=fonte(18, True), fill=(255, 255, 255))
        d.text((x, chao + 34), f'{im.height} px', font=fonte(15), fill=(200, 190, 220))
        x += max(g.width + 36, 150)
    out.save(os.path.join(SAIDA, 'proposta-elenco.png'))
    print('ok', SAIDA)


if __name__ == '__main__':
    main()
