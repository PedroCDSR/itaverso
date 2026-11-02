// Robô que joga o jogo inteiro (Playwright + Chromium), para conferir que as fases continuam possíveis e medir o tempo.
// Uso: com o `npm run dev` rodando, `node ferramentas/teste/jogar.mjs [url] [pasta-capturas]`.
// Variáveis: LIMITE_S (tempo máximo, padrão 420), ESTILO=lento (reage mais devagar e não usa maçã na Fase 1),
// TELA=844x390 (tamanho da janela; 844x390 = iPhone deitado, 915x412 = Android deitado).
//
// Diferente do robo.mjs da Etapa 10, este pilota a INSTÂNCIA de Entrada da cena ativa (troca o método atualizar
// do objeto), o que funciona mesmo depois de recarregamentos do Vite. A cada quadro ele lê o mapa e decide:
// andar para a direita, pular parede/buraco/capivara, jogar maçã, e no chefe ficar embaixo do Jafar cansado.
// Não vai para o build e não é dependência do projeto (o Playwright já vem no ambiente de teste).
import { createRequire } from 'node:module';
import fs from 'node:fs';
const { chromium } = createRequire(import.meta.url)('playwright');

const URL = process.argv[2] || 'http://localhost:5173/';
const PASTA = process.argv[3] || 'capturas';
const LIMITE_S = Number(process.env.LIMITE_S || 420);
const LENTO = process.env.ESTILO === 'lento';
fs.mkdirSync(PASTA, { recursive: true });

const navegador = await chromium.launch();
const [LARG, ALT] = (process.env.TELA || '844x390').split('x').map(Number);
const pagina = await navegador.newPage({ viewport: { width: LARG, height: ALT } });
const erros = [];
pagina.on('console', (m) => m.type() === 'error' && erros.push(m.text()));
pagina.on('pageerror', (e) => erros.push(String(e)));
await pagina.goto(URL);
await pagina.waitForFunction(() => window.jogo && window.jogo.isBooted, null, { timeout: 20000 });

await pagina.evaluate((lento) => {
  const R = (window.robo = { danos: 0, voltas: 0, pularAte: 0, ultimoX: 0, ultimoProgresso: 0, antes: {}, eventos: [] });
  const solido = (cena, x, y) => {
    const t = cena.camada?.getTileAtWorldXY?.(x, y);
    return !!(t && t.index > 0);
  };
  function decidir(cena, e) {
    const q = { direita: false, esquerda: false, pular: false, maca: false, segurando: false };
    const agora = cena.time.now;
    const j = cena.jogador;
    if (cena.scene.key === 'Tapete') {
      // desvia do que estiver à frente na mesma altura; passa por cima de postes e fios
      const tx = cena.tapete.x;
      let alvo = 120;
      for (const o of [...(cena.passaros || []), ...(cena.pipas || [])]) {
        if (o.x > tx - 20 && o.x - tx < 150 && Math.abs(o.y - cena.yTapete) < 46) alvo = o.y > 120 ? o.y - 70 : o.y + 70;
      }
      for (const p of cena.postes || []) if (p.x > tx - 40 && p.x - tx < 170) alvo = Math.min(alvo, p.topo - 34);
      for (const f of cena.fios || []) if (f.x2 > tx - 40 && f.x1 - tx < 170) alvo = Math.min(alvo, f.y - 34);
      q.segurando = cena.yTapete > alvo;
      return q;
    }
    if (!j?.body) return q;
    const noChao = j.body.blocked.down || j.body.touching.down;
    if (cena.scene.key === 'Chefe') {
      const jf = cena.jafar;
      const alvoX = jf.vulneravel ? jf.x + (j.x < jf.x ? -70 : 70) : jf.x + 110 * Math.sign(240 - jf.x || 1);
      if (Math.abs(alvoX - j.x) > 12) (alvoX > j.x ? (q.direita = true) : (q.esquerda = true));
      if (jf.vulneravel && Math.abs(alvoX - j.x) < 40) {
        // vira para o Jafar e joga
        if ((jf.x > j.x) !== j.olhandoDireita) jf.x > j.x ? (q.direita = true) : (q.esquerda = true);
        q.maca = Math.floor(agora / (lento ? 800 : 250)) % 2 === 0;
      }
      // desvia dos projéteis próximos pulando (o lento não desvia)
      if (!lento) for (const p of cena.projeteis?.getChildren?.() || []) {
        if (p.active && Math.abs(p.x - j.x) < 50 && p.y > j.y - 90 && p.y < j.y && noChao) R.pularAte = agora + 300;
      }
      q.pular = agora < R.pularAte;
      return q;
    }
    // preso há muito tempo (muro alto): volta um pouco e vem correndo de novo (pega o toldo no caminho)
    if (agora < (R.recuarAte || 0)) {
      q.esquerda = true;
      return q;
    }
    if (R.travadoDesde && agora - R.travadoDesde > 2500) {
      R.recuarAte = agora + 1100;
      R.subir = j.x; // ao voltar, procura um toldo ou plataforma para subir antes do muro
      R.travadoDesde = 0;
      R.ultimoX = 0;
      return q;
    }
    q.direita = true;
    const pe = j.y;
    const frente = j.body.right + 4;
    const parede = solido(cena, frente + 6, pe - 10) || solido(cena, frente + 6, pe - 40) || j.body.blocked.right;
    let buraco = false;
    for (let dx = 4; dx <= 36; dx += 8) if (!solido(cena, frente + dx, pe + 8)) buraco = true;
    let inimigo = null;
    for (const c of cena.capivaras?.getChildren?.() || []) {
      if (c.perigosa && c.x > j.x - 4 && c.x - j.x < 130 && Math.abs(c.y - j.y) < 30) inimigo = c;
    }
    if (inimigo && !lento && cena.registry.get('macas') > 0 && Math.floor(agora / 300) % 2 === 0) q.maca = true;
    else if (inimigo && inimigo.x - j.x < 60 && noChao) R.pularAte = agora + 260;
    // modo "subir": pula para a plataforma ou toldo que estiver logo à frente e acima
    if (R.subir) {
      if (j.x > R.subir + 40) R.subir = 0;
      const acima = [48, 56, 64].some((h) => solido(cena, frente + 20, pe - h) && !solido(cena, frente + 20, pe - h - 16));
      if (noChao && acima && j.x > R.subir - 140) R.pularAte = agora + 400;
    }
    // um pouco de acaso no tempo do pulo, como uma pessoa (e para o robô não repetir o mesmo erro para sempre)
    if (noChao && (parede || buraco)) R.pularAte = agora + (lento ? 300 : 380) + Math.random() * 120 - 60;
    if (j.x > R.ultimoX + 4) {
      R.ultimoX = j.x;
      R.ultimoProgresso = agora;
      R.travadoDesde = 0;
    } else if (agora - R.ultimoProgresso > 900 && noChao) {
      R.pularAte = agora + 420;
      R.ultimoProgresso = agora;
      R.travadoDesde = R.travadoDesde || agora;
    }
    q.pular = agora < R.pularAte;
    return q;
  }
  // a cada 100 ms, liga o piloto na Entrada da cena ativa (se ainda não tiver)
  setInterval(() => {
    for (const cena of window.jogo.scene.getScenes(true)) {
      const e = cena.entrada;
      if (!e || e.__robo) continue;
      e.__robo = true;
      const original = e.atualizar.bind(e);
      e.atualizar = function () {
        original();
        const q = decidir(cena, e);
        const a = R.antes;
        this.direita = this.direita || q.direita;
        this.esquerda = q.esquerda;
        this.pular = this.pular || q.pular;
        this.maca = this.maca || q.maca;
        this.segurando = this.segurando || q.segurando;
        this.pularApertou = this.pularApertou || (q.pular && !a.pular);
        this.macaApertou = this.macaApertou || (q.maca && !a.maca);
        R.antes = q;
      };
      if (cena.jogador) {
        const levar = cena.jogador.levarDano.bind(cena.jogador);
        cena.jogador.levarDano = (...args) => {
          const v0 = cena.jogador.vida;
          const v = levar(...args);
          if (v < v0) R.danos++;
          if (v === 0) R.voltas++;
          return v;
        };
      }
    }
  }, 100);
}, LENTO);

const inicio = Date.now();
const linhaDoTempo = [];
let ultima = '';
let n = 0;
while ((Date.now() - inicio) / 1000 < LIMITE_S) {
  const info = await pagina.evaluate(() => {
    const cenas = window.jogo.scene.getScenes(true);
    const c = cenas.find((s) => s.jogador);
    return {
      ativas: cenas.map((s) => s.scene.key).filter((k) => k !== 'HUD').join('+'),
      pos: c ? `${c.scene.key} x=${Math.round(c.jogador.x)} y=${Math.round(c.jogador.y)}` : '',
      danos: window.robo.danos,
      voltas: window.robo.voltas,
    };
  });
  if (info.ativas !== ultima) {
    const t = (Date.now() - inicio) / 1000;
    linhaDoTempo.push([t, info.ativas, info.danos, info.voltas]);
    console.log(`${t.toFixed(1)} s  ${info.ativas}  (danos ${info.danos}, voltas ao checkpoint ${info.voltas})`);
    ultima = info.ativas;
    await pagina.waitForTimeout(700);
    await pagina.screenshot({ path: `${PASTA}/${String(++n).padStart(2, '0')}-${info.ativas}.png` });
  } else if (process.env.POS) console.log('   ', info.pos);
  if (/Final/.test(info.ativas)) break;
  // títulos, intro, diálogos e telas de toque: Enter avança
  await pagina.keyboard.press('Enter');
  await pagina.waitForTimeout(500);
}
const total = (Date.now() - inicio) / 1000;
console.log(`TOTAL ${total.toFixed(1)} s · chegou ao Final: ${/Final/.test(ultima) ? 'sim' : 'NÃO'}`);
console.log(`ERROS ${erros.length}`);
for (const e of erros.slice(0, 20)) console.log('  ' + e);
fs.writeFileSync(`${PASTA}/linha-do-tempo.json`, JSON.stringify({ total, linhaDoTempo, erros }, null, 2));
await navegador.close();
