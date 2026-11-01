// Pausa quando a aba perde o foco (trocou de app, chegou notificação, desligou a tela) e com Esc/P.
// Volta só quando a pessoa toca: assim ninguém leva dano no susto ao voltar para o jogo.
import { TEXTOS } from '../data/textos.js';
import { criarSobreposicao } from './sobreposicao.js';
import { pausar, retomar, estaPausado } from './pausaGlobal.js';

let pausarExterno = () => {};

// Botão de pausa do HUD: mostra a mesma tela "Pausado / Toque para continuar".
export function pausarAgora() {
  pausarExterno();
}

export function iniciarPausaFoco() {
  const el = criarSobreposicao('aviso-pausa', 'translucida');
  el.innerHTML = `<div></div><small></small>`;
  el.children[0].textContent = TEXTOS.mobile.pausado;
  el.children[1].textContent = TEXTOS.mobile.tocarContinuar;

  const mostrar = () => {
    if (estaPausado('foco')) return;
    el.classList.add('ativa');
    pausar('foco');
  };
  pausarExterno = mostrar;
  const continuar = (ev) => {
    if (!estaPausado('foco')) return;
    ev.preventDefault();
    el.classList.remove('ativa');
    retomar('foco');
  };

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) mostrar();
  });
  window.addEventListener('blur', mostrar);
  window.addEventListener('pagehide', mostrar);
  el.addEventListener('pointerup', continuar);

  // Teclado: Esc ou P pausa e continua; Enter e espaço também continuam.
  window.addEventListener('keydown', (ev) => {
    if (ev.repeat) return;
    if (ev.key === 'Escape' || ev.key === 'p' || ev.key === 'P') {
      estaPausado('foco') ? continuar(ev) : mostrar();
    } else if ((ev.key === 'Enter' || ev.key === ' ') && estaPausado('foco')) {
      continuar(ev);
    }
  });
}
