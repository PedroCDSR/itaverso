import * as Phaser from 'phaser';
import { LARGURA, ALTURA, CORES, CORES_CSS, FONTES, JOGADOR } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { Entrada } from '../ui/Entrada.js';
import { BotaoSom } from '../ui/BotaoSom.js';
import { tentarTelaCheia } from '../ui/telaCheia.js';
import { bipe } from '../audio/som.js';

// Cena de teste da Etapa 1: um bloco que anda, pula e joga "maçãs", para sentir os controles no celular.
// O Aladdin de verdade (física com pulo variável, coyote time, arte) entra na Etapa 2.
export class Teste extends Phaser.Scene {
  constructor() {
    super('Teste');
  }

  create() {
    const t = TEXTOS.teste;
    this.jogando = false;

    // chão e duas plataformas para pular
    this.chao = this.physics.add.staticGroup();
    const bloco = (x, y, w, h) => this.chao.add(this.add.rectangle(x, y, w, h, CORES.roxo).setOrigin(0));
    bloco(0, ALTURA - 24, LARGURA, 24);
    bloco(150, 170, 70, 10);
    bloco(270, 130, 70, 10);

    // "jogador" provisório: retângulo do tamanho útil do personagem (24x40)
    this.jogador = this.add.rectangle(60, ALTURA - 60, 24, 40, CORES.rosa).setStrokeStyle(2, CORES.roxo);
    this.physics.add.existing(this.jogador);
    this.jogador.body.setCollideWorldBounds(true);
    this.physics.add.collider(this.jogador, this.chao);
    this.olhandoDireita = true;

    this.macas = this.physics.add.group();
    this.physics.add.collider(this.macas, this.chao, (m) => m.destroy());

    this.entrada = new Entrada(this);
    new BotaoSom(this, LARGURA - 20, 20);

    this.add
      .text(LARGURA / 2, 16, t.subtitulo, { fontFamily: FONTES.titulo, fontSize: '8px', color: CORES_CSS.roxo })
      .setOrigin(0.5);
    if (!this.sys.game.device.input.touch) {
      this.add
        .text(LARGURA / 2, ALTURA - 12, t.dicaTeclado, { fontFamily: FONTES.dialogo, fontSize: '12px', color: CORES_CSS.branco })
        .setOrigin(0.5);
    }

    this.criarTelaJogar();
  }

  // Tela inicial com o botão JOGAR: o toque nele libera o som e pede tela cheia (Android).
  criarTelaJogar() {
    const t = TEXTOS.teste;
    const tela = this.add.container(0, 0).setDepth(2000);
    tela.add(this.add.rectangle(0, 0, LARGURA, ALTURA, CORES.lilas, 0.92).setOrigin(0));
    tela.add(
      this.add
        .text(LARGURA / 2, 70, t.titulo, { fontFamily: FONTES.titulo, fontSize: '24px', color: CORES_CSS.branco })
        .setOrigin(0.5)
        .setShadow(2, 2, CORES_CSS.roxo, 0, false, true),
    );
    const botao = this.add.rectangle(LARGURA / 2, 150, 140, 40, CORES.rosa).setStrokeStyle(3, CORES.roxo);
    tela.add(botao);
    tela.add(
      this.add
        .text(LARGURA / 2, 151, TEXTOS.botoes.jogar, { fontFamily: FONTES.titulo, fontSize: '16px', color: CORES_CSS.roxo })
        .setOrigin(0.5),
    );
    tela.add(
      this.add
        .text(LARGURA / 2, 200, t.tocarJogar, { fontFamily: FONTES.dialogo, fontSize: '16px', color: CORES_CSS.roxo })
        .setOrigin(0.5),
    );
    botao.setInteractive({ useHandCursor: true });
    // pointerup (e não pointerdown): o navegador só aceita tela cheia quando o dedo sai da tela
    botao.on('pointerup', () => this.comecar(tela));
    this.input.keyboard?.once('keydown-ENTER', () => this.comecar(tela));
  }

  comecar(tela) {
    if (this.jogando) return;
    tentarTelaCheia(this);
    bipe(520, 0.12);
    tela.destroy();
    this.jogando = true;
  }

  update() {
    const e = this.entrada;
    e.atualizar();
    if (!this.jogando) return;

    const corpo = this.jogador.body;
    if (e.esquerda) {
      corpo.setVelocityX(-JOGADOR.velocidade);
      this.olhandoDireita = false;
    } else if (e.direita) {
      corpo.setVelocityX(JOGADOR.velocidade);
      this.olhandoDireita = true;
    } else {
      corpo.setVelocityX(0);
    }

    if (e.pularApertou && corpo.blocked.down) {
      corpo.setVelocityY(-JOGADOR.forcaPulo);
      bipe(660, 0.08);
    }
    // soltar o pulo cedo corta a subida (prévia do pulo variável da Etapa 2)
    if (!e.pular && corpo.velocity.y < 0) corpo.setVelocityY(corpo.velocity.y * JOGADOR.cortePulo);

    if (e.macaApertou) {
      const dir = this.olhandoDireita ? 1 : -1;
      const m = this.add.circle(this.jogador.x + 14 * dir, this.jogador.y - 10, 5, CORES.amarelo).setStrokeStyle(1, CORES.roxo);
      this.macas.add(m);
      m.body.setCircle(5).setVelocity(220 * dir, -160);
      this.time.delayedCall(2000, () => m.active && m.destroy());
      bipe(880, 0.05);
    }
  }
}
