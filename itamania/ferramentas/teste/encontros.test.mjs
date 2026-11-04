import { test, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { estado } from '../../src/estado.js';
import { MICROMUNDOS, REGIAO_PRACA } from '../../src/data/micromundos.js';
import { iniciarMissao, concluirMissao, recuperarMissaoInterrompida, SistemaEncontros } from '../../src/systems/encontros.js';

globalThis.localStorage = { setItem() {} };
const especial = REGIAO_PRACA.encontros[0];
beforeEach(() => { estado.itacoins = 7; estado.encontros = { concluidas: {}, visitas: {}, pendente: null }; estado.retornoExploracao = null; });
test('14 regiões usam nomes e ordem do mapa, sem anunciar mapas inexistentes', () => {
  assert.equal(MICROMUNDOS.length, 14);
  assert.equal(MICROMUNDOS[3].nome, 'Praça Theodomiro Santiago');
  assert.equal(MICROMUNDOS.filter((r) => r.exploracao).length, 1);
});
test('vitória guarda posição exata e premia uma única vez', () => {
  const s = iniciarMissao(REGIAO_PRACA, especial, { x: 848, y: 596 }, 'cima');
  assert.equal(iniciarMissao(REGIAO_PRACA, especial, { x: 1, y: 1 }, 'baixo'), null);
  assert.equal(concluirMissao('token-errado', true, 3), null);
  assert(estado.encontros.pendente);
  const r = concluirMissao(s.token, true, 3);
  assert.equal(r.x, 848); assert.equal(r.y, 596); assert.equal(r.premio, 8);
  assert.equal(estado.itacoins, 15);
  assert.equal(concluirMissao(s.token, true, 3), null);
  assert.equal(estado.itacoins, 15);
});
test('repetição rende menos, derrota preserva saldo e retorna ao ponto seguro', () => {
  let s = iniciarMissao(REGIAO_PRACA, especial, { x: 848, y: 596 }, 'cima');
  concluirMissao(s.token, true, 20);
  s = iniciarMissao(REGIAO_PRACA, especial, { x: 848, y: 596 }, 'cima');
  assert.equal(concluirMissao(s.token, true, 20).premio, 4);
  const saldo = estado.itacoins;
  s = iniciarMissao(REGIAO_PRACA, especial, { x: 848, y: 596 }, 'cima');
  const r = concluirMissao(s.token, false, 20);
  assert.equal(estado.itacoins, saldo); assert.equal(r.premio, 0);
  assert.equal(r.x, REGIAO_PRACA.pontoSeguro.x);
});
test('recarga interrompe a missão sem apagar descobertas nem conceder recompensa', () => {
  estado.moedasPraca = [1, 4];
  iniciarMissao(REGIAO_PRACA, especial, { x: 850, y: 590 }, 'esquerda');
  assert.equal(recuperarMissaoInterrompida(), true);
  assert.equal(estado.itacoins, 7); assert.deepEqual(estado.moedasPraca, [1, 4]);
  assert.equal(estado.retornoExploracao.x, 850);
  assert.equal(estado.encontros.pendente, null);
  assert.equal(recuperarMissaoInterrompida(), false);
});
test('zonas seguras, diálogo, distância e intervalo protegem contra encontros excessivos', () => {
  const s = new SistemaEncontros(REGIAO_PRACA, 0, { x: 600, y: 598 }, () => 0);
  for (let x = 600; x < 1000; x += 10) assert.equal(s.atualizar({ x, y: 598 }, 40000, false), null);
  for (let x = 960; x > 880; x -= 10) assert.equal(s.atualizar({ x, y: 620 }, 40000, true), null);
  const novo = new SistemaEncontros(REGIAO_PRACA, 0, { x: 880, y: 620 }, () => 0);
  for (let i = 0; i < 40; i++) assert.equal(novo.atualizar({ x: 880 + (i % 9) * 10, y: 620 }, 20000, false), null);
  assert.equal(novo.atualizar({ x: 910, y: 620 }, 40000, false)?.tipo, 'comum');
  assert.equal(novo.atualizar({ x: 911, y: 620 }, 40001, false), null);
});
test('encontro de história pode ser tentado de novo após derrota e não se repete após vitória', () => {
  const historia = { ...especial, id: 'historia-praca', tipo: 'historia' };
  let s = iniciarMissao(REGIAO_PRACA, historia, { x: 848, y: 596 }, 'cima');
  concluirMissao(s.token, false);
  s = iniciarMissao(REGIAO_PRACA, historia, { x: 848, y: 596 }, 'cima');
  assert(s);
  concluirMissao(s.token, true);
  assert.equal(iniciarMissao(REGIAO_PRACA, historia, { x: 848, y: 596 }, 'cima'), null);
});
