// Caixa de diálogo (CLAUDE.md, seções 2.6 e 11.4).
//
// Por que HTML e não texto do Phaser: o jogo desenha em 480x270 e o navegador amplia o canvas inteiro
// (pixelArt). Uma letra manuscrita de 17 px ampliada 2,5x fica serrilhada e borrada no celular. Em HTML, a
// Patrick Hand é desenhada na resolução real da tela, nítida. A caixa acompanha a posição e o tamanho do canvas:
// todas as medidas são em "pixels do jogo" multiplicados pela escala atual (variável CSS --u).
//
// Uso:  await dialogo.mostrar([{ nome: 'Jasmine', texto: 'Oi!', cor: '#FFB0FA' }, ...])
// Avança com toque em qualquer lugar da tela ou com espaço / Enter / W / X / J / seta para cima.
// Primeiro toque durante a "máquina de escrever" completa o texto; o seguinte vai para a próxima caixa.
import { CORES_CSS, DIALOGO } from '../config.js';
import { estaPausado } from './pausaGlobal.js';
import { tocarEfeito } from '../audio/efeitos.js';

let estiloPronto = false;

function prepararEstilo() {
  if (estiloPronto) return;
  estiloPronto = true;
  const css = `
    .dialogo {
      position: absolute; z-index: 5; display: none; box-sizing: border-box;
      --u: 1;
      padding: calc(var(--u) * 5px) calc(var(--u) * 10px) calc(var(--u) * 6px);
      background: #FFFFFF; color: ${CORES_CSS.roxo};
      border: calc(var(--u) * 2px) solid ${CORES_CSS.roxo}; border-radius: calc(var(--u) * 6px);
      box-shadow: 0 calc(var(--u) * 2px) 0 rgba(46, 26, 51, 0.35);
      pointer-events: none;
    }
    .dialogo.ativa { display: block; }
    .dialogo .nome {
      position: absolute; left: calc(var(--u) * 8px); top: calc(var(--u) * -8px);
      padding: calc(var(--u) * 2px) calc(var(--u) * 5px);
      font-family: 'Press Start 2P', monospace; font-size: calc(var(--u) * 7px); line-height: 1;
      color: ${CORES_CSS.branco}; background: ${CORES_CSS.roxo}; border-radius: calc(var(--u) * 3px);
      white-space: nowrap;
    }
    .dialogo .fala {
      font-family: 'Patrick Hand', sans-serif; font-size: calc(var(--u) * ${DIALOGO.tamanhoFonte}px);
      line-height: 1.2; min-height: 2.4em; margin-top: calc(var(--u) * 2px);
      overflow-wrap: break-word;
    }
    /* letras ainda não "escritas" ocupam o lugar (a caixa não pula de tamanho), mas ficam invisíveis */
    .dialogo .fala .falta { visibility: hidden; }
    .dialogo .seta {
      position: absolute; right: calc(var(--u) * 8px); bottom: calc(var(--u) * 5px);
      width: 0; height: 0; display: none;
      border-left: calc(var(--u) * 5px) solid transparent; border-right: calc(var(--u) * 5px) solid transparent;
      border-top: calc(var(--u) * 6px) solid ${CORES_CSS.rosa};
      animation: dialogo-seta 0.7s ease-in-out infinite;
    }
    .dialogo.pronta .seta { display: block; }
    @keyframes dialogo-seta { 50% { transform: translateY(calc(var(--u) * 2px)); } }
  `;
  const tag = document.createElement('style');
  tag.textContent = css;
  document.head.appendChild(tag);
}

const TECLAS = new Set([' ', 'Enter', 'w', 'W', 'x', 'X', 'j', 'J', 'ArrowUp']);

export class Dialogo {
  constructor(scene) {
    prepararEstilo();
    this.scene = scene;
    this.container = document.getElementById('jogo') || document.body;
    const el = document.createElement('div');
    el.className = 'dialogo';
    el.innerHTML = '<div class="nome"></div><div class="fala"><span class="dita"></span><span class="falta"></span></div><div class="seta"></div>';
    this.container.appendChild(el);
    this.el = el;
    this.elNome = el.querySelector('.nome');
    this.elFala = el.querySelector('.fala');
    this.elDita = el.querySelector('.dita');
    this.elFalta = el.querySelector('.falta');

    this.ativo = false;
    this.dedosNovos = new Set(); // só vale o toque que COMEÇOU com a caixa aberta

    this.aoApertar = (ev) => {
      if (!this.ativo || estaPausado()) return;
      this.dedosNovos.add(ev.pointerId);
    };
    this.aoSoltar = (ev) => {
      if (!this.ativo || estaPausado() || !this.dedosNovos.delete(ev.pointerId)) return;
      this.avancar();
    };
    this.aoTeclar = (ev) => {
      if (!this.ativo || ev.repeat || estaPausado() || !TECLAS.has(ev.key)) return;
      ev.preventDefault();
      this.avancar();
    };
    this.container.addEventListener('pointerdown', this.aoApertar, true);
    this.container.addEventListener('pointerup', this.aoSoltar, true);
    // fase de captura: roda ANTES da tela de pausa (ui/PausaFoco.js), que usa espaço/Enter para continuar.
    // Assim a tecla que tira da pausa não avança o diálogo junto.
    window.addEventListener('keydown', this.aoTeclar, true);

    scene.events.on('update', this.posicionar, this);
    scene.events.once('shutdown', () => this.destruir());
  }

  // Mostra uma lista de caixas; a promessa resolve quando a última for fechada.
  mostrar(caixas) {
    this.caixas = caixas.slice();
    this.indice = -1;
    this.ativo = true;
    this.dedosNovos.clear();
    this.el.classList.add('ativa');
    this.posicionar();
    return new Promise((resolve) => {
      this.aoTerminar = resolve;
      this.proxima();
    });
  }

  proxima() {
    this.indice++;
    if (this.indice >= this.caixas.length) {
      this.fechar();
      return;
    }
    const c = this.caixas[this.indice];
    this.elNome.textContent = c.nome || '';
    this.elNome.style.display = c.nome ? 'block' : 'none';
    this.elNome.style.background = c.cor || CORES_CSS.roxo;
    this.texto = c.texto;
    this.letras = 0;
    this.abertaEm = this.scene.time.now;
    this.el.classList.remove('pronta');
    this.desenharTexto();
    this.conferirLinhas();
    // "máquina de escrever" no relógio da cena: para junto quando o jogo pausa
    this.relogio?.remove();
    this.relogio = this.scene.time.addEvent({
      delay: 1000 / DIALOGO.letrasPorSegundo,
      loop: true,
      callback: () => {
        this.letras++;
        this.desenharTexto();
        // "voz" da máquina de escrever: um blip a cada 3 letras (espaços não contam)
        if (this.letras % 3 === 0 && this.texto[this.letras - 1] !== ' ') tocarEfeito('blip', { variar: 0.12, volume: 0.6 });
        if (this.letras >= this.texto.length) this.completar();
      },
    });
  }

  desenharTexto() {
    this.elDita.textContent = this.texto.slice(0, this.letras);
    this.elFalta.textContent = this.texto.slice(this.letras);
  }

  completar() {
    this.relogio?.remove();
    this.relogio = null;
    this.letras = this.texto.length;
    this.desenharTexto();
    this.el.classList.add('pronta');
  }

  avancar() {
    // Um mesmo toque pode chegar duas vezes (toque em qualquer lugar + botão PRÓXIMO do canvas):
    // ignora a segunda chamada no mesmo instante.
    const agora = performance.now();
    if (agora - (this.ultimoAvanco || 0) < 120) return;
    if (this.scene.time.now - this.abertaEm < DIALOGO.esperaMinimaMs) return;
    this.ultimoAvanco = agora;
    if (this.letras < this.texto.length) this.completar();
    else this.proxima();
  }

  fechar() {
    this.ativo = false;
    this.relogio?.remove();
    this.el.classList.remove('ativa', 'pronta');
    const fim = this.aoTerminar;
    this.aoTerminar = null;
    fim?.();
  }

  // Acompanha o canvas (que o Phaser centraliza e amplia com Scale.FIT).
  posicionar() {
    if (!this.ativo) return;
    const canvas = this.scene.game.canvas;
    const rc = canvas.getBoundingClientRect();
    const rp = this.container.getBoundingClientRect();
    const u = rc.width / this.scene.scale.width;
    if (u === this.ultimaEscala && rc.left === this.ultimoX && rc.top === this.ultimoY) return;
    this.ultimaEscala = u;
    this.ultimoX = rc.left;
    this.ultimoY = rc.top;
    const s = this.el.style;
    s.setProperty('--u', String(u));
    s.width = `${DIALOGO.largura * u}px`;
    s.left = `${rc.left - rp.left + ((this.scene.scale.width - DIALOGO.largura) / 2) * u}px`;
    s.top = `${rc.top - rp.top + DIALOGO.topo * u}px`;
  }

  // Só no modo dev: avisa no console se uma fala passar de 2 linhas (regra 6 do CLAUDE.md).
  conferirLinhas() {
    if (!import.meta.env.DEV) return;
    const altura = this.elFala.getBoundingClientRect().height;
    const linha = parseFloat(getComputedStyle(this.elFala).lineHeight);
    const linhas = Math.round(altura / linha);
    if (linhas > DIALOGO.maxLinhas) {
      console.warn(`Fala com ${linhas} linhas (máximo ${DIALOGO.maxLinhas}): "${this.texto}"`);
    }
  }

  destruir() {
    this.relogio?.remove();
    this.scene.events.off('update', this.posicionar, this);
    this.container.removeEventListener('pointerdown', this.aoApertar, true);
    this.container.removeEventListener('pointerup', this.aoSoltar, true);
    window.removeEventListener('keydown', this.aoTeclar, true);
    this.el.remove();
  }
}
