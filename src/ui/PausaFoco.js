// Pausa quando a aba perde o foco (trocou de app, chegou notificação, desligou a tela).
// Volta só quando a pessoa toca: assim ninguém leva dano no susto ao voltar para o jogo.
// (O menu de pausa com opções é a cena Pausa, aberta pelo botão ⏸ ou por Esc/P durante a fase.)
import { TEXTOS } from '../data/textos.js';
import { criarSobreposicao } from './sobreposicao.js';
import { pausar, retomar, estaPausado } from './pausaGlobal.js';

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

  // Teclado: Enter, espaço, Esc ou P continuam depois de perder o foco.
  window.addEventListener('keydown', (ev) => {
    if (ev.repeat || !estaPausado('foco')) return;
    if (['Enter', ' ', 'Escape', 'p', 'P'].includes(ev.key)) continuar(ev);
  });
}
