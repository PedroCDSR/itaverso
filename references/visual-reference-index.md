# Índice de referências visuais

Liga cada arte do jogo às referências que ela deve seguir (CLAUDE.md, seção 7.1). Atualize sempre que entrar uma
referência nova ou uma arte for implementada.

Situação: `provisório` (design ou qualidade ainda não final) · `em validação` · `validado` (prancha comparativa feita e
diferenças anotadas) · `aguardando referência` (qualidade final, mas o design depende de foto do Pedro).

Situação em 01/11/2026, depois da auditoria e da Etapa 8.0 (guia em `estilo/reference-notes.md`):

| Arte do jogo | Arquivo no jogo | Referências | Situação | Diferenças anotadas |
|---|---|---|---|---|
| Aladdin (jogador) | `src/art/jogador.js` (48×64, 23 quadros), gerado por `ferramentas/arte/gerar_jogador.py` + `modelo.py` | `estilo/` (qualidade e escala); `figurinos/` (a subir) | **provisório** (design) · **validado** (escala e acabamento, Etapa 8.0) | Atingido: 58 px = 21,5% da tela (alvo 21–22%), 4 tons por material + contorno colorido, luz de cima e da frente, corrida de 8 quadros, arremesso com antecipação. Fica: figurino inventado (sem fotos); herói 3 a 4 pontos percentuais menor que no SNES (tela 16:9 mostra mais caminho); idle com a mão na cintura lê um pouco "cheio" no peito. Pranchas: `ferramentas/arte/previas/8-0-*.png` |
| Aladdin sentado no tapete | quadros `sentado1..3` de `src/art/jogador.js`, posto por cima do tapete na cena `Tapete` | idem | **fonte única** desde a Etapa 8.0 (provisório como o jogador) | A Tia Paula do tapete ainda está na escala antiga (≈ 34 px sentada): parece menor que o Aladdin até ser refeita na 8A |
| Jasmine, Gênio, Sultão, Abu | `src/art/espaco.js` (`dev`) + `jasmine.js`, `genio.js`, `sultao.js`, `abu.js` (8A) | `estilo/`; `figurinos/` (a subir) | provisório, **duplicado** | proporção "cabeçuda", 2 tons, pouco detalhe |
| Bailarina (8A) | `bailarina.js` (8A) | `estilo/` | provisório | idem |
| Jafar | `src/art/chefe.js` (`dev`) + `jafar.js` (8A) | `estilo/`; `figurinos/` (a subir) | provisório, **duplicado** | duas versões diferentes |
| Tia Paula | `tapete.js`, `chefe.js`, `Graphics` no Final (`dev`) + `paula.js` (8A) | `pessoas/` (a subir) | provisório, **3 versões** | cabelo loiro (Pedro, 01/11); as versões atuais têm coque castanho: errado |
| Tia Claudia | `espaco.js` (`dev`) + `claudia.js` (8A) | `pessoas/` (a subir) | provisório, **duplicado** | só "óculos e cabelo preto" é dado real |
| Capivara | `src/art/objetos.js` (`dev`) + `capivara.js` (8A) | `licenciados/` (divulgação), `estilo/` | provisório | mais escura e menos fofa que a referência |
| Maçã, sapatilha, coração, fonte, bandeira | `src/art/objetos.js` | `estilo/` | provisório | poucos tons; fonte genérica |
| Rua, casas, chão (Itajubá) | `src/art/tiles.js`, casario em canvas no `Preload` | `estilo/`; `lugares/` (a subir) | provisório | paredes lisas, chão repetido, sem objetos nem primeiro plano |
| Barracas e toldos | `Graphics` na cena Itajubá | `estilo/` (`snes-mercado-toldos.jpg`) | provisório | toldos sem dobras e com 1 a 2 tons |
| Estúdio do Espaço | `Preload` (canvas) + `tiles-espaco` | `estilo/`; `lugares/` (a subir) | provisório | espelhos lisos, cena vazia |
| Arena do chefe | `src/levels/chefe.js` + `Graphics` | `estilo/` | provisório | reaproveita os morros; pouca textura |
| Céu e cidade do Tapete | código na cena Tapete | `estilo/` (`snes-tapete.jpg`, `snes-corda.jpg`) | provisório | prédios em bloco, sem textura |
| Fachada do Teatro do Colégio G9 | código na cena Tapete | `lugares/` (a subir) | aguardando referência | fachada genérica |
| Palco e cortinas (Final) | cena Final | `estilo/` | provisório | |
| Tapete mágico | `src/art/tapete.js` | `logo/` (a subir) | provisório | estampa segue a descrição do logo |
| HUD, menus, botões, diálogo | `scenes/HUD.js`, `ui/` | paleta da seção 7 | em validação | coerentes; revisar junto com a arte nova |
| Imagem de compartilhamento e ícones | `public/og-image.png`, ícones | arte do jogo | provisório | gerados com a arte provisória: regenerar no fim |
| Cenários da Etapa 8B | branch `etapa-8b-cenarios` | `estilo/` | em validação | trabalho incompleto, ainda não integrado |
