# STATUS · ITAMANIA

## Capivara exploradora na praça (04/11/2026)

- Protagonista aprovada pelo Pedro: proposta 1, capivara quadrúpede caramelo, mochila verde e lenço amarelo.
- Tela inicial com EXPLORAR A PRAÇA, sem apagar progresso existente. Folha original com 16 quadros (quatro direções), WebP de 406.682 bytes.
- Praça: caminhada, colisão nas patas, moedas persistentes, conversas e pausa; moradores e mapa preservados.
- Teste reproduzível: `ferramentas/teste/praca.mjs`, com Playwright externo. Título, quatro direções, moeda persistente, conversa, colisão, pausa e joystick de toque em 844x390: todos passaram, zero erros no console.
- Robô das fases 1 a 4: 25,2 / 25,6 / 30,5 / 34,7 s, todas concluídas, zero erros. As fases ainda usam os heróis humanos anteriores e aguardam a adaptação da protagonista, conforme DESIGN.md.
- Build: 2.616.476 bytes (2,62 MB). Avisos existentes de resolução das fontes no build; fontes servidas e carregadas no teste de navegador.
- Nenhuma dependência nova no jogo. Sunny Land e Rex Plugins não foram integrados nesta entrega.


## Praça na disposição real (05/11/2026), aprovada pelo Pedro depois de 5 propostas

Ruas pela marcação do Pedro no satélite: asfalto na rua de cima (oeste), nas ruas que sobem e descem, na avenida da
esquerda e na rua de baixo; o resto é calçadão com o mesmo piso cinza-claro da praça.

- **Praça simétrica:** 4 canteiros com 2 tiles de calçada até a borda, cada um com uma árvore alta e rala e duas
  palmeiras-imperiais (tronco marrom alto, palmito verde, copa acima dos prédios). Concha acústica e espelho d'água
  comprido com jatos na faixa oeste; busto pequeno de perfil, dentro da água, na ponta leste do espelho.
- **Copa transparente:** árvores e palmeiras ficam a 40% quando o herói passa atrás (`PRACA.copaTransparente`).
- **Quadras cheias** de sobrados ecléticos claros (peças modulares do pacote repintadas, `pecas_praca.sobrado()`).
  Especiais: torre vermelha com lojas (quarteirão do Subway), Café do Vadinho, Hotel Centenário (rosado), Cesar Burg,
  Fórum Cível (branco com faixa azul), Club Itajubense girado 90° (pórtico para a praça), Five Stars (bar com telão).
- **Peças:** `ferramentas/arte/pecas_praca.py` (clube, sobrados, torre, hotel, fórum, Five Stars, concha, busto,
  jatos, árvore alta, palmeira-imperial), `montar_cafe.py`, `montar_burg.py`. São montagens e repinturas de peças do
  Modern Exteriors; desenho próprio só onde o pacote não tem: concha, busto de perfil, placas/letreiros, moldura e
  xadrez do Burg, tronco da palmeira.
- **Pendências:** OK do Five Stars para o nome no letreiro (sem ele, trocar por "BAR"); o busto de perfil é desenho
  simples (o Pedro pode desenhar um melhor); letreiro "MARKET"/"STORE" do pacote em alguns prédios.
- **Teste:** praça, conversa, copa transparente, saída para o mapa, título, pausa e fases 1 a 4 sem erros no console.
  `dist/` = 2,5 MB.


## Praça com o Modern Exteriors (04/11/2026, noite)

O Pedro achou o estilo do Ninja Adventure antigo demais e comprou o **Modern Exteriors 16x16** (LimeZu). A praça foi
refeita com ele, na disposição do satélite que o Pedro mandou.

- **Licença** (PDF no pacote, cópia em `referencias/licenciados/`): pode editar e usar em qualquer projeto, inclusive
  aberto no GitHub; não pode revender nem distribuir o pacote; crédito obrigatório (na tela de título e no
  `CREDITS.md`). Por isso o pacote completo (348 MB) fica em `referencias/licenciados/modern-exteriors/`, fora do Git
  (`.gitignore`), e o gerador copia para `public/assets/limezu/` só o que a praça usa (~290 KB).
- **Sessão nova:** o pacote não está no repositório. Para rodar o gerador de novo, baixar a versão 16x16 pelo link de
  download da compra (está no e-mail do itch.io do Pedro; não guardar o link no repositório) e extrair a pasta
  `Modern_Exteriors_16x16` em `referencias/licenciados/modern-exteriors/`.
- **Mapa** (`gerar_praca.py` → `praca.tmj`, 70x45 tiles): ruas de asfalto com faixas de pedestre e calçadas em volta;
  praça com piso claro, 4 maciços de árvores (noroeste, nordeste, sudoeste e o grande do leste/sudeste), espelho
  d'água retangular no largo e fonte redonda a nordeste dele, bancos, postes, placa. Em cima: sobrado (G5), Hotel
  Centenário, Café do Vadinho; do outro lado da rua, Cesar Burg. À esquerda: Fórum Cível e Club Itajubense (casarão
  com torre). À direita: açaí e arena. As bordas de calçada, grama e água saem dos autotiles do pacote (47 bordas,
  lidas automaticamente). Prédios e árvores são imagens na camada de objetos, ordenadas pela base.
- **Personagens (provisório):** Geraldo = escoteiro de cabelo castanho, Helena = escoteira de cabelo cacheado; moradores
  são carteiros e escoteiros do pacote (o pacote só traz esses). Para ter moradores variados, o Modern Interiors
  (mesmo autor) traz um gerador de personagens.
- **Placas em inglês** nas fachadas do pacote ("STORE", "MARKET"); os nomes certos aparecem nas falas. Falta: busto
  de Theodomiro (o pacote não tem) e letreiros em português.
- **Teste (Chromium):** praça carrega, andar, conversar (guia), placas, itacoins, pausa, saída para o mapa, título,
  capturas antigas, sem erros no console. `dist/` = 2,3 MB.


## Praça andável (04/11/2026, tarde)

Pedido do Pedro: reformular o começo com o Centro explorável, vista de cima, usando pacotes prontos (nada de arte
feita do zero). Fluxo novo: Título → **Praça** (andável) → saída do sul → mapa das fases. O botão do mapa que era
MENU virou PRAÇA (volta ao centro).

- **Arte:** pacote Ninja Adventure (Pixel-boy e AAA, CC0), baixado do itch.io com a rede liberada pelo Pedro. Só os
  arquivos usados foram copiados para `public/assets/ninja/` (~300 KB). Licença em `referencias/licenciados/`.
- **Mapa:** `public/assets/mapas/praca.tmj`, formato do **Tiled** (abre e edita no Tiled). Gerado por
  `ferramentas/mapas/gerar_praca.py`, que monta as bordas da grama, dos caminhos e da água a partir dos tiles do
  pacote. Prévia em `ferramentas/arte/previas/praca-mapa.png`. Camadas: chão, água, objetos, cima (copas por cima do
  herói), colisão (invisível) e pontos (início, moradores, placas, itacoins, saída).
- **Praça (pelo mapa do Pedro e o satélite):** moldura de caminho, 4 gramados com árvores nos cantos (no mapa do Pedro
  são palmeiras; o pacote não tem), caminhos em cruz, fonte no meio com uma estátua no lugar do busto, bancos. Na rua
  de cima: Club Itajubense, Café do Vadinho e Cesar Burg (lojas do pacote com placa), casas. Ruas de terra em volta
  (o pacote não tem asfalto nem calçada).
- **Personagens:** Geraldo = "Boy" e Helena = "Princess" do pacote (provisório, até o Pedro desenhar a versão vista
  de cima). Moradores: guia, Dona Cida no banco, barista, atendente, estudante que passeia, gato. Balão "..." em quem
  ainda não falou, "!" quando dá para conversar.
- **Controles:** toque = joystick que nasce onde o dedo encosta na metade esquerda + botão FALAR; teclado = setas ou
  WASD + espaço, Enter, X ou J. Pausa (Esc ou botão) com CONTINUAR, SOM, MENU e MAPA.
- **Itacoins:** 14 espalhadas; as pegas ficam salvas (`estado.moedasPraca`).
- **Teste (Chromium):** do Título à praça, conversa com o guia, placas, itacoin, pausa, saída para o mapa, joystick de
  toque no iPhone 13 deitado; capturas antigas (título, mapa, fases 1 a 4) sem erros no console. `dist/` = 2,3 MB.
- **Limites do pacote:** estilo de vila japonesa (telhados, lojas), sem asfalto, sem palmeira, estátua genérica. Se a
  ideia vingar, o passo seguinte é o Modern Exteriors (LimeZu, pago), mais parecido com uma cidade moderna.

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
