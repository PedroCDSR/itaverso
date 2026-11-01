# Geradores de arte

Scripts que **montam** as matrizes de `src/art/` a partir de partes (cabeça, túnica, braços, pernas) e poses.
O jogo usa só as matrizes; os scripts servem para redesenhar rápido (por exemplo, quando chegarem as fotos dos
figurinos). Também dá para editar as matrizes à mão, sem rodar nada.

**Personagens (desde a Etapa 8.0):** `modelo.py` é o renderizador comum (volumes com luz em 4 tons, linha de
separação e contorno colorido; ver `references/estilo/reference-notes.md`) e `pixel.py` tem a saída em JS e a prévia.
`gerar_jogador.py` é o exemplo completo: esqueleto, poses e animações do Aladdin em quadros de 48×64.

Precisa de Python 3. O Pillow é opcional: serve só para gerar a imagem de prévia.

```bash
python3 ferramentas/arte/gerar_jogador.py . /tmp
```

```bash
python3 ferramentas/arte/gerar_tiles.py . /tmp
```

```bash
python3 ferramentas/arte/gerar_tapete.py . /tmp
```

```bash
python3 ferramentas/arte/gerar_objetos.py . /tmp
```

```bash
python3 ferramentas/arte/gerar_espaco.py . /tmp
```

Os mapas das fases têm geradores próprios:

```bash
python3 ferramentas/mapas/gerar_itajuba.py > src/levels/itajuba.js
```

```bash
python3 ferramentas/mapas/gerar_espaco.py > src/levels/espaco.js
```

Rodar um gerador **sobrescreve** a matriz correspondente em `src/art/`: edições feitas à mão nela se perdem.

A arte da Fase 3 (Jafar, projétil, gaiola e Tia Paula) vem de outro gerador. A Tia Paula tem aparência A DEFINIR:
o desenho é neutro e fica num sprite separado (`tiaPaula`), para trocar fácil.

```bash
python3 ferramentas/arte/gerar_chefe.py . /tmp
```

## Prancha comparativa (obrigatória, CLAUDE.md seção 7.1)

Toda arte nova ou refeita termina com uma prancha em `ferramentas/arte/previas/`: a referência (de
`references/estilo/`, `figurinos/`, `pessoas/` ou `lugares/`) ao lado da nossa arte, **na mesma escala** (por exemplo,
as duas ampliadas para a mesma altura de tela). Nome sugerido: `comparar-<arte>.png`.

Depois de gerar, anote no `references/visual-reference-index.md` e no PR as diferenças de proporção, silhueta, cores,
composição, sombreamento e acabamento que ficaram, e o motivo.
