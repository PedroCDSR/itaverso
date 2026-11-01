# Prévia · Aladdin versão 2 ("linha B")

Pergunta do Pedro (01/11/2026): como deixar o herói o mais próximo possível do Aladdin do SNES sem ser plágio.
Resposta: copiar a **linguagem** (silhueta, proporção, animação, acabamento), nunca o **design** da Disney (regra 3).
Só prévia: `src/` não mudou. Gerado por `python3 ferramentas/arte/previa_aladdin_v2.py`.

| Arquivo | O que é |
|---|---|
| `aladdin-v1-x-v2.png` | silhueta de referência (cinza, só escala) × herói de hoje × versão 2, parado e correndo (6×) |
| `aladdin-rosto.png` | close do rosto (12×): hoje × versão 2, parado, piscando e correndo |
| `aladdin-v2-quadros.png` | os 23 quadros da versão 2 (4×) |
| `aladdin-v2-parado.gif`, `-corrida.gif`, `-pulo.gif`, `-arremesso.gif` | animações (4×) |

O que muda (mesmo esqueleto, luz, escala de 58 px e poses do herói de hoje):
- **Roupa do gênero, nas cores da escola:** colete **verde** aberto com debrum dourado sobre o peito, calça **larga
  lilás** franzida no tornozelo com punho rosa, faixa rosa larga na cintura, faixa rosa na cabeça, sandálias.
- **Fica de fora o que é da Disney:** colete roxo, calça bufante branca, fez vermelho. A calça foi escurecida de
  propósito para nunca ler como branca.
- **Pano que esvoaça:** a calça "atrasa" com o vento na corrida e infla no pulo; a silhueta das pernas fica larga,
  como na referência.
- **Mais magro (pedido do Pedro):** tronco, cintura, braços e coxas mais finos; a calça larga continua, então a
  silhueta fica esguia em cima e solta embaixo, como na referência.
- **Rosto novo (pedido do Pedro):** rosto mais fino e um pouco mais comprido, queixo estreito, maçã do rosto marcada,
  olho de perto maior (2×2) com pupila e brilho, sobrancelha grossa e arqueada, sorriso de canto confiante, cabelo
  mais cheio em cima. Traços nossos (cachos com a faixa rosa), não os do filme.
- **Quadros novos:** piscada no parado e aterrissagem (o corpo amassa ao tocar o chão, antes de voltar ao parado).

Teste da regra 3: lado a lado com o original deve dar "mesmo nível e mesmo jeito de pixel art", não "o mesmo
personagem redesenhado". Cores, rosto, cabelo (cachos com faixa) e peças são nossos.

Próximos passos se aprovado: aplicar no `gerar_jogador.py` (troca de figurino), ligar `piscando` e `aterrissando`
nas animações e, depois, mais quadros no estilo da referência (corrida de 10 a 12, parado impaciente, cambalhota).
