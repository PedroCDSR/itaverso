import * as Phaser from 'phaser';
import { INIMIGOS, CORES_CSS, FONTES } from '../config.js';

// Inimigos leves (DESIGN.md, regra 2: ninguém morre).
//   capivara: anda devagar; pisão = deita e cochila com "zzz"; pão de queijo = come feliz e vai embora.
//   pombo:    anda bicando o chão; pisão = sai voando; pão de queijo = come e sai voando feliz.
// Encostar de lado num inimigo acordado dá um toque no herói.
export class Inimigo extends Phaser.Physics.Arcade.Sprite {
  constructor(scene, x, y, tipo, camada) {
    super(scene, x, y, tipo, 0);
    this.tipo = tipo;
    this.cfg = INIMIGOS[tipo];
    scene.add.existing(this);
    scene.physics.add.existing(this);
    this.camada = camada;
    this.setOrigin(0.5, 1);
    const c = this.cfg.corpo;
    this.body.setSize(c.largura, c.altura).setOffset((this.width - c.largura) / 2, this.height - c.altura);
    this.estado = 'andando';
    this.direcao = -1;
    this.proximaBicada = scene.time.now + Phaser.Math.Between(800, 2400);
    this.play(`${tipo}-andar`);
  }

  get perigoso() {
    return this.estado === 'andando' || this.estado === 'bicando';
  }

  atualizar(agora) {
    if (!this.active || !this.body) return;
    const corpo = this.body;
    if (this.estado === 'andando') {
      const noChao = corpo.blocked.down;
      const frenteX = this.x + this.direcao * (this.cfg.corpo.largura / 2 + 2);
      const chaoFrente = this.camada.getTileAtWorldXY(frenteX, this.y + 4);
      const bateu = (this.direcao < 0 && corpo.blocked.left) || (this.direcao > 0 && corpo.blocked.right);
      if (bateu || (noChao && !chaoFrente)) this.direcao *= -1;
      corpo.setVelocityX(this.cfg.velocidade * this.direcao);
      // o pombo para de vez em quando para bicar o chão
      if (this.tipo === 'pombo' && agora > this.proximaBicada) {
        this.estado = 'bicando';
        corpo.setVelocityX(0);
        this.play('pombo-bicar');
        this.scene.time.delayedCall(700, () => {
          if (this.estado !== 'bicando') return;
          this.estado = 'andando';
          this.play('pombo-andar');
          this.proximaBicada = this.scene.time.now + Phaser.Math.Between(1500, 3500);
        });
      }
    } else if (this.estado === 'bicando' || this.estado === 'dormindo' || this.estado === 'comendo') {
      corpo.setVelocityX(0);
    }
    // os desenhos: capivara olha para a direita, pombo para a esquerda
    this.setFlipX(this.tipo === 'pombo' ? this.direcao > 0 : this.direcao < 0);
  }

  // Pisão do herói.
  pisado() {
    if (!this.perigoso) return;
    this.scene.tweens.add({ targets: this, scaleY: 0.7, scaleX: 1.15, duration: 80, yoyo: true });
    if (this.cfg.sono) {
      this.estado = 'dormindo';
      this.body.setVelocityX(0);
      this.play('capivara-dormir');
      this.balao('zzz', true);
    } else {
      this.voarEmbora();
    }
  }

  // Pegou um pão de queijo: come feliz e vai embora.
  comer(deOndeX) {
    if (!this.perigoso) return;
    this.estado = 'comendo';
    this.direcao = deOndeX < this.x ? -1 : 1;
    this.body.setVelocityX(0);
    this.play(`${this.tipo}-comer`);
    this.balao('nham!', false);
    this.scene.time.delayedCall(1300, () => {
      if (!this.active) return;
      if (this.tipo === 'pombo') {
        this.voarEmbora();
        return;
      }
      this.estado = 'indo';
      this.direcao *= -1;
      this.play('capivara-andar');
      this.anims.timeScale = 1.5;
      this.body.setVelocityX(40 * this.direcao);
      this.scene.tweens.add({ targets: this, alpha: 0, delay: 1800, duration: 600, onComplete: () => this.destroy() });
    });
  }

  voarEmbora() {
    this.estado = 'voando';
    this.body.setAllowGravity(false);
    this.body.checkCollision.none = true;
    this.play('pombo-voar');
    const dir = Math.random() < 0.5 ? -1 : 1;
    this.setFlipX(dir > 0);
    this.body.setVelocity(90 * dir, -120);
    this.scene.tweens.add({ targets: this, alpha: 0, delay: 1200, duration: 500, onComplete: () => this.destroy() });
  }

  balao(texto, repetir) {
    const t = this.scene.add
      .text(this.x + 6, this.y - 26, texto, { fontFamily: FONTES.dialogo, fontSize: '13px', color: CORES_CSS.branco })
      .setOrigin(0.5)
      .setDepth(this.depth + 1)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
    if (repetir) this.scene.tweens.add({ targets: t, y: t.y - 8, alpha: 0.3, duration: 1100, yoyo: true, repeat: -1 });
    else this.scene.tweens.add({ targets: t, y: t.y - 14, alpha: 0, delay: 400, duration: 700, onComplete: () => t.destroy() });
  }
}
