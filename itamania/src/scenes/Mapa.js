import * as Phaser from 'phaser';
import { LARGURA, ALTURA, CORES, CORES_CSS, FONTES } from '../config.js';
import { NOMES_FASES } from '../data/textos.js';
import { FASES } from '../levels/index.js';
import { Botao } from '../ui/Botao.js';
import { BotaoSom } from '../ui/BotaoSom.js';
import { estado } from '../estado.js';
import { heroi, g } from '../genero.js';
import { tocarMusica } from '../audio/musica.js';
import { tocarEfeito } from '../audio/efeitos.js';

// Mapa-múndi em pé (arte do Pedro: public/assets/mapa.png, 480 x 853; original em referencias/).
// O herói fica numa das moedas do mapa. Setas (ou tocar numa moeda) andam até a fase vizinha; o painel de baixo
// mostra o nome do lugar e o botão JOGAR. A câmera acompanha o herói; dá para arrastar para olhar o mapa.
const ESCALA = 480 / 1080;
// Moedas dos 14 lugares no desenho original (1080 x 1920).
const MOEDAS = [
  null,
  [218, 1787], [308, 1787], [528, 1702], [730, 1640], [198, 1566], [193, 1290], [511, 1035],
  [828, 898], [583, 738], [397, 354], [679, 305], [847, 426], [895, 515], [985, 546],
];
const PONTOS = MOEDAS.map((p) => (p ? [Math.round(p[0] * ESCALA), Math.round(p[1] * ESCALA)] : null));

export class Mapa extends Phaser.Scene {
  constructor() {
    super('Mapa');
  }

  init(dados) {
    this.intro = !!dados?.intro;
    this.ocupado = false;
    this.andando = false;
    this.pularPasseio = false;
  }

  create() {
    tocarMusica('mapa');
    const fundo = this.add.image(0, 0, 'mapa-mundi').setOrigin(0);
    this.alturaMapa = fundo.height;
    const cam = this.cameras.main;
    cam.setBounds(0, 0, LARGURA, this.alturaMapa);

    // anel que pulsa nas fases jogáveis
    for (let n = 1; n <= 14; n++) {
      const [x, y] = PONTOS[n];
      if (FASES[n] && n <= estado.liberada) {
        const anel = this.add.circle(x, y, 9).setStrokeStyle(2, CORES.amarelo).setDepth(5);
        this.tweens.add({ targets: anel, scale: 1.6, alpha: 0, duration: 900, repeat: -1 });
      }
      const zona = this.add.zone(x, y - 6, 34, 34).setInteractive({ useHandCursor: true }).setDepth(6);
      zona.on('pointerup', () => !this.arrastou && this.tocarPonto(n));
    }

    // herói em cima da fase atual
    this.atual = Phaser.Math.Clamp(this.intro ? 1 : estado.ultimaNoMapa || estado.liberada, 1, 14);
    const [hx, hy] = PONTOS[this.atual];
    this.heroi = this.add.sprite(hx, hy + 2, `heroi-${heroi()}-normal`, 0).setOrigin(0.5, 1).setDepth(20);
    this.animHeroi('parado');
    cam.startFollow(this.heroi, true, 0.12, 0.12, 0, -20);

    this.criarPainel();
    new BotaoSom(this, LARGURA - 20, 20);

    // arrastar solta a câmera do herói (andar de novo volta a seguir)
    this.input.on('pointerdown', () => (this.arrastou = false));
    this.input.on('pointermove', (p) => {
      if (!p.isDown || this.ocupado) return;
      if (Math.abs(p.position.y - p.downY) > 8) {
        this.arrastou = true;
        cam.stopFollow();
        cam.scrollY = Phaser.Math.Clamp(cam.scrollY + (p.prevPosition.y - p.position.y), 0, this.alturaMapa - ALTURA);
      }
    });
    this.input.on('wheel', (p, o, dx, dy) => {
      cam.stopFollow();
      cam.scrollY = Phaser.Math.Clamp(cam.scrollY + dy * 0.5, 0, this.alturaMapa - ALTURA);
    });
    const kb = this.input.keyboard;
    kb?.on('keydown-RIGHT', () => this.andarPara(this.atual + 1));
    kb?.on('keydown-UP', () => this.andarPara(this.atual + 1));
    kb?.on('keydown-LEFT', () => this.andarPara(this.atual - 1));
    kb?.on('keydown-DOWN', () => this.andarPara(this.atual - 1));
    kb?.on('keydown-ENTER', () => this.jogar());
    kb?.on('keydown-SPACE', () => this.jogar());
    cam.fadeIn(300);
    this.atualizarPainel();
    if (this.intro) this.passeio();
  }

  animHeroi(nome) {
    this.heroi.play(`${heroi()}-normal-${estado.bone ? 'b' : 's'}-${nome}`, true);
  }

  // Painel fixo embaixo: setas, nome do lugar e JOGAR.
  criarPainel() {
    const y = ALTURA - 26;
    this.add.rectangle(LARGURA / 2, y, LARGURA - 16, 40, CORES.roxo, 0.9).setScrollFactor(0).setDepth(50).setStrokeStyle(2, CORES.amarelo);
    this.txtNumero = this.add.text(54, y - 12, '', { fontFamily: FONTES.titulo, fontSize: '7px', color: CORES_CSS.amarelo }).setScrollFactor(0).setDepth(51);
    this.txtNome = this.add.text(54, y - 2, '', { fontFamily: FONTES.dialogo, fontSize: '16px', color: CORES_CSS.branco }).setScrollFactor(0).setDepth(51);
    const seta = (x, dir) => {
      const s = this.add.container(x, y).setScrollFactor(0).setDepth(51);
      s.add(this.add.circle(0, 0, 14, CORES.azul).setStrokeStyle(2, CORES.branco));
      s.add(dir < 0 ? this.add.triangle(-1, 0, 8, 0, 8, 12, 0, 6, CORES.branco) : this.add.triangle(1, 0, 0, 0, 0, 12, 8, 6, CORES.branco));
      s.setSize(36, 36).setInteractive({ useHandCursor: true });
      s.on('pointerup', () => this.andarPara(this.atual + dir));
      return s;
    };
    this.setaVoltar = seta(28, -1);
    this.setaIr = seta(LARGURA - 146, 1);
    this.botaoJogar = new Botao(this, LARGURA - 72, y, 'JOGAR', () => this.jogar(), { largura: 96, altura: 26, cor: 'amarelo', tamanhoFonte: '9px' });
    this.botaoJogar.setDepth(52);
    new Botao(this, 40, 20, 'MENU', () => this.scene.start('Titulo'), { largura: 64, altura: 20, tamanhoFonte: '7px' }).setDepth(52);
  }

  atualizarPainel() {
    const n = this.atual;
    const jogavel = FASES[n] && n <= estado.liberada;
    this.txtNumero.setText(`FASE ${n}${estado.feitas.includes(n) ? ' · FEITA' : ''}`);
    this.txtNome.setText(NOMES_FASES[n] + (FASES[n] ? (jogavel ? '' : ' (termine a anterior)') : ' · em breve'));
    this.botaoJogar.setVisible(!!jogavel && !this.ocupado);
    this.setaVoltar.setAlpha(n > 1 ? 1 : 0.35);
    this.setaIr.setAlpha(n < 14 ? 1 : 0.35);
  }

  tocarPonto(n) {
    if (n === this.atual) this.jogar();
    else this.andarPara(n);
  }

  // Anda pelas moedas até a fase n, passando pelas do meio.
  async andarPara(n) {
    if (this.ocupado || this.andando || n < 1 || n > 14 || n === this.atual) return;
    this.andando = true;
    this.cameras.main.startFollow(this.heroi, true, 0.12, 0.12, 0, -20);
    const passo = n > this.atual ? 1 : -1;
    this.animHeroi('correndo');
    while (this.atual !== n) {
      const prox = this.atual + passo;
      const [x, y] = PONTOS[prox];
      this.heroi.setFlipX(x < this.heroi.x);
      const dist = Phaser.Math.Distance.Between(this.heroi.x, this.heroi.y, x, y + 2);
      await new Promise((ok) => this.tweens.add({ targets: this.heroi, x, y: y + 2, duration: Math.max(140, dist * 3.2), onComplete: ok }));
      this.atual = prox;
      tocarEfeito('moeda', { variar: 0.1, volume: 0.4 });
      this.atualizarPainel();
    }
    this.animHeroi('parado');
    estado.ultimaNoMapa = this.atual;
    this.andando = false;
  }

  jogar() {
    const n = this.atual;
    if (this.ocupado || this.andando) return;
    if (!FASES[n] || n > estado.liberada) {
      tocarEfeito('dano', { volume: 0.4 });
      this.tweens.add({ targets: this.heroi, x: this.heroi.x + 3, duration: 50, yoyo: true, repeat: 2 });
      return;
    }
    tocarEfeito('botao');
    this.ocupado = true;
    this.animHeroi('vitoria');
    this.cameras.main.fadeOut(350);
    this.cameras.main.once('camerafadeoutcomplete', () => this.scene.start('Fase', { fase: n }));
  }

  // Abertura: a câmera sobe da Rodoviária até a Prefeitura mostrando cada lugar e volta para a fase 1.
  async passeio() {
    const cam = this.cameras.main;
    this.ocupado = true;
    this.atualizarPainel();
    cam.stopFollow();
    const faixa = this.add
      .text(LARGURA / 2, 52, '', { fontFamily: FONTES.dialogo, fontSize: '17px', color: CORES_CSS.branco, backgroundColor: '#2B2D5CDD', padding: { x: 8, y: 3 }, align: 'center' })
      .setOrigin(0.5)
      .setScrollFactor(0)
      .setDepth(60);
    const pular = new Botao(this, LARGURA - 74, 20, 'PULAR', () => (this.pularPasseio = true), { largura: 64, altura: 20, tamanhoFonte: '7px' });
    pular.setDepth(61);
    const ir = (y, ms) =>
      new Promise((ok) => this.tweens.add({ targets: cam, scrollY: Phaser.Math.Clamp(y - ALTURA / 2, 0, this.alturaMapa - ALTURA), duration: ms, ease: 'Sine.inOut', onComplete: ok }));
    const pausa = (ms) => new Promise((ok) => this.time.delayedCall(ms, ok));
    faixa.setText(g('Bem-vind{o|a} a Itajubá!'));
    cam.scrollY = this.alturaMapa - ALTURA;
    await pausa(1300);
    for (let n = 1; n <= 14 && !this.pularPasseio; n++) {
      faixa.setText(`${n}. ${NOMES_FASES[n]}`);
      await ir(PONTOS[n][1], 380);
      const anel = this.add.circle(PONTOS[n][0], PONTOS[n][1], 8).setStrokeStyle(3, CORES.amarelo).setDepth(7);
      this.tweens.add({ targets: anel, scale: 2.2, alpha: 0, duration: 600, onComplete: () => anel.destroy() });
      tocarEfeito('moeda', { variar: 0.1, volume: 0.45 });
      await pausa(n === 14 ? 1400 : 320);
    }
    if (!this.pularPasseio) {
      faixa.setText('A aventura começa na Rodoviária!');
      await ir(PONTOS[1][1], 1400);
      await pausa(500);
    }
    faixa.destroy();
    pular.container.destroy();
    this.ocupado = false;
    cam.startFollow(this.heroi, true, 0.12, 0.12, 0, -20);
    this.atualizarPainel();
    this.jogar();
  }
}
