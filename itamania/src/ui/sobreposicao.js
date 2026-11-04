// Telas em HTML por cima do jogo ("Gire o celular" e "Pausado").
// São HTML, e não Phaser, porque precisam aparecer mesmo com o jogo pausado.
import { CORES_CSS } from '../config.js';

let estiloPronto = false;

function prepararEstilo() {
  if (estiloPronto) return;
  estiloPronto = true;
  const css = `
    .sobreposicao {
      position: fixed; inset: 0; z-index: 10;
      display: none; flex-direction: column; align-items: center; justify-content: center; gap: 16px;
      padding: 24px; box-sizing: border-box; text-align: center;
      background: ${CORES_CSS.lilas}; color: ${CORES_CSS.roxo};
      font-family: 'Press Start 2P', monospace; font-size: 16px; line-height: 1.6;
    }
    .sobreposicao.ativa { display: flex; }
    .sobreposicao small { font-family: 'Patrick Hand', sans-serif; font-size: 22px; }
    .sobreposicao.translucida { background: rgba(109, 107, 217, 0.85); color: ${CORES_CSS.branco}; }
    .sobreposicao.translucida small { color: ${CORES_CSS.amarelo}; animation: piscar 1.2s infinite; }
    #aviso-girar { z-index: 11; }
    .celular {
      width: 40px; height: 68px; border: 4px solid ${CORES_CSS.roxo}; border-radius: 8px;
      background: ${CORES_CSS.rosa}; animation: girar 2s ease-in-out infinite;
    }
    @keyframes girar { 0%, 20% { transform: rotate(0deg); } 50%, 80% { transform: rotate(-90deg); } 100% { transform: rotate(0deg); } }
    @keyframes piscar { 50% { opacity: 0.4; } }
  `;
  const tag = document.createElement('style');
  tag.textContent = css;
  document.head.appendChild(tag);
}

// Os avisos ficam DENTRO da div do jogo: em tela cheia (Android) só aparece o que está dentro dela.
export function criarSobreposicao(id, classes = '') {
  prepararEstilo();
  const el = document.createElement('div');
  el.id = id;
  el.className = `sobreposicao ${classes}`.trim();
  (document.getElementById('jogo') || document.body).appendChild(el);
  return el;
}
