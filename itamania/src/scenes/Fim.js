import * as Phaser from 'phaser';
import { LARGURA, CORES_CSS, FONTES } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { Botao } from '../ui/Botao.js';
import { fundoCidade } from '../ui/fundoCidade.js';
import { heroi } from '../genero.js';
import { tocarMusica } from '../audio/musica.js';

// Por enquanto o jogo vai até a fase 4: esta tela fecha o Ato 1 e traz a dedicatória.
export class Fim extends Phaser.Scene {
  constructor() {
    super('Fim');
  }

  create() {
    this.mover = fundoCidade(this, ['#F2A05A', '#F4B070', '#F6C088', '#F8D0A0', '#FAE0BC', '#FCEED6']);
    tocarMusica('titulo');
    const estilo = (tam, cor = CORES_CSS.branco) => ({ fontFamily: FONTES.titulo, fontSize: tam, color: cor, align: 'center' });
    this.add.text(LARGURA / 2, 40, TEXTOS.final.obrigado, estilo('14px', CORES_CSS.amarelo)).setOrigin(0.5).setStroke(CORES_CSS.roxo, 5);
    this.add
      .text(LARGURA / 2, 66, TEXTOS.final.detalhe, { fontFamily: FONTES.dialogo, fontSize: '16px', color: CORES_CSS.branco })
      .setOrigin(0.5)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
    this.add.sprite(LARGURA / 2, 186, `heroi-${heroi()}-normal`, 0).setOrigin(0.5, 1).setScale(2).play(`${heroi()}-normal-b-vitoria`);
    this.add
      .text(LARGURA / 2, 100, 'Dedicado a Geraldo e Helena', { fontFamily: FONTES.dialogo, fontSize: '18px', color: CORES_CSS.amareloClaro })
      .setOrigin(0.5)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
    new Botao(this, LARGURA / 2 - 70, 226, TEXTOS.botoes.mapa, () => this.scene.start('Mapa'), { largura: 120, altura: 26, cor: 'amarelo' });
    new Botao(this, LARGURA / 2 + 70, 226, 'INÍCIO', () => this.scene.start('Titulo'), { largura: 120, altura: 26 });
  }

  update(t, d) {
    this.mover(d);
  }
}
