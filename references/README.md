# Referências visuais

Fotos e imagens que servem de **base para desenhar** a arte original do jogo. Nada desta pasta vai para o site
(o build só usa `public/` e `src/`), então o tamanho dos arquivos aqui não pesa no Netlify.

Antes de qualquer arte, siga o fluxo da seção 7.1 do `CLAUDE.md`: imagens, `reference-notes.md` de cada pasta e o índice `visual-reference-index.md`.

| Pasta | O que colocar | Usado para |
|---|---|---|
| `figurinos/` | Fotos dos figurinos do espetáculo (Aladdin, Jasmine, Gênio, Abu, Jafar e demais), de frente e de costas | Desenhar os personagens (CLAUDE.md, seção 8) |
| `pessoas/` | Foto ou descrição da Tia Paula e da Tia Claudia (cabelo, óculos, roupa típica) | Desenhar as duas personagens |
| `lugares/` | Fonte de Itajubá, praça, ruas, morros, fachada do Teatro do Colégio G9, estúdio do Espaço | Cenários das fases |
| `logo/` | Logo da escola no arquivo original (de preferência PNG ou SVG em alta resolução) | Conferir a paleta e a estampa do tapete. A versão final usada no jogo vai em `public/assets/logo.png` |
| `estilo/` | Exemplos de jogos ou ilustrações cujo *clima* você gosta (cores, traço, iluminação) | Só inspiração geral |

## Como subir pelo GitHub (navegador ou celular)

1. Abra a pasta desejada no GitHub (por exemplo `references/figurinos`).
2. Toque em **Add file → Upload files** e escolha as fotos.
3. Escreva uma frase curta no campo de descrição (ex.: "Figurinos do Aladdin e da Jasmine") e confirme.

Dica: dê nomes que digam o que é a foto, por exemplo `jasmine-frente.jpg`, `fonte-praca-1.jpg`.

## Cuidados

- **Rosto de alunos:** não suba fotos em que dê para reconhecer crianças. Para figurinos, prefira a roupa no cabide
  ou fotos sem o rosto. O jogo não retrata alunos (CLAUDE.md, seção 8).
- **Tia Paula e Tia Claudia:** só suba fotos com o OK delas.
- **Direito autoral:** nada daqui é copiado para o jogo; a arte é sempre redesenhada. Mesmo assim, não suba sprites,
  telas ou arquivos extraídos do jogo original nem imagens do filme. ROMs (`.sfc`, `.smc`, `.zip`) são bloqueadas
  pelo `.gitignore` e nunca entram no repositório.
