// Músicas e vinhetas do ITAMANIA: melodias ORIGINAIS, compostas para este jogo, tocadas em código (audio/musica.js).
//
// Como escrever:
// - Cada passo é uma colcheia. `bpm` = tempos por minuto.
// - Notas: C D E F G A B, com # para sustenido, e a oitava (C5 = dó uma oitava acima do dó central).
// - '-' segura a nota anterior. '.' é silêncio. '|' só separa compassos.
// - Cada voz se repete no próprio tamanho. Bateria: k = bumbo, s = caixa, h = chimbal.

export const MUSICAS = {
  // Título: alegre, de quem chegou numa cidade nova (Ré maior).
  titulo: {
    bpm: 112,
    vozes: [
      { onda: 'square', volume: 0.32, notas: 'D5 . F#5 A5 - F#5 E5 D5 | E5 - B4 - - . . . | C#5 . E5 G5 - E5 D5 C#5 | D5 - A4 - - . . . | B4 . D5 F#5 - E5 D5 B4 | A4 . F#4 A4 D5 - E5 . | F#5 . E5 D5 C#5 . A4 . | D5 - - - - . . .' },
      { onda: 'triangle', volume: 0.55, notas: 'D3 . A3 . D3 . A3 . | E3 . B3 . E3 . B3 . | A2 . E3 . A2 . E3 . | D3 . A3 . F#3 . A3 . | G2 . D3 . G2 . D3 . | D3 . A3 . D3 . A3 . | A2 . E3 . A2 . C#3 . | D3 . A3 . D3 . . .' },
    ],
    bateria: 'k . h . s . h . | k . h k s . h .',
  },

  // Mapa e cartão: calmo, de passeio (Sol maior).
  mapa: {
    bpm: 92,
    vozes: [
      { onda: 'triangle', volume: 0.5, notas: 'G4 - B4 - D5 - B4 . | C5 - A4 - F#4 - D4 . | E4 - G4 - B4 - G4 . | A4 - - - D4 - - . | G4 - B4 - D5 - E5 . | D5 - B4 - G4 - E4 . | C5 - B4 - A4 - F#4 . | G4 - - - - - - .' },
      { onda: 'sine', volume: 0.55, notas: 'G2 . D3 . G2 . D3 . | D2 . A2 . D2 . A2 . | E2 . B2 . E2 . B2 . | D2 . A2 . D2 . F#2 .' },
    ],
  },

  // Fase 1, Rodoviária: ritmo de viagem, "trem" na bateria (Dó maior).
  rodoviaria: {
    bpm: 132,
    vozes: [
      { onda: 'square', volume: 0.3, notas: 'C5 . E5 . G5 . E5 G5 | A5 - G5 . E5 . C5 . | D5 . F5 . A5 . F5 A5 | G5 - - . . . . . | C5 . E5 . G5 . C6 . | B5 - A5 . G5 . E5 . | F5 . E5 . D5 . G4 . | C5 - - . . . . .' },
      { onda: 'triangle', volume: 0.55, notas: 'C3 . G3 . C3 . G3 . | F2 . C3 . F2 . C3 . | D3 . A3 . D3 . A3 . | G2 . D3 . G2 . B2 . | C3 . G3 . C3 . G3 . | A2 . E3 . A2 . E3 . | F2 . C3 . G2 . D3 . | C3 . G3 . C3 . . .' },
    ],
    bateria: 'k h h h s h h h | k h h k s h h h',
  },

  // Fase 2, Praça do Soldado: marchinha leve (Fá maior).
  praca: {
    bpm: 120,
    vozes: [
      { onda: 'square', volume: 0.3, notas: 'F4 . A4 . C5 - A4 . | A#4 . D5 . F5 - D5 . | C5 . A4 . F4 . A4 . | G4 - - . C5 . . . | F4 . A4 . C5 - F5 . | E5 . D5 . C5 . A#4 . | A4 . G4 . C5 . E4 . | F4 - - . . . . .' },
      { onda: 'triangle', volume: 0.55, notas: 'F2 . C3 . F2 . C3 . | A#2 . F3 . A#2 . F3 . | F2 . C3 . F2 . A2 . | C3 . G3 . C3 . E3 .' },
    ],
    bateria: 'k . s . k . s s | k . s . k k s .',
  },

  // Fase 3, Rua Nova: comércio movimentado, sincopado (Lá menor e Dó).
  ruanova: {
    bpm: 126,
    vozes: [
      { onda: 'square', volume: 0.28, notas: 'A4 . C5 E5 . C5 D5 . | E5 . G5 - E5 D5 C5 . | F5 . E5 D5 . C5 B4 . | C5 . A4 - - . . . | A4 . C5 E5 . G5 A5 . | G5 . E5 - D5 . C5 . | D5 . E5 F5 . E5 D5 B4 | A4 - - . . . . .' },
      { onda: 'triangle', volume: 0.55, notas: 'A2 . A3 . E3 . A3 . | C3 . C4 . G3 . C4 . | F2 . F3 . C3 . F3 . | E2 . E3 . B2 . E3 .' },
    ],
    bateria: 'k . h k s . h . | k h . k s . h h',
  },

  // Fase 4, Praça central: festiva, cheiro de pão de queijo (Mi bemol... aqui Mi maior para soar brilhante).
  centro: {
    bpm: 138,
    vozes: [
      { onda: 'square', volume: 0.3, notas: 'E5 . G#5 . B5 . G#5 . | A5 . F#5 . D#5 . B4 . | C#5 . E5 . A5 . G#5 F#5 | G#5 - - . . . . . | E5 . G#5 . B5 . E6 . | D#6 . C#6 . B5 . A5 . | G#5 . F#5 . D#5 . B4 . | E5 - - . . . . .' },
      { onda: 'triangle', volume: 0.55, notas: 'E3 . B3 . E3 . B3 . | B2 . F#3 . B2 . F#3 . | A2 . E3 . A2 . E3 . | E3 . B3 . G#3 . B3 . | E3 . B3 . E3 . B3 . | A2 . E3 . A2 . E3 . | B2 . F#3 . B2 . D#3 . | E3 . B3 . E3 . . .' },
    ],
    bateria: 'k . h . s . h k | k . h . s . h h',
  },
};

export const VINHETAS = {
  checkpoint: { bpm: 220, vozes: [{ onda: 'square', volume: 0.25, notas: 'E5 G5 C6 - -' }] },
  poder: { bpm: 260, vozes: [{ onda: 'square', volume: 0.25, notas: 'C5 E5 G5 C6 E6 G6 - - -' }, { onda: 'triangle', volume: 0.5, notas: 'C3 . G3 . C4 - - - -' }] },
  vitoria: {
    bpm: 200,
    vozes: [
      { onda: 'square', volume: 0.25, notas: 'G4 C5 E5 G5 . E5 G5 - - - - .' },
      { onda: 'triangle', volume: 0.6, notas: 'C3 . G3 . C4 . E3 G3 - - - .' },
    ],
  },
};
