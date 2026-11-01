// Músicas e vinhetas do jogo: melodias ORIGINAIS deste projeto, compostas para o jogo (nenhuma melodia conhecida).
// Tocadas em código pelo src/audio/musica.js, sem arquivos.
//
// Como escrever:
// - Cada "passo" é uma colcheia (meio tempo). `bpm` = tempos por minuto.
// - Notas: C D E F G A B, com # para sustenido, e a oitava (C5 = dó do meio + 1 oitava).
// - '-' segura a nota anterior por mais um passo. '.' é silêncio. '|' é só para separar compassos (ignorado).
// - Cada voz se repete no seu próprio tamanho (um baixo de 16 passos embaixo de uma melodia de 32 funciona).
// - Bateria: k = bumbo, s = caixa, h = chimbal.
// - onda: 'square' (quadrada, a "voz" de videogame), 'triangle' (suave), 'sine' (bem suave).

export const MUSICAS = {
  // Tela de título: calma, convidando a jogar (Sol maior).
  titulo: {
    bpm: 96,
    vozes: [
      {
        onda: 'triangle',
        volume: 0.5,
        notas: 'G4 . B4 D5 G5 - D5 . | E5 . D5 B4 A4 - - . | C5 . E5 G5 F#5 - D5 . | E5 D5 B4 A4 G4 - - .',
      },
      {
        onda: 'sine',
        volume: 0.55,
        notas: 'G2 . D3 . G3 . D3 . | E2 . B2 . E3 . B2 . | C3 . G3 . D3 . A3 . | C3 . D3 . G2 . D3 .',
      },
    ],
  },

  // Fase 1, Itajubá: saltitante, de correr pela rua (Dó maior).
  itajuba: {
    bpm: 140,
    vozes: [
      {
        onda: 'square',
        volume: 0.22,
        notas:
          'C5 . E5 G5 A5 G5 E5 . | D5 . F5 A5 G5 - . . | E5 G5 A5 C6 B5 A5 G5 . | F5 E5 D5 E5 C5 - - . |' +
          'C5 . E5 G5 A5 G5 E5 . | D5 . F5 A5 G5 - . . | A5 . G5 E5 F5 . D5 . | G5 F5 E5 D5 C5 - - .',
      },
      {
        onda: 'triangle',
        volume: 0.6,
        notas:
          'C3 . C4 . G3 . C4 . | D3 . D4 . A3 . D4 . | A2 . A3 . E3 . A3 . | F2 . F3 . G2 . G3 . |' +
          'C3 . C4 . G3 . C4 . | D3 . D4 . G2 . G3 . | F2 . F3 . C3 . F3 . | G2 . G3 . C3 . C4 .',
      },
    ],
    bateria: 'k . h . s . h . | k . h k s . h .',
  },

  // Fase 2, Espaço Paula De Marco: valsinha de caixinha de música, clima de aula de balé (3/4, Dó maior).
  espaco: {
    bpm: 100,
    vozes: [
      {
        onda: 'triangle',
        volume: 0.5,
        notas:
          'E5 - G5 - C6 - | B5 - A5 - G5 - | F5 - A5 - D6 - | C6 - B5 - G5 - |' +
          'E5 - G5 - C6 - | D6 - C6 - A5 - | G5 - F5 - D5 - | C5 - - - . .',
      },
      {
        onda: 'sine',
        volume: 0.55,
        notas:
          'C3 - G3 - G3 - | G2 - D3 - D3 - | D3 - A3 - A3 - | G2 - D3 - D3 - |' +
          'C3 - G3 - G3 - | F2 - C3 - C3 - | G2 - D3 - D3 - | C3 - G3 - C3 -',
      },
    ],
  },

  // Fase 3, Chefe: mais agitada, em menor, mas brincalhona (Lá menor).
  chefe: {
    bpm: 152,
    vozes: [
      {
        onda: 'square',
        volume: 0.2,
        notas: 'A4 . A4 C5 . A4 E5 . | D5 . C5 B4 . G4 A4 . | A4 . A4 C5 . E5 G5 . | F5 . E5 D5 B4 . A4 .',
      },
      {
        onda: 'triangle',
        volume: 0.6,
        notas:
          'A2 A3 A2 A3 A2 A3 A2 A3 | G2 G3 G2 G3 G2 G3 G2 G3 | F2 F3 F2 F3 F2 F3 F2 F3 | E2 E3 E2 E3 E2 E3 E2 E3',
      },
    ],
    bateria: 'k . s . k k s .',
  },

  // Fase 4, Tapete: notas longas, de voar ao entardecer (Fá maior).
  tapete: {
    bpm: 108,
    vozes: [
      {
        onda: 'triangle',
        volume: 0.5,
        notas: 'F5 - - A5 C6 - - A5 | G5 - - A#5 D6 - C6 - | A5 - - F5 C5 - - F5 | G5 - E5 - F5 - - -',
      },
      {
        onda: 'sine',
        volume: 0.55,
        notas: 'F2 . C3 . F3 . C3 . | G2 . D3 . G3 . D3 . | F2 . C3 . A3 . C3 . | C3 . G3 . F2 . C3 .',
      },
    ],
    bateria: 'k . h . . . h .',
  },

  // Final: festa, o espetáculo vai começar (Dó maior).
  final: {
    bpm: 132,
    vozes: [
      {
        onda: 'square',
        volume: 0.2,
        notas: 'G5 . G5 . C6 - G5 . | A5 . C6 . E6 - D6 . | C6 . A5 . G5 . E5 . | F5 . D5 . C5 - - .',
      },
      {
        onda: 'triangle',
        volume: 0.6,
        notas: 'C3 . G3 . C3 . G3 . | F2 . C3 . F3 . C3 . | C3 . G3 . A2 . E3 . | G2 . D3 . C3 . G3 .',
      },
    ],
    bateria: 'k . h . s . h .',
  },
};

// Vinhetas curtas, tocadas uma vez por cima da música (que abaixa enquanto isso).
export const VINHETAS = {
  checkpoint: { bpm: 220, vozes: [{ onda: 'square', volume: 0.25, notas: 'E5 G5 C6 - -' }] },
  ingresso: { bpm: 240, vozes: [{ onda: 'square', volume: 0.25, notas: 'G5 B5 D6 G6 - - -' }] },
  vitoria: {
    bpm: 200,
    vozes: [
      { onda: 'square', volume: 0.25, notas: 'C5 E5 G5 C6 . G5 C6 - - - - .' },
      { onda: 'triangle', volume: 0.6, notas: 'C3 . G3 . C4 . E3 G3 - - - .' },
    ],
  },
};
