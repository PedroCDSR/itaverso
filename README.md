# Jogo do Aladdin · Paula De Marco Espaço de Artes

Jogo de plataforma curto, para celular, que apresenta o espetáculo **Aladdin** do Paula De Marco Espaço de Artes
(sexta-feira, 20/11/2026, Teatro do Colégio G9, Itajubá/MG). A pessoa joga 2 a 3 minutos e termina no botão de
ingressos. Toda a arte é original.

O plano completo, as regras e o status estão em [CLAUDE.md](CLAUDE.md).

## Rodar no computador

Precisa do Node 22.

```bash
npm install
```

```bash
npm run dev
```

O `--host` já está no script: no celular, na mesma rede Wi-Fi, abra o endereço "Network" que aparece no terminal.

## Gerar o site

```bash
npm run build
```

O resultado vai para `dist/`. Para conferir o build:

```bash
npm run preview
```

## Onde mexer

| O quê | Arquivo |
|---|---|
| Data, local, WhatsApp, Instagram | `src/data/evento.js` |
| Todos os textos e diálogos | `src/data/textos.js` |
| Velocidade, pulo, gravidade, vida do chefe | `src/config.js` |
| Fases (mapas em texto) | `src/levels/` |
| Sprites (matriz de texto ou PNG) | `src/art/` e `public/assets/sprites/` |
| Ordem das cenas (fases) | `src/fluxo.js` |
| Imagem de compartilhamento e ícones | `node ferramentas/og/gerar.mjs` (gera `public/og-image.png` e os ícones) |

## Branches e Netlify

- `main`: produção. Só recebe merge no lançamento (cada deploy de produção gasta créditos do plano gratuito).
- `dev`: integração. Cada etapa abre um PR `etapa-N-nome` → `dev`.
