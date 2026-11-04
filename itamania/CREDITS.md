# Créditos e licenças

Tudo que vem de fora do projeto fica registrado aqui (autoria, licença e onde está).

| Item | Autor | Licença | Arquivo |
|---|---|---|---|
| Phaser 4 | Phaser Studio | MIT | dependência npm |
| Vite | Evan You e colaboradores | MIT | dependência de desenvolvimento |
| Fonte "Press Start 2P" | CodeMan38 | SIL Open Font License 1.1 | `public/assets/fonts/PressStart2P.woff2` (licença em `OFL-PressStart2P.txt`) |
| Fonte "Patrick Hand" | Patrick Wagesreiter | SIL Open Font License 1.1 | `public/assets/fonts/PatrickHand.woff2` (licença em `OFL-PatrickHand.txt`) |
| ZzFX (gerador de efeitos sonoros, função `zzfxG`) | Frank Force ([KilledByAPixel/ZzFX](https://github.com/KilledByAPixel/ZzFX)) | MIT | adaptado em `src/audio/zzfx.js` |
| Modern Exteriors 16x16 (chão, prédios, árvores, móveis e personagens da praça) | LimeZu ([limezu.itch.io](https://limezu.itch.io/)) | Licença paga, comprada pelo Pedro em 04/11/2026: pode editar e usar em projetos comerciais e abertos; não pode revender nem distribuir o pacote; **crédito obrigatório** (na tela de título) | recortes em `public/assets/limezu/` (licença em `referencias/licenciados/modern-exteriors-licenca.pdf`; o pacote completo fica fora do Git) |
| Ninja Adventure Asset Pack (balões "!" e "...") | Pixel-boy e AAA ([pixel-boy.itch.io](https://pixel-boy.itch.io/ninja-adventure-asset-pack)) | CC0 1.0 (crédito opcional) | `public/assets/ninja/` (licença em `referencias/licenciados/ninja-adventure/`) |
| Nomes e logos de comércios de Itajubá (Casa Joka, Cesar Burg, Café do Vadinho), redesenhados em pixel | os próprios comércios | Uso autorizado pelos donos, informado pelo Pedro em 04/11/2026 | `public/assets/cenario/` |

As fontes vêm do repositório oficial `google/fonts` e foram convertidas para woff2, só com o alfabeto latino
(Latin-1), para ficarem leves. A OFL permite essa conversão.

Na praça, prédios, árvores e palmeiras são peças do Modern Exteriors montadas e repintadas por nós
(`ferramentas/arte/pecas_praca.py`); concha acústica, busto de perfil, letreiros e tronco das palmeiras-imperiais são
desenho próprio.

Heróis (Geraldo e Helena) e mapa-múndi: desenhos do Pedro. Na praça vista de cima, os heróis e os moradores ainda
são personagens do Modern Exteriors (provisório, até existir o desenho do Pedro visto de cima). Demais personagens, cenários, efeitos sonoros e músicas
(gerados em código): criação original deste projeto. Nenhum arquivo de arte, som ou música de outro jogo é usado.

Licença do ZzFX:

> MIT License. Copyright (c) 2019 Frank Force.
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
> documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
> rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
> persons to whom the Software is furnished to do so, subject to the following conditions:
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
> Software.
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
> WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
> COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
> OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
