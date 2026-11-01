import * as Phaser from 'phaser';
import { LARGURA, CORES, CORES_CSS, FONTES } from '../config.js';
import { TEXTOS } from '../data/textos.js';

// Tela provisória do fim da Fase 1, até a Fase 2 (Espaço) existir na Etapa 4.
export class EmBreve extends Phaser.Scene {
  constructor() {
    super('EmBreve');
  }

  create(dados) {
    const t = TEXTOS.emBreve;
    this.cameras.main.setBackgroundColor(CORES_CSS.lilas).fadeIn(300, 158, 158, 255);
    this.add
      .text(LARGURA / 2, 60, t.titulo, { fontFamily: FONTES.titulo, fontSize: '12px', color: CORES_CSS.branco })
      .setOrigin(0.5)
      .setShadow(2, 2, CORES_CSS.roxo, 0, false, true);
    this.add.sprite(LARGURA / 2 - 50, 101, 'sapatilha', 0).setScale(2);
    this.add
      .text(LARGURA / 2 - 30, 101, `${t.sapatilhas(dados?.sapatilhas ?? 0)} / ${dados?.total ?? 0}`, {
        fontFamily: FONTES.dialogo,
        fontSize: '22px',
        color: CORES_CSS.roxo,
      })
      .setOrigin(0, 0.5);
    this.add
      .text(LARGURA / 2, 140, t.proxima, { fontFamily: FONTES.dialogo, fontSize: '18px', color: CORES_CSS.roxo })
      .setOrigin(0.5);

    const botao = this.add.rectangle(LARGURA / 2, 200, 190, 40, CORES.rosa).setStrokeStyle(3, CORES.roxo);
    this.add
      .text(LARGURA / 2, 201, t.jogarDeNovo, { fontFamily: FONTES.titulo, fontSize: '12px', color: CORES_CSS.roxo })
      .setOrigin(0.5);
    const deNovo = () => this.scene.start('Itajuba', { direto: true });
    botao.setInteractive({ useHandCursor: true }).on('pointerup', deNovo);
    this.input.keyboard?.once('keydown-ENTER', deNovo);
  }
}
