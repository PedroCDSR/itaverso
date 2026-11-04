import * as Phaser from 'phaser';
import { LARGURA, CORES, CORES_CSS, FONTES, PRACA } from '../config.js';
import { TEXTOS } from '../data/textos.js';

const K = Phaser.Input.Keyboard.KeyCodes;

// Controles da praça andável, numa cena por cima (sem o zoom da câmera do mapa).
// Toque: joystick que nasce onde o dedo encosta na metade esquerda; botão FALAR à direita.
// Teclado: setas ou WASD para andar; espaço, Enter, X ou J para conversar.
// A cena da praça lê `estado` a cada quadro: { dx, dy } (vetor de -1 a 1) e `falarApertou`.
export class PracaUI extends Phaser.Scene {
  constructor() {
    super('PracaUI');
  }

  create() {
    this.estado = { dx: 0, dy: 0, falarApertou: false };
    this.antesFalar = false;
    this.base = null; // onde o dedo do joystick encostou
    this.toque = this.sys.game.device.input.touch;
    const j = PRACA.joystick;
    this.anel = this.add.circle(0, 0, j.raio, CORES.branco, 0.15).setStrokeStyle(2, CORES.branco, 0.6).setVisible(false);
    this.bolinha = this.add.circle(0, 0, 11, CORES.branco, 0.55).setVisible(false);
    const b = PRACA.botao;
    this.botao = this.add.container(b.x, b.y).setVisible(this.toque);
    this.botao.add(this.add.circle(0, 0, b.raio, CORES.lilas).setStrokeStyle(2, CORES.roxo));
    this.botao.add(
      this.add.text(0, 0, TEXTOS.praca.botao, { fontFamily: FONTES.titulo, fontSize: '7px', color: CORES_CSS.branco }).setOrigin(0.5),
    );
    this.botao.setAlpha(j.opacidade);
    const kb = this.input.keyboard;
    this.teclas = kb
      ? {
          esq: [kb.addKey(K.LEFT), kb.addKey(K.A)],
          dir: [kb.addKey(K.RIGHT), kb.addKey(K.D)],
          cima: [kb.addKey(K.UP), kb.addKey(K.W)],
          baixo: [kb.addKey(K.DOWN), kb.addKey(K.S)],
          falar: [kb.addKey(K.SPACE), kb.addKey(K.ENTER), kb.addKey(K.X), kb.addKey(K.J)],
        }
      : null;
  }

  update() {
    const j = PRACA.joystick;
    const b = PRACA.botao;
    let dx = 0;
    let dy = 0;
    let falar = false;
    let dedoJoystick = null;
    for (const p of this.input.manager.pointers) {
      if (!p || !p.isDown) continue;
      if (Phaser.Math.Distance.Between(p.x, p.y, b.x, b.y) < b.raio * 1.5) {
        falar = true;
      } else if (p.x < LARGURA / 2 && p.y > 40) {
        dedoJoystick = p;
      }
    }
    if (dedoJoystick) {
      if (!this.base || this.base.id !== dedoJoystick.id) this.base = { id: dedoJoystick.id, x: dedoJoystick.x, y: dedoJoystick.y };
      let vx = dedoJoystick.x - this.base.x;
      let vy = dedoJoystick.y - this.base.y;
      const d = Math.hypot(vx, vy);
      if (d > j.raio) {
        // o anel acompanha o dedo quando ele vai longe (não precisa voltar ao centro para mudar de direção)
        this.base.x += (vx / d) * (d - j.raio);
        this.base.y += (vy / d) * (d - j.raio);
        vx = dedoJoystick.x - this.base.x;
        vy = dedoJoystick.y - this.base.y;
      }
      if (d > j.zonaMorta) {
        dx = vx / j.raio;
        dy = vy / j.raio;
      }
      this.anel.setPosition(this.base.x, this.base.y).setVisible(true);
      this.bolinha.setPosition(dedoJoystick.x, dedoJoystick.y).setVisible(true);
    } else {
      this.base = null;
      this.anel.setVisible(false);
      this.bolinha.setVisible(false);
    }
    if (this.teclas) {
      const algum = (l) => l.some((k) => k.isDown);
      if (algum(this.teclas.esq)) dx = -1;
      if (algum(this.teclas.dir)) dx = 1;
      if (algum(this.teclas.cima)) dy = -1;
      if (algum(this.teclas.baixo)) dy = 1;
      if (algum(this.teclas.falar)) falar = true;
      // aperto rápido (tecla solta antes do quadro seguinte) também conta
      if (this.teclas.falar.some((k) => Phaser.Input.Keyboard.JustDown(k))) this.apertouTecla = true;
    }
    const m = Math.hypot(dx, dy);
    if (m > 1) {
      dx /= m;
      dy /= m;
    }
    this.botao.setAlpha(falar ? 0.8 : j.opacidade);
    this.estado = { dx, dy, falarApertou: (falar && !this.antesFalar) || !!this.apertouTecla };
    this.apertouTecla = false;
    this.antesFalar = falar;
  }

  // Depois de fechar um diálogo, o dedo/tecla que fechou não vale como novo "falar".
  ignorarAteSoltar() {
    this.antesFalar = true;
    this.apertouTecla = false;
    this.teclas?.falar.forEach((k) => Phaser.Input.Keyboard.JustDown(k)); // descarta o aperto que fechou a caixa
  }
}
