# CLAUDE.md · ITAMANIA, o mundo de Itajubá

Este arquivo é a fonte de verdade das regras de trabalho. Leia inteiro antes de começar.
Fale sempre em **português do Brasil**, simples e direto. **Não use travessões** (nem no jogo, nem nas respostas, nem
nos comentários novos).

- História, personagens, fases e regras de conteúdo: [`itamania/DESIGN.md`](itamania/DESIGN.md) (texto do Pedro, fonte
  de verdade da história).
- Andamento, decisões e próximo passo: [`itamania/STATUS.md`](itamania/STATUS.md). **Leia antes de começar e atualize
  ao terminar.**
- Plano da etapa em andamento: [`itamania/PLANO.md`](itamania/PLANO.md).

## 1. O que é

Jogo de plataforma 2D para celular sobre Itajubá/MG, com a jogabilidade e a linguagem visual de um jogo de plataforma
de 16 bits. Projeto do Pedro (pedrocdsr).

- Roda no navegador do celular, deitado, com toque (teclado como bônus). É curto e **não tem game over**: cada fase
  tem ponto de retorno.
- 14 fases e 1 fase secreta, escolhidas num **mapa-múndi em pé** desenhado pelo Pedro, de baixo para cima.
- Público inclui crianças. Tom leve, carinhoso, sem nada assustador de verdade.
- Lado educativo: cada fase termina com um **cartão de curiosidade** real sobre a cidade (uma frase, uns 5 segundos).

## 2. A história em uma página

**Geraldo ou Helena** (homenagem aos avós do Pedro), escolhidos na tela inicial: uma criança que acabou de chegar a
Itajubá, animada com a vida nova, e quer conhecer a cidade. Cada partida é só a história de quem foi escolhido.
Mochila e tênis; o boné amarelo entra na fase 3. Quem chegou sem conhecer a cidade termina cuidando dela.

| Ato | Fases | Resumo |
|---|---|---|
| 1, o sonho | 1 a 4 | Chega de ônibus na Rodoviária (trem-museu como tutorial), vê um helicóptero e quer ser piloto. Descobre que o helicóptero é feito na fábrica da cidade e que quem estuda na UNIFEI trabalha lá. Ganha o boné, o café com leite e o pão de queijo e aprende a história de Theodomiro Santiago. |
| 2, o encanto | 5 a 8 (+ secreta) | Vê a cidade do alto (Morro Chic, Coroados, Praçonha) e junta 3 pistas sobre a Mulher de Bronze. No cemitério, à noite, a lua revela a história real da estátua e uma saída secreta para o céu estrelado. |
| 3, a UNIFEI | 9 | Escolhe o curso, atravessa os anos de faculdade, apresenta o TCC (chefe leve), se forma e ganha a mochila-hélice. "Anos depois..." |
| 4, do engenheiro ao prefeito | 10 a 14 | Pinheirinho, Agonia, Kart, voo no helicóptero que ajudou a construir (Lago) e, anos depois, a cidade o escolhe para {prefeito\|prefeita}. |

**Evolução do herói:** sem boné → boné (3) → café com leite, que faz crescer e aguenta um toque a mais, e pão de
queijo para arremessar (4) → mochila-hélice (9) → helicóptero (13) → {prefeito|prefeita} (14).

**Moeda:** itacoins (pedrinhas amarelas, a "pedra amarela" do nome da cidade), desde a fase 2.

**Inimigos (todos leves):** capivaras, pombos da praça, morcegos fofos no cemitério, provas voadoras na UNIFEI.
Inimigo atingido pega o item, come e vai embora feliz (ou cochila com "zzz").

A tabela completa das fases, as curiosidades com fonte e as "vagas" (lugares e pessoas reais) estão no `DESIGN.md`.

## 3. Regras fixas

1. **Estilo do gênero pode, elementos da Nintendo não.** Nada de Mario, Goomba, Koopa, planta carnívora, cogumelo,
   cano verde, bloco "?", morros ou nuvens com olhos. Mecânicas do gênero (crescer com item, arremessar) podem, com
   visual e sons próprios. Nunca extrair, recortar ou decalcar sprites, sons ou músicas de jogos comerciais.
2. **Sem violência.** 3. **Sem piada com droga.**
4. **Pessoas reais só com OK delas**, sempre carinhosas. Tudo que é real entra como "vaga": o jogo sempre funciona com
   a versão genérica (`src/data/vagas.js`, `real: true/false`).
5. **Marcas:** o Pedro autorizou em 04/11/2026 os nomes e logos dos comércios de Itajubá (Casa Joka, Cesar Burg, Café
   do Vadinho), desenhados em pixel por nós. A fábrica de helicópteros continua **sem nome** até haver autorização.
6. **Política:** nada de partido, campanha, urna ou propaganda. O prefeito do jogo não lembra políticos reais.
7. **Sem coleta de dados.** Site estático, sem servidor, cadastro ou login.
8. **Fatos só com fonte.** O que não foi confirmado fica marcado "(confirmar)" no `DESIGN.md` e não vai para o jogo.
9. **Mulher de Bronze:** a estátua não fala nem se mexe (é memorial de uma família real). Mostrar a fase 8 ao CODPHAI
   ou à família antes de publicar.

## 4. Como trabalhar

- **Autonomia (pedido do Pedro, 04/11/2026):** tomar as decisões técnicas e artísticas, testar no Chromium com
  Playwright e registrar no `STATUS.md`. Só perguntar o que só o Pedro resolve (autorizações, fotos, compra de assets,
  mudança de história).
- **Branches:** o Netlify (projeto `itamania`, diretório base `itamania`) publica a branch `claude/busy-hamilton-cxbmdi`.
  Trabalhe na branch da sessão e só leve para a `claude/busy-hamilton-cxbmdi` o que estiver testado (cada deploy gasta
  créditos do plano gratuito). A `main` não é tocada sem o Pedro pedir. Commit e push ao fim de cada parte. Não abrir
  PR sem o Pedro pedir.
- Autor dos commits: `Pedro Rocha <65837046+PedroCDSR@users.noreply.github.com>` (`git config` sem `--global`).
- Comandos, dentro de `itamania/`: `npm install`, `npm run dev`, `npm run build`. Atalhos: `?fase=1` a `?fase=4` e
  `?heroi=helena`.
- Ao terminar uma parte: `npm run build` sem erros, peso do `dist/` (meta abaixo de 3 MB), robô de teste
  (`ferramentas/teste/jogar.mjs`) sem erros no console, capturas conferidas e `STATUS.md` atualizado.
- Nas capturas do Playwright, usar `--use-angle=swiftshader` (sem isso o canvas some embaixo da camada HTML do mapa).

## 5. Arte (abordagem híbrida)

A arte que dá vida ao jogo vem de mão humana; o Claude integra, anima, ajusta e completa.

1. **Desenhos do Pedro são a base** (heróis 16x24 e 16x32, mapa-múndi, referências em `itamania/referencias/`). Copiar
   pixel a pixel o que ele desenhou; derivar animações sem mudar o design.
2. **Assets licenciados** (itch.io, OpenGameArt, Kenney etc.) podem entrar quando a licença permitir, registrados em
   `CREDITS.md`. Preferir um pacote coerente a misturar estilos.
3. **Geradores Python** (`ferramentas/arte/`) completam o que falta, no mesmo estilo e escala, e escrevem PNG em
   `public/assets/` ou matrizes em `src/art/`. Nunca entregar arte genérica ou abaixo do nível dos desenhos do Pedro.
- **Escala:** sprites desenhados em 16x24 (criança) e 16x32 (grande e adultos), ampliados 2x no jogo (48 e 64 px, a
  escala dos prédios). NPCs adultos usam o corpo de 16x32.
- O mapa-múndi é uma camada HTML em alta resolução por cima do canvas (`src/ui/mapaHtml.js`).

## 6. Técnica

- Phaser 4.2.1 (Arcade Physics), Vite 8, Node 22. Resolução 480×270, `pixelArt`, `Scale.FIT`. Mobile first,
  deitado, `100dvh`, aviso de girar o celular, pausa ao perder o foco, som só depois do primeiro toque (ZzFX e música
  em código).
- Constantes de jogo em `src/config.js`. Textos em `src/data/textos.js`, com marcação de gênero `{animado|animada}`
  trocada por `src/genero.js` conforme o herói.
- Fases são dados (`src/levels/faseN.js`: mapa em texto, cenário, lugares, NPCs, missão, curiosidade) lidos pela cena
  genérica `src/scenes/Fase.js`. Legenda dos mapas no topo de `src/levels/leitor.js`.
- Diálogo em HTML nítido (`src/ui/Dialogo.js`), no máximo 2 linhas por caixa.

## 7. Estrutura do repositório

```
itamania/              o jogo (tudo que vai para o Netlify sai daqui)
  DESIGN.md            história e fases (Pedro)
  STATUS.md            andamento e decisões
  PLANO.md             plano da etapa atual
  referencias/         desenhos e mapa originais do Pedro (não vão para o build)
  ferramentas/         geradores de arte (Python) e robô de teste (Playwright)
  public/assets/       sprites, cenários, mapa em alta, fontes
  src/                 scenes, levels, objects, ui, audio, data, art
```

O código que está na raiz do repositório, fora de `itamania/`, é **legado de outro projeto** (que já tem repositório
próprio). Não usar como referência de regras nem editar; a remoção está pendente.
