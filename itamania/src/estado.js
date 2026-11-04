// Progresso da partida. Fica só no aparelho (localStorage), sem servidor e sem dado pessoal (DESIGN.md, regra 7).
import { escolherHeroi } from './genero.js';

const CHAVE = 'itamania-progresso-v1';

const NOVO = () => ({
  heroi: 'geraldo',
  liberada: 1, // maior fase que dá para jogar no mapa
  feitas: [], // fases já terminadas
  itacoins: 0,
  bone: false,
  paes: 0, // pães de queijo na mochila
  temPao: false, // ganhou o poder do pão de queijo (fase 4)
  temCafe: false, // conhece o café com leite (fase 4)
});

export const estado = NOVO();

export function carregar() {
  try {
    const salvo = JSON.parse(localStorage.getItem(CHAVE) || 'null');
    if (salvo && typeof salvo === 'object') Object.assign(estado, NOVO(), salvo);
  } catch {
    // sem localStorage (aba anônima, bloqueio): joga sem salvar
  }
  escolherHeroi(estado.heroi);
  return estado;
}

export function salvar() {
  try {
    localStorage.setItem(CHAVE, JSON.stringify(estado));
  } catch {
    // sem localStorage: segue sem salvar
  }
}

export function temProgresso() {
  return estado.feitas.length > 0;
}

export function novoJogo(heroi) {
  Object.assign(estado, NOVO(), { heroi });
  escolherHeroi(heroi);
  salvar();
}

export function terminarFase(n) {
  if (!estado.feitas.includes(n)) estado.feitas.push(n);
  estado.liberada = Math.max(estado.liberada, n + 1);
  salvar();
}
