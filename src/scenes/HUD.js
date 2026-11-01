import * as Phaser from 'phaser';
import { LARGURA, CORES, CORES_CSS, FONTES } from '../config.js';
import { BotaoSom } from '../ui/BotaoSom.js';
import { pausarAgora } from '../ui/PausaFoco.js';

// HUD (cena sobreposta à fase): corações, maçãs e sapatilhas à esquerda; pausa e som à direita.
// Lê tudo do "registry" do jogo (vida, vidaMax, macas, sapatilhas); a fase só atualiza os valores.
export class HUD extends Phaser.Scene {
  constructor() {
    super('HUD');
  }

  create() {
    const reg = this.registry;
    const estilo = { fontFamily: FONTES.titulo, fontSize: '8px', color: CORES_CSS.branco };
    const sombra = (t) => t.setShadow(1, 1, CORES_CSS.roxo, 0, false, true);

    // fundo suave atrás dos contadores, para ler em cima do céu claro
    this.add.rectangle(6, 6, 176, 22, CORES.roxo, 0.35).setOrigin(0).setStrokeStyle(1, CORES.roxo, 0.6);

    this.coracoes = [];
    for (let i = 0; i < reg.get('vidaMax'); i++) {
      this.coracoes.push(this.add.image(17 + i * 13, 17, 'coracao', 0));
    }
    this.add.image(64, 17, 'maca');
    this.txtMacas = sombra(this.add.text(72, 13, '', estilo));
    this.add.sprite(110, 18, 'sapatilha', 0);
    this.txtSapatilhas = sombra(this.add.text(120, 13, '', estilo));

    // botão de pausa (duas barrinhas) ao lado do som
    const px = LARGURA - 56;
    const py = 20;
    const g = this.add.graphics();
    g.fillStyle(CORES.lilas, 0.6).fillCircle(px, py, 14).lineStyle(2, CORES.roxo).strokeCircle(px, py, 14);
    g.fillStyle(CORES.branco).fillRect(px - 5, py - 6, 4, 12).fillRect(px + 1, py - 6, 4, 12);
    this.add
      .zone(px, py, 36, 36)
      .setInteractive({ useHandCursor: true })
      .on('pointerup', () => pausarAgora());
    new BotaoSom(this, LARGURA - 20, py);

    this.atualizar();
    const aoMudar = () => this.atualizar();
    reg.events.on('changedata', aoMudar);
    this.events.once('shutdown', () => reg.events.off('changedata', aoMudar));
  }

  atualizar() {
    const reg = this.registry;
    const vida = reg.get('vida');
    this.coracoes.forEach((c, i) => c.setFrame(i < vida ? 0 : 1));
    this.txtMacas.setText(`x${reg.get('macas')}`);
    this.txtSapatilhas.setText(`x${reg.get('sapatilhas')}`);
  }
}
