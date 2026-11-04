import { construir, CHAO } from './construtor.js';
import { nomeVaga } from '../data/vagas.js';
import { estado } from '../estado.js';
import { TEXTOS } from '../data/textos.js';

// Fase 4, Praça central (Praça Theodomiro Santiago), DESIGN.md: conhece a lanchonete (pão de queijo, arremesso) e
// o café (café com leite, cresce), descobre que quem estuda na UNIFEI trabalha na fábrica e aprende a história de
// Theodomiro Santiago. Depois, plataforma com os poderes novos até o fim.
const FONTE = 26; // fonte com o busto (172 px)
const BURG = 50; // Cesar Burg (180 px)
const CAFE = 74; // Café do Vadinho (188 px)

const mapa = construir(190, (m) => {
  m.set(4, CHAO - 1, 'P');
  m.moedas(8, 14, CHAO - 1, 2);
  // borda da fonte (dá para andar em cima)
  m.linha(FONTE + 1, FONTE + 9, 14, '-');
  m.set(FONTE + 12, CHAO - 1, 'N'); // guia ao lado do busto
  m.set(BURG + 6, CHAO - 1, 'N'); // atendente do Cesar Burg
  m.linha(BURG, BURG + 10, 9, '-'); // toldo
  m.moedas(BURG + 1, BURG + 9, 8, 2);
  m.set(CAFE + 6, CHAO - 1, 'N'); // barista do Café do Vadinho
  m.set(CAFE + 16, CHAO - 1, 'N'); // estudante da UNIFEI
  m.set(98, CHAO - 1, 'K');
  // daqui em diante: pombos e capivaras para testar o pão de queijo, copos de café com leite no caminho
  m.set(104, CHAO - 1, 'C');
  m.linha(108, 111, 12, '=');
  m.set(109, 11, 'c');
  m.set(116, CHAO - 1, 'V');
  m.set(119, CHAO - 1, 'V');
  m.arco(122, 127, 10);
  m.buraco(124, 125);
  m.set(130, CHAO - 1, 'p');
  m.set(131, CHAO - 1, 'p');
  m.set(134, CHAO - 1, 'C');
  m.linha(138, 141, 11, '=');
  m.linha(144, 147, 8, '=');
  m.moedas(144, 147, 7);
  m.set(150, CHAO - 1, 'V');
  m.set(153, CHAO - 1, 'C');
  m.set(156, CHAO - 1, 'K');
  m.set(160, CHAO - 1, 'c');
  m.set(166, CHAO - 1, 'V');
  m.set(169, CHAO - 1, 'C');
  m.buraco(172, 173);
  m.arco(170, 175, 10);
  m.set(178, CHAO - 1, 'p');
  m.set(184, CHAO - 1, 'E');
});

export const FASE4 = {
  numero: 4,
  musica: 'centro',
  ceu: ['#6E86D8', '#8494DE', '#9EA2E2', '#BAAEE0', '#D6B8D8', '#ECC2CC', '#F8D0C0'],
  fundos: [
    { chave: 'morros', fator: 0.12 },
    { chave: 'casas', fator: 0.35, y: 6 },
  ],
  lugares: [
    { img: 'igreja', col: 8, dx: 0, fator: 0.6, prof: -2 },
    { img: 'arvore2', col: 18 },
    { img: 'fonte', col: FONTE, dx: -8, prof: 1.2 },
    { img: 'cesar-burg', col: BURG },
    { img: 'cafe', col: CAFE },
    { img: 'arvore', col: 96 },
    { img: 'arvore2', col: 128 },
    { img: 'arvore', col: 160 },
  ],
  npcs: [
    {
      sprite: 'npc-guia',
      nome: 'Guia da praça',
      falas: [
        { texto: 'Esse é o busto de Theodomiro Santiago.' },
        { texto: 'Em 1913 ele fundou aqui a escola de engenharia que hoje é a UNIFEI.' },
        { quem: 'heroi', texto: 'Uma escola de engenharia tão antiga? Que legal!' },
      ],
    },
    {
      sprite: 'npc-atendente',
      nome: 'Atendente',
      falas: [
        { texto: `Oi! Bem-vind{o|a} ao ${nomeVaga('lanchonete')}! Prova nosso pão de queijo quentinho.` },
        { texto: 'Leve alguns! Quem pega um pão de queijo come e vai embora feliz.' },
      ],
      acao: 'pao',
    },
    {
      sprite: 'npc-barista',
      nome: 'Barista',
      falas: [
        { texto: `Um café com leite do ${nomeVaga('cafe')} para dar energia?` },
        { texto: 'Com ele você fica maior e aguenta um esbarrão a mais!' },
      ],
      acao: 'cafe',
    },
    {
      sprite: 'npc-estudante',
      nome: 'Estudante',
      falas: [
        { texto: 'Eu estudo engenharia na UNIFEI.' },
        { texto: 'Muita gente que estuda lá vai trabalhar na fábrica de helicópteros!' },
        { quem: 'heroi', texto: 'Então quem faz helicóptero estudou engenharia... Vou guardar essa ideia!' },
      ],
    },
  ],
  gatilhos: [],
  missao: 'Prove o pão de queijo e o café com leite da praça',
  exigir: () => (estado.temPao && estado.temCafe ? null : TEXTOS.avisos.semPoderes),
  mapa,
  curiosidade: {
    texto: 'Theodomiro Santiago fundou em 1913 o Instituto Eletrotécnico e Mecânico de Itajubá, a 10ª escola de engenharia do Brasil. Ele virou IEI (1936), EFEI (1968) e UNIFEI (2002).',
    fonte: 'UNIFEI e BOCEHM (revistas.uece.br)',
  },
};
