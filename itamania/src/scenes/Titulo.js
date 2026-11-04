import * as Phaser from 'phaser';
import { LARGURA, ALTURA, CORES, CORES_CSS, FONTES } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { Botao } from '../ui/Botao.js';
import { BotaoSom } from '../ui/BotaoSom.js';
import { fundoCidade } from '../ui/fundoCidade.js';
import { tocarMusica } from '../audio/musica.js';
import { estado } from '../estado.js';

// Entrada da versão de desenvolvimento: capivara exploradora e acesso direto à praça.
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
      .text(LARGURA / 2, 82, TEXTOS.praca.chamada, { fontFamily: FONTES.titulo, fontSize: '8px', color: CORES_CSS.branco })
      .setOrigin(0.5)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);

    // A praça de desenvolvimento começa com a capivara escolhida pelo Pedro.
    this.escolhido = estado.heroi || 'geraldo';
    this.add.rectangle(LARGURA / 2, 151, 250, 116, CORES.roxo, 0.65).setStrokeStyle(2, CORES.amarelo);
    this.add.sprite(LARGURA / 2, 178, 'capivara-exploradora', 0)
      .setOrigin(0.5, 1).setDisplaySize(76, 76).play('exploradora-parado-baixo');
    this.add.text(LARGURA / 2, 190, TEXTOS.praca.personagem, {
      fontFamily: FONTES.titulo, fontSize: '8px', color: CORES_CSS.amarelo,
    }).setOrigin(0.5);
    this.add.text(LARGURA / 2, 204, TEXTOS.praca.apresentacao, {
      fontFamily: FONTES.dialogo, fontSize: '13px', color: CORES_CSS.branco,
    }).setOrigin(0.5);
    new Botao(this, LARGURA / 2, 234, TEXTOS.praca.explorar, () => this.continuar(), {
      largura: 250, altura: 28, cor: 'amarelo', tamanhoFonte: '9px',
    });
    new BotaoSom(this, LARGURA - 20, 20);
    // crédito obrigatório da licença do Modern Exteriors (arte da praça)
    this.add.rectangle(0, ALTURA - 14, LARGURA, 14, CORES.roxo, 0.75).setOrigin(0);
    this.add
      .text(LARGURA / 2, ALTURA - 8, TEXTOS.creditos, { fontFamily: FONTES.dialogo, fontSize: '12px', color: CORES_CSS.branco })
      .setOrigin(0.5);
    this.input.keyboard?.on('keydown-ENTER', () => this.continuar());
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

  continuar() {
    estado.heroi = this.escolhido;
    this.scene.start('Praca');
  }

  update(t, delta) {
    this.mover(delta);
  }
}
