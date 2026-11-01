import * as Phaser from 'phaser';
import { LARGURA, ALTURA, CORES_CSS, JOGADOR } from './config.js';
import { Boot } from './scenes/Boot.js';
import { Preload } from './scenes/Preload.js';
import { Itajuba } from './scenes/Itajuba.js';
import { HUD } from './scenes/HUD.js';
import { EmBreve } from './scenes/EmBreve.js';
import { Tapete } from './scenes/Tapete.js';
import { Final } from './scenes/Final.js';
import { ligarPausaGlobal } from './ui/pausaGlobal.js';
import { iniciarAvisoGirar } from './ui/AvisoGirar.js';
import { iniciarPausaFoco } from './ui/PausaFoco.js';
import { iniciarSom } from './audio/som.js';

const container = document.getElementById('jogo');

// Configuração do Phaser (CLAUDE.md, seção 4).
const config = {
  type: Phaser.AUTO,
  parent: container,
  width: LARGURA,
  height: ALTURA,
  backgroundColor: CORES_CSS.lilas,
  pixelArt: true,
  roundPixels: true,
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
    // tela cheia na div inteira (com os avisos HTML dentro), não só no canvas
    fullscreenTarget: container,
  },
  input: {
    // até 4 dedos ao mesmo tempo (andar e pular juntos, com folga)
    activePointers: 4,
    // Escuta toques na página inteira, não só no desenho do jogo: no celular deitado sobram
    // faixas nas laterais, e é exatamente ali que ficam os polegares.
    touch: { target: container },
  },
  physics: {
    default: 'arcade',
    arcade: { gravity: { x: 0, y: JOGADOR.gravidade }, debug: false },
  },
  scene: [Boot, Preload, Itajuba, HUD, EmBreve, Tapete, Final],
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
  const jogo = new Phaser.Game(config);
  ligarPausaGlobal(jogo);
  iniciarSom(jogo);
  iniciarPausaFoco();
  iniciarAvisoGirar();
  // só no `npm run dev`: deixa o jogo acessível no console do navegador para depurar
  if (import.meta.env.DEV) window.jogo = jogo;
}

iniciar();
