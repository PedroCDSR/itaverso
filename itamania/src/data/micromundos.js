import { NOMES_FASES } from './textos.js';

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
    id: 'jardins-praca', regiao: 4, nome: 'Trilhas da praça', tipo: 'travessia',
    largura: 3360, fim: 3232, recompensa: 5, recompensaRepetida: 1,
    retornos: [80, 1000, 1900],
    buracos: [[672, 736], [1376, 1440], [2208, 2272]],
    plataformas: [[384, 176, 96], [800, 176, 80], [1136, 160, 80], [1568, 176, 96], [1856, 160, 80], [2432, 176, 96], [2768, 160, 96]],
    inimigos: [912, 1696, 2576, 2928],
  },
};

// A fuga reutiliza o percurso, com perseguidor e regras de retorno do mesmo sistema.
MISSOES['fuga-praca'] = { ...MISSOES['jardins-praca'], id: 'fuga-praca', nome: 'Corrida pelos jardins', tipo: 'fuga' };
