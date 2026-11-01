import { LARGURA, ALTURA, CORES, CORES_CSS, FONTES } from '../config.js';

// Caixa de diálogo na parte de baixo da tela, com o texto aparecendo letra por letra.
// Tocar (ou Espaço/Enter) completa o texto; tocar de novo passa para a próxima caixa.
// Máximo de 2 linhas por caixa (CLAUDE.md, regra 6): use \n em src/data/textos.js.
export class Dialogo {
  constructor(scene, { y = ALTURA - 44, letrasPorSeg = 45, dica = '' } = {}) {
    this.scene = scene;
    this.letrasPorSeg = letrasPorSeg;
    const L = LARGURA - 32;
    const A = 64;
    this.cont = scene.add.container(LARGURA / 2, y).setScrollFactor(0).setDepth(3000);
    const g = scene.add.graphics();
    g.fillStyle(CORES.roxo, 0.6).fillRoundedRect(-L / 2 + 3, -A / 2 + 3, L, A, 6);
    g.fillStyle(CORES.branco, 0.96).fillRoundedRect(-L / 2, -A / 2, L, A, 6);
    g.lineStyle(3, CORES.roxo, 1).strokeRoundedRect(-L / 2, -A / 2, L, A, 6);
    this.texto = scene.add
      .text(-L / 2 + 14, -A / 2 + 8, '', { fontFamily: FONTES.dialogo, fontSize: '20px', color: '#3A2F7A', lineSpacing: -2 })
      .setOrigin(0, 0);
    // triângulo "próximo" que pisca quando o texto terminou (Patrick Hand não tem ▶)
    this.seta = scene.add.triangle(L / 2 - 16, A / 2 - 12, 0, 0, 10, 0, 5, 7, CORES.rosa).setStrokeStyle(1, CORES.roxo);
    this.dica = scene.add
      .text(L / 2 - 26, A / 2 - 9, dica, { fontFamily: FONTES.dialogo, fontSize: '13px', color: CORES_CSS.roxo })
      .setOrigin(1, 0.5);
    this.cont.add([g, this.texto, this.seta, this.dica]);
    scene.tweens.add({ targets: this.seta, alpha: 0.2, yoyo: true, repeat: -1, duration: 400 });
    this.cheio = '';
    this.mostradas = 0;
  }

  mostrar(texto) {
    this.cheio = texto;
    this.mostradas = 0;
    this.texto.setText('');
    this.cont.setVisible(true);
  }

  get terminou() {
    return this.mostradas >= this.cheio.length;
  }

  completar() {
    this.mostradas = this.cheio.length;
    this.texto.setText(this.cheio);
  }

  esconder() {
    this.cont.setVisible(false);
  }

  // Chamar no update() da cena.
  atualizar(delta) {
    if (this.terminou) {
      this.seta.setVisible(true);
      this.dica.setVisible(true);
      return;
    }
    this.seta.setVisible(false);
    this.dica.setVisible(false);
    this.mostradas = Math.min(this.cheio.length, this.mostradas + (this.letrasPorSeg * delta) / 1000);
    this.texto.setText(this.cheio.slice(0, Math.floor(this.mostradas)));
  }
}
