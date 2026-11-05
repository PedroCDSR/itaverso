// Validação no Chromium com o motor real. Playwright é ferramenta externa, não dependência do jogo.
import { createRequire } from 'node:module';
import { createServer } from 'vite';
import fs from 'node:fs';
import assert from 'node:assert/strict';
const { chromium } = createRequire(import.meta.url)('playwright');
const pasta = process.argv[2] || '/tmp/itamania-urbana-capturas';
fs.mkdirSync(pasta, { recursive: true });
const server = await createServer({ server: { host: '127.0.0.1', port: 5187, strictPort: true } });
await server.listen();
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined,
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-angle=swiftshader'] });
const errors = [], failed = [];
try {
 const page = await browser.newPage({ viewport: { width: 960, height: 540 } });
 page.on('pageerror', e => errors.push(e.message));
 page.on('response', r => { if(r.status() >= 400) failed.push(r.url()); });
 await page.addInitScript(() => { localStorage.setItem('itamania-progresso-v1', JSON.stringify({ heroi: 'geraldo', viuPraca: true, itacoins: 9, moedasPraca: [0] })); });
 await page.goto('http://127.0.0.1:5187/?missao=urbana');
 await page.waitForFunction(() => window.missao?.jogador?.active);
 await page.waitForTimeout(500);
 await page.screenshot({path: `${pasta}/01-inicio.png`});
 await page.evaluate(() => {
   jogo.loop.stop();
   const s = missao;
   s.robo = { modo: 'baixo', saltoAte: 0, antes: false };
   s.entrada.atualizar = function() {
     const j = s.jogador, r = s.robo, chao = j.body.blocked.down || j.body.touching.down;
     this.esquerda = false; this.direita = r.modo !== 'parado';
     this.maca = this.macaApertou = false;
     const apoio = s.def.apoios.some(p => p.altura < 40 && p.x > j.body.right && p.x - j.body.right < 38);
     const pombo = s.inimigos.getChildren().some(i => !i.saiu && i.x > j.x && i.x-j.x < 66);
     if (chao && (apoio || pombo) && r.modo !== 'parado') r.saltoAte = s.time.now + 370;
     this.pular = s.time.now < r.saltoAte;
     this.pularApertou = this.pular && !r.antes; r.antes = this.pular;
   };
 });
 async function avancar(alvo) {
   const r = await page.evaluate(alvo => {
     let frames=0;
     while(missao.jogador.x < alvo && !missao.terminou && frames++ < 6000) jogo.headlessStep(missao.time.now+1000/60,1000/60);
     jogo.step(missao.time.now+1000/60,1000/60);
     return {x:missao.jogador.x,y:missao.jogador.y,vidas:missao.vidas,pontos:missao.placar.pontos,terminou:missao.terminou,frames,
       resultado:JSON.parse(localStorage.getItem('itamania-progresso-v1')).retornoExploracao};
   },alvo);
   assert(r.x >= alvo || r.resultado?.venceu, JSON.stringify(r));
   console.log('Percurso',JSON.stringify(r));
   return r;
 }
 for(const [x,nome] of [[1100,'02-fonte-concha'],[1600,'03-vadinho'],[2550,'04-subida'],[4400,'05-casaroes'],[5420,'06-igreja']]) {
   await avancar(x);
   await page.evaluate(() => {
     missao.robo.modo='parado';
     for(let i=0;i<60;i++) jogo.step(missao.time.now+1000/60,1000/60);
     missao.robo.modo='baixo';
   });
   await page.screenshot({path:`${pasta}/${nome}.png`});
 }
 const final = await avancar(5540);
 assert.equal(final.resultado?.venceu,true); assert(final.vidas>0); assert.equal(final.resultado.x,848);
 await page.screenshot({path:`${pasta}/07-resultado.png`});
 // Reabrir uma missão real permite avaliar o desvio independentemente da coleta da rota baixa.
 await page.evaluate(async () => {
   const {estado}=await import('/src/estado.js');
   const {iniciarMissao}=await import('/src/systems/encontros.js');
   const {REGIAO_PRACA}=await import('/src/data/micromundos.js');
   const sessao=iniciarMissao(REGIAO_PRACA,REGIAO_PRACA.encontros[0],{x:848,y:596},'cima');
   jogo.scene.start('Missao',{sessao});
   jogo.step(performance.now(),1000/60);
 });
 await page.evaluate(() => {
   const s=missao;
   s.robo={etapa:0,antes:false,segurar:0};
   s.jogador.body.reset(2260,605);
   s.entrada.atualizar=function(){
     const j=s.jogador,r=s.robo;
     const alvos=[{x:2330,y:584},{x:2376,y:561},{x:2440,y:536},{x:2560,y:480},{x:2740,y:394},{x:2820,y:394}];
     const alvo=alvos[Math.min(r.etapa,alvos.length-1)];
     const noChao=j.body.blocked.down||j.body.touching.down;
     if(noChao&&Math.abs(j.body.bottom-alvo.y)<9&&Math.abs(j.x-alvo.x)<45&&r.etapa<alvos.length-1)r.etapa++;
     const a=alvos[Math.min(r.etapa,alvos.length-1)];
     this.direita=j.x<a.x-7;this.esquerda=j.x>a.x+7;
     if(noChao&&!s.quicando&&r.etapa<4&&s.time.now>r.segurar+100)r.segurar=s.time.now+350;
     this.pular=s.time.now<r.segurar;this.pularApertou=this.pular&&!r.antes;r.antes=this.pular;
     this.maca=this.macaApertou=false;
   };
   s.quiQues=0;const quicar=s.quicarToldo.bind(s);s.quicarToldo=function(){s.quiQues++;quicar();};
 });
 const desvio=await page.evaluate(()=>{
   for(let i=0;i<1800&&!missao.placar.coletadas.has('estrela-toldos')&&!missao.terminou;i++)jogo.headlessStep(missao.time.now+1000/60,1000/60);
   jogo.step(missao.time.now+1000/60,1000/60);
   return {x:missao.jogador.x,y:missao.jogador.y,etapa:missao.robo.etapa,quiQues:missao.quiQues,estrela:missao.placar.coletadas.has('estrela-toldos'),vidas:missao.vidas};
 });
 await page.screenshot({path:`${pasta}/08-desvio.png`});console.log('Desvio',JSON.stringify(desvio));
 assert(desvio.quiQues>0,JSON.stringify(desvio));assert(desvio.estrela,JSON.stringify(desvio));
 assert.deepEqual(errors,[]);
 // Falhas de assets da praça já existentes são reportadas separadamente, sem ocultar falhas novas.
 assert.equal(failed.filter(u=>u.includes('/missao-urbana/')).length,0);
 console.log(JSON.stringify({errors,failed,capturas:pasta}));
} finally { await browser.close(); await server.close(); }
