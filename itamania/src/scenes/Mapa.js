import * as Phaser from 'phaser';
import { LARGURA, ALTURA, CORES, CORES_CSS, FONTES } from '../config.js';
import { TEXTOS, NOMES_FASES } from '../data/textos.js';
import { FASES } from '../levels/index.js';
import { Botao } from '../ui/Botao.js';
import { BotaoSom } from '../ui/BotaoSom.js';
import { estado } from '../estado.js';
import { heroi } from '../genero.js';
import { tocarMusica } from '../audio/musica.js';
import { tocarEfeito } from '../audio/efeitos.js';

// Mapa-múndi em pé, de baixo para cima (DESIGN.md). O mapa pronto do Pedro entra em public/assets/mapa.png
// (480 px de largura); sem ele, este mapa é desenhado em código (provisório) com o Rio Sapucaí, a Av. BPS e os
// bairros. Arrastar sobe e desce; tocar numa fase liberada entra nela.
const ALTURA_MAPA = 1040;

// Posição de cada fase no mapa (x, y), da 1 (embaixo) à 14 (em cima).
const PONTOS = [
  null,
  [120, 980], [250, 915], [360, 850], [250, 780], [110, 715], [190, 640], [330, 580],
  [400, 500], [270, 430], [120, 360], [210, 280], [350, 215], [230, 140], [240, 64],
];

export class Mapa extends Phaser.Scene {
  constructor() {
    super('Mapa');
  }

  create() {
    tocarMusica('mapa');
    const cam = this.cameras.main;
    cam.setBounds(0, 0, LARGURA, ALTURA_MAPA);
    if (this.textures.exists('mapa-mundi') && this.textures.get('mapa-mundi').key !== '__MISSING') {
      this.add.image(0, 0, 'mapa-mundi').setOrigin(0);
    } else {
      this.desenharMapa();
    }
    this.desenharCaminho();
    this.marcadores = [];
    for (let n = 1; n <= 14; n++) this.criarMarcador(n);

    // herói em cima da última fase liberada
    const alvo = Math.min(estado.liberada, 14);
    const [hx, hy] = PONTOS[alvo];
    this.heroi = this.add.sprite(hx, hy - 8, `heroi-${heroi()}-normal`, 0).setOrigin(0.5, 1).setDepth(20);
    this.heroi.play(`${heroi()}-normal-${estado.bone ? 'b' : 's'}-parado`);
    cam.scrollY = Phaser.Math.Clamp(hy - ALTURA / 2 - 20, 0, ALTURA_MAPA - ALTURA);

    // cabeçalho fixo
    this.add.rectangle(0, 0, LARGURA, 30, CORES.roxo, 0.8).setOrigin(0).setScrollFactor(0).setDepth(50);
    this.add.text(12, 10, TEXTOS.mapa.titulo, { fontFamily: FONTES.titulo, fontSize: '10px', color: CORES_CSS.amarelo }).setScrollFactor(0).setDepth(51);
    this.add.text(LARGURA / 2 + 10, 15, TEXTOS.mapa.dica, { fontFamily: FONTES.dialogo, fontSize: '14px', color: CORES_CSS.branco }).setOrigin(0.5).setScrollFactor(0).setDepth(51);
    new BotaoSom(this, LARGURA - 20, 15);
    const b = new Botao(this, 52, ALTURA - 18, 'INÍCIO', () => this.scene.start('Titulo'), { largura: 84, altura: 20, tamanhoFonte: '7px' });
    b.setDepth(52);

    // arrastar para rolar
    this.input.on('pointermove', (p) => {
      if (!p.isDown) return;
      const dy = p.prevPosition.y - p.position.y;
      cam.scrollY = Phaser.Math.Clamp(cam.scrollY + dy, 0, ALTURA_MAPA - ALTURA);
      if (Math.abs(p.position.y - p.downY) > 6) this.arrastou = true;
    });
    this.input.on('pointerdown', () => (this.arrastou = false));
    this.input.on('wheel', (p, objs, dx, dy) => (cam.scrollY = Phaser.Math.Clamp(cam.scrollY + dy * 0.5, 0, ALTURA_MAPA - ALTURA)));
    this.input.keyboard?.on('keydown-UP', () => (cam.scrollY = Math.max(0, cam.scrollY - 40)));
    this.input.keyboard?.on('keydown-DOWN', () => (cam.scrollY = Math.min(ALTURA_MAPA - ALTURA, cam.scrollY + 40)));
    this.input.keyboard?.on('keydown-ENTER', () => this.entrar(Math.min(estado.liberada, 4)));
    cam.fadeIn(300);
  }

  // Mapa provisório em pixel art feito com formas: verde da serra, rio, avenidas, quarteirões e bairros.
  desenharMapa() {
    const g = this.add.graphics();
    g.fillStyle(0x7cc85a).fillRect(0, 0, LARGURA, ALTURA_MAPA);
    // morros da Mantiqueira nas bordas
    const rnd = new Phaser.Math.RandomDataGenerator(['itajuba']);
    for (let i = 0; i < 60; i++) {
      const x = rnd.pick([rnd.between(-20, 70), rnd.between(410, 500)]);
      const y = rnd.between(0, ALTURA_MAPA);
      const r = rnd.between(18, 40);
      g.fillStyle(0x4f9c44).fillCircle(x, y, r);
      g.fillStyle(0x68b04e).fillCircle(x - r * 0.25, y - r * 0.25, r * 0.6);
    }
    // quarteirões com casinhas
    for (let y = 30; y < ALTURA_MAPA - 20; y += 34) {
      for (let x = 80; x < 400; x += 38) {
        if (rnd.frac() < 0.35) continue;
        g.fillStyle(0xe8dcc4).fillRect(x, y, 30, 24);
        for (let k = 0; k < 3; k++) {
          const cx = x + 3 + k * 9;
          g.fillStyle(rnd.pick([0xf3e3c3, 0xefc2c9, 0xcfe0e8, 0xf6d7a8])).fillRect(cx, y + 9, 7, 8);
          g.fillStyle(0xc9623e).fillRect(cx - 1, y + 6, 9, 4);
        }
      }
    }
    // Rio Sapucaí: serpenteia de baixo para cima, com a Av. BPS dos dois lados
    const pts = [];
    for (let y = ALTURA_MAPA + 10; y >= -10; y -= 20) pts.push(new Phaser.Math.Vector2(300 + Math.sin(y / 120) * 70, y));
    const rio = new Phaser.Curves.Spline(pts);
    g.lineStyle(26, 0xd8d0c0).strokePoints(rio.getPoints(120));
    g.lineStyle(16, 0x3d8fd8).strokePoints(rio.getPoints(120));
    g.lineStyle(4, 0x8fd0f2).strokePoints(rio.getPoints(120).map((p) => new Phaser.Math.Vector2(p.x - 4, p.y)));
    // 7 pontes da Av. BPS
    for (let i = 0; i < 7; i++) {
      const y = 140 + i * 120;
      const x = 300 + Math.sin(y / 120) * 70;
      g.fillStyle(0xbab2b4).fillRect(x - 20, y - 3, 40, 6);
      g.fillStyle(0x948a96).fillRect(x - 20, y + 3, 40, 2);
    }
    const rotulo = (x, y, t) =>
      this.add.text(x, y, t, { fontFamily: FONTES.titulo, fontSize: '7px', color: CORES_CSS.branco }).setOrigin(0.5).setShadow(1, 1, '#2B2D5C', 0, false, true);
    rotulo(300, 1020, 'RIO SAPUCAÍ');
    rotulo(170, 830, 'CENTRO');
    rotulo(390, 650, 'BPS');
    rotulo(330, 470, 'AV. BPS');
    rotulo(140, 560, 'VARGINHA');
    rotulo(180, 330, 'CRUZEIRO');
  }

  desenharCaminho() {
    const g = this.add.graphics().setDepth(5);
    for (let n = 1; n < 14; n++) {
      const [x0, y0] = PONTOS[n];
      const [x1, y1] = PONTOS[n + 1];
      const passos = Math.floor(Phaser.Math.Distance.Between(x0, y0, x1, y1) / 8);
      for (let i = 1; i < passos; i++) {
        const t = i / passos;
        g.fillStyle(n < estado.liberada ? 0xffd43a : 0xffffff, n < estado.liberada ? 1 : 0.6).fillRect(x0 + (x1 - x0) * t - 1.5, y0 + (y1 - y0) * t - 1.5, 3, 3);
      }
    }
  }

  criarMarcador(n) {
    const [x, y] = PONTOS[n];
    const feita = estado.feitas.includes(n);
    const liberada = n <= estado.liberada;
    const existe = !!FASES[n];
    const cor = feita ? CORES.amarelo : liberada && existe ? CORES.laranja : 0x9a9ab8;
    const c = this.add.container(x, y).setDepth(10);
    c.add(this.add.circle(1, 2, 13, 0x000000, 0.3));
    c.add(this.add.circle(0, 0, 13, cor).setStrokeStyle(2, CORES.roxo));
    c.add(this.add.text(0, 1, String(n), { fontFamily: FONTES.titulo, fontSize: '9px', color: CORES_CSS.roxo }).setOrigin(0.5));
    const nome = this.add
      .text(x, y + 20, NOMES_FASES[n], { fontFamily: FONTES.dialogo, fontSize: '13px', color: CORES_CSS.branco, backgroundColor: '#2B2D5CAA', padding: { x: 3, y: 0 } })
      .setOrigin(0.5)
      .setDepth(11);
    if (liberada && existe && !feita) this.tweens.add({ targets: c, scale: 1.15, duration: 500, yoyo: true, repeat: -1 });
    const zona = this.add.zone(x, y, 40, 40).setInteractive({ useHandCursor: true }).setDepth(12);
    zona.on('pointerup', () => !this.arrastou && this.entrar(n));
    this.marcadores.push({ c, nome });
  }

  entrar(n) {
    if (!FASES[n] || n > estado.liberada) {
      tocarEfeito('dano', { volume: 0.4 });
      const [x, y] = PONTOS[n];
      const t = this.add
        .text(x, y - 26, FASES[n] ? 'Termine a fase anterior!' : TEXTOS.mapa.embreve, { fontFamily: FONTES.dialogo, fontSize: '14px', color: CORES_CSS.amarelo })
        .setOrigin(0.5)
        .setDepth(30)
        .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
      this.tweens.add({ targets: t, y: y - 40, alpha: 0, delay: 700, duration: 500, onComplete: () => t.destroy() });
      return;
    }
    tocarEfeito('botao');
    const [x, y] = PONTOS[n];
    this.heroi.play(`${heroi()}-normal-${estado.bone ? 'b' : 's'}-correndo`);
    this.heroi.setFlipX(x < this.heroi.x);
    this.tweens.add({
      targets: this.heroi,
      x,
      y: y - 8,
      duration: 400,
      onComplete: () => {
        this.cameras.main.fadeOut(250);
        this.cameras.main.once('camerafadeoutcomplete', () => this.scene.start('Fase', { fase: n }));
      },
    });
  }
}
