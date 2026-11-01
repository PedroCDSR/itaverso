// "Gire o celular": aparece quando um aparelho de toque está em pé, e pausa o jogo.
// No computador (mouse) nunca aparece, mesmo com a janela estreita.
import { TEXTOS } from '../data/textos.js';
import { criarSobreposicao } from './sobreposicao.js';
import { pausar, retomar } from './pausaGlobal.js';

export function iniciarAvisoGirar() {
  const el = criarSobreposicao('aviso-girar');
  el.innerHTML = `<div class="celular"></div><div></div><small></small>`;
  el.children[1].textContent = TEXTOS.mobile.girar;
  el.children[2].textContent = TEXTOS.mobile.girarDetalhe;

  const emPe = window.matchMedia('(orientation: portrait) and (pointer: coarse)');
  const conferir = () => {
    if (emPe.matches) {
      el.classList.add('ativa');
      pausar('girar');
    } else {
      el.classList.remove('ativa');
      retomar('girar');
    }
  };
  emPe.addEventListener('change', conferir);
  conferir();
}
