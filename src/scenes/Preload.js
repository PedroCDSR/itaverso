import * as Phaser from 'phaser';
import { LARGURA, ALTURA, TILE } from '../config.js';
import { SPRITES_PNG, ArteJogador, ArteTiles, ArteObjetos, ArteEspaco, ArteTapete } from '../art/index.js';
import { texturaDeQuadros } from '../art/matriz.js';

// Para testar uma fase direto pelo link: ?fase=espaco abre a Fase 2, ?fase=tapete a Fase 4 (ex.: na prévia do Netlify).
const FASES = { espaco: 'Espaco', chefe: 'Chefe', tapete: 'Tapete', final: 'Final' };
function faseInicial() {
  const pedida = new URLSearchParams(window.location.search).get('fase');
  return FASES[pedida] || 'Itajuba';
}

// Prepara texturas e animações antes do jogo começar.
export class Preload extends Phaser.Scene {
  constructor() {
    super('Preload');
  }

  preload() {
    for (const [nome, q] of Object.entries(SPRITES_PNG)) {
      this.load.spritesheet(nome, `assets/sprites/${nome}.png`, { frameWidth: q.largura, frameHeight: q.altura });
    }
  }

  create() {
    // Jogador: matriz -> textura (só se não veio PNG)
    const J = ArteJogador;
    texturaDeQuadros(this, 'jogador', J.ORDEM.map((n) => J.QUADROS[n]), J.PALETA, J.LARGURA, J.ALTURA);

    // Tiles: o 0 fica vazio (transparente)
    const T = ArteTiles;
    texturaDeQuadros(this, 'tiles', T.ORDEM.map((n) => T.TILES[n] || null), T.PALETA, TILE, TILE);

    // Objetos da Fase 1 (capivara, maçã, sapatilha, coração, fonte, bandeira)
    for (const [nome, sp] of Object.entries(ArteObjetos.SPRITES)) {
      texturaDeQuadros(this, nome, sp.quadros, ArteObjetos.PALETA, sp.largura, sp.altura);
    }

    // Fase 2: tiles do estúdio (mesma ORDEM de tiles.js) e personagens
    texturaDeQuadros(this, 'tiles-espaco', T.ORDEM.map((n) => ArteEspaco.TILES[n] || null), ArteEspaco.PALETA, TILE, TILE);
    for (const [nome, sp] of Object.entries(ArteEspaco.SPRITES)) {
      texturaDeQuadros(this, nome, sp.quadros, ArteEspaco.PALETA, sp.largura, sp.altura);
    }

    // Fase 4 (Tapete): tapete com passageiros, pássaro, pipa e sapatilha
    for (const [nome, sp] of Object.entries(ArteTapete.SPRITES)) {
      texturaDeQuadros(this, nome, sp.quadros, ArteTapete.PALETA, sp.largura, sp.altura);
    }

    this.criarAnimacoes();
    this.criarCeu();
    this.criarCasas();
    this.criarEstudio();
    this.scene.start(faseInicial());
  }

  // Parede do estúdio (Fase 2): espelhos grandes com barra de balé na frente, entre pilares lilás.
  // Faixa de 240 px que se repete ao longo da fase; o piso de madeira são os tiles.
  criarEstudio() {
    if (this.textures.exists('estudio')) return;
    const w = 240;
    const tex = this.textures.createCanvas('estudio', w, ALTURA);
    const ctx = tex.getContext();
    const ret = (x, y, ww, hh, cor) => {
      ctx.fillStyle = cor;
      ctx.fillRect(x, y, ww, hh);
    };
    const piso = 240; // topo do piso (linha 15 do mapa)
    // parede rosa clarinho, faixa lilás no alto e rodapé
    ret(0, 0, w, ALTURA, '#F6DDF3');
    ret(0, 0, w, 22, '#C9C3FF');
    ret(0, 22, w, 3, '#9E9EFF');
    ret(0, piso - 6, w, 6, '#D57FCF');
    // luzinhas de teto
    for (const x of [60, 180]) {
      ret(x - 10, 25, 20, 4, '#6D6BD9');
      ret(x - 6, 29, 12, 3, '#F9FCBB');
    }
    // pilar lilás entre os espelhos
    ret(0, 25, 14, piso - 31, '#B9B4FF');
    ret(10, 25, 4, piso - 31, '#9E9EFF');
    // espelho (moldura roxa, vidro azulado com reflexos diagonais)
    const ex = 22;
    const ey = 70;
    const ew = w - 30;
    const eh = piso - 6 - ey;
    ret(ex - 3, ey - 3, ew + 6, eh + 3, '#6D6BD9');
    const g = ctx.createLinearGradient(0, ey, 0, ey + eh);
    g.addColorStop(0, '#DCEBFA');
    g.addColorStop(1, '#BFD3F0');
    ctx.fillStyle = g;
    ctx.fillRect(ex, ey, ew, eh);
    ctx.fillStyle = 'rgba(255,255,255,0.55)';
    for (const [x0, larg] of [[30, 10], [48, 4], [130, 14], [152, 5]]) {
      ctx.beginPath();
      ctx.moveTo(ex + x0, ey + eh);
      ctx.lineTo(ex + x0 + larg, ey + eh);
      ctx.lineTo(ex + x0 + larg + 60, ey);
      ctx.lineTo(ex + x0 + 60, ey);
      ctx.fill();
    }
    ret(ex + ew / 2 - 1, ey, 2, eh, '#A9BEE0'); // emenda entre as placas
    // barra de balé (madeira) com suportes, na altura da cintura
    const by = piso - 26;
    for (const x of [ex + 16, ex + ew / 2, ex + ew - 18]) {
      ret(x - 1, by, 3, 12, '#6D6BD9');
    }
    ret(ex - 6, by - 3, ew + 12, 5, '#2E1A33');
    ret(ex - 5, by - 2, ew + 10, 3, '#C98B52');
    ret(ex - 5, by - 2, ew + 10, 1, '#E3B07A');
    tex.refresh();
  }

  criarAnimacoes() {
    const i = (nome) => ArteJogador.ORDEM.indexOf(nome);
    const quadros = (...nomes) => nomes.map((n) => ({ key: 'jogador', frame: i(n) }));
    const anim = (key, frames, frameRate, repeat = -1) => this.anims.create({ key, frames, frameRate, repeat });
    anim('parado', quadros('parado1', 'parado2'), 2);
    anim('correndo', quadros('correndo1', 'correndo2', 'correndo3', 'correndo4', 'correndo5', 'correndo6'), 12);
    anim('pulando', quadros('pulando'), 1);
    anim('caindo', quadros('caindo'), 1);
    anim('arremessando', quadros('arremessando1', 'arremessando2'), 14, 0);
    anim('dano', quadros('dano'), 1);

    const outra = (key, textura, frames, frameRate, repeat = -1) =>
      this.anims.create({ key, frames: frames.map((frame) => ({ key: textura, frame })), frameRate, repeat });
    outra('capivara-andar', 'capivara', [0, 1], 4);
    outra('capivara-comer', 'capivara', [2, 3], 5);
    outra('capivara-dormir', 'capivara', [4, 5], 1.5);
    outra('sapatilha-brilho', 'sapatilha', [0, 0, 0, 1], 4);
    outra('fonte-agua', 'fonte', [0, 1], 4);
    // Fase 2
    outra('jasmine-ensaio', 'jasmine', [0, 1], 1.5);
    outra('genio-ensaio', 'genio', [0, 0, 1], 2);
    outra('sultao-ensaio', 'sultao', [0, 1], 3);
    outra('claudia-ensaio', 'claudia', [0], 1);
    outra('abu-parado', 'abu', [0], 1);
    outra('abu-correr', 'abu', [1, 2], 10);
    outra('abu-aflito', 'abu', [0, 3], 6); // pulando de aflição
    outra('balao-pensando', 'balao', [0, 1, 2], 3);
    anim('voo', [0, 1, 2].map((frame) => ({ key: 'voo', frame })), 8);
    anim('passaro', [0, 1].map((frame) => ({ key: 'passaro', frame })), 6);
    anim('pipa', [0, 1].map((frame) => ({ key: 'pipa', frame })), 3);
  }

  // Casario de Itajubá ao fundo (camada do meio do parallax): sobrados coloniais coloridos, telhado de barro e a
  // torre de uma igreja. Faixa de 2 telas que se repete; o pé das casas fica escondido atrás do chão.
  criarCasas() {
    if (this.textures.exists('casas')) return;
    const w = LARGURA * 2;
    const tex = this.textures.createCanvas('casas', w, ALTURA);
    const ctx = tex.getContext();
    const base = 244; // um pouco abaixo do topo do chão (linha 15 do mapa = 240 px)
    const paredes = ['#F3E3C3', '#F6D7A8', '#EFC2C9', '#CFE0E8', '#E8B48A', '#F2EAD8', '#D8C8F0'];
    const ret = (x, y, ww, hh, cor) => {
      ctx.fillStyle = cor;
      ctx.fillRect(Math.round(x), Math.round(y), Math.round(ww), Math.round(hh));
    };
    // torre da igreja (fica atrás das casas)
    const tx = 560;
    ret(tx, 120, 26, base - 120, '#EDE4D3');
    ret(tx + 20, 120, 6, base - 120, '#CFC3AE');
    ret(tx + 9, 134, 8, 12, '#6D6BD9');
    ctx.fillStyle = '#B5583A';
    ctx.beginPath();
    ctx.moveTo(tx - 3, 121);
    ctx.lineTo(tx + 13, 96);
    ctx.lineTo(tx + 29, 121);
    ctx.fill();
    ret(tx + 12, 86, 2, 10, '#2E1A33');
    ret(tx + 9, 89, 8, 2, '#2E1A33');

    let x = 0;
    let i = 0;
    while (x < w) {
      const larg = [56, 72, 48, 64, 80][i % 5];
      const alt = [58, 74, 50, 66, 82][(i * 3) % 5];
      const topo = base - alt;
      const parede = paredes[i % paredes.length];
      ret(x, topo, larg, alt, parede);
      ret(x + larg - 5, topo, 5, alt, 'rgba(46,26,51,0.12)'); // sombra lateral
      // barra colorida embaixo e beiral
      ret(x, base - 14, larg, 14, 'rgba(46,26,51,0.10)');
      // telhado de barro
      ctx.fillStyle = '#B5583A';
      ctx.beginPath();
      ctx.moveTo(x - 3, topo + 1);
      ctx.lineTo(x + 8, topo - 12);
      ctx.lineTo(x + larg - 8, topo - 12);
      ctx.lineTo(x + larg + 3, topo + 1);
      ctx.fill();
      for (let tx2 = x + 2; tx2 < x + larg; tx2 += 5) ret(tx2, topo - 10, 1, 10, 'rgba(46,26,51,0.18)');
      ret(x - 3, topo, larg + 6, 2, '#8A3E28');
      // janelas com moldura (2 andares quando a casa é alta)
      const andares = alt > 64 ? 2 : 1;
      const cols = Math.max(2, Math.floor(larg / 22));
      for (let a = 0; a < andares; a++) {
        for (let c = 0; c < cols; c++) {
          const jx = x + ((c + 0.5) * larg) / cols - 5;
          const jy = topo + 12 + a * 28;
          ret(jx - 1, jy - 1, 12, 17, '#FFFFFF');
          ret(jx, jy, 10, 15, a === 0 && andares === 2 ? '#7FA9C9' : '#6E8FB0');
          ret(jx + 4, jy, 2, 15, '#FFFFFF');
        }
      }
      // porta
      ret(x + larg / 2 - 6, base - 26, 12, 24, '#7C4128');
      ret(x + larg / 2 - 6, base - 26, 12, 2, '#5A2E1C');
      x += larg + 6 + ((i * 7) % 3) * 4;
      i++;
    }
    tex.refresh();
  }

  // Céu de fim de tarde e morros ao fundo (versão simples; o parallax completo vem na Etapa 8).
  criarCeu() {
    if (!this.textures.exists('ceu')) {
      const tex = this.textures.createCanvas('ceu', LARGURA, ALTURA);
      const ctx = tex.getContext();
      const g = ctx.createLinearGradient(0, 0, 0, ALTURA);
      g.addColorStop(0, '#9E9EFF'); // lilás da escola no alto
      g.addColorStop(0.55, '#E9A6D8'); // rosa do entardecer
      g.addColorStop(1, '#F7C99A'); // pêssego perto do horizonte
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, LARGURA, ALTURA);
      tex.refresh();
    }
    if (!this.textures.exists('morros')) {
      // faixa de morros que se repete na horizontal (largura = 2 telas)
      const w = LARGURA * 2;
      const tex = this.textures.createCanvas('morros', w, ALTURA);
      const ctx = tex.getContext();
      const camada = (cor, base, amp, freqs) => {
        ctx.fillStyle = cor;
        ctx.beginPath();
        ctx.moveTo(0, ALTURA);
        for (let x = 0; x <= w; x++) {
          // soma de senos com período que fecha em w, para a emenda não aparecer
          const y = base - freqs.reduce((s, [f, a, fase]) => s + a * Math.sin((x / w) * Math.PI * 2 * f + fase), 0) * amp;
          ctx.lineTo(x, Math.round(y));
        }
        ctx.lineTo(w, ALTURA);
        ctx.closePath();
        ctx.fill();
      };
      camada('#B98BC9', 150, 18, [[2, 1, 0], [5, 0.4, 1]]);
      camada('#8F6FB3', 180, 14, [[3, 1, 2], [7, 0.3, 0.5]]);
      tex.refresh();
    }
  }
}
