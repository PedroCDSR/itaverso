import * as Phaser from 'phaser';
import { LARGURA, ALTURA, CORES, CORES_CSS, FONTES } from '../config.js';
import { EVENTO } from '../data/evento.js';
import { TEXTOS } from '../data/textos.js';

// Cena de teste da Etapa 0: confere escala, fontes, acentos, paleta e toque.
export class Teste extends Phaser.Scene {
  constructor() {
    super('Teste');
  }

  create() {
    const t = TEXTOS.teste;
    const cx = LARGURA / 2;

    // faixas com as cores da paleta, para conferir no celular
    const cores = [CORES.rosa, CORES.amarelo, CORES.roxo, CORES.verde];
    cores.forEach((c, i) => this.add.rectangle(i * (LARGURA / 4), 0, LARGURA / 4, 8, c).setOrigin(0));

    // Press Start 2P fica nítida em múltiplos de 8 px
    this.add
      .text(cx, 40, t.titulo, { fontFamily: FONTES.titulo, fontSize: '24px', color: CORES_CSS.branco })
      .setOrigin(0.5)
      .setShadow(2, 2, CORES_CSS.roxo, 0, false, true);

    this.add
      .text(cx, 72, t.subtitulo, { fontFamily: FONTES.titulo, fontSize: '8px', color: CORES_CSS.roxo })
      .setOrigin(0.5);

    // caixa de diálogo de exemplo com a fonte manuscrita
    this.add.rectangle(cx, 140, 400, 84, CORES.rosa).setStrokeStyle(2, CORES.roxo);
    this.add
      .text(cx, 140, [t.acentos, `${EVENTO.escola}`, EVENTO.data, EVENTO.local], {
        fontFamily: FONTES.dialogo,
        fontSize: '16px',
        color: CORES_CSS.roxo,
        align: 'center',
        lineSpacing: -2,
      })
      .setOrigin(0.5);

    const aviso = this.add
      .text(cx, 222, t.toque, { fontFamily: FONTES.titulo, fontSize: '8px', color: CORES_CSS.amarelo })
      .setOrigin(0.5);
    this.tweens.add({ targets: aviso, alpha: 0.3, duration: 600, yoyo: true, repeat: -1 });

    // cada toque mostra um círculo no ponto tocado (testa o multitoque)
    this.input.on('pointerdown', (p) => {
      aviso.setText(t.tocou);
      const marca = this.add.circle(p.x, p.y, 10, CORES.amarelo, 0.8);
      this.tweens.add({ targets: marca, scale: 2.5, alpha: 0, duration: 400, onComplete: () => marca.destroy() });
    });

    this.add
      .text(LARGURA - 4, ALTURA - 4, `Phaser ${Phaser.VERSION}`, {
        fontFamily: FONTES.titulo,
        fontSize: '8px',
        color: CORES_CSS.roxo,
      })
      .setOrigin(1, 1);
  }
}
