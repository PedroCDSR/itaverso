import { construir, CHAO } from './construtor.js';
import { nomeVaga, VAGAS } from '../data/vagas.js';
import { ITENS } from '../config.js';
import { estado } from '../estado.js';
import { TEXTOS } from '../data/textos.js';

// Fase 3, Rua Nova (DESIGN.md): compra o boné amarelo com itacoins na loja e descobre que o helicóptero é feito na
// cidade. Novidade: loja. Inimigos: pombos e capivaras. A saída só abre com o boné.
const JOKA = 72; // coluna da Casa Joka (176 px = 11 colunas)

const mapa = construir(170, (m) => {
  m.set(4, CHAO - 1, 'P');
  m.moedas(8, 14, CHAO - 1, 2);
  // toldos e marquises das lojas viram plataformas
  m.linha(12, 19, 9, '-');
  m.moedas(13, 18, 8);
  m.set(22, CHAO - 1, 'V');
  m.linha(26, 33, 9, '-');
  m.moedas(27, 32, 8, 1);
  m.set(36, CHAO - 1, 'C');
  m.set(44, CHAO - 1, 'N'); // técnico da fábrica
  m.arco(50, 55, 10);
  m.buraco(52, 53);
  m.set(58, CHAO - 1, 'V');
  m.set(62, CHAO - 1, 'K');
  m.moedas(64, 68, CHAO - 1, 2);
  m.linha(JOKA, JOKA + 10, 9, '-'); // toldo listrado da Casa Joka
  m.moedas(JOKA + 1, JOKA + 9, 8, 2);
  m.set(JOKA + 6, CHAO - 1, 'N'); // vendedora na porta da loja
  m.set(92, CHAO - 1, 'C');
  m.linha(96, 99, 12, '=');
  m.linha(101, 104, 10, '=');
  m.moedas(101, 104, 9);
  m.set(108, CHAO - 1, 'V');
  m.buraco(112, 113);
  m.arco(110, 115, 10);
  m.linha(118, 125, 9, '-');
  m.set(122, 8, 'h');
  m.set(128, CHAO - 1, 'C');
  m.set(134, CHAO - 1, 'V');
  m.linha(140, 147, 9, '-');
  m.moedas(141, 146, 8);
  m.set(152, CHAO - 1, 'C');
  m.set(164, CHAO - 1, 'E');
});

export const FASE3 = {
  numero: 3,
  musica: 'ruanova',
  ceu: ['#5A8EE0', '#6C9CE6', '#80ACEC', '#96BCF2', '#ACCCF6', '#C4DCFA', '#DCEAFE'],
  fundos: [
    { chave: 'morros', fator: 0.12 },
    { chave: 'casas', fator: 0.35, y: 6 },
  ],
  lugares: [
    { img: 'loja-papelaria', col: 11, dx: 0 },
    { img: 'loja-sapatos', col: 25, dx: 8 },
    { img: 'clube', col: 40, dx: 0, prof: 0.5 },
    { img: VAGAS.loja.real ? 'casa-joka' : 'loja-papelaria', col: JOKA },
    { img: 'loja-sapatos', col: 117, dx: 0, flip: true },
    { img: 'loja-papelaria', col: 139, dx: 0 },
  ],
  npcs: [
    {
      sprite: 'npc-tecnico',
      nome: 'Técnico',
      falas: [
        { texto: 'Oi! Eu trabalho na fábrica de helicópteros aqui de Itajubá.' },
        { quem: 'heroi', texto: 'Helicóptero é feito aqui na cidade? Que incrível!' },
        { texto: 'É sim! Quem sabe um dia você ajuda a construir um.' },
      ],
    },
    {
      sprite: 'npc-vendedora',
      nome: 'Vendedora',
      falas: () =>
        estado.bone
          ? [{ texto: 'Esse boné ficou ótimo em você!' }]
          : [{ texto: `Bem-vind{o|a} à ${nomeVaga('loja')}! Esse boné amarelo custa ${ITENS.precoBone} itacoins.` }],
      acao: 'loja',
    },
  ],
  gatilhos: [],
  missao: `Compre o boné amarelo na ${nomeVaga('loja')}`,
  exigir: () => (estado.bone ? null : TEXTOS.avisos.semBone),
  mapa,
  curiosidade: {
    texto: 'Uma das explicações para o nome Itajubá é "pedra amarela", ou seja, ouro. Há outras versões, como "braço de pedra".',
    fonte: 'IBGE, histórico de Itajubá',
  },
};
