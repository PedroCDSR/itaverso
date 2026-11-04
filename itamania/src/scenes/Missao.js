import * as Phaser from 'phaser';
import { FONTES } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { Entrada } from '../ui/Entrada.js';
import { Botao } from '../ui/Botao.js';
import { estado } from '../estado.js';
import { MISSOES } from '../data/micromundos.js';
import { concluirMissao } from '../systems/encontros.js';
import { tocarEfeito } from '../audio/efeitos.js';
import { tocarMusica, tocarVinheta } from '../audio/musica.js';
import { abrirPausa } from '../fluxo.js';

export class Missao extends Phaser.Scene {
  constructor() { super('Missao'); }
  init(dados) {
    this.sessao = dados.sessao;
    this.def = MISSOES[this.sessao?.missao];
  }
  create() {
    if (!this.def || estado.encontros?.pendente?.token !== this.sessao.token) { this.scene.start('Praca'); return; }
    this.physics.resume();
    const d = this.def;
    this.terminou = false;
    this.vidas = 3;
    this.moedas = 0;
    this.checkpoint = 80;
    this.invencivelAte = 0;
    this.ultimoChao = -1000;
    this.pediuPulo = -1000;
    this.virado = false;
    this.cameras.main.setBackgroundColor('#c3e9e0');
    this.add.tileSprite(0, 0, 480, 270, 'sunny-ceu').setOrigin(0).setTileScale(1, 1.2).setScrollFactor(0).setDepth(-10);
    this.add.tileSprite(0, 80, d.largura, 190, 'sunny-montanhas').setOrigin(0).setAlpha(0.28).setScrollFactor(0.2, 1).setDepth(-8);
    this.add.tileSprite(0, -20, d.largura, 270, 'morros').setOrigin(0).setScrollFactor(0.12, 1).setDepth(-7);
    for (let x = 200; x < d.largura; x += 480) {
      this.add.image(x, 224, 'sunny-arvore').setOrigin(0.5, 1).setScrollFactor(0.8, 1).setDepth(-2);
      this.add.image(x + 120, 224, 'sunny-arbusto').setOrigin(0.5, 1).setDepth(-1);
    }
    // Marcos da praça conectam a aventura lateral ao mesmo lugar da exploração.
    for (const [chave, x, escala] of [['clube', 360, 0.7], ['cafe', 1280, 0.75], ['fonte', 2080, 0.75]]) {
      this.add.image(x, 224, chave).setOrigin(0.5, 1).setScale(escala).setDepth(-3);
    }
    const dados = Array.from({ length: 18 }, () => Array(d.largura / 16).fill(-1));
    for (let col = 0; col < dados[0].length; col++) {
      if (d.buracos.some(([a, b]) => col * 16 >= a && col * 16 < b)) continue;
      dados[14][col] = 26;
      for (let row = 15; row < 18; row++) dados[row][col] = 78;
    }
    const tm = this.make.tilemap({ data: dados, tileWidth: 16, tileHeight: 16 });
    this.chao = tm.createLayer(0, tm.addTilesetImage('sunny-terreno', 'sunny-terreno', 16, 16), 0, 0).setDepth(2);
    this.chao.setCollisionByExclusion([-1]);
    this.physics.world.setBounds(0, -100, d.largura, 600);
    this.physics.world.setBoundsCollision(true, true, false, false);
    this.jogador = this.physics.add.sprite(80, 218, 'capivara-exploradora', 8).setOrigin(0.5, 1).setDisplaySize(40, 40).setDepth(10);
    this.escala = this.jogador.scaleX;
    const lado = this.jogador.frame.width;
    this.jogador.body.setSize(lado * 0.6, lado * 0.55).setOffset(lado * 0.2, lado * 0.33);
    this.jogador.setCollideWorldBounds(true).setMaxVelocity(180, 560);
    this.physics.add.collider(this.jogador, this.chao);
    this.plataformas = this.physics.add.staticGroup();
    for (const [x, y, largura] of d.plataformas) {
      for (let dx = 0; dx < largura; dx += 32) this.plataformas.create(x + dx, y, 'sunny-plataforma').setOrigin(0, 0).refreshBody();
    }
    this.physics.add.collider(this.jogador, this.plataformas, undefined,
      (j, p) => j.body.velocity.y >= 0 && j.body.prev.y + j.body.height <= p.body.top + 8);
    this.itens = this.physics.add.group({ allowGravity: false });
    for (let x = 256; x < d.fim - 80; x += 144) {
      if (d.buracos.some(([a, b]) => x > a - 30 && x < b + 30)) continue;
      this.itens.create(x, 208, 'itacoin', 0).setScale(0.8).play('itacoin-girar');
    }
    for (const [x, y, largura] of d.plataformas) this.itens.create(x + largura / 2, y - 24, 'itacoin', 0).play('itacoin-girar');
    this.physics.add.overlap(this.jogador, this.itens, (_j, item) => {
      item.destroy(); this.moedas++; tocarEfeito('moeda', { volume: 0.5 });
      this.txtMoedas.setText(`${TEXTOS.missao.coleta}: ${this.moedas}`);
      this.poeira(this.jogador.x, this.jogador.y - 16, 0xffdf70);
    });
    this.inimigos = this.physics.add.group();
    for (const x of d.inimigos) {
      const s = this.inimigos.create(x, 220, 'sunny-gamba', 0).setOrigin(0.5, 1).play('gamba-andar');
      s.body.setSize(26, 18).setOffset(5, 10); s.inicio = x; s.lado = -1;
    }
    this.physics.add.collider(this.inimigos, this.chao);
    this.physics.add.overlap(this.jogador, this.inimigos, (j, i) => {
      if (this.terminou || this.time.now < this.invencivelAte || !i.active) return;
      if (j.body.velocity.y > 0 && j.body.prev.y + j.body.height < i.body.top + 12) {
        i.disableBody(true, true); j.setVelocityY(-270); tocarEfeito('pulo'); this.poeira(i.x, i.y, 0xffdf70);
      } else this.dano();
    });
    if (d.tipo === 'fuga') {
      this.perseguidor = this.physics.add.sprite(-100, 218, 'sunny-gamba', 0).setOrigin(0.5, 1).setDepth(9).play('gamba-andar');
      this.perseguidor.body.setSize(26, 18).setOffset(5, 10);
      this.physics.add.collider(this.perseguidor, this.chao);
      this.physics.add.overlap(this.jogador, this.perseguidor, () => this.dano());
    }
    for (const x of d.retornos.slice(1)) {
      this.add.image(x, 224, 'sunny-placa').setOrigin(0.5, 1).setDepth(3);
      this.add.text(x, 181, TEXTOS.missao.retorno, { fontFamily: FONTES.dialogo, fontSize: '11px', color: '#244633' }).setOrigin(0.5);
    }
    this.add.image(d.fim, 224, 'sunny-placa').setOrigin(0.5, 1).setDepth(3);
    this.add.text(d.fim, 178, TEXTOS.missao.saida, { fontFamily: FONTES.titulo, fontSize: '8px', color: '#244633' }).setOrigin(0.5);
    this.entrada = new Entrada(this);
    this.entrada.toque.esconderBotao('maca');
    this.add.rectangle(0, 0, 480, 38, 0x24394b, 0.85).setOrigin(0).setScrollFactor(0).setDepth(50);
    this.txtMoedas = this.add.text(12, 43, `${TEXTOS.missao.coleta}: 0`, { fontFamily: FONTES.dialogo, fontSize: '14px', color: '#244633', backgroundColor: '#fff2cc' }).setScrollFactor(0).setDepth(50);
    this.txtVidas = this.add.text(12, 10, '', { fontFamily: FONTES.titulo, fontSize: '8px', color: '#ffdc74' }).setScrollFactor(0).setDepth(50);
    this.add.text(160, 9, d.tipo === 'fuga' ? TEXTOS.missao.objetivoFuga : TEXTOS.missao.objetivo, { fontFamily: FONTES.dialogo, fontSize: '15px', color: '#ffffff' }).setScrollFactor(0).setDepth(50);
    this.progresso = this.add.rectangle(160, 29, 0, 3, 0xffdc74).setOrigin(0).setScrollFactor(0).setDepth(51);
    new Botao(this, 440, 18, TEXTOS.missao.pausar, () => this.pausar(), { largura: 58, altura: 22, tamanhoFonte: '7px' }).container.setDepth(60);
    this.registry.set('cenaJogo', 'Missao');
    this.input.keyboard.on('keydown-ESC', () => this.pausar());
    this.input.keyboard.on('keydown-P', () => this.pausar());
    this.atualizarVidas();
    const cam = this.cameras.main;
    cam.setBounds(0, 0, d.largura, 270).startFollow(this.jogador, true, 0.12, 0.12).setDeadzone(50, 70).setRoundPixels(true);
    cam.fadeIn(300);
    tocarMusica('centro');
    this.add.text(16, 237, this.sys.game.device.input.touch ? TEXTOS.missao.controlesToque : TEXTOS.missao.controles, { fontFamily: FONTES.dialogo, fontSize: '13px', color: '#ffffff', backgroundColor: '#24394b' }).setScrollFactor(0).setDepth(30);
    if (import.meta.env.DEV) window.missao = this;
  }
  atualizarVidas() { this.txtVidas.setText(`${TEXTOS.missao.folego}: ${this.vidas}/3`); }
  poeira(x, y, cor = 0xe8e0c9) {
    for (let k = 0; k < 5; k++) {
      const p = this.add.rectangle(x, y, 2, 2, cor).setDepth(12);
      this.tweens.add({ targets: p, x: x + Phaser.Math.Between(-15, 15), y: y - Phaser.Math.Between(4, 18), alpha: 0, duration: 350, onComplete: () => p.destroy() });
    }
  }
  dano() {
    if (this.terminou || this.time.now < this.invencivelAte) return;
    this.vidas--; this.atualizarVidas();
    tocarEfeito('dano', { volume: 0.4 }); this.cameras.main.shake(120, 0.003);
    this.invencivelAte = this.time.now + 1400;
    if (this.vidas <= 0) { this.finalizar(false); return; }
    this.jogador.body.reset(this.checkpoint, 218);
    this.perseguidor?.body.reset(this.checkpoint - 180, 218);
    this.jogador.setVelocity(0);
    this.ultimoChao = -1000; this.pediuPulo = -1000;
  }
  abandonar() {
    if (this.terminou) return;
    concluirMissao(this.sessao.token, false);
    this.scene.start('Praca');
  }
  pausar() { if (!this.terminou) abrirPausa(this); }
  finalizar(venceu) {
    if (this.terminou) return;
    this.terminou = true;
    this.jogador.setVelocity(0); this.physics.pause();
    const resultado = concluirMissao(this.sessao.token, venceu, this.moedas);
    if (!resultado) { this.scene.start('Praca'); return; }
    if (venceu) tocarVinheta('vitoria');
    this.add.rectangle(240, 135, 400, 148, 0x24394b, 0.96).setScrollFactor(0).setDepth(2000).setStrokeStyle(2, 0xffdc74);
    this.add.text(240, 84, venceu ? TEXTOS.missao.vitoria : TEXTOS.missao.derrota, { fontFamily: FONTES.titulo, fontSize: '12px', color: '#ffdc74' }).setOrigin(0.5).setScrollFactor(0).setDepth(2001);
    this.add.text(240, 119, venceu ? TEXTOS.missao.premio.replace('{n}', resultado.premio) : TEXTOS.missao.semPerda, { fontFamily: FONTES.dialogo, fontSize: '18px', color: '#ffffff' }).setOrigin(0.5).setScrollFactor(0).setDepth(2001);
    const voltar = () => this.scene.start('Praca');
    new Botao(this, 240, 166, TEXTOS.missao.voltar, voltar, { largura: 220, altura: 30, cor: 'amarelo' }).container.setDepth(2001);
    this.input.keyboard.once('keydown-ENTER', voltar);
  }
  update(t, dt) {
    if (!this.jogador || this.terminou) return;
    this.entrada.atualizar();
    const j = this.jogador, e = this.entrada;
    const noChao = j.body.blocked.down || j.body.touching.down;
    if (noChao) this.ultimoChao = t;
    if (e.pularApertou) this.pediuPulo = t;
    const alvo = e.esquerda ? -160 : e.direita ? 160 : 0;
    const passo = (noChao ? 1500 : 950) * dt / 1000;
    j.setVelocityX(j.body.velocity.x + Math.sign(alvo - j.body.velocity.x) * Math.min(Math.abs(alvo - j.body.velocity.x), passo));
    if (alvo) this.virado = alvo < 0;
    j.setFlipX(this.virado);
    if (t - this.pediuPulo < 110 && t - this.ultimoChao < 110) {
      j.setVelocityY(-370); this.pediuPulo = -1000; this.ultimoChao = -1000;
      this.pulando = true; tocarEfeito('pulo', { volume: 0.35 }); this.poeira(j.x, j.y - 3);
    }
    if (this.pulando && !e.pular && j.body.velocity.y < -100) { j.setVelocityY(j.body.velocity.y * 0.5); this.pulando = false; }
    if (noChao && !this.estavaNoChao) this.poeira(j.x, j.y - 2);
    this.estavaNoChao = noChao;
    const andando = Math.abs(j.body.velocity.x) > 10;
    j.play(`exploradora-${andando && noChao ? 'andar' : 'parado'}-direita`, true);
    // O corpo mantém tamanho constante; a inclinação comunica subida e descida sem deslocar a hitbox.
    j.setAngle(noChao ? 0 : j.body.velocity.y < 0 ? (this.virado ? 7 : -7) : (this.virado ? -5 : 5));
    j.setAlpha(t < this.invencivelAte && Math.floor(t / 90) % 2 ? 0.35 : 1);
    if (noChao) for (const x of this.def.retornos) if (j.x >= x && x > this.checkpoint) { this.checkpoint = x; tocarEfeito('moeda', { volume: 0.3 }); }
    for (const i of this.inimigos.getChildren()) {
      if (!i.active) continue;
      if (i.x < i.inicio - 42 || i.body.blocked.left) i.lado = 1;
      if (i.x > i.inicio + 42 || i.body.blocked.right) i.lado = -1;
      i.setVelocityX(i.lado * 32).setFlipX(i.lado > 0);
    }
    if (this.perseguidor) {
      const p = this.perseguidor;
      p.setVelocityX(112).setFlipX(true);
      const chaoFrente = this.chao.getTileAtWorldXY(p.x + 34, 230);
      if (p.body.blocked.down && (!chaoFrente || chaoFrente.index === -1)) p.setVelocityY(-365);
      if (p.y > 340) p.body.reset(Math.max(0, this.checkpoint - 180), 218);
    }
    this.progresso.width = 220 * Phaser.Math.Clamp(j.x / this.def.fim, 0, 1);
    if (andando && noChao && t > (this.proximaPoeira || 0)) { this.proximaPoeira = t + 160; this.poeira(j.x, j.y - 2); }
    if (j.y > 320) this.dano();
    if (j.x >= this.def.fim && noChao) this.finalizar(true);
  }
}
