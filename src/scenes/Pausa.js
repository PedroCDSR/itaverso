import * as Phaser from 'phaser';
import { LARGURA, ALTURA, CORES, CORES_CSS, FONTES } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { Botao } from '../ui/Botao.js';
import { alternarSom, estaMudo } from '../audio/som.js';
import { alternarTelaCheia, estaEmTelaCheia, telaCheiaDisponivel } from '../ui/telaCheia.js';
import { FINAL, SOBREPOSTAS } from '../fluxo.js';

// Menu de pausa (CLAUDE.md, seção 11): continuar, som, tela cheia (opcional), sobre o espetáculo, pular para o final.
// Abrir com abrirPausa() (src/fluxo.js): esta cena pausa a fase e o HUD e os retoma ao continuar.
export class Pausa extends Phaser.Scene {
  constructor() {
    super('Pausa');
  }

  init(dados) {
    this.cena = dados.cena;
  }

  create() {
    const t = TEXTOS.pausa;
    this.sobrepostas = SOBREPOSTAS.filter((k) => this.scene.isActive(k));
    [this.cena, ...this.sobrepostas].forEach((k) => this.scene.pause(k));
    const cx = LARGURA / 2;
    // fundo interativo: segura os toques, para não acertarem os botões do HUD por baixo
    this.add.rectangle(0, 0, LARGURA, ALTURA, CORES.roxo, 0.75).setOrigin(0).setInteractive();
    this.add
      .text(cx, 26, t.titulo, { fontFamily: FONTES.titulo, fontSize: '16px', color: CORES_CSS.branco })
      .setOrigin(0.5)
      .setShadow(2, 2, '#3A2F7A', 0, false, true);

    const opcoes = [
      { rotulo: t.continuar, acao: () => this.continuar(), cor: 'rosa' },
      { rotulo: this.rotuloSom(), acao: () => this.som(), id: 'som' },
    ];
    // tela cheia só onde o navegador deixa (Android e computador; no iPhone o botão não aparece)
    if (telaCheiaDisponivel(this)) opcoes.push({ rotulo: this.rotuloTelaCheia(), acao: () => this.telaCheia(), id: 'telaCheia' });
    opcoes.push({ rotulo: t.sobre, acao: () => this.sobre() }, { rotulo: t.pularFinal, acao: () => this.pularFinal() });

    const passo = 38;
    const y0 = 62 + (5 - opcoes.length) * (passo / 2);
    this.botoes = {};
    opcoes.forEach((o, i) => {
      const b = new Botao(this, cx, y0 + i * passo, o.rotulo, o.acao, { largura: 220, altura: 30, cor: o.cor || 'lilas' });
      if (o.id) this.botoes[o.id] = b;
    });

    // o rótulo da tela cheia muda também quando a pessoa sai pelo botão "voltar" do Android
    this.scale.on('enterfullscreen', this.atualizarRotulos, this);
    this.scale.on('leavefullscreen', this.atualizarRotulos, this);
    this.events.once('shutdown', () => {
      this.scale.off('enterfullscreen', this.atualizarRotulos, this);
      this.scale.off('leavefullscreen', this.atualizarRotulos, this);
    });
    this.events.on('resume', () => this.input.keyboard?.resetKeys());

    this.input.keyboard?.on('keydown-ESC', () => this.continuar());
    this.input.keyboard?.on('keydown-P', () => this.continuar());
  }

  rotuloSom() {
    return estaMudo() ? TEXTOS.pausa.somDesligado : TEXTOS.pausa.somLigado;
  }

  rotuloTelaCheia() {
    return estaEmTelaCheia(this) ? TEXTOS.pausa.sairTelaCheia : TEXTOS.pausa.telaCheia;
  }

  atualizarRotulos() {
    this.botoes.som?.setRotulo(this.rotuloSom());
    this.botoes.telaCheia?.setRotulo(this.rotuloTelaCheia());
  }

  som() {
    alternarSom();
    this.atualizarRotulos();
  }

  telaCheia() {
    alternarTelaCheia(this);
    // o evento de tela cheia chega um pouco depois; atualiza o rótulo também por garantia
    this.time.delayedCall(300, () => this.atualizarRotulos());
  }

  sobre() {
    this.scene.pause();
    this.scene.launch('Sobre', { de: this.scene.key });
    this.scene.bringToTop('Sobre');
  }

  continuar() {
    if (!this.scene.isActive()) return;
    this.scene.stop();
    [this.cena, ...this.sobrepostas].forEach((k) => this.scene.resume(k));
  }

  pularFinal() {
    [this.cena, ...this.sobrepostas].forEach((k) => this.scene.stop(k));
    this.scene.start(FINAL); // start() também fecha esta cena
  }
}
