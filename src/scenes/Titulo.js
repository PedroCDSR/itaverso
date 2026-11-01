import * as Phaser from 'phaser';
import { LARGURA, ALTURA, TILE, CORES, CORES_CSS, FONTES } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { EVENTO } from '../data/evento.js';
import { TEM_LOGO } from '../art/index.js';
import { Botao } from '../ui/Botao.js';
import { BotaoSom } from '../ui/BotaoSom.js';
import { fundoEntardecer } from '../ui/fundo.js';
import { novaPartida } from '../estado.js';

// Tela de título (CLAUDE.md, seção 11.1): logo, nome do jogo, JOGAR e SOBRE O ESPETÁCULO.
export class Titulo extends Phaser.Scene {
  constructor() {
    super('Titulo');
  }

  create() {
    const t = TEXTOS.titulo;
    this.morros = fundoEntardecer(this);
    const cx = LARGURA / 2;

    // logo da escola (PNG) ou, enquanto ele não existe, o nome da escola em texto
    if (TEM_LOGO && this.textures.exists('logo')) {
      const logo = this.add.image(cx, 26, 'logo');
      logo.setScale(Math.min(140 / logo.width, 36 / logo.height));
    } else {
      this.add
        .text(cx, 24, EVENTO.escola, { fontFamily: FONTES.dialogo, fontSize: '20px', color: CORES_CSS.branco })
        .setOrigin(0.5)
        .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
    }

    this.add
      .text(cx, 66, t.jogo, { fontFamily: FONTES.titulo, fontSize: '32px', color: CORES_CSS.rosa })
      .setOrigin(0.5)
      .setStroke(CORES_CSS.roxo, 6)
      .setShadow(3, 3, '#3A2F7A', 0, true, true);
    this.add
      .text(cx, 96, t.subtitulo, { fontFamily: FONTES.dialogo, fontSize: '18px', color: CORES_CSS.amarelo })
      .setOrigin(0.5)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);

    // Aladdin parado ao lado dos botões
    this.add.sprite(70, ALTURA - TILE * 2, 'jogador').setOrigin(0.5, 1).play('parado');

    const jogar = new Botao(this, cx, 140, t.jogar, () => this.jogar(), { largura: 170, altura: 36, cor: 'rosa', tamanhoFonte: '16px' });
    this.tweens.add({ targets: jogar.container, scale: 1.05, yoyo: true, repeat: -1, duration: 600, ease: 'Sine.easeInOut' });
    new Botao(this, cx, 186, t.sobre, () => this.sobre(), { largura: 200, altura: 28, cor: 'lilas' });

    this.add
      .text(cx, ALTURA - 16, t.rodape, { fontFamily: FONTES.titulo, fontSize: '8px', color: CORES_CSS.branco })
      .setOrigin(0.5)
      .setShadow(1, 1, '#3A2F7A', 0, false, true);
    if (!this.sys.game.device.input.touch) {
      this.add
        .text(cx, 212, t.dicaTeclado, { fontFamily: FONTES.dialogo, fontSize: '13px', color: CORES_CSS.branco })
        .setOrigin(0.5)
        .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
    }

    new BotaoSom(this, LARGURA - 20, 20);
    this.input.keyboard?.on('keydown-ENTER', () => this.jogar());
    this.events.on('resume', () => this.input.keyboard?.resetKeys());
  }

  jogar() {
    if (!this.scene.isActive()) return;
    novaPartida(this);
    this.cameras.main.fadeOut(250, 158, 158, 255);
    this.cameras.main.once('camerafadeoutcomplete', () => this.scene.start('Intro'));
  }

  sobre() {
    this.scene.pause();
    this.scene.launch('Sobre', { de: this.scene.key });
  }

  update(_, delta) {
    this.morros.tilePositionX += delta * 0.006;
  }
}
