import { construir, CHAO } from './construtor.js';

// Fase 2, Praça do Soldado (DESIGN.md): vê o helicóptero da praça e decide ser piloto. Novidade: itacoins.
// Inimigos: pombos da praça (e uma capivara passeando). Estátua do soldado e helicóptero exposto (arte do projeto).
const mapa = construir(156, (m) => {
  m.set(4, CHAO - 1, 'P');
  m.set(10, CHAO - 1, 'N'); // vovó: explica as itacoins
  m.moedas(14, 20, CHAO - 1, 2);
  m.linha(22, 26, 11, '=');
  m.moedas(22, 26, 10);
  m.set(30, CHAO - 1, 'V');
  m.set(31, CHAO - 2, 'G'); // dica: pisar no pombo (o gatilho fica um pouco antes, à altura do herói)
  m.arco(36, 41, 10);
  m.buraco(38, 39);
  m.set(46, CHAO - 1, 'V');
  m.linha(50, 53, 12, '=');
  m.linha(55, 58, 9, '=');
  m.moedas(55, 58, 8);
  m.set(62, CHAO - 1, 'K');
  // pedestal da estátua do soldado (dá para subir)
  m.ret(70, 12, 72, 14, 'x');
  m.moedas(70, 72, 11);
  m.set(78, CHAO - 1, 'V');
  m.set(84, CHAO - 1, 'C');
  m.arco(88, 93, 10);
  m.buraco(90, 91);
  m.linha(96, 99, 12, '=');
  m.set(98, 11, 'h');
  m.set(102, CHAO - 1, 'V');
  m.moedas(104, 108, CHAO - 1, 2);
  m.set(112, CHAO - 1, 'N'); // morador ao lado do helicóptero
  m.moedas(130, 136, 12);
  m.linha(130, 136, 13, '=');
  m.set(140, CHAO - 1, 'V');
  m.set(150, CHAO - 1, 'E');
});

export const FASE2 = {
  numero: 2,
  musica: 'praca',
  ceu: ['#4E90E6', '#62A0EC', '#78B0F2', '#8EC0F8', '#A6D0FC', '#C0E0FF', '#DAEEFF'],
  fundos: [
    { chave: 'morros', fator: 0.15 },
    { chave: 'casas', fator: 0.4, y: 14 },
  ],
  lugares: [
    { img: 'arvore', col: 0, dx: -40 },
    { img: 'arvore2', col: 16 },
    { img: 'arvore', col: 44 },
    { img: 'estatua', col: 70, dx: -13, dy: 0 },
    { img: 'arvore2', col: 80 },
    { img: 'helicoptero', col: 114, dx: 0 },
    { img: 'arvore', col: 128 },
    { img: 'arvore2', col: 142 },
  ],
  npcs: [
    {
      sprite: 'npc-vovo',
      nome: 'Vovó da praça',
      falas: [
        { texto: 'Oi! Viu as pedrinhas amarelas? São as itacoins.' },
        { texto: 'Pegue todas! Elas servem para comprar coisas na cidade.' },
      ],
    },
    {
      sprite: 'npc-guia',
      nome: 'Morador',
      falas: [
        { texto: 'Bonito, né? Esse helicóptero fica aqui na praça para todo mundo ver.' },
        { quem: 'heroi', texto: 'Parece o que eu vi voando no céu!' },
        { quem: 'heroi', texto: 'Decidi: quando eu crescer, vou ser {piloto|pilota} de helicóptero!' },
        { texto: 'Que sonho bonito! Siga em frente, Itajubá tem muito mais para mostrar.' },
      ],
    },
  ],
  gatilhos: [{ dica: { toque: 'Pule em cima do pombo: ele sai voando!', teclado: 'Pule em cima do pombo: ele sai voando!' } }],
  missao: 'Junte itacoins e chegue ao helicóptero da praça',
  mapa,
  curiosidade: {
    texto: 'Itajubá tem a primeira e única fábrica de helicópteros da América Latina.',
    fonte: 'Rádio Senado, 2022',
  },
};
