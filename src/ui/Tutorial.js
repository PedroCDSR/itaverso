import { LARGURA, CORES, CORES_CSS, FONTES, CONTROLES } from '../config.js';
import { TEXTOS } from '../data/textos.js';

// Tutorial do começo da Fase 1 (pedido do Pedro, 01/11/2026): quem joga pode nunca ter jogado nada.
// Passo a passo, com uma seta pulando em cima do controle certo:
//   1. andar (◀ ▶ ou setas)  2. pular (PULAR ou espaço)  3. maçã (MAÇÃ ou X)
//   4. quando a 1ª capivara aparece: "pule em cima dela para ela dormir", com a seta em cima da capivara.
// Cada passo some quando a pessoa faz a ação (ou depois de um tempo, para ninguém ficar travado).
// No celular a seta aponta para o botão na tela; no computador, o texto mostra as teclas.
// Quem já viu (JOGAR DE NOVO) não vê de novo: flag `tutorialVisto` no registry.
export class Tutorial {
  constructor(scene, { entrada, jogador, capivaras }) {
    this.scene = scene;
    this.entrada = entrada;
    this.jogador = jogador;
    this.capivaras = capivaras;
    this.toque = scene.sys.game.device.input.touch;
    this.t = TEXTOS.tutorial;
    this.passo = 0;
    this.acabou = scene.registry.get('tutorialVisto') === true;
    this.capivaraFeita = this.acabou;
    this.andou = 0;

    // balão de texto (fixo na tela) e seta (fixa na tela ou no mundo, conforme o passo)
    this.balao = scene.add.container(0, 0).setScrollFactor(0).setDepth(1600).setVisible(false);
    this.balaoFundo = scene.add.rectangle(0, 0, 10, 10, CORES.branco).setStrokeStyle(2, CORES.roxo);
    this.balaoTexto = scene.add
      .text(0, 1, '', { fontFamily: FONTES.dialogo, fontSize: '16px', color: CORES_CSS.roxo, align: 'center' })
      .setOrigin(0.5);
    this.balao.add([this.balaoFundo, this.balaoTexto]);
    // duas setas (andar aponta para ◀ e para ▶ ao mesmo tempo); os outros passos usam só a primeira
    this.setas = [0, 1].map(() => {
      const seta = scene.add.container(0, 0).setDepth(1600).setVisible(false);
      // seta apontando para baixo (triângulo + haste), rosa com borda roxa
      const g = scene.add.graphics();
      g.fillStyle(CORES.roxo).fillTriangle(-11, -2, 11, -2, 0, 13).fillRect(-5, -16, 10, 15);
      g.fillStyle(CORES.rosa).fillTriangle(-8, 0, 8, 0, 0, 10).fillRect(-3, -14, 6, 15);
      seta.add(g);
      return seta;
    });
    this.alvos = [];
    this.balanco = 0;
  }

  // Chamar quando a fase começa de verdade (depois da faixa do objetivo).
  iniciar() {
    if (this.acabou) return;
    this.scene.time.delayedCall(2300, () => this.irPara(1));
  }

  irPara(n) {
    this.passo = n;
    this.inicioPasso = this.scene.time.now;
    const t = this.t;
    if (n === 1) this.mostrar(this.toque ? t.andarToque : t.andarTeclado, this.alvoBotao('esquerda', 'direita'));
    else if (n === 2) this.mostrar(this.toque ? t.pularToque : t.pularTeclado, this.alvoBotao('pular'));
    else if (n === 3) this.mostrar(this.toque ? t.macaToque : t.macaTeclado, this.alvoBotao('maca'));
    else this.esconder();
  }

  // Pontos (na tela) logo acima de cada botão. No computador não há botões: as setas ficam escondidas.
  alvoBotao(...nomes) {
    if (!this.toque) return [];
    return nomes.map((n) => ({ x: CONTROLES[n].x, y: CONTROLES[n].y - CONTROLES[n].raio - 6, tela: true }));
  }

  mostrar(texto, alvos) {
    this.balaoTexto.setText(texto);
    const w = this.balaoTexto.width + 18;
    const h = this.balaoTexto.height + 10;
    this.balaoFundo.setSize(w, h);
    this.balaoFundo.setDisplaySize(w, h);
    // o balão fica perto da seta, mas sempre inteiro dentro da tela
    const cx = alvos.length ? alvos.reduce((s, a) => s + a.x, 0) / alvos.length : LARGURA / 2;
    const bx = Math.max(w / 2 + 6, Math.min(LARGURA - w / 2 - 6, cx));
    const by = alvos.length && alvos[0].tela ? alvos[0].y - 34 - h / 2 : 112;
    this.balao.setPosition(bx, by).setVisible(true).setAlpha(0);
    this.scene.tweens.add({ targets: this.balao, alpha: 1, duration: 200 });
    this.alvos = alvos;
    this.setas.forEach((seta, i) => {
      seta.setVisible(!!alvos[i]);
      if (alvos[i]) seta.setScrollFactor(alvos[i].tela ? 0 : 1);
    });
  }

  esconder() {
    this.balao.setVisible(false);
    this.setas.forEach((s) => s.setVisible(false));
    this.alvos = [];
  }

  // Chamar a cada quadro (depois de entrada.atualizar()).
  update(delta) {
    if (this.capivaraFeita && this.passo >= 4) return;
    const e = this.entrada;
    const tempo = this.scene.time.now - (this.inicioPasso || 0);

    // seta balançando para chamar atenção
    this.balanco += delta * 0.008;
    this.alvos.forEach((a, i) => this.setas[i].setPosition(a.x, a.y + Math.sin(this.balanco) * 4 - 12));

    // enquanto explica os botões, as capivaras da tela esperam paradas (ninguém leva dano aprendendo)
    if (this.passo > 0 && this.passo < 4) {
      for (const c of this.capivaras.getChildren()) {
        if (c.active && c.perigosa && Math.abs(c.x - this.jogador.x) < 300) c.body.setVelocityX(0);
      }
    }

    if (this.passo === 1) {
      if (e.esquerda || e.direita) this.andou += delta;
      if (this.andou > 600 || tempo > 9000) this.irPara(2);
    } else if (this.passo === 2) {
      if (e.pularApertou || tempo > 9000) this.scene.time.delayedCall(400, () => this.passo === 2 && this.irPara(3));
    } else if (this.passo === 3) {
      if (e.macaApertou || tempo > 9000) {
        this.passo = 3.5; // espera o próximo quadro sem repetir
        this.scene.time.delayedCall(500, () => {
          this.irPara(4);
          this.scene.registry.set('tutorialVisto', true);
        });
      }
    }

    // dica da capivara: vale desde o começo (se a pessoa correr na frente do tutorial)
    if (!this.capivaraFeita) this.dicaCapivara();
  }

  dicaCapivara() {
    const j = this.jogador;
    const perto = this.capivaras
      .getChildren()
      .filter((c) => c.active && c.perigosa && c.x > j.x - 20 && c.x - j.x < 230)
      .sort((a, b) => a.x - b.x)[0];
    if (this.capivaraAlvo) {
      const c = this.capivaraAlvo;
      // terminou quando ela dormiu/comeu ou quando o jogador já passou dela
      if (!c.active || !c.perigosa || j.x > c.x + 40) {
        this.capivaraFeita = true;
        this.esconder();
        return;
      }
      this.alvos = [{ x: c.x, y: c.y - c.displayHeight - 4, tela: false }];
      return;
    }
    // só entra depois dos passos dos botões (até lá as capivaras ficam paradas)
    if (perto && this.passo >= 4) {
      this.capivaraAlvo = perto;
      this.passo = Math.max(this.passo, 4);
      this.mostrar(this.t.capivara, [{ x: perto.x, y: perto.y - perto.displayHeight - 4, tela: false }]);
      // o balão fica fixo no alto da tela; a seta acompanha a capivara no mundo
      this.balao.setPosition(LARGURA / 2, 104);
    }
  }
}
