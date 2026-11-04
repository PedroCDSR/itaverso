import { CORES } from '../config.js';
import { alternarSom, estaMudo, quandoMudarMudo } from '../audio/som.js';

// Botão de som liga/desliga (alto-falante desenhado com formas). Fica no canto de cima, longe dos controles.
export class BotaoSom {
  constructor(scene, x, y) {
    this.scene = scene;
    this.g = scene.add.graphics().setScrollFactor(0).setDepth(1001);
    // área de toque generosa em volta do desenho
    this.area = scene.add
      .zone(x, y, 36, 36)
      .setScrollFactor(0)
      .setDepth(1001)
      .setInteractive({ useHandCursor: true });
    this.x = x;
    this.y = y;
    this.area.on('pointerdown', (p, lx, ly, ev) => {
      ev.stopPropagation();
      alternarSom();
    });
    this.desenhar();
    // a tecla M (ou outro botão de som) também muda o desenho
    const largar = quandoMudarMudo(() => this.g.active && this.desenhar());
    scene.events.once('shutdown', largar);
  }

  desenhar() {
    const { g, x, y } = this;
    g.clear();
    g.fillStyle(CORES.lilas, 0.6).fillCircle(x, y, 14).lineStyle(2, CORES.roxo).strokeCircle(x, y, 14);
    // corpo do alto-falante
    g.fillStyle(CORES.branco, 1);
    g.fillRect(x - 8, y - 3, 4, 6);
    g.fillTriangle(x - 4, y - 3, x + 1, y - 8, x + 1, y + 3);
    g.fillTriangle(x - 4, y + 3, x + 1, y + 8, x + 1, y - 3);
    g.lineStyle(2, CORES.branco, 1);
    if (estaMudo()) {
      // X de mudo
      g.lineBetween(x + 4, y - 4, x + 10, y + 4).lineBetween(x + 10, y - 4, x + 4, y + 4);
    } else {
      // ondas de som
      g.beginPath().arc(x + 2, y, 5, -0.9, 0.9).strokePath();
      g.beginPath().arc(x + 2, y, 9, -0.9, 0.9).strokePath();
    }
  }
}
