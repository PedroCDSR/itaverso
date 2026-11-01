# Prévia · lugares reais da Fase 1 (para aprovação do Pedro)

Só prévia: nada disto está ligado ao jogo (`src/` não foi alterado). Gerado por
`python3 ferramentas/arte/gerar_lugares.py` (usa `cenario.py`, novo, para prédios e objetos, e `modelo.py` para as
estátuas de bronze).

| Arquivo | O que é |
|---|---|
| `fase1-panorama.png` | tira da Fase 1 com os 6 lugares em ordem, casario, céu de entardecer, serra e o Aladdin (2×) |
| `fase1-telas.png` | 6 telas de 480×270 do jogo, uma por lugar (2×) |
| `1-clube-itajubense.png` … `6-praca-do-soldado.png` | prancha por lugar: foto × pixel art na mesma altura, com o Aladdin (58 px) |
| `nativo/tiles-paralelepipedo.png` | chão novo da rua: 3 variações de tile 16×16 de paralelepípedo (topo com meio-fio + meio) |
| `nativo/*.png` | cada lugar em 1×, pronto para virar textura (`cenario.para_matriz` gera a matriz de `src/art/`) |

Medidas (herói = 58 px, chão em y = 240): igreja 244 px de altura (4,2 heróis), clube 178 px (camada do fundo, tingida
16% para o lilás), café 174 px (toldo a 80 px do chão), posto 156 px com a placa (cabine 82 px), estátua no pedestal
156 px (soldado ≈ 60 px), helicóptero 248×112 px, fonte 172×108 px.

Fundo e chão (pedido do Pedro, 01/11/2026): rua de **paralelepípedo** de granito com meio-fio claro (no lugar do
chão de pedra terracota atual) e **Serra da Mantiqueira** ao fundo em 3 camadas verdes cobertas de mata (copas
redondas com luz de cima-esquerda; a camada mais longe é verde-azulada, com menos contraste, e a do meio tem
clareiras de pasto). Só na prévia: `src/art/tiles.js` e o `Preload` ainda não mudaram.

Padrão do guia aplicado: 5 tons por material (luz de cima e da esquerda-frente), contorno colorido do próprio
material, sombra projetada sob as cornijas, reboco com manchas, escorridos e rachaduras, céu em faixas sem degradê,
fundo puxado para o lilás.

Diferenças que ficam (e o motivo):
- Alturas comprimidas para caber na tela (convenção do gênero); portas e janelas mantidas do tamanho do herói.
- Busto e estátua sem traços de rosto: as fotos não mostram os rostos de perto (seção 7.1, não inventar).
- Posto: placa oval com aro azul e **ESSO** em vermelho no campo branco (decisão do Pedro, 01/11/2026: "pode chamar
  de Esso"). Letras de pixel desenhadas por nós, sem decalcar o logotipo oficial.
- Café: a lotérica vizinha virou uma placa clara sem nome; pessoas, carros, postes e fios ficaram de fora.
- Helicóptero de perfil (no jogo o cenário é de lado) e sem inscrições.
