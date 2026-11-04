import { CORES } from '../config.js';

// Botão de pausa (duas barras) no canto de cima, ao lado do botão de som. Chama `acao` ao tocar.
export class BotaoPausa {
  constructor(scene, x, y, acao) {
    const g = scene.add.graphics().setScrollFactor(0).setDepth(1001);
    g.fillStyle(CORES.lilas, 0.6).fillCircle(x, y, 14).lineStyle(2, CORES.roxo).strokeCircle(x, y, 14);
    g.fillStyle(CORES.branco, 1).fillRect(x - 5, y - 6, 3, 12).fillRect(x + 2, y - 6, 3, 12);
    this.area = scene.add.zone(x, y, 36, 36).setScrollFactor(0).setDepth(1001).setInteractive({ useHandCursor: true });
    this.area.on('pointerup', () => acao());
  }
}
