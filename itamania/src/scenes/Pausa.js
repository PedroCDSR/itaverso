import * as Phaser from 'phaser';
import { LARGURA, ALTURA, CORES, CORES_CSS, FONTES } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { Botao } from '../ui/Botao.js';
import { alternarSom, estaMudo } from '../audio/som.js';
import { pararMusica } from '../audio/musica.js';

// Menu de pausa por cima da fase: continuar, som, recomeçar a fase, voltar ao mapa.
export class Pausa extends Phaser.Scene {
  constructor() {
    super('Pausa');
  }

  init(dados) {
    this.cena = dados?.cena || 'Fase';
  }

  create() {
    const extras = this.cena === 'Praca' ? ['PracaUI'] : [];
    this.scene.pause(this.cena);
    this.scene.pause('HUD');
    extras.forEach((c) => this.scene.pause(c));
    this.add.rectangle(0, 0, LARGURA, ALTURA, CORES.roxo, 0.75).setOrigin(0);
    this.add.text(LARGURA / 2, 52, TEXTOS.pausa.titulo, { fontFamily: FONTES.titulo, fontSize: '16px', color: CORES_CSS.amarelo }).setOrigin(0.5);
    const voltar = () => {
      this.scene.resume(this.cena);
      this.scene.resume('HUD');
      extras.forEach((c) => this.scene.resume(c));
      this.scene.stop();
    };
    const opc = { largura: 200, altura: 26 };
    new Botao(this, LARGURA / 2, 96, TEXTOS.botoes.continuar, voltar, { ...opc, cor: 'amarelo' });
    const som = new Botao(this, LARGURA / 2, 130, this.rotuloSom(), () => {
      alternarSom();
      som.setRotulo(this.rotuloSom());
    }, opc);
    if (this.cena === 'Missao') {
      new Botao(this, LARGURA / 2, 164, TEXTOS.missao.voltar, () => {
        this.scene.get('Missao').abandonar();
        this.scene.stop();
      }, opc);
    } else if (this.cena === 'Fase') {
      new Botao(this, LARGURA / 2, 164, TEXTOS.botoes.recomecar, () => this.trocar('Fase', { fase: this.registry.get('fase') }), opc);
    } else {
      new Botao(this, LARGURA / 2, 164, TEXTOS.botoes.menu, () => this.trocar('Titulo'), opc);
    }
    if (this.cena !== 'Missao') new Botao(this, LARGURA / 2, 198, TEXTOS.botoes.mapa, () => this.trocar('Mapa'), opc);
    this.input.keyboard?.on('keydown-ESC', voltar);
    this.input.keyboard?.on('keydown-P', voltar);
  }

  rotuloSom() {
    return `${TEXTOS.botoes.som}: ${estaMudo() ? 'DESLIGADO' : 'LIGADO'}`;
  }

  trocar(cena, dados) {
    pararMusica(0.2);
    this.scene.stop('HUD');
    this.scene.stop(this.cena);
    this.scene.start(cena, dados);
  }
}
