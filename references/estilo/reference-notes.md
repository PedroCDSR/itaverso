# Notas · estilo (guia de linguagem visual)

**Objetivo:** fixar o padrão de qualidade da pixel art do jogo. As capturas do Aladdin do SNES (Capcom/Disney, 1993)
são o alvo de **linguagem e acabamento**: escala, tons, contorno, luz, densidade de detalhe e animação.
**Não** são modelo de design de personagem nem de composição de tela (regra 3).

Medido na Etapa 8.0 (01/11/2026). As capturas foram reduzidas para a resolução nativa do SNES (256×224) antes de
medir; como são JPEG, as cores abaixo são aproximadas (agrupadas por mediana) e servem de **faixa**, não de valor exato.

## Imagens

| Arquivo | Tamanho | O que mostra | Para que olhar |
|---|---|---|---|
| `snes-mercado-toldos.jpg` | 600×498 (≈ 2,3× a tela nativa) | Mercado: parede de terracota com rachaduras, barracas com toldos de pano, objetos de feira, pano roxo em primeiro plano | Escala do herói, densidade de detalhe, toldos com dobras, camada da frente |
| `snes-pulo-mercado.jpg` | 527×379 | Herói no meio do pulo, mesmo cenário | Pose de pulo aberta, silhueta legível |
| `snes-voo-pano-portao.jpg` | 1280×720 (tela de 852×720 no meio) | Herói descendo com um pano, portão de arenito, céu com nuvens | Arenito em 4 a 5 tons, camadas de fundo |
| `snes-tapete.jpg` | 516×387 | Voo noturno: lua, estrelas, nuvens, pássaros | Céu escuro quase liso, brilho da lua, nuvens em faixas |
| `snes-corda.jpg` | 250×207 | Descida por corda, cidade e palácio ao fundo | Profundidade: fundo dessaturado e puxado para a cor do céu |

## Medidas do herói (nas capturas → alvo no nosso jogo)

| Item | Medido nas capturas | Alvo no jogo (480×270) | Atingido na 8.0 |
|---|---|---|---|
| Altura do herói em pé | ≈ 54 a 56 px numa tela de 224 (cabelo ao pé, sem o chapéu) = **24 a 25%** da altura. A leitura antiga de "≈ 28%" contava o chapéu e a esticada da captura | corpo de **56 a 60 px** num quadro de **48×64** = 21 a 22% (a nossa tela é mais larga, 16:9, e precisa mostrar mais caminho à frente) | **58 px = 21,5%** (linhas 6 a 63 do quadro, com contorno) |
| Largura parado | ≈ 18 a 20 px | 18 a 22 px | 20 px |
| Cabeça | do alto do cabelo ao queixo ≈ 10 a 11 px = **1/5** da altura; rosto ≈ 1/6 | cabeça com cabelo ≈ 1/4,5; rosto ≈ 1/6. Nada de proporção "cabeçuda" | cabelo + rosto 13 px (1/4,5); rosto 9 px (1/6,4) |
| Pernas | ≈ metade da altura (quadril na metade do corpo) | idem | quadril na linha 35 (pé na 62): pernas = 27 de 56 |
| Silhueta | esguia, ombros estreitos, braços longos e soltos do corpo nas poses | idem; mãos 1 px maiores que o pulso para ler no celular | idem |
| Caixa de colisão | — | menor que o desenho: só do ombro ao pé | 18×46 (cabe nos vãos de 3 tiles = 48 px) |

## Cor, luz e contorno

| Item | Nas capturas | Regra para o jogo |
|---|---|---|
| Tons por material | pele 3 a 4, tecido 3 a 4, metal 4 com brilho; arenito 4 a 5 | **4 tons por material** (brilho, base, sombra, sombra funda) + 1 cor de contorno própria do material. Sem degradê nem pontilhado nos sprites |
| Contorno | escuro e **colorido** (marrom, vinho), não preto puro; some por dentro da forma | 1 px, na cor de contorno do material vizinho (ex.: pele `#4A2216`, túnica `#173A20`, calça `#4A321C`). Linha interna só onde uma parte passa na frente de outra, no tom mais escuro da parte de **trás** |
| Luz | de cima e de um lado, igual para todos na cena | **de cima e da frente do personagem** (vetor 0,55 / −0,75 / 0,55 em `ferramentas/arte/modelo.py`). Partes do lado de trás do corpo (braço e perna mais longe) ficam 1 tom mais escuras. Ao espelhar o sprite, a luz espelha junto (convenção do gênero) |
| Saturação | personagens mais saturados que o fundo | personagem sempre mais saturado e mais contrastado que a camada em que está |

## Paleta de cenário (compatível com a paleta da escola)

Os cenários usam cores quentes de fim de tarde; menus, HUD e botões continuam na paleta da escola (CLAUDE.md, seção 7).
Cada material tem 4 a 5 tons, da luz à sombra funda. Faixas medidas nas capturas → valores para o jogo:

| Material | Nas capturas (aprox.) | Nossa rampa (luz → sombra funda) | Ligação com a escola |
|---|---|---|---|
| Arenito (muros, pedra) | `#B8854E` `#AA7840` `#925C31` `#804833` `#72312A` | `#F1D49A` `#D9B475` `#B98D55` `#8E6440` `#5E3F2E` | luz puxada para o amarelo `#F9FCBB` |
| Terracota (reboco, telhado) | `#C96540` `#BE4F34` `#913A1C` | `#E8875E` `#C9623E` `#A0472C` `#73301F` `#4A1E18` | sombra funda puxada para o roxo `#6D6BD9` |
| Areia e chão de terra | `#EEDF94` `#E4C880` `#DAB26C` `#BE8746` `#9A4942` | `#F7E7B0` `#E6CB8C` `#C9A36A` `#9C7448` `#6A4A34` | — |
| Madeira (toldo, porta) | `#634026` | `#C08A55` `#955F37` `#6A3D22` `#472513` | igual ao couro do herói |
| Pano de toldo rosa | `#D06846` `#B90D59` `#82072D` | `#FFD6FB` `#FFB0FA` `#D17ACB` `#94489A` `#4C1E52` | rosa `#FFB0FA` como tom base |
| Pano de toldo verde | `#21C181` `#2E7E66` `#28464E` | `#B5E99A` `#6CC24A` `#3F8C3A` `#285E2E` `#173A20` | verde `#6CC24A` como tom base |
| Céu de entardecer | dia: `#6C67CE` `#9084C8`; noite: `#210842` | alto `#7C7CE0` → `#9E9EFF` → `#C8A2F0` → horizonte `#F7B6D8` | lilás `#9E9EFF` no meio do céu |
| Fundo distante (cidade, morros) | `#A06D7C` `#946170` `#8C5A65` `#784954` `#653943` | `#C6A3D6` `#A487C4` `#8A6FB2` `#6E59A0` | puxado para o lilás/roxo do céu, pouco contraste |
| Pano de primeiro plano | `#920AA5` `#702058` | `#8A5BD0` `#6D6BD9` `#4F4DB0` `#36347E` | roxo `#6D6BD9` |

## Cenário: densidade, camadas e ritmo

| Item | Nas capturas | Alvo no jogo |
|---|---|---|
| Superfícies grandes | parede com rachaduras, tijolos aparentes e manchas a cada ~40 px; nunca uma cor lisa | nenhuma superfície maior que 2 tiles com uma cor só; detalhe (rachadura, tijolo, mancha, janela) a cada 2 a 3 tiles |
| Objetos | algo de interesse a cada ~1/3 de tela (barraca, janela em arco, vaso, cesto) | idem: pelo menos 3 pontos de interesse por tela de 480 px |
| Camadas | 3 de fundo (céu, cidade dessaturada, construções do meio) + jogo + primeiro plano ocasional (panos roxos na frente, cortando a borda de baixo) | 3 camadas de parallax (0,15 / 0,35 / 0,6) + jogo + 1 elemento de primeiro plano a cada 2 ou 3 telas, sem esconder o herói |
| Contraste por profundidade | fundo com 2 a 3 tons, baixo contraste; meio com 4; jogo com 4 a 5 e contorno | idem |

## Animação

| Item | Nas capturas / no gênero | Alvo | Atingido na 8.0 (herói) |
|---|---|---|---|
| Parado | respiração e movimento secundário | 2 a 4 quadros | 4 (respira; pontas da faixa balançam) |
| Corrida | muitos quadros, corpo inclinado, braços opostos | 6 a 8 quadros | 8 a 16 qps, corpo inclinado 12°, sobe e desce 1,6 px |
| Pulo / queda | pose aberta, silhueta clara | 1 a 2 cada | 2 + 2 |
| Arremesso | antecipação (braço atrás) e exagero | 2 a 3, com antecipação | 3 (antecipa → solta → acompanha); a maçã sai depois da antecipação (60 ms) |
| Dano | recuo e expressão | 1 | 1 (corpo arqueado, olhos apertados) |
| Movimento secundário | panos e cabelo seguem o movimento | panos com onda própria por quadro | faixa da cabeça e da cintura com onda e vento por quadro |

## Como gerar personagens neste padrão

`ferramentas/arte/modelo.py` desenha o personagem a partir de volumes (cápsulas e elipses) com material, aplica a
luz em 4 tons, a linha de separação e o contorno colorido. `ferramentas/arte/gerar_jogador.py` é o exemplo completo
(esqueleto, poses, rosto à mão). Os demais personagens (Etapa 8A) devem usar o mesmo renderizador, a mesma luz e a
mesma escala (quadros de 48×64, adultos com 56 a 60 px; crianças e o Abu, menores).

## Validação

Toda arte nova ganha uma prancha "referência × nossa" na mesma escala em `ferramentas/arte/previas/`, com as
diferenças anotadas no índice. "Dá para reconhecer" não é critério de conclusão.
