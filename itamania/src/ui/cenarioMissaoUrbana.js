import { FONTES } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { PERCURSO_URBANO as MAPA, APOIOS_URBANOS, chaoUrbano } from '../data/missaoUrbana.js';

export function desenharCidade(scene) {
  const ceu = scene.add.graphics().setScrollFactor(0).setDepth(-20);
  for (let y = 0; y < 270; y += 6) {
    const t = y / 270;
    ceu.fillStyle((Math.round(117 + t * 83) << 16) | (Math.round(181 + t * 47) << 8) | 237);
    ceu.fillRect(0, y, 480, 6);
  }
  scene.add.image(240, 152, 'morros').setDisplaySize(600, 78).setAlpha(0.25).setScrollFactor(0).setDepth(-18);
  const horizonte = scene.add.graphics().setScrollFactor(0.15, 0).setDepth(-16);
  for (let x = 0; x < 1500; x += 28) {
    const h = 20 + (x * 7 % 37);
    horizonte.fillStyle([0x9baab3, 0xc5b9a7, 0xb6c3c3][Math.floor(x / 28) % 3]);
    horizonte.fillRect(x, 180 - h, 25, h);
    horizonte.fillStyle(0x8297a5);
    for (let y = 186 - h; y < 174; y += 10) horizonte.fillRect(x + 6, y, 4, 5);
  }
  for (const [nome, x, h] of MAPA.fachadas) {
    const im = scene.add.image(x, chaoUrbano(x) - 4, `urbano-${nome}`).setOrigin(0.5, 1).setDepth(-5);
    im.setScale(h / im.height);
  }
  const t = TEXTOS.missao.urbano;
  scene.add.text(296, chaoUrbano(296) - 143, t.clube, {
    fontFamily: FONTES.titulo, fontSize: '7px', color: '#514d50', backgroundColor: '#e8dec7', padding: { x: 4, y: 3 },
  }).setOrigin(0.5).setDepth(-3);
  scene.add.text(1464, chaoUrbano(1464) - 76, t.cafe, {
    fontFamily: FONTES.titulo, fontSize: '8px', color: '#fff0cf', backgroundColor: '#685043', padding: { x: 6, y: 4 },
  }).setOrigin(0.5).setDepth(-3);
  scene.add.image(818, chaoUrbano(818) - 5, 'urbano-fonte').setOrigin(0.5, 1).setScale(1.3).setDepth(-2);
  scene.add.image(550, chaoUrbano(550) - 6, 'limezu-palmeira_imp1').setOrigin(0.5, 1).setDepth(-4);
  for (const x of [1216, 3160, 4864]) scene.add.image(x, chaoUrbano(x) - 6, 'limezu-arvore_rua').setOrigin(0.5, 1).setScale(0.8).setDepth(-4);
  for (let x = 600; x < 5360; x += 640) scene.add.image(x, chaoUrbano(x) - 3, 'limezu-poste').setOrigin(0.5, 1).setDepth(-1);
  const chao = scene.add.graphics().setDepth(1);
  chao.fillStyle(0x8c9096); chao.beginPath(); chao.moveTo(0, chaoUrbano(0));
  for (const [x, y] of MAPA.perfil) chao.lineTo(x, y);
  chao.lineTo(MAPA.largura, MAPA.altura); chao.lineTo(0, MAPA.altura); chao.closePath(); chao.fillPath();
  for (let x = 0; x < MAPA.largura; x += 16) {
    const y = chaoUrbano(x), seguinte = chaoUrbano(x + 16);
    chao.lineStyle(12, 0xd9d9cb).lineBetween(x, y + 6, x + 16, seguinte + 6);
    chao.lineStyle(2, 0xf7edcf).lineBetween(x, y, x + 16, seguinte);
    chao.lineStyle(1, 0x999f9f).lineBetween(x, y + 2, x, y + 11);
    for (let dy = 24; dy < 270; dy += 16) {
      chao.lineStyle(1, 0x717b86).lineBetween(x, y + dy, x + 16, seguinte + dy);
      if ((x / 16 + dy / 8) % 2 === 0) chao.lineBetween(x, y + dy, x, y + dy + 16);
      chao.lineStyle(1, 0xb5b5a9).lineBetween(x + 2, y + dy + 2, x + 11, y + dy + 2);
    }
  }
  for (const p of APOIOS_URBANOS) desenharApoio(scene, p);
  scene.add.text(2496, chaoUrbano(2496) - 19, t.toldo, {
    fontFamily: FONTES.dialogo, fontSize: '13px', color: '#70452f', backgroundColor: '#fff0c9', padding: { x: 3, y: 2 },
  }).setOrigin(0.5, 1).setDepth(3);
}

function desenharApoio(scene, p) {
  const g = scene.add.graphics().setDepth(3), fundo = chaoUrbano(p.x + p.largura / 2);
  if (p.tipo === 'banco') {
    scene.add.image(p.x + p.largura / 2, p.y - 4, 'limezu-banco_h').setDisplaySize(p.largura, 30).setDepth(3);
    g.fillStyle(0x655c58); g.fillRect(p.x + 8, p.y + 2, 4, fundo - p.y); g.fillRect(p.x + p.largura - 12, p.y + 2, 4, fundo - p.y);
  } else if (p.tipo === 'toldo') {
    scene.toldoVisual = scene.add.image(p.x, p.y, 'urbano-toldo').setOrigin(0, 0).setDepth(4);
    g.lineStyle(3, 0x66584e).lineBetween(p.x + 5, p.y, p.x + 16, p.y + 32);
    g.lineBetween(p.x + p.largura - 5, p.y, p.x + p.largura - 16, p.y + 32);
  } else if (p.tipo === 'marquise') {
    g.fillStyle(0xbdb8a5); g.fillRect(p.x, p.y, p.largura, 10); g.lineStyle(4, 0x655c58);
    for (const dx of [12, p.largura - 24]) g.lineBetween(p.x + dx, p.y + 9, p.x + dx + 12, p.y + 36);
  } else {
    g.fillStyle(0xa4a69b); g.fillRect(p.x, p.y, p.largura, fundo - p.y + 4);
    for (let dy = 10; dy < fundo - p.y; dy += 10) {
      g.lineStyle(1, 0x777f80).lineBetween(p.x, p.y + dy, p.x + p.largura, p.y + dy);
      for (let dx = 12; dx < p.largura; dx += 24) g.lineBetween(p.x + dx, p.y + dy, p.x + dx, p.y + dy + 10);
    }
    if (p.tipo === 'jardim') scene.add.image(p.x + p.largura / 2, p.y - 5, 'limezu-flores').setOrigin(0.5, 1).setDisplaySize(p.largura - 8, 14).setDepth(2);
  }
  g.fillStyle(0xf2e6c5); g.fillRect(p.x, p.y, p.largura, 3);
}

export function bandeira(scene, x, nome, chegada = false) {
  const y = chaoUrbano(x), g = scene.add.graphics().setDepth(4);
  g.fillStyle(0x6a5d50); g.fillRect(x - 2, y - 57, 4, 57);
  g.fillStyle(chegada ? 0xe5b458 : 0x477bca); g.fillRect(x, y - 56, chegada ? 82 : 30, 20);
  scene.add.text(x + (chegada ? 41 : 15), y - 46, nome, {
    fontFamily: FONTES.titulo, fontSize: chegada ? '7px' : '8px', color: chegada ? '#473c37' : '#ffffff',
  }).setOrigin(0.5).setDepth(5);
  return g;
}
