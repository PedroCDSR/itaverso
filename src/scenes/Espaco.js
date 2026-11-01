import * as Phaser from 'phaser';
import { LARGURA, ALTURA, TILE, CORES, CORES_CSS, FONTES, CAMERA, JOGADOR as J, ESPACO } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { Entrada } from '../ui/Entrada.js';
import { Dialogo } from '../ui/Dialogo.js';
import { tocarEfeito } from '../audio/efeitos.js';
import { tocarMusica, tocarVinheta, pararMusica } from '../audio/musica.js';
import { lerMapa, TIPO_TILE } from '../levels/leitor.js';
import { ESPACO as MAPA, NPCS_ESPACO } from '../levels/espaco.js';
import { Jogador } from '../objects/Jogador.js';
import { Npc } from '../objects/Npc.js';

// Cor da etiqueta com o nome de quem fala, na caixa de diálogo.
const COR_NOME = {
  jasmine: '#6D6BD9',
  genio: '#8C7CDB',
  sultao: '#47913A',
  claudia: '#D57FCF',
  abu: '#8A5A3A',
};

// Fase 2, Espaço Paula De Marco (CLAUDE.md, seção 11, cena 4). Sem inimigos.
// Estúdio com espelhos, barras e piso de madeira. Os personagens do espetáculo ensaiam e cada um fala quando o
// jogador chega perto. A Tia Claudia entrega os ingressos (contador no HUD). Depois o Abu chega correndo:
// o Jafar levou a Tia Paula! Transição para o chefe.
export class Espaco extends Phaser.Scene {
  constructor() {
    super('Espaco');
  }

  create() {
    this.conversando = false;
    this.terminou = false;
    const mapa = lerMapa(MAPA, 'ESPACO');
    this.mapa = mapa;

    // parede com espelhos e barras (acompanha o mundo, é a parede do fundo da sala)
    this.add.tileSprite(0, 0, mapa.larguraPx, ALTURA, 'estudio').setOrigin(0).setScrollFactor(1);
    this.desenharCartazes();

    const tm = this.make.tilemap({ data: mapa.tiles, tileWidth: TILE, tileHeight: TILE });
    const tileset = tm.addTilesetImage('tiles-espaco', 'tiles-espaco', TILE, TILE, 0, 0);
    this.camada = tm.createLayer(0, tileset, 0, 0);
    this.camada.setCollision([TIPO_TILE.chaoTopo, TIPO_TILE.chao]);
    this.camada.forEachTile((t) => {
      if (t.index === TIPO_TILE.plataforma) t.setCollision(false, false, true, false);
    });
    this.physics.world.setBounds(0, -ALTURA, mapa.larguraPx, mapa.alturaPx + ALTURA * 2);
    this.physics.world.setBoundsCollision(true, true, false, false);

    // objetos: sapatilhas e personagens
    this.itens = this.physics.add.group({ allowGravity: false, immovable: true });
    this.npcs = [];
    let iNpc = 0;
    for (const o of mapa.objetos) {
      if (o.tipo === 'sapatilha') {
        const s = this.itens.create(o.x, o.y - TILE / 2, 'sapatilha', 0).setDepth(5).play('sapatilha-brilho');
        this.tweens.add({ targets: s, y: s.y - 3, duration: 700, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
      } else if (o.tipo === 'npc') {
        const id = NPCS_ESPACO[iNpc++];
        if (!id) throw new Error(`ESPACO: há mais 'N' no mapa do que nomes em NPCS_ESPACO`);
        this.npcs.push(new Npc(this, o.x, o.y, id).setDepth(6));
      }
    }
    this.claudia = this.npcs.find((n) => n.id === 'claudia');
    if (this.claudia) this.desenharBalcao(this.claudia);

    // jogador
    this.jogador = new Jogador(this, mapa.inicio.x, mapa.inicio.y).setDepth(10);
    this.physics.add.collider(this.jogador, this.camada);
    this.physics.add.overlap(this.jogador, this.itens, (j, item) => this.pegar(item));

    const cam = this.cameras.main;
    cam.setBounds(0, 0, mapa.larguraPx, mapa.alturaPx);
    cam.startFollow(this.jogador, true, CAMERA.suavidade, CAMERA.suavidade);
    cam.setDeadzone(CAMERA.zonaMortaLargura, CAMERA.zonaMortaAltura);
    cam.fadeIn(400, 158, 158, 255);

    this.entrada = new Entrada(this);
    this.entrada.toque.esconderBotao('maca'); // sem inimigos: nada de maçã aqui
    this.dialogo = new Dialogo(this);

    // HUD: vida cheia, mantém maçãs e sapatilhas da Fase 1, e o contador de ingressos aparece (começa em 0)
    const reg = this.registry;
    this.totalSapatilhas = this.itens.getLength();
    reg.set({
      vida: J.coracoes,
      vidaMax: J.coracoes,
      macas: reg.get('macas') ?? J.macasIniciais,
      sapatilhas: reg.get('sapatilhas') ?? 0,
      sapatilhasTotal: (reg.get('sapatilhasTotalFase1') ?? 0) + this.totalSapatilhas,
      ingressos: 0,
    });
    this.scene.launch('HUD');
    tocarMusica('espaco');
    this.faixa(TEXTOS.espaco.nomeFase, 100, () => this.faixa(TEXTOS.espaco.objetivo, 0));
  }

  // ---------------------------------------------------------------- cenário

  // Cartazes do espetáculo na parede, entre os espelhos.
  desenharCartazes() {
    const g = this.add.graphics();
    for (let x = 8 + 240 * 2; x < this.mapa.larguraPx - 240; x += 240 * 3) {
      g.fillStyle(0x2e1a33).fillRect(x - 2, 34, 50, 32);
      g.fillStyle(CORES.roxo).fillRect(x - 1, 35, 48, 30);
      g.fillStyle(CORES.amarelo).fillRect(x + 3, 39, 40, 22);
      this.add
        .text(x + 23, 50, TEXTOS.espaco.cartaz.replace(' · ', '\n'), {
          fontFamily: FONTES.titulo,
          fontSize: '6px',
          color: CORES_CSS.roxo,
          align: 'center',
          lineSpacing: 3,
        })
        .setOrigin(0.5);
    }
  }

  // Balcão da recepção na frente da Tia Claudia (as pernas dela ficam escondidas atrás), com placa.
  desenharBalcao(npc) {
    const g = this.add.graphics().setDepth(7);
    const x0 = npc.x - 26;
    const larg = 44;
    const topo = npc.y - 16; // baixo o bastante para a camiseta dela aparecer
    g.fillStyle(0x2e1a33).fillRect(x0 - 2, topo - 2, larg + 4, 18);
    g.fillStyle(CORES.lilas).fillRect(x0, topo, larg, 16);
    g.fillStyle(CORES.roxo).fillRect(x0, topo + 12, larg, 4);
    g.fillStyle(CORES.rosa).fillRect(x0 - 2, topo - 4, larg + 4, 4);
    // quadradinhos do logo
    for (let i = 0; i < 3; i++) {
      const t = 10 - i * 3;
      g.lineStyle(1, i % 2 ? CORES.rosa : CORES.amarelo).strokeRect(npc.x - 4 - t / 2, topo + 6 - t / 2, t, t);
    }
    // placa "INGRESSOS" pendurada
    const placa = this.add
      .text(npc.x, npc.y - 74, TEXTOS.espaco.balcao, {
        fontFamily: FONTES.titulo,
        fontSize: '7px',
        color: CORES_CSS.roxo,
        backgroundColor: CORES_CSS.amarelo,
        padding: { x: 4, y: 3 },
      })
      .setOrigin(0.5)
      .setDepth(5);
    const gp = this.add.graphics().setDepth(4);
    gp.lineStyle(1, 0x2e1a33).lineBetween(placa.x - 18, 25, placa.x - 18, placa.y).lineBetween(placa.x + 18, 25, placa.x + 18, placa.y);
    // porta da sala do outro lado (por onde o Abu chega)
    const px = this.mapa.larguraPx - 34;
    const base = 15 * TILE;
    g.fillStyle(0x2e1a33).fillRect(px - 2, base - 52, 32, 52);
    g.fillStyle(0xb7793f).fillRect(px, base - 50, 28, 50);
    g.fillStyle(0x7e4d25).fillRect(px + 4, base - 46, 20, 18).fillRect(px + 4, base - 24, 20, 20);
    g.fillStyle(CORES.amarelo).fillRect(px + 4, base - 28, 3, 3);
    this.porta = { x: px + 14, y: base };
  }

  // Faixa de texto no meio da tela que aparece e some (mesma ideia da Fase 1).
  faixa(texto, atraso = 0, depois) {
    const t = this.add
      // roxo com sombra branca: a parede do estúdio é clara
      .text(LARGURA / 2, 78, texto, { fontFamily: FONTES.dialogo, fontSize: '18px', color: CORES_CSS.roxo })
      .setOrigin(0.5)
      .setScrollFactor(0)
      .setDepth(1500)
      .setShadow(1, 1, CORES_CSS.branco, 0, false, true)
      .setAlpha(0);
    this.tweens.chain({
      targets: t,
      tweens: [
        { alpha: 1, duration: 250, delay: atraso },
        { alpha: 0, delay: 1500, duration: 350 },
      ],
      onComplete: () => {
        t.destroy();
        depois?.();
      },
    });
  }

  pegar(item) {
    if (!item.active) return;
    this.registry.inc('sapatilhas', 1);
    tocarEfeito('sapatilha', { variar: 0.08 });
    this.tweens.killTweensOf(item);
    item.disableBody(false, false);
    this.tweens.add({ targets: item, y: item.y - 14, alpha: 0, scale: 1.4, duration: 220, onComplete: () => item.destroy() });
  }

  // ---------------------------------------------------------------- conversas

  caixas(id, falas, nome) {
    return falas.map((texto) => ({ nome, texto, cor: COR_NOME[id] }));
  }

  async conversar(npc) {
    this.conversando = true;
    npc.olharPara(this.jogador.x);
    this.jogador.olhandoDireita = npc.x > this.jogador.x;
    const t = TEXTOS.espaco;
    if (npc.id === 'claudia') {
      await this.dialogo.mostrar(this.caixas('claudia', t.claudia.antes, t.claudia.nome));
      npc.jaFalou();
      await this.entregarIngressos(npc);
      await this.dialogo.mostrar(this.caixas('claudia', t.claudia.depois, t.claudia.nome));
      await this.abuChegaCorrendo();
      return;
    }
    const d = t.npcs[npc.id];
    await this.dialogo.mostrar(this.caixas(npc.id, d.falas, d.nome));
    npc.jaFalou();
    this.fimDaConversa();
  }

  fimDaConversa() {
    this.conversando = false;
    this.entrada.ignorarAteSoltar();
  }

  // Os ingressos saem da mão da Tia Claudia e voam, um a um, até o contador do HUD.
  entregarIngressos(npc) {
    npc.anims.stop();
    npc.setFrame(1);
    const cam = this.cameras.main;
    const n = ESPACO.ingressos;
    return new Promise((resolve) => {
      for (let i = 0; i < n; i++) {
        this.time.delayedCall(250 + i * ESPACO.intervaloIngressoMs, () => {
          // começa na mão dela (coordenadas de tela, porque o destino é o HUD)
          const mx = npc.x + (npc.flipX ? -12 : 12) - cam.scrollX;
          const my = npc.y - 26 - cam.scrollY;
          const ing = this.add.image(mx, my, 'ingresso').setScrollFactor(0).setDepth(1600);
          const alvo = this.registry.get('posIngressoHud') ?? { x: 196, y: 17 };
          this.tweens.add({
            targets: ing,
            x: alvo.x,
            y: alvo.y,
            angle: 360,
            duration: 600,
            ease: 'Quad.in',
            onComplete: () => {
              ing.destroy();
              this.registry.inc('ingressos', 1);
              tocarEfeito('pegarMaca', { variar: 0.1 });
              if (i === n - 1) {
                this.aviso(npc.x, npc.y - 60, TEXTOS.espaco.ingressos(n));
                tocarVinheta('ingresso');
                npc.setFrame(0);
                this.time.delayedCall(500, resolve);
              }
            },
          });
        });
      }
    });
  }

  aviso(x, y, texto) {
    const t = this.add
      .text(x, y, texto, { fontFamily: FONTES.dialogo, fontSize: '16px', color: CORES_CSS.roxo })
      .setOrigin(0.5)
      .setDepth(20)
      .setShadow(1, 1, CORES_CSS.branco, 0, false, true);
    this.tweens.add({ targets: t, y: y - 18, alpha: 0, delay: 600, duration: 700, onComplete: () => t.destroy() });
  }

  // O Abu entra correndo pela porta do fundo, para perto do jogador e conta a notícia.
  async abuChegaCorrendo() {
    const j = this.jogador;
    const porta = this.porta ?? { x: this.mapa.larguraPx - 20, y: 15 * TILE };
    const abu = this.add.sprite(porta.x, porta.y, 'abu', 1).setOrigin(0.5, 1).setDepth(9).setFlipX(true);
    abu.play('abu-correr');
    tocarEfeito('botao');
    // o jogador e a Tia Claudia olham para a porta
    j.olhandoDireita = true;
    j.setFlipX(false);
    this.claudia?.setFlipX(false);
    // para entre o balcão da Tia Claudia e a porta
    const destinoX = Math.min((this.claudia?.x ?? j.x) + 48, porta.x);
    const dist = Math.abs(porta.x - destinoX);
    await new Promise((resolve) =>
      this.tweens.add({
        targets: abu,
        x: destinoX,
        duration: (dist / ESPACO.velocidadeAbu) * 1000,
        onComplete: resolve,
      }),
    );
    abu.play('abu-aflito');
    this.cameras.main.shake(150, 0.004);
    const t = TEXTOS.espaco;
    await this.dialogo.mostrar([
      ...this.caixas('abu', t.abu.falas, t.abu.nome),
      ...this.caixas('claudia', t.final.falas, t.final.nome),
    ]);
    this.irParaOChefe();
  }

  irParaOChefe() {
    this.terminou = true;
    pararMusica(0.6);
    tocarEfeito('dano');
    const cam = this.cameras.main;
    cam.flash(250, 109, 107, 217);
    cam.fadeOut(800, 46, 26, 51);
    cam.once('camerafadeoutcomplete', () => {
      this.scene.stop('HUD');
      this.scene.start('Chefe');
    });
  }

  // ---------------------------------------------------------------- quadro a quadro

  update(agora, delta) {
    this.entrada.atualizar();
    const j = this.jogador;
    const cam = this.cameras.main;
    cam.setFollowOffset(j.olhandoDireita ? -CAMERA.folgaFrente : CAMERA.folgaFrente, 0);

    // NPCs que ainda não falaram ficam de olho no jogador
    for (const npc of this.npcs) if (!npc.falou) npc.olharPara(j.x);

    if (this.conversando || this.terminou) {
      // parado enquanto conversa (a gravidade continua, para pousar se estava no ar)
      j.body.setVelocityX(0);
      j.body.setGravityY(0);
      j.setAlpha(1);
      if (j.body.blocked.down) j.play('parado', true);
      j.setFlipX(!j.olhandoDireita);
      return;
    }

    j.atualizar(this.entrada, agora, delta, false);
    if (this.entrada.pularApertou && j.body.velocity.y < -200) tocarEfeito('pulo');

    // chegou perto de alguém que ainda não falou: conversa (só a distância em x conta, para não passar
    // pulando por cima sem querer)
    const perto = this.npcs.find((n) => !n.falou && Math.abs(n.x - j.x) < ESPACO.distanciaConversa);
    if (perto) this.conversar(perto);

    // segurança: se cair do mapa por algum motivo, volta ao começo
    if (j.y > this.mapa.alturaPx + 48) j.reposicionar(this.mapa.inicio.x, this.mapa.inicio.y, agora);
  }
}
