"""Gera o mapa da Fase 2 (Espaço Paula De Marco) em src/levels/espaco.js.

Estúdio de 100 colunas (1.600 px): correndo direto são ~12 s; com as 4 conversas, a entrega dos ingressos e a
chegada do Abu, a fase fica em 30 a 45 s. Tablados (=) em escada com sapatilhas em cima, para ter o que pular.
Alturas: pulo alto ≈ 69 px (4 tiles); tablado na linha 12 = 3 tiles acima do piso; na linha 10 = 5 tiles
(alcançável a partir do tablado da linha 12).
Uso: python3 ferramentas/mapas/gerar_espaco.py > src/levels/espaco.js
"""

L, A = 100, 17


def novo(larg):
    grade = [['.'] * larg for _ in range(A)]
    for y in (15, 16):
        for x in range(larg):
            grade[y][x] = '#'
    return grade


g = novo(L)


def p(x, y, c):
    g[y][x] = c


def arco(x0, y_base=13):
    for i, dy in enumerate((0, 1, 2, 1, 0)):
        p(x0 + i, y_base - dy, 's')


def tablado(x0, y, larg=4):
    for x in range(x0, x0 + larg):
        p(x, y, '=')


p(3, 14, 'P')
arco(9)
p(20, 14, 'N')  # Jasmine, na barra
tablado(26, 12); tablado(32, 10)
p(27, 10, 's'); p(28, 10, 's'); p(33, 8, 's'); p(34, 8, 's')
p(42, 14, 'N')  # Gênio
arco(48)
p(60, 14, 'N')  # Sultão
tablado(66, 12); tablado(72, 10); tablado(78, 12)
p(67, 10, 's'); p(68, 10, 's'); p(73, 8, 's'); p(74, 8, 's'); p(79, 10, 's'); p(80, 10, 's')
p(90, 14, 'N')  # Tia Claudia, no balcão
INTEIRO = g

# Nível fácil (src/dificuldade.js): estúdio de 60 colunas, com os mesmos 4 personagens mais perto uns dos outros.
g = novo(60)
p(3, 14, 'P')
arco(8)
p(15, 14, 'N')  # Jasmine
tablado(20, 12)
p(21, 10, 's'); p(22, 10, 's')
p(28, 14, 'N')  # Gênio
arco(33)
p(40, 14, 'N')  # Sultão
tablado(45, 12)
p(46, 10, 's'); p(47, 10, 's')
p(53, 14, 'N')  # Tia Claudia
FACIL = g


def escrever(nome, grade):
    print(f'export const {nome} = [')
    for linha in grade:
        print(f"  '{''.join(linha)}',")
    print('];')


print("// Fase 2, Espaço Paula De Marco (CLAUDE.md, seção 11, cena 4): estúdio de dança, sem inimigos.")
print("// Legenda em leitor.js e no CLAUDE.md (seção 10). 'N' = personagem que conversa; quem é cada um, da esquerda")
print("// para a direita, está em NPCS_ESPACO. A fase termina na Tia Claudia (último 'N'), por isso não tem 'E'.")
print("// Gerado por ferramentas/mapas/gerar_espaco.py; dá para editar à mão.")
print("// ESPACO: níveis médio e difícil. ESPACO_FACIL: nível fácil (60 colunas, mesmos personagens).")
escrever('ESPACO', INTEIRO)
print()
escrever('ESPACO_FACIL', FACIL)
print()
print("// Quem é cada 'N' do mapa, da esquerda para a direita. As falas ficam em data/textos.js (espaco).")
print("export const NPCS_ESPACO = ['jasmine', 'genio', 'sultao', 'claudia'];")
