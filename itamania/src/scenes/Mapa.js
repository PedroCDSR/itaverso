import * as Phaser from 'phaser';
import { LARGURA, ALTURA, CORES, CORES_CSS, FONTES } from '../config.js';
import { NOMES_FASES, TEXTOS } from '../data/textos.js';
import { FASES } from '../levels/index.js';
import { Botao } from '../ui/Botao.js';
import { BotaoSom } from '../ui/BotaoSom.js';
import { MapaHtml } from '../ui/mapaHtml.js';
import { estado } from '../estado.js';
import { tocarMusica } from '../audio/musica.js';
import { tocarEfeito } from '../audio/efeitos.js';
import { MICROMUNDOS } from '../data/micromundos.js';

// Mapa-múndi em pé (arte do Pedro em alta resolução: public/assets/mapa-hd.png, 1080x1920; original em
// referencias/). O mapa fica numa camada HTML (ui/mapaHtml.js) que rola só na vertical: arrastar, roda do mouse
// e setas para cima e para baixo. Sem passeio automático: abre mostrando a Rodoviária. O herói fica numa moeda;
// tocar noutra moeda faz ele andar até lá (setas para os lados também). O painel do Phaser embaixo mostra o
// número e o nome do lugar, JOGAR, PRAÇA (volta ao centro explorável) e o som.
const RODAPE = 46; // altura do painel em px do jogo (a camada do mapa ocupa o resto do canvas)
const ALTURA_HEROI = 66; // em px do desenho original
// Moedas dos 14 lugares no desenho original (1080 x 1920).
const MOEDAS = [
  null,
  [218, 1787], [308, 1787], [528, 1702], [730, 1640], [198, 1566], [193, 1290], [511, 1035],
  [828, 898], [583, 738], [397, 354], [679, 305], [847, 426], [895, 515], [985, 546],
];

export class Mapa extends Phaser.Scene {
  constructor() {
    super('Mapa');
  }

  init(dados) {
    this.intro = !!dados?.intro;
    this.ocupado = false;
    this.andando = false;
  }

  create() {
    tocarMusica('mapa');
    this.cameras.main.setBackgroundColor(CORES.roxo);
    this.atual = Phaser.Math.Clamp(this.intro ? 1 : estado.ultimaNoMapa || estado.liberada, 1, 14);

    // sprite escondido: só roda a animação; a camada HTML copia o quadro atual
    this.heroi = this.add.sprite(-100, -100, 'capivara-exploradora', 8).setVisible(false);
    this.animHeroi('parado');

    const aneis = [];
    for (let n = 1; n <= 14; n++) if (MICROMUNDOS[n - 1].exploracao || (FASES[n] && n <= estado.liberada)) aneis.push(n);
    this.mapa = new MapaHtml(this, {
      imagem: 'assets/mapa-hd.png',
      moedas: MOEDAS,
      aneis,
      rodape: RODAPE,
      alturaHeroi: ALTURA_HEROI,
      quadroHeroi: () => this.heroi.frame,
      aoTocarMoeda: (n) => this.tocarPonto(n),
    });
    this.pos = this.mapa.heroiPos;
    this.colocarHeroi(this.atual);
    // abre embaixo (Rodoviária); voltando de uma fase mais acima, mostra onde o herói está
    if (this.atual > 3) this.mapa.centrar(MOEDAS[this.atual][1], false);
    if (this.intro) this.mapa.mostrarFaixa('Toque numa moeda para começar');

    this.criarPainel();

    const kb = this.input.keyboard;
    kb?.on('keydown-RIGHT', () => this.andarPara(this.atual + 1));
    kb?.on('keydown-LEFT', () => this.andarPara(this.atual - 1));
    kb?.on('keydown-UP', () => this.mapa.rolarPasso(-1));
    kb?.on('keydown-DOWN', () => this.mapa.rolarPasso(1));
    kb?.on('keydown-ENTER', () => this.jogar());
    kb?.on('keydown-SPACE', () => this.jogar());
    this.cameras.main.fadeIn(300);
    this.atualizarPainel();
  }

  colocarHeroi(n) {
    const [x, y] = MOEDAS[n];
    this.pos.x = x;
    this.pos.y = y + 4;
  }

  animHeroi(nome) {
    this.heroi.play(`exploradora-${nome === 'correndo' ? 'andar' : 'parado'}-direita`, true);
  }

  // Painel fixo embaixo: PRAÇA, número e nome do lugar, JOGAR e som.
  criarPainel() {
    const y = ALTURA - RODAPE / 2;
    this.add.rectangle(LARGURA / 2, y, LARGURA - 8, RODAPE - 6, CORES.roxo).setStrokeStyle(2, CORES.amarelo);
    new Botao(this, 36, y, TEXTOS.botoes.praca, () => this.voltarMenu(), { largura: 56, altura: 22, tamanhoFonte: '7px' });
    this.txtNumero = this.add.text(76, y - 13, '', { fontFamily: FONTES.titulo, fontSize: '7px', color: CORES_CSS.amarelo });
    this.txtNome = this.add.text(76, y - 4, '', { fontFamily: FONTES.dialogo, fontSize: '16px', color: CORES_CSS.branco });
    this.botaoJogar = new Botao(this, LARGURA - 92, y, 'JOGAR', () => this.jogar(), { largura: 96, altura: 26, cor: 'amarelo', tamanhoFonte: '9px' });
    new BotaoSom(this, LARGURA - 22, y);
  }

  atualizarPainel() {
    const n = this.atual;
    const exploracao = MICROMUNDOS[n - 1].exploracao;
    const jogavel = exploracao || (FASES[n] && n <= estado.liberada);
    this.txtNumero.setText(`${exploracao ? 'LOCAL' : 'FASE'} ${n}${estado.feitas.includes(n) ? ' · FEITA' : ''}`);
    this.txtNome.setText(NOMES_FASES[n] + (FASES[n] ? (jogavel ? '' : ' (termine a anterior)') : ' · em breve'));
    this.botaoJogar.setVisible(!!jogavel && !this.ocupado);
    this.botaoJogar.setRotulo(exploracao ? TEXTOS.missao.explorar : TEXTOS.botoes.jogar);
  }

  tocarPonto(n) {
    this.mapa.mostrarFaixa('');
    if (n === this.atual) this.jogar();
    else this.andarPara(n);
  }

  // Anda pelas moedas até a fase n, passando pelas do meio; a camada rola junto se o herói sair da tela.
  async andarPara(n) {
    if (this.ocupado || this.andando || n < 1 || n > 14 || n === this.atual) return;
    this.andando = true;
    this.mapa.mostrarFaixa('');
    const passo = n > this.atual ? 1 : -1;
    this.animHeroi('correndo');
    while (this.atual !== n) {
      const prox = this.atual + passo;
      const [x, y] = MOEDAS[prox];
      this.pos.virado = x < this.pos.x;
      const dist = Phaser.Math.Distance.Between(this.pos.x, this.pos.y, x, y + 4);
      await new Promise((ok) =>
        this.tweens.add({ targets: this.pos, x, y: y + 4, duration: Math.max(160, dist * 1.5), onUpdate: () => this.mapa.seguirHeroi(), onComplete: ok }),
      );
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
    if (MICROMUNDOS[n - 1].exploracao) {
      this.ocupado = true;
      this.sair(() => this.scene.start(MICROMUNDOS[n - 1].exploracao), 350);
      return;
    }
    if (!FASES[n] || n > estado.liberada) {
      tocarEfeito('dano', { volume: 0.4 });
      this.tweens.add({ targets: this.pos, x: this.pos.x + 6, duration: 50, yoyo: true, repeat: 2 });
      return;
    }
    tocarEfeito('botao');
    this.ocupado = true;
    this.atualizarPainel();
    this.animHeroi('vitoria');
    this.sair(() => this.scene.start('Fase', { fase: n }), 450);
  }

  voltarMenu() {
    if (this.ocupado) return;
    this.ocupado = true;
    this.sair(() => this.scene.start('Praca'), 300); // o mapa volta para a praça (o centro explorável)
  }

  sair(depois, ms) {
    this.mapa.esconder();
    this.cameras.main.fadeOut(ms);
    this.cameras.main.once('camerafadeoutcomplete', depois);
  }
}
