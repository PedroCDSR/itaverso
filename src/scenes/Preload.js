import * as Phaser from 'phaser';
import { LARGURA, ALTURA, TILE } from '../config.js';
import { SPRITES_PNG, TEM_LOGO, ArteJogador, ArteTiles, ArteObjetos, ArteTapete } from '../art/index.js';
import { texturaDeQuadros } from '../art/matriz.js';

// Para testar uma cena direto pelo link (ex.: na prévia do Netlify): ?fase=itajuba, ?fase=tapete, ?fase=final...
// Sem o parâmetro, o jogo começa no Título.
const FASES = { titulo: 'Titulo', intro: 'Intro', itajuba: 'Itajuba', tapete: 'Tapete', final: 'Final' };
function faseInicial() {
  const pedida = new URLSearchParams(window.location.search).get('fase');
  return FASES[pedida] || 'Titulo';
}

// Prepara texturas e animações antes do jogo começar.
export class Preload extends Phaser.Scene {
  constructor() {
    super('Preload');
  }

  preload() {
    if (TEM_LOGO) this.load.image('logo', 'assets/logo.png');
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

    // Fase 4 (Tapete): tapete com passageiros, pássaro, pipa e sapatilha
    for (const [nome, sp] of Object.entries(ArteTapete.SPRITES)) {
      texturaDeQuadros(this, nome, sp.quadros, ArteTapete.PALETA, sp.largura, sp.altura);
    }

    this.criarAnimacoes();
    this.criarCeu();
    this.criarCasas();
    this.scene.start(faseInicial());
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
