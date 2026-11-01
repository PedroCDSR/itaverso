import * as Phaser from 'phaser';
import { LARGURA, CORES, CORES_CSS, FONTES, CONTROLES } from '../config.js';
import { TEXTOS } from '../data/textos.js';

// Botões de toque na tela: ◀ ▶ à esquerda, PULAR e MAÇÃ à direita.
//
// Em vez de eventos de "apertou o botão X", a cada quadro olhamos onde estão TODOS os dedos na tela.
// Assim o multitoque funciona sozinho (andar + pular), e deslizar o polegar de ◀ para ▶ troca a direção
// sem precisar levantar o dedo.
export class ControlesToque {
  constructor(scene) {
    this.scene = scene;
    this.modoTapete = false;
    this.estado = { esquerda: false, direita: false, pular: false, maca: false, segurando: false };

    // só desenha os botões em aparelhos com toque
    this.visivel = scene.sys.game.device.input.touch;
    this.botoes = {};
    if (this.visivel) this.desenhar();
  }

  desenhar() {
    const c = CONTROLES;
    const criar = (nome, cfg, rotulo, tamanhoFonte) => {
      const g = this.scene.add.container(cfg.x, cfg.y).setScrollFactor(0).setDepth(1000);
      const fundo = this.scene.add.circle(0, 0, cfg.raio, CORES.lilas).setStrokeStyle(2, CORES.roxo);
      g.add(fundo);
      if (typeof rotulo === 'string') {
        g.add(
          this.scene.add
            .text(0, 0, rotulo, { fontFamily: FONTES.titulo, fontSize: tamanhoFonte, color: CORES_CSS.branco })
            .setOrigin(0.5),
        );
      } else {
        g.add(rotulo);
      }
      g.setAlpha(c.opacidade);
      this.botoes[nome] = g;
    };
    // setas desenhadas como triângulos (a fonte manuscrita não tem ◀ ▶)
    // (no Phaser os pontos do triângulo contam a partir do canto da caixa 18x22; a origem 0.5 centraliza)
    const seta = (paraDireita) =>
      paraDireita
        ? this.scene.add.triangle(2, 0, 0, 0, 0, 22, 18, 11, CORES.branco)
        : this.scene.add.triangle(-2, 0, 18, 0, 18, 22, 0, 11, CORES.branco);
    criar('esquerda', c.esquerda, seta(false));
    criar('direita', c.direita, seta(true));
    criar('pular', c.pular, TEXTOS.botoes.pular, '8px');
    criar('maca', c.maca, TEXTOS.botoes.maca, '8px');
  }

  // No tapete os botões somem e vale "segurar em qualquer lugar".
  setModoTapete(ligado) {
    this.modoTapete = ligado;
    Object.values(this.botoes).forEach((b) => b.setVisible(!ligado));
  }

  // Chamar uma vez por quadro, no update() da cena.
  atualizar() {
    const e = { esquerda: false, direita: false, pular: false, maca: false, segurando: false };
    const c = CONTROLES;
    // pointers[0] é o mouse; os toques vêm depois. O mouse também conta (ajuda a testar no computador).
    for (const p of this.scene.input.manager.pointers) {
      if (!p || !p.isDown) continue;
      e.segurando = true;
      if (this.modoTapete || p.y < c.alturaMinima) continue;
      if (p.x < LARGURA / 2) {
        // metade esquerda: o que estiver mais perto, ◀ ou ▶ (a área vai até a borda da tela)
        const meio = (c.esquerda.x + c.direita.x) / 2;
        if (p.x < meio) e.esquerda = true;
        else if (p.x < c.direita.x + c.direita.raio * 2.5) e.direita = true;
      } else {
        // metade direita: PULAR ou MAÇÃ, o centro mais próximo
        const dPular = Phaser.Math.Distance.Between(p.x, p.y, c.pular.x, c.pular.y) / c.pular.raio;
        const dMaca = Phaser.Math.Distance.Between(p.x, p.y, c.maca.x, c.maca.y) / c.maca.raio;
        if (dPular <= dMaca) {
          if (p.x > c.maca.x - c.maca.raio * 2) e.pular = true;
        } else {
          e.maca = true;
        }
      }
    }
    this.estado = e;

    if (this.visivel && !this.modoTapete) {
      for (const nome of ['esquerda', 'direita', 'pular', 'maca']) {
        this.botoes[nome].setAlpha(e[nome] ? c.opacidadeApertado : c.opacidade);
      }
    }
    return e;
  }
}
