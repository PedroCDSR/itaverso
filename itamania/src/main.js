import * as Phaser from 'phaser';
import { LARGURA, ALTURA, CORES_CSS, JOGADOR } from './config.js';
import { Boot } from './scenes/Boot.js';
import { Preload } from './scenes/Preload.js';
import { Titulo } from './scenes/Titulo.js';
import { Mapa } from './scenes/Mapa.js';
import { Fase } from './scenes/Fase.js';
import { HUD } from './scenes/HUD.js';
import { Cartao } from './scenes/Cartao.js';
import { Fim } from './scenes/Fim.js';
import { Pausa } from './scenes/Pausa.js';
import { Praca } from './scenes/Praca.js';
import { PracaUI } from './scenes/PracaUI.js';
import { ligarPausaGlobal } from './ui/pausaGlobal.js';
import { iniciarAvisoGirar } from './ui/AvisoGirar.js';
import { iniciarPausaFoco } from './ui/PausaFoco.js';
import { iniciarSom } from './audio/som.js';

const container = document.getElementById('jogo');

const config = {
  type: Phaser.AUTO,
  parent: container,
  width: LARGURA,
  height: ALTURA,
  backgroundColor: CORES_CSS.roxo,
  pixelArt: true,
  roundPixels: true,
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH, fullscreenTarget: container },
  // até 4 dedos; toque escutado na div inteira (as faixas laterais do celular deitado contam)
  input: { activePointers: 4, touch: { target: container } },
  audio: { noAudio: true }, // som todo em código (src/audio/), com um AudioContext só
  physics: { default: 'arcade', arcade: { gravity: { x: 0, y: JOGADOR.gravidade }, debug: false } },
  scene: [Boot, Preload, Titulo, Praca, PracaUI, Mapa, Fase, HUD, Cartao, Fim, Pausa],
};

async function iniciar() {
  try {
    await Promise.all([document.fonts.load('16px "Press Start 2P"'), document.fonts.load('16px "Patrick Hand"')]);
  } catch {
    // sem a fonte, segue com a padrão
  }
  const jogo = new Phaser.Game(config);
  ligarPausaGlobal(jogo);
  iniciarSom();
  iniciarPausaFoco();
  iniciarAvisoGirar();
  if (import.meta.env.DEV) window.jogo = jogo;
}

iniciar();
