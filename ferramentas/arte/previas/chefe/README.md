# Prévia · Tia Paula visível na gaiola (Fase 3, Resgate)

Pedido do Pedro (01/11/2026): na luta contra o Jafar é preciso **ver a Tia Paula dentro da gaiola**.
Só prévia: `src/` não mudou. Gerado por `python3 ferramentas/arte/previa_chefe.py`.

| Arquivo | O que é |
|---|---|
| `gaiola-atual-x-nova.png` | gaiola de hoje × nova fechada (com a Tia Paula) × nova aberta, 5× |
| `chefe-telas.png` | 2 telas do jogo (2×): durante a luta e na vitória, com a faixa do HUD e os botões de toque marcados |

Por que hoje não dá para ver: a gaiola (40×56) tem grades grossas a cada 3 px, e a Tia Paula provisória fica atrás
delas, contra o céu escuro.

Proposta:
- gaiola maior (64×96) para a Tia Paula nova (57 px) caber inteira, de pé;
- grades em 2 camadas: as de trás finas e escuras; na frente, só 6 grades finas, com um vão de 23 px no meio
  (o rosto e o corpo dela ficam livres; o anel do meio não cruza o rosto);
- brilho lilás em faixas atrás dela (o feitiço do Jafar), que a destaca no céu da noite;
- pose "socorro": mãos agarradas na grade, boca aberta, balão "Socorro!";
- continua pendurada no alto à direita, abaixo do HUD e longe dos botões PULAR e MAÇÃ;
- vitória: a portinha abre para o lado, o brilho some e ela desce feliz.

Ajustes no jogo quando for implementar: `gBase` de 170 para ~126 (topo da gaiola em y 30), a Tia Paula vai para a
camada entre as grades (desenhar gaiola de trás → Tia Paula → gaiola da frente), e o tween de balanço move as 3 peças
juntas. A arena nova (noite, serra verde, chão de paralelepípedo, Jafar maior) também aparece nas telas.

**Hora do dia (Pedro, 01/11/2026):** a luta é **ao pôr do sol** (sol grande encostando na serra, céu lilás → rosa → laranja), para o voo seguinte acontecer no crepúsculo. Sequência do dia: Fase 1 fim de tarde → Espaço (interno) → Chefe pôr do sol → Tapete crepúsculo → Final à noite no teatro (19h).
