# STATUS · ITAMANIA

## Onde está (05/11/2026, madrugada)

Fluxo: Título (escolha Geraldo ou Helena, ITAMANIA colorido) → mapa do Pedro em alta resolução (rola para cima e
para baixo) → fases 1 a 4 → cartão de curiosidade de cada fase → tela "Continua em breve" depois da fase 4.

- Fase 1 Rodoviária e trem-museu (locomotiva + 1 vagão), fase 2 Praça do Soldado (itacoins, pombos), fase 3 Rua
  Nova (compra o boné na Casa Joka), fase 4 Praça Theodomiro Santiago (pão de queijo no Cesar Burg, café com leite no
  Café do Vadinho: o herói cresce de 48 para 64 px e aguenta um toque a mais).
- Robô (`ferramentas/teste/jogar.mjs`, Chromium com `--use-angle=swiftshader`): fases 1 a 4 pelo mapa em
  24,8 + 24,6 + 30,7 + 38,8 s, sem erros no console. `dist/` = 2,0 MB.
- Netlify: projeto `itamania`, branch `claude/busy-hamilton-cxbmdi`, base `itamania`. O trabalho é feito em
  `claude/itamania-etapa2` e só entra na branch do Netlify quando está testado.
- Janelas desta etapa: NPCs (`claude/itamania-npcs`) e mapa/título (`claude/itamania-mapa`), já juntadas.

## Decisões

- Herói: sprites 16x24 desenhados pelo Pedro (`ferramentas/arte/heroi_base.py`, copiados pixel a pixel), sem e com
  boné. Animações derivadas só nas pernas, braço e olhos (`gerar_heroi16.py`). No jogo aparecem em 2x (32x48).
- Herói grande (16x32, desenho do Pedro, só com boné) = forma do café com leite. Escala 2x: criança 48 px, grande e
  adultos 64 px, a escala dos prédios. A forma adulta do Ato 4 ainda não foi feita.
- Mapa-múndi (04/11, pedido do Pedro): o desenho dele em alta resolução (`public/assets/mapa-hd.png`, 1080x1920,
  198 KB) numa camada HTML por cima do canvas (`src/ui/mapaHtml.js`), sem passeio automático. Abre na Rodoviária e
  rola só na vertical: arrastar, roda do mouse, setas para cima e para baixo. Tocar numa moeda anda até ela (setas
  para os lados também); o painel do Phaser embaixo tem MENU, nome da fase, JOGAR e som. O trecho visível é
  desenhado num canvas do tamanho da tela. O `mapa.png` de 480 px não é mais carregado. Nas capturas do Playwright,
  usar `--use-angle=swiftshader`: sem isso o Chromium sem tela não mostra o canvas do Phaser embaixo da camada.
- Título: "ITAMANIA" com uma cor por letra como no topo do mapa (vermelho, amarelo, verde, azul, repetidos; conferido
  no desenho), tom claro em cima, contorno escuro e sombra em degrau.
- Comércios reais (Casa Joka, Cesar Burg, Café do Vadinho) liberados pelo Pedro; fábrica de helicópteros sem nome.
- NPCs redesenhados no estilo dos heróis (16x32, `ferramentas/arte/gerar_npcs16.py`).

## Próximo passo

Retorno do Pedro sobre as fases 1 a 4. Pendências dele: teste em celular de verdade, autorização da fábrica e
dos personagens reais que ainda são genéricos.
