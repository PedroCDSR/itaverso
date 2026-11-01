// Gera public/og-image.png (1200x630), os ícones (favicon, iPhone, manifest) a partir da arte do jogo.
// Arte 100% original: céu e morros do jogo, o Aladdin provisório (src/art/jogador.js) e as cores da escola.
// Rodar na raiz do repositório:  node ferramentas/og/gerar.mjs   (precisa do Playwright com Chromium)
import { createRequire } from 'node:module';
// o Playwright não é dependência do projeto: usa o instalado na máquina (require funciona de qualquer pasta)
const { chromium } = createRequire(import.meta.url)('playwright');
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import * as J from '../../src/art/jogador.js';
import * as T from '../../src/art/tiles.js';
import { EVENTO } from '../../src/data/evento.js';

const raiz = resolve('.');
const fonte = (arq) => `data:font/woff2;base64,${readFileSync(`${raiz}/public/assets/fonts/${arq}`).toString('base64')}`;

const html = `<!doctype html><html><head><style>
@font-face { font-family: 'PS2P'; src: url(${fonte('PressStart2P.woff2')}); }
@font-face { font-family: 'PH'; src: url(${fonte('PatrickHand.woff2')}); }
body { margin: 0; background: transparent; }
canvas { display: block; }
</style></head><body>
<canvas id="og" width="1200" height="630"></canvas>
<canvas id="icone" width="512" height="512"></canvas>
<script>
const J = ${JSON.stringify({ PALETA: J.PALETA, Q: J.QUADROS.parado1 })};
const T = ${JSON.stringify({ PALETA: T.PALETA, topo: T.TILES.chaoTopo, chao: T.TILES.chao })};
const EV = ${JSON.stringify(EVENTO)};
function matriz(ctx, linhas, paleta, x0, y0, esc) {
  linhas.forEach((l, y) => { for (let x = 0; x < l.length; x++) { const c = l[x]; if (c === '.') continue;
    ctx.fillStyle = paleta[c]; ctx.fillRect(x0 + x * esc, y0 + y * esc, esc, esc); } });
}
function quadrados(ctx, cx, cy, r, cores) {
  // quadrados arredondados concêntricos (motivo do logo da escola)
  cores.forEach((cor, i) => { const s = r * (1 - i / cores.length); ctx.fillStyle = cor; ctx.beginPath();
    ctx.roundRect(cx - s, cy - s, s * 2, s * 2, s * 0.25); ctx.fill(); });
}
function texto(ctx, t, x, y, fonte, tam, cor, contorno, sombra) {
  ctx.font = tam + 'px ' + fonte; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  if (sombra) { ctx.fillStyle = sombra; ctx.fillText(t, x + tam / 8, y + tam / 8); }
  if (contorno) { ctx.lineJoin = 'round'; ctx.lineWidth = tam / 6; ctx.strokeStyle = contorno; ctx.strokeText(t, x, y); }
  ctx.fillStyle = cor; ctx.fillText(t, x, y);
}
async function og() {
  const c = document.getElementById('og'), ctx = c.getContext('2d'); ctx.imageSmoothingEnabled = false;
  const W = 1200, H = 630;
  const g = ctx.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0, '#9E9EFF'); g.addColorStop(0.55, '#E9A6D8'); g.addColorStop(1, '#F7C99A');
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  const morro = (cor, base, amp, f) => { ctx.fillStyle = cor; ctx.beginPath(); ctx.moveTo(0, H);
    for (let x = 0; x <= W; x += 4) ctx.lineTo(x, base - amp * (Math.sin(x / W * Math.PI * 2 * f[0] + f[1]) + 0.4 * Math.sin(x / W * Math.PI * 2 * f[2])));
    ctx.lineTo(W, H); ctx.fill(); };
  morro('#B98BC9', 390, 40, [2, 0, 5]); morro('#8F6FB3', 450, 30, [3, 2, 7]);
  // chão de tiles (escala 4)
  for (let x = 0; x < W; x += 64) { matriz(ctx, T.topo, T.PALETA, x, H - 128, 4); matriz(ctx, T.chao, T.PALETA, x, H - 64, 4); }
  // Aladdin provisório do jogo (escala 8)
  matriz(ctx, J.Q, J.PALETA, 830, H - 128 - 48 * 8, 8);
  quadrados(ctx, 80, 80, 44, ['#FFB0FA', '#F9FCBB', '#9E9EFF', '#FFB0FA']);
  texto(ctx, EV.escola, 520, 80, 'PH', 52, '#FFFFFF', null, '#6D6BD9');
  texto(ctx, 'ALADDIN', 480, 210, 'PS2P', 96, '#FFB0FA', '#6D6BD9', '#3A2F7A');
  texto(ctx, 'o jogo do espetáculo', 470, 310, 'PH', 56, '#F9FCBB', null, '#6D6BD9');
  // faixa com data e local
  ctx.fillStyle = '#6D6BD9'; ctx.beginPath(); ctx.roundRect(90, 370, 760, 80, 14); ctx.fill();
  texto(ctx, '20/11 · Teatro do Colégio G9 · Itajubá', 470, 408, 'PH', 50, '#FFFFFF');
}
async function icone() {
  const c = document.getElementById('icone'), ctx = c.getContext('2d'); ctx.imageSmoothingEnabled = false;
  ctx.fillStyle = '#9E9EFF'; ctx.fillRect(0, 0, 512, 512);
  quadrados(ctx, 256, 256, 210, ['#FFB0FA', '#F9FCBB', '#9E9EFF']);
  // rosto do Aladdin provisório (parte de cima do quadro 32x48), bem grande
  matriz(ctx, J.Q.slice(2, 26), J.PALETA, 256 - 16 * 13, 70, 13);
}
document.fonts.load('20px PS2P').then(() => document.fonts.load('20px PH')).then(async () => { await og(); await icone(); window.pronto = true; });
</script></body></html>`;

const navegador = await chromium.launch();
const pagina = await navegador.newPage();
await pagina.setContent(html);
await pagina.waitForFunction('window.pronto === true');
await pagina.locator('#og').screenshot({ path: `${raiz}/public/og-image.png` });
// ícones: redimensiona o canvas de 512 no próprio navegador
for (const [tam, arq] of [[512, 'icone-512.png'], [192, 'icone-192.png'], [180, 'apple-touch-icon.png'], [32, 'favicon.png']]) {
  const dados = await pagina.evaluate((t) => {
    const c = document.createElement('canvas'); c.width = c.height = t;
    const ctx = c.getContext('2d'); ctx.imageSmoothingEnabled = t < 64 ? true : false;
    ctx.drawImage(document.getElementById('icone'), 0, 0, t, t);
    return c.toDataURL('image/png').split(',')[1];
  }, tam);
  writeFileSync(`${raiz}/public/${arq}`, Buffer.from(dados, 'base64'));
}
await navegador.close();
console.log('ok: public/og-image.png e ícones');
