import * as Phaser from 'phaser';
import { FONTES, MISSAO_URBANA as FISICA } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { Entrada } from '../ui/Entrada.js';
import { Botao } from '../ui/Botao.js';
import { estado } from '../estado.js';
import { MISSOES } from '../data/micromundos.js';
import { APOIOS_URBANOS, FICHAS_URBANAS, chaoUrbano, tocaCalcada } from '../data/missaoUrbana.js';
import { PontosMissao } from '../systems/pontosMissao.js';
import { desenharCidade, bandeira } from '../ui/cenarioMissaoUrbana.js';
import { concluirMissao } from '../systems/encontros.js';
import { tocarEfeito } from '../audio/efeitos.js';
import { tocarMusica, tocarVinheta } from '../audio/musica.js';
import { abrirPausa } from '../fluxo.js';

export class Missao extends Phaser.Scene {
  constructor() { super('Missao'); }
  init(dados) { this.sessao = dados?.sessao; this.def = MISSOES[this.sessao?.missao]; }
  create() {
    if (!this.def || estado.encontros?.pendente?.token !== this.sessao?.token) { this.scene.start('Praca'); return; }
    this.physics.resume();
    this.terminou = false; this.vidas = FISICA.vidas; this.placar = new PontosMissao();
    this.checkpoint = this.def.inicio; this.invencivelAte = 0;
    this.ultimoChao = this.pediuPulo = -1000; this.virado = this.pulando = this.quicando = false;
    this.estavaNoChao = false; this.proximaPoeira = 0; this.setorAtual = null;
    desenharCidade(this);
    this.physics.world.setBounds(0, 0, this.def.largura, this.def.altura);
    this.physics.world.setBoundsCollision(true, true, false, false);
    this.jogador = this.physics.add.sprite(this.checkpoint, chaoUrbano(this.checkpoint), 'capivara-exploradora', 8)
      .setOrigin(0.5, 1).setDisplaySize(40, 40).setDepth(10);
    const lado = this.jogador.frame.width;
    // Patas encostam na calçada; a mochila não interfere na colisão da missão.
    this.jogador.body.setSize(lado * 0.6, lado * 0.55).setOffset(lado * 0.2, lado * 0.37);
    this.jogador.setCollideWorldBounds(true).setMaxVelocity(180, 560);
    this.plataformas = this.physics.add.staticGroup();
    for (const p of APOIOS_URBANOS) {
      const apoio = this.add.rectangle(p.x, p.y, p.largura, 8, 0xffffff, 0).setOrigin(0);
      this.plataformas.add(apoio); apoio.body.updateFromGameObject(); apoio.setData('apoio', p);
    }
    this.physics.add.collider(this.jogador, this.plataformas, (_j, p) => {
      if (p.getData('apoio').tipo === 'toldo' && this.jogador.body.velocity.y >= 0) this.quicarToldo();
    }, (j, p) => j.body.velocity.y >= 0 && j.body.prev.y + j.body.height <= p.body.top + 5);
    this.itens = this.physics.add.group({ allowGravity: false });
    for (const f of FICHAS_URBANAS) {
      const item = this.itens.create(f.x, f.y, f.valor === 50 ? 'urbano-estrela' : 'urbano-ficha');
      item.setData('ficha', f); item.body.setCircle(f.valor === 50 ? 10 : 7);
    }
    this.physics.add.overlap(this.jogador, this.itens, (_j, item) => this.coletar(item));
    this.inimigos = this.physics.add.group({ allowGravity: false });
    for (const x of this.def.pombos) {
      const i = this.inimigos.create(x, chaoUrbano(x), 'pombo', 0).setOrigin(0.5, 1).setDepth(7).play('pombo-andar');
      i.body.setSize(18, 12).setOffset(6, 12); i.inicio = x; i.lado = -1; i.saiu = false;
    }
    this.physics.add.overlap(this.jogador, this.inimigos, (j, i) => {
      if (this.terminou || i.saiu || this.time.now < this.invencivelAte) return;
      if (j.body.velocity.y > 0 && j.body.prev.y + j.body.height < i.body.top + 12) {
        i.saiu = true; i.body.enable = false; i.play('pombo-voar');
        this.tweens.add({ targets: i, x: i.x + 100, y: i.y - 140, alpha: 0, duration: 650, onComplete: () => i.destroy() });
        j.setVelocityY(-250); tocarEfeito('pulo', { volume: 0.3 });
      } else this.dano();
    });
    if (this.def.tipo === 'fuga') {
      this.perseguidor = this.physics.add.sprite(0, chaoUrbano(0), 'sunny-gamba', 0)
        .setOrigin(0.5, 1).setDepth(9).play('gamba-andar').setFlipX(true);
      this.perseguidor.body.setAllowGravity(false).setSize(26, 18).setOffset(5, 10);
      this.physics.add.overlap(this.jogador, this.perseguidor, () => this.dano());
    } else this.perseguidor = null;
    // O Arcade resolve os apoios; só a superfície inclinada precisa desta resolução analítica.
    this.resolverCalcada = () => {
      const b = this.jogador.body;
      if (this.terminou || !b.enable) return;
      if (tocaCalcada({ x: b.center.x, anteriorX: b.prev.x + b.halfWidth,
        fundo: b.bottom, fundoAnterior: b.prev.y + b.height, velocidadeY: b.velocity.y, alturaCorpo: b.height })) {
        b.position.y = chaoUrbano(b.center.x) - b.height;
        b.velocity.y = 0; b.blocked.down = true; b.touching.down = true; b.updateCenter();
      }
    };
    this.physics.world.on('worldstep', this.resolverCalcada);
    this.events.once('shutdown', () => {
      this.physics.world.off('worldstep', this.resolverCalcada);
      if (import.meta.env.DEV && window.missao === this) delete window.missao;
    });
    bandeira(this, 48, TEXTOS.missao.urbano.inicio, true);
    this.def.retornos.slice(1).forEach((x, i) => bandeira(this, x, `C${i + 1}`));
    bandeira(this, this.def.fim + 22, TEXTOS.missao.saida, true);
    this.criarInterface();
    const cam = this.cameras.main;
    cam.setBounds(0, 0, this.def.largura, this.def.altura).startFollow(this.jogador, true, 0.12, 0.12)
      .setFollowOffset(-45, 80).setDeadzone(36, 24).setRoundPixels(true);
    cam.scrollX = 0; cam.scrollY = chaoUrbano(80) - 215; cam.fadeIn(300);
    tocarMusica('centro'); this.aviso(TEXTOS.missao.urbano.dica);
    if (import.meta.env.DEV) window.missao = this;
  }
  criarInterface() {
    const t = TEXTOS.missao;
    this.entrada = new Entrada(this); this.entrada.toque.esconderBotao('maca');
    this.add.rectangle(0, 0, 480, 42, 0x24394b, 0.94).setOrigin(0).setScrollFactor(0).setDepth(50);
    const estilo = { fontFamily: FONTES.dialogo, fontSize: '14px', color: '#ffffff' };
    this.txtPontos = this.add.text(12, 5, `${t.coleta}: 0`, { ...estilo, color: '#ffe295' }).setScrollFactor(0).setDepth(51);
    this.txtVidas = this.add.text(12, 24, '', { ...estilo, fontSize: '11px' }).setScrollFactor(0).setDepth(51);
    this.txtSetor = this.add.text(160, 5, t.objetivo, estilo).setScrollFactor(0).setDepth(51);
    this.progresso = this.add.rectangle(160, 32, 0, 3, 0xffdc74).setOrigin(0).setScrollFactor(0).setDepth(51);
    this.add.rectangle(160, 32, 220, 3, 0xffffff, 0.2).setOrigin(0).setScrollFactor(0).setDepth(50);
    new Botao(this, 440, 20, t.pausar, () => this.pausar(), { largura: 58, altura: 24, tamanhoFonte: '7px' }).container.setDepth(60);
    this.txtAviso = this.add.text(240, 53, '', { ...estilo, fontSize: '13px', color: '#344652', backgroundColor: '#fff0cd', padding: { x: 6, y: 4 }, wordWrap: { width: 365 } })
      .setOrigin(0.5, 0).setScrollFactor(0).setDepth(60);
    this.registry.set('cenaJogo', 'Missao');
    this.input.keyboard.on('keydown-ESC', () => this.pausar());
    this.input.keyboard.on('keydown-P', () => this.pausar());
    this.atualizarVidas();
  }
  atualizarVidas() { this.txtVidas.setText(`${TEXTOS.missao.folego}: ${this.vidas}/${FISICA.vidas}`); }
  aviso(texto) {
    this.avisoTimer?.remove(); this.txtAviso.setText(texto).setVisible(true);
    this.avisoTimer = this.time.delayedCall(3200, () => this.txtAviso.setVisible(false));
  }
  coletar(item) {
    const f = item.getData('ficha'), resultado = this.placar.coletar(f.id);
    if (!resultado) return;
    item.destroy(); this.txtPontos.setText(`${TEXTOS.missao.coleta}: ${resultado.pontos}`);
    tocarEfeito(resultado.bonus ? 'pegarItem' : 'moeda', { volume: 0.4 });
    const txt = this.add.text(f.x, f.y - 10, `+${resultado.valor}`, {
      fontFamily: FONTES.dialogo, fontSize: '14px', color: '#fff2b1', stroke: '#65533f', strokeThickness: 3,
    }).setOrigin(0.5).setDepth(15);
    this.tweens.add({ targets: txt, y: txt.y - 24, alpha: 0, duration: 700, onComplete: () => txt.destroy() });
    this.poeira(f.x, f.y, 0xffdf70);
    if (resultado.bonus) this.aviso(TEXTOS.missao.urbano.sequencia);
  }
  quicarToldo() {
    this.jogador.setVelocityY(-FISICA.puloToldo); this.quicando = true; this.pulando = false;
    this.ultimoChao = this.pediuPulo = -1000;
    this.tweens.add({ targets: this.toldoVisual, scaleY: 0.65, yoyo: true, duration: 100 });
    tocarEfeito('toldo', { volume: 0.5 }); this.aviso(TEXTOS.missao.urbano.quique);
  }
  poeira(x, y, cor = 0xe8e0c9) {
    for (let k = 0; k < 4; k++) {
      const p = this.add.rectangle(x, y, 2, 2, cor).setDepth(12);
      this.tweens.add({ targets: p, x: x + Phaser.Math.Between(-12, 12), y: y - Phaser.Math.Between(4, 15), alpha: 0, duration: 300, onComplete: () => p.destroy() });
    }
  }
  dano() {
    if (this.terminou || this.time.now < this.invencivelAte) return;
    this.vidas--; this.atualizarVidas(); tocarEfeito('dano', { volume: 0.35 });
    this.cameras.main.shake(100, 0.002); this.invencivelAte = this.time.now + FISICA.invencivelMs;
    if (this.vidas <= 0) { this.finalizar(false); return; }
    this.jogador.body.reset(this.checkpoint, chaoUrbano(this.checkpoint) - 3);
    this.jogador.setVelocity(0); this.jogador.setAngle(0);
    if (this.perseguidor) this.perseguidor.body.reset(Math.max(0, this.checkpoint - 200), chaoUrbano(this.checkpoint - 200));
    this.ultimoChao = this.pediuPulo = -1000; this.pulando = this.quicando = false;
  }
  abandonar() {
    if (this.terminou) return;
    this.terminou = true; concluirMissao(this.sessao.token, false); this.scene.start('Praca');
  }
  pausar() { if (!this.terminou) abrirPausa(this); }
  finalizar(venceu) {
    if (this.terminou) return;
    this.terminou = true; this.jogador.setVelocity(0); this.physics.pause(); this.txtAviso.setVisible(false);
    const r = concluirMissao(this.sessao.token, venceu, this.placar.pontos);
    if (!r) { this.scene.start('Praca'); return; }
    if (venceu) tocarVinheta('vitoria');
    const t = TEXTOS.missao;
    this.add.rectangle(240, 135, 432, 196, 0x24394b, 0.98).setScrollFactor(0).setDepth(2000).setStrokeStyle(2, 0xffdc74);
    const texto = (y, txt, tamanho, cor = '#ffffff') => this.add.text(240, y, txt, { fontFamily: FONTES.dialogo, fontSize: `${tamanho}px`, color: cor }).setOrigin(0.5).setScrollFactor(0).setDepth(2001);
    texto(61, venceu ? t.vitoria : t.derrota, 23, '#ffdc74');
    texto(89, `${t.coleta}: ${this.placar.pontos}   ·   ${t.urbano.recorde.replace('{n}', r.recorde)}`, 17);
    texto(115, venceu ? t.urbano.medalhas.replace('{n}', r.medalhas) : t.semPerda, 16);
    texto(143, venceu ? (r.premio ? t.premio.replace('{n}', r.premio) : t.urbano.semPremio) : t.semPerda, 15);
    const voltar = () => this.scene.start('Praca');
    new Botao(this, 240, 193, t.voltar, voltar, { largura: 230, altura: 30, cor: 'amarelo' }).container.setDepth(2001);
    this.input.keyboard.once('keydown-ENTER', voltar);
  }
  update(t, dt) {
    if (!this.jogador || this.terminou) return;
    this.entrada.atualizar();
    const j = this.jogador, e = this.entrada;
    const noChao = j.body.blocked.down || j.body.touching.down;
    if (noChao && !this.quicando) this.ultimoChao = t;
    if (e.pularApertou) this.pediuPulo = t;
    const alvo = e.esquerda ? -FISICA.velocidade : e.direita ? FISICA.velocidade : 0;
    const passo = (noChao ? FISICA.aceleracaoChao : FISICA.aceleracaoAr) * Math.min(dt, 50) / 1000;
    j.setVelocityX(j.body.velocity.x + Math.sign(alvo - j.body.velocity.x) * Math.min(Math.abs(alvo - j.body.velocity.x), passo));
    if (alvo) this.virado = alvo < 0;
    j.setFlipX(this.virado);
    if (t - this.pediuPulo < FISICA.bufferMs && t - this.ultimoChao < FISICA.coyoteMs && !this.quicando) {
      j.setVelocityY(-FISICA.pulo); this.pediuPulo = this.ultimoChao = -1000;
      this.pulando = true; tocarEfeito('pulo', { volume: 0.35 }); this.poeira(j.x, j.y - 3);
    }
    if (this.pulando && !e.pular && j.body.velocity.y < -100) { j.setVelocityY(j.body.velocity.y * FISICA.cortePulo); this.pulando = false; }
    if (this.quicando && j.body.velocity.y > 0) this.quicando = false;
    if (noChao && !this.estavaNoChao && !this.quicando) this.poeira(j.x, j.y - 2);
    this.estavaNoChao = noChao;
    const andando = Math.abs(j.body.velocity.x) > 10;
    j.play(`exploradora-${andando && noChao ? 'andar' : 'parado'}-direita`, true);
    j.setAngle(noChao ? 0 : j.body.velocity.y < 0 ? (this.virado ? 6 : -6) : (this.virado ? -4 : 4));
    j.setAlpha(t < this.invencivelAte && Math.floor(t / 90) % 2 ? 0.35 : 1);
    if (noChao && Math.abs(j.body.bottom - chaoUrbano(j.x)) < 12) {
      for (const x of this.def.retornos) if (j.x >= x && x > this.checkpoint) {
        this.checkpoint = x; tocarEfeito('pegarItem', { volume: 0.3 }); this.aviso(TEXTOS.missao.urbano.checkpoint);
      }
    }
    for (const i of this.inimigos.getChildren()) {
      if (!i.active || i.saiu) continue;
      if (i.x < i.inicio - 36) i.lado = 1;
      if (i.x > i.inicio + 36) i.lado = -1;
      i.setVelocityX(i.lado * FISICA.velocidadePombo).setFlipX(i.lado > 0); i.y = chaoUrbano(i.x);
    }
    if (this.perseguidor) {
      this.perseguidor.setVelocityX(FISICA.velocidadePerseguidor); this.perseguidor.y = chaoUrbano(this.perseguidor.x);
    }
    let setor = this.def.setores[0][1];
    for (const [x, nome] of this.def.setores) if (j.x >= x) setor = nome;
    if (setor !== this.setorAtual) { this.setorAtual = setor; this.txtSetor.setText(TEXTOS.missao.urbano.setores[setor]); }
    this.progresso.width = 220 * Phaser.Math.Clamp(j.x / this.def.fim, 0, 1);
    if (andando && noChao && t > this.proximaPoeira) { this.proximaPoeira = t + 180; this.poeira(j.x, j.y - 2); }
    if (j.y > chaoUrbano(j.x) + 96) this.dano();
    if (j.x >= this.def.fim && noChao && Math.abs(j.body.bottom - chaoUrbano(j.x)) < 12) this.finalizar(true);
  }
}
