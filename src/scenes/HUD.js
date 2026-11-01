import * as Phaser from 'phaser';
import { LARGURA, CORES, CORES_CSS, FONTES } from '../config.js';
import { BotaoSom } from '../ui/BotaoSom.js';
import { BotaoPausa } from '../ui/BotaoPausa.js';
import { abrirPausa } from '../fluxo.js';

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

    // fundo suave atrás dos contadores, para ler em cima do céu claro (cresce quando há ingressos)
    this.fundo = this.add.rectangle(6, 6, 148, 22, CORES.roxo, 0.35).setOrigin(0).setStrokeStyle(1, CORES.roxo, 0.6);

    // com mais de 3 corações (níveis fácil e médio), os outros contadores andam para a direita
    const dx = Math.max(0, reg.get('vidaMax') - 3) * 13;
    this.larguraFundo = 148 + dx;
    this.coracoes = [];
    for (let i = 0; i < reg.get('vidaMax'); i++) {
      this.coracoes.push(this.add.image(17 + i * 13, 17, 'coracao', 0));
    }
    this.add.image(64 + dx, 17, 'maca');
    this.txtMacas = sombra(this.add.text(72 + dx, 13, '', estilo));
    this.add.sprite(110 + dx, 18, 'sapatilha', 0);
    this.txtSapatilhas = sombra(this.add.text(120 + dx, 13, '', estilo));
    // ingressos: só a partir da Fase 2 (registry 'ingressos' diferente de null)
    this.iconeIngresso = this.add.image(162 + dx, 17, 'ingresso');
    this.txtIngressos = sombra(this.add.text(173 + dx, 13, '', estilo));
    // a Fase 2 usa esta posição para mandar os ingressos voando até aqui
    reg.set('posIngressoHud', { x: this.iconeIngresso.x, y: this.iconeIngresso.y });
    this.ingressosAntes = reg.get('ingressos');

    // botão de pausa ao lado do som: abre o menu de pausa (Etapa 7). Esc ou P também abrem.
    const py = 20;
    new BotaoPausa(this, LARGURA - 56, py, () => abrirPausa(this));
    this.botaoSom = new BotaoSom(this, LARGURA - 20, py);
    this.input.keyboard?.on('keydown-ESC', () => abrirPausa(this));
    this.input.keyboard?.on('keydown-P', () => abrirPausa(this));
    // o som pode ter mudado no menu de pausa
    this.events.on('resume', () => this.botaoSom.desenhar());

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
    const ingressos = reg.get('ingressos');
    const temIngressos = ingressos !== null && ingressos !== undefined;
    this.iconeIngresso.setVisible(temIngressos);
    this.txtIngressos.setVisible(temIngressos).setText(`x${ingressos ?? 0}`);
    this.fundo.width = this.larguraFundo + (temIngressos ? 48 : 0);
    // pulinho no ícone quando chega ingresso novo
    if (temIngressos && ingressos > (this.ingressosAntes ?? 0)) {
      this.tweens.add({ targets: this.iconeIngresso, scale: 1.5, duration: 90, yoyo: true });
    }
    this.ingressosAntes = ingressos;
  }
}
