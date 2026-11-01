import * as Phaser from 'phaser';

// Primeira cena: só passa para o Preload (texturas e animações). Depois vem o Título (Etapa 7).
export class Boot extends Phaser.Scene {
  constructor() {
    super('Boot');
  }

  create() {
    this.scene.start('Preload');
  }
}
