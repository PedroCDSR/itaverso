import * as Phaser from 'phaser';
import { LARGURA, ALTURA, CORES } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { criarCartaoEvento } from '../ui/CartaoEvento.js';
import { abrirIngressos, abrirInstagram } from '../ui/links.js';

// "Sobre o espetáculo": cartão do evento por cima da cena que chamou (Título ou Pausa).
// Quem chama pausa a si mesma e passa { de: <nome da cena> }; o VOLTAR retoma essa cena.
export class Sobre extends Phaser.Scene {
  constructor() {
    super('Sobre');
  }

  init(dados) {
    this.de = dados.de;
  }

  create() {
    const c = TEXTOS.cartao;
    this.add.rectangle(0, 0, LARGURA, ALTURA, CORES.lilas, 0.9).setOrigin(0).setInteractive(); // segura os toques
    criarCartaoEvento(this, {
      botoes: [
        { rotulo: c.ingressos, acao: abrirIngressos, cor: 'rosa' },
        { rotulo: c.instagram, acao: abrirInstagram },
        { rotulo: c.voltar, acao: () => this.voltar() },
      ],
    });
    this.input.keyboard?.once('keydown-ESC', () => this.voltar());
  }

  voltar() {
    this.scene.stop();
    if (this.de) this.scene.resume(this.de);
  }
}
