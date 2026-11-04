import * as Phaser from 'phaser';
import { CORES_CSS, PRACA } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { nomeVaga } from '../data/vagas.js';
import { estado, salvar } from '../estado.js';
import { heroi, nomeHeroi, g } from '../genero.js';
import { Dialogo } from '../ui/Dialogo.js';
import { tocarEfeito } from '../audio/efeitos.js';
import { tocarMusica, pararMusica } from '../audio/musica.js';
import { abrirPausa } from '../fluxo.js';

// Praça Theodomiro Santiago andável, vista de cima (o começo do Centro explorável).
// Mapa no formato do Tiled (public/assets/mapas/praca.tmj, gerado por ferramentas/mapas/gerar_praca.py e editável no
// Tiled). Arte: pacote Ninja Adventure (CC0). Personagens do pacote: 16x16, colunas = baixo, cima, esquerda, direita;
// linhas 0 a 3 = passos.
const DIRS = ['baixo', 'cima', 'esquerda', 'direita'];

// Texto com as marcações de gênero e os nomes das vagas (lugares reais autorizados ou genéricos).
function texto(t) {
  return g(t.replace('{cafe}', nomeVaga('cafe')).replace('{lanchonete}', nomeVaga('lanchonete')));
}

export class Praca extends Phaser.Scene {
  constructor() {
    super({ key: 'Praca', physics: { arcade: { gravity: { x: 0, y: 0 } } } });
  }

  create() {
    this.ocupado = false;
    this.saindo = false;
    const mapa = this.make.tilemap({ key: 'praca' });
    const tilesets = mapa.tilesets.map((t) => mapa.addTilesetImage(t.name, `ninja-${t.name}`));
    const camada = (nome, prof) => mapa.createLayer(nome, tilesets, 0, 0).setDepth(prof);
    camada('chao', 0);
    camada('agua', 1);
    camada('objetos', 2);
    camada('cima', 5000);
    this.colisao = camada('colisao', 0).setVisible(false);
    this.colisao.setCollisionByExclusion([-1]);
    this.physics.world.setBounds(0, 0, mapa.widthInPixels, mapa.heightInPixels);

    // pontos do mapa (camada de objetos do Tiled)
    const pontos = mapa.getObjectLayer('pontos').objects.map((o) => ({
      tipo: o.type,
      x: o.x,
      y: o.y,
      ...Object.fromEntries((o.properties || []).map((p) => [p.name, p.value])),
    }));
    const inicio = pontos.find((p) => p.tipo === 'inicio');

    // herói (personagem do pacote no lugar do desenho do Pedro, até existir a versão vista de cima)
    this.chaveHeroi = PRACA.heroi[heroi()];
    this.heroi = this.physics.add.sprite(inicio.x, inicio.y, `ninja-${this.chaveHeroi}`, 1);
    this.heroi.setOrigin(0.5, 1).setCollideWorldBounds(true);
    this.heroi.body.setSize(10, 6).setOffset(3, 10);
    this.direcao = 'cima';
    this.physics.add.collider(this.heroi, this.colisao);

    // moradores, placas e fonte (tudo com que se conversa)
    this.alvos = [];
    this.npcs = this.physics.add.group({ immovable: true });
    for (const p of pontos.filter((q) => q.tipo === 'npc')) {
      const s = this.npcs.create(p.x, p.y, `ninja-${p.sprite}`, 0).setOrigin(0.5, 1);
      s.body.setSize(10, 6).setOffset(3, 10);
      s.dados = p;
      s.chave = p.sprite;
      s.direcao = 'baixo';
      if (p.anda) this.passear(s);
      this.alvos.push({ x: p.x, y: p.y - 4, fala: p.fala, npc: s, balao: this.balao(s, 'reticencias') });
    }
    this.physics.add.collider(this.heroi, this.npcs);
    for (const p of pontos.filter((q) => q.tipo === 'placa' || q.tipo === 'fonte')) {
      this.alvos.push({ x: p.x, y: p.y, fala: p.fala });
    }
    const gatoP = pontos.find((p) => p.tipo === 'gato');
    if (gatoP) {
      this.gato = this.add.sprite(gatoP.x, gatoP.y, 'ninja-Cat', 0).setOrigin(0.5, 1).play('gato-parado');
      this.alvos.push({ x: gatoP.x, y: gatoP.y - 4, fala: 'gato', gato: true });
    }
    this.saida = pontos.find((p) => p.tipo === 'saida');

    // itacoins (as que já foram pegas não voltam: estado.moedasPraca)
    estado.moedasPraca = estado.moedasPraca || [];
    this.moedas = this.physics.add.group();
    pontos
      .filter((p) => p.tipo === 'itacoin')
      .forEach((p, i) => {
        if (estado.moedasPraca.includes(i)) return;
        const m = this.moedas.create(p.x, p.y, 'itacoin', 0).setScale(0.5).play('itacoin-girar'); // folha 2x da plataforma
        m.indice = i;
        m.body.setSize(16, 16);
        this.tweens.add({ targets: m, y: p.y - 2, duration: 600, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
      });
    this.physics.add.overlap(this.heroi, this.moedas, (_h, m) => this.pegarMoeda(m));

    this.exclamacao = this.add.image(0, 0, 'ninja-exclamacao').setOrigin(0.5, 1).setDepth(6000).setVisible(false);

    const cam = this.cameras.main;
    cam.setZoom(PRACA.zoom).setBounds(0, 0, mapa.widthInPixels, mapa.heightInPixels).setRoundPixels(true);
    cam.startFollow(this.heroi, true, 0.15, 0.15);
    cam.fadeIn(400);

    this.dialogo = new Dialogo(this);
    this.registry.set({ fase: null, vida: 0, vidaMax: 0, itacoins: estado.itacoins, mostrarItacoins: true, paes: null, cenaJogo: 'Praca' });
    this.scene.launch('HUD');
    this.scene.launch('PracaUI');
    this.ui = this.scene.get('PracaUI');
    this.events.once('shutdown', () => {
      this.scene.stop('HUD');
      this.scene.stop('PracaUI');
    });
    tocarMusica('centro');
    this.input.keyboard?.on('keydown-ESC', () => abrirPausa(this));
    this.input.keyboard?.on('keydown-P', () => abrirPausa(this));

    if (!estado.viuPraca) {
      estado.viuPraca = true;
      salvar();
      this.time.delayedCall(500, () => this.falar(TEXTOS.praca.chegada));
    }
    if (import.meta.env.DEV) window.praca = this;
  }

  balao(s, chave) {
    return this.add.image(s.x, s.y - 18, `ninja-${chave}`).setOrigin(0.5, 1).setDepth(6000);
  }

  // morador que anda de um lado para o outro e para um pouco
  passear(s) {
    const x0 = s.x;
    const ir = (lado) => {
      if (!s.active) return;
      s.indo = lado;
      s.direcao = lado > 0 ? 'direita' : 'esquerda';
      this.tweens.add({
        targets: s,
        x: x0 + lado * 40,
        duration: (40 / PRACA.velocidadeNpc) * 1000,
        onUpdate: () => !this.falandoCom(s) || this.tweens.getTweensOf(s).forEach((t) => t.pause()),
        onComplete: () => {
          s.indo = 0;
          this.time.delayedCall(1200, () => ir(-lado));
        },
      });
    };
    this.time.delayedCall(800, () => ir(1));
  }

  falandoCom(s) {
    return this.ocupado && this.conversando === s;
  }

  pegarMoeda(m) {
    if (!m.active) return;
    estado.itacoins++;
    estado.moedasPraca.push(m.indice);
    salvar();
    this.registry.set('itacoins', estado.itacoins);
    tocarEfeito('moeda', { variar: 0.08 });
    this.tweens.killTweensOf(m);
    m.body.enable = false;
    this.tweens.add({ targets: m, y: m.y - 14, alpha: 0, duration: 260, onComplete: () => m.destroy() });
  }

  update(t, delta) {
    // personagens do pacote: animação de acordo com a direção e se está andando
    this.npcs.getChildren().forEach((s) => {
      s.setDepth(10 + s.y / 1000);
      const andando = !!s.indo && !this.falandoCom(s);
      this.animar(s, s.chave, s.direcao, andando);
    });
    this.alvos.forEach((a) => {
      if (a.npc) {
        a.x = a.npc.x;
        a.y = a.npc.y - 4;
        a.balao?.setPosition(a.npc.x, a.npc.y - 17);
      }
    });
    if (this.gato) this.gato.setDepth(10 + this.gato.y / 1000);
    this.heroi.setDepth(10 + this.heroi.y / 1000);

    if (this.ocupado || this.saindo) {
      this.heroi.body.setVelocity(0, 0);
      this.animar(this.heroi, this.chaveHeroi, this.direcao, false);
      this.exclamacao.setVisible(false);
      return;
    }
    const { dx, dy, falarApertou } = this.ui.estado || { dx: 0, dy: 0 };
    this.heroi.body.setVelocity(dx * PRACA.velocidade, dy * PRACA.velocidade);
    const andando = Math.hypot(dx, dy) > 0.15;
    if (andando) this.direcao = Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? 'direita' : 'esquerda') : dy > 0 ? 'baixo' : 'cima';
    this.animar(this.heroi, this.chaveHeroi, this.direcao, andando);

    // quem está na frente do herói
    const frente = { baixo: [0, 8], cima: [0, -14], esquerda: [-11, -4], direita: [11, -4] }[this.direcao];
    const fx = this.heroi.x + frente[0];
    const fy = this.heroi.y + frente[1];
    let alvo = null;
    let menor = PRACA.alcanceFala;
    for (const a of this.alvos) {
      const d = Phaser.Math.Distance.Between(fx, fy, a.x, a.y);
      if (d < menor) {
        menor = d;
        alvo = a;
      }
    }
    this.exclamacao.setVisible(!!alvo);
    if (alvo) this.exclamacao.setPosition(this.heroi.x, this.heroi.y - 17);
    if (alvo && falarApertou) this.conversar(alvo);

    if (this.saida && this.heroi.y > this.saida.y - 6 && Math.abs(this.heroi.x - this.saida.x) < 24) this.irParaMapa();
  }

  animar(s, chave, direcao, andando) {
    const anim = `${chave}-${andando ? 'andar' : 'parado'}-${direcao}`;
    if (s.anims.currentAnim?.key !== anim) s.play(anim, true);
  }

  async conversar(alvo) {
    if (alvo.npc) {
      const s = alvo.npc;
      this.conversando = s;
      // o morador vira para o herói
      const vx = this.heroi.x - s.x;
      const vy = this.heroi.y - s.y;
      s.direcao = Math.abs(vx) > Math.abs(vy) ? (vx > 0 ? 'direita' : 'esquerda') : vy > 0 ? 'baixo' : 'cima';
      alvo.balao?.destroy();
      alvo.balao = null;
    }
    if (alvo.gato) this.gato.play('gato-parado');
    await this.falar(TEXTOS.praca.falas[alvo.fala] || []);
    if (alvo.npc?.dados.anda) this.tweens.getTweensOf(alvo.npc).forEach((tw) => tw.resume());
    this.conversando = null;
  }

  async falar(caixas) {
    if (!caixas.length) return;
    this.ocupado = true;
    const lista = caixas.map((c) => ({
      nome: c.quem === 'heroi' ? nomeHeroi() : c.quem || '',
      cor: c.quem === 'heroi' ? CORES_CSS.azul : CORES_CSS.laranja,
      texto: texto(c.texto),
    }));
    await this.dialogo.mostrar(lista);
    this.ui.ignorarAteSoltar();
    this.ocupado = false;
  }

  irParaMapa() {
    if (this.saindo) return;
    this.saindo = true;
    tocarEfeito('botao');
    pararMusica(0.3);
    this.cameras.main.fadeOut(400);
    this.cameras.main.once('camerafadeoutcomplete', () => this.scene.start('Mapa'));
  }
}
