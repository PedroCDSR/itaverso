import * as Phaser from 'phaser';
import { LARGURA, ALTURA, TILE, CORES, CORES_CSS, FONTES, CAMERA, JOGADOR as J, MACA } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { Entrada } from '../ui/Entrada.js';
import { tentarTelaCheia } from '../ui/telaCheia.js';
import { bipe } from '../audio/som.js';
import { lerMapa, TIPO_TILE } from '../levels/leitor.js';
import { ITAJUBA } from '../levels/itajuba.js';
import { Jogador } from '../objects/Jogador.js';
import { Capivara } from '../objects/Capivara.js';

// Fase 1, Itajubá (CLAUDE.md, seção 11, cena 3).
// Rua, feira com toldos que quicam, praça com a fonte, capivaras, maçãs, sapatilhas, corações e 1 checkpoint.
// Termina na porta do Espaço Paula De Marco. O HUD é outra cena, por cima (scenes/HUD.js), e lê o "registry".
export class Itajuba extends Phaser.Scene {
  constructor() {
    super('Itajuba');
  }

  // dados.direto = true pula a tela "JOGAR" (ao jogar de novo)
  init(dados) {
    this.direto = !!dados?.direto;
  }

  create() {
    this.jogando = false;
    this.terminou = false;
    this.voltando = false; // no meio da volta ao checkpoint
    const mapa = lerMapa(ITAJUBA, 'ITAJUBA');
    this.mapa = mapa;

    // --- fundo em 3 camadas: céu parado, morros bem devagar, casario mais perto ---
    this.add.image(0, 0, 'ceu').setOrigin(0).setScrollFactor(0);
    this.morros = this.add.tileSprite(0, 0, LARGURA, ALTURA, 'morros').setOrigin(0).setScrollFactor(0);
    this.casas = this.add.tileSprite(0, 0, LARGURA, ALTURA, 'casas').setOrigin(0).setScrollFactor(0);

    // barracas embaixo dos toldos (desenhadas antes dos tiles, para ficarem atrás)
    this.desenharBarracas(mapa);

    // --- tiles ---
    const tm = this.make.tilemap({ data: mapa.tiles, tileWidth: TILE, tileHeight: TILE });
    const tileset = tm.addTilesetImage('tiles', 'tiles', TILE, TILE, 0, 0);
    this.camada = tm.createLayer(0, tileset, 0, 0);
    this.camada.setCollision([TIPO_TILE.chaoTopo, TIPO_TILE.chao]);
    // plataformas e toldos: só colidem por cima (dá para subir por baixo)
    this.camada.forEachTile((t) => {
      if (t.index === TIPO_TILE.plataforma || t.index === TIPO_TILE.toldo) t.setCollision(false, false, true, false);
    });

    // mundo: sem parede embaixo, para dar para cair nos buracos
    this.physics.world.setBounds(0, -ALTURA, mapa.larguraPx, mapa.alturaPx + ALTURA * 2);
    this.physics.world.setBoundsCollision(true, true, false, false);

    // --- objetos do mapa ---
    this.solidos = this.physics.add.staticGroup(); // fonte
    this.itens = this.physics.add.group({ allowGravity: false, immovable: true });
    this.capivaras = this.add.group({ runChildUpdate: false });
    this.bandeiras = [];
    this.totalSapatilhas = 0;
    for (const o of mapa.objetos) this.criarObjeto(o);

    // --- jogador ---
    this.jogador = new Jogador(this, mapa.inicio.x, mapa.inicio.y).setDepth(10);
    this.checkpoint = { x: mapa.inicio.x, y: mapa.inicio.y };
    this.physics.add.collider(this.jogador, this.camada, (j, tile) => this.tocouTile(tile));
    this.physics.add.collider(this.jogador, this.solidos);
    this.physics.add.overlap(this.jogador, this.itens, (j, item) => this.pegar(item));
    this.physics.add.overlap(this.jogador, this.capivaras, (j, c) => this.encostouCapivara(c));

    this.physics.add.collider(this.capivaras, this.camada);
    this.physics.add.collider(this.capivaras, this.solidos);

    // maçãs arremessadas
    this.macasVoando = this.physics.add.group();
    this.physics.add.collider(this.macasVoando, this.camada, (m) => this.macaQuicou(m));
    this.physics.add.collider(this.macasVoando, this.solidos, (m) => this.macaQuicou(m));

    // --- câmera ---
    const cam = this.cameras.main;
    cam.setBounds(0, 0, mapa.larguraPx, mapa.alturaPx);
    cam.startFollow(this.jogador, true, CAMERA.suavidade, CAMERA.suavidade);
    cam.setDeadzone(CAMERA.zonaMortaLargura, CAMERA.zonaMortaAltura);
    cam.fadeIn(300);

    this.entrada = new Entrada(this);

    // estado que o HUD mostra
    this.registry.set({ vida: J.coracoes, vidaMax: J.coracoes, macas: J.macasIniciais, sapatilhas: 0 });

    if (this.direto) this.comecar(null);
    else this.criarTelaJogar();
  }

  // ---------------------------------------------------------------- objetos

  criarObjeto(o) {
    const flutuar = (alvo) =>
      this.tweens.add({ targets: alvo, y: alvo.y - 3, duration: 700, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
    switch (o.tipo) {
      case 'capivara': {
        const c = new Capivara(this, o.x, o.y, this.camada).setDepth(6);
        this.capivaras.add(c);
        break;
      }
      case 'maca':
      case 'coracao':
      case 'sapatilha': {
        const chave = { maca: 'maca', coracao: 'coracao', sapatilha: 'sapatilha' }[o.tipo];
        const item = this.itens.create(o.x, o.y - TILE / 2, chave, 0).setDepth(5);
        item.tipo = o.tipo;
        if (o.tipo === 'sapatilha') {
          item.play('sapatilha-brilho');
          this.totalSapatilhas++;
        }
        flutuar(item);
        break;
      }
      case 'fonte': {
        // 'F' marca o canto inferior esquerdo; a fonte ocupa 3 tiles de largura
        const x0 = o.col * TILE;
        this.add.sprite(x0, o.y, 'fonte').setOrigin(0, 1).setDepth(4).play('fonte-agua');
        // duas partes sólidas: a bacia (baixa e larga) e a coluna com o prato (alta e estreita)
        const bacia = this.add.zone(x0 + 24, o.y - 6, 46, 12);
        const coluna = this.add.zone(x0 + 24, o.y - 15, 22, 30);
        this.solidos.add(bacia);
        this.solidos.add(coluna);
        break;
      }
      case 'checkpoint': {
        // a bandeira é só desenho; a passagem do jogador é checada no update()
        const b = this.add.sprite(o.x, o.y, 'bandeira', 0).setOrigin(0.5, 1).setDepth(4);
        b.ativa = false;
        this.bandeiras.push(b);
        break;
      }
      case 'saida':
        this.criarEspaco(o);
        break;
      default:
        break;
    }
  }

  // Fachada do Espaço Paula De Marco, com placa e porta (a saída da fase).
  criarEspaco(o) {
    const g = this.add.graphics().setDepth(3);
    const largura = 9 * TILE;
    const altura = 8 * TILE;
    const x0 = o.x - largura / 2;
    const base = o.y;
    const topo = base - altura;
    // parede lilás com faixa rosa e contorno
    g.fillStyle(0x2e1a33).fillRect(x0 - 2, topo - 2, largura + 4, altura + 2);
    g.fillStyle(CORES.lilas).fillRect(x0, topo, largura, altura);
    g.fillStyle(0x8c8ce6).fillRect(x0 + largura - 8, topo, 8, altura);
    g.fillStyle(CORES.rosa).fillRect(x0, topo + 34, largura, 6);
    // marquise
    g.fillStyle(0x2e1a33).fillRect(x0 - 8, topo - 8, largura + 16, 10);
    g.fillStyle(CORES.roxo).fillRect(x0 - 6, topo - 6, largura + 12, 6);
    // janelas com cortininha rosa
    for (const dx of [16, largura - 40]) {
      g.fillStyle(0x2e1a33).fillRect(x0 + dx - 1, topo + 50, 26, 30);
      g.fillStyle(0xcfe0e8).fillRect(x0 + dx, topo + 51, 24, 28);
      g.fillStyle(CORES.rosa).fillRect(x0 + dx, topo + 51, 24, 6);
    }
    // porta (onde o jogador entra)
    const px = o.x - 14;
    g.fillStyle(0x2e1a33).fillRect(px - 2, base - 50, 32, 50);
    g.fillStyle(CORES.rosa).fillRect(px, base - 48, 28, 48);
    g.fillStyle(0xd57fcf).fillRect(px + 13, base - 48, 2, 48);
    g.fillStyle(CORES.amarelo).fillRect(px + 9, base - 24, 3, 3).fillRect(px + 16, base - 24, 3, 3);
    // quadradinhos concêntricos do logo em cima da porta
    for (let i = 0; i < 3; i++) {
      const t = 12 - i * 4;
      g.lineStyle(1, i % 2 ? CORES.rosa : CORES.amarelo).strokeRect(o.x - t / 2, base - 62 - t / 2, t, t);
    }
    this.add
      .text(o.x, topo + 18, TEXTOS.itajuba.placaEspaco, {
        fontFamily: FONTES.titulo,
        fontSize: '8px',
        color: CORES_CSS.branco,
        align: 'center',
        wordWrap: { width: largura - 16 },
      })
      .setOrigin(0.5)
      .setDepth(3)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);

    this.saida = this.add.zone(o.x, base - 24, 20, 48);
    this.physics.add.existing(this.saida, true);
  }

  // Barracas da feira: postes e balcão com frutas embaixo de cada sequência de toldos.
  desenharBarracas(mapa) {
    const g = this.add.graphics();
    mapa.tiles.forEach((fila, lin) => {
      let inicio = -1;
      for (let col = 0; col <= fila.length; col++) {
        const eToldo = fila[col] === TIPO_TILE.toldo;
        if (eToldo && inicio < 0) inicio = col;
        if (!eToldo && inicio >= 0) {
          this.desenharBarraca(g, mapa, lin, inicio, col - 1);
          inicio = -1;
        }
      }
    });
  }

  desenharBarraca(g, mapa, lin, c0, c1) {
    // acha o chão embaixo do toldo
    let chao = lin + 1;
    while (chao < mapa.linhas && mapa.tiles[chao][c0] < 0) chao++;
    const yTopo = (lin + 1) * TILE - 4;
    const yChao = chao * TILE;
    const x0 = c0 * TILE + 3;
    const x1 = (c1 + 1) * TILE - 6;
    // postes
    g.fillStyle(0x2e1a33).fillRect(x0 - 1, yTopo, 5, yChao - yTopo).fillRect(x1 - 1, yTopo, 5, yChao - yTopo);
    g.fillStyle(0x9a5532).fillRect(x0, yTopo, 3, yChao - yTopo).fillRect(x1, yTopo, 3, yChao - yTopo);
    // balcão de madeira
    const yBalcao = yChao - 18;
    g.fillStyle(0x2e1a33).fillRect(x0 - 2, yBalcao - 1, x1 - x0 + 7, 19);
    g.fillStyle(0xb7793f).fillRect(x0 - 1, yBalcao, x1 - x0 + 5, 17);
    g.fillStyle(0x7e4d25).fillRect(x0 - 1, yBalcao + 4, x1 - x0 + 5, 2);
    // frutas e cestos (cores variando de barraca para barraca)
    const cores = [[0xe0453a, 0xf7a43a], [0x6cc24a, 0xf9fcbb], [0xffb0fa, 0xe0453a]][c0 % 3];
    for (let x = x0 + 4; x < x1 - 2; x += 6) {
      g.fillStyle(cores[(x / 6) % 2 | 0]).fillCircle(x, yBalcao - 3, 3);
    }
  }

  // ---------------------------------------------------------------- tela JOGAR (provisória até a Etapa 7)

  criarTelaJogar() {
    const t = TEXTOS.teste;
    const tela = this.add.container(0, 0).setDepth(2000).setScrollFactor(0);
    tela.add(this.add.rectangle(0, 0, LARGURA, ALTURA, CORES.lilas, 0.92).setOrigin(0));
    tela.add(
      this.add
        .text(LARGURA / 2, 64, t.titulo, { fontFamily: FONTES.titulo, fontSize: '24px', color: CORES_CSS.branco })
        .setOrigin(0.5)
        .setShadow(2, 2, CORES_CSS.roxo, 0, false, true),
    );
    tela.add(
      this.add
        .text(LARGURA / 2, 98, TEXTOS.itajuba.nomeFase, { fontFamily: FONTES.dialogo, fontSize: '18px', color: CORES_CSS.roxo })
        .setOrigin(0.5),
    );
    const botao = this.add.rectangle(LARGURA / 2, 150, 140, 40, CORES.rosa).setStrokeStyle(3, CORES.roxo);
    tela.add(botao);
    tela.add(
      this.add
        .text(LARGURA / 2, 151, TEXTOS.botoes.jogar, { fontFamily: FONTES.titulo, fontSize: '16px', color: CORES_CSS.roxo })
        .setOrigin(0.5),
    );
    const dica = this.sys.game.device.input.touch ? t.tocarJogar : t.dicaTeclado;
    tela.add(
      this.add
        .text(LARGURA / 2, 205, dica, {
          fontFamily: FONTES.dialogo,
          fontSize: '15px',
          color: CORES_CSS.roxo,
          align: 'center',
          wordWrap: { width: LARGURA - 40 },
        })
        .setOrigin(0.5),
    );
    botao.setInteractive({ useHandCursor: true });
    // pointerup: o navegador só aceita tela cheia quando o dedo sai da tela
    botao.on('pointerup', () => this.comecar(tela));
    this.input.keyboard?.once('keydown-ENTER', () => this.comecar(tela));
  }

  comecar(tela) {
    if (this.jogando) return;
    if (tela) {
      tentarTelaCheia(this);
      tela.destroy();
    }
    bipe(520, 0.12);
    this.jogando = true;
    this.scene.launch('HUD');
    this.faixa(TEXTOS.itajuba.objetivo);
  }

  // Faixa de texto que aparece no meio da tela e some.
  faixa(texto) {
    const t = this.add
      .text(LARGURA / 2, 78, texto, { fontFamily: FONTES.dialogo, fontSize: '18px', color: CORES_CSS.branco })
      .setOrigin(0.5)
      .setScrollFactor(0)
      .setDepth(1500)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true)
      .setAlpha(0);
    this.tweens.chain({
      targets: t,
      tweens: [
        { alpha: 1, duration: 250 },
        { alpha: 0, delay: 1800, duration: 400 },
      ],
      onComplete: () => t.destroy(),
    });
  }

  // Texto pequeno que sobe e some num ponto do mundo ("+1", "Ponto salvo!").
  aviso(x, y, texto, cor = CORES_CSS.branco) {
    const t = this.add
      .text(x, y, texto, { fontFamily: FONTES.dialogo, fontSize: '14px', color: cor })
      .setOrigin(0.5)
      .setDepth(20)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
    this.tweens.add({ targets: t, y: y - 18, alpha: 0, delay: 300, duration: 600, onComplete: () => t.destroy() });
  }

  // ---------------------------------------------------------------- regras

  tocouTile(tile) {
    // toldo: lança bem alto (mais alto segurando PULAR)
    if (tile.index !== TIPO_TILE.toldo || !this.jogador.body.blocked.down) return;
    this.jogador.quicar(this.entrada.pular ? J.quiqueToldo : J.quiqueToldoSemBotao);
    bipe(330, 0.12);
  }

  pegar(item) {
    if (!item.active) return;
    const reg = this.registry;
    if (item.tipo === 'maca') {
      if (reg.get('macas') >= J.macasMaximo) return; // bolsa cheia: deixa a maçã ali
      reg.inc('macas', 1);
      bipe(760, 0.06);
    } else if (item.tipo === 'coracao') {
      if (this.jogador.vida >= J.coracoes) return; // vida cheia: guarda o coração para depois
      this.jogador.vida++;
      reg.set('vida', this.jogador.vida);
      bipe(1040, 0.15);
    } else {
      reg.inc('sapatilhas', 1);
      bipe(1320, 0.07);
    }
    this.tweens.killTweensOf(item);
    item.disableBody(false, false);
    this.tweens.add({ targets: item, y: item.y - 14, alpha: 0, scale: 1.4, duration: 220, onComplete: () => item.destroy() });
  }

  encostouCapivara(c) {
    if (!c.perigosa || this.voltando) return;
    const j = this.jogador;
    // pisão: caindo e com o pé acima do meio da capivara
    if (j.body.velocity.y > 0 && j.body.bottom <= c.body.top + 8) {
      c.dormir();
      j.quicar(this.entrada.pular ? J.quiqueInimigo * 1.45 : J.quiqueInimigo);
      bipe(440, 0.1);
      return;
    }
    this.levarDano(c.x);
  }

  levarDano(deOndeX) {
    const agora = this.time.now;
    if (this.jogador.estaInvencivel(agora)) return;
    const vida = this.jogador.levarDano(deOndeX, agora);
    this.registry.set('vida', vida);
    this.cameras.main.shake(120, 0.006);
    bipe(180, 0.18);
    if (vida <= 0) this.voltarAoCheckpoint(true);
  }

  // Sem corações ou caiu no buraco: volta ao último checkpoint com vida cheia (sem game over).
  voltarAoCheckpoint(comPausa) {
    if (this.voltando) return;
    this.voltando = true;
    const cam = this.cameras.main;
    const voltar = () => {
      this.jogador.reposicionar(this.checkpoint.x, this.checkpoint.y, this.time.now);
      this.registry.set('vida', this.jogador.vida);
      // garante maçãs para a capivara do caminho
      if (this.registry.get('macas') < 3) this.registry.set('macas', 3);
      cam.flash(200, 255, 176, 250);
      this.voltando = false;
    };
    if (comPausa) this.time.delayedCall(450, voltar);
    else voltar();
  }

  arremessar() {
    const reg = this.registry;
    reg.inc('macas', -1);
    const j = this.jogador;
    const dir = j.olhandoDireita ? 1 : -1;
    const m = this.macasVoando.create(j.x + 12 * dir, j.y - MACA.alturaSaida, 'maca').setDepth(11);
    m.body.setSize(8, 8);
    m.setBounce(MACA.quique);
    m.quiques = 0;
    m.setVelocity(MACA.velocidadeX * dir + j.body.velocity.x * 0.3, MACA.velocidadeY);
    m.setAngularVelocity(720 * dir);
    this.time.delayedCall(MACA.duracaoMs, () => m.active && m.destroy());
    bipe(880, 0.05);
  }

  // Maçã x capivara: checado à mão a cada quadro (o overlap entre dois grupos não disparou no teste).
  macasAcertaram() {
    for (const m of this.macasVoando.getChildren()) {
      if (!m.active) continue;
      for (const c of this.capivaras.getChildren()) {
        if (c.perigosa && Phaser.Geom.Intersects.RectangleToRectangle(m.getBounds(), retanguloDoCorpo(c.body))) {
          c.comer(m.x);
          bipe(990, 0.1);
          m.destroy();
          break;
        }
      }
    }
  }

  // A maçã quica algumas vezes e some; bater de frente numa parede também faz sumir.
  macaQuicou(m) {
    if (!m.active) return;
    const b = m.body;
    if (b.blocked.left || b.blocked.right) {
      this.poeira(m.x, m.y);
      m.destroy();
      return;
    }
    if (!b.blocked.down) return;
    m.quiques++;
    if (m.quiques === 1) this.poeira(m.x, m.y + 4);
    if (m.quiques >= MACA.quiquesMaximo) m.destroy();
  }

  poeira(x, y) {
    for (let i = 0; i < 4; i++) {
      const p = this.add.circle(x, y, 2, 0xf4cf95).setDepth(12);
      this.tweens.add({
        targets: p,
        x: x + Phaser.Math.Between(-10, 10),
        y: y - Phaser.Math.Between(2, 10),
        alpha: 0,
        duration: 300,
        onComplete: () => p.destroy(),
      });
    }
  }

  ativarBandeira(b) {
    if (b.ativa) return;
    b.ativa = true;
    b.setFrame(1);
    this.tweens.add({ targets: b, scaleY: 1.12, duration: 100, yoyo: true });
    this.checkpoint = { x: b.x, y: b.y };
    this.aviso(b.x, b.y - 52, TEXTOS.itajuba.checkpoint, CORES_CSS.amarelo);
    bipe(660, 0.08);
    this.time.delayedCall(90, () => bipe(990, 0.12));
  }

  chegouNaPorta() {
    if (this.terminou) return;
    this.terminou = true;
    const j = this.jogador;
    j.body.setVelocity(0, 0);
    j.play('parado');
    bipe(784, 0.1);
    this.time.delayedCall(120, () => bipe(1046, 0.18));
    this.tweens.add({ targets: j, alpha: 0, duration: 400 });
    const cam = this.cameras.main;
    cam.fadeOut(700, 158, 158, 255);
    cam.once('camerafadeoutcomplete', () => {
      this.scene.stop('HUD');
      this.scene.start('EmBreve', { sapatilhas: this.registry.get('sapatilhas'), total: this.totalSapatilhas });
    });
  }

  // ---------------------------------------------------------------- quadro a quadro

  update(agora, delta) {
    const e = this.entrada;
    e.atualizar();
    const cam = this.cameras.main;
    cam.setFollowOffset(this.jogador.olhandoDireita ? -CAMERA.folgaFrente : CAMERA.folgaFrente, 0);
    this.morros.tilePositionX = cam.scrollX * 0.15;
    this.casas.tilePositionX = cam.scrollX * 0.4;

    this.capivaras.getChildren().forEach((c) => c.atualizar());

    if (!this.jogando || this.terminou) {
      this.jogador.body.setVelocityX(0);
      return;
    }

    const j = this.jogador;
    const temMaca = this.registry.get('macas') > 0;
    const pulouAntes = j.body.velocity.y < 0;
    const soltouMaca = j.atualizar(e, agora, delta, temMaca);
    if (!pulouAntes && j.body.velocity.y < -200 && e.pularApertou) bipe(660, 0.08);
    if (soltouMaca) this.arremessar();
    else if (e.macaApertou && !temMaca) this.aviso(j.x, j.y - 52, TEXTOS.itajuba.semMaca);
    this.macasAcertaram();

    // checkpoint e saída (checados aqui, sem física extra)
    for (const b of this.bandeiras) {
      if (!b.ativa && Math.abs(j.x - b.x) < 14 && Math.abs(j.y - b.y) < 48) this.ativarBandeira(b);
    }
    if (this.saida && this.physics.overlap(j, this.saida)) this.chegouNaPorta();

    // caiu no buraco: volta ao último checkpoint
    if (j.y > this.mapa.alturaPx + 48) {
      this.voltarAoCheckpoint(false);
    }
  }
}

// Caixa de colisão de um corpo Arcade como retângulo do Phaser.
function retanguloDoCorpo(b) {
  return new Phaser.Geom.Rectangle(b.x, b.y, b.width, b.height);
}
