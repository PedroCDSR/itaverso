import * as Phaser from 'phaser';
import { LARGURA, ALTURA, CORES_CSS, JOGADOR } from './config.js';
import { Boot } from './scenes/Boot.js';
import { Preload } from './scenes/Preload.js';
import { Titulo } from './scenes/Titulo.js';
import { Intro } from './scenes/Intro.js';
import { Itajuba } from './scenes/Itajuba.js';
import { HUD } from './scenes/HUD.js';
import { Espaco } from './scenes/Espaco.js';
import { Chefe } from './scenes/Chefe.js';
import { Tapete } from './scenes/Tapete.js';
import { Final } from './scenes/Final.js';
import { Pausa } from './scenes/Pausa.js';
import { Sobre } from './scenes/Sobre.js';
import { ligarPausaGlobal } from './ui/pausaGlobal.js';
import { iniciarAvisoGirar } from './ui/AvisoGirar.js';
import { iniciarPausaFoco } from './ui/PausaFoco.js';
import { iniciarSom } from './audio/som.js';
import { carregarDificuldade } from './dificuldade.js';

// nível escolhido antes (ou ?dificuldade=...), aplicado antes de qualquer cena ler as constantes
carregarDificuldade();

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
    // tela cheia (só pelo botão da pausa) na div inteira, com os avisos HTML dentro, não só no canvas
    fullscreenTarget: container,
  },
  input: {
    // até 4 dedos ao mesmo tempo (andar e pular juntos, com folga)
    activePointers: 4,
    // Escuta toques na página inteira, não só no desenho do jogo: no celular deitado sobram
    // faixas nas laterais, e é exatamente ali que ficam os polegares.
    touch: { target: container },
  },
  // O som do jogo é todo nosso (src/audio/), com um AudioContext só. Sem isto o Phaser criaria um segundo
  // contexto, que nunca tocaria nada e ainda contaria no limite de contextos do iPhone.
  audio: { noAudio: true },
  physics: {
    default: 'arcade',
    arcade: { gravity: { x: 0, y: JOGADOR.gravidade }, debug: false },
  },
  // Pausa e Sobre ficam no fim da lista: assim aparecem desenhadas por cima das outras cenas.
  scene: [Boot, Preload, Titulo, Intro, Itajuba, Espaco, Chefe, HUD, Tapete, Final, Pausa, Sobre],
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
  iniciarSom();
  iniciarPausaFoco();
  iniciarAvisoGirar();
  // só no `npm run dev`: deixa o jogo acessível no console do navegador para depurar
  if (import.meta.env.DEV) window.jogo = jogo;
}

iniciar();
