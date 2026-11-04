import * as Phaser from 'phaser';
import { LARGURA, CORES, CORES_CSS, FONTES } from '../config.js';
import { BotaoSom } from '../ui/BotaoSom.js';
import { BotaoPausa } from '../ui/BotaoPausa.js';
import { abrirPausa } from '../fluxo.js';

// HUD (cena por cima da fase): corações, itacoins e pães de queijo à esquerda; pausa e som à direita.
// Lê tudo do "registry" (vida, vidaMax, itacoins, mostrarItacoins, paes); a fase só muda os valores.
export class HUD extends Phaser.Scene {
  constructor() {
    super('HUD');
  }

  create() {
    const reg = this.registry;
    const estilo = { fontFamily: FONTES.titulo, fontSize: '8px', color: CORES_CSS.branco };
    const sombra = (t) => t.setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
    this.fundo = this.add.rectangle(6, 6, 100, 22, CORES.roxo, 0.45).setOrigin(0).setStrokeStyle(1, CORES.roxo, 0.8);
    this.coracoes = [];
    for (let i = 0; i < reg.get('vidaMax'); i++) this.coracoes.push(this.add.image(17 + i * 13, 17, 'coracao', 0));
    let x = 17 + reg.get('vidaMax') * 13 + 6;
    this.iconeMoeda = this.add.sprite(x, 17, 'itacoin', 0).play('itacoin-girar');
    this.txtMoedas = sombra(this.add.text(x + 9, 13, '', estilo));
    this.xPao = x + 48;
    this.iconePao = this.add.image(this.xPao, 17, 'paodequeijo', 0);
    this.txtPaes = sombra(this.add.text(this.xPao + 9, 13, '', estilo));
    new BotaoPausa(this, LARGURA - 56, 20, () => abrirPausa(this.scene.get('Fase')));
    this.botaoSom = new BotaoSom(this, LARGURA - 20, 20);
    this.events.on('resume', () => this.botaoSom.desenhar());
    this.antes = { itacoins: reg.get('itacoins'), paes: reg.get('paes') };
    this.atualizar();
    const aoMudar = () => this.atualizar();
    reg.events.on('changedata', aoMudar);
    this.events.once('shutdown', () => reg.events.off('changedata', aoMudar));
  }

  atualizar() {
    const reg = this.registry;
    const vida = reg.get('vida');
    this.coracoes.forEach((c, i) => c.setFrame(i < vida ? 0 : 1));
    const comMoedas = !!reg.get('mostrarItacoins');
    const paes = reg.get('paes');
    const comPao = paes !== null && paes !== undefined;
    this.iconeMoeda.setVisible(comMoedas);
    this.txtMoedas.setVisible(comMoedas).setText(`x${reg.get('itacoins')}`);
    this.iconePao.setVisible(comPao);
    this.txtPaes.setVisible(comPao).setText(`x${paes ?? 0}`);
    const base = 17 + reg.get('vidaMax') * 13;
    this.fundo.width = comPao ? this.xPao + 34 : comMoedas ? base + 50 : base;
    if (comMoedas && reg.get('itacoins') > this.antes.itacoins) this.pulo(this.iconeMoeda);
    if (comPao && paes > (this.antes.paes ?? 0)) this.pulo(this.iconePao);
    this.antes = { itacoins: reg.get('itacoins'), paes };
  }

  pulo(alvo) {
    this.tweens.killTweensOf(alvo);
    alvo.setScale(1);
    this.tweens.add({ targets: alvo, scale: 1.5, duration: 80, yoyo: true });
  }
}
