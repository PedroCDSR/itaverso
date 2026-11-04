// Constantes do ITAMANIA num lugar só, para ajuste fácil.

export const LARGURA = 480;
export const ALTURA = 270;
export const TILE = 16;

// Paleta da interface: céu de Minas, pedra amarela (itacoin) e o verde da serra.
export const CORES = {
  azul: 0x3a5fcd,
  azulClaro: 0x9ec8ff,
  amarelo: 0xffd43a,
  amareloClaro: 0xfff6a8,
  verde: 0x5cc24a,
  laranja: 0xf2803a,
  rosa: 0xf07ab4,
  roxo: 0x2b2d5c,
  branco: 0xffffff,
  // nomes usados pelos módulos copiados do Aladdin (Botao, ControlesToque, BotaoSom)
  lilas: 0x9ec8ff,
};
export const CORES_CSS = {
  azul: '#3A5FCD',
  azulClaro: '#9EC8FF',
  amarelo: '#FFD43A',
  amareloClaro: '#FFF6A8',
  verde: '#5CC24A',
  laranja: '#F2803A',
  rosa: '#F07AB4',
  roxo: '#2B2D5C',
  branco: '#FFFFFF',
  lilas: '#9EC8FF',
};

export const FONTES = {
  titulo: '"Press Start 2P"',
  dialogo: '"Patrick Hand"',
};

// Herói. Altura do pulo ≈ forcaPulo² / (2 × gravidade). Normal: 360²/1800 = 72 px (4,5 tiles).
export const JOGADOR = {
  velocidade: 132,
  aceleracaoChao: 1400,
  aceleracaoAr: 900,
  freio: 1800,
  aterrissagemMs: 90,
  gravidade: 900,
  gravidadeQuedaExtra: 500,
  quedaMaxima: 520,
  forcaPulo: 360,
  cortePulo: 0.45,
  coyoteMs: 100,
  bufferPuloMs: 100,
  quiqueInimigo: 250,
  quiqueToldo: 520,
  quiqueToldoSemBotao: 420,
  recuoDano: { x: 150, y: 200 },
  atordoadoMs: 280,
  coracoes: 3,
  invencivelMs: 1100,
  // corpo de colisão dentro do quadro 48x64 (pé na linha 63)
  corpo: {
    normal: { largura: 16, altura: 36, x: 16, y: 28 },
    turbinado: { largura: 18, altura: 44, x: 15, y: 20 },
  },
  antecipacaoArremessoMs: 60,
  arremessoMs: 190,
};

// Pão de queijo arremessado: arco curto que quica e rola.
export const PAO = {
  velocidadeX: 230,
  velocidadeY: -150,
  gravidade: 700,
  quiques: 2,
  vidaMs: 1400,
  iniciais: 5, // quantos a lanchonete dá
};

export const CAMERA = {
  zonaMortaLargura: 64,
  zonaMortaAltura: 56,
  suavidade: 0.15,
  folgaFrente: 40,
};

// Inimigos leves (DESIGN.md): ninguém morre. Pisão = cochila (capivara) ou voa embora (pombo).
// Pão de queijo = pega, come e vai embora feliz.
export const INIMIGOS = {
  capivara: { velocidade: 26, corpo: { largura: 26, altura: 16 }, sono: true },
  pombo: { velocidade: 34, corpo: { largura: 16, altura: 14 }, sono: false },
};

export const ITENS = {
  precoBone: 10, // itacoins (fase 3)
};

export const CONTROLES = {
  opacidade: 0.35,
  opacidadeApertado: 0.7,
  esquerda: { x: 40, y: 228, raio: 24 },
  direita: { x: 104, y: 228, raio: 24 },
  pular: { x: 436, y: 222, raio: 30 },
  maca: { x: 366, y: 236, raio: 22 },
  alturaMinima: 120,
};

export const DIALOGO = {
  largura: 400,
  topo: 34,
  tamanhoFonte: 17,
  letrasPorSegundo: 55,
  esperaMinimaMs: 250,
  maxLinhas: 2,
};

// Conversa com NPC: distância em x para a fala começar.
export const CONVERSA = { distancia: 40 };

// Cartão de curiosidade: tempo mínimo na tela antes do botão CONTINUAR (uns 5 s de leitura, DESIGN.md).
export const CARTAO = { esperaMs: 2500 };

export const SOM = {
  volumeGeral: 0.8,
  volumeEfeitos: 0.7,
  volumeMusica: 0.25,
  volumeVinheta: 0.6,
  tema: null, // sem música em arquivo: todas as músicas são feitas em código (src/audio/musicas.js)
  cenasTema: [],
  volumeTema: 0.5,
};
