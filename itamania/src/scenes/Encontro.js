import * as Phaser from 'phaser';
import { FONTES } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { tocarEfeito } from '../audio/efeitos.js';

export class Encontro extends Phaser.Scene {
  constructor() { super('Encontro'); }
  init(dados) { this.sessao = dados.sessao; }
  create() {
    const t = TEXTOS.missao;
    this.cameras.main.setBackgroundColor('#24394b');
    this.add.rectangle(240, 135, 480, 86, 0xf4cc65).setAngle(-4);
    const s = this.add.sprite(-60, 140, 'sunny-gamba', 0).setDisplaySize(100, 78).play('gamba-andar');
    this.tweens.add({ targets: s, x: 95, duration: 350, ease: 'Back.out' });
    this.add.text(165, 95, t.encontro, { fontFamily: FONTES.titulo, fontSize: '12px', color: '#24394b' });
    this.add.text(165, 124, t.vilao, { fontFamily: FONTES.dialogo, fontSize: '23px', color: '#24394b' });
    this.add.text(165, 154, t.convite, { fontFamily: FONTES.dialogo, fontSize: '15px', color: '#24394b' });
    tocarEfeito('dano', { volume: 0.25 });
    this.cameras.main.shake(180, 0.004);
    // Cortina de blocos, sem flashes repetidos; cerca de dois segundos até a missão.
    this.time.delayedCall(1450, () => {
      for (let col = 0; col < 20; col++) for (let row = 0; row < 12; row++) {
        const bloco = this.add.rectangle(col * 24, row * 24, 24, 24, 0x24394b).setOrigin(0).setScale(0);
        this.tweens.add({ targets: bloco, scaleX: 1, scaleY: 1, duration: 180, delay: (col + row) * 10 });
      }
    });
    this.time.delayedCall(2050, () => this.scene.start('Missao', { sessao: this.sessao }));
  }
}
