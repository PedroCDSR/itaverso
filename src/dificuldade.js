// Níveis de dificuldade (escolhidos no Título; decisão do Pedro em 01/11/2026).
//
// Cada nível só AJUSTA as constantes de config.js: na troca, tudo volta ao valor original (o "difícil", que era o
// jogo até aqui) e depois recebe os ajustes do nível. Assim as cenas continuam lendo JOGADOR, CHEFE e TAPETE
// como sempre. Os mapas curtos do fácil (sem buracos) ficam em src/levels/ e as cenas escolhem pelo `mapaCurto`.
//
// Fácil: jogo ~40% mais curto (Fase 1 e Tapete menores), sem buracos, Jafar com metade da força.
// Médio: mapas inteiros, um pouco mais de vida e um Jafar um pouco mais fraco.
// Difícil: o jogo original.
import { JOGADOR, CHEFE, TAPETE } from './config.js';

export const NIVEIS = {
  facil: {
    mapaCurto: true,
    JOGADOR: { coracoes: 5 },
    // 50% mais fraco: metade dos acertos (5 → 3, arredondado para cima), leque de 2 tiros e tiros mais lentos
    CHEFE: { vida: 3, projeteis: 2, velocidadeProjetil: 85, vulneravelMs: 4200 },
    TAPETE: { sapatilhasPerdidas: 1 },
  },
  medio: {
    mapaCurto: false,
    JOGADOR: { coracoes: 4 },
    CHEFE: { vida: 4, velocidadeProjetil: 100 },
    TAPETE: { sapatilhasPerdidas: 1 },
  },
  dificil: {
    mapaCurto: false,
  },
};
export const PADRAO = 'medio';

const ALVOS = { JOGADOR, CHEFE, TAPETE };
// cópia dos valores originais (o nível difícil), para poder voltar a eles
const ORIGINAL = Object.fromEntries(Object.entries(ALVOS).map(([k, v]) => [k, { ...v }]));
const CHAVE = 'aladdin-dificuldade';

let atual = PADRAO;

export function aplicarDificuldade(nivel) {
  if (!NIVEIS[nivel]) nivel = PADRAO;
  atual = nivel;
  for (const [nome, alvo] of Object.entries(ALVOS)) Object.assign(alvo, ORIGINAL[nome], NIVEIS[nivel][nome] || {});
  try {
    localStorage.setItem(CHAVE, nivel);
  } catch {
    // sem armazenamento (aba anônima): só não lembra a escolha
  }
}

export function dificuldade() {
  return atual;
}

export function mapaCurto() {
  return NIVEIS[atual].mapaCurto;
}

// Na abertura: ?dificuldade=facil|medio|dificil (para testar) ou a última escolha deste aparelho.
export function carregarDificuldade() {
  let nivel = new URLSearchParams(location.search).get('dificuldade');
  if (!NIVEIS[nivel]) {
    try {
      nivel = localStorage.getItem(CHAVE);
    } catch {
      nivel = null;
    }
  }
  aplicarDificuldade(NIVEIS[nivel] ? nivel : PADRAO);
}
