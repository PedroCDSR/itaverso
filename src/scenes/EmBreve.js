import * as Phaser from 'phaser';
import { LARGURA, CORES_CSS, FONTES } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { Botao } from '../ui/Botao.js';

// Ponte PROVISÓRIA entre a Fase 1 e o Tapete, no lugar das Fases 2 (Espaço) e 3 (Chefe).
// Sai nas Etapas 4 e 5: a Itajubá passa a ir para o Espaco, e o Chefe termina indo para o Tapete.
export class EmBreve extends Phaser.Scene {
  constructor() {
    super('EmBreve');
  }

  create(dados) {
    const t = TEXTOS.emBreve;
    this.cameras.main.setBackgroundColor(CORES_CSS.lilas).fadeIn(300, 158, 158, 255);
    this.add
      .text(LARGURA / 2, 50, t.titulo, { fontFamily: FONTES.titulo, fontSize: '12px', color: CORES_CSS.branco })
      .setOrigin(0.5)
      .setShadow(2, 2, CORES_CSS.roxo, 0, false, true);
    this.add.sprite(LARGURA / 2 - 50, 91, 'sapatilha', 0).setScale(2);
    this.add
      .text(LARGURA / 2 - 30, 91, `${t.sapatilhas(dados?.sapatilhas ?? 0)} / ${dados?.total ?? 0}`, {
        fontFamily: FONTES.dialogo,
        fontSize: '22px',
        color: CORES_CSS.roxo,
      })
      .setOrigin(0, 0.5);
    this.add
      .text(LARGURA / 2, 140, t.proxima, { fontFamily: FONTES.dialogo, fontSize: '18px', color: CORES_CSS.roxo, align: 'center' })
      .setOrigin(0.5);

    const seguir = () => {
      if (this.saindo) return;
      this.saindo = true;
      this.scene.start('Tapete'); // o Tapete continua a contagem de sapatilhas do registry
    };
    new Botao(this, LARGURA / 2, 205, t.continuar, seguir, { largura: 200, altura: 36, cor: 'rosa', tamanhoFonte: '12px' });
    this.input.keyboard?.once('keydown-ENTER', seguir);
  }
}
