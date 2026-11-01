import * as Phaser from 'phaser';
import { LARGURA, ALTURA, TILE, CORES, CORES_CSS, FONTES, TAPETE as CFG } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { Entrada } from '../ui/Entrada.js';
import { BotaoSom } from '../ui/BotaoSom.js';
import { tentarTelaCheia } from '../ui/telaCheia.js';
import { tocarEfeito } from '../audio/efeitos.js';
import { tocarMusica, tocarVinheta, pararMusica } from '../audio/musica.js';
import { TAPETE as MAPA } from '../levels/tapete.js';

// Fase 4 (CLAUDE.md, seção 11.6): Aladdin e Tia Paula voam de tapete sobre Itajubá ao entardecer.
// A câmera anda sozinha para a direita; o tapete fica sempre no mesmo x da tela e só sobe e desce.
// Segurar (qualquer lugar da tela, espaço, W ou seta para cima) sobe; soltar desce.
// Bater num pássaro, pipa, poste ou fio só pisca e perde sapatilhas: o voo nunca para.
//
// O movimento vertical é feito à mão (sem Arcade Physics): aceleração até uma velocidade máxima,
// com resposta mais forte quando a pessoa inverte o sentido. Os valores ficam em config.js (TAPETE).

const T = TEXTOS.tapete;
const CHAO_Y = 228; // linha dos telhados mais próximos
const LINHAS_MAPA = MAPA.length;
const LARGURA_MAPA = MAPA[0].length * TILE;
const TEATRO = { largura: 200, altura: 170 };

export class Tapete extends Phaser.Scene {
  constructor() {
    super('Tapete');
  }

  create() {
    tocarMusica('tapete'); // se o som ainda não foi liberado, começa no 1º toque
    this.estado = 'esperando'; // esperando → voando → chegando
    this.sapatilhas = this.registry.get('sapatilhas') ?? 0;
    this.registry.set('sapatilhas', this.sapatilhas);
    this.vy = 0;
    this.invencivelAte = 0;
    this.tempo = 0;
    this.fimRolagem = LARGURA_MAPA; // câmera para aqui: o teatro inteiro na tela
    this.teatroX = LARGURA_MAPA + LARGURA - TEATRO.largura - 16;

    this.criarTexturasCenario();
    this.criarFundo();
    this.criarObjetos();
    this.criarTeatro();

    // tapete com os passageiros
    this.tapete = this.add.sprite(CFG.xNaTela, 120, 'voo', 0).setDepth(50).play('voo');
    this.yTapete = 120;

    this.cameras.main.setBounds(0, 0, this.fimRolagem + LARGURA, ALTURA);
    this.entrada = new Entrada(this);
    this.entrada.setModoTapete(true);

    this.criarHud();
    this.criarTelaInicio();
    this.cameras.main.fadeIn(400, 158, 158, 255);
  }

  // ---------- cenário ----------

  // Cidade ao fundo e telhados perto: desenhados em canvas uma vez, depois só repetidos (tileSprite).
  criarTexturasCenario() {
    const sorteio = semente(7);
    if (!this.textures.exists('cidadeLonge')) {
      const w = LARGURA * 2;
      const tex = this.textures.createCanvas('cidadeLonge', w, 90);
      const ctx = tex.getContext();
      let x = 0;
      while (x < w) {
        const larg = 22 + Math.floor(sorteio() * 30);
        const alt = 24 + Math.floor(sorteio() * 34);
        ctx.fillStyle = '#A9779E';
        ctx.fillRect(x, 90 - alt, larg, alt);
        // janelas acesas (fim de tarde)
        ctx.fillStyle = '#F9E3A8';
        for (let jy = 90 - alt + 6; jy < 84; jy += 9) {
          for (let jx = x + 4; jx < x + larg - 4; jx += 7) if (sorteio() < 0.35) ctx.fillRect(jx, jy, 2, 3);
        }
        x += larg + Math.floor(sorteio() * 6);
      }
      // torre de igreja, para lembrar o centro de Itajubá (genérica: sem foto de referência ainda)
      ctx.fillStyle = '#A9779E';
      ctx.fillRect(300, 18, 18, 72);
      ctx.beginPath();
      ctx.moveTo(296, 20);
      ctx.lineTo(309, 2);
      ctx.lineTo(322, 20);
      ctx.fill();
      tex.refresh();
    }
    if (!this.textures.exists('telhados')) {
      const w = LARGURA;
      const h = ALTURA - CHAO_Y + 12;
      const tex = this.textures.createCanvas('telhados', w, h);
      const ctx = tex.getContext();
      const paredes = ['#E7B98A', '#F2D0A4', '#D99A74', '#EFC3B5'];
      let x = 0;
      while (x < w) {
        const larg = 40 + Math.floor(sorteio() * 40);
        const topo = 10 + Math.floor(sorteio() * 10);
        ctx.fillStyle = paredes[Math.floor(sorteio() * paredes.length)];
        ctx.fillRect(x, topo, larg, h - topo);
        // telhado de telha (terracota) com a borda escura
        ctx.fillStyle = '#B5563A';
        ctx.fillRect(x - 2, topo - 6, larg + 4, 7);
        ctx.fillStyle = '#7C3524';
        ctx.fillRect(x - 2, topo, larg + 4, 1);
        for (let tx = x; tx < x + larg; tx += 5) ctx.fillRect(tx, topo - 6, 1, 6);
        // janelas
        ctx.fillStyle = '#6D6BD9';
        for (let jx = x + 8; jx < x + larg - 10; jx += 16) ctx.fillRect(jx, topo + 10, 6, 8);
        x += larg;
      }
      tex.refresh();
    }
  }

  criarFundo() {
    this.add.image(0, 0, 'ceu').setOrigin(0).setScrollFactor(0);
    // sol que vai se pondo durante a fase (entardecer)
    this.sol = this.add.circle(LARGURA - 110, 70, 22, 0xfff1a8).setScrollFactor(0);
    this.brilhoSol = this.add.circle(LARGURA - 110, 70, 34, 0xfff1a8, 0.25).setScrollFactor(0);
    this.morros = this.add.tileSprite(0, 0, LARGURA, ALTURA, 'morros').setOrigin(0).setScrollFactor(0);
    this.cidade = this.add.tileSprite(0, CHAO_Y - 70, LARGURA, 90, 'cidadeLonge').setOrigin(0).setScrollFactor(0);
    this.telhados = this.add
      .tileSprite(0, CHAO_Y - 12, LARGURA, ALTURA - CHAO_Y + 12, 'telhados')
      .setOrigin(0)
      .setScrollFactor(0)
      .setDepth(40);
  }

  // Lê o mapa: sapatilhas, pássaros, pipas e postes com fio.
  criarObjetos() {
    this.coletaveis = [];
    this.passaros = [];
    this.pipas = [];
    this.postes = [];
    this.fios = [];
    const fiosG = this.add.graphics().setDepth(45);
    this.linhasPipa = this.add.graphics().setDepth(20);

    for (let lin = 0; lin < LINHAS_MAPA; lin++) {
      let posteAnterior = null;
      for (let col = 0; col < MAPA[lin].length; col++) {
        const c = MAPA[lin][col];
        const x = col * TILE + TILE / 2;
        const y = lin * TILE + TILE / 2;
        if (c === 's') {
          const s = this.add.image(x, y, 'sapatilhaCeu').setDepth(30);
          this.tweens.add({ targets: s, y: y - 3, duration: 600, yoyo: true, repeat: -1, ease: 'Sine.inOut', delay: (col * 70) % 600 });
          this.coletaveis.push(s);
        } else if (c === 'B') {
          const p = this.add.sprite(x, y, 'passaro').setDepth(35).play('passaro');
          p.baseY = y;
          p.fase = col;
          this.passaros.push(p);
        } else if (c === 'Q') {
          const p = this.add.sprite(x, y, 'pipa').setDepth(25).play('pipa');
          p.baseX = x;
          p.baseY = y;
          p.fase = col;
          this.pipas.push(p);
        } else if (c === 'f') {
          const poste = { x, topo: lin * TILE + 4 };
          this.postes.push(poste);
          if (posteAnterior) this.fios.push({ x1: posteAnterior.x, x2: x, y: posteAnterior.topo + 2, flecha: 10 });
          posteAnterior = poste;
        }
      }
    }

    // postes de madeira e fios (estáticos: desenhados uma vez)
    for (const p of this.postes) {
      fiosG.fillStyle(0x5a3a2a).fillRect(p.x - 3, p.topo, 6, ALTURA - p.topo);
      fiosG.fillStyle(0x7a4a2a).fillRect(p.x - 2, p.topo, 2, ALTURA - p.topo);
      fiosG.fillStyle(0x5a3a2a).fillRect(p.x - 8, p.topo + 2, 16, 3); // travessa
      fiosG.fillStyle(CORES.amarelo).fillRect(p.x - 7, p.topo, 2, 2).fillRect(p.x + 5, p.topo, 2, 2); // isoladores
    }
    for (const f of this.fios) {
      // fio caído no meio (curva), em dois traços para ficar visível sobre o céu
      for (const [dy, cor] of [[0, 0x2e1a33], [1, 0x4a3050]]) {
        fiosG.lineStyle(1, cor, 1).beginPath();
        for (let x = f.x1; x <= f.x2; x += 4) {
          const y = this.alturaFio(f, Math.min(x, f.x2)) + dy;
          x === f.x1 ? fiosG.moveTo(x, y) : fiosG.lineTo(x, y);
        }
        fiosG.lineTo(f.x2, f.y + dy).strokePath();
      }
      // passarinhos pintados no fio, só de enfeite
      const meio = (f.x1 + f.x2) / 2;
      fiosG.fillStyle(0x2e1a33).fillCircle(meio - 20, this.alturaFio(f, meio - 20) - 3, 2);
    }
  }

  alturaFio(f, x) {
    return f.y + f.flecha * Math.sin((Math.PI * (x - f.x1)) / (f.x2 - f.x1));
  }

  // Fachada do Teatro do Colégio G9 (provisória e genérica: falta foto de referência, ver CLAUDE.md seção 13).
  criarTeatro() {
    const { largura: w, altura: h } = TEATRO;
    const x0 = this.teatroX;
    const y0 = ALTURA - h;
    const g = this.add.graphics().setDepth(42);
    // prédio
    g.fillStyle(0xf2deb0).fillRect(x0, y0 + 26, w, h - 26);
    g.fillStyle(0xcdb386).fillRect(x0, y0 + 26, 6, h - 26);
    // frontão com a borda roxa
    g.fillStyle(CORES.roxo).fillRect(x0 - 6, y0 + 18, w + 12, 10);
    g.fillStyle(0xf2deb0).fillTriangle(x0 + 10, y0 + 18, x0 + w / 2, y0 - 6, x0 + w - 10, y0 + 18);
    g.lineStyle(2, CORES.roxo).strokeTriangle(x0 + 10, y0 + 18, x0 + w / 2, y0 - 6, x0 + w - 10, y0 + 18);
    // letreiro com luzinhas
    g.fillStyle(CORES.rosa).fillRect(x0 + 30, y0 + 34, w - 60, 30);
    g.lineStyle(2, CORES.roxo).strokeRect(x0 + 30, y0 + 34, w - 60, 30);
    this.luzes = [];
    for (let lx = x0 + 34; lx < x0 + w - 30; lx += 8) {
      this.luzes.push(this.add.circle(lx, y0 + 32, 1.5, CORES.amarelo).setDepth(43));
      this.luzes.push(this.add.circle(lx, y0 + 66, 1.5, CORES.amarelo).setDepth(43));
    }
    this.tweens.add({ targets: this.luzes, alpha: 0.3, duration: 400, yoyo: true, repeat: -1 });
    // colunas
    for (const cx of [x0 + 14, x0 + 44, x0 + w - 54, x0 + w - 24]) {
      g.fillStyle(0xfff6dc).fillRect(cx, y0 + 74, 10, h - 84);
      g.fillStyle(0xd9c8a0).fillRect(cx + 7, y0 + 74, 3, h - 84);
    }
    // porta com cortina lilás
    const px = x0 + w / 2 - 28;
    g.fillStyle(CORES.roxo).fillRect(px - 3, y0 + 84, 62, h - 94);
    g.fillStyle(CORES.lilas).fillRect(px, y0 + 87, 56, h - 97);
    g.fillStyle(0x7c7ce0).fillRect(px + 27, y0 + 87, 2, h - 97);
    // degraus
    g.fillStyle(0xcdb386).fillRect(x0 - 8, ALTURA - 10, w + 16, 10);
    g.fillStyle(0xe7d2a8).fillRect(x0 - 4, ALTURA - 14, w + 8, 4);

    const estilo = { fontFamily: FONTES.titulo, fontSize: '12px', color: CORES_CSS.roxo };
    this.add.text(x0 + w / 2, y0 + 44, T.teatro, estilo).setOrigin(0.5).setDepth(43);
    this.add
      .text(x0 + w / 2, y0 + 57, T.teatroNome, { ...estilo, fontSize: '7px' })
      .setOrigin(0.5)
      .setDepth(43);
    this.portaTeatro = { x: x0 + w / 2, y: ALTURA - 40 };
  }

  // ---------- HUD e início ----------

  criarHud() {
    this.add.image(18, 18, 'sapatilhaCeu').setScrollFactor(0).setDepth(900).setScale(1.5);
    this.textoSapatilhas = this.add
      .text(32, 12, String(this.sapatilhas), { fontFamily: FONTES.titulo, fontSize: '12px', color: CORES_CSS.branco })
      .setScrollFactor(0)
      .setDepth(900)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
    new BotaoSom(this, LARGURA - 20, 20);
  }

  criarTelaInicio() {
    const toque = this.sys.game.device.input.touch;
    const tela = this.add.container(0, 0).setScrollFactor(0).setDepth(2000);
    tela.add(this.add.rectangle(LARGURA / 2, 196, 380, 70, CORES.lilas, 0.9).setStrokeStyle(2, CORES.roxo));
    tela.add(
      this.add
        .text(LARGURA / 2, 176, T.titulo, { fontFamily: FONTES.titulo, fontSize: '10px', color: CORES_CSS.branco })
        .setOrigin(0.5)
        .setShadow(1, 1, CORES_CSS.roxo, 0, false, true),
    );
    tela.add(
      this.add
        .text(LARGURA / 2, 196, toque ? T.dicaToque : T.dicaTeclado, {
          fontFamily: FONTES.dialogo,
          fontSize: '14px',
          color: CORES_CSS.roxo,
          align: 'center',
          wordWrap: { width: 360 },
        })
        .setOrigin(0.5),
    );
    const aviso = this.add
      .text(LARGURA / 2, 216, toque ? T.comecarToque : T.comecarTeclado, {
        fontFamily: FONTES.titulo,
        fontSize: '8px',
        color: CORES_CSS.amarelo,
      })
      .setOrigin(0.5)
      .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
    tela.add(aviso);
    this.tweens.add({ targets: aviso, alpha: 0.35, duration: 500, yoyo: true, repeat: -1 });
    this.telaInicio = tela;

    // começa ao soltar o dedo (o navegador só aceita tela cheia no "pointerup") ou com espaço/W/seta
    const comecar = () => {
      if (this.estado !== 'esperando') return;
      tentarTelaCheia(this);
      tocarEfeito('botao');
      tela.destroy();
      this.estado = 'voando';
    };
    this.input.once('pointerup', comecar);
    this.input.keyboard?.once('keydown', comecar);
  }

  // ---------- jogo ----------

  update(agora, delta) {
    const dt = Math.min(delta, 50) / 1000; // evita "pulo" grande depois de um engasgo
    this.tempo += dt;
    const cam = this.cameras.main;
    this.entrada.atualizar();

    if (this.estado === 'voando') {
      cam.scrollX = Math.min(cam.scrollX + CFG.velocidadeRolagem * dt, this.fimRolagem);
      this.moverTapete(dt);
      this.tapete.x = cam.scrollX + CFG.xNaTela;
      this.verificarColisoes(agora);
      if (cam.scrollX >= this.fimRolagem) this.chegar();
    } else if (this.estado === 'esperando') {
      this.tapete.x = cam.scrollX + CFG.xNaTela;
    }

    // tapete: balanço leve por cima da posição "de verdade" e inclinação conforme sobe/desce
    if (this.estado !== 'chegando') {
      this.tapete.y = this.yTapete + Math.sin(this.tempo * 3) * 1.5;
      const alvoRot = this.vy * CFG.inclinacao;
      this.tapete.rotation += (alvoRot - this.tapete.rotation) * Math.min(1, dt * 10);
    }

    this.animarObjetos(dt, cam);

    // parallax e o sol baixando aos poucos
    const progresso = cam.scrollX / this.fimRolagem;
    this.morros.tilePositionX = cam.scrollX * 0.15;
    this.cidade.tilePositionX = cam.scrollX * 0.35;
    this.telhados.tilePositionX = cam.scrollX;
    this.sol.y = this.brilhoSol.y = 70 + progresso * 90;
  }

  moverTapete(dt) {
    const sobe = this.entrada.segurando;
    let a = sobe ? -CFG.aceleracaoSubida : CFG.aceleracaoDescida;
    // inverteu o sentido: acelera mais forte, para a resposta parecer imediata
    if (this.vy !== 0 && Math.sign(this.vy) !== Math.sign(a)) a *= CFG.multiplicadorVirada;
    this.vy = Phaser.Math.Clamp(this.vy + a * dt, -CFG.velMaxSubida, CFG.velMaxDescida);
    this.yTapete += this.vy * dt;
    if (this.yTapete < CFG.yMin) {
      this.yTapete = CFG.yMin;
      this.vy = Math.max(this.vy, 0);
    } else if (this.yTapete > CFG.yMax) {
      // no limite de baixo o tapete só desliza sobre os telhados (sem dano)
      this.yTapete = CFG.yMax;
      this.vy = Math.min(this.vy, 0);
    }
  }

  animarObjetos(dt, cam) {
    const visivel = (x) => x > cam.scrollX - 60 && x < cam.scrollX + LARGURA + 60;
    for (const p of this.passaros) {
      if (!visivel(p.x)) continue;
      if (p.fugindo) {
        p.x += 60 * dt;
        p.y -= 90 * dt;
      } else {
        p.x -= CFG.passaroVelocidade * dt;
        p.y = p.baseY + Math.sin(this.tempo * 3 + p.fase) * CFG.passaroOnda;
      }
    }
    // pipas balançam; a linha vai até o chão (só enfeite)
    this.linhasPipa.clear().lineStyle(1, 0xffffff, 0.7);
    for (const p of this.pipas) {
      if (!visivel(p.x)) continue;
      p.x = p.baseX + Math.sin(this.tempo * 1.7 + p.fase) * 6;
      p.y = p.baseY + Math.sin(this.tempo * 2.3 + p.fase) * 4;
      p.rotation = Math.sin(this.tempo * 1.7 + p.fase) * 0.12;
      this.linhasPipa.lineBetween(p.x, p.y + 2, p.x - 120, ALTURA);
    }
  }

  // Caixa de colisão do tapete (menor que o desenho, para ser justo).
  caixaTapete() {
    const c = CFG.corpo;
    return new Phaser.Geom.Rectangle(this.tapete.x - c.largura / 2, this.yTapete - c.altura / 2 + c.dy, c.largura, c.altura);
  }

  verificarColisoes(agora) {
    const caixa = this.caixaTapete();
    const R = Phaser.Geom.Rectangle;

    // sapatilhas: área um pouco maior, fácil de pegar
    const caixaColeta = new R(caixa.x - 6, caixa.y - 8, caixa.width + 12, caixa.height + 16);
    for (const s of this.coletaveis) {
      if (s.active && R.Contains(caixaColeta, s.x, s.y)) this.coletar(s);
    }

    if (agora < this.invencivelAte) return;
    for (const p of this.passaros) {
      if (!p.fugindo && R.Overlaps(caixa, new R(p.x - 6, p.y - 4, 12, 8))) return this.bater(agora, p);
    }
    for (const p of this.pipas) {
      if (R.Overlaps(caixa, new R(p.x - 6, p.y - 12, 12, 16))) return this.bater(agora);
    }
    for (const p of this.postes) {
      if (R.Overlaps(caixa, new R(p.x - 3, p.topo, 6, ALTURA - p.topo))) return this.bater(agora);
    }
    for (const f of this.fios) {
      const xi = Math.max(caixa.x, f.x1);
      const xf = Math.min(caixa.right, f.x2);
      for (let x = xi; x <= xf; x += 4) {
        const y = this.alturaFio(f, x);
        if (y >= caixa.y && y <= caixa.bottom) return this.bater(agora);
      }
    }
  }

  coletar(s) {
    s.active = false;
    this.tweens.killTweensOf(s);
    this.tweens.add({ targets: s, y: s.y - 14, alpha: 0, scale: 1.6, duration: 250, onComplete: () => s.destroy() });
    this.sapatilhas++;
    this.registry.set('sapatilhas', this.sapatilhas);
    this.textoSapatilhas.setText(String(this.sapatilhas));
    tocarEfeito('sapatilha', { variar: 0.08 });
  }

  // Batida: pisca, perde algumas sapatilhas e segue voando.
  bater(agora, passaro) {
    this.invencivelAte = agora + CFG.invencivelMs;
    if (passaro) passaro.fugindo = true;
    const perdidas = Math.min(CFG.sapatilhasPerdidas, this.sapatilhas);
    this.sapatilhas -= perdidas;
    this.registry.set('sapatilhas', this.sapatilhas);
    this.textoSapatilhas.setText(String(this.sapatilhas));

    this.tweens.add({
      targets: this.tapete,
      alpha: 0.25,
      duration: 100,
      yoyo: true,
      repeat: Math.floor(CFG.invencivelMs / 200) - 1,
      onComplete: () => this.tapete.setAlpha(1),
    });
    this.cameras.main.shake(120, 0.004);
    tocarEfeito('dano');

    // sapatilhas perdidas caem do tapete
    for (let i = 0; i < perdidas; i++) {
      const s = this.add.image(this.tapete.x, this.yTapete, 'sapatilhaCeu').setDepth(60);
      this.tweens.add({
        targets: s,
        x: s.x - 20 - i * 16,
        y: ALTURA + 10,
        angle: 200,
        duration: 900,
        ease: 'Quad.in',
        onComplete: () => s.destroy(),
      });
    }
    if (perdidas > 0) {
      const txt = this.add
        .text(this.tapete.x, this.yTapete - 30, T.perdeu.replace('{n}', perdidas), {
          fontFamily: FONTES.titulo,
          fontSize: '10px',
          color: CORES_CSS.rosa,
        })
        .setOrigin(0.5)
        .setDepth(901)
        .setShadow(1, 1, CORES_CSS.roxo, 0, false, true);
      this.tweens.add({ targets: txt, y: txt.y - 20, alpha: 0, duration: 800, onComplete: () => txt.destroy() });
    }
  }

  // Fim: o tapete pousa na porta do teatro e a cena final começa.
  chegar() {
    this.estado = 'chegando';
    this.tweens.killTweensOf(this.tapete);
    this.tapete.setAlpha(1);
    this.tweens.add({
      targets: this.tapete,
      x: this.portaTeatro.x,
      y: this.portaTeatro.y,
      rotation: 0,
      duration: CFG.pousoMs,
      ease: 'Sine.inOut',
      onComplete: () => this.mostrarChegada(),
    });
  }

  mostrarChegada() {
    pararMusica(0.3);
    tocarVinheta('vitoria');
    const caixa = this.add.container(LARGURA / 2, 60).setScrollFactor(0).setDepth(2000);
    caixa.add(this.add.rectangle(0, 0, 300, 40, CORES.lilas, 0.95).setStrokeStyle(2, CORES.roxo));
    caixa.add(
      this.add.text(0, 0, T.chegou, { fontFamily: FONTES.dialogo, fontSize: '18px', color: CORES_CSS.roxo }).setOrigin(0.5),
    );
    caixa.setScale(0);
    this.tweens.add({ targets: caixa, scale: 1, duration: 300, ease: 'Back.out' });
    this.time.delayedCall(CFG.esperaFinalMs, () => {
      this.cameras.main.fadeOut(500, 158, 158, 255);
      this.cameras.main.once('camerafadeoutcomplete', () => this.scene.start('Final', { sapatilhas: this.sapatilhas }));
    });
  }
}

// Sorteio com semente: o cenário sai sempre igual.
function semente(s) {
  return () => {
    s = (s * 16807) % 2147483647;
    return (s - 1) / 2147483646;
  };
}
