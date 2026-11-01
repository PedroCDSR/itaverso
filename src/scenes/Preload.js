import * as Phaser from 'phaser';
import { LARGURA, ALTURA, TILE } from '../config.js';
import { SPRITES_PNG, ArteJogador, ArteTiles } from '../art/index.js';
import { texturaDeQuadros } from '../art/matriz.js';

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

    this.criarAnimacoes();
    this.criarCeu();
    this.scene.start('Teste');
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
