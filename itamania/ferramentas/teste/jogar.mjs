// Robô que joga as fases (Playwright + Chromium) para conferir que dá para terminar e medir o tempo.
// Uso, com o `npm run dev` rodando: node ferramentas/teste/jogar.mjs [url] [pasta-capturas]
// Variáveis: FASES=1,2,3,4 (quais jogar, em sequência, numa partida só), HEROI=helena, TELA=844x390, LIMITE_S=240.
//
// O robô troca o método `atualizar` da Entrada da cena Fase: anda para a direita, pula em paredes, buracos e
// inimigos, joga pão de queijo, avança os diálogos e recua quando empaca.
import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)('playwright');

const base = process.argv[2] || 'http://localhost:5180/';
const pasta = process.argv[3] || null;
const fases = (process.env.FASES || '1,2,3,4').split(',').map(Number);
const heroi = process.env.HEROI || 'geraldo';
const [w, h] = (process.env.TELA || '960x540').split('x').map(Number);
const limite = Number(process.env.LIMITE_S || 240) * 1000;

const navegador = await chromium.launch();
const pagina = await navegador.newPage({ viewport: { width: w, height: h } });
const erros = [];
pagina.on('console', (m) => m.type() === 'error' && erros.push(m.text()));
pagina.on('pageerror', (e) => erros.push(e.message));
await pagina.goto(`${base}?fase=${fases[0]}&heroi=${heroi}`);
await pagina.evaluate(() => localStorage.clear());
await pagina.goto(`${base}?fase=${fases[0]}&heroi=${heroi}`);

// instala o robô dentro da página (roda a cada quadro, dentro do update da cena)
await pagina.evaluate(() => {
  const r = { segurarPuloAte: 0, ultimoX: 0, paradoDesde: 0, recuarAte: 0, log: [] };
  window.robo = r;
  setInterval(() => {
    const jogo = window.jogo;
    const sc = jogo?.scene.getScene('Fase');
    if (!sc || !sc.sys.isActive() || !sc.entrada || sc.entrada.robo) return;
    sc.entrada.robo = true;
    sc.entrada.atualizar = function () {
      const agora = sc.time.now;
      const j = sc.jogador;
      const e = this;
      const antes = { pular: e.pular, maca: e.maca };
      e.esquerda = e.direita = e.pular = e.maca = false;
      if (!j || !j.body) return;
      const corpo = j.body;
      const T = 16;
      const tile = (x, y) => sc.camada.getTileAtWorldXY(x, y);
      const chaoEmbaixo = (x) => {
        for (let y = j.y + 2; y < sc.mapa.alturaPx; y += 16) if (tile(x, y)) return true;
        return false;
      };
      // empacou? recua um pouco e tenta de novo
      if (Math.abs(j.x - r.ultimoX) > 3) {
        r.ultimoX = j.x;
        r.paradoDesde = agora;
      } else if (agora - r.paradoDesde > 1500 && !sc.ocupado && sc.jogando) {
        r.recuarAte = agora + 350;
        r.paradoDesde = agora;
        r.segurarPuloAte = agora + 700;
      }
      if (agora < r.recuarAte) e.esquerda = true;
      else e.direita = true;
      const noChao = corpo.blocked.down;
      const frente = j.x + 22;
      const parede = corpo.blocked.right || tile(frente, j.y - 8) || tile(frente, j.y - 30);
      const buraco = noChao && !chaoEmbaixo(j.x + 26);
      let inimigoPerto = null;
      for (const i of sc.inimigos.getChildren()) {
        if (i.active && i.perigoso && i.x > j.x - 6 && i.x - j.x < 70 && Math.abs(i.y - j.y) < 40) inimigoPerto = i;
      }
      if (noChao && (parede || buraco || (inimigoPerto && inimigoPerto.x - j.x < 46))) r.segurarPuloAte = agora + 420;
      e.pular = agora < r.segurarPuloAte;
      // pão de queijo nos inimigos à frente
      if (inimigoPerto && window.estadoJogo?.temPao !== false) e.maca = !antes.maca;
      e.segurando = e.pular;
      e.pularApertou = e.pular && !antes.pular;
      e.macaApertou = e.maca && !antes.maca;
    };
  }, 100);
});

const t0 = Date.now();
let faseAtual = fases[0];
const tempos = {};
let inicioFase = Date.now();
while (Date.now() - t0 < limite) {
  await pagina.waitForTimeout(300);
  // diálogos: avança
  const temDialogo = await pagina.evaluate(() => !!document.querySelector('.dialogo.ativa'));
  if (temDialogo) await pagina.keyboard.press('Enter');
  const cena = await pagina.evaluate(() => {
    const s = window.jogo?.scene.getScenes(true).map((x) => x.sys.settings.key) || [];
    const f = window.jogo?.scene.getScene('Fase');
    return { ativas: s, fase: f?.numero, x: f?.jogador?.x | 0, moedas: window.jogo?.registry.get('itacoins') };
  });
  if (cena.ativas.includes('Cartao')) {
    tempos[faseAtual] = ((Date.now() - inicioFase) / 1000).toFixed(1);
    if (pasta) await pagina.screenshot({ path: `${pasta}/robo-cartao${faseAtual}.png` });
    const i = fases.indexOf(faseAtual);
    if (i === fases.length - 1) break;
    faseAtual = fases[i + 1];
    await pagina.waitForTimeout(2800);
    // CONTINUAR do cartão e entrada pelo mapa (tecla Enter no mapa entra na fase liberada mais alta até a 4)
    await pagina.mouse.click(w / 2, h * (240 / 270));
    await pagina.waitForTimeout(900);
    await pagina.keyboard.press('Enter');
    inicioFase = Date.now();
    await pagina.waitForTimeout(1200);
  }
}
const final = await pagina.evaluate(() => ({ estado: JSON.parse(localStorage.getItem('itamania-progresso-v1') || '{}') }));
console.log('tempos por fase (s):', JSON.stringify(tempos));
console.log('progresso salvo:', JSON.stringify(final.estado));
console.log(erros.length ? 'ERROS:\n' + erros.join('\n') : 'sem erros no console');
if (pasta) await pagina.screenshot({ path: `${pasta}/robo-fim.png` });
await navegador.close();
