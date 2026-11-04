// Mapa-múndi em alta resolução, numa camada HTML por cima do canvas (pedido do Pedro, 04/11/2026).
//
// Por que HTML: o canvas tem 480x270 e é ampliado inteiro; o mapa do Pedro (1080x1920) reduzido a 480 px perdia
// os detalhes. Aqui a imagem original é desenhada na resolução real da tela, ocupando a largura do canvas, e rola
// só na vertical: arrastar (dedo ou mouse), roda do mouse e setas para cima e para baixo.
//
// O `body` tem `touch-action: none` e o Phaser escuta toques na div #jogo; por isso o arraste é feito à mão com
// pointer events e todos os eventos param aqui (stopPropagation), sem vazar para o jogo.
//
// A camada cobre o canvas inteiro menos a faixa de baixo (`rodape`, em pixels do jogo), onde fica o painel do
// Phaser com o nome da fase e os botões. Coordenadas das moedas e do herói em pixels do desenho original.
import { CORES_CSS, FONTES } from '../config.js';

export const MAPA_LARGURA = 1080;
export const MAPA_ALTURA = 1920;

let estiloPronto = false;

function prepararEstilo() {
  if (estiloPronto) return;
  estiloPronto = true;
  const css = `
    .mapa-hd {
      position: absolute; z-index: 2; overflow: hidden; touch-action: none; cursor: grab;
      background: ${CORES_CSS.roxo}; opacity: 0; transition: opacity 0.3s;
      -webkit-user-select: none; user-select: none;
    }
    .mapa-hd.visivel { opacity: 1; }
    .mapa-hd.arrastando { cursor: grabbing; }
    .mapa-hd .fundo { position: absolute; left: 0; top: 0; width: 100%; height: 100%; pointer-events: none; }
    .mapa-hd .anel {
      position: absolute; box-sizing: border-box; border-radius: 50%; pointer-events: none;
      border: solid ${CORES_CSS.amarelo}; transform: translate(-50%, -50%);
      animation: mapa-anel 0.9s ease-out infinite;
    }
    @keyframes mapa-anel {
      from { transform: translate(-50%, -50%) scale(1); opacity: 1; }
      to { transform: translate(-50%, -50%) scale(1.7); opacity: 0; }
    }
    .mapa-hd .heroi {
      position: absolute; left: 0; top: 0; pointer-events: none; image-rendering: pixelated;
      filter: drop-shadow(0 2px 0 rgba(26, 26, 64, 0.45));
    }
    .mapa-hd .faixa {
      position: absolute; left: 50%; transform: translateX(-50%); white-space: nowrap; pointer-events: none;
      font-family: ${FONTES.dialogo}, sans-serif; color: ${CORES_CSS.branco};
      background: rgba(43, 45, 92, 0.88); border: solid ${CORES_CSS.amarelo};
      transition: opacity 0.4s;
    }
    .mapa-hd .faixa.some { opacity: 0; }
  `;
  const tag = document.createElement('style');
  tag.textContent = css;
  document.head.appendChild(tag);
}

export class MapaHtml {
  // opcoes: { imagem, moedas: [[x, y]...] (índice = fase), aneis: [n...], rodape (px do jogo),
  //           aoTocarMoeda(n), quadroHeroi() -> Phaser.Frame, alturaHeroi (px do desenho) }
  constructor(scene, opcoes) {
    prepararEstilo();
    this.scene = scene;
    this.op = opcoes;
    this.container = document.getElementById('jogo') || document.body;
    this.scroll = MAPA_ALTURA; // em px do desenho; começa embaixo (é limitado no primeiro posicionar)
    this.alvo = null; // rolagem suave (teclas, roda, seguir o herói)
    this.velocidade = 0; // inércia depois de soltar o arraste (px do desenho por ms)
    this.heroiPos = { x: 0, y: 0, virado: false };

    const el = document.createElement('div');
    el.className = 'mapa-hd';
    // O mapa é desenhado num canvas do tamanho da área visível (só o trecho que aparece), e não como uma <img>
    // de 1920 px de altura movida com transform: a camada gigante quebrava a composição do canvas do Phaser no
    // Chromium e gastava memória de vídeo no celular.
    el.innerHTML = '<canvas class="fundo"></canvas><div class="faixa some"></div>';
    this.el = el;
    this.trilho = el; // moedas e herói ficam direto na camada, posicionados já descontando a rolagem
    this.cvFundo = el.querySelector('.fundo');
    this.ctxFundo = this.cvFundo.getContext('2d');
    this.faixa = el.querySelector('.faixa');
    this.img = new Image();
    this.img.onload = () => (this.desenhado = null);
    this.img.src = opcoes.imagem;

    this.aneis = (opcoes.aneis || []).map((n) => {
      const a = document.createElement('div');
      a.className = 'anel';
      this.trilho.insertBefore(a, this.faixa);
      return { n, el: a };
    });

    // herói: canvas pequeno com o quadro atual da animação do Phaser (pixel nítido)
    this.cvHeroi = document.createElement('canvas');
    this.cvHeroi.className = 'heroi';
    this.ctxHeroi = this.cvHeroi.getContext('2d');
    this.trilho.insertBefore(this.cvHeroi, this.faixa);
    this.container.appendChild(el);

    this.ligarEventos();
    scene.events.on('update', this.atualizar, this);
    scene.events.once('shutdown', () => this.destruir());
    requestAnimationFrame(() => el.classList.add('visivel'));
  }

  // ---------- eventos ----------
  ligarEventos() {
    const el = this.el;
    const parar = (ev) => ev.stopPropagation();
    this.paradores = ['touchstart', 'touchmove', 'touchend', 'touchcancel', 'mousedown', 'mousemove', 'mouseup', 'click', 'contextmenu'];
    for (const tipo of this.paradores) el.addEventListener(tipo, parar);
    this.parar = parar;

    this.arraste = null;
    this.aoApertar = (ev) => {
      ev.stopPropagation();
      if (this.arraste) return; // um dedo só
      this.arraste = { id: ev.pointerId, y0: ev.clientY, x0: ev.clientX, ultimoY: ev.clientY, ultimoT: performance.now(), moveu: false, s0: this.scroll };
      this.velocidade = 0;
      this.alvo = null;
      el.setPointerCapture?.(ev.pointerId);
    };
    this.aoMover = (ev) => {
      ev.stopPropagation();
      const a = this.arraste;
      if (!a || ev.pointerId !== a.id) return;
      if (!a.moveu && Math.hypot(ev.clientY - a.y0, ev.clientX - a.x0) > 8) {
        a.moveu = true;
        el.classList.add('arrastando');
      }
      if (!a.moveu) return;
      const agora = performance.now();
      const dy = (a.ultimoY - ev.clientY) / this.k;
      const dt = Math.max(1, agora - a.ultimoT);
      this.velocidade = this.velocidade * 0.6 + (dy / dt) * 0.4;
      a.ultimoY = ev.clientY;
      a.ultimoT = agora;
      this.rolarPara(this.scroll + dy);
    };
    this.aoSoltar = (ev) => {
      ev.stopPropagation();
      const a = this.arraste;
      if (!a || ev.pointerId !== a.id) return;
      this.arraste = null;
      el.classList.remove('arrastando');
      if (ev.type === 'pointercancel') return;
      if (!a.moveu) {
        this.velocidade = 0;
        this.tocar(ev.clientX, ev.clientY);
      } else if (performance.now() - a.ultimoT > 90) {
        this.velocidade = 0; // parou o dedo antes de soltar: sem inércia
      }
    };
    this.aoRodar = (ev) => {
      ev.preventDefault();
      ev.stopPropagation();
      const passo = ev.deltaMode === 1 ? ev.deltaY * 40 : ev.deltaMode === 2 ? ev.deltaY * 400 : ev.deltaY;
      this.velocidade = 0;
      this.alvo = this.limitar((this.alvo ?? this.scroll) + passo / this.k);
    };
    el.addEventListener('pointerdown', this.aoApertar);
    el.addEventListener('pointermove', this.aoMover);
    el.addEventListener('pointerup', this.aoSoltar);
    el.addEventListener('pointercancel', this.aoSoltar);
    el.addEventListener('wheel', this.aoRodar, { passive: false });
  }

  // Toque sem arraste: acha a moeda mais perto do ponto tocado.
  tocar(cx, cy) {
    const r = this.el.getBoundingClientRect();
    const x = (cx - r.left) / this.k;
    const y = (cy - r.top) / this.k + this.scroll;
    let melhor = 0;
    let dist = 60; // raio de toque em px do desenho (a moeda tem ~30)
    this.op.moedas.forEach((p, n) => {
      if (!p) return;
      const d = Math.hypot(p[0] - x, p[1] - 10 - y);
      if (d < dist) {
        dist = d;
        melhor = n;
      }
    });
    if (melhor) this.op.aoTocarMoeda?.(melhor);
  }

  // ---------- rolagem ----------
  get alturaVisivel() {
    return this.alturaCss / this.k;
  }

  limitar(s) {
    return Math.max(0, Math.min(MAPA_ALTURA - this.alturaVisivel, s));
  }

  rolarPara(s) {
    this.scroll = this.limitar(s);
  }

  // Rola suave pelas teclas (dir = -1 sobe, 1 desce).
  rolarPasso(dir) {
    this.velocidade = 0;
    this.alvo = this.limitar((this.alvo ?? this.scroll) + dir * this.alturaVisivel * 0.35);
  }

  // Mostra um ponto do desenho (y) mais ou menos no meio da tela.
  centrar(y, suave = true) {
    const s = this.limitar(y - this.alturaVisivel * 0.55);
    if (suave) this.alvo = s;
    else {
      this.scroll = s;
      this.alvo = null;
    }
  }

  // Se o herói sair da parte visível, rola até ele.
  seguirHeroi() {
    const y = this.heroiPos.y;
    const margem = this.alturaVisivel * 0.22;
    if (y - 90 < this.scroll + margem || y > this.scroll + this.alturaVisivel - margem) this.centrar(y);
  }

  irParaBaixo() {
    this.scroll = MAPA_ALTURA;
    this.alvo = null;
    this.iniciado = false; // o próximo posicionar limita
  }

  mostrarFaixa(texto) {
    this.faixa.textContent = texto;
    this.faixa.classList.toggle('some', !texto);
  }

  esconder() {
    this.el.classList.remove('visivel');
  }

  // ---------- a cada quadro ----------
  atualizar(t, delta) {
    this.posicionar();
    if (!this.k) return;
    if (!this.arraste && Math.abs(this.velocidade) > 0.01) {
      this.rolarPara(this.scroll + this.velocidade * delta);
      this.velocidade *= Math.pow(0.994, delta);
      if (this.scroll <= 0 || this.scroll >= MAPA_ALTURA - this.alturaVisivel) this.velocidade = 0;
    } else if (this.alvo != null) {
      const d = this.alvo - this.scroll;
      if (Math.abs(d) < 0.5) {
        this.scroll = this.alvo;
        this.alvo = null;
      } else this.scroll += d * Math.min(1, delta * 0.012);
    }
    this.desenharFundo();
    this.desenharHeroi();
  }

  // Copia o trecho visível do mapa para o canvas da camada, na resolução real da tela.
  desenharFundo() {
    const img = this.img;
    if (!img.complete || !img.naturalWidth) return;
    const dpr = window.devicePixelRatio || 1;
    const cv = this.cvFundo;
    const w = Math.round(this.el.clientWidth * dpr);
    const h = Math.round(this.alturaCss * dpr);
    const s = Math.round(this.scroll * this.k * dpr) / (this.k * dpr); // rolagem presa ao pixel da tela
    const chave = `${w}x${h}@${s}`;
    if (chave === this.desenhado) return;
    this.desenhado = chave;
    if (cv.width !== w || cv.height !== h) {
      cv.width = w;
      cv.height = h;
    }
    const c = this.ctxFundo;
    // ampliando, pixel nítido; reduzindo, suavizado (fica melhor que pular pixels)
    c.imageSmoothingEnabled = w < MAPA_LARGURA;
    c.imageSmoothingQuality = 'high';
    const fonteH = h * (MAPA_LARGURA / w);
    c.drawImage(img, 0, s, MAPA_LARGURA, fonteH, 0, 0, w, h);
    this.scrollDesenhado = s;
    for (const a of this.aneis) a.el.style.top = `${(this.op.moedas[a.n][1] - s) * this.k}px`;
  }

  // Acompanha o canvas (que o Phaser centraliza e amplia com Scale.FIT), também ao girar a tela.
  posicionar() {
    const canvas = this.scene.game.canvas;
    const rc = canvas.getBoundingClientRect();
    const rp = this.container.getBoundingClientRect();
    const u = rc.width / this.scene.scale.width;
    if (u === this.ultimaEscala && rc.left === this.ultimoX && rc.top === this.ultimoY) return;
    this.ultimaEscala = u;
    this.ultimoX = rc.left;
    this.ultimoY = rc.top;
    const largura = rc.width;
    this.alturaCss = rc.height - (this.op.rodape || 0) * u;
    this.k = largura / MAPA_LARGURA;
    const s = this.el.style;
    s.left = `${rc.left - rp.left}px`;
    s.top = `${rc.top - rp.top}px`;
    s.width = `${largura}px`;
    s.height = `${this.alturaCss}px`;
    for (const a of this.aneis) {
      const [x, y] = this.op.moedas[a.n];
      const d = 34 * this.k;
      Object.assign(a.el.style, { left: `${x * this.k}px`, top: `${(y - this.scroll) * this.k}px`, width: `${d}px`, height: `${d}px`, borderWidth: `${Math.max(2, 5 * this.k)}px` });
    }
    this.scroll = this.limitar(this.scroll);
    if (this.alvo != null) this.alvo = this.limitar(this.alvo);
    this.quadroDesenhado = null; // redesenha o herói no tamanho novo
    this.desenhado = null;
  }

  desenharHeroi() {
    const q = this.op.quadroHeroi?.();
    if (!q) return;
    const cv = this.cvHeroi;
    if (q !== this.quadroDesenhado) {
      this.quadroDesenhado = q;
      if (cv.width !== q.cutWidth || cv.height !== q.cutHeight) {
        cv.width = q.cutWidth;
        cv.height = q.cutHeight;
      }
      this.ctxHeroi.clearRect(0, 0, cv.width, cv.height);
      this.ctxHeroi.drawImage(q.source.image, q.cutX, q.cutY, q.cutWidth, q.cutHeight, 0, 0, q.cutWidth, q.cutHeight);
      // tamanho na tela: altura fixa em px do desenho, largura na proporção do quadro
      const alt = (this.op.alturaHeroi || 80) * this.k;
      cv.style.height = `${alt}px`;
      cv.style.width = `${(alt * q.cutWidth) / q.cutHeight}px`;
    }
    const { x, y, virado } = this.heroiPos;
    const w = parseFloat(cv.style.width);
    const h = parseFloat(cv.style.height);
    const s = this.scrollDesenhado ?? this.scroll;
    cv.style.transform = `translate(${x * this.k - w / 2}px, ${(y - s) * this.k - h}px)${virado ? ' scaleX(-1)' : ''}`;
    // tamanho da faixa acompanha a escala
    const u = this.ultimaEscala;
    Object.assign(this.faixa.style, { top: `${8 * u}px`, fontSize: `${15 * u}px`, padding: `${2 * u}px ${8 * u}px`, borderWidth: `${1.5 * u}px`, borderRadius: `${4 * u}px` });
  }

  destruir() {
    this.scene.events.off('update', this.atualizar, this);
    const el = this.el;
    for (const tipo of this.paradores) el.removeEventListener(tipo, this.parar);
    el.removeEventListener('pointerdown', this.aoApertar);
    el.removeEventListener('pointermove', this.aoMover);
    el.removeEventListener('pointerup', this.aoSoltar);
    el.removeEventListener('pointercancel', this.aoSoltar);
    el.removeEventListener('wheel', this.aoRodar);
    el.remove();
  }
}
