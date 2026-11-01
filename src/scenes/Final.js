import * as Phaser from 'phaser';
import { LARGURA, ALTURA, CORES, CORES_CSS, FONTES } from '../config.js';
import { TEXTOS, comNumero } from '../data/textos.js';
import { TEM_LOGO } from '../art/index.js';
import { BotaoSom } from '../ui/BotaoSom.js';
import { Dialogo } from '../ui/Dialogo.js';
import { criarCartaoEvento } from '../ui/CartaoEvento.js';
import { abrirIngressos, abrirInstagram, compartilhar } from '../ui/links.js';
import { tocarEfeito } from '../audio/efeitos.js';
import { tocarMusica, tocarVinheta } from '../audio/musica.js';
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
    tocarMusica('final');
    this.desenharPalco();

    // Tia Paula no centro do palco, sob o canhão de luz
    this.tiaPaula = this.desenharTiaPaula(LARGURA / 2, CHAO_PALCO);
    this.aladdin = this.add.sprite(LARGURA / 2 - 70, CHAO_PALCO, 'jogador').setOrigin(0.5, 1).play('parado');

    this.criarCortinas();
    new BotaoSom(this, LARGURA - 17, 17).g.setDepth(4000);

    // caixa de diálogo em HTML (ui/Dialogo.js), no alto, sem tapar o palco
    this.dialogo = new Dialogo(this);

    // tocar durante as cortinas acelera a abertura
    this.input.on('pointerup', () => this.fase === 'cortinas' && this.acelerarCortinas());
    this.input.keyboard?.on('keydown-SPACE', () => this.fase === 'cortinas' && this.acelerarCortinas());
    this.input.keyboard?.on('keydown-ENTER', () => this.fase === 'cortinas' && this.acelerarCortinas());
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

  // Tia Paula de pé, com o MESMO design provisório do Tapete (ferramentas/arte/gerar_tapete.py): coque castanho,
  // vestido roxo com faixa amarela, meia lilás e sapatilha rosa. Aparência real A DEFINIR (CLAUDE.md, seção 8).
  desenharTiaPaula(x, y) {
    const g = this.add.graphics({ x, y });
    const r = (cor, x0, y0, w, h) => g.fillStyle(cor, 1).fillRect(x0, y0, w, h);
    const k = 0x2e1a33; // contorno
    // pernas e sapatilhas
    r(k, -5, -13, 10, 11);
    r(0x7c7ce0, -4, -13, 3, 11);
    r(0x9e9eff, 1, -13, 3, 11);
    r(k, -7, -3, 15, 3);
    r(0xffb0fa, -6, -3, 5, 2);
    r(0xffb0fa, 1, -3, 5, 2);
    // vestido com saia rodada
    g.fillStyle(k, 1).fillTriangle(-14, -11, 14, -11, 0, -32);
    g.fillStyle(0x6d6bd9, 1).fillTriangle(-12, -12, 12, -12, 0, -31);
    g.fillStyle(0x4f4db0, 1).fillTriangle(-12, -12, -6, -12, -1, -30);
    r(k, -6, -32, 12, 12);
    r(0x6d6bd9, -5, -31, 10, 11);
    r(0xf9fcbb, -6, -22, 12, 2); // faixa amarela na cintura
    // braço com microfone
    r(0xe8b48a, 5, -29, 3, 7);
    r(0x222222, 7, -33, 2, 7);
    g.fillStyle(0x777777, 1).fillCircle(8, -34, 2);
    // pescoço e cabeça
    r(0xc48c64, -1, -34, 3, 3);
    g.fillStyle(k, 1).fillCircle(0, -40, 7);
    g.fillStyle(0xe8b48a, 1).fillCircle(0, -40, 6);
    // cabelo puxado para trás, com coque alto de bailarina
    g.fillStyle(0x5a3a2a, 1).fillRect(-6, -47, 12, 4).fillRect(-6, -45, 2, 5).fillRect(4, -45, 2, 5);
    g.fillStyle(0x5a3a2a, 1).fillCircle(0, -49, 4);
    g.fillStyle(0x3e2619, 1).fillRect(-1, -51, 2, 2);
    // olhos e sorriso
    r(0x2a1a1c, -3, -41, 1, 2);
    r(0x2a1a1c, 2, -41, 1, 2);
    r(0x9a4040, -1, -37, 3, 1);
    r(0xf9fcbb, -6, -38, 1, 1); // brinco
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
      tocarEfeito('botao');
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

  async comecarFalas() {
    if (this.fase !== 'cortinas') return;
    this.fase = 'falas';
    this.tweens.add({ targets: this.tiaPaula, y: CHAO_PALCO - 2, yoyo: true, repeat: -1, duration: 500 });
    const nome = TEXTOS.chefe.nomePaula;
    await this.dialogo.mostrar(TEXTOS.final.falaTiaPaula.map((texto) => ({ nome, texto, cor: CORES_CSS.roxo })));
    if (this.sys.isActive()) this.mostrarCartao();
  }

  acelerarCortinas() {
    this.tweens.getTweens().forEach((tw) => tw.complete());
  }

  mostrarCartao() {
    this.fase = 'cartao';
    tocarVinheta('vitoria');
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
    novaPartida(this); // (a Itajubá também zera vida, maçãs e sapatilhas ao começar)
    this.cameras.main.fadeOut(250, 158, 158, 255);
    this.cameras.main.once('camerafadeoutcomplete', () => this.scene.start(PRIMEIRA_FASE));
  }

}
