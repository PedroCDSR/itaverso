import { FICHAS_URBANAS } from '../data/missaoUrbana.js';

// Sem relógio: parar ou cair não apaga a sequência. IDs impedem repetir coletas no checkpoint.
export class PontosMissao {
  constructor() { this.pontos = 0; this.coletadas = new Set(); this.completas = new Set(); }
  coletar(id) {
    const ficha = FICHAS_URBANAS.find((f) => f.id === id);
    if (!ficha || this.coletadas.has(id)) return null;
    this.coletadas.add(id);
    let bonus = 0;
    if (ficha.sequencia && !this.completas.has(ficha.sequencia)) {
      const grupo = FICHAS_URBANAS.filter((f) => f.sequencia === ficha.sequencia);
      if (grupo.every((f) => this.coletadas.has(f.id))) {
        bonus = 50; this.completas.add(ficha.sequencia);
      }
    }
    this.pontos += ficha.valor + bonus;
    return { valor: ficha.valor, bonus, pontos: this.pontos };
  }
}
