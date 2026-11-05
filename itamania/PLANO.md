# Entrega atual: missão urbana da praça até a igreja

Proposta A e percurso visual aprovados pelo Pedro. Implementação e publicação somente em `dev-itamania`.
Escopo: cena lateral, assets exclusivos, coleta/pontos, desvio opcional, checkpoints e recompensas finitas.
Não alterar controles, colisões ou conversas da praça top-down. Sem agentes ou janelas adicionais.
Detalhes e limitações da validação em `MISSOES.md` e `STATUS.md`.

---

# Entrega atual: encontros e missões Sunny Land

Pedido do Pedro (04/11/2026): converter o desafio da praça para o estilo Sunny Land e validar o ciclo de encontros
com capivara. Implementação e critérios em [MISSOES.md](MISSOES.md). Branch local `missao-praca-sunnyland`.
Montagem foi local. Depois da configuração confirmada pelo Pedro, publicada somente em `dev-itamania`,
contexto `branch-deploy`, sem alterar produção. Ver MISSOES.md para o destino correto das próximas entregas.

---

# PLANO · ITAMANIA etapa 2 (madrugada de 04 para 05/11/2026)

Pedido do Pedro (04/11/2026, com a imagem `referencias/herois-grandes.png`):
1. Incluir os personagens grandes (16x32, "depois do café").
2. Título com o ITAMANIA em letras de cores diferentes, como no mapa.
3. Mapa: navegação só para cima e para baixo, sem passeio automático rápido, com mais densidade de pixels.
4. Trem com poucos vagões.
5. Desenvolver até a fase 4.
6. Revisar os outros personagens (NPCs) para combinar com os heróis atuais.
7. Publicar no Netlify só no final, em dev.

## Decisões

- **Escala.** Desenho 16x24 (criança) e 16x32 (grande) ampliados 2x no jogo: criança com 48 px, grande com 64 px
  (24% da tela, a mesma escala dos prédios, que foram feitos para um herói de ~58 px). O café com leite
  (fase 4 em diante) faz crescer de 48 para 64 px e aguenta um toque a mais; levar um toque volta a criança.
  Os NPCs adultos usam o corpo de 16x32 (mesma altura do herói grande), então a criança fica na proporção certa de
  criança no meio dos adultos.
- **Mapa em alta densidade.** O mapa vira uma camada HTML por cima do jogo, com a imagem original (1080 x 1920)
  ajustada à largura da tela. Assim aparece com a resolução da tela do celular, não com os 480 px do jogo.
  Arrastar (ou rolar, ou setas para cima e para baixo) move o mapa; tocar numa moeda escolhe a fase; painel com
  JOGAR. Sem passeio automático.
- **Trem:** locomotiva e 1 vagão.
- **Netlify:** o site `itamania` publica a branch `claude/busy-hamilton-cxbmdi`. O trabalho desta etapa fica na
  branch `claude/itamania-etapa2` e só entra na `claude/busy-hamilton-cxbmdi` no fim, testado. Isso evita gastar
  créditos com deploys intermediários. A `main` não é tocada.

## Janelas (sessões em paralelo, cada uma na sua branch e nos seus arquivos)

| Janela | Branch | Arquivos | Entrega |
|---|---|---|---|
| Esta (coordenação) | `claude/itamania-etapa2` | herói, fases, `Fase.js`, `Preload.js`, níveis, testes | herói grande, café com leite, fases 2 a 4, trem, integração |
| NPCs | `claude/itamania-npcs` | `ferramentas/arte/gerar_npcs16.py`, `public/assets/sprites/npc-*.png` | 8 NPCs no estilo 16x32 dos heróis |
| Mapa e título | `claude/itamania-mapa` | `src/scenes/Mapa.js`, `src/scenes/Titulo.js`, `src/ui/mapaHtml.js`, `public/assets/mapa-hd.png` | mapa HTML em alta densidade e título colorido |

## Ordem

1. Herói grande e café com leite (esta janela).
2. Trem com 1 vagão; fases 2, 3 e 4 ligadas e revisadas; robô jogando 1 a 4.
3. Juntar as branches das janelas, ajustar `art/index.js` para os NPCs novos (quadros de 32x64).
4. Teste final no Chromium (sem erros no console, capturas conferidas, robô do título até o fim da fase 4).
5. Merge na `claude/busy-hamilton-cxbmdi` (deploy de dev no Netlify) e relatório no `STATUS.md`.
