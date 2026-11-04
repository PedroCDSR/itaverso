"""Renderizador de personagens em pixel art a partir de um "boneco" (esqueleto + volumes).

Por que existe: desenhar 15 quadros à mão com 4 tons por material e contorno colorido é lento e cada quadro sai
diferente do outro. Aqui cada parte do corpo é um volume simples (cápsula afinada ou elipse) com um material.
O renderizador:

1. calcula, para cada pixel, a "normal" do volume (como se fosse um cilindro ou uma esfera) e a luz que chega nele
   (luz de cima e da frente do personagem, guia em references/estilo/reference-notes.md);
2. escolhe 1 de 4 tons do material (brilho, base, sombra, sombra funda), sem degradê nem pontilhado;
3. separa as partes que se sobrepõem com uma linha no tom mais escuro da parte de TRÁS (lê braço sobre peito,
   perna da frente sobre a de trás);
4. aplica o contorno de 1 px na cor de contorno do material vizinho (contorno colorido, nunca preto puro).

Detalhes que não são volume (olhos, boca, costuras, brilhos) são pintados depois, pixel a pixel.

O resultado é uma matriz de caracteres (um por pixel) e uma paleta, no formato de src/art/ (ver pixel.py).
"""
import math

# ---------------------------------------------------------------------------------------------------------------
# Materiais: 4 tons (0 brilho, 1 base, 2 sombra, 3 sombra funda) + contorno, cada um com um caractere próprio.
# limiares: quanto de luz (0..1) precisa para cada tom. Materiais brilhantes têm limiares mais baixos.
# ---------------------------------------------------------------------------------------------------------------


class Material:
    def __init__(self, nome, chars, cores, limiares=(0.80, 0.45, 0.12)):
        assert len(chars) == 5 and len(cores) == 5, nome
        self.nome = nome
        self.chars = chars  # 4 tons + contorno
        self.cores = cores
        self.limiares = limiares

    def tom(self, luz):
        a, b, c = self.limiares
        if luz >= a:
            return 0
        if luz >= b:
            return 1
        if luz >= c:
            return 2
        return 3

    @property
    def contorno(self):
        return self.chars[4]


def normalizar(v):
    n = math.sqrt(sum(c * c for c in v)) or 1.0
    return tuple(c / n for c in v)


# Luz: vem de cima e da frente do personagem (ele olha para +x) e um pouco da câmera.
LUZ = normalizar((0.55, -0.75, 0.55))


class Boneco:
    """Uma tela de L x A em que as partes são desenhadas de trás para a frente."""

    def __init__(self, largura, altura, luz=LUZ):
        self.L, self.A = largura, altura
        self.luz = luz
        self.mat = [[None] * largura for _ in range(altura)]  # Material do pixel
        self.tom = [[0] * largura for _ in range(altura)]
        self.parte = [[-1] * largura for _ in range(altura)]  # índice da parte (ordem de desenho)
        self.separar = [[False] * largura for _ in range(altura)]
        self.fixo = [[None] * largura for _ in range(altura)]  # caractere pintado à mão (vence tudo)
        self.n = 0

    # --- pintura de um pixel de volume ---
    def _pintar(self, x, y, mat, normal, escurecer, separar, parte):
        if not (0 <= x < self.L and 0 <= y < self.A):
            return
        nx, ny, nz = normal
        luz = nx * self.luz[0] + ny * self.luz[1] + nz * self.luz[2]
        luz = max(0.0, luz)
        t = min(3, mat.tom(luz) + escurecer)
        self.mat[y][x] = mat
        self.tom[y][x] = t
        self.parte[y][x] = parte
        self.separar[y][x] = separar
        self.fixo[y][x] = None

    def capsula(self, a, b, r0, r1=None, mat=None, escurecer=0, separar=True, achatar=1.0, pontas=True):
        """Cápsula de a até b com raio r0 (em a) e r1 (em b). Normal cilíndrica, arredondada nas pontas.
        achatar < 1 deixa a normal mais "chapada" (tecido largo); pontas=False corta as pontas retas."""
        if r1 is None:
            r1 = r0
        parte = self.n
        self.n += 1
        ax, ay = a
        bx, by = b
        dx, dy = bx - ax, by - ay
        comp2 = dx * dx + dy * dy or 1e-6
        rmax = max(r0, r1)
        x0, x1 = int(math.floor(min(ax, bx) - rmax - 1)), int(math.ceil(max(ax, bx) + rmax + 1))
        y0, y1 = int(math.floor(min(ay, by) - rmax - 1)), int(math.ceil(max(ay, by) + rmax + 1))
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                px, py = x + 0.5, y + 0.5
                t = ((px - ax) * dx + (py - ay) * dy) / comp2
                if not pontas and (t < 0 or t > 1):
                    continue
                tc = min(1.0, max(0.0, t))
                cx, cy = ax + dx * tc, ay + dy * tc
                r = r0 + (r1 - r0) * tc
                ox, oy = px - cx, py - cy
                d = math.sqrt(ox * ox + oy * oy)
                if d > r:
                    continue
                if r < 0.01:
                    continue
                nx, ny = ox / r * achatar, oy / r * achatar
                nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
                self._pintar(x, y, mat, (nx, ny, nz), escurecer, separar, parte)
        return parte

    def elipse(self, c, rx, ry, mat, escurecer=0, separar=True, achatar=1.0, giro=0.0):
        """Elipse (esfera achatada) centrada em c; giro em graus."""
        parte = self.n
        self.n += 1
        cx, cy = c
        g = math.radians(giro)
        cg, sg = math.cos(g), math.sin(g)
        rm = max(rx, ry)
        for y in range(int(cy - rm - 1), int(cy + rm + 2)):
            for x in range(int(cx - rm - 1), int(cx + rm + 2)):
                px, py = x + 0.5 - cx, y + 0.5 - cy
                u = (px * cg + py * sg) / rx
                v = (-px * sg + py * cg) / ry
                d2 = u * u + v * v
                if d2 > 1:
                    continue
                # normal de volta para o espaço da tela
                nx = (u * cg - v * sg) * achatar
                ny = (u * sg + v * cg) * achatar
                nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
                self._pintar(x, y, mat, (nx, ny, nz), escurecer, separar, parte)
        return parte

    def poligono(self, pts, mat, escurecer=0, separar=True, normal=None):
        """Polígono cheio. normal(x, y) -> (nx, ny, nz); sem ela, a normal é a de um cilindro vertical
        ao longo da largura do polígono naquela linha."""
        parte = self.n
        self.n += 1
        ys = [p[1] for p in pts]
        for y in range(int(math.floor(min(ys))), int(math.ceil(max(ys))) + 1):
            py = y + 0.5
            xs = []
            for i in range(len(pts)):
                (xa, ya), (xb, yb) = pts[i], pts[(i + 1) % len(pts)]
                if (ya <= py < yb) or (yb <= py < ya):
                    xs.append(xa + (py - ya) * (xb - xa) / (yb - ya))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                xa, xb = xs[i], xs[i + 1]
                for x in range(int(math.floor(xa)), int(math.ceil(xb))):
                    px = x + 0.5
                    if px < xa or px > xb:
                        continue
                    if normal:
                        n = normal(px, py)
                    else:
                        meio, meia = (xa + xb) / 2, max(0.5, (xb - xa) / 2)
                        nx = (px - meio) / meia * 0.95
                        n = (nx, 0.0, math.sqrt(max(0.0, 1 - nx * nx)))
                    self._pintar(x, y, mat, n, escurecer, separar, parte)
        return parte

    # --- pintura à mão (detalhes) ---
    def px(self, x, y, char):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.L and 0 <= y < self.A:
            self.fixo[y][x] = char

    def tom_em(self, x, y, mat, tom):
        """Força um tom de um material num pixel (ex.: dobra de tecido)."""
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.L and 0 <= y < self.A and self.mat[y][x] is not None:
            self.mat[y][x] = mat
            self.tom[y][x] = tom
            self.fixo[y][x] = None

    def ocupado(self, x, y):
        return 0 <= x < self.L and 0 <= y < self.A and (self.mat[y][x] is not None or self.fixo[y][x])

    def material_em(self, x, y):
        if 0 <= x < self.L and 0 <= y < self.A:
            return self.mat[y][x]
        return None

    # --- finalização ---
    def texto(self, contorno_fixo=None):
        """Aplica separação e contorno e devolve as linhas de caracteres.
        contorno_fixo: {char_fixo: char_de_contorno} para pixels pintados à mão que encostam no vazio."""
        L, A = self.L, self.A
        tom = [row[:] for row in self.tom]
        # 1. separação: pixel de uma parte de trás que encosta numa parte da frente vira sombra funda
        for y in range(A):
            for x in range(L):
                m = self.mat[y][x]
                if m is None or self.fixo[y][x]:
                    continue
                p = self.parte[y][x]
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if not (0 <= xx < L and 0 <= yy < A):
                        continue
                    q = self.parte[yy][xx]
                    if q > p and self.separar[yy][xx] and self.mat[yy][xx] is not None:
                        # só separa se o vizinho for de outro material ou se os dois forem "separáveis"
                        tom[y][x] = 3
                        break
        # 2. caracteres
        saida = [['.'] * L for _ in range(A)]
        for y in range(A):
            for x in range(L):
                if self.fixo[y][x]:
                    saida[y][x] = self.fixo[y][x]
                elif self.mat[y][x] is not None:
                    saida[y][x] = self.mat[y][x].chars[tom[y][x]]
        # 3. contorno colorido (4 vizinhos); usa o material do vizinho mais escuro do lado de dentro
        final = [row[:] for row in saida]
        for y in range(A):
            for x in range(L):
                if saida[y][x] != '.':
                    continue
                escolhido = None
                for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
                    xx, yy = x + dx, y + dy
                    if not (0 <= xx < L and 0 <= yy < A) or saida[yy][xx] == '.':
                        continue
                    m = self.mat[yy][xx]
                    if self.fixo[yy][xx]:
                        c = (contorno_fixo or {}).get(self.fixo[yy][xx])
                        if c:
                            escolhido = c
                        continue
                    if m is not None:
                        escolhido = m.contorno
                if escolhido:
                    final[y][x] = escolhido
        return [''.join(l) for l in final]


def paleta_de(materiais, extras=None):
    pal = {}
    for m in materiais:
        for ch, cor in zip(m.chars, m.cores):
            assert ch not in pal or pal[ch] == cor, f'caractere repetido {ch} em {m.nome}'
            pal[ch] = cor
    for ch, cor in (extras or {}).items():
        assert ch not in pal, f'caractere repetido {ch}'
        pal[ch] = cor
    return pal


# ----------------------------------------------------------------------------------------------
# Ferramentas de geometria para poses
# ----------------------------------------------------------------------------------------------

def ponto(origem, comprimento, angulo):
    """Ponto a 'comprimento' de 'origem' na direção 'angulo' (graus; 0 = para baixo, +90 = para a frente/+x)."""
    a = math.radians(angulo)
    return (origem[0] + comprimento * math.sin(a), origem[1] + comprimento * math.cos(a))


def mistura(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
