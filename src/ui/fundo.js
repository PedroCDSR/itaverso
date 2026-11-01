import { LARGURA, ALTURA, TILE } from '../config.js';
import { ArteTiles } from '../art/index.js';

// Fundo de fim de tarde usado nos menus (Título e Intro): céu, morros e uma faixa de chão.
// Devolve os morros, para a cena fazer o parallax andar devagar no update().
export function fundoEntardecer(scene, { chao = true } = {}) {
  scene.add.image(0, 0, 'ceu').setOrigin(0).setScrollFactor(0);
  const morros = scene.add.tileSprite(0, 0, LARGURA, ALTURA, 'morros').setOrigin(0).setScrollFactor(0);
  if (chao) {
    const topo = ArteTiles.ORDEM.indexOf('chaoTopo');
    const meio = ArteTiles.ORDEM.indexOf('chao');
    for (let x = 0; x < LARGURA; x += TILE) {
      scene.add.image(x, ALTURA - TILE * 2, 'tiles', topo).setOrigin(0);
      scene.add.image(x, ALTURA - TILE, 'tiles', meio).setOrigin(0);
    }
  }
  return morros;
}
