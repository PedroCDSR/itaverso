import { test } from 'node:test';
import assert from 'node:assert/strict';
import { PERCURSO_URBANO as MAPA, APOIOS_URBANOS, FICHAS_URBANAS, chaoUrbano, tocaCalcada } from '../../src/data/missaoUrbana.js';
import { MISSAO_URBANA as F, JOGADOR } from '../../src/config.js';
import { PontosMissao } from '../../src/systems/pontosMissao.js';

test('coleta fora de ordem e sem relógio completa sequência, checkpoint não duplica ficha ou bônus', () => {
  const s = new PontosMissao();
  for (const i of [3, 0, 4, 2]) assert.equal(s.coletar(`bancos-${i}`).bonus, 0);
  assert.equal(s.coletar('bancos-1').bonus, 50);
  assert.equal(s.pontos, 100);
  for (let i = 0; i < 5; i++) assert.equal(s.coletar(`bancos-${i}`), null);
  assert.equal(s.coletar('inexistente'), null);
  assert.equal(s.pontos, 100);
});
test('todos os coletáveis somam 850, outra tentativa tem pontuação independente', () => {
  const s = new PontosMissao();
  for (const f of FICHAS_URBANAS) s.coletar(f.id);
  assert.equal(s.pontos, 850);
  assert.equal(s.completas.size, 8);
  assert.equal(new Set(FICHAS_URBANAS.map((f) => f.id)).size, FICHAS_URBANAS.length);
  assert.equal(new PontosMissao().pontos, 0);
});
test('praça plana, subida suave e chegada plana não contêm abismos', () => {
  assert.equal(chaoUrbano(80), chaoUrbano(1728));
  assert.equal(chaoUrbano(4960), chaoUrbano(MAPA.fim));
  for (let x = 1; x <= MAPA.largura; x++) {
    assert(chaoUrbano(x) <= chaoUrbano(x - 1));
    assert(chaoUrbano(x - 1) - chaoUrbano(x) < 0.1);
  }
});
test('calçada sustenta a caminhada nos dois sentidos em 30, 60 e 120 passos/s', () => {
  for (const fps of [30, 60, 120]) for (const direcao of [1, -1]) {
    const dt = 1 / fps;
    let x = direcao === 1 ? 80 : 5520;
    let fundo = chaoUrbano(x), vy = 0, pousos = 0;
    for (let i = 0; i < fps * 34; i++) {
      const antes = x, anterior = fundo;
      x = Math.max(0, Math.min(MAPA.largura - 1, x + direcao * F.velocidade * dt));
      vy += JOGADOR.gravidade * dt; fundo += vy * dt;
      if (tocaCalcada({ x, anteriorX: antes, fundo, fundoAnterior: anterior, velocidadeY: vy, alturaCorpo: 22 })) {
        fundo = chaoUrbano(x); vy = 0; pousos++;
      }
      assert(Math.abs(fundo - chaoUrbano(x)) < 2, `queda inesperada em ${x}`);
    }
    assert(pousos > fps * 20);
  }
});
test('pulo não cola no chão e queda abaixo da calçada não teleporta para cima', () => {
  assert.equal(tocaCalcada({ x: 2000, anteriorX: 2000, fundo: 630, fundoAnterior: 630, velocidadeY: -100, alturaCorpo: 22 }), false);
  const y = chaoUrbano(2000);
  assert.equal(tocaCalcada({ x: 2000, anteriorX: 2000, fundo: y + 130, fundoAnterior: y + 125, velocidadeY: 100, alturaCorpo: 22 }), false);
});

function alcanca(origem, destino, impulso) {
  // Integra o salto com gravidade do jogo e testa uma aterrissagem descendo no apoio.
  for (const velocidade of [40, 80, 120, F.velocidade]) {
    let x = origem.x + origem.largura - 12, y = origem.y, vy = -impulso;
    for (let i = 0; i < 240; i++) {
      const antes = y; vy += JOGADOR.gravidade / 120; y += vy / 120; x += velocidade / 120;
      if (vy >= 0 && antes <= destino.y && y >= destino.y && x + 12 >= destino.x && x - 12 <= destino.x + destino.largura) return true;
    }
  }
  return false;
}
test('todos os apoios do desvio são alcançáveis e a marquise exige o quique do toldo', () => {
  const ids = ['degrau1', 'degrau2', 'mureta', 'toldo', 'marquise', 'descida'];
  const apoios = ids.map((id) => APOIOS_URBANOS.find((p) => p.id === id));
  for (let i = 1; i < apoios.length; i++) {
    assert(alcanca(apoios[i - 1], apoios[i], i === 4 ? F.puloToldo : F.pulo), `${ids[i - 1]} → ${ids[i]}`);
  }
  assert.equal(alcanca(apoios[3], apoios[4], F.pulo), false);
  for (const p of apoios) assert(chaoUrbano(p.x) > p.y);
});
