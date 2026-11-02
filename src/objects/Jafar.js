import * as Phaser from 'phaser';
import { CHEFE as C } from '../config.js';

// Jafar, o chefe da Fase 3 (design original e provisório: public/assets/sprites/jafar.png, gerar_elenco.py).
//
// Ciclo (constantes em config.js, CHEFE):
//   flutuando (vai de um lado para o outro, lá em cima, fora do alcance)
//   -> avisando (para e brilha: "vai atirar!")
//   -> lança 3 projéteis em leque na direção do jogador
//   -> descendo -> cansado (no chão, piscando: é a hora de acertar maçãs) -> subindo -> flutuando ...
// Só leva dano de maçã quando está cansado. A cena ouve os eventos 'lancar', 'cansou' e 'derrotado'.
export class Jafar extends Phaser.Physics.Arcade.Sprite {
  constructor(scene, x, vida = C.vida) {
    super(scene, x, C.alturaVoo, 'jafar', 0);
    scene.add.existing(this);
    scene.physics.add.existing(this);
    this.body.setAllowGravity(false);
    // quadro de 64x84 (Etapa 8A): a caixa cobre cabeça e tronco; a cauda de fumaça não conta
    this.body.setSize(22, 46).setOffset(27, 12);
    this.vida = vida;
    this.direcao = -1;
    this.estado = 'parado'; // até a luta começar
    this.ateMs = 0; // fim do estado atual (ms do relógio da cena)
    this.invencivelAte = 0;
    this.acertosNestaDescida = 0;
    this.yBase = C.alturaVoo; // y sem o balanço de flutuar
    this.play('jafar-flutuar');
  }

  get vulneravel() {
    return this.estado === 'cansado';
  }

  comecar(agora) {
    this.mudar('flutuando', agora + C.flutuarMs);
  }

  mudar(estado, ateMs = Infinity) {
    this.estado = estado;
    this.ateMs = ateMs;
  }

  // alvoX = x do jogador (para virar para ele e mirar o leque)
  atualizar(agora, delta, alvoX) {
    if (this.estado === 'parado' || this.estado === 'derrotado') return;
    const dt = delta / 1000;
    // a arte olha para a direita (como todo o elenco): espelha quando o jogador está à esquerda
    this.setFlipX(alvoX < this.x);

    switch (this.estado) {
      case 'flutuando': {
        this.x += this.direcao * C.velocidade * dt;
        if (this.x < C.limiteEsquerda) this.direcao = 1;
        if (this.x > C.limiteDireita) this.direcao = -1;
        this.y = this.yBase + Math.sin(agora / 260) * 4;
        if (agora >= this.ateMs) {
          this.mudar('avisando', agora + C.avisoMs);
          this.play('jafar-lancar');
        }
        break;
      }
      case 'avisando': {
        // pisca em amarelo, cada vez mais rápido, para dar tempo de fugir
        const piscar = Math.floor(agora / 90) % 2 === 0;
        if (piscar) this.setTint(0xf9fcbb);
        else this.clearTint();
        if (agora >= this.ateMs) {
          this.clearTint();
          this.emit('lancar', this.x, this.y - 18);
          this.mudar('lancou', agora + 350);
        }
        break;
      }
      case 'lancou':
        if (agora >= this.ateMs) this.descer();
        break;
      case 'cansado': {
        // pisca (ainda visível) enquanto está vulnerável
        this.setAlpha(Math.floor(agora / 110) % 2 === 0 ? 0.55 : 1);
        if (agora >= this.ateMs) this.subir();
        break;
      }
      default:
        break; // descendo / subindo: quem anda é o tween
    }
  }

  descer() {
    this.mudar('descendo');
    this.play('jafar-tonto');
    this.scene.tweens.add({
      targets: this,
      y: C.alturaCansado,
      duration: C.descerMs,
      ease: 'Bounce.out',
      onComplete: () => {
        if (this.estado !== 'descendo') return;
        this.acertosNestaDescida = 0;
        this.mudar('cansado', this.scene.time.now + C.vulneravelMs);
        this.emit('cansou');
      },
    });
  }

  subir() {
    this.mudar('subindo');
    this.setAlpha(1);
    this.play('jafar-flutuar');
    this.scene.tweens.add({
      targets: this,
      y: C.alturaVoo,
      duration: C.descerMs,
      ease: 'Sine.inOut',
      onComplete: () => {
        if (this.estado !== 'subindo') return;
        this.yBase = C.alturaVoo;
        this.mudar('flutuando', this.scene.time.now + C.flutuarMs);
      },
    });
  }

  // Uma maçã encostou. Devolve 'acertou', 'derrotado' ou 'bateu' (não estava vulnerável).
  levarMaca(agora) {
    if (!this.vulneravel) return 'bateu';
    if (agora < this.invencivelAte) return 'ignorou';
    this.vida = Math.max(0, this.vida - 1);
    this.invencivelAte = agora + C.invencivelAcertoMs;
    this.acertosNestaDescida++;
    // pisca branco no acerto
    this.setTint(0xffffff).setTintMode(Phaser.TintModes.FILL);
    this.scene.time.delayedCall(90, () => this.active && this.clearTint());
    this.scene.tweens.add({ targets: this, scaleX: 1.15, scaleY: 0.88, duration: 70, yoyo: true });
    if (this.vida <= 0) {
      this.scene.tweens.killTweensOf(this);
      this.mudar('derrotado');
      this.setAlpha(1);
      this.emit('derrotado');
      return 'derrotado';
    }
    if (this.acertosNestaDescida >= C.acertosPorDescida) {
      // já apanhou bastante desta vez: volta para cima (sem esperar o tempo acabar)
      this.scene.time.delayedCall(250, () => this.estado === 'cansado' && this.subir());
    }
    return 'acertou';
  }
}
