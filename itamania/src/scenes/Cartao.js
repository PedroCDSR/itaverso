import * as Phaser from 'phaser';
import { LARGURA, ALTURA, CORES, CORES_CSS, FONTES, CARTAO } from '../config.js';
import { TEXTOS, NOMES_FASES } from '../data/textos.js';
import { FASES } from '../levels/index.js';
import { Botao } from '../ui/Botao.js';
import { tocarMusica } from '../audio/musica.js';
import { g } from '../genero.js';

// Cartão de curiosidade no fim de cada fase (DESIGN.md): uma frase real sobre a cidade, uns 5 s de leitura.
// O texto e a fonte de cada fato ficam no arquivo da fase (`curiosidade`). Fato sem fonte não entra.
export class Cartao extends Phaser.Scene {
  constructor() {
    super('Cartao');
  }

  init(dados) {
    this.numero = dados.fase;
  }

  create() {
    const c = FASES[this.numero].curiosidade;
    tocarMusica('mapa');
    this.add.rectangle(0, 0, LARGURA, ALTURA, CORES.roxo).setOrigin(0);
    // cartão amarelo-claro com borda e sombra
    const w = 380;
    const h = 186;
    const x0 = (LARGURA - w) / 2;
    const y0 = 26;
    this.add.rectangle(x0 + 4, y0 + 4, w, h, 0x000000, 0.35).setOrigin(0);
    this.add.rectangle(x0, y0, w, h, CORES.amareloClaro).setOrigin(0).setStrokeStyle(3, CORES.amarelo);
    this.add.text(LARGURA / 2, y0 + 12, `FASE ${this.numero} · ${NOMES_FASES[this.numero].toUpperCase()}`, { fontFamily: FONTES.titulo, fontSize: '7px', color: CORES_CSS.laranja }).setOrigin(0.5, 0);
    this.add.text(LARGURA / 2, y0 + 30, TEXTOS.cartao.titulo, { fontFamily: FONTES.titulo, fontSize: '12px', color: CORES_CSS.azul }).setOrigin(0.5, 0);
    this.add.sprite(x0 + 26, y0 + 36, 'itacoin', 0).play('itacoin-girar').setScale(1.5);
    this.add.sprite(x0 + w - 26, y0 + 36, 'itacoin', 0).play('itacoin-girar').setScale(1.5);
    this.add
      .text(LARGURA / 2, y0 + 56, g(c.texto), { fontFamily: FONTES.dialogo, fontSize: '19px', color: CORES_CSS.roxo, align: 'center', wordWrap: { width: w - 36 }, lineSpacing: 2 })
      .setOrigin(0.5, 0);
    this.add.text(LARGURA / 2, y0 + h - 14, `Fonte: ${c.fonte}`, { fontFamily: FONTES.dialogo, fontSize: '12px', color: '#6A6A9A' }).setOrigin(0.5);
    const b = new Botao(this, LARGURA / 2, 240, TEXTOS.cartao.continuar, () => this.seguir(), { largura: 170, altura: 26, cor: 'amarelo' });
    b.setVisible(false);
    this.time.delayedCall(CARTAO.esperaMs, () => b.setVisible(true));
    this.cameras.main.fadeIn(300, 43, 45, 92);
  }

  seguir() {
    // depois da fase 4 (última construída por enquanto) vem a tela de "continua"; senão, o mapa
    this.scene.start(FASES[this.numero + 1] ? 'Mapa' : 'Fim', { de: this.numero });
  }
}
