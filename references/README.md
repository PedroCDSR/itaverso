# Referências visuais

Biblioteca de referências do jogo. É aqui que a arte começa e é contra isto que ela é validada (CLAUDE.md, seção 7.1).
Nada desta pasta vai para o site (o build só usa `public/` e `src/`), então o tamanho dos arquivos não pesa no Netlify.

**Antes de qualquer arte:** olhar as imagens da pasta certa, ler o `reference-notes.md` dela e conferir o
[`visual-reference-index.md`](visual-reference-index.md).

| Pasta | O que colocar | Para que serve |
|---|---|---|
| `figurinos/` | Fotos dos figurinos **do espetáculo da escola** (Aladdin, Jasmine, Gênio, Abu, Jafar e demais), de frente e de costas, sem rosto de alunos | Design dos personagens (seção 8) |
| `pessoas/` | Foto ou descrição da Tia Paula e da Tia Claudia, só com o OK delas | Traços que identificam as duas |
| `lugares/` | Fonte de Itajubá, praça, ruas, morros, fachada do Teatro do Colégio G9, estúdio do Espaço | Cenários das fases |
| `logo/` | Logo da escola no arquivo original (PNG ou SVG em alta resolução) | Paleta e estampa do tapete. A versão usada no jogo vai em `public/assets/logo.png` |
| `estilo/` | Capturas de jogos cuja linguagem visual é o alvo (hoje: Aladdin do SNES) | **Padrão de qualidade**: escala, tons, contorno, luz, densidade de detalhe, animação. Nunca o design dos personagens (regra 3) |
| `licenciados/` | Assets de terceiros com licença de uso (ou a divulgação deles, enquanto não forem comprados) | Uso direto conforme a licença, sempre com `CREDITS.md` |

## Como subir pelo GitHub (navegador ou celular)

1. Abra a pasta desejada no GitHub (por exemplo `references/figurinos`).
2. Toque em **Add file → Upload files** e escolha as fotos.
3. Escreva uma frase curta no campo de descrição (ex.: "Figurinos do Aladdin e da Jasmine") e confirme.

Dica: dê nomes que digam o que é a foto, por exemplo `jasmine-frente.jpg`, `fonte-praca-1.jpg`.
Capturas de jogos vão em `estilo/`, não em `figurinos/`.

## Cuidados

- **Rosto de alunos:** não suba fotos em que dê para reconhecer crianças. Para figurinos, prefira a roupa no cabide
  ou fotos sem o rosto. O jogo não retrata alunos (CLAUDE.md, seção 8).
- **Tia Paula e Tia Claudia:** só suba fotos com o OK delas.
- **Direito autoral:** capturas de tela para estudo podem ficar em `estilo/`. Nunca suba sprites, tiles ou arquivos
  **extraídos** do jogo original nem arquivos do filme. Nada de `references/` vai para `public/` sem licença e
  registro em `CREDITS.md`. ROMs (`.sfc`, `.smc`, `.zip`) são bloqueadas pelo `.gitignore`.
