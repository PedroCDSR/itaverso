// Arte da Fase 3 (Resgate) em matriz de texto: o projétil do Jafar (estrela girando, 2 quadros).
// Gerado por ferramentas/arte/gerar_chefe.py; dá para editar à mão.
// Jafar, gaiola e Tia Paula são PNG em public/assets/sprites/ (ferramentas/arte/gerar_elenco.py, Etapa 8A).

export const PALETA = {
  'k': '#2E1A33',
  'w': '#FFFFFF',
  'e': '#2A1A1C',
  's': '#D9956A',
  'S': '#B06E46',
  'p': '#5A3A8C',
  'P': '#3B2560',
  'l': '#9E9EFF',
  'm': '#C2457F',
  'M': '#8E2E5E',
  'o': '#F2C94C',
  'O': '#B98A2A',
  'y': '#F9FCBB',
  'b': '#6E4A2A',
  'h': '#E8C25A',
  'H': '#B88A32',
  'q': '#E8B48A',
  'Q': '#C48C64',
  'v': '#6D6BD9',
  'V': '#4F4DB0',
  'r': '#FFB0FA',
  'n': '#9A4040',
};

export const SPRITES = {
  projetil: {
    largura: 12,
    altura: 12,
    quadros: [
      [
        '............',
        '.....kk.....',
        '....kmmk....',
        '....kmmk....',
        '..kkmmrmkk..',
        '.kmmmyyrmmk.',
        '.kmmryyrrmk.',
        '..kkmrrrkk..',
        '....kmrk....',
        '....kmmk....',
        '.....kk.....',
        '............',
      ],
      [
        '............',
        '..k......k..',
        '.kmkk..kkmk.',
        '..kmmkkmmk..',
        '..kmmmrmmk..',
        '...kmyyrk...',
        '...kryyrrk..',
        '..kmmrrrmk..',
        '..kmmkrmmk..',
        '.kmkk.kkkmk.',
        '..k......k..',
        '............',
      ],
    ],
  },
};
