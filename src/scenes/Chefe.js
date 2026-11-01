import * as Phaser from 'phaser';
import { LARGURA, ALTURA, TILE, CORES, CORES_CSS, FONTES, JOGADOR as J, MACA, CHEFE as C } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { Entrada } from '../ui/Entrada.js';
import { tocarEfeito } from '../audio/efeitos.js';
import { tocarMusica, tocarVinheta, pararMusica } from '../audio/musica.js';
import { Dialogo } from '../ui/Dialogo.js';
import { lerMapa, TIPO_TILE } from '../levels/leitor.js';
import { CHEFE as MAPA_CHEFE } from '../levels/chefe.js';
import { Jogador } from '../objects/Jogador.js';
import { Jafar } from '../objects/Jafar.js';

// cor do nome na caixa de diálogo
const COR_NOME = { jafar: CORES_CSS.roxo, paula: '#D57FCF' };

// Fase 3, Resgate (CLAUDE.md, seção 11, cena 5). Arena de uma tela, sem rolagem.
// A Tia Paula está presa numa gaiola no canto direito. O Jafar flutua, lança 3 projéteis em leque e depois desce
// cansado, piscando: é a hora de acertar maçãs. 5 acertos vencem. As maçãs reaparecem no chão.
// Sem game over: sem corações, o jogador volta ao começo da arena com vida cheia (a vida do Jafar continua igual).
export class Chefe extends Phaser.Scene {
  constructor() {
    super('Chefe');
  }

  // Vindo da Fase 2 o jogo já tem vida no registry: começa direto. No atalho ?fase=chefe (registry vazio) mostra a
  // tela JOGAR, porque o primeiro toque é que libera o som e a tela cheia.
  init(dados) {
    this.direto = !!dados?.direto || this.registry.has('vida');
  }

  create() {
    this.jogando = false;
    this.venceu = false;
    this.voltando = false;
    const mapa = lerMapa(MAPA_CHEFE, 'CHEFE');
    this.mapa = mapa;

    this.criarFundo();

    // --- tiles ---
    const tm = this.make.tilemap({ data: mapa.tiles, tileWidth: TILE, tileHeight: TILE });
    const tileset = tm.addTilesetImage('tiles', 'tiles', TILE, TILE, 0, 0);
    this.camada = tm.createLayer(0, tileset, 0, 0);
    this.camada.setCollision([TIPO_TILE.chaoTopo, TIPO_TILE.chao]);
    this.camada.forEachTile((t) => {
      if (t.index === TIPO_TILE.plataforma) t.setCollision(false, false, true, false);
    });
    this.physics.world.setBounds(0, -ALTURA, mapa.larguraPx, mapa.alturaPx + ALTURA);
    this.physics.world.setBoundsCollision(true, true, false, false);
    this.chaoY = (mapa.linhas - 2) * TILE; // topo do chão

    // --- Tia Paula na gaiola, pendurada no canto de cima à direita ---
    // (pendurada, e não no chão, para não ficar escondida atrás do botão PULAR no celular)
    const gx = LARGURA - 30;
    const gBase = 170; // pé da gaiola
    const corrente = this.add.graphics().setDepth(2);
    for (let y = 0; y < gBase - 56; y += 6) {
      corrente.fillStyle(0x2e1a33).fillRect(gx - 2, y, 4, 5);
      corrente.fillStyle(0xb98a2a).fillRect(gx - 1, y + 1, 2, 3);
    }
    this.paula = this.add.sprite(gx, gBase - 5, 'tiaPaula', 0).setOrigin(0.5, 1).setDepth(3).play('paula-presa');
    this.gaiola = this.add.sprite(gx, gBase, 'gaiola', 0).setOrigin(0.5, 1).setDepth(4);
    // balança de leve
    this.tweens.add({ targets: [this.gaiola, this.paula], angle: { from: -2, to: 2 }, duration: 1400, yoyo: true, repeat: -1, ease: 'Sine.inOut' });

    // --- estado do HUD (vem da fase anterior; no atalho ?fase=chefe começa do zero) ---
    const reg = this.registry;
    // ingressos e sapatilhas vêm das fases anteriores e passam adiante sem mudar
    reg.set({
      vida: J.coracoes,
      vidaMax: J.coracoes,
      macas: reg.has('macas') ? Math.max(reg.get('macas'), J.macasIniciais) : J.macasIniciais,
      sapatilhas: reg.get('sapatilhas') ?? 0,
    });

    // --- jogador ---
    this.inicio = { x: mapa.inicio.x, y: mapa.inicio.y };
    this.jogador = new Jogador(this, this.inicio.x, this.inicio.y).setDepth(10);
    this.physics.add.collider(this.jogador, this.camada);

    // --- Jafar ---
    this.jafar = new Jafar(this, LARGURA / 2 + 60).setDepth(8).setAlpha(0);
    this.jafar.on('lancar', (x, y) => this.lancarLeque(x, y));
    this.jafar.on('cansou', () => this.aviso(this.jafar.x, this.jafar.y - 40, TEXTOS.chefe.dicaCansado, CORES_CSS.amarelo));
    this.jafar.on('derrotado', () => this.vencer());

    // --- projéteis (sem gravidade) e maçãs ---
    this.projeteis = this.physics.add.group({ allowGravity: false });
    this.physics.add.overlap(this.jogador, this.projeteis, (j, p) => this.atingido(p));

    this.macasVoando = this.physics.add.group();
    this.physics.add.collider(this.macasVoando, this.camada, (m) => this.macaQuicou(m));

    this.macasChao = this.physics.add.group({ allowGravity: false, immovable: true });
    this.lugaresMaca = mapa.objetos.filter((o) => o.tipo === 'maca');
    this.lugaresMaca.forEach((o) => this.criarMacaChao(o));
    this.physics.add.overlap(this.jogador, this.macasChao, (j, m) => this.pegarMaca(m));

    this.criarBarraChefe();
    this.entrada = new Entrada(this);
    this.dialogo = new Dialogo(this);
    this.cameras.main.fadeIn(300);

    if (this.direto) this.comecar(null);
    else this.criarTelaJogar();
  }

  // ---------------------------------------------------------------- cenário

  // Céu de entardecer virando noite (o Jafar trouxe a magia escura), lua e morros.
  criarFundo() {
    this.add.image(0, 0, 'ceu').setOrigin(0).setScrollFactor(0);
    this.add.rectangle(0, 0, LARGURA, ALTURA, 0x3b2560, 0.35).setOrigin(0);
    const g = this.add.graphics();
    // estrelinhas e lua crescente
    const estrelas = [[40, 30], [96, 52], [150, 22], [222, 44], [300, 26], [352, 58], [404, 36], [460, 64], [260, 70]];
    g.fillStyle(CORES.amarelo, 0.9);
    estrelas.forEach(([x, y]) => g.fillRect(x, y, 2, 2));
    g.fillStyle(CORES.amarelo).fillCircle(420, 92, 14);
    g.fillStyle(0x6b5590).fillCircle(427, 87, 12);
    this.add.tileSprite(0, 0, LARGURA, ALTURA, 'morros').setOrigin(0).setTint(0x9a86c8);
    // colunas do terraço onde acontece a luta
    const colunas = [40, 200, 280, 440];
    for (const x of colunas) {
      g.fillStyle(0x2e1a33).fillRect(x - 9, 120, 18, 120);
      g.fillStyle(0xe8b48a).fillRect(x - 7, 124, 14, 116);
      g.fillStyle(0xc98f6a).fillRect(x + 3, 124, 4, 116);
      g.fillStyle(0x2e1a33).fillRect(x - 12, 114, 24, 8);
      g.fillStyle(0xb5583a).fillRect(x - 11, 115, 22, 6);
    }
    // arcos entre as colunas
    g.lineStyle(6, 0x2e1a33).beginPath().arc(120, 122, 80, Math.PI, 0).strokePath();
    g.lineStyle(4, 0xe8b48a).beginPath().arc(120, 122, 80, Math.PI, 0).strokePath();
    g.lineStyle(6, 0x2e1a33).beginPath().arc(360, 122, 80, Math.PI, 0).strokePath();
    g.lineStyle(4, 0xe8b48a).beginPath().arc(360, 122, 80, Math.PI, 0).strokePath();
  }

  // Barra de vida do chefe no topo, entre os contadores do HUD e os botões de pausa e som.
  criarBarraChefe() {
    // começa depois dos contadores do HUD (que vão até x≈196 quando há ingressos) e termina antes da pausa (x≈410)
    const x = 212;
    const y = 12;
    const largura = 186;
    this.barra = { x: x + 50, y, largura: largura - 50, altura: 8 };
    this.add
      .text(x, y + 4, TEXTOS.chefe.nomeChefe, { fontFamily: FONTES.titulo, fontSize: '8px', color: CORES_CSS.branco })
      .setOrigin(0, 0.5)
      .setDepth(900)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
    const b = this.barra;
    this.add.rectangle(b.x - 2, b.y - 2, b.largura + 4, b.altura + 4, 0x2e1a33).setOrigin(0).setDepth(900);
    this.add.rectangle(b.x, b.y, b.largura, b.altura, CORES.lilas, 0.5).setOrigin(0).setDepth(900);
    this.barraVida = this.add.rectangle(b.x, b.y, b.largura, b.altura, CORES.rosa).setOrigin(0).setDepth(901);
    // marquinhas de cada acerto
    const g = this.add.graphics().setDepth(902);
    g.fillStyle(0x2e1a33);
    for (let i = 1; i < C.vida; i++) g.fillRect(b.x + Math.round((b.largura * i) / C.vida), b.y, 1, b.altura);
    this.atualizarBarra();
  }

  atualizarBarra() {
    this.barraVida.width = (this.barra.largura * this.jafar.vida) / C.vida;
  }

  // ---------------------------------------------------------------- começo

  // Tela "JOGAR" só no atalho ?fase=chefe: o primeiro toque libera o som e a tela cheia.
  criarTelaJogar() {
    const tela = this.add.container(0, 0).setDepth(2000);
    tela.add(this.add.rectangle(0, 0, LARGURA, ALTURA, CORES.lilas, 0.92).setOrigin(0));
    tela.add(
      this.add
        .text(LARGURA / 2, 70, TEXTOS.chefe.nomeFase, { fontFamily: FONTES.titulo, fontSize: '16px', color: CORES_CSS.branco })
        .setOrigin(0.5)
        .setShadow(2, 2, CORES_CSS.roxo, 0, false, true),
    );
    const botao = this.add.rectangle(LARGURA / 2, 140, 140, 40, CORES.rosa).setStrokeStyle(3, CORES.roxo);
    tela.add(botao);
    tela.add(
      this.add
        .text(LARGURA / 2, 141, TEXTOS.botoes.jogar, { fontFamily: FONTES.titulo, fontSize: '16px', color: CORES_CSS.roxo })
        .setOrigin(0.5),
    );
    const dica = this.sys.game.device.input.touch ? TEXTOS.teste.tocarJogar : TEXTOS.teste.dicaTeclado;
    tela.add(
      this.add
        .text(LARGURA / 2, 200, dica, {
          fontFamily: FONTES.dialogo,
          fontSize: '15px',
          color: CORES_CSS.roxo,
          align: 'center',
          wordWrap: { width: LARGURA - 40 },
        })
        .setOrigin(0.5),
    );
    botao.setInteractive({ useHandCursor: true }).on('pointerup', () => this.comecar(tela));
    this.input.keyboard?.once('keydown-ENTER', () => this.comecar(tela));
  }

  // Entrada do Jafar (fala), pedido de socorro e, depois, a luta.
  comecar(tela) {
    if (this.jogando) return;
    if (tela) tela.destroy();
    this.jogando = true;
    this.scene.launch('HUD');
    this.scene.bringToTop('HUD');
    if (tela) tocarEfeito('botao');
    tocarMusica('chefe');

    const jf = this.jafar;
    const t = TEXTOS.chefe;
    // aparece mais baixo, para não ficar escondido atrás da caixa de diálogo, e sobe quando a luta começa
    jf.y = 150;
    this.tweens.add({ targets: jf, alpha: 1, duration: 500 });
    this.fumaca(jf.x, jf.y, 8);
    this.time.delayedCall(1100, () => this.balao(this.paula.x - 20, this.paula.y - 62, t.paulaSocorro, 1300));
    // a fala espera o toque; a luta só começa depois dela
    this.time.delayedCall(600, async () => {
      await this.dialogo.mostrar([
        { nome: t.nomeJafar, texto: t.jafarEntrada, cor: COR_NOME.jafar },
        ...t.paulaAntes.map((texto) => ({ nome: t.nomePaula, texto, cor: COR_NOME.paula })),
      ]);
      this.faixa(t.objetivo);
      this.tweens.add({
        targets: jf,
        y: C.alturaVoo,
        duration: 500,
        ease: 'Sine.inOut',
        onComplete: () => {
          jf.comecar(this.time.now);
          this.inicioLuta = this.time.now;
        },
      });
    });
  }

  // ---------------------------------------------------------------- regras

  lancarLeque(x, y) {
    const j = this.jogador;
    // mira no peito do jogador
    const mira = Phaser.Math.Angle.Between(x, y, j.x, j.y - 20);
    const passo = Phaser.Math.DegToRad(C.aberturaLequeGraus);
    const meio = (C.projeteis - 1) / 2;
    for (let i = 0; i < C.projeteis; i++) {
      const ang = mira + (i - meio) * passo;
      // um pouco maior que o desenho, para ver bem na tela do celular
      const p = this.projeteis.create(x, y, 'projetil', 0).setDepth(9).setScale(1.5);
      p.play('projetil-girar');
      p.body.setCircle(4, 2, 2);
      this.physics.velocityFromRotation(ang, C.velocidadeProjetil, p.body.velocity);
    }
    this.cameras.main.shake(80, 0.003);
    tocarEfeito('projetil');
  }

  atingido(p) {
    if (this.voltando || this.venceu) return;
    const agora = this.time.now;
    if (this.jogador.estaInvencivel(agora)) return;
    this.estouro(p.x, p.y, CORES.rosa);
    p.destroy();
    const vida = this.jogador.levarDano(p.x, agora);
    this.registry.set('vida', vida);
    this.cameras.main.shake(120, 0.006);
    tocarEfeito('dano');
    if (vida <= 0) this.voltarAoInicio();
  }

  // Sem corações: volta ao começo da arena com vida cheia. A vida do Jafar continua (config: manterVidaAoReiniciar).
  voltarAoInicio() {
    if (this.voltando) return;
    this.voltando = true;
    this.time.delayedCall(450, () => {
      this.jogador.reposicionar(this.inicio.x, this.inicio.y, this.time.now);
      this.registry.set('vida', this.jogador.vida);
      if (this.registry.get('macas') < C.macasMinimasAoReiniciar) this.registry.set('macas', C.macasMinimasAoReiniciar);
      this.projeteis.clear(true, true);
      if (!C.manterVidaAoReiniciar) {
        this.jafar.vida = C.vida;
        this.atualizarBarra();
      }
      this.cameras.main.flash(200, 255, 176, 250);
      this.voltando = false;
    });
  }

  criarMacaChao(o) {
    const m = this.macasChao.create(o.x, o.y - 6, 'maca').setDepth(5);
    m.lugar = o;
    m.setAlpha(0);
    this.tweens.add({ targets: m, alpha: 1, duration: 250 });
    this.tweens.add({ targets: m, y: m.y - 3, duration: 600, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
  }

  pegarMaca(m) {
    if (!m.active || this.registry.get('macas') >= J.macasMaximo) return;
    this.registry.inc('macas', 1);
    tocarEfeito('pegarMaca');
    this.tweens.killTweensOf(m);
    m.disableBody(false, false);
    this.tweens.add({ targets: m, y: m.y - 14, alpha: 0, scale: 1.4, duration: 220, onComplete: () => m.destroy() });
    // outra maçã aparece no mesmo lugar depois de um tempo
    this.time.delayedCall(C.macaReaparecerMs, () => !this.venceu && this.criarMacaChao(m.lugar));
  }

  arremessar() {
    this.registry.inc('macas', -1);
    const j = this.jogador;
    const dir = j.olhandoDireita ? 1 : -1;
    const m = this.macasVoando.create(j.x + 12 * dir, j.y - MACA.alturaSaida, 'maca').setDepth(11);
    m.body.setSize(8, 8);
    m.setBounce(MACA.quique);
    m.quiques = 0;
    m.setVelocity(MACA.velocidadeX * dir + j.body.velocity.x * 0.3, MACA.velocidadeY);
    m.setAngularVelocity(720 * dir);
    this.time.delayedCall(MACA.duracaoMs, () => m.active && m.destroy());
    tocarEfeito('maca');
  }

  macaQuicou(m) {
    if (!m.active) return;
    const b = m.body;
    if (b.blocked.left || b.blocked.right) return m.destroy();
    if (!b.blocked.down) return;
    m.quiques++;
    if (m.quiques >= MACA.quiquesMaximo) m.destroy();
  }

  // Maçã x Jafar, checado à mão a cada quadro (como na Fase 1).
  macasAcertaram() {
    const jf = this.jafar;
    if (!jf.active || this.venceu) return;
    const caixa = new Phaser.Geom.Rectangle(jf.body.x, jf.body.y, jf.body.width, jf.body.height);
    for (const m of this.macasVoando.getChildren()) {
      if (!m.active || !Phaser.Geom.Intersects.RectangleToRectangle(m.getBounds(), caixa)) continue;
      const r = jf.levarMaca(this.time.now);
      if (r === 'ignorou') continue;
      if (r === 'bateu') {
        // não estava cansado: a maçã só bate e cai
        this.estouro(m.x, m.y, CORES.amarelo);
        tocarEfeito('pisao', { volume: 0.5 });
      } else {
        this.atualizarBarra();
        this.estouro(m.x, m.y, 0xe0453a);
        this.aviso(jf.x, jf.y - 36, TEXTOS.chefe.ai);
        this.cameras.main.shake(90, 0.004);
        tocarEfeito('acertoChefe');
      }
      m.destroy();
    }
  }

  // ---------------------------------------------------------------- vitória

  vencer() {
    if (this.venceu) return;
    this.venceu = true;
    this.tempoLuta = Math.round((this.time.now - (this.inicioLuta ?? this.time.now)) / 100) / 10;
    this.registry.set('tempoChefe', this.tempoLuta);
    this.projeteis.clear(true, true);
    this.macasVoando.clear(true, true);
    const jf = this.jafar;
    const j = this.jogador;
    j.body.setVelocityX(0);

    const t = TEXTOS.chefe;
    pararMusica(0.4);
    this.balao(jf.x, jf.y - 44, t.jafarDerrotado, 900);
    tocarEfeito('acertoChefe');
    // nuvem de fumaça e o Jafar some
    this.time.delayedCall(700, () => {
      this.fumaca(jf.x, jf.y, 18);
      this.cameras.main.shake(200, 0.006);
      this.tweens.add({ targets: jf, alpha: 0, scale: 0.3, angle: 200, duration: 500, onComplete: () => jf.destroy() });
    });
    // a gaiola se abre e a Tia Paula sai feliz
    this.time.delayedCall(1500, () => {
      this.gaiola.setFrame(1);
      this.estouro(this.gaiola.x, this.gaiola.y - 30, CORES.amarelo);
      tocarVinheta('vitoria');
      this.paula.play('paula-feliz');
      this.paula.setDepth(6);
      // pula da gaiola para o chão, num arco
      this.tweens.killTweensOf(this.paula);
      this.paula.setAngle(0);
      this.tweens.add({ targets: this.paula, x: LARGURA - 150, duration: 750, ease: 'Linear' });
      this.tweens.chain({
        targets: this.paula,
        tweens: [
          { y: this.paula.y - 30, duration: 300, ease: 'Sine.out' },
          { y: this.chaoY, duration: 450, ease: 'Sine.in' },
        ],
      });
    });
    // a Tia Paula agradece (caixa de diálogo, toque para avançar) e os dois vão para o tapete
    this.time.delayedCall(2500, async () => {
      j.setFlipX(this.paula.x < j.x);
      await this.dialogo.mostrar(t.paulaObrigada.map((texto) => ({ nome: t.nomePaula, texto, cor: COR_NOME.paula })));
      const cam = this.cameras.main;
      cam.fadeOut(700, 158, 158, 255);
      cam.once('camerafadeoutcomplete', () => {
        this.scene.stop('HUD');
        this.scene.start('Tapete');
      });
    });
  }

  // ---------------------------------------------------------------- efeitos

  fumaca(x, y, n) {
    for (let i = 0; i < n; i++) {
      const cor = [0xd8c8f0, 0x9e9eff, 0xb7a6d6][i % 3];
      const p = this.add.circle(x + Phaser.Math.Between(-10, 10), y + Phaser.Math.Between(-14, 14), Phaser.Math.Between(5, 9), cor).setDepth(12);
      this.tweens.add({
        targets: p,
        x: p.x + Phaser.Math.Between(-30, 30),
        y: p.y + Phaser.Math.Between(-30, 10),
        scale: 2.2,
        alpha: 0,
        duration: Phaser.Math.Between(500, 900),
        onComplete: () => p.destroy(),
      });
    }
  }

  estouro(x, y, cor) {
    for (let i = 0; i < 5; i++) {
      const p = this.add.rectangle(x, y, 3, 3, cor).setDepth(12);
      const ang = (i / 5) * Math.PI * 2;
      this.tweens.add({
        targets: p,
        x: x + Math.cos(ang) * 12,
        y: y + Math.sin(ang) * 12,
        alpha: 0,
        duration: 280,
        onComplete: () => p.destroy(),
      });
    }
  }

  // Balão de fala (Patrick Hand, no máximo 2 linhas) que some sozinho.
  balao(x, y, texto, duracaoMs) {
    const t = this.add
      .text(0, 0, texto, {
        fontFamily: FONTES.dialogo,
        fontSize: '15px',
        color: CORES_CSS.roxo,
        align: 'center',
        wordWrap: { width: 170 },
      })
      .setOrigin(0.5);
    const w = t.width + 14;
    const h = t.height + 6;
    // não deixa o balão sair da tela
    const cx = Phaser.Math.Clamp(x, w / 2 + 4, LARGURA - w / 2 - 4);
    const cy = Math.max(y, h / 2 + 34);
    const fundo = this.add.graphics();
    fundo.fillStyle(0xffffff, 0.95).fillRoundedRect(-w / 2, -h / 2, w, h, 6);
    fundo.lineStyle(2, CORES.roxo).strokeRoundedRect(-w / 2, -h / 2, w, h, 6);
    const c = this.add.container(cx, cy, [fundo, t]).setDepth(1500).setScale(0.6).setAlpha(0);
    this.tweens.add({ targets: c, scale: 1, alpha: 1, duration: 150, ease: 'Back.out' });
    this.time.delayedCall(duracaoMs, () =>
      this.tweens.add({ targets: c, alpha: 0, duration: 200, onComplete: () => c.destroy() }),
    );
  }

  faixa(texto) {
    const t = this.add
      .text(LARGURA / 2, 140, texto, { fontFamily: FONTES.dialogo, fontSize: '18px', color: CORES_CSS.branco })
      .setOrigin(0.5)
      .setDepth(1500)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true)
      .setAlpha(0);
    this.tweens.chain({
      targets: t,
      tweens: [
        { alpha: 1, duration: 250 },
        { alpha: 0, delay: 2200, duration: 400 },
      ],
      onComplete: () => t.destroy(),
    });
  }

  aviso(x, y, texto, cor = CORES_CSS.branco) {
    const t = this.add
      .text(x, y, texto, { fontFamily: FONTES.dialogo, fontSize: '15px', color: cor })
      .setOrigin(0.5)
      .setDepth(20)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
    this.tweens.add({ targets: t, y: y - 18, alpha: 0, delay: 500, duration: 600, onComplete: () => t.destroy() });
  }

  // ---------------------------------------------------------------- quadro a quadro

  update(agora, delta) {
    this.entrada.atualizar();
    const j = this.jogador;
    if (this.jafar.active) this.jafar.atualizar(agora, delta, j.x);

    // projéteis que saíram da tela ou bateram no chão somem
    for (const p of this.projeteis.getChildren()) {
      if (p.y > this.chaoY - 2 || p.x < -16 || p.x > LARGURA + 16 || p.y < -16) {
        if (p.y > this.chaoY - 2) this.estouro(p.x, this.chaoY - 2, CORES.rosa);
        p.destroy();
      }
    }

    if (!this.jogando || this.venceu || !this.inicioLuta) {
      j.body.setVelocityX(0);
      j.atualizar({ esquerda: false, direita: false, pular: false, pularApertou: false, macaApertou: false }, agora, delta, false);
      return;
    }

    const temMaca = this.registry.get('macas') > 0;
    const pulouAntes = j.body.velocity.y < 0;
    const soltouMaca = j.atualizar(this.entrada, agora, delta, temMaca);
    if (!pulouAntes && j.body.velocity.y < -200 && this.entrada.pularApertou) tocarEfeito('pulo');
    if (soltouMaca) this.arremessar();
    else if (this.entrada.macaApertou && !temMaca) this.aviso(j.x, j.y - 52, TEXTOS.chefe.semMaca);
    this.macasAcertaram();
  }
}
