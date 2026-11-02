import * as Phaser from 'phaser';
import { LARGURA, ALTURA, TILE, CORES, CORES_CSS, FONTES } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { Botao } from '../ui/Botao.js';
import { BotaoSom } from '../ui/BotaoSom.js';
import { Dialogo } from '../ui/Dialogo.js';
import { fundoEntardecer } from '../ui/fundo.js';
import { tocarMusica } from '../audio/musica.js';
import { PRIMEIRA_FASE } from '../fluxo.js';

// Intro (CLAUDE.md, seção 11.2): 3 caixas de texto. PRÓXIMO (ou tocar em qualquer lugar) avança; PULAR vai direto para a fase.
export class Intro extends Phaser.Scene {
  constructor() {
    super('Intro');
  }

  create() {
    const t = TEXTOS.intro;
    this.cameras.main.fadeIn(250, 158, 158, 255);
    this.morros = fundoEntardecer(this);
    const chao = ALTURA - TILE * 2;

    // cartaz do espetáculo num poste (original, nas cores da escola)
    const cartaz = this.add.container(300, chao);
    cartaz.add(this.add.rectangle(0, -40, 4, 80, 0x7a4a2a).setOrigin(0.5));
    cartaz.add(this.add.rectangle(0, -96, 92, 64, CORES.rosa).setStrokeStyle(3, CORES.roxo));
    cartaz.add(this.add.text(0, -108, 'ALADDIN', { fontFamily: FONTES.titulo, fontSize: '10px', color: CORES_CSS.roxo }).setOrigin(0.5));
    cartaz.add(this.add.text(0, -88, '20/11', { fontFamily: FONTES.titulo, fontSize: '12px', color: CORES_CSS.branco }).setOrigin(0.5).setStroke(CORES_CSS.roxo, 3));
    cartaz.add(this.add.text(0, -72, 'Teatro G9', { fontFamily: FONTES.dialogo, fontSize: '13px', color: CORES_CSS.roxo }).setOrigin(0.5));

    // Aladdin entra andando pela esquerda e para perto do cartaz
    this.aladdin = this.add.sprite(-20, chao, 'jogador').setOrigin(0.5, 1).play('correndo');
    this.tweens.add({
      targets: this.aladdin,
      x: 230,
      duration: 1400,
      onComplete: () => this.aladdin.play('parado'),
    });

    tocarMusica('titulo'); // continua a música do Título (se já estiver tocando, não reinicia)
    // caixas em HTML (ui/Dialogo.js): tocar em qualquer lugar ou espaço/Enter avança; no fim, vai para a fase
    this.dialogo = new Dialogo(this);
    this.dialogo.mostrar(t.caixas.map((texto) => ({ texto }))).then(() => this.seguir());

    // PRÓXIMO (principal, rosa) ao lado de PULAR: tocar em qualquer lugar também avança, mas o botão deixa claro
    // o que fazer. Na última caixa ele vira COMEÇAR.
    this.botaoProximo = new Botao(this, LARGURA - 202, ALTURA - 18, `${t.proximo} >`, () => this.dialogo.avancar(), {
      largura: 116,
      altura: 24,
      cor: 'rosa',
    });
    new Botao(this, LARGURA - 72, ALTURA - 18, `${t.pular} >>`, () => this.seguir(), { largura: 116, altura: 24 });
    new BotaoSom(this, LARGURA - 20, ALTURA - 52);

    this.input.keyboard?.on('keydown-ESC', () => this.seguir());
  }

  seguir() {
    if (this.saindo) return;
    this.saindo = true;
    this.cameras.main.fadeOut(250, 158, 158, 255);
    this.cameras.main.once('camerafadeoutcomplete', () => this.scene.start(PRIMEIRA_FASE));
  }

  update(_, delta) {
    this.morros.tilePositionX += delta * 0.006;
    const ultima = this.dialogo.caixas && this.dialogo.indice >= this.dialogo.caixas.length - 1;
    const rotulo = ultima ? `${TEXTOS.intro.comecar} >` : `${TEXTOS.intro.proximo} >`;
    if (this.botaoProximo.texto.text !== rotulo) this.botaoProximo.texto.setText(rotulo);
  }
}
