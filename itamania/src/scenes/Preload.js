import * as Phaser from 'phaser';
import { TILE } from '../config.js';
import { CENARIO_PNG, SPRITES_PNG, TEM_MAPA, ArteTiles, ArteObjetos, ArteHeroi } from '../art/index.js';
import { texturaDeQuadros } from '../art/matriz.js';
import { HEROIS, escolherHeroi } from '../genero.js';
import { carregar, estado } from '../estado.js';
import { FASES } from '../levels/index.js';

// Arte do pacote Ninja Adventure usada na praça (public/assets/ninja/)
const NINJA_TILESETS = ['TilesetFloor', 'TilesetWater', 'TilesetNature', 'TilesetHouse', 'TilesetElement', 'TilesetLogic'];
const NINJA_PERSONAGENS = ['Boy', 'Princess', 'OldMan', 'OldWoman', 'Woman', 'Villager4', 'Villager3', 'Noble'];

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
    // Praça andável: mapa do Tiled e arte do pacote Ninja Adventure (CC0)
    this.load.tilemapTiledJSON('praca', 'assets/mapas/praca.tmj');
    for (const t of NINJA_TILESETS) this.load.image(`ninja-${t}`, `assets/ninja/tilesets/${t}.png`);
    for (const c of NINJA_PERSONAGENS) {
      this.load.spritesheet(`ninja-${c}`, `assets/ninja/personagens/${c}.png`, { frameWidth: 16, frameHeight: 16 });
    }
    this.load.spritesheet('ninja-Cat', 'assets/ninja/personagens/Cat.png', { frameWidth: 16, frameHeight: 16 });
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
    // personagens do pacote: quadro = linha * 4 + coluna (colunas: baixo, cima, esquerda, direita)
    for (const c of NINJA_PERSONAGENS) {
      ['baixo', 'cima', 'esquerda', 'direita'].forEach((dir, col) => {
        anim(`${c}-andar-${dir}`, `ninja-${c}`, [0, 1, 2, 3].map((l) => l * 4 + col), 7);
        anim(`${c}-parado-${dir}`, `ninja-${c}`, [col], 1);
      });
    }
    anim('gato-parado', 'ninja-Cat', [0, 1], 2);
    anim('itacoin-girar', 'itacoin', [0, 1, 2, 3], 8);
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
    const q = new URLSearchParams(window.location.search);
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
    if (FASES[fase]) {
      estado.liberada = Math.max(estado.liberada, fase);
      if (fase > 3) estado.bone = true;
      this.scene.start('Fase', { fase });
    } else {
      this.scene.start(q.get('cena') || 'Titulo');
    }
  }
}
