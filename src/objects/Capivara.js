import * as Phaser from 'phaser';
import { CAPIVARA as C, CORES_CSS, FONTES } from '../config.js';
import { TEXTOS } from '../data/textos.js';

// Capivara de Itajubá: fofa e trapalhona, nunca assustadora (CLAUDE.md, seção 8).
//
// Estados:
//   'andando'   anda devagar de um lado para o outro e vira na parede ou na beirada; encostar de lado tira 1 coração
//   'dormindo'  levou um pisão: deita e dorme com "zzz" (não machuca mais)
//   'comendo'   levou uma maçã: senta e come feliz, depois vai embora devagar (não machuca mais)
export class Capivara extends Phaser.Physics.Arcade.Sprite {
  constructor(scene, x, y, camada) {
    super(scene, x, y, 'capivara', 0);
    scene.add.existing(this);
    scene.physics.add.existing(this);
    this.camada = camada;
    this.setOrigin(0.5, 1);
    this.body.setSize(C.corpo.largura, C.corpo.altura).setOffset(C.corpo.x, C.corpo.y);
    this.estado = 'andando';
    this.direcao = -1; // começa andando na direção do jogador
    this.play('capivara-andar');
  }

  get perigosa() {
    return this.estado === 'andando';
  }

  atualizar() {
    if (!this.active) return;
    const corpo = this.body;
    if (this.estado === 'andando') {
      // vira ao bater numa parede ou ao chegar na beirada (olha o tile logo à frente, embaixo dos pés)
      const noChao = corpo.blocked.down;
      const frenteX = this.x + this.direcao * (C.corpo.largura / 2 + 2);
      const chaoFrente = this.camada.getTileAtWorldXY(frenteX, this.y + 4);
      const bateu = (this.direcao < 0 && corpo.blocked.left) || (this.direcao > 0 && corpo.blocked.right);
      if (bateu || (noChao && !chaoFrente)) this.direcao *= -1;
      corpo.setVelocityX(C.velocidade * this.direcao);
    } else if (this.estado === 'indo') {
      corpo.setVelocityX(C.velocidadeIndoEmbora * this.direcao);
    } else {
      corpo.setVelocityX(0);
    }
    // o desenho olha para a direita
    this.setFlipX(this.direcao < 0);
  }

  // Pisão do jogador: dorme.
  dormir() {
    if (!this.perigosa) return;
    this.estado = 'dormindo';
    this.body.setVelocityX(0);
    this.play('capivara-dormir');
    // achata e volta, para o pisão "ter peso"
    this.scene.tweens.add({ targets: this, scaleY: 0.7, scaleX: 1.15, duration: 80, yoyo: true });
    this.balao(TEXTOS.itajuba.zzz, true);
  }

  // Levou uma maçã: come feliz e depois vai embora.
  comer(deOndeX) {
    if (!this.perigosa) return;
    this.estado = 'comendo';
    this.direcao = deOndeX < this.x ? -1 : 1; // vira para quem jogou a maçã
    this.body.setVelocityX(0);
    this.play('capivara-comer');
    this.balao(TEXTOS.itajuba.nham, false);
    this.scene.time.delayedCall(C.comendoSeg * 1000, () => {
      if (!this.active) return;
      this.estado = 'indo';
      this.direcao *= -1; // vai para o outro lado, devagar
      this.play('capivara-andar');
      this.anims.timeScale = 1.5;
      this.scene.tweens.add({ targets: this, alpha: 0, delay: 2200, duration: 600, onComplete: () => this.destroy() });
    });
  }

  // Texto pequeno acima da cabeça ("zzz" fica flutuando; "nham!" sobe e some).
  balao(texto, repetir) {
    const t = this.scene.add
      .text(this.x + 6, this.y - 26, texto, { fontFamily: FONTES.dialogo, fontSize: '13px', color: CORES_CSS.branco })
      .setOrigin(0.5)
      .setDepth(this.depth + 1)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
    if (repetir) {
      this.scene.tweens.add({ targets: t, y: t.y - 8, alpha: 0.3, duration: 1100, yoyo: true, repeat: -1 });
    } else {
      this.scene.tweens.add({ targets: t, y: t.y - 14, alpha: 0, delay: 400, duration: 700, onComplete: () => t.destroy() });
    }
  }
}
