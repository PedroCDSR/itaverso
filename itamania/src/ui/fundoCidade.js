import * as Phaser from 'phaser';
import { LARGURA, ALTURA } from '../config.js';

// Fundo de menu: céu em faixas, serra e casario de Itajubá andando devagar. Devolve uma função para o update().
export function fundoCidade(scene, ceu = ['#6FA8F0', '#86B8F4', '#9EC8FF', '#B6D6FF', '#CCE2FF', '#E2EEFF']) {
  const g = scene.add.graphics();
  const h = Math.ceil(ALTURA / ceu.length);
  ceu.forEach((cor, i) => g.fillStyle(Phaser.Display.Color.HexStringToColor(cor).color).fillRect(0, i * h, LARGURA, h + 1));
  const morros = scene.add.tileSprite(0, 0, LARGURA, ALTURA, 'morros').setOrigin(0);
  const casas = scene.add.tileSprite(0, 16, LARGURA, ALTURA, 'casas').setOrigin(0);
  const chao = scene.add.tileSprite(0, ALTURA - 24, LARGURA, 32, 'tiles', 1).setOrigin(0);
  let x = 0;
  return (delta) => {
    x += delta * 0.02;
    morros.tilePositionX = x * 0.3;
    casas.tilePositionX = x;
    chao.tilePositionX = x * 2.2;
  };
}
