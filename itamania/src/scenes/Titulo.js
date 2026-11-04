import * as Phaser from 'phaser';
import { LARGURA, ALTURA, CORES, CORES_CSS, FONTES } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { Botao } from '../ui/Botao.js';
import { BotaoSom } from '../ui/BotaoSom.js';
import { fundoCidade } from '../ui/fundoCidade.js';
import { tocarMusica } from '../audio/musica.js';
import { tocarEfeito } from '../audio/efeitos.js';
import { estado, novoJogo, temProgresso } from '../estado.js';
import { HEROIS } from '../genero.js';

// Tela inicial: nome do jogo e a escolha entre Geraldo e Helena (homenagem aos avós do autor).
// Cada partida é só a história de quem foi escolhido.
export class Titulo extends Phaser.Scene {
  constructor() {
    super('Titulo');
  }

  create() {
    this.mover = fundoCidade(this);
    tocarMusica('titulo');
    const titulo = this.add
      .text(LARGURA / 2, 36, TEXTOS.jogo, { fontFamily: FONTES.titulo, fontSize: '30px', color: CORES_CSS.amarelo })
      .setOrigin(0.5)
      .setStroke(CORES_CSS.roxo, 6)
      .setShadow(3, 3, '#1A1A40', 0, true, true);
    this.tweens.add({ targets: titulo, y: 40, duration: 1400, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
    this.add
      .text(LARGURA / 2, 64, TEXTOS.subtitulo, { fontFamily: FONTES.dialogo, fontSize: '17px', color: CORES_CSS.branco })
      .setOrigin(0.5)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
    this.add
      .text(LARGURA / 2, 86, TEXTOS.escolha, { fontFamily: FONTES.titulo, fontSize: '8px', color: CORES_CSS.branco })
      .setOrigin(0.5)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);

    // cartões dos dois heróis
    this.escolhido = estado.heroi || 'geraldo';
    this.cartoes = {};
    Object.keys(HEROIS).forEach((chave, i) => {
      const x = LARGURA / 2 + (i === 0 ? -62 : 62);
      const fundo = this.add.rectangle(x, 150, 104, 100, CORES.roxo, 0.55).setStrokeStyle(3, CORES.branco);
      const s = this.add.sprite(x, 192, `heroi-${chave}-normal`, 0).setOrigin(0.5, 1).setScale(2);
      s.play(`${chave}-normal-s-parado`);
      const nome = this.add
        .text(x, 113, HEROIS[chave].nome.toUpperCase(), { fontFamily: FONTES.titulo, fontSize: '9px', color: CORES_CSS.branco })
        .setOrigin(0.5);
      fundo.setInteractive({ useHandCursor: true }).on('pointerup', () => this.escolher(chave));
      this.cartoes[chave] = { fundo, s, nome };
    });
    this.escolher(this.escolhido, true);

    if (temProgresso()) {
      new Botao(this, LARGURA / 2 - 72, 226, TEXTOS.botoes.continuar, () => this.continuar(), { largura: 130, altura: 26, cor: 'amarelo' });
      new Botao(this, LARGURA / 2 + 72, 226, TEXTOS.botoes.novo, () => this.jogar(), { largura: 130, altura: 26 });
    } else {
      new Botao(this, LARGURA / 2, 226, TEXTOS.botoes.jogar, () => this.jogar(), { largura: 150, altura: 28, cor: 'amarelo', tamanhoFonte: '10px' });
    }
    new BotaoSom(this, LARGURA - 20, 20);
    this.input.keyboard?.on('keydown-LEFT', () => this.escolher('geraldo'));
    this.input.keyboard?.on('keydown-RIGHT', () => this.escolher('helena'));
    this.input.keyboard?.on('keydown-ENTER', () => this.jogar());
    this.cameras.main.fadeIn(300);
  }

  escolher(chave, silencioso = false) {
    this.escolhido = chave;
    for (const [k, c] of Object.entries(this.cartoes)) {
      const sel = k === chave;
      c.fundo.setStrokeStyle(3, sel ? CORES.amarelo : CORES.branco).setFillStyle(CORES.roxo, sel ? 0.8 : 0.4);
      c.nome.setColor(sel ? CORES_CSS.amarelo : CORES_CSS.branco);
      c.s.play(`${k}-normal-s-${sel ? 'vitoria' : 'parado'}`, true);
    }
    if (!silencioso) tocarEfeito('botao');
  }

  jogar() {
    novoJogo(this.escolhido);
    this.cameras.main.fadeOut(300);
    this.cameras.main.once('camerafadeoutcomplete', () => this.scene.start('Fase', { fase: 1 }));
  }

  continuar() {
    estado.heroi = this.escolhido;
    this.scene.start('Mapa');
  }

  update(t, delta) {
    this.mover(delta);
  }
}
