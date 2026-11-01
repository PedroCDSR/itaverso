import * as Phaser from 'phaser';
import { tocarEfeito } from '../audio/efeitos.js';
import { tocarMusica } from '../audio/musica.js';
import { LARGURA, ALTURA, CORES, CORES_CSS, FONTES } from '../config.js';
import { TEXTOS } from '../data/textos.js';
import { EVENTO, linkWhatsapp } from '../data/evento.js';
import { BotaoSom } from '../ui/BotaoSom.js';

// Tela final PROVISÓRIA (Etapa 6): cortinas abrindo, dados do espetáculo e dois botões.
// A versão completa (Tia Paula no palco, COMPARTILHAR, INSTAGRAM, logo) vem na Etapa 7.
export class Final extends Phaser.Scene {
  constructor() {
    super('Final');
  }

  create(dados) {
    const F = TEXTOS.final;
    tocarMusica('final');
    const sapatilhas = dados?.sapatilhas ?? this.registry.get('sapatilhas') ?? 0;
    this.add.rectangle(0, 0, LARGURA, ALTURA, CORES.lilas).setOrigin(0);

    const titulo = { fontFamily: FONTES.titulo, color: CORES_CSS.branco };
    const texto = { fontFamily: FONTES.dialogo, color: CORES_CSS.roxo, align: 'center' };
    this.add
      .text(LARGURA / 2, 28, F.titulo, { ...titulo, fontSize: '12px' })
      .setOrigin(0.5)
      .setShadow(2, 2, CORES_CSS.roxo, 0, false, true);
    this.add.text(LARGURA / 2, 50, F.sapatilhas.replace('{n}', sapatilhas), { ...texto, fontSize: '16px' }).setOrigin(0.5);

    // cartão com os dados do evento
    this.add.rectangle(LARGURA / 2, 116, 360, 92, CORES.branco, 0.9).setStrokeStyle(2, CORES.roxo);
    const linhas = [
      `${EVENTO.titulo} · ${EVENTO.escola}`,
      EVENTO.data,
      `Horário: ${EVENTO.horario}`,
      EVENTO.local,
      `Ingresso: ${EVENTO.ingresso}`,
    ];
    this.add.text(LARGURA / 2, 116, linhas.join('\n'), { ...texto, fontSize: '14px', lineSpacing: -2 }).setOrigin(0.5);

    this.botao(LARGURA / 2 - 95, 196, F.ingressos, CORES.rosa, () => window.open(linkWhatsapp(), '_blank'));
    this.botao(LARGURA / 2 + 95, 196, F.jogarDeNovo, CORES.amarelo, () => {
      this.registry.set('sapatilhas', 0);
      this.scene.start('Tapete');
    });
    this.add.text(LARGURA / 2, 240, F.provisorio, { ...texto, fontSize: '12px', color: CORES_CSS.branco }).setOrigin(0.5);
    new BotaoSom(this, LARGURA - 20, 20);

    // cortinas rosa que se abrem
    const metade = LARGURA / 2;
    const esq = this.add.rectangle(0, 0, metade, ALTURA, 0xd57fcf).setOrigin(0).setDepth(10);
    const dir = this.add.rectangle(metade, 0, metade, ALTURA, 0xd57fcf).setOrigin(0).setDepth(10);
    this.tweens.add({ targets: esq, x: -metade + 24, duration: 1200, ease: 'Sine.inOut', delay: 300 });
    this.tweens.add({ targets: dir, x: LARGURA - 24, duration: 1200, ease: 'Sine.inOut', delay: 300 });
    this.cameras.main.fadeIn(400, 158, 158, 255);
  }

  botao(x, y, rotulo, cor, acao) {
    const fundo = this.add.rectangle(x, y, 170, 36, cor).setStrokeStyle(3, CORES.roxo);
    this.add.text(x, y + 1, rotulo, { fontFamily: FONTES.titulo, fontSize: '9px', color: CORES_CSS.roxo }).setOrigin(0.5);
    fundo.setInteractive({ useHandCursor: true });
    // pointerup: abrir link novo só funciona dentro do gesto, e o dedo já saiu da tela
    fundo.on('pointerup', () => {
      tocarEfeito('botao');
      acao();
    });
  }
}
