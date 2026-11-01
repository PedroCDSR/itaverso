# Geradores de arte

Scripts que **montam** as matrizes de `src/art/` a partir de partes (cabeça, túnica, braços, pernas) e poses.
O jogo usa só as matrizes; os scripts servem para redesenhar rápido (por exemplo, quando chegarem as fotos dos
figurinos). Também dá para editar as matrizes à mão, sem rodar nada.

Precisa de Python 3. O Pillow é opcional: serve só para gerar a imagem de prévia.

```bash
python3 ferramentas/arte/gerar_jogador.py . /tmp
```

```bash
python3 ferramentas/arte/gerar_tiles.py . /tmp
```

Rodar um gerador **sobrescreve** a matriz correspondente em `src/art/`: edições feitas à mão nela se perdem.

A arte da Fase 3 (Jafar, projétil, gaiola e Tia Paula) vem de outro gerador. A Tia Paula tem aparência A DEFINIR:
o desenho é neutro e fica num sprite separado (`tiaPaula`), para trocar fácil.

```bash
python3 ferramentas/arte/gerar_chefe.py . /tmp
```
