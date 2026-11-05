// Teste do ciclo completo. Uso: node ferramentas/teste/missao.mjs [url] [capturas].
// Playwright externo, como nos outros robôs deste repositório.
import { createRequire } from 'node:module';
import assert from 'node:assert/strict';
import fs from 'node:fs';
const { chromium } = createRequire(import.meta.url)('playwright');
const url = process.argv[2] || 'http://localhost:5181/';
const pasta = process.argv[3] || 'capturas';
fs.mkdirSync(pasta, { recursive: true });
const navegador = await chromium.launch({ args: ['--use-angle=swiftshader'] });
const erros = [];
try {
  const pagina = await navegador.newPage({ viewport: { width: 960, height: 540 } });
  pagina.on('pageerror', (e) => erros.push(e.message));
  pagina.on('console', (m) => { if (m.type() === 'error') erros.push(m.text()); });
  await pagina.addInitScript(() => {
    if (!localStorage.getItem('itamania-progresso-v1')) localStorage.setItem('itamania-progresso-v1', JSON.stringify({ heroi: 'geraldo', viuPraca: true, itacoins: 9, moedasPraca: [0] }));
  });
  await pagina.goto(`${url}?cena=Praca`);
  await pagina.waitForFunction(() => window.praca?.heroi?.active);
  async function fecharDialogo() {
    for (let i = 0; i < 12 && await pagina.evaluate(() => praca.ocupado); i++) {
      await pagina.keyboard.press('Enter'); await pagina.waitForTimeout(130);
    }
  }
  async function encontro() {
    await fecharDialogo();
    await pagina.evaluate(() => { praca.heroi.body.reset(848, 596); praca.direcao = 'cima'; });
    await pagina.waitForTimeout(180);
    await pagina.keyboard.down('Space'); await pagina.waitForTimeout(130); await pagina.keyboard.up('Space');
    await pagina.waitForFunction(() => jogo.scene.isActive('Encontro'));
    await pagina.waitForTimeout(500);
    await pagina.screenshot({ path: `${pasta}/encontro.png` });
    await pagina.waitForFunction(() => jogo.scene.isActive('Missao') && window.missao?.jogador?.active);
    await pagina.waitForTimeout(400);
  }
  async function jogarAteFim() {
    await pagina.evaluate(() => {
      const s = window.missao;
      const robo = { segurarAte: 0, anterior: false };
      s.entrada.atualizar = function () {
        this.esquerda = false; this.direita = true; this.maca = false; this.macaApertou = false;
        const j = s.jogador;
        const chao = j.body.blocked.down || j.body.touching.down;
        const buraco = false; // A calçada urbana é contínua.
        const inimigo = s.inimigos.getChildren().some((i) => i.active && i.x > j.x && i.x - j.x < 64);
        if (chao && (buraco || inimigo)) robo.segurarAte = s.time.now + 390;
        this.pular = s.time.now < robo.segurarAte;
        this.pularApertou = this.pular && !robo.anterior;
        robo.anterior = this.pular;
      };
    });
    await pagina.waitForFunction(() => window.missao?.terminou, null, { timeout: 80000 });
    const resultado = await pagina.evaluate(() => ({ venceu: JSON.parse(localStorage.getItem('itamania-progresso-v1')).retornoExploracao.venceu, x: missao.jogador.x, vidas: missao.vidas, pontos: missao.placar.pontos }));
    assert.equal(resultado.venceu, true, JSON.stringify(resultado));
    assert(resultado.x >= 5512);
    console.log('Travessia física concluída:', JSON.stringify(resultado));
  }
  await encontro();
  await pagina.screenshot({ path: `${pasta}/missao-inicio.png` });
  await jogarAteFim();
  await pagina.screenshot({ path: `${pasta}/missao-vitoria.png` });
  const saldoVitoria = await pagina.evaluate(() => JSON.parse(localStorage.getItem('itamania-progresso-v1')).itacoins);
  assert(saldoVitoria > 9);
  await pagina.keyboard.press('Enter');
  await pagina.waitForFunction(() => jogo.scene.isActive('Praca'));
  assert.deepEqual(await pagina.evaluate(() => [praca.heroi.x, praca.heroi.y]), [848, 596]);
  console.log('PASS: vitória retorna à posição original com recompensa.');
  await pagina.waitForTimeout(800); await fecharDialogo();
  await pagina.screenshot({ path: `${pasta}/praca-retorno.png` });
  // A segunda sessão usa o mesmo motor físico e comprova que a pausa não deixa a próxima missão congelada.
  await encontro();
  await pagina.keyboard.press('Escape');
  await pagina.waitForFunction(() => jogo.scene.isActive('Pausa'));
  const antes = await pagina.evaluate(() => missao.jogador.x);
  await pagina.waitForTimeout(300);
  assert.equal(await pagina.evaluate(() => missao.jogador.x), antes);
  await pagina.keyboard.press('Escape');
  await pagina.waitForFunction(() => !jogo.scene.isActive('Pausa'));
  // Queda e derrota são exercitadas pela física, sem chamar finalizar diretamente.
  for (let i = 0; i < 3; i++) {
    await pagina.evaluate(() => missao.jogador.body.reset(704, 800));
    await pagina.waitForTimeout(1550);
  }
  assert.equal(await pagina.evaluate(() => JSON.parse(localStorage.getItem('itamania-progresso-v1')).retornoExploracao.venceu), false);
  assert.equal(await pagina.evaluate(() => JSON.parse(localStorage.getItem('itamania-progresso-v1')).itacoins), saldoVitoria);
  await pagina.screenshot({ path: `${pasta}/missao-derrota.png` });
  await pagina.keyboard.press('Enter');
  await pagina.waitForFunction(() => jogo.scene.isActive('Praca'));
  assert.deepEqual(await pagina.evaluate(() => [praca.heroi.x, praca.heroi.y]), [664, 598.4]);
  console.log('PASS: derrota volta ao ponto seguro sem perda de progresso.');
  await pagina.waitForTimeout(800); await fecharDialogo();
  await encontro();
  await pagina.reload();
  await pagina.waitForFunction(() => window.jogo?.scene.isActive('Praca'));
  assert.deepEqual(await pagina.evaluate(() => [praca.heroi.x, praca.heroi.y]), [848, 596]);
  assert.equal(await pagina.evaluate(() => JSON.parse(localStorage.getItem('itamania-progresso-v1')).encontros.pendente), null);
  assert.equal(await pagina.evaluate(() => JSON.parse(localStorage.getItem('itamania-progresso-v1')).itacoins), saldoVitoria);
  console.log('PASS: recarga recupera a praça sem duplicar recompensa.');
  await pagina.waitForTimeout(800); await fecharDialogo();
  // Uma zona comum usa o mesmo contrato para iniciar a variante de fuga.
  await pagina.evaluate(() => {
    praca.heroi.body.reset(900, 620);
    praca.encontros.ultima = { x: 900, y: 620 };
    praca.encontros.distancia = 200;
    praca.encontros.liberarEm = 0;
    praca.encontros.sorteio = () => 0;
  });
  await pagina.waitForFunction(() => jogo.scene.isActive('Missao') && window.missao?.def.tipo === 'fuga');
  await pagina.waitForTimeout(450);
  assert(await pagina.evaluate(() => !!missao.perseguidor?.active));
  await jogarAteFim();
  await pagina.screenshot({ path: `${pasta}/fuga-vitoria.png` });
  assert.deepEqual(erros, []);
  console.log('PASS: encontro especial, comum, travessia, fuga, pausa, vitória, derrota e recuperação; zero erros.');
} finally {
  await navegador.close();
}
