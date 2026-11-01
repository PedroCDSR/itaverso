import { CORES, FONTES } from '../config.js';
import { tocarEfeito } from '../audio/efeitos.js';

// Botão de menu: retângulo na paleta da escola com texto em Press Start 2P.
// A ação roda no "pointerup" (dedo saindo da tela): é o único momento em que o navegador aceita
// abrir link, compartilhar ou entrar em tela cheia. A área de toque é um pouco maior que o desenho.
//
// opcoes: { largura, altura, cor: 'rosa' | 'lilas' | 'amarelo' | 'branco', tamanhoFonte }
export class Botao {
  constructor(scene, x, y, rotulo, acao, opcoes = {}) {
    const { largura = 180, altura = 30, cor = 'lilas', tamanhoFonte = '8px' } = opcoes;
    this.scene = scene;
    this.acao = acao;
    this.container = scene.add.container(x, y).setScrollFactor(0);
    const sombra = scene.add.rectangle(2, 2, largura, altura, CORES.roxo).setAlpha(0.6);
    this.fundo = scene.add.rectangle(0, 0, largura, altura, CORES[cor]).setStrokeStyle(2, CORES.roxo);
    this.texto = scene.add
      .text(0, 1, rotulo, { fontFamily: FONTES.titulo, fontSize: tamanhoFonte, color: '#3A2F7A', align: 'center' })
      .setOrigin(0.5);
    this.container.add([sombra, this.fundo, this.texto]);
    this.container.setSize(largura + 8, altura + 8);
    this.container.setInteractive({ useHandCursor: true });

    this.apertado = false;
    this.container.on('pointerdown', () => {
      this.apertado = true;
      this.fundo.setPosition(1, 1);
      this.texto.setPosition(1, 2);
    });
    this.container.on('pointerout', () => this.soltarVisual());
    this.container.on('pointerup', () => {
      const valeu = this.apertado;
      this.soltarVisual();
      if (!valeu || !this.container.visible) return;
      tocarEfeito('botao');
      this.acao();
    });
  }

  soltarVisual() {
    this.apertado = false;
    this.fundo.setPosition(0, 0);
    this.texto.setPosition(0, 1);
  }

  setRotulo(t) {
    this.texto.setText(t);
    return this;
  }

  setVisible(v) {
    this.container.setVisible(v);
    if (v) this.container.setInteractive();
    else this.container.disableInteractive();
    return this;
  }

  setDepth(d) {
    this.container.setDepth(d);
    return this;
  }
}
