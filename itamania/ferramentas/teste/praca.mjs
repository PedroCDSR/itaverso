// Com o Vite rodando: node ferramentas/teste/praca.mjs [url] [pasta de capturas].
// Playwright é ferramenta externa de teste, como no robô jogar.mjs.
import { createRequire } from 'node:module';
import assert from 'node:assert/strict';
import fs from 'node:fs';
const { chromium } = createRequire(import.meta.url)('playwright');
const url = process.argv[2] || 'http://localhost:5180/';
const pasta = process.argv[3] || 'capturas';
fs.mkdirSync(pasta, { recursive: true });
const browser = await chromium.launch({ args: ['--use-angle=swiftshader'] });
try {
  const page = await browser.newPage({ viewport: { width: 844, height: 390 } });
  const erros = [];
  page.on('pageerror', (e) => erros.push(e.message));
  page.on('console', (m) => { if (m.type() === 'error') erros.push(m.text()); });
  await page.goto(url);
  await page.waitForFunction(() => window.jogo?.scene.isActive('Titulo'));
  await page.waitForTimeout(500);
  await page.screenshot({ path: `${pasta}/capivara-titulo.png` });
  await page.keyboard.press('Enter');
  await page.waitForFunction(() => window.praca?.heroi?.active);
  await page.waitForTimeout(900);
  for (let i = 0; i < 5; i++) { await page.keyboard.press('Enter'); await page.waitForTimeout(120); }
  assert.equal(await page.evaluate(() => praca.heroi.texture.key), 'capivara-exploradora');
  
  for (const [tecla, dir] of [['ArrowLeft', 'esquerda'], ['ArrowRight', 'direita'], ['ArrowUp', 'cima'], ['ArrowDown', 'baixo']]) {
    const antes = await page.evaluate(() => ({ x: praca.heroi.x, y: praca.heroi.y }));
    await page.keyboard.down(tecla);
    await page.waitForTimeout(300);
    assert.equal(await page.evaluate(() => praca.heroi.anims.currentAnim.key), `exploradora-andar-${dir}`);
    await page.screenshot({ path: `${pasta}/capivara-${dir}.png` });
    assert(await page.evaluate(({ x, y }) => Math.hypot(praca.heroi.x - x, praca.heroi.y - y) > 1, antes));
    await page.keyboard.up(tecla);
    await page.waitForTimeout(100);
  }

  // A moeda é recolhida pelo overlap da física, e continua recolhida depois de recarregar.
  const antes = await page.evaluate(() => {
    const moeda = praca.moedas.getChildren()[0];
    const n = jogo.registry.get('itacoins');
    praca.heroi.body.reset(moeda.x, moeda.y + 4);
    return n;
  });
  await page.waitForFunction((n) => jogo.registry.get('itacoins') === n + 1, antes);
  // Aproximação e conversa pelo controle real, sem chamar conversar diretamente.
  await page.evaluate(() => {
    const alvo = praca.alvos.find((a) => a.npc && !a.npc.dados.anda);
    praca.heroi.body.reset(alvo.x, alvo.y + 22);
    praca.direcao = 'cima';
  });
  await page.waitForTimeout(200);
  await page.keyboard.down('Space');
  await page.waitForTimeout(150);
  await page.keyboard.up('Space');
  await page.waitForSelector('.dialogo.ativa');
  await page.screenshot({ path: `${pasta}/capivara-conversa.png` });
  for (let i = 0; i < 12 && await page.evaluate(() => praca.ocupado); i++) {
    await page.keyboard.press('Enter'); await page.waitForTimeout(150);
  }
  assert.equal(await page.evaluate(() => praca.ocupado), false);
  const parede = await page.evaluate(() => {
    const dados = praca.colisao.layer.data;
    const candidatos = [];
    for (let y = 1; y < dados.length - 3; y++) for (let x = 2; x < dados[y].length - 2; x++) {
      if (dados[y][x].collides && !dados[y + 1][x].collides && !dados[y + 2][x].collides) candidatos.push({ x: x * 16 + 8, y: (y + 1) * 16 });
    }
    const alvo = candidatos.sort((a, b) => Math.hypot(a.x - praca.heroi.x, a.y - praca.heroi.y) - Math.hypot(b.x - praca.heroi.x, b.y - praca.heroi.y))[0];
    praca.heroi.body.reset(alvo.x, alvo.y + 16);
    return alvo;
  });
  await page.keyboard.down('ArrowUp');
  await page.waitForTimeout(650);
  assert(await page.evaluate((y) => praca.heroi.body.blocked.up && praca.heroi.body.y >= y - 0.1, parede.y));
  await page.keyboard.up('ArrowUp');
  await page.keyboard.press('Escape');
  await page.waitForFunction(() => jogo.scene.isActive('Pausa'));
  await page.screenshot({ path: `${pasta}/capivara-pausa.png` });
  await page.reload();
  await page.waitForFunction(() => window.jogo?.scene.isActive('Titulo'));
  await page.keyboard.press('Enter');
  await page.waitForFunction(() => window.praca?.heroi?.active);
  assert.equal(await page.evaluate(() => jogo.registry.get('itacoins')), antes + 1);
  await page.waitForTimeout(600);
  await page.screenshot({ path: `${pasta}/capivara-praca.png` });
  const mobile = await browser.newPage({ viewport: { width: 844, height: 390 }, hasTouch: true, isMobile: true });
  mobile.on('pageerror', (e) => erros.push(e.message));
  mobile.on('console', (m) => { if (m.type() === 'error') erros.push(m.text()); });
  await mobile.addInitScript(() => localStorage.setItem('itamania-progresso-v1', JSON.stringify({ heroi: 'geraldo', viuPraca: true })));
  await mobile.goto(`${url}?cena=Praca`);
  await mobile.waitForFunction(() => window.praca?.heroi?.active);
  await mobile.waitForTimeout(800);
  const posicao = await mobile.evaluate(() => praca.heroi.x);
  const cdp = await mobile.context().newCDPSession(mobile);
  const canvas = await mobile.locator('canvas').boundingBox();
  const x = canvas.x + canvas.width * 0.25, y = canvas.y + canvas.height * 0.7;
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y }] });
  await mobile.waitForTimeout(100);
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x + 60, y }] });
  await mobile.waitForTimeout(600);
  assert(await mobile.evaluate((antes) => praca.heroi.x > antes + 8, posicao));
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  await mobile.screenshot({ path: `${pasta}/capivara-toque.png` });
  assert.deepEqual(erros, []);
  console.log('PASS: título, praça, quatro direções, moeda persistente, conversa, colisão, pausa e joystick de toque; zero erros.');
} finally {
  await browser.close();
}
