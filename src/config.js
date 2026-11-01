// Constantes do jogo num lugar só, para ajuste fácil (CLAUDE.md, seção 3).
// Os valores de física começam como palpite e serão afinados na Etapa 2, testando no celular.

// Resolução base: tudo é desenhado em 480x270 e ampliado para caber na tela.
export const LARGURA = 480;
export const ALTURA = 270;
export const TILE = 16;

// Paleta da escola (seção 7). Números para o Phaser; strings para textos e CSS.
export const CORES = {
  rosa: 0xffb0fa,
  lilas: 0x9e9eff,
  amarelo: 0xf9fcbb,
  roxo: 0x6d6bd9,
  verde: 0x6cc24a,
  branco: 0xffffff,
};
export const CORES_CSS = {
  rosa: '#FFB0FA',
  lilas: '#9E9EFF',
  amarelo: '#F9FCBB',
  roxo: '#6D6BD9',
  verde: '#6CC24A',
  branco: '#FFFFFF',
};

export const FONTES = {
  titulo: '"Press Start 2P"',
  dialogo: '"Patrick Hand"',
};

// Jogador (pixels por segundo; valores provisórios)
export const JOGADOR = {
  velocidade: 140,
  gravidade: 900,
  forcaPulo: 340,
  // fator aplicado à velocidade vertical ao soltar o pulo cedo (pulo variável)
  cortePulo: 0.45,
  coyoteMs: 100,
  bufferPuloMs: 100,
  quiqueInimigo: 260,
  quiqueToldo: 520,
  coracoes: 3,
  invencivelMs: 1000,
  macasIniciais: 5,
};

export const CHEFE = {
  vida: 5,
};

export const TAPETE = {
  duracaoSeg: 40,
};

// Controles de toque, em pixels do jogo (480x270). Num celular deitado 1 px do jogo vale ~1,4 px da tela,
// então raio 24 dá um botão de ~68 px reais (mínimo pedido: 64 px).
// As áreas de toque são maiores que o desenho: cada metade de baixo da tela é dividida entre os botões dela.
export const CONTROLES = {
  opacidade: 0.35,
  opacidadeApertado: 0.7,
  esquerda: { x: 40, y: 228, raio: 24 },
  direita: { x: 104, y: 228, raio: 24 },
  pular: { x: 436, y: 222, raio: 30 },
  maca: { x: 366, y: 236, raio: 22 },
  // toques acima desta linha (y) não contam como botão, para não atrapalhar o HUD
  alturaMinima: 120,
};
