// Áudio do jogo: um AudioContext só, compartilhado pelos efeitos (ZzFX) e pela música.
//
// Caminho do som:  efeitos ─┐
//                           ├─> volume geral (mudo = 0) ─> alto-falante
//                  música ──┘
//
// Desbloqueio (Etapa 9, revisão da Etapa 1): celulares só liberam som dentro de um gesto da pessoa.
// - O contexto é criado e "acordado" (resume + som vazio) dentro do gesto.
// - Os ouvintes NÃO são removidos depois do primeiro toque: no iPhone o primeiro evento pode não contar
//   como gesto (pointerdown/touchstart não contam; touchend e click contam), e o iOS também "interrompe"
//   o áudio quando chega ligação ou a pessoa troca de app. A cada toque, se o som não está rodando, tenta de novo.
// - O Phaser roda com `audio.noAudio` (main.js): ele não cria um segundo AudioContext que nunca seria usado.

import { SOM } from '../config.js';

const CHAVE_MUDO = 'aladdin-som-mudo';

let ctx = null;
let saida = null; // volume geral
let mudo = lerMudo();
let pausado = false; // jogo pausado (aba sem foco, celular em pé)
const aoLigar = new Set(); // quem quer saber quando o som começa a rodar (a música)
const aoMudarMudo = new Set(); // botões de som que precisam se redesenhar

function lerMudo() {
  try {
    return localStorage.getItem(CHAVE_MUDO) === '1';
  } catch {
    return false;
  }
}

function salvarMudo() {
  try {
    localStorage.setItem(CHAVE_MUDO, mudo ? '1' : '0');
  } catch {
    // navegação privada: só não lembra a escolha
  }
}

// criar = false: só devolve o contexto se ele já existir (evita criar antes do 1º toque, o que gera aviso no Chrome).
export function contextoAudio(criar = true) {
  if (!ctx && criar) {
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return null;
    ctx = new AC();
    saida = ctx.createGain();
    saida.gain.value = mudo ? 0 : SOM.volumeGeral;
    saida.connect(ctx.destination);
    ctx.addEventListener?.('statechange', () => {
      if (ctx.state === 'running') aoLigar.forEach((fn) => fn());
    });
  }
  return ctx;
}

// Nó onde efeitos e música se ligam (passa pelo volume geral).
export function saidaAudio() {
  contextoAudio();
  return saida;
}

// Pode agendar som? Vale também com o contexto ainda "acordando" (o resume() é assíncrono): o som agendado
// toca assim que ele ligar. É o caso do clique no JOGAR, que é o mesmo toque que libera o áudio.
export function somAtivo() {
  return !!ctx && ctx.state !== 'closed' && !mudo && !pausado;
}

export function quandoSomLigar(fn) {
  aoLigar.add(fn);
}

export function quandoMudarMudo(fn) {
  aoMudarMudo.add(fn);
  return () => aoMudarMudo.delete(fn);
}

// Tenta ligar o som. Só funciona de verdade dentro de um gesto (toque, clique, tecla).
function acordar() {
  if (mudo || pausado) return;
  const c = contextoAudio();
  if (!c || c.state === 'running') return;
  // O iPhone antigo exige tocar algo (mesmo vazio) dentro do gesto, além do resume().
  const buf = c.createBuffer(1, 1, 22050);
  const src = c.createBufferSource();
  src.buffer = buf;
  src.connect(c.destination);
  src.start(0);
  c.resume().catch(() => {});
}

// Liga os ouvintes de gesto. Ficam ligados o tempo todo (ver comentário no topo); o custo é uma checagem por toque.
export function iniciarSom() {
  ['touchend', 'pointerup', 'click', 'keydown', 'pointerdown'].forEach((ev) =>
    window.addEventListener(ev, acordar, { capture: true, passive: true }),
  );
  // atalho no computador: M liga e desliga o som
  window.addEventListener('keydown', (ev) => {
    if (!ev.repeat && (ev.key === 'm' || ev.key === 'M')) alternarSom();
  });
}

export function estaMudo() {
  return mudo;
}

export function alternarSom() {
  mudo = !mudo;
  salvarMudo();
  const c = contextoAudio();
  if (c) {
    saida.gain.setTargetAtTime(mudo ? 0 : SOM.volumeGeral, c.currentTime, 0.02);
    // mudo: suspende para não gastar bateria; ligar acontece dentro do toque no botão, então o iPhone aceita
    if (mudo) setTimeout(() => mudo && c.state === 'running' && c.suspend(), 120);
    else acordar();
  }
  aoMudarMudo.forEach((fn) => fn(mudo));
  return mudo;
}

// Chamados pela pausa global (ui/pausaGlobal.js).
export function suspenderAudio() {
  pausado = true;
  if (ctx && ctx.state === 'running') ctx.suspend();
}

export function retomarAudio() {
  pausado = false;
  // quase sempre chamado dentro do toque que tira a pausa; se não for, o próximo toque acorda o som
  acordar();
}
