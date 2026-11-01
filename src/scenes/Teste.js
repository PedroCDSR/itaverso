import * as Phaser from 'phaser';
import { LARGURA, ALTURA, TILE, CORES, CORES_CSS, FONTES, CAMERA } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { Entrada } from '../ui/Entrada.js';
import { BotaoSom } from '../ui/BotaoSom.js';
import { BotaoPausa } from '../ui/BotaoPausa.js';
import { somarSapatilha, sapatilhas } from '../estado.js';
import { FINAL } from '../fluxo.js';
import { bipe } from '../audio/som.js';
import { lerMapa, TIPO_TILE } from '../levels/leitor.js';
import { TESTE } from '../levels/teste.js';
import { Jogador } from '../objects/Jogador.js';

// Fase de teste (Etapas 2 e 7): mapa em texto, jogador com a física final, câmera e céu de fim de tarde.
// Enquanto as fases de verdade (Etapas 3 a 6) não existem, ela faz o papel do jogo entre a Intro e o Final:
// as sapatilhas já contam e a saída (E) leva ao Final. Os outros objetos ainda são só marcadores.
export class Teste extends Phaser.Scene {
  constructor() {
    super('Teste');
  }

  create() {
    this.jogando = true;
    this.cameras.main.fadeIn(250, 158, 158, 255);
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
    this.botaoSom = new BotaoSom(this, LARGURA - 20, 20);
    new BotaoPausa(this, LARGURA - 56, 20, () => this.abrirPausa());
    this.input.keyboard?.on('keydown-ESC', () => this.abrirPausa());
    this.input.keyboard?.on('keydown-P', () => this.abrirPausa());
    // ao voltar da pausa: som pode ter mudado e as teclas não podem ficar "presas"
    this.events.on('resume', () => {
      this.botaoSom.desenhar();
      this.input.keyboard?.resetKeys();
    });

    // contador provisório de sapatilhas (o HUD completo vem na Etapa 3)
    this.contador = this.add
      .text(12, 12, '', { fontFamily: FONTES.titulo, fontSize: '8px', color: CORES_CSS.branco })
      .setScrollFactor(0)
      .setDepth(1001)
      .setBackgroundColor(CORES_CSS.roxo)
      .setPadding(6, 5, 6, 4);
    this.atualizarContador();
    this.ligarObjetos();
    if (!this.sys.game.device.input.touch) {
      this.add
        .text(LARGURA / 2, 40, TEXTOS.teste.dicaTeclado, { fontFamily: FONTES.dialogo, fontSize: '12px', color: CORES_CSS.branco })
        .setOrigin(0.5, 0)
        .setScrollFactor(0)
        .setDepth(900)
        .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
    }

  }

  // Marcadores provisórios dos objetos do mapa (Etapa 3 troca por objetos de verdade).
  criarMarcadores(objetos) {
    const cor = { maca: 0xe0453a, sapatilha: CORES.rosa, coracao: 0xff5a7a, capivara: 0x8a5a3a, checkpoint: CORES.verde, fonte: 0x9fb6c9, saida: CORES.amarelo };
    const tam = { capivara: [26, 16], fonte: [44, 24], saida: [18, 30], checkpoint: [6, 28] };
    this.marcadores = [];
    for (const o of objetos) {
      const [w, h] = tam[o.tipo] || [8, 8];
      const y = tam[o.tipo] ? o.y - h / 2 : o.y - TILE / 2;
      const x = o.tipo === 'fonte' ? o.x + TILE : o.x;
      const obj = this.add.rectangle(x, y, w, h, cor[o.tipo]).setStrokeStyle(1, 0x2e1a33);
      this.marcadores.push({ tipo: o.tipo, obj });
    }
  }

  // Sapatilhas que somam e a saída que leva ao Final.
  ligarObjetos() {
    this.saindo = false;
    for (const m of this.marcadores) {
      if (m.tipo !== 'sapatilha' && m.tipo !== 'saida') continue;
      this.physics.add.existing(m.obj, true);
      this.physics.add.overlap(this.jogador, m.obj, () => {
        if (m.tipo === 'sapatilha') {
          m.obj.destroy();
          somarSapatilha(this);
          this.atualizarContador();
          bipe(990, 0.06);
        } else {
          this.irParaFinal();
        }
      });
    }
  }

  atualizarContador() {
    this.contador.setText(`SAPATILHAS ${sapatilhas(this)}`);
  }

  abrirPausa() {
    if (!this.scene.isActive() || this.saindo) return;
    this.scene.pause();
    this.scene.launch('Pausa', { cena: this.scene.key });
  }

  irParaFinal() {
    if (this.saindo) return;
    this.saindo = true;
    this.jogando = false;
    bipe(784, 0.25);
    this.cameras.main.fadeOut(400, 0, 0, 0);
    this.cameras.main.once('camerafadeoutcomplete', () => this.scene.start(FINAL));
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
