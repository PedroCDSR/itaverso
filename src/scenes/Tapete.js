import * as Phaser from 'phaser';
import { LARGURA, ALTURA, TILE, CORES, CORES_CSS, FONTES, TAPETE as CFG } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { Entrada } from '../ui/Entrada.js';
import { BotaoSom } from '../ui/BotaoSom.js';
import { BotaoPausa } from '../ui/BotaoPausa.js';
import { abrirPausa } from '../fluxo.js';
import { tocarEfeito } from '../audio/efeitos.js';
import { tocarMusica, tocarVinheta, pararMusica } from '../audio/musica.js';
import { TAPETE as MAPA } from '../levels/tapete.js';
import { ONDA_ALADDIN, ONDA_PAULA } from '../art/tapete.js';

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

    this.criarFundo();
    this.criarObjetos();
    this.criarTeatro();

    // tapete com os passageiros
    // O tapete é um container: tapete + Tia Paula (textura "voo") e, por cima, o Aladdin sentado, que é o quadro
    // "sentado" do MESMO sprite do jogador (fonte única). Ele balança junto com a onda do tapete.
    this.tapeteVoo = this.add.sprite(0, 0, 'voo', 0).play('voo');
    this.aladdinSentado = this.add.sprite(CFG.aladdin.x, CFG.aladdin.y, 'jogador').setOrigin(0.5, 1).play('sentado');
    // Tia Paula sentada atrás dele: quadro "sentada" do sprite único dela (public/assets/sprites/tiaPaula.png)
    this.paulaSentada = this.add.sprite(-14, 20, 'tiaPaula', 4).setOrigin(0.5, 1);
    this.tapeteVoo.on('animationupdate', (anim, quadro) => {
      this.aladdinSentado.y = CFG.aladdin.y + ONDA_ALADDIN[quadro.index - 1];
      this.paulaSentada.y = 20 + ONDA_PAULA[quadro.index - 1];
    });
    this.tapete = this.add.container(CFG.xNaTela, 120, [this.tapeteVoo, this.paulaSentada, this.aladdinSentado]).setDepth(50);
    this.yTapete = 120;

    this.cameras.main.setBounds(0, 0, this.fimRolagem + LARGURA, ALTURA);
    this.entrada = new Entrada(this);
    this.entrada.setModoTapete(true);

    this.criarHud();
    this.criarTelaInicio();
    this.cameras.main.fadeIn(400, 158, 158, 255);
  }

  // ---------- cenário ----------

  criarFundo() {
    // Crepúsculo (decisão do Pedro): o sol já se pôs depois do resgate; estrelas, horizonte laranja e janelas
    // acendendo. Camadas em PNG (ferramentas/arte/gerar_cenarios.py): céu parado, Serra da Mantiqueira, cidade
    // com prédios, Hotel Coroados no alto do morro, UNIFEI e telhados de perto.
    this.add.image(0, 0, 'ceu-crepusculo').setOrigin(0).setScrollFactor(0);
    this.morros = this.add.tileSprite(0, 0, LARGURA, ALTURA, 'serra-crepusculo').setOrigin(0).setScrollFactor(0);
    // Hotel Coroados: aparece por volta dos 12 s de voo (camada do meio, parallax 0,35)
    this.add.image(640, ALTURA + 30, 'coroados').setOrigin(0, 1).setScrollFactor(0.35);
    this.cidade = this.add.tileSprite(0, 0, LARGURA, ALTURA, 'cidade-crepusculo').setOrigin(0).setScrollFactor(0);
    // UNIFEI: por volta dos 25 s (camada de perto, parallax 0,6, atrás dos telhados)
    this.add.image(1700, ALTURA + 4, 'unifei').setOrigin(0, 1).setScrollFactor(0.6).setDepth(39);
    this.telhados = this.add.tileSprite(0, 0, LARGURA, ALTURA, 'telhados-crepusculo').setOrigin(0).setScrollFactor(0).setDepth(40);
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
          // tucanos e maritacas (Pedro): alterna pelo número da coluna
          const ave = col % 2 ? 'maritaca' : 'tucano';
          const p = this.add.sprite(x, y, ave).setDepth(35).play(ave);
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
    this.botaoSom = new BotaoSom(this, LARGURA - 20, 20);
    // pausa (Etapa 7): botão ao lado do som, Esc ou P
    new BotaoPausa(this, LARGURA - 56, 20, () => abrirPausa(this));
    this.input.keyboard?.on('keydown-ESC', () => abrirPausa(this));
    this.input.keyboard?.on('keydown-P', () => abrirPausa(this));
    this.events.on('resume', () => {
      this.botaoSom.desenhar();
      this.input.keyboard?.resetKeys();
    });
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

    // começa ao soltar o dedo ou com uma tecla
    const comecar = () => {
      if (this.estado !== 'esperando') return;
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

    // parallax
    this.morros.tilePositionX = cam.scrollX * 0.15;
    this.cidade.tilePositionX = cam.scrollX * 0.35;
    this.telhados.tilePositionX = cam.scrollX;
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
      if (!p.fugindo && R.Overlaps(caixa, new R(p.x - 8, p.y - 5, 16, 10))) return this.bater(agora, p);
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
