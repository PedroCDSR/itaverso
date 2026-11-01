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
3. **Jogabilidade e linguagem visual inspiradas no Aladdin do Super Nintendo (1993); personagens, cenários e arquivos próprios.** (Revisada em 01/11/2026; substitui a redação anterior, que era lida como proibição de estudar o estilo.)
   - **Permitido e esperado (referência de desenvolvimento):** estudar a fundo as capturas em `references/estilo/`:
     proporção do corpo e do personagem na tela, composição, perspectiva, camadas, arquitetura dos cenários, paleta,
     iluminação, sombreamento (número de tons), contorno, densidade de detalhe, ritmo e técnica de animação. Usar
     essas medidas como **padrão mínimo de qualidade** e criar personagens e cenários próprios com qualidade técnica e
     estética comparável. Mecânicas e números de física também servem de referência. Estilo, técnica e convenções do
     gênero (arenito ao entardecer, toldos de pano que quicam, maçãs, tapete voador) **não** são cópia.
   - **Proibido:** extrair, recortar ou reaproveitar sprites, tiles, cenários, músicas, sons, fontes ou logotipos do
     jogo (Capcom/Disney) ou do filme; decalcar (desenhar por cima) ou redesenhar pixel a pixel qualquer elemento
     deles; reproduzir o **design** de personagens protegidos como a Disney os desenhou (ex.: Aladdin de colete roxo,
     fez vermelho e calça bufante branca; o macaco Abu; Jafar, Gênio, Jasmine e Iago dos filmes) ou a composição
     específica de uma tela do jogo; usar ou redistribuir arquivos de terceiros sem licença. O site é público e
     promove a escola.
   - **Teste prático:** se alguém, vendo o nosso sprite ao lado do original, disser "é o mesmo personagem
     redesenhado", passou do limite. Se disser "tem o mesmo nível e o mesmo jeito de pixel art", está certo.
   - Os personagens seguem os figurinos do espetáculo da escola (seção 8). Assets de terceiros com licença que permita
     o uso podem entrar (`references/licenciados/`), sempre registrados em `CREDITS.md`.
   - A restrição de direito autoral **nunca** justifica arte genérica, simplificada ou abaixo do padrão medido nas
     referências. Toda arte segue a seção 7 (inclusive o protocolo 7.1) e todos os personagens seguem a seção 8.
4. **Leve.** Peso total do site abaixo de 3 MB (limite de 5 MB). A hospedagem é o plano gratuito do Netlify, que cobra créditos por banda.
5. **Site estático.** Sem backend, sem login, sem coleta de dados pessoais.
6. **Textos editáveis num lugar só.** Todo texto exibido no jogo e todos os dados do evento ficam em `src/data/`. Português do Brasil, frases curtas (no máximo 2 linhas por caixa de diálogo), tom leve e divertido para crianças.

## 3. Como trabalhar neste repositório

- **Autonomia até a entrega final (decisão do Pedro, 01/11/2026).** O Pedro define a direção e avalia o jogo pronto;
  a condução técnica e operacional é do Claude. Não pedir aprovação de etapas, protótipos, escalas, personagens,
  cenários ou implementações parciais. Nas decisões técnicas e artísticas, escolher a alternativa que melhor atende ao
  objetivo final, testar comparando, descartar o que ficar abaixo do padrão e continuar trabalhando até atingir os
  critérios. Corrigir integração, inconsistências, duplicações e bugs sem esperar OK. Manter o jogo funcionando no
  `dev` o tempo todo e registrar decisões no PR e na seção "Status".
- **Só consultar o Pedro** quando houver impedimento real que só ele resolve: comprar ou autorizar um asset de
  terceiros, enviar fotos ou informações pessoais, mudança irreversível de escopo, ou algo que impeça continuar.
  Mesmo assim, seguir com uma alternativa provisória **claramente marcada** (seção 7.1) para não travar o resto.
- Falta de aprovação intermediária nunca justifica baixar a qualidade: uma etapa só termina quando atende aos
  critérios da seção 12 e, para arte, ao protocolo 7.1.
- Uma etapa por vez no `dev` (janelas em paralelo estouram o limite de uso e geram conflitos). Antes de etapas grandes, escreva um plano curto no PR, sem esperar OK.
- Branch `main` = produção. Cada deploy de produção consome créditos do plano gratuito do Netlify, então ela só recebe merge no lançamento.
- Branch `dev` = integração. Deploys de `dev` e de PRs são gratuitos.
- Cada etapa: nova branch `etapa-N-nome` a partir de `dev` e PR contra `dev`. Nunca fazer merge em `main`; isso é decisão do Pedro.
- **Regra até o lançamento (decisão do Pedro, 01/11/2026):** o Claude decide sozinho, testa ele mesmo no Chromium com Playwright (sem erros no console, capturas conferidas) e **faz o merge do PR no `dev`**. O Pedro só avalia o produto final antes do lançamento. Não é preciso esperar OK de plano nem teste do Pedro entre as etapas. `main` continua intocável: o merge em `main` é só do Pedro.
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
references/            biblioteca de referências (seção 7.1; não vai para o build)
  visual-reference-index.md   índice: cada arte do jogo, suas referências, situação e diferenças
  figurinos/ pessoas/ lugares/ logo/ estilo/ licenciados/   cada uma com seu reference-notes.md
ferramentas/           geradores de arte (arte/) e de mapas (mapas/), em Python; não vai para o build
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
  horario: '19h',
  local: 'Teatro do Colégio G9, Itajubá/MG',
  ingresso: 'R$ 75,00 · compra pelo WhatsApp com a Tia Claudia',
  whatsapp: '553584713436',
  mensagemWhatsapp:
    'Oi! Vim pelo jogo do Aladdin e quero saber dos ingressos para o espetáculo do dia 20/11.',
  instagram: 'https://www.instagram.com/espacodeartespaulademarco/',
};
```

O botão de ingresso abre `https://wa.me/<whatsapp>?text=<mensagem com encodeURIComponent>`. A compra é feita com a **Tia Claudia** por esse WhatsApp (informação do Pedro, 01/11/2026). A mensagem pronta permite à escola saber quantos contatos vieram do jogo.

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

- Tiles de 16×16. **Escala dos personagens (decisão de 01/11/2026):** quadros de 48×64, corpo do Aladdin com ~56 a
  60 px de altura (≈ 21 a 22% da altura da tela de 270). Nas capturas de referência o herói ocupa ≈ 28% da tela; com
  os 32×48 antigos ficava em ≈ 15%, pequeno demais para o nível de detalhe esperado. Hitbox, pulos e mapas são
  reajustados junto (seção 9 continua valendo). Os números exatos ficam em `references/estilo/reference-notes.md`.
- Enquanto não houver PNGs, cada sprite é uma matriz de texto em `src/art/` (um caractere por pixel, cada caractere mapeado a uma cor), convertida em textura no `Preload`. A matriz é só o formato do arquivo: o padrão de qualidade é o da seção 7.1, não "arte simples".
- **Fonte única:** cada personagem e cada objeto tem **um** sprite em `src/art/`, usado por todas as cenas. Nada de redesenhar o mesmo personagem em outra cena com `Graphics` ou num gerador paralelo.
- Quando existir `public/assets/sprites/<nome>.png` com os mesmos tamanhos de quadro, o `Preload` usa o PNG no lugar da matriz.
- Animações mínimas do jogador: parado (2 quadros), correndo (6), pulando (1), caindo (1), arremessando (2), dano (1).

### 7.1 Protocolo de fidelidade visual

(Recriada em 01/11/2026. A primeira versão existiu das 02:16 às 02:22 e foi removida; esta corrige os problemas dela:
proibia estudar proporções das capturas, exigia não inventar quando não havia referência e tinha tabelas que ninguém
preenchia.)

Vale para personagens, cenários, objetos, animações, HUD e menus. Fidelidade visual é requisito de qualidade **desde o
primeiro rascunho**, não polimento posterior.

**Tipos de referência e o que se exige de cada um:**

| Pasta | Conteúdo | O que seguir com fidelidade |
|---|---|---|
| `figurinos/` | fotos dos figurinos do espetáculo | design do personagem: silhueta, peças, cores, acessórios |
| `pessoas/` | Tia Paula e Tia Claudia (com o OK delas) | traços que identificam: cabelo, óculos, roupa típica |
| `lugares/` | Itajubá, Espaço, Teatro do Colégio G9 | arquitetura, cores, elementos marcantes |
| `logo/` | logo da escola | paleta e estampa do tapete |
| `estilo/` | capturas de jogos (Aladdin do SNES) | **linguagem e qualidade**: escala, tons, contorno, luz, densidade, animação. Nunca o design (regra 3) |
| `licenciados/` | assets de terceiros com licença | uso direto conforme a licença, com `CREDITS.md` |

**Antes de implementar:**

1. Abrir as imagens relevantes; ler o `reference-notes.md` da pasta e o `references/visual-reference-index.md`.
2. Escrever no PR a **ficha da arte**: referências usadas e medidas-alvo (altura em px e % da tela, número de tons por
   material, cores-chave em hex, tipo de contorno, número de quadros, densidade de detalhe do cenário).

**Durante:**

3. Um sprite por personagem ou objeto, usado por todas as cenas (seção 7, "Fonte única").
4. Arte provisória é marcada como **provisória** no índice e nunca é tratada como final.

**Depois (obrigatório para concluir):**

5. Gerar uma **prancha comparativa** lado a lado (referência × nossa, mesma escala) em `ferramentas/arte/previas/`.
6. Listar as diferenças de proporção, silhueta, cores, composição, sombreamento e acabamento.
7. Corrigir o que for possível. Registrar no índice e no PR as diferenças que ficam e o motivo.

**Não está concluída se:** só "dá para reconhecer"; funciona, mas está abaixo das medidas-alvo; ou as diferenças não
foram registradas.

**Referência insuficiente:** dizer o que falta, o impacto e o que o Pedro precisa enviar (seção 13). Até lá, fazer uma
versão com a qualidade técnica completa, marcada como **provisória**, sem inventar traços de identidade de pessoas
reais (rosto, cabelo, roupa típica) além do que já está escrito na seção 8. Nunca apresentá-la como final.

**Relação com a regra 3:** a regra 3 define o que não pode ser copiado; esta seção define o nível de qualidade. Nenhuma
das duas justifica entregar arte genérica.

## 8. Personagens

Todos com design próprio. O elenco se baseia nos figurinos do espetáculo (`references/figurinos/`): desenhar a versão da escola, com a qualidade medida em `references/estilo/`. Não reproduzir o design de personagens de filme, animação ou jogo (regra 3); estudar a linguagem visual deles é permitido. Não retratar o rosto de alunos; usar só os figurinos como referência. Enquanto não houver fotos, cada personagem tem um design próprio provisório, com qualidade completa e marcado no índice (seção 7.1).

- **Aladdin** (jogador): herói ágil, com o figurino do espetáculo.
- **Tia Claudia** (staff do Espaço): usa óculos, tem cabelo preto e pele branca (informação do Pedro, 01/11/2026). Entrega os ingressos.
- **Tia Paula De Marco** (diretora da escola): é resgatada e abre o espetáculo. **Loira, de pele branca, de rabo de cavalo, com camiseta preta** (a camiseta preta do espetáculo, com "Aladdin" dourado, fumaça azul e roxa e a lâmpada: `references/pessoas/tia-paula-camiseta-aladdin.jpg`). Informação do Pedro, 01/11/2026. O resto (rosto, calça, sapatos): neutro e provisório até a foto.
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
- Escala 48×64 (Etapa 8.0): caixa de colisão de 18×46 (cabe em vãos de 3 tiles), pulo alto de 80 px (5 tiles), pulo
  curto de ~38 px, toldo de ~150 px segurando PULAR. O muro de 6 tiles da Fase 1 continua pedindo o toldo.
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
- **Sem tela cheia automática** (decisão do Pedro, 01/11/2026): o jogo roda no navegador normal ocupando `100dvh`. No Android, a tela cheia faz o Chrome mostrar por vários segundos a faixa "Para sair da tela cheia..." por cima do começo do jogo. Também não há trava de orientação.
- Tela cheia **opcional** pelo botão "TELA CHEIA" do menu de pausa (só aparece onde o navegador permite; no iPhone, não).
- `public/manifest.webmanifest` (`display: fullscreen`, `orientation: landscape`, ícones): quem usar "Adicionar à tela inicial" abre o jogo sem barras e deitado.
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
N  personagem que conversa (quem é cada um, da esquerda para a direita, vem de uma lista no arquivo da fase)
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
3. **Fase 1, Itajubá** (60 a 90 s): rua com casas, praça e barracas, morros ao fundo em parallax de 2 ou 3 camadas. **Lugares reais, nesta ordem** (pedido do Pedro, 01/11/2026; fotos e detalhes em `references/lugares/reference-notes.md`): Clube Itajubense (no fundo) → fonte da praça com o busto do Teodomiro Santiago → Café do Vadinho → Igreja Matriz → posto Esso, "o menor posto de gasolina do mundo" (placa "ESSO" em letras de pixel próprias; decisão do Pedro, 01/11/2026) → Praça do Soldado (estátua e helicóptero). Pular a fonte, quicar nos toldos, passar pelas capivaras. Com pisão ou maçã, a capivara pega a maçã e sai feliz comendo, ou adormece com um "zzz". Sapatilhas para coletar e 1 checkpoint no meio. Termina na porta do Espaço Paula De Marco.
4. **Fase 2, Espaço Paula De Marco** (30 a 45 s, sem inimigos): estúdio de dança com espelhos, barras e piso de madeira. Os personagens do espetáculo estão ensaiando; chegar perto de cada um mostra uma fala. Tia Claudia entrega os ingressos e o contador aparece no HUD. Em seguida, alguém chega correndo: o Jafar levou a Tia Paula! Transição para o chefe.
5. **Fase 3, Resgate** (arena de uma tela, **ao pôr do sol**: o sol encostando na serra; decisão do Pedro, 01/11/2026): Tia Paula presa numa gaiola no canto, **visível dentro dela**. O Jafar flutua de um lado para o outro, lança 3 projéteis em leque a cada poucos segundos e fica vulnerável (piscando) logo depois. 5 acertos de maçã para vencer; maçãs reaparecem no chão da arena. Barra de vida do chefe no topo. Ao vencer, o Jafar some numa nuvem de fumaça e a gaiola se abre.
6. **Fase 4, Tapete** (35 a 45 s, rolagem automática): Aladdin e Tia Paula voam sobre Itajubá **no crepúsculo** (sol já posto, brilho laranja no horizonte, primeiras estrelas, janelas acendendo), passando pelo Hotel Coroados e pela UNIFEI, com a serra ao fundo; os pássaros são tucanos e maritacas. Segurar sobe, soltar desce. Obstáculos: pássaros, pipas e fios. Bater só faz piscar e perder sapatilhas, nunca para o jogo. Termina na fachada do Teatro do Colégio G9.
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
| 8 | Arte, em 3 partes: **8.0** guia de linguagem visual (medidas-alvo tiradas de `references/estilo/`, escala 48×64, ajuste de hitbox e pulos); **8A** personagens (um sprite por personagem, ligado a todas as cenas, sem duplicatas); **8B** cenários de todas as fases, parallax, objetos e camada da frente | protocolo 7.1 cumprido: medidas-alvo atingidas, pranchas comparativas em `ferramentas/arte/previas/`, índice atualizado, nenhuma arte provisória sem marcação |
| 9 | Som: efeitos com ZzFX, música, botão de som | som funciona no iPhone depois do primeiro toque |
| 10 | Polimento e revisão geral: dificuldade, partículas leves, tremor de tela suave nos impactos, revisão de textos, duração total de 2 a 3 min, peso abaixo de 3 MB, consistência visual entre fases, animações e transições, nenhuma duplicata ou provisório indevido, testes de regressão, `og-image` regenerada, `CREDITS.md` e documentação, relatório final para o Pedro | jogada completa automatizada sem erros em tamanhos de iPhone e Android; relatório entregue |
| 11 | Lançamento: merge de `dev` em `main` feito pelo Pedro; conferir a prévia do link no WhatsApp | link de produção no ar (meta: 10/11) |

## 13. Pendências do Pedro

- [x] Conectar o repositório no Netlify (01/11/2026): projeto `aladdin-paulademarco`, produção em https://aladdin-paulademarco.netlify.app (`main`), *Branch deploys* = `dev`, *Deploy Previews* ligados. O menu fica em Project configuration > Developer settings > Branches and deploy contexts.
- [x] Horário do espetáculo (19h), valor (R$ 75,00) e forma de compra (WhatsApp com a Tia Claudia), informados em 01/11/2026
- [ ] Fotos dos figurinos em `references/figurinos/`
- [ ] Foto ou descrição da Tia Paula e da Tia Claudia, e o OK das duas para aparecerem no jogo
- [ ] Testar os 3 níveis de dificuldade no celular
- [x] Fotos dos lugares da Fase 1 (Clube Itajubense, fonte da praça, Café do Vadinho, Igreja Matriz, posto Esso, Praça do Soldado), enviadas em 01/11/2026
- [ ] Fotos da fachada do Teatro do Colégio G9 e do estúdio do Espaço
- [ ] Logo em boa resolução em `public/assets/logo.png`
- [ ] Música CC0, se não for usar a gerada em código
- [ ] Revisão dos textos em `src/data/textos.js`
- [ ] (Opcional) Comprar o pacote "8-bit Capibaras" do 14collective (itch.io, US$ 2; a página diz que pode ser usado em projetos comerciais) e subir os arquivos em `references/licenciados/`. Sem ele, a capivara é própria, desenhada no mesmo nível de qualidade.

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
| 3 | 01/11/2026 | [PR 7](https://github.com/PedroCDSR/jogo-aladdin-paula-de-marco/pull/7) | Fase 1 com 320 colunas: rua, feira com 6 barracas de toldo, praça com fonte, checkpoint, buracos e plataformas, porta do Espaço. 12 capivaras (pisão = dorme; maçã = come e vai embora; de lado = 1 coração), 38 sapatilhas, 9 maçãs, 3 corações. HUD com corações, maçãs, sapatilhas, pausa e som. Casario de Itajubá no fundo (3 camadas). `dist/` com 1,5 MB. |
| 4 | 01/11/2026 | [PR 12](https://github.com/PedroCDSR/jogo-aladdin-paula-de-marco/pull/12) | Fase 2 com 100 colunas: estúdio com espelhos, barras, piso de madeira e tablados. Diálogo em HTML nítido (Patrick Hand, até 2 linhas, máquina de escrever, avança com toque ou tecla). Jasmine, Gênio e Sultão ensaiando (1 fala cada), Tia Claudia no balcão entrega 4 ingressos que voam até o contador do HUD, Abu chega correndo com a notícia. Cena `Chefe` provisória. `?fase=espaco` abre direto na Fase 2. Já junta as Etapas 6 e 9: o jogo vai da Fase 1 ao Final. `dist/` com 1,56 MB. |
| 5 | 01/11/2026 | [PR 13](https://github.com/PedroCDSR/jogo-aladdin-paula-de-marco/pull/13) | Fase 3 (Resgate): arena de uma tela (terraço com arcos ao anoitecer), Tia Paula numa gaiola pendurada no canto, Jafar original e provisório que flutua, avisa piscando, lança 3 projéteis em leque e desce cansado e piscando (vulnerável). 5 acertos de maçã (no máximo 2 por descida), barra de vida no topo, maçãs que reaparecem no chão. Vitória: fumaça, gaiola abre, Tia Paula agradece e vai para o Tapete. Robôs no Chromium venceram em 17,8 s (ágil) e 29,6 s (lento, sem desviar, voltou ao início 1 vez). `dist/` com 1,60 MB. |
| 6 | 01/11/2026 | [PR 8](https://github.com/PedroCDSR/jogo-aladdin-paula-de-marco/pull/8) | Fase 4 (Tapete): rolagem automática de 40 s + pouso de ~4 s no Teatro do Colégio G9, segurar sobe / soltar desce (toque em qualquer lugar, espaço, W ou seta para cima), pássaros (sabiás), pipas, postes e fios, sapatilhas no céu, batida = pisca e perde 2 sapatilhas. Tela Final provisória. Teste direto: `?fase=tapete`. Feita antes das Etapas 4 e 5 (modo autônomo). `dist/` = 1,51 MB (já com a Etapa 3). |
| 7 | 01/11/2026 | [PR 11](https://github.com/PedroCDSR/jogo-aladdin-paula-de-marco/pull/11) | Título, Sobre o espetáculo, Intro (3 caixas, PULAR), Final completo (cortinas, Tia Paula anuncia, cartão com QUERO INGRESSOS, COMPARTILHAR, INSTAGRAM, JOGAR DE NOVO), menu de pausa (continuar, som, tela cheia opcional, sobre, pular para o final), meta tags + Open Graph + favicon + manifest. Tela cheia automática removida. Fluxo completo: Título → Intro → Itajubá → Espaço → Chefe → Tapete → Final. `dist/` = 1,63 MB (com todas as etapas). |
| 9 | 01/11/2026 | [PR 10](https://github.com/PedroCDSR/jogo-aladdin-paula-de-marco/pull/10) | Som feito antes das Etapas 4, 5, 7 e 8. 13 efeitos com ZzFX (pulo, maçã, toldo, pisão, capivara comendo, sapatilha, maçã e coração recolhidos, dano, botão, blip de diálogo, acerto no chefe, projétil), 6 músicas originais em loop (título, Itajubá, Espaço, Chefe, Tapete, Final) e 3 vinhetas (checkpoint, ingresso, vitória), tudo em código. Desbloqueio do áudio refeito para o iPhone. Botão de som e tecla M lembram a escolha. Fase 1, Tapete e Final já ligados. `dist/` com 1,45 MB. |
| 8.0 | 01/11/2026 | [PR 17](https://github.com/PedroCDSR/jogo-aladdin-paula-de-marco/pull/17) | Guia de linguagem visual com medidas das capturas (`references/estilo/reference-notes.md`) e paleta de cenário. Escala 48×64: Aladdin redesenhado (provisório no design, final na qualidade) com o renderizador de volumes `ferramentas/arte/modelo.py`: 58 px = 21,5% da tela, 4 tons por material, contorno colorido, 23 quadros (parado 4, corrida 8, pulo 2, queda 2, arremesso 3 com antecipação, dano 1, sentado 3). Aladdin do tapete sai do mesmo sprite. Caixa 18×46, pulo 80 px. Pranchas em `ferramentas/arte/previas/8-0-*.png`. Robô novo (`ferramentas/teste/jogar.mjs`) jogou do Título ao Final em 157 s e 260 s (duas jogadas; a diferença é o robô caindo no buraco das colunas 164 a 168), sem erros. `dist/` = 1,69 MB. |
| 8A+8B | 01/11/2026 | [PR 23](https://github.com/PedroCDSR/jogo-aladdin-paula-de-marco/pull/23) | Prévias aprovadas pelo Pedro levadas ao jogo. **Personagens:** Aladdin v2 (corpo esguio, rosto novo, colete verde aberto, calça larga lilás que esvoaça, piscada e aterrissagem), Tia Paula (loira, rabo de cavalo, camiseta preta do espetáculo; um sprite só para Chefe, Tapete e Final), Tia Claudia, Jasmine, Sultão, Gênio, Abu (macaco-prego com chapeuzinho azul) e Jafar na escala nova, em PNG (`gerar_elenco.py`); capivara mantida. **Lugares:** rua de paralelepípedo, Serra da Mantiqueira verde, Clube Itajubense, fonte com o busto, Café do Vadinho, Igreja Matriz, posto Esso e Praça do Soldado na Fase 1; arena ao pôr do sol com a Tia Paula visível na gaiola; voo no crepúsculo com Hotel Coroados, UNIFEI, tucanos e maritacas (`gerar_cenarios.py`). |
| Correções + níveis | 01/11/2026 | [PR 24](https://github.com/PedroCDSR/jogo-aladdin-paula-de-marco/pull/24) | **Bugs:** gaiola fechada durante a luta (2 barras finas na frente, Tia Paula visível); tiles na frente dos lugares (a igreja escondia plataforma e toldo; o toldo virou escadinha encostada no muro e a plataforma virou tábua no buraco); Clube Itajubense todo branco; rua e muro embaixo dos prédios do voo; morro do Hotel Coroados com topo largo. **Maçãs sem limite.** **Dificuldade** escolhida no Título depois de JOGAR (`src/dificuldade.js`, lembra a última escolha; teste: `?dificuldade=facil`): fácil = Fase 1 com 192 colunas e sem buracos, Espaço com 60 colunas, Tapete com 4 trechos (20 s), 5 corações, Jafar com 3 de vida e leque de 2 tiros mais lentos, perde 1 sapatilha; médio (escolha do Claude, padrão) = mapas inteiros, 4 corações, Jafar com 4 de vida e tiros um pouco mais lentos, perde 1 sapatilha; difícil = o jogo de antes. Robô: fácil 96 s, médio 146 s, difícil 142 s, sem erros. `dist/` = 2,0 MB. |
| Sapatilha nova | 01/11/2026 | (este PR) | Par de sapatilhas de ponta rosa bebê, de frente, lado a lado (19×18, laço no alto, fitas cruzadas em X sobre a palmilha creme, brilho piscando), desenho próprio a partir dos prints do Pedro (só referência, não vão para o repositório). A mesma arte vale na Fase 1, no Espaço, no céu do Tapete e no HUD (a `sapatilhaCeu` saiu). Contadores do HUD afastados para caber o ícone. |

**Próximo passo (01/11/2026):** as Etapas 3 a 7, 8.0 e 9 estão no `dev`: o jogo vai de ponta a ponta (Título → Intro →
Itajubá → Espaço → Chefe → Tapete → Final), com o herói novo na escala 48×64. Próximas, uma por vez:
**8A** personagens na escala 48×64 com `ferramentas/arte/modelo.py` (Jasmine, Gênio, Sultão, Abu, Tia Claudia, Tia
Paula loira, Jafar, capivara; aproveitar só o que servir da branch `etapa-8a-personagens`, que ainda está em 32×48) →
**8B** cenários (partindo da branch `etapa-8b-cenarios`) → **10** polimento, revisão geral e relatório final. Novas
fases que usam o HUD precisam estar em `FASES` (`src/fluxo.js`) para o menu de pausa funcionar nelas. Para testar
direto: `?fase=itajuba`, `?fase=espaco`, `?fase=chefe`, `?fase=tapete`, `?fase=final`. Jogada automática:
`node ferramentas/teste/jogar.mjs` com o `npm run dev` rodando.
O Pedro só testa no fim, antes do lançamento, e revisa as falas em `src/data/textos.js`.

**Decisões dos níveis de dificuldade (01/11/2026):**
- Pedido do Pedro: o jogo estava difícil; o nível de antes virou o "difícil". Fácil = ~40% mais curto, sem buracos e Jafar 50% mais fraco. O médio ficou a critério do Claude.
- `src/dificuldade.js` guarda os valores originais de `JOGADOR`, `CHEFE` e `TAPETE` e aplica por cima os ajustes do nível (as cenas continuam lendo `config.js`). Os mapas curtos (`ITAJUBA_FACIL`, `ESPACO_FACIL`, `TAPETE_FACIL`) saem dos mesmos geradores e as cenas escolhem com `mapaCurto()`.
- O mapa fácil da Fase 1 corta 5 trechos do mapa inteiro (`CORTES` em `gerar_itajuba.py`) e tapa os buracos; os 6 lugares reais continuam e mudam de coluna junto (`ITAJUBA_FACIL_LUGARES`).
- Medido com o robô, o fácil ficou ~32% mais curto, não 40%: as falas do Espaço e o pouso do tapete têm tempo fixo. Para gente de verdade a diferença deve ser maior, porque é na Fase 1 e no chefe que se perde mais tempo.

**Decisões técnicas da Etapa 1:**
- O toque é escutado na **div inteira** (`input.touch.target`), não só no canvas: no celular deitado sobram faixas laterais, e é ali que ficam os polegares.
- Os controles leem, a cada quadro, a posição de todos os dedos (`ui/ControlesToque.js`). Multitoque e deslizar de ◀ para ▶ funcionam sem eventos extras. As cenas usam só `ui/Entrada.js` (toque + teclado juntos).
- "Gire o celular" e "Pausado" são HTML **dentro** da div `#jogo`, porque em tela cheia só aparece o que está dentro do elemento em tela cheia. Pausa com motivos acumulados em `ui/pausaGlobal.js`.
- ~~Tela cheia + trava deitado ao tocar em JOGAR no Android.~~ Removido na Etapa 7 (decisão do Pedro): a faixa "Para sair da tela cheia..." do Chrome atrapalhava o começo. Agora a tela cheia é só pelo botão da pausa (`ui/telaCheia.js`), sem trava de orientação, e há o manifest para "Adicionar à tela inicial".
- Depois de perder o foco, o jogo só volta com um toque, para ninguém levar dano no susto.
- O aviso de girar só aparece em aparelho de toque (`pointer: coarse`); no computador, nunca.
- O iPhone silencia o Web Audio quando a chave lateral está no silencioso. Isso é do aparelho e foi mantido de propósito.
- No `npm run dev` o jogo fica em `window.jogo` para depurar no console.

**Decisões técnicas da Etapa 2:**
- *(Substituída em 01/11/2026 pela nova regra 3 e pela seção 7.1: as capturas agora valem como padrão de linguagem e de qualidade, não só de clima.)* ~~**Referências visuais (01/11/2026):** das capturas do Aladdin de SNES usamos só o clima:~~ paleta quente de arenito e terracota, céu de entardecer lilás → rosa, camadas de cenário, toldos de feira (aqui nas cores da escola), contorno escuro com sombra em 2 tons. **Nada** do visual dos personagens (Aladdin/Abu/guardas/Jasmine) nem do palácio.
- Aladdin **provisório e original**: cabelo cacheado escuro, faixa rosa na cabeça, túnica verde com faixa rosa, calça areia, sandálias. Redesenhar com os figurinos.
- A arte nasce de geradores em `ferramentas/arte/` (Python) que escrevem as matrizes em `src/art/`. O jogo só lê as matrizes; dá para editar à mão.
- PNG final: colocar em `public/assets/sprites/` e registrar em `SPRITES_PNG` (`src/art/index.js`). A lista evita pedidos 404.
- Tiles via `Tilemap` do Phaser; `=` e `T` só colidem por cima. O mundo não tem chão invisível: cair abaixo do mapa volta ao checkpoint (por enquanto, o `P`).
- Objetos do mapa (C, a, s, h, K, F, E) aparecem como marcadores coloridos; ganham comportamento na Etapa 3.

**Decisões técnicas da Etapa 3:**
- Decisões do Pedro (01/11/2026): ele delegou as escolhas. Branch `etapa-3-itajuba`; encostar de lado numa capivara acordada tira 1 coração.
- ~~A seção 7.1 (gestão rígida de referências) foi removida a pedido do Pedro. Continua valendo a regra 3: as capturas do jogo original em `references/` servem só de clima, nunca de modelo de personagem, sprite ou cenário.~~ *(Substituída em 01/11/2026: a 7.1 foi recriada e a regra 3 revisada; ver a seção "Revisão das instruções de arte".)*
- Mapa montado por trechos em `ferramentas/mapas/gerar_itajuba.py` (anota alcance do pulo e do toldo). O `src/levels/itajuba.js` gerado é editável à mão.
- Arte dos objetos (capivara com 6 quadros, maçã, sapatilha, coração cheio/vazio, fonte com água animada, bandeira) em `ferramentas/arte/gerar_objetos.py` → `src/art/objetos.js`. Casario e torre da igreja são desenhados em canvas no `Preload`; barracas e fachada do Espaço, com `Graphics` na cena.
- HUD é uma cena separada (`scenes/HUD.js`) que lê o `registry` (`vida`, `vidaMax`, `macas`, `sapatilhas`). O botão de pausa abre o menu de pausa da Etapa 7.
- Toldo: quica 520 segurando PULAR (≈150 px) e 420 sem segurar (≈98 px). Pisar na capivara segurando PULAR também vai mais alto.
- Maçã: arco baixo que quica até 3 vezes e rola, para acertar capivaras de perto e de longe (até ~140 px). O `overlap` do Arcade entre dois grupos não disparou para maçã × capivara; a checagem é feita à mão no `update()`.
- Ao voltar ao checkpoint: vida cheia, 1 s de invencibilidade e no mínimo 3 maçãs. Capivaras dormindo continuam dormindo.
- Coração só é recolhido se faltar vida; maçã só se houver espaço (máximo 9).
- Ao chegar na porta, a Fase 2 começa (a tela `EmBreve` saiu na Etapa 4; a tela "JOGAR" provisória saiu na Etapa 7).
- Teste automatizado no Chromium (Playwright) conferiu: pisão, maçã, quique no toldo, checkpoint, buraco, 3 danos, coleta, chegada na porta e jogar de novo, sem erros no console.

**Decisões técnicas da Etapa 4:**
- Modo autônomo autorizado pelo Pedro (01/11/2026): decisões tomadas sem esperar OK e registradas aqui e no PR.
- Quando a etapa começou, o `dev` ainda não tinha a Etapa 3; a branch recebeu o PR 7 por merge. Enquanto isso, outras sessões mergearam as Etapas 3, 6 e 9 no `dev`; antes do merge, a branch juntou o `dev` de novo e ligou tudo: som novo no Espaço (música `espaco`, sapatilha, pulo, vinheta `ingresso`, `blip` a cada 3 letras do diálogo), `Chefe` provisória com CONTINUAR → Tapete (música `chefe`) e JOGAR DE NOVO do Final voltando à Fase 1. A tela `EmBreve` saiu.
- **Texto serrilhado (risco da Etapa 2): resolvido com HTML.** O canvas de 480×270 é ampliado inteiro, então qualquer texto do Phaser fica com a resolução do jogo, por mais que se aumente a fonte. A caixa de diálogo (`ui/Dialogo.js`) é uma `div` dentro de `#jogo` (aparece em tela cheia), posicionada sobre o canvas a cada quadro, com todas as medidas em "pixels do jogo" × escala (variável CSS `--u`). Assim a quebra de linha é a mesma em qualquer tela e a letra sai nítida. Resultado conferido em captura de 844×390 com densidade 3 (iPhone deitado).
- Diálogo: no máximo 2 linhas (no `npm run dev` aparece aviso no console se passar), "máquina de escrever" no relógio da cena (para junto com a pausa), 1º toque completa o texto, o seguinte avança, seta rosa piscando quando dá para avançar. Só conta o toque que **começou** com a caixa aberta (o dedo que segurava ▶ ao chegar no NPC não pula a fala) e há 250 ms mínimos por caixa. Teclas: espaço, Enter, W, X, J, seta para cima. A tecla que tira da pausa não avança a fala (a escuta é na fase de captura). Ao fechar, `Entrada.ignorarAteSoltar()` evita que o mesmo toque vire pulo.
- Conversa dispara pela distância só em x (44 px), para ninguém passar pulando por cima sem querer. Enquanto conversa, o jogador fica parado. Quem ainda não falou tem um balãozinho "..." e olha para o jogador.
- Personagens originais e provisórios em `ferramentas/arte/gerar_espaco.py` → `src/art/espaco.js` (as fotos dos figurinos ainda não chegaram; as capturas de jogo foram movidas para `references/estilo/` e, desde a revisão de 01/11, valem como padrão de qualidade, não só de clima): Jasmine (trança, tiara, top lilás, calça bufante rosa; 2 quadros de balé), Gênio (pele lilás, coque, colete rosa, cauda de fumaça amarela; flutua), Sultão (turbante rosa com pena, barba branca, capa roxa; bate palmas), Tia Claudia (cabelo preto no ombro, óculos de armação roxa, camiseta rosa com os quadradinhos do logo; quadro com os ingressos na mão), Abu (macaquinho com colete rosa e chapéu roxo; correndo e aflito). Nenhum usa as cores ou silhuetas do filme.
- Mapa da Fase 2 em `ferramentas/mapas/gerar_espaco.py` → `src/levels/espaco.js`. Novo caractere `N` (personagem); quem é cada um vem de `NPCS_ESPACO`, na ordem. Tiles do estúdio usam a mesma `ORDEM` de `tiles.js` com outra textura (`tiles-espaco`): piso de madeira e tablado lilás (atravessa por baixo).
- Parede com espelhos e barras desenhada em canvas no `Preload` (faixa de 240 px repetida); cartaz "ALADDIN · 20/11", balcão e porta com `Graphics` na cena.
- Sem inimigos: o botão MAÇÃ some (`ControlesToque.esconderBotao`). Vida cheia ao entrar; maçãs e sapatilhas da Fase 1 continuam.
- Ingressos: a Tia Claudia entrega 4 (`ESPACO.ingressos` em `config.js`). O HUD mostra o contador só quando `ingressos` não é `null` (a Fase 1 zera para `null`). O total de sapatilhas das duas fases vai em `sapatilhasTotal`.
- Quem chega correndo é o **Abu**, pela porta do fundo do estúdio: "O Jafar levou a Tia Paula!". A Tia Claudia fecha com "Corre, Aladdin!". Transição com clarão roxo e escurecida para `scenes/Chefe.js`, tela provisória com sapatilhas, ingressos e CONTINUAR (vai para o Tapete) até a Etapa 5.
- `?fase=espaco` e `?fase=chefe` entraram na mesma lista do `?fase=tapete` (`FASES` no `Preload`). Valem também na produção; não atrapalham quem joga normalmente.
- Teste automatizado no Chromium (Playwright), sem erros no console: fase inteira com teclado (4 conversas, 13 caixas, 4 ingressos, chegada no Chefe em 28 s com o robô lendo ~1 s por caixa); com toque em 844×390: Fase 1 → porta → Fase 2, dedo antigo não avança a fala, pausa no meio do diálogo e volta sem avançar, toque avança e fecha.

**Decisões técnicas da Etapa 5 (chefe):**
- Modo autônomo autorizado pelo Pedro (01/11/2026): decisões tomadas sem esperar OK e registradas aqui e no PR.
- Começou quando o `dev` ainda só tinha a Etapa 2. A base que o chefe precisava (vida e dano do jogador, HUD, arte de maçã e coração) foi copiada **sem mudanças** do PR 7, para não duplicar código. Antes do merge, a branch juntou o `dev` com as Etapas 3, 4, 6 e 9: a `Chefe` provisória e a `Tapete` provisória desta etapa saíram, ficou o atalho `?fase=` do `Preload`, e o chefe ganhou o som da Etapa 9 e o diálogo da Etapa 4.
- Ciclo do Jafar (`objects/Jafar.js`, números em `CHEFE` no `config.js`): flutua de um lado para o outro lá em cima (2,2 s) → pisca em amarelo (0,6 s, aviso) → 3 projéteis em leque mirando o jogador (22° entre eles, 115 px/s) → desce cansado até a altura da maçã e pisca por 3,6 s → sobe. Só leva dano de maçã cansado; maçã que bate nele voando só faz um "tic".
- No máximo **2 acertos por descida** (depois ele sobe na hora), então são pelo menos 3 descidas: a luta não acaba num sopro, mas também não se arrasta. Encostar no Jafar não machuca; só os projéteis tiram coração.
- **Sem game over e sem frustração:** sem corações, volta ao começo da arena com vida cheia, no mínimo 3 maçãs, e **a vida do Jafar continua como estava** (`manterVidaAoReiniciar`). Ninguém perde o progresso da luta.
- Maçãs: o jogador entra com as que trouxe (no mínimo 5). Há 2 lugares no chão (`a` no mapa) onde aparece uma maçã; quando alguém pega, outra surge no mesmo lugar 2 s depois.
- Barra de vida do Jafar no topo, entre os contadores do HUD e os botões de pausa e som (x de 212 a 398, sem encostar no contador de ingressos). Uma marquinha por acerto.
- A gaiola fica **pendurada** no canto de cima à direita, e não no chão: no celular o botão PULAR cobria a gaiola e a Tia Paula. Na vitória a porta abre e ela pula para o chão.
- Falas: Jafar e Tia Paula na caixa de diálogo da Etapa 4 (entrada e agradecimento; a luta só começa depois da fala). "Socorro!", "ai!" e "Nããão! Puf!" são balõezinhos rápidos do Phaser. Música `chefe`; efeitos `projetil`, `acertoChefe`, `maca`, `pegarMaca`, `dano` e `pulo`; vinheta `vitoria` quando a gaiola abre. No fim: `scene.stop('HUD')` + `scene.start('Tapete')`.
- Vindo da Fase 2, o chefe começa direto (o `registry` já tem `vida`). Pelo atalho `?fase=chefe`, aparece a tela JOGAR, porque é o toque que libera o som.
- Arte original e provisória em `ferramentas/arte/gerar_chefe.py` → `src/art/chefe.js`: **Jafar** (mago de capuz roxo pontudo com beirada lilás, bigodão enrolado, cavanhaque, medalhão de lua dourado, forro magenta, varinha de estrela, cauda de fumaça no lugar das pernas; 4 quadros: flutuar ×2, lançar, tonto com olhos em X), projétil (estrela magenta girando, desenhada 1,5× maior para ver no celular), gaiola dourada (fechada com cadeado / aberta) e **Tia Paula** em pé (aparência A DEFINIR: mesmas cores da Tia Paula do tapete, coque castanho e vestido roxo com faixa amarela; 4 quadros: pedindo socorro ×2, feliz, parada). Nada segue o filme: sem turbante, sem preto e vermelho, sem cajado de cobra. Redesenhar o Jafar quando chegarem as fotos do figurino.
- Arena em `src/levels/chefe.js` (30×17 tiles, 2 plataformas). Céu do entardecer escurecido, estrelas, lua, morros e um terraço com colunas e arcos desenhado com `Graphics`.
- Teste automatizado no Chromium (Playwright), sem erros no console: robô ágil (desvia dos projéteis) venceu em 17,8 s; robô sem desvio venceu em 17,5 s levando 1 dano; robô lento (reage 1,2 s depois e joga 1 maçã a cada 0,8 s) venceu em 29,6 s, levou 4 danos e voltou ao início 1 vez. Também conferidos: tela de celular deitado (iPhone 13) com os botões de toque, passagem da Fase 2 para o chefe com os ingressos no HUD e chegada no Tapete de verdade.

**Decisões técnicas da Etapa 6:**
- O voo do tapete é feito à mão (sem Arcade Physics): aceleração para cima ao segurar, para baixo ao soltar, velocidade máxima nos dois sentidos e aceleração 1,8× ao inverter, para a resposta parecer imediata sem tranco. Sobe até 165 px/s, desce até 140 px/s (`TAPETE` em `config.js`).
- A câmera anda sozinha (96 px/s); o tapete fica sempre no x 120 da tela. A duração sai do tamanho do mapa: 8 trechos de 30 colunas = 3840 px = 40 s.
- Mapa do céu em `src/levels/tapete.js`, com legenda própria: `s` sapatilha, `B` pássaro, `Q` pipa, `f` topo de poste (dois `f` na mesma linha ganham um fio). Os trechos têm 30 colunas e são emendados.
- No limite de baixo o tapete só desliza sobre os telhados, sem dano. Batida: 1,2 s piscando, perde até 2 sapatilhas (caem do tapete), o pássaro foge; postes, fios e pipas continuam no lugar.
- Arte original em `ferramentas/arte/gerar_tapete.py` → `src/art/tapete.js`: tapete ondulando (3 quadros) com a estampa dos quadrados concêntricos do logo (rosa, amarelo, verde, roxo sobre lilás), Aladdin provisório sentado, **Tia Paula provisória** (coque castanho, vestido roxo; aparência A DEFINIR), sabiá-laranjeira, pipa nas cores da escola, sapatilha de ponta.
- Fachada do teatro, cidade ao fundo (com uma torre de igreja genérica) e telhados são desenhados em código e **genéricos**: refazer quando chegarem as fotos do Teatro do Colégio G9.
- O sol desce durante a fase (entardecer). Parallax: morros 0,15, cidade 0,35, telhados 1.
- `?fase=tapete` ou `?fase=final` no link abre a fase direto (útil na prévia do Netlify). Sem o parâmetro abre o Título (desde a Etapa 7).
- A tela Final provisória desta etapa foi trocada pela versão completa da Etapa 7.
- O contador de sapatilhas do tapete usa o `registry` (`sapatilhas`), o mesmo nome do HUD do PR 7.
- (Etapa 4) JOGAR DE NOVO do Final agora volta à Fase 1.

**Decisões técnicas da Etapa 9 (som):**
- Tudo em código, sem arquivo de áudio: efeitos com o ZzFX (só o gerador `zzfxG`, em `src/audio/zzfx.js`, MIT, registrado no `CREDITS.md`) e músicas tocadas por um tocador próprio (`src/audio/musica.js`). Peso extra no build: ~10 KB.
- **Um AudioContext só** (`src/audio/som.js`), com volume geral. O Phaser roda com `audio: { noAudio: true }`, para não criar um segundo contexto que nunca tocaria (o iPhone limita contextos).
- **Desbloqueio revisado (Etapa 1):** o contexto só é criado dentro de um gesto (nada de aviso no console antes do toque). Os ouvintes de gesto (`touchend`, `pointerup`, `click`, `keydown`, `pointerdown`) ficam ligados o tempo todo: no iPhone o primeiro evento pode não contar como gesto, e o iOS também interrompe o áudio em ligações e troca de app. A cada toque, se o som não está rodando, tenta de novo (resume + som vazio).
- Efeitos e música podem ser agendados enquanto o contexto ainda está "acordando" (o `resume()` é assíncrono): o som do botão JOGAR, que é o mesmo toque que libera o áudio, toca.
- Pausa (aba sem foco, celular em pé) suspende o contexto: música e efeitos param juntos e voltam no toque que tira a pausa.
- Mudo: volume geral a zero e contexto suspenso (economiza bateria). A escolha fica no `localStorage` (`aladdin-som-mudo`). Tecla **M** no computador. Os botões de som se redesenham sozinhos (`quandoMudarMudo`).
- **Como usar nas cenas novas:** `tocarEfeito('nome')` (`src/audio/efeitos.js`; prontos para as próximas etapas: `blip` para cada caixa ou letra de diálogo, `acertoChefe`, `projetil`, `botao`), `tocarMusica('espaco' | 'chefe' | 'tapete' | 'final' | 'titulo')` no `create()` da cena e `tocarVinheta('ingresso' | 'vitoria' | 'checkpoint')`. Pedir uma música antes do 1º toque é seguro: ela começa quando o som ligar. A vinheta abaixa a música enquanto toca.
- Partituras em texto (`src/audio/musicas.js`): uma colcheia por ficha, `-` segura, `.` é silêncio, bateria `k s h`. Melodias compostas para o jogo, curtas (4 a 8 compassos), em tons maiores (Lá menor só no chefe), onda quadrada filtrada + baixo em triângulo.
- Ligados até agora: Fase 1 (música do título na tela JOGAR, depois a de Itajubá), `EmBreve` e `Final` (música de festa), Tapete (música, sapatilha, batida = `dano`, chegada = vinheta de vitória). Espaço e Chefe provisório ligados na Etapa 4; falta a luta do Chefe (Etapa 5) e Título/Intro (Etapa 7).
- Volumes em `config.js` (`SOM`): música (0,25) mais baixa que os efeitos (0,7). Pico medido no Chromium: ~0,3 para cada música.
- Teste no Chromium com `--autoplay-policy=user-gesture-required` (igual ao celular): nenhum contexto antes do toque; contexto `running` depois do toque em JOGAR; música agendando; efeitos de pulo, maçã, pisão e coleta tocando; pausa suspende e o toque retoma; mudo lembrado depois de recarregar; nenhum erro no console. Não dá para testar o iPhone de verdade daqui: fica para o teste final do Pedro.

**Decisões técnicas da Etapa 7:**
- Feita em paralelo com as Etapas 3, 4, 5, 6 e 9 e juntada depois. Fluxo: Título → Intro → Itajubá → Espaço → Chefe → Tapete → Final (`src/fluxo.js` guarda a primeira fase, o Final e a lista de fases que a pausa conhece). Saíram a tela "JOGAR" provisória da Itajubá, o Final provisório e a tela cheia automática da Itajubá, do Chefe e do Tapete.
- Som: os botões usam `tocarEfeito('botao')`; o Título e a Intro tocam a música `titulo`; o Final toca `final` e a vinheta `vitoria` quando aparece o cartão.
- Intro e Final usam a caixa de diálogo em HTML da Etapa 4 (`ui/Dialogo.js`), que fica nítida no celular. A minha versão em canvas foi descartada.
- `abrirPausa()` traz a Pausa para o topo (`bringToTop`), porque o Chefe traz o HUD para o topo.
- O botão de pausa do HUD (e o novo botão do Tapete) e as teclas Esc/P abrem o menu de pausa com `abrirPausa()` (`src/fluxo.js`), que pausa a fase e o HUD juntos. `pausarAgora()` saiu do `PausaFoco.js`.
- Menus em Phaser, com `ui/Botao.js` (ação no `pointerup`, o único momento em que o navegador aceita abrir link, compartilhar e tela cheia). O cartão do evento (`ui/CartaoEvento.js`) é o mesmo no Sobre (Título e Pausa) e no Final; tudo lê de `src/data/`.
- Pausa e Sobre são cenas sobrepostas: quem chama se pausa (`scene.pause`) e abre a outra por cima; VOLTAR/CONTINUAR retomam. Esc ou P abrem a pausa na fase. O aviso HTML "Pausado" continua só para perda de foco.
- COMPARTILHAR usa `navigator.share` com o texto e o link da página aberta (prévias do Netlify compartilham a si mesmas). Sem suporte, copia texto + link e o botão mostra "LINK COPIADO!" por 2 s. Links abrem com `window.open` e, se um bloqueador impedir, na mesma aba.
- JOGAR DE NOVO vai direto para a primeira fase (quem joga de novo já viu a intro) e zera as sapatilhas.
- Tia Paula no Final, de pé com microfone, usa o **mesmo design provisório** do Tapete (coque castanho, vestido roxo, faixa amarela), desenhado com `Graphics`. A aparência real está A DEFINIR (seção 8): trocar pelo sprite na Etapa 8.
- Sem `logo.png`, Título e Final mostram o nome da escola em texto. Ao colocar o arquivo, mudar `TEM_LOGO` para `true` em `src/art/index.js` (evita pedido 404).
- `og-image.png` (1200×630, 81 KB) e ícones (favicon 32, apple-touch 180, manifest 192/512) são gerados por `ferramentas/og/gerar.mjs` com a arte do próprio jogo (céu, morros, tiles, Aladdin provisório, quadrados do logo). Rodar de novo quando a arte mudar. As meta tags `og:image` e `og:url` usam o endereço de produção, porque o WhatsApp exige endereço completo.
- `?fase=` no link agora aceita `titulo`, `intro`, `itajuba`, `tapete` e `final`; sem o parâmetro, o jogo começa no Título.
- Teste automatizado (Playwright): jogada completa do Título ao Final, passando por Sobre, Intro, Itajubá (pausa, som, sobre, continuar), Espaço, Chefe, Tapete inteiro (com pausa) e Final (compartilhar, ingressos, Instagram, jogar de novo, pular para o final), sem erros no console.

**Ajustes pedidos pelo Pedro depois de jogar (01/11/2026):**
- Intro: botão **PRÓXIMO** (rosa) ao lado de PULAR; na última caixa vira **COMEÇAR**. Tocar em qualquer lugar continua avançando; `Dialogo.avancar()` ignora a 2ª chamada do mesmo toque (botão do canvas + toque na tela).
- Tutorial no começo da Fase 1 (`ui/Tutorial.js`, textos em `TEXTOS.tutorial`): setas pulando em cima de ◀ ▶, PULAR e MAÇÃ (no computador, o texto mostra as teclas), um passo por vez, cada um some quando a pessoa faz a ação (ou depois de 9 s). Enquanto explica os botões, as capivaras da tela esperam paradas. Depois, quando a primeira capivara acordada se aproxima: "Pule em cima da capivara para ela dormir!" com a seta em cima dela. Só aparece na primeira partida (`tutorialVisto` no registry).
- Jasmine: "Olha só a minha pirueta!".

**Decisões técnicas da Etapa 8.0 (guia e escala):**
- Medidas tiradas das capturas reduzidas à tela nativa do SNES (256×224): herói com ≈ 54 a 56 px = 24 a 25% da tela
  (a leitura antiga de 28% contava o chapéu). Alvo mantido em 56 a 60 px (21 a 22%) porque a nossa tela é 16:9 e
  precisa mostrar mais caminho. Atingido: 58 px. Detalhes, paleta de cenário e regras de luz e contorno no guia.
- **Renderizador de volumes** (`ferramentas/arte/modelo.py`): cada parte do corpo é uma cápsula ou elipse com material;
  a luz (de cima e da frente) escolhe 1 de 4 tons; parte de trás 1 tom mais escura; linha de separação onde uma parte
  passa na frente da outra; contorno colorido do material vizinho. Rosto, brilhos e dobras são pintados à mão por cima.
  Foi escolhido no lugar do `pixel.py` da 8A (formas chapadas de 2 tons) porque mantém a qualidade igual em 23 quadros.
  A 8A deve usar o mesmo renderizador.
- **Aladdin provisório** (sem fotos do figurino): cabelo preto cacheado, faixa rosa amarrada na cabeça com pontas ao
  vento, túnica verde curta sem mangas com gola em V, faixa rosa na cintura, calça areia justa no tornozelo com barra
  de couro, sandálias, argola e bracelete dourados. Nada do design da Disney (sem colete, sem fez, sem calça bufante).
- Animações ficam junto da arte (`ANIMACOES` em `src/art/jogador.js`); o `Preload` só lê. A maçã sai 60 ms depois do
  toque (quadro de antecipação); o dano interrompe o arremesso.
- Física: caixa 18×46 (offset 15,17), pulo 360 → 380 (72 → 80 px), câmera com zona morta de 56 px de altura, maçã sai
  26 px acima do pé e 14 px à frente. Os mapas não têm teto baixo (conferido por script: nenhum vão menor que 3 tiles);
  o muro de 6 tiles ainda exige o toldo. Uma capivara da Fase 1 passou da coluna 152 para a 155: com o herói maior, o
  recuo do dano o jogava no buraco logo atrás.
- Tapete: o Aladdin sentado é o quadro `sentado` do sprite do jogador, dentro de um container com o tapete (a textura
  `voo` agora só tem o tapete e a Tia Paula) e balança com a onda (`ONDA_ALADDIN`). `yMin` 34 → 44 e caixa 44×34 para
  a cabeça dele caber na tela. A Tia Paula do tapete ficou menor que ele até a 8A.
- `og-image.png` e ícones regenerados com o herói novo (`ferramentas/og/gerar.mjs` ajustado para 48×64).
- O robô da Etapa 10 (`robo.mjs`) não conseguia apertar os controles (troca o protótipo de `Entrada`, e o Vite pode
  servir outra cópia do módulo). O `jogar.mjs` troca o método da **instância** da cena ativa; pula paredes e buracos,
  joga maçã, recua para pegar o toldo, desvia no Chefe e no Tapete. Na mesma máquina, o robô fez a versão antiga em
  185 s e a nova em 157 s (antes de juntar o tutorial do `dev`) e 260 s (com o tutorial, que espera até 9 s por passo). O trecho "degrau → bloco estreito → buraco" (colunas 158 a 168) derruba quem pula
  segurando ▶ nas duas versões: é desenho da fase, para avaliar no polimento.

**Revisão das instruções de arte (01/11/2026):**
- Motivo: a arte ficou longe das referências enviadas pelo Pedro. Auditoria no Git:
  - `802af5e` (31/10): o Pedro subiu 5 capturas do Aladdin do SNES e a folha de capivaras do 14collective em `references/figurinos/`.
  - `57d5f8a` (01/11, 02:16): criada a seção 7.1, o índice e as notas por pasta. `5f92d81` (02:22): tudo removido a pedido do Pedro ("arte com mais liberdade"), antes de ser usado.
  - As decisões das Etapas 2, 3 e 4 fixaram "capturas = só clima" e cada etapa desenhou seus próprios personagens provisórios.
- Problemas encontrados: regra 3 lida como proibição de estilo; capturas na pasta errada (o README mandava capturas para `estilo/` e pedia para não subir "telas"); critério da Etapa 8 sem medida ("coerente com a paleta"); escala 32×48 em 480×270 deixava o herói com ≈ 15% da tela (≈ 28% nas capturas); "arte simples" escrito na seção 7; personagens duplicados (Jafar em `chefe.js` e `jafar.js`; Tia Paula no Tapete, no Final com `Graphics` e em `paula.js`; NPCs em `espaco.js` e na 8A).
- O que foi feito: nova regra 3 (permitido × proibido × teste prático), seção 7.1 recriada e corrigida, escala 48×64 e "fonte única" na seção 7, seção 8 e critérios das Etapas 8 e 10 revistos, autonomia até a entrega final na seção 3. Capturas movidas com `git mv` para `references/estilo/` e a folha de capivaras para `references/licenciados/`. `references/README.md`, índice e notas de cada pasta recriados. As decisões antigas ficaram riscadas, não apagadas.

**Riscos anotados:**
- A Fase 1 tem ~4.900 px: correndo direto dá ~35 s; com capivaras, toldos e coleta, a estimativa é de 60 a 80 s. Medir no celular e ajustar no polimento (Etapa 10).
- ~~Texto serrilhado no diálogo~~: resolvido na Etapa 4 com a caixa em HTML. Os outros textos do Phaser (HUD, faixas, avisos) continuam na resolução do jogo; se incomodarem no celular, dá para levá-los para HTML do mesmo jeito.
- A Fase 2 tem 13 caixas de diálogo. Com leitura de ~2,5 s por caixa, a fase fica perto de 45 s (o limite de cima). Se ficar longa no teste com crianças, cortar falas em `textos.js`.
- Som no iPhone: só testado em Chromium. Se não tocar depois do 1º toque no Safari, conferir primeiro a chave de silencioso (decisão da Etapa 1: o jogo respeita a chave).
- O Phaser completo pesa ~1,2 MB minificado (~330 KB comprimido na transferência). Cabe no orçamento; se apertar, trocar pelo build só com Arcade Physics.
