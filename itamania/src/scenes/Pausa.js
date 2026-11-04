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

  create() {
    this.scene.pause('Fase');
    this.scene.pause('HUD');
    this.add.rectangle(0, 0, LARGURA, ALTURA, CORES.roxo, 0.75).setOrigin(0);
    this.add.text(LARGURA / 2, 52, TEXTOS.pausa.titulo, { fontFamily: FONTES.titulo, fontSize: '16px', color: CORES_CSS.amarelo }).setOrigin(0.5);
    const voltar = () => {
      this.scene.resume('Fase');
      this.scene.resume('HUD');
      this.scene.stop();
    };
    const opc = { largura: 200, altura: 26 };
    new Botao(this, LARGURA / 2, 96, TEXTOS.botoes.continuar, voltar, { ...opc, cor: 'amarelo' });
    const som = new Botao(this, LARGURA / 2, 130, this.rotuloSom(), () => {
      alternarSom();
      som.setRotulo(this.rotuloSom());
    }, opc);
    new Botao(this, LARGURA / 2, 164, TEXTOS.botoes.recomecar, () => this.trocar('Fase', { fase: this.registry.get('fase') }), opc);
    new Botao(this, LARGURA / 2, 198, TEXTOS.botoes.mapa, () => this.trocar('Mapa'), opc);
    this.input.keyboard?.on('keydown-ESC', voltar);
    this.input.keyboard?.on('keydown-P', voltar);
  }

  rotuloSom() {
    return `${TEXTOS.botoes.som}: ${estaMudo() ? 'DESLIGADO' : 'LIGADO'}`;
  }

  trocar(cena, dados) {
    pararMusica(0.2);
    this.scene.stop('HUD');
    this.scene.stop('Fase');
    this.scene.start(cena, dados);
  }
}
