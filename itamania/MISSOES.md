# Missão urbana da praça: da praça à igreja

Direção e mapa visual aprovados pelo Pedro. Destino final: largo diante da igreja.
Publicação autorizada em desenvolvimento: branch `dev-itamania`, endereço
https://dev-itamania--itamania.netlify.app. Não alterar produção (`claude/busy-hamilton-cxbmdi`) ou `main`.

## Percurso lateral

Praça plana: Club Itajubense, fonte, concha acústica e Café do Vadinho. Depois do café começa a subida suave,
seguindo sobrados, comércio de tijolinhos, casarão verde, casarão azul e prédio branco de molduras azuis
com embasamento de pedra. A igreja com torre central e relógio encerra o percurso.

O chão é contínuo. Rota baixa com bancos, canteiros e pequenos degraus. Desvio opcional alcançado por
escadinha e mureta, com toldo elástico, marquise e estrela. Apoios ligados à arquitetura. Cair desse desvio
leva à calçada. Dois checkpoints: depois do Vadinho e antes do largo final. Três fôlegos; dano volta ao
checkpoint, sem fôlego retorna ao ponto seguro da exploração. Não se apagam descobertas nem saldo anterior.

A câmera acompanha a subida e o salto. Correr/pular e pausa usam os controles existentes da missão.
Controles, colisões, conversas e mapa da praça top-down não foram alterados.

## Pontos e itacoins

- 40 fichas, cada uma com valor de 10 pontos. Estrela opcional: 50 pontos.
- Oito grupos de cinco fichas. Completar um grupo rende +50, sem relógio ou ordem obrigatória.
- Máximo: 850 pontos. Fichas e bônus só pontuam uma vez por tentativa e não voltam no checkpoint.
- Dano não apaga pontos; derrotas não salvam recorde nem medalhas.
- Recorde e medalhas de 200, 500 e 750 pontos são persistentes, concedidos ao concluir.
- Primeira conclusão: 5 itacoins. Cada medalha inédita: 1, 2 e 2 itacoins, respectivamente.
- Teto de 10 itacoins para o circuito, compartilhado entre travessia e fuga. Repetições sem novas conquistas: zero.
- Progresso legado com qualquer variante concluída considera a primeira recompensa já recebida.
- Sessão por token é consumida junto do resultado e pagamento. Recarregar resultado não duplica recompensa.
- Interromper/abandonar não paga e recupera a exploração. Dados continuam locais, sem servidor.

## Entrada e retorno preservados

Encontro especial: Gambá Travesso à direita da praça, interação FALAR/espaço. Encontro comum continua restrito
à rua lateral: 160 px de distância mínima, proteção de 30 s e chance de 25% a cada 48 px. A variante de fuga
usa o circuito urbano e mantém o gambá perseguidor. Vitória retorna às coordenadas e direção do encontro;
derrota volta ao ponto seguro. Os IDs existentes foram mantidos para preservar saves.
Os 14 nomes do mapa permanecem intactos; somente a praça tem micromundo implementado neste recorte.

## Arquivos e validação

- `src/data/missaoUrbana.js`: terreno, apoios, fachadas e coletas.
- `src/scenes/Missao.js`, `src/ui/cenarioMissaoUrbana.js`: física e apresentação exclusivas da missão.
- `src/systems/pontosMissao.js`: pontuação sem duplicação.
- `src/systems/encontros.js`: conclusão, economia finita e retorno persistente.
- `ferramentas/arte/gerar_missao_urbana.py`: assets exclusivos a partir dos recortes existentes.
- Licenças e créditos: `CREDITS.md`. A imagem conceitual orienta o mapa, não é usada como cenário achatado.

Dentro de `itamania/`:

```bash
node ferramentas/teste/encontros.test.mjs
node ferramentas/teste/missao-urbana.test.mjs
python ferramentas/arte/gerar_missao_urbana.py
npm run build
```

Com Playwright externo e Chromium disponíveis, `node ferramentas/teste/missao-urbana.mjs` abre um servidor
Vite local e prepara capturas e testes do percurso/desvio. `CHROMIUM_PATH` permite selecionar o executável.
Os robôs anteriores `missao.mjs` e `missao-toque.mjs` usam um Vite já iniciado e exercitam o ciclo de encontro.
Atalho só no Vite: `?missao=urbana` ou `?missao=urbana&fuga=1`. No build publicado a entrada segue pelo encontro.

Nesta sessão, build e 15 testes de regras passaram. Validação no navegador não concluída: o sandbox bloqueou
a abertura do Chromium e do servidor local. Testes em Safari/iPhone e Android reais continuam pendentes.
