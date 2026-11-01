import * as Phaser from 'phaser';
import { LARGURA, CORES, CORES_CSS, FONTES } from '../config.js';
import { TEXTOS } from '../data/textos.js';

// Fase 3, Resgate: TELA PROVISÓRIA até a luta contra o Jafar existir (Etapa 5).
// Mostra o que foi recolhido até aqui e o botão de jogar de novo.
export class Chefe extends Phaser.Scene {
  constructor() {
    super('Chefe');
  }

  create() {
    const t = TEXTOS.chefe;
    const reg = this.registry;
    this.cameras.main.setBackgroundColor('#2E1A33').fadeIn(500, 46, 26, 51);
    const titulo = (y, texto, tam, cor) =>
      this.add
        .text(LARGURA / 2, y, texto, { fontFamily: FONTES.titulo, fontSize: tam, color: cor })
        .setOrigin(0.5)
        .setShadow(2, 2, CORES_CSS.roxo, 0, false, true);
    const linha = (y, texto, cor = CORES_CSS.branco) =>
      this.add.text(LARGURA / 2, y, texto, { fontFamily: FONTES.dialogo, fontSize: '18px', color: cor }).setOrigin(0.5);

    titulo(42, t.titulo, '12px', CORES_CSS.rosa);
    linha(74, t.aviso, CORES_CSS.amarelo);
    linha(98, t.proxima, CORES_CSS.lilas);
    this.add.sprite(LARGURA / 2 - 92, 131, 'sapatilha', 0).setScale(2);
    this.add
      .text(LARGURA / 2 - 72, 131, t.sapatilhas(reg.get('sapatilhas') ?? 0, reg.get('sapatilhasTotal') ?? 0), {
        fontFamily: FONTES.dialogo,
        fontSize: '18px',
        color: CORES_CSS.branco,
      })
      .setOrigin(0, 0.5);
    this.add.image(LARGURA / 2 - 92, 157, 'ingresso').setScale(2);
    this.add
      .text(LARGURA / 2 - 72, 157, t.ingressos(reg.get('ingressos') ?? 0), {
        fontFamily: FONTES.dialogo,
        fontSize: '18px',
        color: CORES_CSS.branco,
      })
      .setOrigin(0, 0.5);

    const botao = this.add.rectangle(LARGURA / 2, 214, 190, 40, CORES.rosa).setStrokeStyle(3, CORES.lilas);
    this.add
      .text(LARGURA / 2, 215, t.jogarDeNovo, { fontFamily: FONTES.titulo, fontSize: '12px', color: CORES_CSS.roxo })
      .setOrigin(0.5);
    const deNovo = () => this.scene.start('Itajuba', { direto: true });
    botao.setInteractive({ useHandCursor: true }).on('pointerup', deNovo);
    this.input.keyboard?.once('keydown-ENTER', deNovo);
  }
}
