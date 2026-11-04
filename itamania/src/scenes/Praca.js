import * as Phaser from 'phaser';
import { CORES_CSS, PRACA } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { nomeVaga } from '../data/vagas.js';
import { estado, salvar } from '../estado.js';
import { g } from '../genero.js';
import { Dialogo } from '../ui/Dialogo.js';
import { tocarEfeito } from '../audio/efeitos.js';
import { tocarMusica, pararMusica } from '../audio/musica.js';
import { abrirPausa } from '../fluxo.js';

// Praça Theodomiro Santiago andável, vista de cima (o começo do Centro explorável).
// Mapa no formato do Tiled (public/assets/mapas/praca.tmj, gerado por ferramentas/mapas/gerar_praca.py e editável no
// Tiled). Arte: Modern Exteriors (LimeZu). Chão em camadas de tiles; prédios, árvores e móveis são imagens da camada
// "objetos", ordenadas pela base (quem está mais embaixo aparece na frente).
// Personagens do pacote: quadros de 16x32; linha 0 parado, linha 1 andando; 6 quadros por direção.

// Texto com as marcações de gênero e os nomes das vagas (lugares reais autorizados ou genéricos).
function texto(t) {
  return g(t.replace('{cafe}', nomeVaga('cafe')).replace('{lanchonete}', nomeVaga('lanchonete')));
}

const props = (o) => Object.fromEntries((o.properties || []).map((p) => [p.name, p.value]));

export class Praca extends Phaser.Scene {
  constructor() {
    super({ key: 'Praca', physics: { arcade: { gravity: { x: 0, y: 0 } } } });
  }

  create() {
    this.ocupado = false;
    this.saindo = false;
    const mapa = this.make.tilemap({ key: 'praca' });
    const chao = mapa.addTilesetImage('chao', 'limezu-chao');
    for (const nome of ['asfalto', 'calcada', 'grama_cheia', 'grama', 'agua', 'faixas']) mapa.createLayer(nome, chao, 0, 0).setDepth(0);
    this.colisao = mapa.createLayer('colisao', chao, 0, 0).setVisible(false);
    this.colisao.setCollisionByExclusion([-1]);
    this.physics.world.setBounds(0, 0, mapa.widthInPixels, mapa.heightInPixels);

    // objetos: o gid aponta para uma imagem do tileset "objetos" (o tipo de cada imagem é a chave da textura)
    // (o Phaser guarda tilesets de imagens soltas em imageCollections; a chave sai do nome do arquivo)
    const tipoPorGid = {};
    for (const col of mapa.imageCollections) {
      for (const im of col.images) tipoPorGid[im.gid] = im.image.split('/').pop().replace('.png', '');
    }
    this.alvos = [];
    this.copas = []; // árvores e palmeiras: ficam transparentes quando o herói passa atrás
    for (const o of mapa.getObjectLayer('objetos').objects) {
      const chave = tipoPorGid[o.gid] || o.type;
      const img = this.add.image(o.x, o.y, `limezu-${chave}`).setOrigin(0, 1).setDepth(10 + o.y / 1000);
      const p = props(o);
      if (p.fala) this.alvos.push({ x: o.x + img.width / 2, y: o.y + 2, fala: p.fala });
      if (/^(arvore|palmeira)/.test(chave)) this.copas.push(img);
      if (chave === 'jatos') this.tweens.add({ targets: img, alpha: 0.7, duration: 420, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
    }

    // pontos do mapa (início, moradores, itacoins, saída)
    const pontos = mapa.getObjectLayer('pontos').objects.map((o) => ({ tipo: o.type, x: o.x, y: o.y, ...props(o) }));
    const inicio = pontos.find((p) => p.tipo === 'inicio');

    // Capivara exploradora: a colisão fica nas patas para caminhar atrás dos objetos.
    this.chaveHeroi = 'exploradora';
    this.heroi = this.physics.add.sprite(inicio.x, inicio.y, 'capivara-exploradora', 12);
    this.heroi.setOrigin(0.5, 1).setDisplaySize(32, 32).setCollideWorldBounds(true);
    const lado = this.heroi.frame.width;
    this.heroi.body.setSize(lado * 0.5, lado * 0.2).setOffset(lado * 0.25, lado * 0.73);
    this.direcao = 'cima';
    this.physics.add.collider(this.heroi, this.colisao);

    // moradores
    this.npcs = this.physics.add.group({ immovable: true });
    for (const p of pontos.filter((q) => q.tipo === 'npc')) {
      const s = this.npcs.create(p.x, p.y, `limezu-${p.sprite}`, 18).setOrigin(0.5, 1);
      s.body.setSize(10, 6).setOffset(3, 26);
      s.dados = p;
      s.chave = p.sprite;
      s.direcao = 'baixo';
      if (p.anda) this.passear(s);
      this.alvos.push({ x: p.x, y: p.y - 4, fala: p.fala, npc: s, balao: this.balao(s, 'reticencias') });
    }
    this.physics.add.collider(this.heroi, this.npcs);
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
    return this.add.image(s.x, s.y - 33, `ninja-${chave}`).setOrigin(0.5, 1).setDepth(6000);
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
        a.balao?.setPosition(a.npc.x, a.npc.y - 33);
      }
    });
    this.heroi.setDepth(10 + this.heroi.y / 1000);
    // copa transparente: o herói está atrás da árvore (mais ao norte que a base) e dentro do desenho dela
    for (const c of this.copas) {
      const atras = this.heroi.y < c.y - 4 && this.heroi.y > c.y - c.height && Math.abs(this.heroi.x - (c.x + c.width / 2)) < c.width / 2;
      const alvo = atras ? PRACA.copaTransparente : 1;
      if (c.alpha !== alvo) c.setAlpha(Math.abs(c.alpha - alvo) < 0.03 ? alvo : Phaser.Math.Linear(c.alpha, alvo, 0.25));
    }

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
    const frente = { baixo: [0, 8], cima: [0, -10], esquerda: [-11, -3], direita: [11, -3] }[this.direcao];
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
    if (alvo) this.exclamacao.setPosition(this.heroi.x, this.heroi.y - 33);
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
    await this.falar(TEXTOS.praca.falas[alvo.fala] || []);
    if (alvo.npc?.dados.anda) this.tweens.getTweensOf(alvo.npc).forEach((tw) => tw.resume());
    this.conversando = null;
  }

  async falar(caixas) {
    if (!caixas.length) return;
    this.ocupado = true;
    const lista = caixas.map((c) => ({
      nome: c.quem === 'heroi' ? TEXTOS.praca.nomeHeroi : c.quem || '',
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
