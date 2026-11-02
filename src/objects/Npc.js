import * as Phaser from 'phaser';

// Personagem que conversa (Fase 2). Fica ensaiando no lugar, vira para o lado do jogador e mostra um
// balãozinho "..." enquanto ainda tem algo a dizer. Não tem física: a conversa é disparada pela distância.
export class Npc extends Phaser.GameObjects.Sprite {
  // id = chave da textura e das animações ('jasmine', 'genio'...). x,y = pé do personagem.
  constructor(scene, x, y, id) {
    super(scene, x, y, id, 0);
    scene.add.existing(this);
    this.id = id;
    this.setOrigin(0.5, 1);
    this.falou = false;
    if (scene.anims.exists(`${id}-ensaio`)) this.play(`${id}-ensaio`);
    // o Gênio flutua
    if (id === 'genio') {
      scene.tweens.add({ targets: this, y: y - 4, duration: 900, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
    }
    this.balao = scene.add.sprite(x + 10, y - this.height + 8, 'balao', 0).setOrigin(0.5, 1).play('balao-pensando');
    scene.tweens.add({ targets: this.balao, y: this.balao.y - 3, duration: 600, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
  }

  setDepth(d) {
    super.setDepth(d);
    this.balao?.setDepth(d + 1);
    return this;
  }

  // Desenhado olhando para a direita: vira quando o jogador está à esquerda.
  olharPara(x) {
    this.setFlipX(x < this.x);
  }

  // Depois de falar, o balãozinho some.
  jaFalou() {
    this.falou = true;
    const balao = this.balao;
    if (!balao) return;
    this.balao = null;
    this.scene.tweens.killTweensOf(balao);
    this.scene.tweens.add({ targets: balao, alpha: 0, scale: 0.5, duration: 200, onComplete: () => balao.destroy() });
  }
}
