import * as Phaser from 'phaser';
import { TILE } from '../config.js';
import { CENARIO_PNG, SPRITES_PNG, TEM_MAPA, ArteTiles, ArteObjetos, ArteHeroi } from '../art/index.js';
import { texturaDeQuadros } from '../art/matriz.js';
import { HEROIS, escolherHeroi } from '../genero.js';
import { carregar, estado } from '../estado.js';
import { FASES } from '../levels/index.js';
import { recuperarMissaoInterrompida, iniciarMissao } from '../systems/encontros.js';
import { REGIAO_PRACA } from '../data/micromundos.js';

import { OBJETOS_PRACA, PERSONAGENS_PRACA } from '../data/pracaArte.js';

// Carrega a arte e cria as animações. Teste direto pelo link: ?fase=1 a ?fase=4, ?heroi=helena, ?bone=1,
// ?pao=1 (já com o pão de queijo), ?cena=Praca | Mapa | Titulo | Fim.
export class Preload extends Phaser.Scene {
  constructor() {
    super('Preload');
  }

  preload() {
    const barra = this.add.rectangle(140, 135, 0, 8, 0xffd43a).setOrigin(0, 0.5);
    this.add.rectangle(140, 135, 200, 8).setOrigin(0, 0.5).setStrokeStyle(1, 0xffffff);
    this.load.on('progress', (p) => (barra.width = 200 * p));
    for (const nome of CENARIO_PNG) this.load.image(nome, `assets/cenario/${nome}.png`);
    for (const [nome, [w, h]] of Object.entries(SPRITES_PNG)) {
      this.load.spritesheet(nome, `assets/sprites/${nome}.png`, { frameWidth: w, frameHeight: h });
    }
    for (const chave of Object.keys(HEROIS)) {
      for (const forma of ['normal', 'grande']) {
        const [w, h] = ArteHeroi.TAMANHOS[forma];
        this.load.spritesheet(`heroi-${chave}-${forma}`, `assets/sprites/heroi-${chave}-${forma}.png`, { frameWidth: w, frameHeight: h });
      }
    }
    // Praça andável: mapa do Tiled e arte do Modern Exteriors (LimeZu); balões do Ninja Adventure (CC0)
    this.load.tilemapTiledJSON('praca', 'assets/mapas/praca.tmj');
    this.load.image('limezu-chao', 'assets/limezu/chao.png');
    this.load.image('capivara-exploradora', 'assets/sprites/capivara-exploradora.webp');
    for (const nome of ['terreno', 'ceu', 'montanhas', 'arvore', 'arbusto', 'plataforma', 'placa']) {
      this.load.image(`sunny-${nome}`, `assets/sunnyland/${nome}.png`);
    }
    this.load.spritesheet('sunny-gamba', 'assets/sunnyland/gamba.png', { frameWidth: 36, frameHeight: 28 });
    for (const nome of ['clube', 'cafe', 'sobrado', 'loja', 'tijolos', 'verde', 'azul', 'brancoazul', 'concha', 'fonte', 'igreja', 'toldo', 'ficha', 'estrela']) {
      this.load.image(`urbano-${nome}`, `assets/missao-urbana/${nome}.png`);
    }
    for (const o of OBJETOS_PRACA) this.load.image(`limezu-${o}`, `assets/limezu/objetos/${o}.png`);
    for (const c of PERSONAGENS_PRACA) {
      this.load.spritesheet(`limezu-${c}`, `assets/limezu/personagens/${c}.png`, { frameWidth: 16, frameHeight: 32 });
    }
    for (const e of ['exclamacao', 'reticencias', 'coracao']) this.load.image(`ninja-${e}`, `assets/ninja/ui/${e}.png`);
    // o mapa do Pedro em alta resolução é mostrado em HTML (ui/mapaHtml.js); aqui só aquece o cache do navegador
    if (TEM_MAPA) new Image().src = 'assets/mapa-hd.png';
  }

  create() {
    // tiles (o 0 fica vazio; 5 e 6 são os invisíveis)
    const T = ArteTiles;
    const quadros = T.ORDEM.map((n) => T.TILES[n] || null).concat([null, null]);
    texturaDeQuadros(this, 'tiles', quadros, T.PALETA, TILE, TILE);
    for (const nome of ['capivara', 'coracao']) {
      const sp = ArteObjetos.SPRITES[nome];
      texturaDeQuadros(this, nome, sp.quadros, ArteObjetos.PALETA, sp.largura, sp.altura);
    }

    const anim = (key, textura, frames, frameRate, repeat = -1) =>
      this.anims.create({ key, frames: frames.map((frame) => ({ key: textura, frame })), frameRate, repeat });

    // Folha original com quatro direções e quatro passos. Os quadros mantêm a mesma escala.
    const capivara = this.textures.get('capivara-exploradora');
    const lado = Math.floor(capivara.source[0].width / 4);
    ['baixo', 'esquerda', 'direita', 'cima'].forEach((dir, linha) => {
      for (let coluna = 0; coluna < 4; coluna++) capivara.add(linha * 4 + coluna, 0, coluna * lado, linha * lado, lado, lado);
      anim(`exploradora-parado-${dir}`, 'capivara-exploradora', [linha * 4], 1);
      anim(`exploradora-andar-${dir}`, 'capivara-exploradora', [0, 1, 2, 3].map((c) => linha * 4 + c), 8);
    });

    // herói: uma animação por herói × forma × boné (sem boné = quadros 0..n-1; com boné = n..2n-1)
    const H = ArteHeroi;
    const n = H.NOMES.length;
    for (const chave of Object.keys(HEROIS)) {
      for (const forma of ['normal', 'grande']) {
        for (const [b, desloc] of [['s', 0], ['b', n]]) {
          for (const [nome, a] of Object.entries(H.ANIMACOES)) {
            anim(`${chave}-${forma}-${b}-${nome}`, `heroi-${chave}-${forma}`, a.quadros.map((q) => H.NOMES.indexOf(q) + desloc), a.fps, a.repetir);
          }
        }
      }
    }
    // personagens da praça: 24 quadros por linha (direita, cima, esquerda, baixo; 6 cada); linha 0 parado, 1 andando
    for (const c of PERSONAGENS_PRACA) {
      ['direita', 'cima', 'esquerda', 'baixo'].forEach((dir, i) => {
        const q = (linha) => [0, 1, 2, 3, 4, 5].map((k) => linha * 24 + i * 6 + k);
        anim(`${c}-parado-${dir}`, `limezu-${c}`, q(0), 6);
        anim(`${c}-andar-${dir}`, `limezu-${c}`, q(1), 10);
      });
    }
    anim('itacoin-girar', 'itacoin', [0, 1, 2, 3], 8);
    anim('gamba-andar', 'sunny-gamba', [0, 1, 2, 3, 4, 5], 9);
    anim('cafe-vapor', 'cafecomleite', [0, 1], 3);
    anim('heli-voar', 'heliceu', [0, 1], 16);
    anim('pombo-andar', 'pombo', [0, 1], 5);
    anim('pombo-bicar', 'pombo', [2, 0], 5);
    anim('pombo-voar', 'pombo', [3, 4], 10);
    anim('pombo-comer', 'pombo', [5, 2], 5);
    anim('capivara-andar', 'capivara', [0, 1], 4);
    anim('capivara-comer', 'capivara', [2, 3], 5);
    anim('capivara-dormir', 'capivara', [4, 5], 1.5);

    carregar();
    const interrompida = recuperarMissaoInterrompida();
    const q = new URLSearchParams(window.location.search);
    // Atalho exclusivo do Vite para avaliar a missão sem depender de alterações na praça.
    if (import.meta.env.DEV && q.get('missao') === 'urbana') {
      const encontro = REGIAO_PRACA.encontros[q.get('fuga') === '1' ? 1 : 0];
      const sessao = iniciarMissao(REGIAO_PRACA, encontro, { x: 848, y: 596 }, 'cima');
      if (sessao) { this.scene.start('Missao', { sessao }); return; }
    }
    if (q.get('heroi')) {
      escolherHeroi(q.get('heroi'));
      estado.heroi = q.get('heroi');
    }
    if (q.get('bone')) estado.bone = true;
    if (q.get('pao')) {
      estado.temPao = true;
      estado.paes = Math.max(estado.paes, 5);
    }
    const fase = Number(q.get('fase'));
    if (interrompida || estado.retornoExploracao) {
      this.scene.start('Praca');
    } else if (FASES[fase]) {
      estado.liberada = Math.max(estado.liberada, fase);
      if (fase > 3) estado.bone = true;
      this.scene.start('Fase', { fase });
    } else {
      this.scene.start(q.get('cena') || 'Titulo');
    }
  }
}
