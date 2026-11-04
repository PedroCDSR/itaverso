// Pausa do jogo inteiro, com motivos acumulados.
// Ex.: celular em pé ('girar') e aba sem foco ('foco') ao mesmo tempo: o jogo só volta quando os dois acabarem.
import { suspenderAudio, retomarAudio } from '../audio/som.js';

let jogo = null;
const motivos = new Set();
const ouvintes = new Set();

export function ligarPausaGlobal(game) {
  jogo = game;
}

export function pausar(motivo) {
  const antes = motivos.size;
  motivos.add(motivo);
  if (antes === 0 && jogo) {
    jogo.pause();
    suspenderAudio();
  }
  avisar();
}

export function retomar(motivo) {
  if (!motivos.delete(motivo)) return;
  if (motivos.size === 0 && jogo) {
    jogo.resume();
    retomarAudio();
  }
  avisar();
}

export function estaPausado(motivo) {
  return motivo ? motivos.has(motivo) : motivos.size > 0;
}

// Avisa as telas (DOM) que mostram "Gire o celular" e "Pausado".
export function aoMudarPausa(fn) {
  ouvintes.add(fn);
}

function avisar() {
  ouvintes.forEach((fn) => fn(motivos));
}
