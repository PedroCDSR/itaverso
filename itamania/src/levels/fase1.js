import { construir, CHAO } from './construtor.js';
import { esperar } from '../util.js';
import { tocarEfeito } from '../audio/efeitos.js';

// Fase 1, Rodoviária e trem-museu (DESIGN.md). Chegada de ônibus; o trem parado em frente (peça de museu, não anda)
// é o tutorial: subir na locomotiva e pular para o vagão. Lá de cima, o helicóptero cruza o céu.
// Sem inimigos e sem itacoins (as itacoins começam na fase 2).
const LOCO = 40; // coluna da locomotiva (144 px = 9 colunas)
const V1 = 51; // vagão 1 (120 px = 7,5 colunas)

const mapa = construir(116, (m) => {
  m.set(11, CHAO - 1, 'P');
  m.set(15, CHAO - 1, 'G'); // dica: andar
  m.set(34, CHAO - 1, 'N'); // guia do museu
  m.set(37, CHAO - 1, 'G'); // dica: pular
  // locomotiva: limpa-trilhos baixo, caldeira (topo y 192) e cabine (teto y 176)
  m.ret(LOCO, 13, LOCO, 14, 'x');
  m.ret(LOCO + 1, 12, LOCO + 5, 14, 'x');
  m.ret(LOCO + 6, 11, LOCO + 8, 14, 'x');
  // vagão (teto y 176), com 2 colunas de vão depois da locomotiva
  m.ret(V1, 11, V1 + 6, 14, 'x');
  m.set(V1 + 4, 10, 'G'); // em cima do vagão: o helicóptero passa
  m.set(76, CHAO - 1, 'K');
  // canteiros baixos para pular no caminho até a saída
  m.ret(84, 13, 86, 14, 'x');
  m.ret(95, 12, 97, 14, 'x');
  m.set(110, CHAO - 1, 'E');
});

// Chegada: o ônibus entra pela esquerda, para, o herói desce e o ônibus vai embora.
async function chegada(cena) {
  const j = cena.jogador;
  j.setVisible(false);
  const bus = cena.add.image(-180, cena.chaoY + 2, 'onibus').setOrigin(0, 1).setDepth(9);
  await new Promise((ok) => cena.tweens.add({ targets: bus, x: 30, duration: 1700, ease: 'Cubic.out', onComplete: ok }));
  tocarEfeito('botao');
  await esperar(cena, 300);
  j.setVisible(true);
  j.x = 30 + 150;
  cena.tweens.add({ targets: j, x: 30 + 168, duration: 300 });
  await esperar(cena, 350);
  await cena.falar([
    { quem: 'Motorista', texto: 'Chegamos! Bem-vind{o|a} a Itajubá!' },
    { quem: 'heroi', texto: 'Uau! Cidade nova, vida nova. Estou {animado|animada}!' },
    { quem: 'heroi', texto: 'Eu não conheço nada aqui. Quero conhecer tudo!' },
  ]);
  bus.setDepth(3);
  cena.tweens.add({ targets: bus, x: 1900, duration: 4200, ease: 'Cubic.in', onComplete: () => bus.destroy() });
}

// O helicóptero cruza o céu enquanto o herói está em cima do vagão.
async function helicoptero(cena) {
  const cam = cena.cameras.main;
  const h = cena.add.sprite(cam.scrollX + 540, 54, 'heliceu', 0).setDepth(-5).play('heli-voar');
  h.setScrollFactor(0.2, 1);
  h.x = cam.scrollX * 0.2 + 540;
  cena.ocupado = true;
  cena.jogador.olhandoDireita = true;
  cena.tweens.add({ targets: h, x: h.x - 640, y: 40, duration: 5200, onComplete: () => h.destroy() });
  await esperar(cena, 1200);
  await cena.falar([
    { quem: 'heroi', texto: 'Olha lá no céu! Um helicóptero!' },
    { quem: 'heroi', texto: 'Que demais! Para onde será que ele vai?' },
  ]);
}

export const FASE1 = {
  numero: 1,
  musica: 'rodoviaria',
  ceu: ['#5C9CEC', '#6FA8F0', '#86B8F4', '#9EC8FF', '#B6D6FF', '#CCE2FF', '#E2EEFF'],
  fundos: [
    { chave: 'morros', fator: 0.15 },
    { chave: 'casas', fator: 0.4, y: 14 },
  ],
  lugares: [
    { img: 'rodoviaria', col: 0, dx: -6 },
    { img: 'arvore2', col: 30, dx: 0 },
    { img: 'locomotiva', col: LOCO, dy: 4, prof: 2 },
    { img: 'vagao1', col: V1, dy: 2, prof: 2 },
    { img: 'arvore', col: 78 },
    { img: 'arvore2', col: 100 },
  ],
  npcs: [
    {
      sprite: 'npc-guia',
      nome: 'Guia do museu',
      falas: [
        { texto: 'Esse trem é peça de museu. Ele não anda mais, mas pode subir!' },
        { texto: 'Lá de cima dos vagões dá para ver a cidade inteira.' },
      ],
    },
  ],
  gatilhos: [
    { dica: { toque: 'Toque nas setas para andar', teclado: 'Setas ou A e D para andar' } },
    { dica: { toque: 'Toque em PULAR. Segure para ir mais alto!', teclado: 'Espaço ou W para pular. Segure para ir mais alto!' } },
    { evento: helicoptero },
  ],
  missao: 'Suba no trem-museu e olhe a cidade lá de cima',
  chegada,
  mapa,
  curiosidade: {
    texto: 'Em 1932 foi aprovada a construção de uma nova estação de trem em Itajubá, na Linha Sapucaí da Rede Mineira de Viação.',
    fonte: 'Decreto de 1932, Senado Federal',
  },
};
