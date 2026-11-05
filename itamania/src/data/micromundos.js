import { NOMES_FASES } from './textos.js';
import { PERCURSO_URBANO } from './missaoUrbana.js';

// Os nomes e a ordem vêm do mapa do Pedro. Só a praça tem micromundo implementado neste recorte.
export const MICROMUNDOS = NOMES_FASES.slice(1).map((nome, i) => ({
  id: i + 1, nome, exploracao: i === 3 ? 'Praca' : null,
  missoes: i === 3 ? ['jardins-praca', 'fuga-praca'] : [],
  pontoSeguro: i === 3 ? { x: 664, y: 598.4 } : null,
  encontros: i === 3 ? [
    { id: 'gamba-jardim', tipo: 'especial', x: 848, y: 576, missao: 'jardins-praca' },
    { id: 'rua-lateral', tipo: 'comum', x: 880, y: 608, largura: 96, altura: 32, missao: 'fuga-praca' },
  ] : [],
}));
export const REGIAO_PRACA = MICROMUNDOS[3];
export const MISSOES = {
  'jardins-praca': {
    ...PERCURSO_URBANO,
    id: 'jardins-praca', regiao: 4, nome: 'Da praça à igreja', tipo: 'travessia',
    recompensa: 5,
    medalhas: [{ pontos: 200, premio: 1 }, { pontos: 500, premio: 2 }, { pontos: 750, premio: 2 }],
  },
};

// A fuga reutiliza o percurso, com perseguidor e regras de retorno do mesmo sistema.
MISSOES['fuga-praca'] = { ...MISSOES['jardins-praca'], id: 'fuga-praca', nome: 'Corrida até a igreja', tipo: 'fuga', economia: 'jardins-praca' };
