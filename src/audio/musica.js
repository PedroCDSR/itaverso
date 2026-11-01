// Tocador de música em código: lê as partituras de musicas.js e agenda as notas no AudioContext.
// Usa o agendamento "com antecedência": a cada 25 ms, marca as notas dos próximos ~150 ms no relógio do áudio.
// Assim o ritmo fica certinho mesmo se o jogo engasgar um quadro.
// Quando o áudio está suspenso (pausa, mudo, antes do 1º toque), o relógio do áudio para e nada é agendado.

import { SOM } from '../config.js';
import { MUSICAS, VINHETAS } from './musicas.js';
import { contextoAudio, saidaAudio, somAtivo, quandoSomLigar } from './som.js';

const ANTECEDENCIA = 0.15; // segundos agendados à frente
const NOTAS = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };

// ---------------------------------------------------------------- partitura → eventos

// 'C5 . E5 - |' → [{ freq, passos }, null, ...] (null = silêncio ou continuação)
function lerVoz(texto) {
  const fichas = texto.split(/[\s|]+/).filter(Boolean);
  const passos = new Array(fichas.length).fill(null);
  let ultima = -1;
  fichas.forEach((f, i) => {
    if (f === '-') {
      if (ultima >= 0) passos[ultima].passos++;
      return;
    }
    if (f === '.') {
      ultima = -1;
      return;
    }
    const m = /^([A-G])(#?)(\d)$/.exec(f);
    if (!m) throw new Error(`Nota inválida na música: ${f}`);
    const midi = 12 * (Number(m[3]) + 1) + NOTAS[m[1]] + (m[2] ? 1 : 0);
    passos[i] = { freq: 440 * 2 ** ((midi - 69) / 12), passos: 1 };
    ultima = i;
  });
  return passos;
}

function lerBateria(texto) {
  return texto.split(/[\s|]+/).filter(Boolean);
}

const cachePartituras = new Map();
function partitura(nome, fonte) {
  if (!cachePartituras.has(nome)) {
    const m = fonte[nome];
    if (!m) return null;
    const vozes = m.vozes.map((v) => ({ ...v, passos: lerVoz(v.notas) }));
    const bateria = m.bateria ? lerBateria(m.bateria) : null;
    const tamanho = Math.max(...vozes.map((v) => v.passos.length), bateria?.length ?? 0);
    cachePartituras.set(nome, { duracaoPasso: 30 / m.bpm, vozes, bateria, tamanho });
  }
  return cachePartituras.get(nome);
}

// ---------------------------------------------------------------- instrumentos

let ruido = null;
function bufferRuido(c) {
  if (!ruido) {
    ruido = c.createBuffer(1, c.sampleRate * 0.3, c.sampleRate);
    const d = ruido.getChannelData(0);
    for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  }
  return ruido;
}

function nota(c, destino, onda, freq, inicio, duracao, volume) {
  const osc = c.createOscillator();
  const g = c.createGain();
  osc.type = onda;
  osc.frequency.value = freq;
  // envelope: ataque rápido, cai um pouco, solta no fim (sem estalos)
  const fim = inicio + Math.max(0.05, duracao * 0.92);
  g.gain.setValueAtTime(0, inicio);
  g.gain.linearRampToValueAtTime(volume, inicio + 0.006);
  g.gain.setTargetAtTime(volume * 0.6, inicio + 0.02, 0.08);
  g.gain.setTargetAtTime(0, fim - 0.03, 0.015);
  osc.connect(g).connect(destino);
  osc.start(inicio);
  osc.stop(fim + 0.05);
}

function tambor(c, destino, tipo, inicio) {
  if (tipo === 'k') {
    // bumbo: seno que desce rápido de tom
    const osc = c.createOscillator();
    const g = c.createGain();
    osc.frequency.setValueAtTime(150, inicio);
    osc.frequency.exponentialRampToValueAtTime(45, inicio + 0.12);
    g.gain.setValueAtTime(0.7, inicio);
    g.gain.exponentialRampToValueAtTime(0.001, inicio + 0.15);
    osc.connect(g).connect(destino);
    osc.start(inicio);
    osc.stop(inicio + 0.16);
    return;
  }
  // caixa e chimbal: ruído filtrado, curtinho
  const src = c.createBufferSource();
  src.buffer = bufferRuido(c);
  const f = c.createBiquadFilter();
  const g = c.createGain();
  const caixa = tipo === 's';
  f.type = caixa ? 'bandpass' : 'highpass';
  f.frequency.value = caixa ? 1800 : 7000;
  const dur = caixa ? 0.12 : 0.04;
  g.gain.setValueAtTime(caixa ? 0.35 : 0.15, inicio);
  g.gain.exponentialRampToValueAtTime(0.001, inicio + dur);
  src.connect(f).connect(g).connect(destino);
  src.start(inicio);
  src.stop(inicio + dur + 0.01);
}

function agendarPasso(c, p, i, destino, inicio) {
  for (const v of p.vozes) {
    const n = v.passos[i % v.passos.length];
    if (n) nota(c, destino, v.onda, n.freq, inicio, n.passos * p.duracaoPasso, v.volume);
  }
  if (p.bateria) {
    const t = p.bateria[i % p.bateria.length];
    if (t !== '.') tambor(c, destino, t, inicio);
  }
}

// ---------------------------------------------------------------- música de fundo

let barramento = null; // volume da música (abaixa durante vinhetas), com filtro para suavizar a onda quadrada
let atual = null; // { nome, p, passo, proximo, volume }
let relogio = null;
let pendente = null; // música pedida antes do som existir (antes do 1º toque)

function prepararBarramento(c) {
  if (barramento) return;
  barramento = c.createGain();
  barramento.gain.value = SOM.volumeMusica;
  const filtro = c.createBiquadFilter();
  filtro.type = 'lowpass';
  filtro.frequency.value = 3200;
  barramento.connect(filtro).connect(saidaAudio());
}

function tique() {
  if (!atual || !somAtivo()) return;
  const c = contextoAudio();
  // voltou de uma pausa ou acabou de ligar: recomeça do relógio de agora (sem despejar notas atrasadas)
  if (atual.proximo < c.currentTime) atual.proximo = c.currentTime + 0.05;
  while (atual.proximo < c.currentTime + ANTECEDENCIA) {
    agendarPasso(c, atual.p, atual.passo, atual.volume, atual.proximo);
    atual.passo = (atual.passo + 1) % atual.p.tamanho;
    atual.proximo += atual.p.duracaoPasso;
  }
}

// Troca a música de fundo (ou continua, se já for a mesma). Pode chamar antes do 1º toque: ela começa quando o som ligar.
export function tocarMusica(nome) {
  if (atual?.nome === nome || pendente === nome) return;
  pararMusica();
  const p = partitura(nome, MUSICAS);
  const c = contextoAudio(false);
  if (!p) return;
  if (!c) {
    pendente = nome;
    return;
  }
  prepararBarramento(c);
  // cada música tem o seu volume, para poder sumir aos poucos na troca sem cortar a nota no meio
  const volume = c.createGain();
  volume.gain.setValueAtTime(0, c.currentTime);
  volume.gain.linearRampToValueAtTime(1, c.currentTime + 0.4);
  volume.connect(barramento);
  atual = { nome, p, passo: 0, proximo: 0, volume };
  if (!relogio) relogio = setInterval(tique, 25);
  tique();
}

export function pararMusica(fade = 0.4) {
  pendente = null;
  if (!atual) return;
  const c = contextoAudio();
  const v = atual.volume;
  v.gain.cancelScheduledValues(c.currentTime);
  v.gain.setValueAtTime(v.gain.value, c.currentTime);
  v.gain.linearRampToValueAtTime(0, c.currentTime + fade);
  setTimeout(() => v.disconnect(), (fade + ANTECEDENCIA + 0.5) * 1000);
  atual = null;
}

export function musicaAtual() {
  return atual?.nome ?? pendente;
}

// Vinheta curta (checkpoint, ingresso, vitória). A música abaixa enquanto ela toca e volta depois.
export function tocarVinheta(nome) {
  if (!somAtivo()) return;
  const c = contextoAudio();
  const p = partitura(nome, VINHETAS);
  if (!p) return;
  prepararBarramento(c);
  const inicio = c.currentTime + 0.02;
  const fim = inicio + p.tamanho * p.duracaoPasso;
  const g = c.createGain();
  g.gain.value = SOM.volumeVinheta;
  g.connect(saidaAudio());
  for (let i = 0; i < p.tamanho; i++) agendarPasso(c, p, i, g, inicio + i * p.duracaoPasso);
  setTimeout(() => g.disconnect(), (fim - c.currentTime + 0.5) * 1000);
  // abaixa a música
  const b = barramento.gain;
  b.cancelScheduledValues(c.currentTime);
  b.setValueAtTime(b.value, c.currentTime);
  b.linearRampToValueAtTime(SOM.volumeMusica * 0.25, inicio + 0.05);
  b.setValueAtTime(SOM.volumeMusica * 0.25, fim);
  b.linearRampToValueAtTime(SOM.volumeMusica, fim + 0.4);
}

// Quando o som liga (1º toque, volta da pausa), agenda na hora, sem esperar o próximo tique.
quandoSomLigar(() => {
  if (pendente) {
    const nome = pendente;
    pendente = null;
    tocarMusica(nome);
  }
  tique();
});
