# Proposta · revisão dos personagens (Etapa 8A)

Base: sprites atuais de `src/art/` × medidas dos sheets do SNES (`references/estilo/sprites-spritedatabase/`, branch
do PR 22; usados só para medir altura e quadros, nunca como desenho). Prancha: `elenco-atual-x-escala.png`
(gerada por `ferramentas/arte/previa_elenco.py`). Telas atuais do jogo conferidas no Chromium (Espaço, Chefe, Tapete,
Final).

## O que está errado hoje

1. **Escala antiga (32×48):** só o Aladdin foi refeito na 8.0. Jasmine (44 px), Tia Claudia (42), Sultão (48),
   Gênio (44) e Jafar (50) ficaram **menores que o herói** (58). No SNES, o Jafar é maior que o herói, o Gênio é o
   maior do elenco (≈ 1,6×) e os adultos têm a altura do herói.
2. **Acabamento chapado:** feitos com o `pixel.py` antigo (2 tons por material, contorno escuro único). O herói usa
   4 tons + contorno colorido (`modelo.py`); lado a lado, o elenco parece de outro jogo.
3. **Poucos quadros:** NPCs com 2 quadros; no SNES, NPCs têm 4 a 6 e os chefes dezenas.
4. **Tia Paula errada e triplicada:** coque castanho e vestido roxo (o certo é loira, rabo de cavalo e a camiseta preta
   do Aladdin), e existe em 3 versões: `chefe.js`, `tapete.js` e um desenho com `Graphics` no Final.

## Proposta por personagem

Todos com o esqueleto comum (`ferramentas/arte/humano.py`, branch `etapa-8a-personagens-v2`) e o renderizador do
herói: 4 tons por material, contorno colorido, luz de cima e da frente. **Um sprite por personagem**, usado em todas
as cenas.

| Personagem | Hoje | Alvo | Quadros propostos | Design (provisório até as fotos dos figurinos) |
|---|---|---|---|---|
| Jasmine | 44 px, 2 q. | 50–54 px (48×64) | parada 4, pirueta 4, fala 2 | bailarina da escola: top e calça de dança, tiara, trança; sem as cores do filme |
| Gênio | 44 px, 2 q. | 80–90 px (80×96) | flutuar 4 (cauda de fumaça ondulando), fala 2, "tchan!" 2 | pele lilás, coque, colete rosa, braceletes dourados; o maior do elenco |
| Sultão | 48 px, 2 q. | 62–66 px (48×72) | parado 4, palmas 4 | robusto, turbante rosa com pena, barba branca, capa roxa |
| Tia Claudia | 42 px, 2 q. | 56–58 px (48×64) | parada 4, entregar ingressos 3, fala 2 | cabelo preto e óculos (seção 8); roupa neutra até a foto |
| Tia Paula | 48 px, 3 versões | 56–58 px (48×64) | socorro 2, feliz 2, parada 4, sentada no tapete 3, microfone no palco 2 | **loira, rabo de cavalo, camiseta preta com "Aladdin" dourado e fumaça azul/roxa**; resto neutro |
| Abu | 31 px, 9 cores | 24–30 px | parado 4, correr 6, aflito 2 | macaquinho com colete rosa e chapéu roxo; mais volume (4 tons) |
| Jafar | 50 px, 4 q. | 64–74 px (64×80) | flutuar 4 (capa ondulando), aviso 2, lançar 3, cansado 2, tonto 2 | mantém o design próprio (capuz roxo pontudo, bigode enrolado, varinha de estrela, cauda de fumaça); nada do filme |
| Aladdin | 58 px, 23 q. | — | — | fica como está (8.0) |

Novos (pedido do voo do tapete): **tucano** e **maritaca**, já desenhados na prévia `../tapete/aves.png`.

## Ordem sugerida

Tia Paula (aparece em 3 fases) → Jafar (chefe) → Tia Claudia e Jasmine → Gênio e Sultão → Abu. Para cada
um: prancha "sprite atual × novo × escala do herói" em `ferramentas/arte/previas/personagens/` antes de ligar no jogo.

## O que depende do Pedro

- Fotos dos figurinos (Jasmine, Gênio, Sultão, Abu, Jafar): sem elas, o design continua provisório, mas com a
  qualidade completa.
- Foto ou descrição e o OK da Tia Paula e da Tia Claudia.

## Desenhos da proposta (01/11/2026)

Gerados por `python3 ferramentas/arte/elenco_proposta.py` (mesmo renderizador e luz do herói, escala por personagem):

| Arquivo | Conteúdo |
|---|---|
| `proposta-elenco.png` | todos lado a lado na escala do jogo, com o Aladdin |
| `proposta-tia-paula.png` | parada, socorro (gaiola), feliz, microfone (Final), sentada (tapete): **um sprite para as 3 cenas** |
| `proposta-tia-claudia.png` | parada, fala, entrega os ingressos |
| `proposta-jasmine.png` | parada, pirueta 1 e 2 |
| `proposta-sultao.png` | parado, palmas |
| `proposta-jafar.png` | flutuando, lançando, cansado/tonto |
| `proposta-genio.png` | flutuando, "tchan!" |
| `proposta-abu.png` | parado, correndo, aflito |
| `nativo/*.png` | cada quadro em 1× |

Alturas atingidas: Tia Paula 57, Tia Claudia 57, Jasmine 54, Sultão 70, Jafar 65–69, Gênio 89–92, Abu 25–31 (herói 58).

**A capivara fica como está** (decisão do Pedro, 01/11/2026).

Mudanças de design em relação ao jogo de hoje (todas provisórias até as fotos):
- Tia Paula: coque castanho e vestido roxo → loira, rabo de cavalo, camiseta preta do espetáculo, jeans e tênis.
- Abu: colete e chapéu (lembravam o Abu do filme) → **macaco-prego** com lenço rosa da escola.
- Gênio: cabelo em coque (lembrava o do filme) → turbante magenta com joia; ganhou tamanho de "gigante".
- Jasmine: calça bufante → saia longa de dança com cinto de moedas (bailarina da escola).
- Jafar e Sultão: mesmo design, agora no tamanho e no acabamento certos.

Se aprovar, a 8A troca os sprites no jogo com as animações completas da tabela acima.

**Pele (informação do Pedro, 01/11/2026):** Tia Paula, Tia Claudia e o Sultão têm **pele branca**.
