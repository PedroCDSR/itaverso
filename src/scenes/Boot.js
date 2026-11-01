import * as Phaser from 'phaser';

// Primeira cena: por enquanto só passa para a próxima.
// Nas próximas etapas: Preload (texturas das matrizes de arte, PNGs, áudio) e depois Título.
export class Boot extends Phaser.Scene {
  constructor() {
    super('Boot');
  }

  create() {
    this.scene.start('Teste');
  }
}
