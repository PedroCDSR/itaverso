# CLAUDE.md · ITAMANIA

Jogo de plataforma 2D para celular sobre Itajubá/MG, com a jogabilidade e a linguagem visual de um jogo de plataforma
de 16 bits. Projeto do Pedro (pedrocdsr). Esta pasta (`itamania/`) é um projeto **independente** do jogo do Aladdin
que está na raiz deste repositório: as regras do `CLAUDE.md` da raiz **não valem aqui**, exceto o que for repetido
abaixo. O motor (Phaser 4 + Vite, toque, diálogo em HTML, som em código) foi copiado do Aladdin e adaptado.

Fale sempre em **português do Brasil**, simples e direto. **Não use travessões** nos textos (nem no jogo, nem nas
respostas, nem nos comentários novos).

- Documento de design completo: [`DESIGN.md`](DESIGN.md) (texto do Pedro, fonte de verdade da história e das fases).
- Andamento, decisões e próximo passo: [`STATUS.md`](STATUS.md). **Leia antes de começar e atualize ao terminar.**

## Como trabalhar

- Branch de trabalho atual: `claude/busy-hamilton-cxbmdi` (repositório `PedroCDSR/itaverso`). Commit e push ao fim de
  cada parte, para nada se perder se o limite de uso acabar. Não abrir PR sem o Pedro pedir.
- Autor dos commits: `Pedro Rocha <65837046+PedroCDSR@users.noreply.github.com>` (`git config` sem `--global`).
- Autonomia total (pedido do Pedro, 04/11/2026): tomar as decisões, testar no Chromium com Playwright, registrar no
  `STATUS.md`. Só perguntar o que só ele resolve.
- Dentro de `itamania/`: `npm install`, `npm run dev`, `npm run build`. Teste direto de uma fase: `?fase=1` a `?fase=4`
  e `?heroi=helena`.
- Ao terminar uma parte: `npm run build` sem erros, peso do `dist/`, robô de teste sem erros no console, `STATUS.md`.

## Regras fixas (do DESIGN.md, resumidas)

1. Estilo do gênero pode, elementos da Nintendo não (nada de Mario, Goomba, Koopa, cogumelo, cano verde, bloco "?",
   morros ou nuvens com olhos). Sons e visual próprios.
2. Sem violência: inimigo atingido pega o item, come e vai embora feliz (ou cochila com "zzz").
3. Sem piada com droga. 4. Pessoas reais só com OK, sempre carinhosas; o jogo funciona com a versão genérica.
5. Marcas: o DESIGN.md pede marcas fora do jogo, **mas o Pedro autorizou em 04/11/2026** usar nomes e logos dos
   comércios de Itajubá (tem autorização dos donos). Por isso Cesar Burg, Café do Vadinho e Casa Joka aparecem com
   o nome na fachada, desenhado em pixel por nós. A fábrica de helicópteros continua **sem nome** (não é comércio e
   não entrou na autorização). Cada vaga tem as duas versões em `src/data/vagas.js` (`real: true/false`).
6. Política: nada de partido, campanha, urna. O prefeito do jogo não lembra políticos reais.
7. Sem coleta de dados, sem servidor. 8. Fatos só com fonte; "(confirmar)" nunca vai para o jogo.

## Técnica

- Phaser 4.2.1 (Arcade), Vite 8, resolução 480×270, `pixelArt`, `Scale.FIT`. Mobile first, deitado, toque e teclado.
- Constantes de jogo em `src/config.js`. Textos em `src/data/textos.js`, com marcação de gênero `{animado|animada}`
  trocada por `src/genero.js` conforme o herói escolhido (Geraldo ou Helena).
- Fases são dados (`src/levels/faseN.js`: mapa em texto, cenário, lugares, NPCs, missão, curiosidade) lidos por uma
  cena genérica `src/scenes/Fase.js`. Legenda dos mapas no topo de `src/levels/leitor.js`.
- Arte: geradores Python em `ferramentas/arte/` escrevem matrizes em `src/art/` (herói com o renderizador de volumes
  `modelo.py`) ou PNG em `public/assets/`. Cenários reais de Itajubá reaproveitam os PNGs feitos para o Aladdin
  (fonte com o busto, Café do Vadinho, Praça do Soldado, casario, serra), que são arte própria do projeto.
- Referências e notas de pesquisa: `referencias/README.md`.
