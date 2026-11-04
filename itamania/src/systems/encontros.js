import { estado, salvar } from '../estado.js';
import { MISSOES, MICROMUNDOS } from '../data/micromundos.js';

function progresso() {
  estado.encontros ||= { concluidas: {}, visitas: {}, historias: {}, pendente: null };
  estado.encontros.historias ||= {};
  return estado.encontros;
}

export function iniciarMissao(regiao, encontro, retorno, direcao) {
  const p = progresso();
  const missao = MISSOES[encontro.missao];
  if (!missao || !regiao.missoes.includes(missao.id) || p.pendente) return null;
  if (encontro.tipo === 'historia' && p.historias[encontro.id]) return null;
  const sessao = {
    token: globalThis.crypto.randomUUID(), missao: missao.id, regiao: regiao.id,
    retorno: { x: retorno.x, y: retorno.y }, direcao, tipo: encontro.tipo, encontro: encontro.id,
  };
  p.pendente = sessao;
  p.visitas[encontro.id] = (p.visitas[encontro.id] || 0) + 1;
  salvar();
  return sessao;
}

// A sessão é consumida uma única vez. Reabrir uma tela de vitória não duplica o prêmio.
export function concluirMissao(token, venceu, moedas = 0) {
  const p = progresso();
  const sessao = p.pendente;
  if (!sessao || sessao.token !== token) return null;
  const m = MISSOES[sessao.missao];
  const repetida = !!p.concluidas[m.id];
  const premio = venceu ? (repetida ? m.recompensaRepetida : m.recompensa) + (repetida ? Math.min(3, moedas) : moedas) : 0;
  if (venceu) p.concluidas[m.id] = (p.concluidas[m.id] || 0) + 1;
  if (venceu && sessao.tipo === 'historia') p.historias[sessao.encontro] = true;
  estado.itacoins += premio;
  const regiao = MICROMUNDOS.find((r) => r.id === sessao.regiao);
  const pos = venceu ? sessao.retorno : regiao.pontoSeguro || sessao.retorno;
  estado.retornoExploracao = { ...pos, direcao: sessao.direcao, venceu, premio, interrompida: false };
  p.pendente = null;
  salvar();
  return estado.retornoExploracao;
}

export function recuperarMissaoInterrompida() {
  const p = progresso();
  if (!p.pendente) return false;
  estado.retornoExploracao = { ...p.pendente.retorno, direcao: p.pendente.direcao, interrompida: true, premio: 0 };
  p.pendente = null;
  salvar();
  return true;
}

// Sorteio somente após distância percorrida, em zonas explícitas, longe de conversas e do retorno de uma missão.
export class SistemaEncontros {
  constructor(regiao, agora, posicao, sorteio = Math.random) {
    this.regiao = regiao;
    this.ultima = { x: posicao.x, y: posicao.y };
    this.distancia = 0;
    this.ultimoSorteio = 0;
    this.liberarEm = agora + 30000;
    this.sorteio = sorteio;
  }
  atualizar(pos, agora, ocupado) {
    const andou = Math.hypot(pos.x - this.ultima.x, pos.y - this.ultima.y);
    this.ultima = { x: pos.x, y: pos.y };
    if (ocupado || andou > 20) return null;
    this.distancia += andou;
    if (agora < this.liberarEm || this.distancia < 160 || this.distancia - this.ultimoSorteio < 48) return null;
    const zona = this.regiao.encontros.find((e) => e.tipo === 'comum' && pos.x >= e.x && pos.x <= e.x + e.largura && pos.y >= e.y && pos.y <= e.y + e.altura);
    if (!zona) return null;
    this.ultimoSorteio = this.distancia;
    return this.sorteio() < 0.25 ? zona : null;
  }
}
