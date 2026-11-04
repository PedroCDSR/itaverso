import * as Phaser from 'phaser';
import { ControlesToque } from './ControlesToque.js';

const K = Phaser.Input.Keyboard.KeyCodes;

// Junta teclado e toque num só lugar. As cenas leem só daqui:
//   entrada.esquerda / direita / pular (segurando)
//   entrada.pularApertou / macaApertou (só no quadro em que apertou)
//   entrada.segurando (tapete: qualquer dedo na tela, espaço ou seta para cima)
export class Entrada {
  constructor(scene) {
    this.scene = scene;
    this.toque = new ControlesToque(scene);
    const kb = scene.input.keyboard;
    this.teclas = kb
      ? {
          esquerda: [kb.addKey(K.LEFT), kb.addKey(K.A)],
          direita: [kb.addKey(K.RIGHT), kb.addKey(K.D)],
          pular: [kb.addKey(K.SPACE), kb.addKey(K.W), kb.addKey(K.UP)],
          maca: [kb.addKey(K.X), kb.addKey(K.J)],
        }
      : { esquerda: [], direita: [], pular: [], maca: [] };
    this.antes = { pular: false, maca: false };
    this.zerar();
  }

  zerar() {
    this.esquerda = this.direita = this.pular = this.maca = this.segurando = false;
    this.pularApertou = this.macaApertou = false;
  }

  // Depois de fechar um diálogo: um botão que ainda está apertado só vale de novo depois de solto
  // (senão o toque/tecla que fechou a caixa viraria um pulo no quadro seguinte).
  ignorarAteSoltar() {
    this.antes.pular = true;
    this.antes.maca = true;
  }

  setModoTapete(ligado) {
    this.toque.setModoTapete(ligado);
  }

  // Chamar no começo do update() da cena.
  atualizar() {
    const t = this.toque.atualizar();
    const algum = (lista) => lista.some((k) => k.isDown);
    this.esquerda = t.esquerda || algum(this.teclas.esquerda);
    this.direita = t.direita || algum(this.teclas.direita);
    // apertar os dois lados ao mesmo tempo = ficar parado
    if (this.esquerda && this.direita) this.esquerda = this.direita = false;
    this.pular = t.pular || algum(this.teclas.pular);
    this.maca = t.maca || algum(this.teclas.maca);
    this.segurando = t.segurando || algum(this.teclas.pular);

    // "apertou agora" = está apertado neste quadro e não estava no anterior
    this.pularApertou = this.pular && !this.antes.pular;
    this.macaApertou = this.maca && !this.antes.maca;
    this.antes.pular = this.pular;
    this.antes.maca = this.maca;
  }
}
