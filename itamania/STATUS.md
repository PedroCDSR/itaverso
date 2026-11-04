# STATUS · ITAMANIA

## Onde está (04/11/2026)

**MVP (pedido do Pedro):** Título (escolha Geraldo ou Helena) → passeio pelo mapa mostrando os 14 lugares →
Fase 1 (Rodoviária e trem-museu) → cartão de curiosidade → tela "Continua em breve" com a dedicatória.

- Link de teste (artifact privado): https://claude.ai/artifact/AAYHV3LRoXotovFiommWSH
- Local: `cd itamania && npm install && npm run dev`. Atalhos: `?fase=1`, `?heroi=helena`, `?cena=Mapa`.
- Robô: `node ferramentas/teste/jogar.mjs` (com `NODE_PATH=/opt/node22/lib/node_modules` no container) terminou a
  fase 1 em ~26 s, sem erros no console. `dist/` = 1,7 MB.

## Decisões

- Herói: sprites 16x24 desenhados pelo Pedro (`ferramentas/arte/heroi_base.py`, copiados pixel a pixel), sem e com
  boné. Animações derivadas só nas pernas, braço e olhos (`gerar_heroi16.py`). No jogo aparecem em 2x (32x48).
- Fora do MVP por enquanto (pedido do Pedro): forma grande/adulta e café com leite. Fases 2 a 4 têm rascunho pronto
  (`src/levels/fase2.js` a `fase4.js`, com pão de queijo, loja do boné, Casa Joka, Cesar Burg e Café do Vadinho),
  mas não estão ligadas em `src/levels/index.js`.
- Mapa-múndi (04/11, pedido do Pedro): o desenho dele em alta resolução (`public/assets/mapa-hd.png`, 1080x1920,
  198 KB) numa camada HTML por cima do canvas (`src/ui/mapaHtml.js`), sem passeio automático. Abre na Rodoviária e
  rola só na vertical: arrastar, roda do mouse, setas para cima e para baixo. Tocar numa moeda anda até ela (setas
  para os lados também); o painel do Phaser embaixo tem MENU, nome da fase, JOGAR e som. O trecho visível é
  desenhado num canvas do tamanho da tela. O `mapa.png` de 480 px não é mais carregado. Nas capturas do Playwright,
  usar `--use-angle=swiftshader`: sem isso o Chromium sem tela não mostra o canvas do Phaser embaixo da camada.
- Título: "ITAMANIA" com uma cor por letra como no topo do mapa (vermelho, amarelo, verde, azul, repetidos; conferido
  no desenho), tom claro em cima, contorno escuro e sombra em degrau.
- Comércios reais (Casa Joka, Cesar Burg, Café do Vadinho) liberados pelo Pedro; fábrica de helicópteros sem nome.
- NPCs adultos ainda no estilo antigo (48x64); refazer no estilo 16x24 do herói.

## Próximo passo

Esperar o retorno do Pedro sobre o MVP antes de seguir.
