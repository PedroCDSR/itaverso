import * as Phaser from 'phaser';
import { LARGURA, ALTURA, TILE, CORES_CSS, FONTES, CAMERA, JOGADOR as J, PAO, CONVERSA, ITENS } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { FASES } from '../levels/index.js';
import { lerMapa, TIPO_TILE } from '../levels/leitor.js';
import { Entrada } from '../ui/Entrada.js';
import { Dialogo } from '../ui/Dialogo.js';
import { Jogador } from '../objects/Jogador.js';
import { Inimigo } from '../objects/Inimigo.js';
import { tocarEfeito } from '../audio/efeitos.js';
import { tocarMusica, tocarVinheta, pararMusica } from '../audio/musica.js';
import { estado, salvar, terminarFase } from '../estado.js';
import { g, nomeHeroi } from '../genero.js';
import { abrirPausa } from '../fluxo.js';
import { esperar } from '../util.js';

// Cena genérica de fase. Cada fase é um conjunto de dados em src/levels/faseN.js (mapa, cenário, NPCs, missão,
// curiosidade). Estrutura (DESIGN.md): chegada → missão curta do lugar → plataforma até o fim → cartão de curiosidade.
export class Fase extends Phaser.Scene {
  constructor() {
    super('Fase');
  }

  init(dados) {
    this.numero = dados?.fase || 1;
    this.def = FASES[this.numero];
  }

  create() {
    const d = this.def;
    this.jogando = false;
    this.terminou = false;
    this.voltando = false;
    this.ocupado = false; // em conversa ou cena: o herói não anda
    const mapa = lerMapa(d.mapa, `FASE${this.numero}`);
    this.mapa = mapa;
    this.chaoY = (mapa.linhas - 2) * TILE; // topo da rua

    this.criarFundo();
    for (const l of d.lugares || []) this.criarLugar(l);

    // tiles
    const tm = this.make.tilemap({ data: mapa.tiles, tileWidth: TILE, tileHeight: TILE });
    const tileset = tm.addTilesetImage('tiles', d.tiles || 'tiles', TILE, TILE, 0, 0);
    this.camada = tm.createLayer(0, tileset, 0, 0).setDepth(1.5);
    this.camada.setCollision([TIPO_TILE.chaoTopo, TIPO_TILE.chao, TIPO_TILE.invisivel]);
    this.camada.forEachTile((t) => {
      if ([TIPO_TILE.plataforma, TIPO_TILE.toldo, TIPO_TILE.plataformaInvisivel].includes(t.index)) {
        t.setCollision(false, false, true, false);
      }
    });
    this.physics.world.setBounds(0, -ALTURA, mapa.larguraPx, mapa.alturaPx + ALTURA * 2);
    this.physics.world.setBoundsCollision(true, true, false, false);

    // objetos
    this.itens = this.physics.add.group({ allowGravity: false, immovable: true });
    this.inimigos = this.add.group();
    this.npcs = [];
    this.gatilhos = [];
    this.retornos = [];
    let iNpc = 0;
    let iGat = 0;
    for (const o of mapa.objetos) {
      if (o.tipo === 'npc') this.criarNpc(o, d.npcs[iNpc++]);
      else if (o.tipo === 'gatilho') this.gatilhos.push({ ...o, ...d.gatilhos[iGat++], feito: false });
      else this.criarObjeto(o);
    }

    // herói
    this.jogador = new Jogador(this, mapa.inicio.x, mapa.inicio.y, { bone: estado.bone }).setDepth(10);
    this.retorno = { x: mapa.inicio.x, y: mapa.inicio.y };
    this.physics.add.collider(this.jogador, this.camada, (j, tile) => this.tocouTile(tile));
    this.physics.add.overlap(this.jogador, this.itens, (j, item) => this.pegar(item));
    this.physics.add.overlap(this.jogador, this.inimigos, (j, i) => this.encostouInimigo(i));
    this.physics.add.collider(this.inimigos, this.camada);

    this.paesVoando = this.physics.add.group();
    this.physics.add.collider(this.paesVoando, this.camada, (p) => this.paoQuicou(p));

    const cam = this.cameras.main;
    cam.setBounds(0, 0, mapa.larguraPx, mapa.alturaPx);
    cam.startFollow(this.jogador, true, CAMERA.suavidade, CAMERA.suavidade);
    cam.setDeadzone(CAMERA.zonaMortaLargura, CAMERA.zonaMortaAltura);
    cam.fadeIn(350);

    this.entrada = new Entrada(this);
    if (!estado.temPao) this.entrada.toque.esconderBotao('maca');
    this.dialogo = new Dialogo(this);
    this.input.keyboard?.on('keydown-ESC', () => this.pausar());
    this.input.keyboard?.on('keydown-P', () => this.pausar());

    this.registry.set({
      vida: J.coracoes,
      vidaMax: J.coracoes,
      itacoins: estado.itacoins,
      mostrarItacoins: this.numero >= 2,
      paes: estado.temPao ? estado.paes : null,
      missao: g(d.missao),
      fase: this.numero,
    });
    this.scene.launch('HUD');
    this.scene.bringToTop('HUD');
    tocarMusica(d.musica);
    this.comecar();
  }

  pausar() {
    if (this.terminou) return;
    abrirPausa(this);
  }

  // ---------------------------------------------------------------- cenário

  criarFundo() {
    const d = this.def;
    // céu em faixas chapadas (sem degradê), do alto para o horizonte
    const ceu = this.add.graphics().setScrollFactor(0).setDepth(-10);
    const faixas = d.ceu;
    const h = Math.ceil(ALTURA / faixas.length);
    faixas.forEach((cor, i) => ceu.fillStyle(Phaser.Display.Color.HexStringToColor(cor).color).fillRect(0, i * h, LARGURA, h + 1));
    // nuvens simples (formas próprias, sem olhos)
    this.nuvens = [];
    for (let i = 0; i < 5; i++) {
      const n = this.add.graphics().setScrollFactor(0).setDepth(-9);
      const w = Phaser.Math.Between(40, 80);
      n.fillStyle(0xffffff, 0.85).fillRect(0, 0, w, 6).fillRect(8, -4, w - 22, 5).fillRect(w * 0.4, -7, w * 0.3, 4);
      n.fillStyle(0xdde6ff, 0.85).fillRect(4, 6, w - 8, 2);
      n.x = Phaser.Math.Between(0, LARGURA);
      n.y = Phaser.Math.Between(18, 90);
      n.vel = Phaser.Math.FloatBetween(0.04, 0.12);
      this.nuvens.push(n);
    }
    this.camadasFundo = (d.fundos || []).map((f) => {
      const t = this.add.tileSprite(0, f.y || 0, LARGURA, ALTURA, f.chave).setOrigin(0).setScrollFactor(0).setDepth(-8 + (f.fator || 0));
      if (f.tom) t.setTint(Phaser.Display.Color.HexStringToColor(f.tom).color);
      t.fator = f.fator;
      return t;
    });
  }

  // Lugar (prédio, monumento): imagem com a base no chão da coluna indicada. `fator` < 1 = mais longe (parallax).
  criarLugar(l) {
    const y = (l.lin != null ? l.lin * TILE : this.chaoY) + (l.dy || 0);
    const img = this.add.image(l.col * TILE + (l.dx || 0), y, l.img).setOrigin(0, 1).setDepth(l.frente ? 12 : (l.prof ?? 1));
    if (l.flip) img.setFlipX(true);
    if (l.fator && l.fator !== 1) {
      img.setScrollFactor(l.fator, 1);
      img.x = l.col * TILE * l.fator + (l.dx || 0);
    }
    if (l.tom) img.setTint(Phaser.Display.Color.HexStringToColor(l.tom).color);
    if (l.anima) l.anima(this, img);
    return img;
  }

  // ---------------------------------------------------------------- objetos

  criarObjeto(o) {
    const flutuar = (alvo) =>
      this.tweens.add({ targets: alvo, y: alvo.y - 3, duration: 700, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
    switch (o.tipo) {
      case 'itacoin': {
        const it = this.itens.create(o.x, o.y - TILE / 2, 'itacoin', 0).setDepth(5);
        it.tipo = 'itacoin';
        it.play('itacoin-girar');
        break;
      }
      case 'coracao': {
        const it = this.itens.create(o.x, o.y - TILE / 2, 'coracao', 0).setDepth(5);
        it.tipo = 'coracao';
        flutuar(it);
        break;
      }
      case 'pao': {
        const it = this.itens.create(o.x, o.y - TILE / 2, 'paodequeijo', 0).setDepth(5);
        it.tipo = 'pao';
        flutuar(it);
        break;
      }
      case 'cafe': {
        const it = this.itens.create(o.x, o.y - 9, 'cafecomleite', 0).setDepth(5);
        it.tipo = 'cafe';
        it.play('cafe-vapor');
        break;
      }
      case 'capivara':
      case 'pombo': {
        const i = new Inimigo(this, o.x, o.y, o.tipo, this.camada).setDepth(6);
        this.inimigos.add(i);
        break;
      }
      case 'retorno': {
        const p = this.add.sprite(o.x, o.y, 'placaretorno', 0).setOrigin(0.5, 1).setDepth(4);
        p.ativa = false;
        this.retornos.push(p);
        break;
      }
      case 'saida': {
        this.saida = this.add.sprite(o.x, o.y, 'placasaida', 0).setOrigin(0.5, 1).setDepth(4);
        this.saidaZona = new Phaser.Geom.Rectangle(o.x - 10, o.y - 60, 20, 60);
        break;
      }
      default:
        break;
    }
  }

  criarNpc(o, def) {
    if (!def) throw new Error(`Fase ${this.numero}: falta a definição do NPC da coluna ${o.col}`);
    const s = this.add.sprite(o.x, o.y + (def.dy || 0), def.sprite, 0).setOrigin(0.5, 1).setDepth(def.prof ?? 8);
    s.def = def;
    s.falou = false;
    s.longe = true;
    if (def.anim !== false) {
      this.tweens.add({ targets: s, scaleY: 1.02, duration: 900, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
    }
    // balãozinho "..." de quem ainda não falou
    s.balao = this.add
      .text(o.x, o.y - 66 + (def.dy || 0), '...', { fontFamily: FONTES.titulo, fontSize: '8px', color: CORES_CSS.roxo, backgroundColor: '#FFFFFF', padding: { x: 3, y: 2 } })
      .setOrigin(0.5)
      .setDepth(9);
    this.tweens.add({ targets: s.balao, y: s.balao.y - 3, duration: 600, yoyo: true, repeat: -1 });
    this.npcs.push(s);
  }

  // ---------------------------------------------------------------- começo

  async comecar() {
    const d = this.def;
    if (d.chegada) await d.chegada(this);
    if (d.inicio?.length) await this.falar(d.inicio);
    this.jogando = true;
    this.faixa(g(d.missao));
  }

  // Mostra caixas de diálogo. `quem`: 'heroi' (nome do herói) ou um nome qualquer.
  async falar(caixas) {
    this.ocupado = true;
    this.jogador.body.setVelocityX(0);
    this.jogador.tocar('parado');
    const lista = caixas.map((c) => ({
      nome: c.quem === 'heroi' ? nomeHeroi() : c.quem || '',
      cor: c.quem === 'heroi' ? CORES_CSS.azul : c.cor || CORES_CSS.laranja,
      texto: g(c.texto),
    }));
    await this.dialogo.mostrar(lista);
    this.entrada.ignorarAteSoltar();
    this.ocupado = false;
  }

  faixa(texto) {
    const t = this.add
      .text(LARGURA / 2, 78, texto, { fontFamily: FONTES.dialogo, fontSize: '18px', color: CORES_CSS.branco, align: 'center', wordWrap: { width: 360 } })
      .setOrigin(0.5)
      .setScrollFactor(0)
      .setDepth(1500)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true)
      .setAlpha(0);
    this.tweens.chain({ targets: t, tweens: [{ alpha: 1, duration: 250 }, { alpha: 0, delay: 2200, duration: 400 }], onComplete: () => t.destroy() });
  }

  aviso(x, y, texto, cor = CORES_CSS.branco) {
    const t = this.add
      .text(x, y, texto, { fontFamily: FONTES.dialogo, fontSize: '14px', color: cor })
      .setOrigin(0.5)
      .setDepth(20)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
    this.tweens.add({ targets: t, y: y - 18, alpha: 0, delay: 500, duration: 700, onComplete: () => t.destroy() });
  }

  // Dica presa ao mundo (tutorial): aparece quando o herói chega perto e some depois.
  dica(texto, x, y) {
    const t = this.add
      .text(x, y, texto, { fontFamily: FONTES.dialogo, fontSize: '15px', color: CORES_CSS.roxo, backgroundColor: '#FFF6A8', padding: { x: 5, y: 2 }, align: 'center', wordWrap: { width: 190 } })
      .setOrigin(0.5)
      .setDepth(30)
      .setAlpha(0);
    this.tweens.chain({ targets: t, tweens: [{ alpha: 1, y: y - 4, duration: 250 }, { alpha: 0, delay: 3800, duration: 400 }], onComplete: () => t.destroy() });
  }

  // ---------------------------------------------------------------- regras

  tocouTile(tile) {
    if (tile.index !== TIPO_TILE.toldo || !this.jogador.body.blocked.down) return;
    this.jogador.quicar(this.entrada.pular ? J.quiqueToldo : J.quiqueToldoSemBotao);
    tocarEfeito('toldo');
  }

  pegar(item) {
    if (!item.active) return;
    const reg = this.registry;
    if (item.tipo === 'itacoin') {
      estado.itacoins++;
      reg.set('itacoins', estado.itacoins);
      tocarEfeito('moeda', { variar: 0.06 });
    } else if (item.tipo === 'coracao') {
      if (this.jogador.vida >= J.coracoes) return;
      this.jogador.vida++;
      reg.set('vida', this.jogador.vida);
      tocarEfeito('coracao');
    } else if (item.tipo === 'pao') {
      if (!estado.temPao) return;
      estado.paes++;
      reg.set('paes', estado.paes);
      tocarEfeito('pegarItem');
    } else if (item.tipo === 'cafe') {
      if (this.jogador.turbinado) return; // já está turbinado: deixa o copo para depois
      this.crescer();
    }
    this.tweens.killTweensOf(item);
    item.disableBody(false, false);
    this.tweens.add({ targets: item, y: item.y - 14, alpha: 0, scale: 1.4, duration: 220, onComplete: () => item.destroy() });
  }

  crescer() {
    const j = this.jogador;
    tocarEfeito('crescer');
    // pisca entre as duas formas, como nos jogos do gênero, e fica grande
    let n = 0;
    this.time.addEvent({
      delay: 70,
      repeat: 7,
      callback: () => j.setForma(n++ % 2 === 0 ? 'turbinado' : 'normal'),
    });
    this.time.delayedCall(70 * 8 + 10, () => j.setForma('turbinado'));
  }

  encostouInimigo(i) {
    if (!i.perigoso || this.voltando || this.ocupado) return;
    const j = this.jogador;
    if (j.body.velocity.y > 0 && j.body.bottom <= i.body.top + 8) {
      i.pisado();
      j.quicar(this.entrada.pular ? J.quiqueInimigo * 1.45 : J.quiqueInimigo);
      tocarEfeito('pisao');
      return;
    }
    this.levarDano(i.x);
  }

  levarDano(deOndeX) {
    const agora = this.time.now;
    const j = this.jogador;
    if (j.estaInvencivel(agora)) return;
    const eraTurbinado = j.turbinado;
    const vida = j.levarDano(deOndeX, agora);
    this.registry.set('vida', vida);
    this.cameras.main.shake(120, 0.006);
    tocarEfeito(eraTurbinado ? 'encolher' : 'dano');
    if (eraTurbinado) this.aviso(j.x, j.y - 60, g(TEXTOS.avisos.encolheu));
    if (vida <= 0) this.voltarAoRetorno(true);
  }

  // Sem corações ou caiu num buraco: volta ao último ponto de retorno com vida cheia (sem game over).
  voltarAoRetorno(comPausa) {
    if (this.voltando) return;
    this.voltando = true;
    const voltar = () => {
      this.jogador.reposicionar(this.retorno.x, this.retorno.y, this.time.now);
      this.registry.set('vida', this.jogador.vida);
      if (estado.temPao && estado.paes < 3) {
        estado.paes = 3;
        this.registry.set('paes', 3);
      }
      this.cameras.main.flash(200, 255, 230, 140);
      this.voltando = false;
    };
    if (comPausa) this.time.delayedCall(450, voltar);
    else voltar();
  }

  arremessar() {
    estado.paes--;
    this.registry.set('paes', estado.paes);
    const j = this.jogador;
    const dir = j.olhandoDireita ? 1 : -1;
    const alt = j.turbinado ? 34 : 28;
    const p = this.paesVoando.create(j.x + 12 * dir, j.y - alt, 'paodequeijo', 0).setDepth(11);
    p.body.setSize(9, 8);
    p.body.setGravityY(PAO.gravidade - J.gravidade);
    p.setBounce(0.45);
    p.quiques = 0;
    p.setVelocity(PAO.velocidadeX * dir + j.body.velocity.x * 0.3, PAO.velocidadeY);
    p.setAngularVelocity(600 * dir);
    this.time.delayedCall(PAO.vidaMs, () => p.active && p.destroy());
    tocarEfeito('arremesso');
  }

  paesAcertaram() {
    for (const p of this.paesVoando.getChildren()) {
      if (!p.active) continue;
      for (const i of this.inimigos.getChildren()) {
        if (!i.perigoso) continue;
        const b = i.body;
        if (Phaser.Geom.Intersects.RectangleToRectangle(p.getBounds(), new Phaser.Geom.Rectangle(b.x, b.y, b.width, b.height))) {
          i.comer(p.x);
          tocarEfeito('nham');
          p.destroy();
          break;
        }
      }
    }
  }

  paoQuicou(p) {
    if (!p.active) return;
    const b = p.body;
    if (b.blocked.left || b.blocked.right) {
      p.destroy();
      return;
    }
    if (b.blocked.down && ++p.quiques > PAO.quiques) p.destroy();
  }

  ativarRetorno(p) {
    if (p.ativa) return;
    p.ativa = true;
    p.setFrame(1);
    this.tweens.add({ targets: p, scaleY: 1.12, duration: 100, yoyo: true });
    this.retorno = { x: p.x, y: p.y };
    this.aviso(p.x, p.y - 54, TEXTOS.avisos.retorno, CORES_CSS.amarelo);
    tocarVinheta('checkpoint');
  }

  // ---------------------------------------------------------------- NPCs, loja e eventos

  async conversar(npc) {
    const def = npc.def;
    npc.falou = true;
    npc.longe = false;
    npc.balao.setVisible(false);
    npc.setFlipX(this.jogador.x < npc.x); // os desenhos olham para a direita
    npc.setFrame(1);
    const falas = typeof def.falas === 'function' ? def.falas(this) : def.falas;
    this.jogador.olhandoDireita = npc.x > this.jogador.x;
    this.jogador.setFlipX(!this.jogador.olhandoDireita);
    await this.falar(falas.map((f) => ({ quem: def.nome, ...f })));
    npc.setFrame(0);
    if (def.acao) await this.acao(def.acao, npc);
  }

  async acao(nome, npc) {
    if (nome === 'loja') {
      if (estado.bone) return;
      if (estado.itacoins >= ITENS.precoBone) {
        await this.comprarBone(npc);
      } else {
        npc.falou = false; // dá para voltar depois com mais itacoins
        npc.balao.setVisible(true);
        await this.falar([{ quem: npc.def.nome, texto: `Faltam ${ITENS.precoBone - estado.itacoins} itacoins. Procure mais pela rua e volte aqui!` }]);
      }
    } else if (nome === 'pao') {
      estado.temPao = true;
      estado.paes = Math.max(estado.paes, PAO.iniciais);
      this.registry.set('paes', estado.paes);
      this.entrada.toque.botoes.maca?.setVisible(true);
      if (this.entrada.toque.escondidos) this.entrada.toque.escondidos.maca = false;
      tocarVinheta('poder');
      this.ganhouItem('paodequeijo', npc);
      salvar();
      this.dica(this.sys.game.device.input.touch ? TEXTOS.tutorial.paoToque : TEXTOS.tutorial.paoTeclado, this.jogador.x, this.jogador.y - 80);
    } else if (nome === 'cafe') {
      estado.temCafe = true;
      this.ganhouItem('cafecomleite', npc);
      this.crescer();
      salvar();
    } else if (typeof nome === 'function') {
      await nome(this, npc);
    }
  }

  // Item sobe do NPC até o herói (pão de queijo, café com leite).
  ganhouItem(textura, npc) {
    const s = this.add.sprite(npc.x, npc.y - 40, textura, 0).setDepth(20).setScale(1.5);
    this.tweens.add({ targets: s, x: this.jogador.x, y: this.jogador.y - 40, duration: 450, ease: 'Sine.inOut', onComplete: () => this.tweens.add({ targets: s, alpha: 0, scale: 2.2, duration: 250, onComplete: () => s.destroy() }) });
  }

  async comprarBone(npc) {
    this.ocupado = true;
    // as itacoins voam do herói até a vendedora
    for (let i = 0; i < ITENS.precoBone; i++) {
      this.time.delayedCall(i * 70, () => {
        estado.itacoins--;
        this.registry.set('itacoins', estado.itacoins);
        const m = this.add.sprite(this.jogador.x, this.jogador.y - 40, 'itacoin', 0).setDepth(20);
        tocarEfeito('moeda', { variar: 0.1, volume: 0.6 });
        this.tweens.add({ targets: m, x: npc.x, y: npc.y - 44, duration: 350, onComplete: () => m.destroy() });
      });
    }
    await esperar(this, ITENS.precoBone * 70 + 400);
    const b = this.add.sprite(npc.x, npc.y - 46, 'boneitem', 0).setDepth(20);
    await new Promise((ok) => this.tweens.add({ targets: b, x: this.jogador.x, y: this.jogador.y - (this.jogador.turbinado ? 58 : 48), duration: 500, ease: 'Sine.inOut', onComplete: ok }));
    b.destroy();
    estado.bone = true;
    salvar();
    this.jogador.setBone(true);
    this.jogador.tocar('vitoria');
    tocarVinheta('poder');
    await esperar(this, 900);
    await this.falar([{ quem: npc.def.nome, texto: 'Prontinho! Ficou ótimo em você!' }, { quem: 'heroi', texto: 'Meu boné amarelo! Agora sim, {pronto|pronta} para a aventura!' }]);
  }

  async rodarGatilho(gt) {
    gt.feito = true;
    if (gt.evento) await gt.evento(this);
    else if (gt.falas) await this.falar(gt.falas);
    else if (gt.dica) this.dica(this.sys.game.device.input.touch ? gt.dica.toque : gt.dica.teclado, gt.x, gt.y - 70);
  }

  // ---------------------------------------------------------------- fim da fase

  async chegouNaSaida() {
    const d = this.def;
    const falta = d.exigir?.(this);
    if (falta) {
      if (this.avisandoSaida) return;
      this.avisandoSaida = true;
      this.jogador.body.setVelocityX(-120);
      await this.falar([{ quem: 'heroi', texto: falta }]);
      this.time.delayedCall(600, () => (this.avisandoSaida = false));
      return;
    }
    this.terminou = true;
    const j = this.jogador;
    j.body.setVelocity(0, 0);
    j.tocar('vitoria');
    pararMusica(0.2);
    tocarVinheta('vitoria');
    terminarFase(this.numero);
    await esperar(this, 1400);
    const cam = this.cameras.main;
    cam.fadeOut(500, 43, 45, 92);
    cam.once('camerafadeoutcomplete', () => {
      this.scene.stop('HUD');
      this.scene.start('Cartao', { fase: this.numero });
    });
  }

  // ---------------------------------------------------------------- quadro a quadro

  update(agora, delta) {
    const e = this.entrada;
    e.atualizar();
    const cam = this.cameras.main;
    cam.setFollowOffset(this.jogador.olhandoDireita ? -CAMERA.folgaFrente : CAMERA.folgaFrente, 0);
    for (const c of this.camadasFundo) c.tilePositionX = cam.scrollX * c.fator;
    for (const n of this.nuvens) {
      n.x -= n.vel * (delta / 16) + 0;
      const px = n.x - cam.scrollX * 0.05;
      if (px < -100) n.x += LARGURA + 200;
    }
    this.inimigos.getChildren().forEach((i) => i.atualizar(agora));

    const j = this.jogador;
    if (!this.jogando || this.terminou || this.ocupado) {
      j.body.setVelocityX(0);
      if (!this.ocupado && !this.terminou) j.escolherAnimacao(j.body.blocked.down, agora);
      return;
    }

    const pode = estado.temPao && estado.paes > 0;
    j.pulouAgora = false;
    const soltou = j.atualizar(e, agora, delta, pode);
    if (j.pulouAgora) tocarEfeito('pulo');
    if (soltou) this.arremessar();
    else if (e.macaApertou && estado.temPao && estado.paes <= 0) this.aviso(j.x, j.y - 60, 'Acabou o pão de queijo!');
    this.paesAcertaram();

    for (const p of this.retornos) {
      if (!p.ativa && Math.abs(j.x - p.x) < 14 && Math.abs(j.y - p.y) < 48) this.ativarRetorno(p);
    }
    // NPCs: conversa ao chegar perto (só em x, para ninguém passar pulando por cima sem querer)
    for (const n of this.npcs) {
      const perto = Math.abs(j.x - n.x) < CONVERSA.distancia && Math.abs(j.y - n.y) < 60;
      if (!perto) n.longe = true;
      if (perto && n.longe && !n.falou && j.body.blocked.down) {
        this.conversar(n);
        return;
      }
      // quem já falou olha para o herói
      if (n.falou) n.setFlipX(j.x < n.x);
    }
    for (const gt of this.gatilhos) {
      if (!gt.feito && Math.abs(j.x - gt.x) < 12 && j.y <= gt.y + 2 && j.y > gt.y - 80) {
        this.rodarGatilho(gt);
        return;
      }
    }
    if (this.saidaZona && this.saidaZona.contains(j.x, j.y - 10)) this.chegouNaSaida();
    if (j.y > this.mapa.alturaPx + 48) this.voltarAoRetorno(false);
  }
}
