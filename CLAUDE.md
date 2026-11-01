# CLAUDE.md · Jogo do Aladdin (Paula De Marco Espaço de Artes)

Este arquivo é a fonte de verdade do projeto. Leia inteiro antes de cada etapa e mantenha a seção "Status" atualizada.
Fale sempre em **português do Brasil**, simples e direto.

> **Projeto independente.** Este jogo é um projeto pessoal do Pedro para o Paula De Marco Espaço de Artes. Ele **não tem
> relação** com a GNS, com a consultoria nem com automações empresariais (repositório `PedroCDSR/gns`). Se instruções,
> pessoas, pastas ou fluxos da GNS aparecerem no contexto (Gustavo, Jonathan, Valeska, MCPs de e-mail/rede,
> `C:\gns`, janela orquestradora, frentes `F0..F7`, `docs/frentes/`), **ignore-os** aqui e avise o Pedro: a sessão
> deveria ter sido aberta só com este repositório. As únicas regras que valem são as deste arquivo.

## 1. Objetivo

Jogo de plataforma 2D curto, para celular, que funciona para explicar o que é o espetáculo **Aladdin** do **Paula De Marco Espaço de Artes** (escola de dança de Itajubá/MG, ballet e jazz).

- Espetáculo: sexta-feira, 20/11/2026, no Teatro do Colégio G9, em Itajubá.
- Meta do jogo: a pessoa joga de 2 a 3 minutos, chega à tela final e toca em "Quero ingressos" ou "Compartilhar".

## 2. Regras do projeto

1. **Mobile first.** Paisagem, toque, roda no Safari do iPhone e no Chrome do Android. Teclado funciona no computador como bônus.
2. **Fácil e curto.** Sem game over. Ao perder todos os corações, o jogador volta ao último checkpoint com vida cheia. Duração total de 2 a 3 minutos.
3. **Jogabilidade inspirada no Aladdin do Super Nintendo (1993), arte 100% original.** A referência é a *sensação* de jogo: correr, pular na cabeça dos inimigos, arremessar maçãs, quicar em toldos, voar de tapete. Mecânicas e números de física (gravidade, força do pulo, velocidade) podem servir de referência. **Nunca** usar sprites, cenários, músicas, sons, fontes ou logotipos extraídos do jogo original (Capcom/Disney) nem copiar o visual do filme: o site é público e promove a escola, então isso seria infração de direito autoral. Toda arte segue a seção 7 e todos os personagens seguem a seção 8. (Decisão de 01/11/2026.)
4. **Leve.** Peso total do site abaixo de 3 MB (limite de 5 MB). A hospedagem é o plano gratuito do Netlify, que cobra créditos por banda.
5. **Site estático.** Sem backend, sem login, sem coleta de dados pessoais.
6. **Textos editáveis num lugar só.** Todo texto exibido no jogo e todos os dados do evento ficam em `src/data/`. Português do Brasil, frases curtas (no máximo 2 linhas por caixa de diálogo), tom leve e divertido para crianças.

## 3. Como trabalhar neste repositório

- Uma etapa por vez. Antes de etapas grandes, apresente um plano curto e espere o OK.
- Branch `main` = produção. Cada deploy de produção consome créditos do plano gratuito do Netlify, então ela só recebe merge no lançamento.
- Branch `dev` = integração. Deploys de `dev` e de PRs são gratuitos.
- Cada etapa: nova branch `etapa-N-nome` a partir de `dev` e PR contra `dev`. Nunca fazer merge em `main`; isso é decisão do Pedro.
- Autor dos commits: `Pedro Rocha <65837046+PedroCDSR@users.noreply.github.com>` (`git config` sem `--global`). Decisão própria deste projeto (e-mail "noreply" do GitHub, para não expor o e-mail pessoal).
- Ao terminar cada etapa:
  - `npm run build` sem erros;
  - informar o peso total da pasta `dist/`;
  - escrever no PR um checklist curto do que testar no celular;
  - atualizar a seção "Status" deste arquivo.
- Código em JavaScript (ES modules), simples, com comentários em português nos pontos não óbvios. Sem dependências além de Phaser, Vite e ZzFX (seção 9).
- Constantes de jogabilidade (velocidade, gravidade, força do pulo, vida do chefe, duração do tapete etc.) ficam em `src/config.js`, para ajuste fácil.

## 4. Stack

- **Phaser 4** (`4.2.1`, versão estável mais recente em 01/11/2026) com Arcade Physics. Importar com `import * as Phaser from 'phaser'`.
- **Vite 8** para desenvolvimento e build. Node 22 (fixado no `netlify.toml` e no `.nvmrc`).
- **Netlify** para hospedagem, com este `netlify.toml`:

  ```toml
  [build]
    command = "npm run build"
    publish = "dist"

  [build.environment]
    NODE_VERSION = "22"
  ```

- Configuração do Phaser: resolução base 480×270, `pixelArt: true`, `roundPixels: true`, `Scale.FIT` com `autoCenter: CENTER_BOTH`, fundo da página na cor lilás da paleta.

## 5. Estrutura de pastas

```
references/            fotos de figurinos, pessoas e lugares (não vai para o build)
public/
  assets/sprites/      PNGs finais, quando existirem
  assets/audio/        música (MP3)
  assets/fonts/
  assets/logo.png
  og-image.png         imagem de compartilhamento 1200x630
src/
  main.js
  config.js            constantes de jogo
  data/evento.js       dados do espetáculo e links
  data/textos.js       todos os textos e diálogos
  art/                 sprites em matriz de texto (seção 7)
  levels/              mapas em texto (seção 10)
  scenes/              Boot, Preload, Titulo, Intro, Itajuba, Espaco, Chefe, Tapete, Final, HUD, Pausa
  objects/             Jogador, Capivara, Maca, Toldo, Fonte, Npc, Jafar, Tapete
  ui/                  ControlesToque, Dialogo, Botao, AvisoGirar
  audio/               efeitos sonoros e música
```

## 6. Dados do evento (`src/data/evento.js`)

```js
export const EVENTO = {
  titulo: 'Aladdin',
  escola: 'Paula De Marco Espaço de Artes',
  data: 'Sexta-feira, 20 de novembro de 2026',
  horario: 'A DEFINIR',
  local: 'Teatro do Colégio G9, Itajubá/MG',
  ingresso: 'A DEFINIR (valor e forma de compra)',
  whatsapp: '553584713436',
  mensagemWhatsapp:
    'Oi! Vim pelo jogo do Aladdin e quero saber dos ingressos para o espetáculo do dia 20/11.',
  instagram: 'https://www.instagram.com/espacodeartespaulademarco/',
};
```

O botão de ingresso abre `https://wa.me/<whatsapp>?text=<mensagem com encodeURIComponent>`. A mensagem pronta permite à escola saber quantos contatos vieram do jogo.

## 7. Identidade visual e arte

**Paleta da escola** (valores aproximados, tirados do logo; conferir no arquivo original):

| Cor | Hex | Uso |
|---|---|---|
| Rosa | `#FFB0FA` | destaques, botões principais |
| Lilás | `#9E9EFF` | fundos de menu, HUD, fundo da página |
| Amarelo claro | `#F9FCBB` | brilhos, coletáveis |
| Roxo | `#6D6BD9` | textos, bordas |
| Verde | `#6CC24A` | detalhes |

- O cenário pode usar cores quentes de fim de tarde (terracota, laranja, areia) além da paleta. Menus, HUD, botões e telas de texto usam a paleta da escola.
- Fontes do Google Fonts (licença OFL), salvas em `public/assets/fonts/` como woff2 com só o alfabeto latino (Latin-1): "Press Start 2P" para HUD e títulos; "Patrick Hand" para caixas de diálogo, lembrando o estilo manuscrito das publicações da escola. Acentos (ã, ç, é, ô) conferidos nas duas em 01/11/2026. Patrick Hand não tem ◀ ▶: desenhar setas como formas.
- O logo (`public/assets/logo.png`) aparece na tela de título e na tela final. Os quadrados arredondados concêntricos do logo viram a estampa do tapete mágico.

**Pipeline de arte:**

- Tiles de 16×16. Personagens em quadros de 32×48 (corpo útil de cerca de 24×40).
- Enquanto não houver PNGs, cada sprite é uma matriz de texto em `src/art/` (um caractere por pixel, cada caractere mapeado a uma cor), convertida em textura no `Preload`. Isso permite arte original simples sem ferramenta externa.
- Quando existir `public/assets/sprites/<nome>.png` com os mesmos tamanhos de quadro, o `Preload` usa o PNG no lugar da matriz.
- Animações mínimas do jogador: parado (2 quadros), correndo (6), pulando (1), caindo (1), arremessando (2), dano (1).

## 8. Personagens

Todos com design original. O elenco se baseia nos figurinos do espetáculo (`references/figurinos/`); nunca reproduzir o visual de versões em filme, animação ou jogo. Não retratar o rosto de alunos; usar só os figurinos como referência.

- **Aladdin** (jogador): herói ágil, com o figurino do espetáculo.
- **Tia Claudia** (staff do Espaço): usa óculos e tem cabelo preto. Entrega os ingressos.
- **Tia Paula De Marco** (diretora da escola): é resgatada e abre o espetáculo. Aparência: A DEFINIR (ver `references/`).
- **Jasmine, Gênio, Abu e demais personagens do espetáculo**: aparecem rapidamente no Espaço, com uma fala cada.
- **Jafar** (vilão e chefe): com o figurino do espetáculo.
- **Capivaras** (inimigos de Itajubá): fofas e trapalhonas, nunca assustadoras.
- **Tapete mágico**: estampa com os quadrados do logo.

## 9. Controles, física e som

**Toque** (`ui/ControlesToque.js`):

- Lado esquerdo da tela: botões ◀ e ▶. Lado direito: PULAR (maior) e MAÇÃ.
- Multitoque (correr e pular ao mesmo tempo). Áreas de toque generosas (no mínimo cerca de 64 px na tela real), botões semitransparentes.
- No tapete, os botões somem: segurar em qualquer lugar da tela faz subir, soltar faz descer.
- Teclado: setas ou A/D para andar, espaço ou W para pular, X ou J para maçã, Esc para pausa.

**Física do jogador:**

- Pulo variável (soltar cedo = pulo mais baixo), coyote time de 100 ms e buffer de pulo de 100 ms, para o toque ficar justo.
- Cair em cima de um inimigo derrota o inimigo e dá um quique.
- Maçãs: começa com 5 e recolhe mais pelo caminho. Arremesso em arco curto.
- Toldo: superfície que lança o jogador bem alto.
- Vida: 3 corações. Dano = 1 s de invencibilidade piscando e um pequeno recuo. Sem corações, ou ao cair num buraco, volta ao último checkpoint com vida cheia.
- Câmera segue o jogador com zona morta e respeita os limites do mapa.

**Som:**

- Efeitos sonoros gerados em código com ZzFX (biblioteca minúscula, licença MIT), sem arquivos: pulo, maçã, quique, coleta, dano, vitória.
- Música: MP3 com licença livre (CC0) colocado pelo Pedro em `public/assets/audio/`, ou uma melodia original curta gerada em código. Registrar autoria e licença de tudo que vier de fora em `CREDITS.md`.
- O áudio só começa depois do primeiro toque (exigência dos navegadores de celular). Botão de som liga/desliga sempre visível.

**Mobile:**

- Em modo retrato, mostrar o aviso "Gire o celular" por cima do jogo e pausar.
- Tentar tela cheia ao tocar em JOGAR no Android. No iPhone isso normalmente não funciona para páginas, então o jogo não pode depender disso.
- Layout ocupando 100% da altura visível (`100dvh`), sem rolagem, sem zoom por toque duplo, sem seleção de texto.
- Pausar automaticamente quando a aba perde o foco.

## 10. Mapas em texto

Cada fase é uma lista de strings de mesmo comprimento em `src/levels/`. Legenda:

```
.  vazio
#  bloco sólido (chão, muro)
=  plataforma que se atravessa por baixo
T  toldo (quica)
F  fonte (objeto de 3 tiles de largura, ancorado no canto inferior esquerdo)
C  capivara
a  maçã
s  sapatilha (coletável)
h  coração
K  checkpoint
P  início do jogador
E  saída da fase
```

Exemplo:

```js
export const TESTE = [
  '........................................',
  '..................s.s.s.................',
  '..........TTT...............====........',
  '.....a...................a..............',
  '.P..............C.......F.......C...K..E',
  '########################################',
];
```

## 11. Roteiro, cena a cena

1. **Título**: logo, nome do jogo, botões JOGAR e SOBRE O ESPETÁCULO (mostra os dados do evento e o botão de ingresso, para quem não quer jogar). Aviso de girar o celular.
2. **Intro** (3 caixas de texto, com opção de pular): Aladdin está em Itajubá e descobre que vai ter espetáculo no Teatro do Colégio G9, mas precisa buscar os ingressos no Espaço Paula De Marco.
3. **Fase 1, Itajubá** (60 a 90 s): rua com casas, praça e barracas, morros ao fundo em parallax de 2 ou 3 camadas. Pular a fonte, quicar nos toldos, passar pelas capivaras. Com pisão ou maçã, a capivara pega a maçã e sai feliz comendo, ou adormece com um "zzz". Sapatilhas para coletar e 1 checkpoint no meio. Termina na porta do Espaço Paula De Marco.
4. **Fase 2, Espaço Paula De Marco** (30 a 45 s, sem inimigos): estúdio de dança com espelhos, barras e piso de madeira. Os personagens do espetáculo estão ensaiando; chegar perto de cada um mostra uma fala. Tia Claudia entrega os ingressos e o contador aparece no HUD. Em seguida, alguém chega correndo: o Jafar levou a Tia Paula! Transição para o chefe.
5. **Fase 3, Resgate** (arena de uma tela): Tia Paula presa numa gaiola no canto. O Jafar flutua de um lado para o outro, lança 3 projéteis em leque a cada poucos segundos e fica vulnerável (piscando) logo depois. 5 acertos de maçã para vencer; maçãs reaparecem no chão da arena. Barra de vida do chefe no topo. Ao vencer, o Jafar some numa nuvem de fumaça e a gaiola se abre.
6. **Fase 4, Tapete** (35 a 45 s, rolagem automática): Aladdin e Tia Paula voam sobre Itajubá ao entardecer. Segurar sobe, soltar desce. Obstáculos: pássaros, pipas e fios. Bater só faz piscar e perder sapatilhas, nunca para o jogo. Termina na fachada do Teatro do Colégio G9.
7. **Final**: as cortinas se abrem e Tia Paula, no palco, anuncia que o espetáculo vai começar. Depois aparece um cartão com data, horário, local e ingresso, e os botões:
   - QUERO INGRESSOS (WhatsApp com a mensagem pronta);
   - COMPARTILHAR (`navigator.share` com um texto como "Peguei X sapatilhas no jogo do Aladdin da Paula De Marco! Jogue também:" e o link; sem suporte, copia o link);
   - INSTAGRAM;
   - JOGAR DE NOVO.

**HUD** (cena sobreposta): corações, maçãs, sapatilhas, ingressos (a partir da fase 2), botão de pausa e botão de som.

**Pausa**: continuar, som, sobre o espetáculo, pular para o final.

## 12. Etapas de construção

Cada etapa termina com PR contra `dev` e o checklist da seção 3.

| # | Etapa | Pronto quando |
|---|---|---|
| 0 | Base: Vite + Phaser, estrutura de pastas, `config.js`, `netlify.toml`, `README.md`, cena de teste com um texto na tela, branch `dev` criada | build roda e a página abre no celular |
| 1 | Mobile: escala, aviso de girar, controles de toque e teclado, desbloqueio de áudio, tela cheia no Android, pausa ao perder o foco | controles respondem bem no iPhone e no Android |
| 2 | Jogador e mapas: leitor de mapas em texto, jogador com a física da seção 9, câmera, mapa de teste, pipeline de arte em matriz | correr e pular no celular é gostoso |
| 3 | Fase 1, Itajubá: capivaras, maçãs, toldos, fonte, coletáveis, vida, checkpoint, HUD, transição | fase completa e jogável |
| 4 | Fase 2, Espaço: sistema de diálogo, NPCs, ingressos, transição | diálogo legível e fluido no celular |
| 5 | Fase 3, Chefe | dá para vencer em menos de 1 minuto sem frustração |
| 6 | Fase 4, Tapete | o controle de segurar e soltar fica natural |
| 7 | Título, intro, final, pausa, compartilhar, meta tags (título, descrição, Open Graph com `og-image.png`, favicon) | **jogo completo de ponta a ponta (meta: 08/11)** |
| 8 | Arte: sprites originais em matriz ou PNGs fornecidos, cenários, parallax, animações | visual coerente com a paleta |
| 9 | Som: efeitos com ZzFX, música, botão de som | som funciona no iPhone depois do primeiro toque |
| 10 | Polimento: dificuldade, partículas leves, tremor de tela suave nos impactos, revisão de textos, duração total de 2 a 3 min, peso abaixo de 3 MB | teste completo em 2 celulares diferentes |
| 11 | Lançamento: merge de `dev` em `main` feito pelo Pedro; conferir a prévia do link no WhatsApp | link de produção no ar (meta: 10/11) |

## 13. Pendências do Pedro

- [x] Conectar o repositório no Netlify (01/11/2026): projeto `aladdin-paulademarco`, produção em https://aladdin-paulademarco.netlify.app (`main`), *Branch deploys* = `dev`, *Deploy Previews* ligados. O menu fica em Project configuration > Developer settings > Branches and deploy contexts.
- [ ] Horário do espetáculo, valor e forma de compra do ingresso
- [ ] Fotos dos figurinos em `references/figurinos/`
- [ ] Foto ou descrição da Tia Paula e da Tia Claudia, e o OK das duas para aparecerem no jogo
- [ ] Fotos de referência da fonte de Itajubá e da fachada do Teatro do Colégio G9
- [ ] Logo em boa resolução em `public/assets/logo.png`
- [ ] Música CC0, se não for usar a gerada em código
- [ ] Revisão dos textos em `src/data/textos.js`

## 14. Começar uma sessão nova

- Abra a sessão **só com este repositório** (`PedroCDSR/jogo-aladdin-paula-de-marco`). Nunca junto com o `gns`.
- Leia este arquivo inteiro, depois a seção "Status" abaixo para saber em que etapa está.
- Antes de começar uma etapa: `git fetch origin dev` e crie a branch `etapa-N-nome` a partir de `origin/dev`.
- Para testar no navegador: `npm install`, depois `npm run dev` (o jogo fica em `window.jogo` no console).
- **Não há pesquisa de ROM neste repositório.** A engenharia reversa do cartucho original (feita no início do projeto) serviu só
  de estudo; nenhum arquivo, sprite, som ou código do jogo original entra aqui (regra 3). ROMs (`*.sfc`, `*.smc`, `*.zip`)
  estão no `.gitignore` e nunca devem ser adicionadas.

## Status

| # | Data | PR | Observações |
|---|---|---|---|
| 0 | 01/11/2026 | [PR 1](https://github.com/PedroCDSR/jogo-aladdin-paula-de-marco/pull/1) | Vite 8 + Phaser 4.2.1, estrutura de pastas, fontes woff2 (33 KB), cena de teste com acentos e dados do evento. |
| 1 | 01/11/2026 | [PR 2](https://github.com/PedroCDSR/jogo-aladdin-paula-de-marco/pull/2) | Aviso de girar, controles de toque + teclado, pausa ao perder o foco (volta com toque), som liberado no 1º toque, botão de som, tela cheia + trava deitado no Android. Cena de teste com um bloco que anda, pula e joga maçã. |
| 2 | 01/11/2026 | [PR 3](https://github.com/PedroCDSR/jogo-aladdin-paula-de-marco/pull/3) | Leitor de mapas em texto, Aladdin original provisório (13 quadros em matriz), tiles 16×16, física com pulo variável, coyote e buffer, câmera com zona morta e folga à frente, céu de entardecer e morros. Pulo alto 69 px, pulo curto 34 px. |

**Próximo passo (01/11/2026):** o Pedro testa a prévia do PR 3 no celular (sensação de correr e pular) e faz o merge no
`dev`. Depois, **Etapa 3, Fase 1 (Itajubá)**: capivaras, maçãs com arremesso de verdade, toldos que quicam, fonte,
sapatilhas, corações, checkpoint, HUD e transição. Apresentar o plano curto e esperar o OK antes de começar.

**Decisões técnicas da Etapa 1:**
- O toque é escutado na **div inteira** (`input.touch.target`), não só no canvas: no celular deitado sobram faixas laterais, e é ali que ficam os polegares.
- Os controles leem, a cada quadro, a posição de todos os dedos (`ui/ControlesToque.js`). Multitoque e deslizar de ◀ para ▶ funcionam sem eventos extras. As cenas usam só `ui/Entrada.js` (toque + teclado juntos).
- "Gire o celular" e "Pausado" são HTML **dentro** da div `#jogo`, porque em tela cheia (Android) só aparece o que está dentro do elemento em tela cheia. Pausa com motivos acumulados em `ui/pausaGlobal.js`.
- Depois de perder o foco, o jogo só volta com um toque, para ninguém levar dano no susto.
- O aviso de girar só aparece em aparelho de toque (`pointer: coarse`); no computador, nunca.
- O iPhone silencia o Web Audio quando a chave lateral está no silencioso. Isso é do aparelho e foi mantido de propósito.
- No `npm run dev` o jogo fica em `window.jogo` para depurar no console.

**Decisões técnicas da Etapa 2:**
- **Referências visuais (01/11/2026):** das capturas do Aladdin de SNES usamos só o clima: paleta quente de arenito e terracota, céu de entardecer lilás → rosa, camadas de cenário, toldos de feira (aqui nas cores da escola), contorno escuro com sombra em 2 tons. **Nada** do visual dos personagens (Aladdin/Abu/guardas/Jasmine) nem do palácio.
- Aladdin **provisório e original**: cabelo cacheado escuro, faixa rosa na cabeça, túnica verde com faixa rosa, calça areia, sandálias. Redesenhar com os figurinos.
- A arte nasce de geradores em `ferramentas/arte/` (Python) que escrevem as matrizes em `src/art/`. O jogo só lê as matrizes; dá para editar à mão.
- PNG final: colocar em `public/assets/sprites/` e registrar em `SPRITES_PNG` (`src/art/index.js`). A lista evita pedidos 404.
- Tiles via `Tilemap` do Phaser; `=` e `T` só colidem por cima. O mundo não tem chão invisível: cair abaixo do mapa volta ao checkpoint (por enquanto, o `P`).
- Objetos do mapa (C, a, s, h, K, F, E) aparecem como marcadores coloridos; ganham comportamento na Etapa 3.

**Riscos anotados:**
- Texto com Patrick Hand num canvas de 480×270 ampliado pode ficar serrilhado. Avaliar no celular na Etapa 4; se ficar ruim, desenhar o texto de diálogo numa resolução maior (por exemplo, câmera com zoom 2 num jogo de 960×540).
- O Phaser completo pesa ~1,2 MB minificado (~330 KB comprimido na transferência). Cabe no orçamento; se apertar, trocar pelo build só com Arcade Physics.
