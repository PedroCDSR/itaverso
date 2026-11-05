// Geometria exclusiva da missão lateral. A praça top-down não usa estes dados.
export const PERCURSO_URBANO = {
  largura: 5760, altura: 832, inicio: 80, fim: 5512,
  retornos: [80, 1728, 4448],
  perfil: [[0, 640], [1760, 640], [4960, 432], [5760, 432]],
  setores: [
    [0, 'praca'], [1760, 'subida'], [3856, 'casaroes'], [5104, 'igreja'],
  ],
  // Altura relativa à calçada. Cada apoio tem desenho e superfície com a mesma medida.
  apoios: [
    { id: 'banco', x: 376, largura: 64, altura: 18, tipo: 'banco' },
    { id: 'canteiro', x: 1072, largura: 80, altura: 22, tipo: 'jardim' },
    { id: 'degrau1', x: 2304, largura: 48, altura: 20, tipo: 'muro' },
    { id: 'degrau2', x: 2352, largura: 48, altura: 40, tipo: 'muro' },
    { id: 'mureta', x: 2400, largura: 80, altura: 60, tipo: 'jardim' },
    { id: 'toldo', x: 2504, largura: 112, altura: 108, tipo: 'toldo' },
    { id: 'marquise', x: 2696, largura: 144, altura: 180, tipo: 'marquise' },
    { id: 'descida', x: 2912, largura: 96, altura: 88, tipo: 'muro' },
    { id: 'canteiro2', x: 3504, largura: 80, altura: 22, tipo: 'jardim' },
    { id: 'final1', x: 5008, largura: 48, altura: 16, tipo: 'muro' },
    { id: 'final2', x: 5056, largura: 64, altura: 32, tipo: 'muro' },
    { id: 'final3', x: 5120, largura: 48, altura: 16, tipo: 'muro' },
  ],
  pombos: [2064, 3248, 4080],
  // Posição do centro e altura da fachada. Fachadas preenchem a rua inteira.
  fachadas: [
    ['clube', 296, 220], ['sobrado', 624, 170], ['concha', 1040, 118],
    ['cafe', 1464, 210], ['sobrado', 1904, 216], ['tijolos', 2160, 222],
    ['loja', 2544, 202], ['sobrado', 2784, 250], ['verde', 3064, 160],
    ['sobrado', 3344, 200], ['azul', 3664, 178], ['azul', 3952, 182],
    ['brancoazul', 4320, 180], ['brancoazul', 4720, 180], ['igreja', 5496, 205],
  ],
};

export function chaoUrbano(x) {
  const p = PERCURSO_URBANO.perfil;
  for (let i = 1; i < p.length; i++) {
    if (x <= p[i][0]) {
      const [a, ya] = p[i - 1], [b, yb] = p[i];
      return ya + (yb - ya) * Math.max(0, (x - a) / (b - a));
    }
  }
  return p.at(-1)[1];
}

export const APOIOS_URBANOS = PERCURSO_URBANO.apoios.map((p) => ({
  ...p, y: Math.round(chaoUrbano(p.x + p.largura / 2) - p.altura),
}));

export const SEQUENCIAS_URBANAS = [
  { id: 'bancos', x: 332, passo: 38, altura: 28, arco: 34 },
  { id: 'fonte', x: 810, passo: 36, altura: 22, arco: 18 },
  { id: 'jardim', x: 1034, passo: 38, altura: 30, arco: 34 },
  { id: 'cafe', x: 1480, passo: 38, altura: 22, arco: 18 },
  { id: 'subida', x: 1880, passo: 38, altura: 24, arco: 32 },
  { id: 'toldos', x: 2608, passo: 32, altura: 200, arco: 34 },
  { id: 'casaroes', x: 3752, passo: 38, altura: 24, arco: 26 },
  { id: 'chegada', x: 4980, passo: 42, altura: 34, arco: 38 },
];

export const FICHAS_URBANAS = SEQUENCIAS_URBANAS.flatMap((s) =>
  Array.from({ length: 5 }, (_, i) => ({
    id: `${s.id}-${i}`, sequencia: s.id, valor: 10,
    x: s.x + i * s.passo,
    y: Math.round(chaoUrbano(s.x + i * s.passo) - s.altura - Math.sin(i * Math.PI / 4) * s.arco),
  })),
).concat([{ id: 'estrela-toldos', valor: 50, x: 2816, y: APOIOS_URBANOS.find((p) => p.id === 'marquise').y - 28 }]);

export const PONTOS_MAXIMOS_URBANOS = 850;

// Resolver a calçada inclinada sem degraus invisíveis ou alterar a física da exploração.
// Um corpo abaixo do chão (ex.: queda forçada) não é teleportado para cima.
export function tocaCalcada({ x, anteriorX, fundo, fundoAnterior, velocidadeY, alturaCorpo }) {
  const y = chaoUrbano(x), antes = chaoUrbano(anteriorX);
  return velocidadeY >= 0 && fundo >= y && fundoAnterior <= antes + 5 && fundo - y < alturaCorpo;
}
