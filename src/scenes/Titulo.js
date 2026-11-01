import * as Phaser from 'phaser';
import { LARGURA, ALTURA, TILE, CORES, CORES_CSS, FONTES } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { EVENTO } from '../data/evento.js';
import { TEM_LOGO } from '../art/index.js';
import { Botao } from '../ui/Botao.js';
import { BotaoSom } from '../ui/BotaoSom.js';
import { fundoEntardecer } from '../ui/fundo.js';
import { novaPartida } from '../estado.js';
import { tocarMusica } from '../audio/musica.js';
import { NIVEIS, aplicarDificuldade, dificuldade } from '../dificuldade.js';

// Tela de título (CLAUDE.md, seção 11.1): logo, nome do jogo, JOGAR e SOBRE O ESPETÁCULO.
export class Titulo extends Phaser.Scene {
  constructor() {
    super('Titulo');
  }

  create() {
    this.saindo = false;
    const t = TEXTOS.titulo;
    this.morros = fundoEntardecer(this);
    tocarMusica('titulo'); // começa no 1º toque (ou tecla), se o som estiver ligado
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

    const jogar = new Botao(this, cx, 140, t.jogar, () => this.mostrarNiveis(), { largura: 170, altura: 36, cor: 'rosa', tamanhoFonte: '16px' });
    this.tweens.add({ targets: jogar.container, scale: 1.05, yoyo: true, repeat: -1, duration: 600, ease: 'Sine.easeInOut' });
    const sobre = new Botao(this, cx, 186, t.sobre, () => this.sobre(), { largura: 200, altura: 28, cor: 'lilas' });
    this.menu = [jogar.container, sobre.container]; // some enquanto a escolha de dificuldade está aberta

    this.add
      .text(cx, ALTURA - 16, t.rodape, { fontFamily: FONTES.titulo, fontSize: '8px', color: CORES_CSS.branco })
      .setOrigin(0.5)
      .setShadow(1, 1, '#3A2F7A', 0, false, true);
    if (!this.sys.game.device.input.touch) {
      this.dica = this.add
        .text(cx, 212, t.dicaTeclado, { fontFamily: FONTES.dialogo, fontSize: '13px', color: CORES_CSS.branco })
        .setOrigin(0.5)
        .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
    }

    new BotaoSom(this, LARGURA - 20, 20);
    this.criarNiveis();
    // teclado: ENTER abre a escolha e depois confirma o nível destacado; 1, 2 e 3 escolhem direto; Esc volta
    this.input.keyboard?.on('keydown-ENTER', () => (this.escolhendo ? this.jogar(dificuldade()) : this.mostrarNiveis()));
    ['ONE', 'TWO', 'THREE'].forEach((tecla, i) =>
      this.input.keyboard?.on('keydown-' + tecla, () => this.escolhendo && this.jogar(Object.keys(NIVEIS)[i])),
    );
    this.input.keyboard?.on('keydown-ESC', () => this.esconderNiveis());
    this.events.on('resume', () => this.input.keyboard?.resetKeys());
  }

  // Escolha da dificuldade (src/dificuldade.js): 3 botões com uma dica curta ao lado de cada um.
  // O último nível escolhido neste aparelho aparece em rosa.
  criarNiveis() {
    const t = TEXTOS.titulo;
    const xb = 196;
    const itens = [
      this.add
        .text(LARGURA / 2, 122, t.escolha, { fontFamily: FONTES.titulo, fontSize: '8px', color: CORES_CSS.branco })
        .setOrigin(0.5)
        .setShadow(1, 1, '#3A2F7A', 0, false, true),
    ];
    this.botoesNivel = {};
    Object.keys(NIVEIS).forEach((nivel, i) => {
      const y = 146 + i * 32;
      const b = new Botao(this, xb, y, t.niveis[nivel].nome, () => this.jogar(nivel), { largura: 110, altura: 26, tamanhoFonte: '10px' });
      this.botoesNivel[nivel] = b;
      itens.push(
        b.container,
        this.add
          .text(xb + 64, y + 1, t.niveis[nivel].dica, { fontFamily: FONTES.dialogo, fontSize: '15px', color: CORES_CSS.branco })
          .setOrigin(0, 0.5)
          .setShadow(1, 1, CORES_CSS.roxo, 0, false, true),
      );
    });
    const voltar = new Botao(this, LARGURA - 52, ALTURA - 40, t.voltar, () => this.esconderNiveis(), { largura: 76, altura: 22 });
    itens.push(voltar.container);
    this.niveis = itens;
    this.escolhendo = false;
    itens.forEach((o) => o.setVisible(false));
  }

  mostrarNiveis() {
    if (!this.scene.isActive() || this.escolhendo) return;
    this.escolhendo = true;
    this.menu.forEach((o) => o.setVisible(false));
    this.dica?.setVisible(false);
    for (const [nivel, b] of Object.entries(this.botoesNivel)) b.fundo.setFillStyle(nivel === dificuldade() ? CORES.rosa : CORES.lilas);
    this.niveis.forEach((o) => o.setVisible(true));
  }

  esconderNiveis() {
    if (!this.escolhendo) return;
    this.escolhendo = false;
    this.niveis.forEach((o) => o.setVisible(false));
    this.menu.forEach((o) => o.setVisible(true));
    this.dica?.setVisible(true);
  }

  jogar(nivel) {
    if (!this.scene.isActive() || this.saindo) return;
    this.saindo = true;
    aplicarDificuldade(nivel);
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
