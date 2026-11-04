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
    const titulo = this.tituloColorido(LARGURA / 2, 36);
    this.tweens.add({ targets: titulo, y: 40, duration: 1400, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
    this.add
      .text(LARGURA / 2, 64, TEXTOS.subtitulo, { fontFamily: FONTES.dialogo, fontSize: '17px', color: CORES_CSS.branco })
      .setOrigin(0.5)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
    this.add
      .text(LARGURA / 2, 82, TEXTOS.escolha, { fontFamily: FONTES.titulo, fontSize: '8px', color: CORES_CSS.branco })
      .setOrigin(0.5)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);

    // cartões dos dois heróis
    this.escolhido = estado.heroi || 'geraldo';
    this.cartoes = {};
    Object.keys(HEROIS).forEach((chave, i) => {
      const x = LARGURA / 2 + (i === 0 ? -62 : 62);
      const fundo = this.add.rectangle(x, 151, 104, 116, CORES.roxo, 0.55).setStrokeStyle(3, CORES.branco);
      const s = this.add.sprite(x, 189, `heroi-${chave}-normal`, 0).setOrigin(0.5, 1).setScale(2);
      s.play(`${chave}-normal-s-parado`);
      const nome = this.add
        .text(x, 200, HEROIS[chave].nome.toUpperCase(), { fontFamily: FONTES.titulo, fontSize: '9px', color: CORES_CSS.branco })
        .setOrigin(0.5);
      fundo.setInteractive({ useHandCursor: true }).on('pointerup', () => this.escolher(chave));
      this.cartoes[chave] = { fundo, s, nome };
    });
    this.escolher(this.escolhido, true);

    if (temProgresso()) {
      new Botao(this, LARGURA / 2 - 72, 234, TEXTOS.botoes.continuar, () => this.continuar(), { largura: 130, altura: 26, cor: 'amarelo' });
      new Botao(this, LARGURA / 2 + 72, 234, TEXTOS.botoes.novo, () => this.jogar(), { largura: 130, altura: 26 });
    } else {
      new Botao(this, LARGURA / 2, 234, TEXTOS.botoes.jogar, () => this.jogar(), { largura: 150, altura: 28, cor: 'amarelo', tamanhoFonte: '10px' });
    }
    new BotaoSom(this, LARGURA - 20, 20);
    // crédito obrigatório da licença do Modern Exteriors (arte da praça)
    this.add.rectangle(0, ALTURA - 14, LARGURA, 14, CORES.roxo, 0.75).setOrigin(0);
    this.add
      .text(LARGURA / 2, ALTURA - 8, TEXTOS.creditos, { fontFamily: FONTES.dialogo, fontSize: '12px', color: CORES_CSS.branco })
      .setOrigin(0.5);
    this.input.keyboard?.on('keydown-LEFT', () => this.escolher('geraldo'));
    this.input.keyboard?.on('keydown-RIGHT', () => this.escolher('helena'));
    this.input.keyboard?.on('keydown-ENTER', () => this.jogar());
    this.cameras.main.fadeIn(300);
  }

  // "ITAMANIA" com uma cor por letra, como no topo do mapa do Pedro (referencias/mapa-mundi-original.png):
  // vermelho, amarelo, verde e azul, repetidos. Cada letra tem o tom claro em cima, contorno escuro e sombra em
  // degrau (cópias deslocadas 1 px por vez, sem desfoque).
  tituloColorido(x, y) {
    const CORES_LETRAS = [
      ['#FF7464', '#D83828'], // vermelho
      ['#FFFF74', '#F8D038'], // amarelo
      ['#84F484', '#48B848'], // verde
      ['#74B4FF', '#3878E8'], // azul
    ];
    const CONTORNO = '#181420';
    const SOMBRA = '#425772';
    const letras = [...TEXTOS.jogo];
    const tam = 30;
    const passo = tam + 2;
    const estilo = { fontFamily: FONTES.titulo, fontSize: `${tam}px`, color: '#FFFFFF' };
    const grupo = this.add.container(x, y);
    letras.forEach((ch, i) => {
      const lx = (i - (letras.length - 1) / 2) * passo;
      for (let d = 4; d >= 1; d--) {
        grupo.add(this.add.text(lx + d, d, ch, { ...estilo, color: SOMBRA }).setOrigin(0.5).setStroke(SOMBRA, 6));
      }
      const t = this.add.text(lx, 0, ch, estilo).setOrigin(0.5).setStroke(CONTORNO, 6);
      const [claro, base] = CORES_LETRAS[i % CORES_LETRAS.length];
      // corte seco entre o tom claro (terço de cima) e o tom base, como no pixel art
      const grad = t.context.createLinearGradient(0, 0, 0, t.height);
      grad.addColorStop(0, claro);
      grad.addColorStop(0.42, claro);
      grad.addColorStop(0.42, base);
      grad.addColorStop(1, base);
      t.setFill(grad);
      grupo.add(t);
    });
    return grupo;
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
    this.cameras.main.once('camerafadeoutcomplete', () => this.scene.start('Praca'));
  }

  continuar() {
    estado.heroi = this.escolhido;
    this.scene.start('Praca');
  }

  update(t, delta) {
    this.mover(delta);
  }
}
