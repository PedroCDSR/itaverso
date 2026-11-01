import * as Phaser from 'phaser';
import { LARGURA, ALTURA, CORES, CORES_CSS, FONTES } from '../config.js';
import { TEXTOS, comNumero } from '../data/textos.js';
import { TEM_LOGO } from '../art/index.js';
import { BotaoSom } from '../ui/BotaoSom.js';
import { Dialogo } from '../ui/Dialogo.js';
import { criarCartaoEvento } from '../ui/CartaoEvento.js';
import { abrirIngressos, abrirInstagram, compartilhar } from '../ui/links.js';
import { bipe } from '../audio/som.js';
import { sapatilhas, novaPartida } from '../estado.js';
import { PRIMEIRA_FASE } from '../fluxo.js';

const CORTINA = 0xb0479e; // vinho-rosado do pano do palco
const CORTINA_DOBRA = 0x8a3480;
const PALCO = 0x9a6a44; // madeira do palco
const CHAO_PALCO = ALTURA - 58;

// Final (CLAUDE.md, seção 11.7): cortinas abrem, Tia Paula anuncia o espetáculo, depois o cartão do evento.
export class Final extends Phaser.Scene {
  constructor() {
    super('Final');
  }

  create() {
    this.fase = 'cortinas';
    this.cameras.main.fadeIn(300, 0, 0, 0);
    this.desenharPalco();

    // Tia Paula: aparência ainda A DEFINIR (CLAUDE.md, seção 8). Até lá, silhueta neutra e provisória
    // com microfone, sob o canhão de luz. Trocar pelo sprite dela na Etapa 8.
    this.tiaPaula = this.desenharSilhuetaProvisoria(LARGURA / 2, CHAO_PALCO);
    this.aladdin = this.add.sprite(LARGURA / 2 - 70, CHAO_PALCO, 'jogador').setOrigin(0.5, 1).play('parado');

    this.criarCortinas();
    new BotaoSom(this, LARGURA - 17, 17).g.setDepth(4000);

    // caixa no alto, para não tapar o palco
    this.dialogo = new Dialogo(this, { y: 62, dica: TEXTOS.intro.tocar });
    this.dialogo.esconder();
    this.falas = TEXTOS.final.falaTiaPaula;
    this.indice = 0;

    this.input.on('pointerup', (p, alvos) => {
      if (alvos.length === 0) this.avancar();
    });
    this.input.keyboard?.on('keydown-SPACE', () => this.avancar());
    this.input.keyboard?.on('keydown-ENTER', () => this.avancar());
  }

  desenharPalco() {
    const g = this.add.graphics();
    g.fillStyle(0x2e2a5c, 1).fillRect(0, 0, LARGURA, ALTURA); // fundo escuro do teatro
    g.fillStyle(PALCO, 1).fillRect(0, CHAO_PALCO, LARGURA, ALTURA - CHAO_PALCO);
    g.fillStyle(0x7a4f30, 1);
    for (let x = 0; x < LARGURA; x += 24) g.fillRect(x, CHAO_PALCO, 1, ALTURA - CHAO_PALCO); // tábuas
    g.fillStyle(0xc89a6a, 1).fillRect(0, CHAO_PALCO, LARGURA, 3); // borda iluminada do palco
    // canhão de luz amarelo no centro
    g.fillStyle(CORES.amarelo, 0.18).fillTriangle(LARGURA / 2 - 20, 0, LARGURA / 2 + 20, 0, LARGURA / 2 + 70, CHAO_PALCO);
    g.fillTriangle(LARGURA / 2 - 20, 0, LARGURA / 2 - 70, CHAO_PALCO, LARGURA / 2 + 70, CHAO_PALCO);
    g.fillStyle(CORES.amarelo, 0.35).fillEllipse(LARGURA / 2, CHAO_PALCO + 4, 150, 22);
  }

  desenharSilhuetaProvisoria(x, y) {
    const g = this.add.graphics();
    g.fillStyle(0x5a4fa0, 1);
    g.fillCircle(x, y - 44, 7); // cabeça
    g.fillTriangle(x - 15, y, x + 15, y, x, y - 36); // vestido
    g.fillRect(x - 5, y - 37, 10, 13); // tronco
    g.fillStyle(0x2e1a33, 1).fillRect(x + 7, y - 34, 2, 10); // microfone
    g.fillStyle(0x777777, 1).fillCircle(x + 8, y - 35, 2);
    return g;
  }

  criarCortinas() {
    const criar = (lado) => {
      const g = this.add.graphics().setDepth(100);
      const w = LARGURA / 2 + 4;
      g.fillStyle(CORTINA, 1).fillRect(0, 0, w, ALTURA);
      g.fillStyle(CORTINA_DOBRA, 1);
      for (let x = 10; x < w; x += 22) g.fillRect(x, 0, 6, ALTURA);
      g.fillStyle(CORES.amarelo, 1).fillRect(0, ALTURA - 10, w, 3); // franja dourada
      g.x = lado < 0 ? -4 : LARGURA / 2;
      return g;
    };
    this.cortinaEsq = criar(-1);
    this.cortinaDir = criar(1);
    // bambinela (faixa de cima) com o nome do espetáculo
    const topo = this.add.graphics().setDepth(101);
    topo.fillStyle(CORTINA_DOBRA, 1).fillRect(0, 0, LARGURA, 24);
    topo.fillStyle(CORES.amarelo, 1).fillRect(0, 22, LARGURA, 2);
    this.add
      .text(LARGURA / 2, 12, TEM_LOGO ? 'ALADDIN' : 'ALADDIN · PAULA DE MARCO', { fontFamily: FONTES.titulo, fontSize: '8px', color: CORES_CSS.amarelo })
      .setOrigin(0.5)
      .setDepth(102);

    this.time.delayedCall(500, () => {
      bipe(440, 0.2);
      this.tweens.add({ targets: this.cortinaEsq, x: -LARGURA / 2 + 50, duration: 1600, ease: 'Sine.easeInOut' });
      this.tweens.add({
        targets: this.cortinaDir,
        x: LARGURA - 50,
        duration: 1600,
        ease: 'Sine.easeInOut',
        onComplete: () => this.comecarFalas(),
      });
    });
  }

  comecarFalas() {
    this.fase = 'falas';
    this.tweens.add({ targets: this.tiaPaula, y: -2, yoyo: true, repeat: -1, duration: 500 });
    this.dialogo.mostrar(this.falas[0]);
  }

  avancar() {
    if (this.fase === 'cortinas') {
      // tocou durante as cortinas: acelera
      this.tweens.getTweens().forEach((tw) => tw.complete());
      return;
    }
    if (this.fase !== 'falas') return;
    if (!this.dialogo.terminou) {
      this.dialogo.completar();
      return;
    }
    bipe(600, 0.05);
    this.indice++;
    if (this.indice < this.falas.length) this.dialogo.mostrar(this.falas[this.indice]);
    else this.mostrarCartao();
  }

  mostrarCartao() {
    this.fase = 'cartao';
    this.dialogo.esconder();
    bipe(880, 0.2);
    const n = sapatilhas(this);
    const tf = TEXTOS.final;
    const c = TEXTOS.cartao;
    const fundo = this.add.rectangle(0, 0, LARGURA, ALTURA, CORES.lilas, 0.85).setOrigin(0).setDepth(200);
    const { container, botoes } = criarCartaoEvento(this, {
      profundidade: 201,
      extra: comNumero(tf.sapatilhas, tf.sapatilha1, n),
      botoes: [
        { rotulo: c.ingressos, acao: abrirIngressos, cor: 'rosa' },
        { rotulo: c.compartilhar, acao: () => this.compartilhar(n), cor: 'amarelo' },
        { rotulo: c.instagram, acao: abrirInstagram },
        { rotulo: c.jogarDeNovo, acao: () => this.jogarDeNovo() },
      ],
    });
    this.botaoCompartilhar = botoes[1];
    fundo.setAlpha(0);
    container.setAlpha(0).setY(20);
    this.tweens.add({ targets: fundo, alpha: 1, duration: 300 });
    this.tweens.add({ targets: container, alpha: 1, y: 0, duration: 400, ease: 'Back.easeOut' });
  }

  async compartilhar(n) {
    const tf = TEXTOS.final;
    const r = await compartilhar(comNumero(tf.compartilhar, tf.compartilhar1, n));
    // sem o menu de compartilhar do celular, o link foi copiado: avisa no próprio botão por 2 s
    const aviso = { copiou: TEXTOS.cartao.linkCopiado, falhou: TEXTOS.cartao.naoCopiou }[r];
    if (!aviso) return;
    const b = this.botaoCompartilhar;
    b.setRotulo(aviso.toUpperCase());
    this.time.delayedCall(2000, () => b.setRotulo(TEXTOS.cartao.compartilhar));
  }

  jogarDeNovo() {
    // quem joga de novo já viu a intro: vai direto para a primeira fase
    novaPartida(this);
    this.cameras.main.fadeOut(250, 158, 158, 255);
    this.cameras.main.once('camerafadeoutcomplete', () => this.scene.start(PRIMEIRA_FASE));
  }

  update(_, delta) {
    this.dialogo.atualizar(delta);
  }
}
