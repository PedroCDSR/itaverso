import * as Phaser from 'phaser';
import { LARGURA, ALTURA, TILE, CORES, CORES_CSS, FONTES, CAMERA } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { Entrada } from '../ui/Entrada.js';
import { BotaoSom } from '../ui/BotaoSom.js';
import { tentarTelaCheia } from '../ui/telaCheia.js';
import { bipe } from '../audio/som.js';
import { lerMapa, TIPO_TILE } from '../levels/leitor.js';
import { TESTE } from '../levels/teste.js';
import { Jogador } from '../objects/Jogador.js';

// Cena de teste da Etapa 2: mapa em texto, jogador com a física final, câmera e céu de fim de tarde.
// Objetos (maçã, capivara, toldo que quica...) aparecem como marcadores e ganham vida na Etapa 3.
export class Teste extends Phaser.Scene {
  constructor() {
    super('Teste');
  }

  create() {
    this.jogando = false;
    const mapa = lerMapa(TESTE, 'TESTE');
    this.mapa = mapa;

    // fundo: céu parado + morros que andam devagar (parallax simples)
    this.add.image(0, 0, 'ceu').setOrigin(0).setScrollFactor(0);
    this.morros = this.add.tileSprite(0, 0, LARGURA, ALTURA, 'morros').setOrigin(0).setScrollFactor(0);

    // tiles
    const tm = this.make.tilemap({ data: mapa.tiles, tileWidth: TILE, tileHeight: TILE });
    const tileset = tm.addTilesetImage('tiles', 'tiles', TILE, TILE, 0, 0);
    this.camada = tm.createLayer(0, tileset, 0, 0);
    this.camada.setCollision([TIPO_TILE.chaoTopo, TIPO_TILE.chao]);
    // plataformas e toldos: só colidem por cima (dá para subir por baixo)
    this.camada.forEachTile((t) => {
      if (t.index === TIPO_TILE.plataforma || t.index === TIPO_TILE.toldo) t.setCollision(false, false, true, false);
    });

    this.criarMarcadores(mapa.objetos);

    // mundo: sem parede embaixo, para dar para cair nos buracos
    this.physics.world.setBounds(0, -ALTURA, mapa.larguraPx, mapa.alturaPx + ALTURA * 2);
    this.physics.world.setBoundsCollision(true, true, false, false);

    this.jogador = new Jogador(this, mapa.inicio.x, mapa.inicio.y);
    this.physics.add.collider(this.jogador, this.camada);
    this.checkpoint = { x: mapa.inicio.x, y: mapa.inicio.y };

    this.macas = this.physics.add.group();
    this.physics.add.collider(this.macas, this.camada, (m) => m.destroy());

    // câmera
    const cam = this.cameras.main;
    cam.setBounds(0, 0, mapa.larguraPx, mapa.alturaPx);
    cam.startFollow(this.jogador, true, CAMERA.suavidade, CAMERA.suavidade);
    cam.setDeadzone(CAMERA.zonaMortaLargura, CAMERA.zonaMortaAltura);

    this.entrada = new Entrada(this);
    new BotaoSom(this, LARGURA - 20, 20);
    if (!this.sys.game.device.input.touch) {
      this.add
        .text(LARGURA / 2, 10, TEXTOS.teste.dicaTeclado, { fontFamily: FONTES.dialogo, fontSize: '12px', color: CORES_CSS.branco })
        .setOrigin(0.5, 0)
        .setScrollFactor(0)
        .setDepth(900)
        .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
    }

    this.criarTelaJogar();
  }

  // Marcadores provisórios dos objetos do mapa (Etapa 3 troca por objetos de verdade).
  criarMarcadores(objetos) {
    const cor = { maca: 0xe0453a, sapatilha: CORES.rosa, coracao: 0xff5a7a, capivara: 0x8a5a3a, checkpoint: CORES.verde, fonte: 0x9fb6c9, saida: CORES.amarelo };
    const tam = { capivara: [26, 16], fonte: [44, 24], saida: [18, 30], checkpoint: [6, 28] };
    for (const o of objetos) {
      const [w, h] = tam[o.tipo] || [8, 8];
      const y = tam[o.tipo] ? o.y - h / 2 : o.y - TILE / 2;
      const x = o.tipo === 'fonte' ? o.x + TILE : o.x;
      this.add.rectangle(x, y, w, h, cor[o.tipo]).setStrokeStyle(1, 0x2e1a33);
    }
  }

  criarTelaJogar() {
    const t = TEXTOS.teste;
    const tela = this.add.container(0, 0).setDepth(2000).setScrollFactor(0);
    tela.add(this.add.rectangle(0, 0, LARGURA, ALTURA, CORES.lilas, 0.92).setOrigin(0));
    tela.add(
      this.add
        .text(LARGURA / 2, 70, t.titulo, { fontFamily: FONTES.titulo, fontSize: '24px', color: CORES_CSS.branco })
        .setOrigin(0.5)
        .setShadow(2, 2, CORES_CSS.roxo, 0, false, true),
    );
    const botao = this.add.rectangle(LARGURA / 2, 150, 140, 40, CORES.rosa).setStrokeStyle(3, CORES.roxo);
    tela.add(botao);
    tela.add(
      this.add
        .text(LARGURA / 2, 151, TEXTOS.botoes.jogar, { fontFamily: FONTES.titulo, fontSize: '16px', color: CORES_CSS.roxo })
        .setOrigin(0.5),
    );
    tela.add(
      this.add
        .text(LARGURA / 2, 200, t.tocarJogar, { fontFamily: FONTES.dialogo, fontSize: '16px', color: CORES_CSS.roxo })
        .setOrigin(0.5),
    );
    botao.setInteractive({ useHandCursor: true });
    // pointerup: o navegador só aceita tela cheia quando o dedo sai da tela
    botao.on('pointerup', () => this.comecar(tela));
    this.input.keyboard?.once('keydown-ENTER', () => this.comecar(tela));
  }

  comecar(tela) {
    if (this.jogando) return;
    tentarTelaCheia(this);
    bipe(520, 0.12);
    tela.destroy();
    this.jogando = true;
  }

  update(agora, delta) {
    const e = this.entrada;
    e.atualizar();
    // câmera olha um pouco para a frente do jogador
    const cam = this.cameras.main;
    cam.setFollowOffset(this.jogador.olhandoDireita ? -CAMERA.folgaFrente : CAMERA.folgaFrente, 0);
    this.morros.tilePositionX = cam.scrollX * 0.2;

    if (!this.jogando) {
      this.jogador.body.setVelocityX(0);
      return;
    }

    const pulouAntes = this.jogador.body.velocity.y < 0;
    const soltouMaca = this.jogador.atualizar(e, agora, delta);
    if (!pulouAntes && this.jogador.body.velocity.y < -200) bipe(660, 0.08);

    if (soltouMaca) {
      const dir = this.jogador.olhandoDireita ? 1 : -1;
      const m = this.add.circle(this.jogador.x + 12 * dir, this.jogador.y - 30, 4, 0xe0453a).setStrokeStyle(1, 0x2e1a33);
      this.macas.add(m);
      m.body.setCircle(4).setVelocity(220 * dir, -160);
      this.time.delayedCall(2000, () => m.active && m.destroy());
      bipe(880, 0.05);
    }

    // caiu no buraco: volta ao último checkpoint
    if (this.jogador.y > this.mapa.alturaPx + 48) {
      this.jogador.reposicionar(this.checkpoint.x, this.checkpoint.y);
      cam.flash(150, 255, 176, 250);
    }
  }
}
