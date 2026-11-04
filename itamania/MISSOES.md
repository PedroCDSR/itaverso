# Encontros e missões da praça

Esta entrega fica **local**, na branch `missao-praca-sunnyland`, até o Pedro autorizar um deploy. Não fazer push
para `claude/busy-hamilton-cxbmdi`: essa branch aciona o site Netlify `itamania`, e o nome da branch não garante
um deploy gratuito nem um endereço separado de desenvolvimento. Antes de publicar, confirmar o contexto de dev
no Netlify e o consumo de créditos do plano. Não publicar em `main`.

## Jogar localmente

Node 22. Dentro de `itamania/`:

```bash
npm ci
npm run dev -- --port 5181 --strictPort
```

Abrir o jogo no navegador local, escolher EXPLORAR A PRAÇA e caminhar para a direita da praça. O Gambá Travesso
fica perto do canto sudeste, com um sinal de exclamação. Aproximar e usar FALAR no toque ou espaço no teclado.
O centro da praça, os comércios e os diálogos não provocam encontros aleatórios.

- Encontro especial: conversar com o gambá inicia **Trilhas da praça**, uma travessia de aproximadamente 25 a 45 s.
- Encontro comum: somente no trecho de rua lateral marcado em `micromundos.js`, com pelo menos 160 px percorridos,
  30 s de proteção inicial/após retorno e um sorteio de 25% a cada 48 px. Inicia **Corrida pelos jardins**, com perseguidor.
- Missões: capivara, plataformas, buracos curtos, gambás, itacoins opcionais e dois pontos de retorno. Setas ou A/D
  para correr, espaço/W/cima para pular; no celular, setas e PULAR simultâneos. O pulo tem altura variável, tolerância
  de borda e buffer. Esc ou PAUSA abre o menu; VOLTAR À PRAÇA abandona sem perder o progresso da exploração.
- Cada queda/toque tira um fôlego e retorna ao último ponto da trilha. Sem fôlego, volta ao ponto seguro da praça.
- Vitória volta às coordenadas e direção do encontro. Primeiro prêmio: 5 itacoins + moedas da missão. Repetição:
  1 itacoin + no máximo 3 moedas da missão. As recompensas só entram no saldo ao concluir a missão.
- Fechar/recarregar durante encontro ou missão recupera a praça no ponto de origem, sem prêmio e sem apagar
  descobertas. Recarregar na tela de vitória preserva a recompensa, sem concedê-la novamente.
- O ponto 4 do mapa do Pedro abre a praça, sem precisar concluir as fases antigas. O marcador agora é a capivara.

## Conteúdo e arquitetura

- `src/data/micromundos.js`: os **14 nomes e a ordem existentes** em `NOMES_FASES`. Somente o ponto 4 tem exploração
  neste recorte; os outros 13 não são anunciados como mapas prontos. Define zonas, encontro especial, ponto seguro,
  missões, terrenos, buracos, inimigos e recompensas.
- `src/systems/encontros.js`: proteção por distância/tempo, sorteios restritos, sessão persistente, prêmio uma única
  vez, repetição, derrota e recuperação de interrupções. Encontros de história usam tipo `historia` e um ID estável: podem ser tentados novamente após derrota e são bloqueados automaticamente depois da primeira vitória.
- `src/scenes/Encontro.js`: anúncio e cortina de pixels, cerca de 2 s, sem copiar telas ou assets de Pokémon.
- `src/scenes/Missao.js`: travessia/fuga compartilham física, cenário, coleta, pontos de retorno e conclusão.
- `estado.encontros`: missões concluídas, visitas e sessão pendente; migração aditiva na mesma chave de progresso.
- `src/scenes/Praca.js`: snapshot de posição/direção, entrada e retorno. A praça ainda tem sua própria cena; futuras
  regiões devem fornecer uma cena/mapa e adaptar o destino de retorno antes de se declararem disponíveis.

A missão é uma adaptação livre dos jardins da praça, não uma reprodução geográfica: Modern Exteriors fica na
exploração; Sunny Land dá terreno, árvores, arbustos, céu, plataformas e gambás na vista lateral. Morros e marcos
(clube, café e fonte) do projeto ligam os dois modos. As quatro fases de plataforma antigas continuam como referência
histórica; não são o novo sistema de micromundos.

## Validação

Playwright é ferramenta externa de desenvolvimento, como nos robôs existentes; não é dependência do jogo.
Com o Vite rodando e Playwright/Chromium disponíveis:

```bash
node ferramentas/teste/encontros.test.mjs
node ferramentas/teste/praca.mjs http://localhost:5181/ capturas/praca
node ferramentas/teste/missao.mjs http://localhost:5181/ capturas/missoes
node ferramentas/teste/missao-toque.mjs http://localhost:5181/ capturas/toque
npm run build
```

Os robôs usam `window.jogo`, disponível só no Vite de desenvolvimento. Os testes de missão percorrem a física
até a saída; os de queda posicionam a capivara sobre um buraco e verificam o retorno. A automação de toque usa
Chromium com perfil mobile, não substitui testar em Safari/iPhone e Android reais.
