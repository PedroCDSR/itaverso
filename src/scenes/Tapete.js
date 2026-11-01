import * as Phaser from 'phaser';
import { LARGURA, ALTURA, CORES, CORES_CSS, FONTES } from '../config.js';
import { TEXTOS } from '../data/textos.js';

// Tela PROVISÓRIA da Fase 4 (Tapete), até a Etapa 6 trocar este arquivo pela fase de verdade.
// Mostra o Aladdin e a Tia Paula num tapete com a estampa de quadrados do logo, e deixa lutar de novo.
export class Tapete extends Phaser.Scene {
  constructor() {
    super('Tapete');
  }

  create() {
    const t = TEXTOS.tapete;
    this.add.image(0, 0, 'ceu').setOrigin(0);
    this.add.tileSprite(0, 0, LARGURA, ALTURA, 'morros').setOrigin(0);
    this.cameras.main.fadeIn(400, 158, 158, 255);

    this.add
      .text(LARGURA / 2, 40, t.titulo, { fontFamily: FONTES.titulo, fontSize: '16px', color: CORES_CSS.branco })
      .setOrigin(0.5)
      .setShadow(2, 2, CORES_CSS.roxo, 0, false, true);

    // tapete com os dois em cima, balançando
    const voo = this.add.container(LARGURA / 2, 124);
    const g = this.add.graphics();
    g.fillStyle(0x2e1a33).fillRect(-46, -2, 92, 12);
    g.fillStyle(CORES.rosa).fillRect(-44, 0, 88, 8);
    // quadrados concêntricos do logo como estampa
    for (let x = -36; x <= 36; x += 18) {
      g.lineStyle(1, CORES.roxo).strokeRect(x - 4, 1, 8, 6);
      g.fillStyle(CORES.amarelo).fillRect(x - 1, 3, 2, 2);
    }
    g.fillStyle(CORES.amarelo).fillRect(-48, 1, 3, 2).fillRect(-48, 5, 3, 2).fillRect(45, 1, 3, 2).fillRect(45, 5, 3, 2);
    const aladdin = this.add.sprite(-16, 2, 'jogador', 0).setOrigin(0.5, 1).play('parado');
    const paula = this.add.sprite(18, 2, 'tiaPaula', 2).setOrigin(0.5, 1).setFlipX(true).play('paula-feliz');
    voo.add([aladdin, paula, g]);
    this.tweens.add({ targets: voo, y: 116, duration: 900, yoyo: true, repeat: -1, ease: 'Sine.inOut' });

    // fundo claro atrás do texto, para ler bem em cima dos morros
    this.add.rectangle(LARGURA / 2, 160, LARGURA - 80, 34, CORES.branco, 0.85).setStrokeStyle(2, CORES.roxo);
    this.add
      .text(LARGURA / 2, 160, t.proxima, {
        fontFamily: FONTES.dialogo,
        fontSize: '17px',
        color: CORES_CSS.roxo,
        align: 'center',
        wordWrap: { width: LARGURA - 60 },
      })
      .setOrigin(0.5);

    const botao = this.add.rectangle(LARGURA / 2, 214, 190, 40, CORES.rosa).setStrokeStyle(3, CORES.roxo);
    this.add
      .text(LARGURA / 2, 215, t.jogarDeNovo, { fontFamily: FONTES.titulo, fontSize: '12px', color: CORES_CSS.roxo })
      .setOrigin(0.5);
    const deNovo = () => this.scene.start('Chefe', { direto: true });
    botao.setInteractive({ useHandCursor: true }).on('pointerup', deNovo);
    this.input.keyboard?.once('keydown-ENTER', deNovo);
  }
}
