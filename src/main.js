import * as Phaser from 'phaser';
import { LARGURA, ALTURA, CORES_CSS, JOGADOR } from './config.js';
import { Boot } from './scenes/Boot.js';
import { Teste } from './scenes/Teste.js';

// Configuração do Phaser (CLAUDE.md, seção 4).
const config = {
  type: Phaser.AUTO,
  parent: 'jogo',
  width: LARGURA,
  height: ALTURA,
  backgroundColor: CORES_CSS.lilas,
  pixelArt: true,
  roundPixels: true,
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
  input: {
    // até 4 dedos ao mesmo tempo (correr e pular juntos, com folga)
    activePointers: 4,
  },
  physics: {
    default: 'arcade',
    arcade: { gravity: { x: 0, y: JOGADOR.gravidade }, debug: false },
  },
  scene: [Boot, Teste],
};

// Espera as fontes antes de criar o jogo: o Phaser desenha texto em canvas e não troca a fonte depois.
async function iniciar() {
  try {
    await Promise.all([
      document.fonts.load('16px "Press Start 2P"'),
      document.fonts.load('16px "Patrick Hand"'),
    ]);
  } catch {
    // sem a fonte o jogo ainda funciona, com a fonte padrão do navegador
  }
  new Phaser.Game(config);
}

iniciar();
