// Efeitos sonoros gerados em código com o ZzFX (sem arquivos de áudio). Todos originais deste projeto.
// Cada efeito é a lista de parâmetros do ZzFX, na ordem:
//   volume, aleatório, frequência, ataque, sustentação, soltura, forma, curva, deslize, deslize2,
//   salto de tom, tempo do salto, repetição, ruído, modulação, bitcrush, eco, volume sust., decaimento, tremolo, filtro
// Forma: 0 seno, 1 triângulo, 2 serra, 3 tangente, 4 ruído. Para criar um som novo, dá para testar no site do ZzFX
// (https://killedbyapixel.github.io/ZzFX/) e colar a lista aqui.

import { SOM } from '../config.js';
import { zzfxG, ZZFX_TAXA } from './zzfx.js';
import { contextoAudio, saidaAudio, somAtivo } from './som.js';

export const EFEITOS = {
  // jogador
  pulo: [0.5, 0.05, 260, 0.01, 0.03, 0.12, 0, 1.4, 11],
  maca: [0.35, 0.05, 520, 0.005, 0.02, 0.07, 1, 1, -22, 0, 0, 0, 0, 1.5],
  dano: [0.55, 0.05, 330, 0, 0.05, 0.25, 1, 2, -9, 0, 0, 0, 0, 0.6],
  // mundo
  toldo: [0.6, 0, 140, 0.01, 0.08, 0.3, 0, 1, 7, 0, 0, 0, 0, 0, 9],
  pisao: [0.55, 0.05, 150, 0.005, 0.03, 0.12, 1, 2, 16],
  capivaraCome: [0.45, 0.1, 240, 0, 0.04, 0.08, 2, 1, 0, 0, -70, 0.04, 0, 0, 0, 0, 0, 1, 0, 0, 1500],
  // coleta
  sapatilha: [0.45, 0, 1180, 0, 0.04, 0.16, 0, 1.8, 0, 0, 560, 0.04],
  pegarMaca: [0.45, 0, 620, 0, 0.03, 0.09, 1, 1.5, 0, 0, 240, 0.03],
  coracao: [0.5, 0, 523, 0.01, 0.12, 0.25, 0, 1, 0, 0, 262, 0.06, 0.12],
  // interface e diálogo
  botao: [0.4, 0, 660, 0, 0.02, 0.06, 1, 1, 0, 0, 330, 0.02],
  blip: [0.22, 0.12, 820, 0, 0.012, 0.03, 1, 1],
  // chefe
  acertoChefe: [0.7, 0.05, 220, 0.005, 0.08, 0.3, 2, 1.5, -6, 0, 0, 0, 0, 0.8, 0, 0, 0.06, 1, 0, 0, 2400],
  projetil: [0.3, 0.05, 700, 0.02, 0.05, 0.15, 0, 1, -14, 0, 0, 0, 0, 0, 12],
};

// Buffers prontos (gerar custa pouco, mas não precisa repetir a cada pulo).
const cache = new Map();

function buffer(nome) {
  let b = cache.get(nome);
  if (!b) {
    const params = EFEITOS[nome];
    if (!params) return null;
    const amostras = zzfxG(...params);
    const c = contextoAudio();
    b = c.createBuffer(1, amostras.length || 1, ZZFX_TAXA);
    b.getChannelData(0).set(amostras);
    cache.set(nome, b);
  }
  return b;
}

const ultimaVez = new Map();

// Toca um efeito. `variar` muda um pouco o tom a cada vez (bom para o blip do diálogo e coletas seguidas).
export function tocarEfeito(nome, { variar = 0.04, volume = 1 } = {}) {
  if (!somAtivo()) return;
  const c = contextoAudio();
  // evita o mesmo som empilhado no mesmo instante (ex.: duas sapatilhas no mesmo quadro)
  const agora = c.currentTime;
  if (agora - (ultimaVez.get(nome) ?? -1) < 0.03) return;
  ultimaVez.set(nome, agora);
  const b = buffer(nome);
  if (!b) return;
  const src = c.createBufferSource();
  src.buffer = b;
  src.playbackRate.value = 1 + (Math.random() * 2 - 1) * variar;
  const g = c.createGain();
  g.gain.value = SOM.volumeEfeitos * volume;
  src.connect(g).connect(saidaAudio());
  src.start();
}
