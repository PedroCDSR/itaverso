// Abre o jogo no Chromium, tira capturas de cada tela e lista erros do console.
// Uso: node ferramentas/teste/capturas.mjs [url-base] [pasta]
import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)('playwright');
const base = process.argv[2] || 'http://localhost:5180/';
const pasta = process.argv[3] || '.';
const navegador = await chromium.launch({ args: ['--use-angle=swiftshader'] });
const erros = [];
async function tela(caminho, nome, esperaMs = 2500, acao) {
  const p = await navegador.newPage({ viewport: { width: 960, height: 540 } });
  p.on('console', (m) => m.type() === 'error' && erros.push(`${nome}: ${m.text()}`));
  p.on('pageerror', (e) => erros.push(`${nome}: ${e.message}`));
  await p.goto(base + caminho);
  await p.waitForTimeout(esperaMs);
  if (acao) await acao(p);
  await p.screenshot({ path: `${pasta}/${nome}.png` });
  await p.close();
}
await tela('', 'titulo');
await tela('?cena=Mapa', 'mapa');
for (const f of [1, 2, 3, 4]) {
  await tela(`?fase=${f}`, `fase${f}`, f === 1 ? 2800 : 1500, async (p) => {
    // avança os diálogos iniciais com espaço
    for (let i = 0; i < 8; i++) {
      await p.keyboard.press('Space');
      await p.waitForTimeout(250);
    }
    await p.waitForTimeout(500);
  });
}
console.log(erros.length ? erros.join('\n') : 'sem erros no console');
await navegador.close();
