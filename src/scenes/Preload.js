import * as Phaser from 'phaser';
import { LARGURA, ALTURA, TILE } from '../config.js';
import { SPRITES_PNG, CENARIO_PNG, TEM_LOGO, ArteJogador, ArteTiles, ArteObjetos, ArteEspaco, ArteTapete } from '../art/index.js';
import { texturaDeQuadros } from '../art/matriz.js';
import * as ArteChefe from '../art/chefe.js';

// Para testar uma cena direto pelo link (ex.: na prévia do Netlify): ?fase=itajuba, ?fase=espaco, ?fase=chefe,
// ?fase=tapete, ?fase=final... Sem o parâmetro, o jogo começa no Título.
const FASES = { titulo: 'Titulo', intro: 'Intro', itajuba: 'Itajuba', espaco: 'Espaco', chefe: 'Chefe', tapete: 'Tapete', final: 'Final' };
function faseInicial() {
  const pedida = new URLSearchParams(window.location.search).get('fase');
  return FASES[pedida] || 'Titulo';
}

// Prepara texturas e animações antes do jogo começar.
export class Preload extends Phaser.Scene {
  constructor() {
    super('Preload');
  }

  // Fase 3, Resgate: Jafar, projétil, gaiola e Tia Paula (art/chefe.js) e as animações deles.
  criarArteChefe() {
    for (const [nome, sp] of Object.entries(ArteChefe.SPRITES)) {
      texturaDeQuadros(this, nome, sp.quadros, ArteChefe.PALETA, sp.largura, sp.altura);
    }
    const anim = (key, textura, frames, frameRate, repeat = -1) =>
      this.anims.create({ key, frames: frames.map((frame) => ({ key: textura, frame })), frameRate, repeat });
    anim('jafar-flutuar', 'jafar', [0, 1], 3);
    anim('jafar-lancar', 'jafar', [2], 1);
    anim('jafar-tonto', 'jafar', [3], 1);
    anim('projetil-girar', 'projetil', [0, 1], 10);
    // Tia Paula: um sprite só para Chefe, Tapete e Final (public/assets/sprites/tiaPaula.png)
    anim('paula-presa', 'tiaPaula', [0, 1], 3);
    anim('paula-feliz', 'tiaPaula', [2, 3], 3);
    anim('paula-sentada', 'tiaPaula', [4], 1);
    anim('paula-microfone', 'tiaPaula', [5, 6], 2);
  }

  preload() {
    if (TEM_LOGO) this.load.image('logo', 'assets/logo.png');
    for (const [nome, q] of Object.entries(SPRITES_PNG)) {
      this.load.spritesheet(nome, `assets/sprites/${nome}.png`, { frameWidth: q.largura, frameHeight: q.altura });
    }
    for (const nome of CENARIO_PNG) this.load.image(nome, `assets/cenario/${nome}.png`);
  }

  create() {
    this.criarArteChefe();

    // Jogador: matriz -> textura (só se não veio PNG)
    const J = ArteJogador;
    texturaDeQuadros(this, 'jogador', J.ORDEM.map((n) => J.QUADROS[n]), J.PALETA, J.LARGURA, J.ALTURA);

    // Tiles: o 0 fica vazio (transparente)
    const T = ArteTiles;
    texturaDeQuadros(this, 'tiles', T.ORDEM.map((n) => T.TILES[n] || null), T.PALETA, TILE, TILE);

    // Objetos da Fase 1 (capivara, maçã, sapatilha, coração, bandeira)
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
    // animações do jogador definidas junto com a arte (src/art/jogador.js, gerado por gerar_jogador.py)
    for (const [nome, a] of Object.entries(ArteJogador.ANIMACOES)) anim(nome, quadros(...a.quadros), a.fps, a.repetir);

    const outra = (key, textura, frames, frameRate, repeat = -1) =>
      this.anims.create({ key, frames: frames.map((frame) => ({ key: textura, frame })), frameRate, repeat });
    outra('capivara-andar', 'capivara', [0, 1], 4);
    outra('capivara-comer', 'capivara', [2, 3], 5);
    outra('capivara-dormir', 'capivara', [4, 5], 1.5);
    outra('sapatilha-brilho', 'sapatilha', [0, 0, 0, 1], 4);
    // Fase 2
    outra('jasmine-ensaio', 'jasmine', [0, 0, 1, 2, 1], 2.5);
    outra('genio-ensaio', 'genio', [0, 0, 1], 2);
    outra('sultao-ensaio', 'sultao', [0, 1], 3);
    outra('claudia-ensaio', 'claudia', [0, 2], 1.5);
    outra('abu-parado', 'abu', [0], 1);
    outra('abu-correr', 'abu', [1, 2], 10);
    outra('abu-aflito', 'abu', [0, 3], 6); // pulando de aflição
    outra('balao-pensando', 'balao', [0, 1, 2], 3);
    anim('voo', [0, 1, 2].map((frame) => ({ key: 'voo', frame })), 8);
    anim('tucano', [0, 1].map((frame) => ({ key: 'tucano', frame })), 5);
    anim('maritaca', [0, 1].map((frame) => ({ key: 'maritaca', frame })), 9);
    anim('pipa', [0, 1].map((frame) => ({ key: 'pipa', frame })), 3);
  }
}
