# Notas · estilo (guia de linguagem visual)

**Objetivo:** fixar o padrão de qualidade da pixel art do jogo. As capturas do Aladdin do SNES (Capcom/Disney, 1993)
são o alvo de **linguagem e acabamento**: escala, tons, contorno, luz, densidade de detalhe e animação.
**Não** são modelo de design de personagem nem de composição de tela (regra 3).

## Imagens

| Arquivo | O que mostra | Para que olhar |
|---|---|---|
| `snes-mercado-toldos.jpg` | Mercado: parede de arenito com rachaduras, barracas com toldos de pano, objetos de feira, pano roxo em primeiro plano | Densidade de detalhe, toldos com dobras e 3 a 4 tons, camada da frente, escala do herói |
| `snes-pulo-mercado.jpg` | Herói no meio do pulo, mesmo cenário | Pose de pulo com braços e pernas abertos, leitura da silhueta |
| `snes-voo-pano-portao.jpg` | Herói descendo com um pano, portão de arenito, céu azul com nuvens | Arquitetura em 3 a 4 tons, sombra projetada, camadas de fundo |
| `snes-tapete.jpg` | Voo noturno: lua, estrelas, nuvens, pássaros | Céu em degradê com pontilhado, brilho da lua, nuvens em camadas |
| `snes-corda.jpg` | Descida por corda, cidade e palácio ao fundo | Profundidade com fundo dessaturado e silhuetas |

## Medidas-alvo (primeira leitura; a Etapa 8.0 confere e completa)

| Item | Nas capturas (aprox.) | Alvo no jogo (480×270) |
|---|---|---|
| Altura do herói | ≈ 60 a 66 px numa tela de 224 (≈ 28%) | corpo de 56 a 60 px num quadro de 48×64 (≈ 21 a 22%) |
| Proporção do corpo | cabeça ≈ 1/5 a 1/6 da altura, pernas longas, silhueta esguia e expressiva | idem: nada de proporção "cabeçuda" |
| Tons por material | pele 3 a 4, tecido 3 a 4 (luz, base, sombra, sombra funda), metal 4+ com brilho | mínimo de 3 tons por material, 4 nos tecidos grandes |
| Contorno | escuro e colorido (marrom/vinho), não preto puro; some por dentro da forma | contorno colorido 1 px, com quebra de luz no lado iluminado |
| Luz | vinda do alto e de um lado, consistente na cena | definir a direção por fase e manter em todos os sprites da fase |
| Paredes e chão | textura com rachaduras, tijolos aparentes e manchas; 4 a 6 tons | nenhuma superfície grande lisa com uma cor só |
| Densidade de cenário | objetos de feira, janelas em arco, panos, vasos; sempre algo a cada ~1/3 de tela | idem; repetição de tile disfarçada com variações |
| Camadas | fundo distante dessaturado + meio + jogo + primeiro plano ocasional | 3 camadas de parallax + elementos de primeiro plano |
| Animação | corrida com muitos quadros, antecipação e exagero nos arremessos | corrida de 6 a 8 quadros, arremesso com antecipação |

## Validação

Toda arte nova ganha uma prancha "referência × nossa" na mesma escala em `ferramentas/arte/previas/`, com as
diferenças anotadas no índice. "Dá para reconhecer" não é critério de conclusão.
