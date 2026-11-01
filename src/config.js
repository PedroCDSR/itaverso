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

// Jogador (pixels e segundos). Ajuste aqui e teste no celular.
// Altura do pulo ≈ forcaPulo² / (2 × gravidade): 360² / 1800 = 72 px = 4,5 tiles.
export const JOGADOR = {
  velocidade: 140, // corrida máxima
  aceleracaoChao: 1400, // quanto mais alto, mais "na hora" ele arranca
  aceleracaoAr: 900, // controle no ar (um pouco menor que no chão)
  freio: 1800, // parar ao soltar o direcional
  gravidade: 900,
  gravidadeQuedaExtra: 500, // cai mais rápido do que sobe: pulo mais "firme"
  quedaMaxima: 520,
  forcaPulo: 360,
  // ao soltar o pulo durante a subida, a velocidade vertical é multiplicada por isto (pulo variável)
  cortePulo: 0.45,
  coyoteMs: 100, // ainda dá para pular logo depois de sair da beirada
  bufferPuloMs: 100, // apertar pular pouco antes de tocar o chão também vale
  quiqueInimigo: 260,
  quiqueToldo: 520,
  coracoes: 3,
  invencivelMs: 1000,
  macasIniciais: 5,
  // corpo de colisão dentro do quadro 32x48 (menor que o desenho, para não "enroscar" nas beiradas)
  corpo: { largura: 14, altura: 36, x: 9, y: 11 },
};

// Câmera: zona morta no meio da tela onde o jogador anda sem a câmera mexer
export const CAMERA = {
  zonaMortaLargura: 64,
  zonaMortaAltura: 48,
  suavidade: 0.15,
  // a câmera fica um pouco à frente do jogador, mostrando mais do caminho
  folgaFrente: 40,
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
