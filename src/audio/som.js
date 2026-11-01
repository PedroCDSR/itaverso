// Áudio do jogo: um AudioContext só, compartilhado pelos efeitos (ZzFX na Etapa 9) e pela música.
// Celulares só liberam som depois de um toque: desbloquearAudio() roda no primeiro toque ou tecla.

const CHAVE_MUDO = 'aladdin-som-mudo';

let ctx = null;
let mudo = lerMudo();
let jogo = null;

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

export function contextoAudio() {
  if (!ctx) {
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return null;
    ctx = new AC();
  }
  return ctx;
}

// Liga o som no primeiro gesto da pessoa. O iPhone exige tocar um som (mesmo vazio) dentro do gesto.
export function iniciarSom(game) {
  jogo = game;
  jogo.sound.mute = mudo;
  const desbloquear = () => {
    const c = contextoAudio();
    if (!c) return;
    const buf = c.createBuffer(1, 1, 22050);
    const src = c.createBufferSource();
    src.buffer = buf;
    src.connect(c.destination);
    src.start(0);
    if (c.state !== 'running' && !mudo) c.resume();
    ['pointerdown', 'touchend', 'keydown'].forEach((ev) => window.removeEventListener(ev, desbloquear, true));
  };
  ['pointerdown', 'touchend', 'keydown'].forEach((ev) => window.addEventListener(ev, desbloquear, true));
}

export function estaMudo() {
  return mudo;
}

export function alternarSom() {
  mudo = !mudo;
  salvarMudo();
  if (jogo) jogo.sound.mute = mudo;
  const c = contextoAudio();
  if (c) mudo ? c.suspend() : c.resume();
  return mudo;
}

export function suspenderAudio() {
  if (ctx && ctx.state === 'running') ctx.suspend();
}

export function retomarAudio() {
  if (ctx && !mudo) ctx.resume();
}

// Bipe simples, só para testar o som enquanto o ZzFX não entra (Etapa 9).
export function bipe(freq = 660, duracao = 0.08) {
  const c = contextoAudio();
  if (!c || mudo || c.state !== 'running') return;
  const osc = c.createOscillator();
  const vol = c.createGain();
  osc.type = 'square';
  osc.frequency.setValueAtTime(freq, c.currentTime);
  osc.frequency.exponentialRampToValueAtTime(freq * 1.5, c.currentTime + duracao);
  vol.gain.setValueAtTime(0.06, c.currentTime);
  vol.gain.exponentialRampToValueAtTime(0.0001, c.currentTime + duracao);
  osc.connect(vol).connect(c.destination);
  osc.start();
  osc.stop(c.currentTime + duracao);
}
