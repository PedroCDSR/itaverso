// Registro da arte do jogo.
//
// PNGs finais: quando um PNG com os MESMOS tamanhos de quadro for colocado em public/assets/sprites/<nome>.png,
// adicione o nome em SPRITES_PNG (ex.: jogador: { largura: 32, altura: 48 }). O Preload carrega o PNG e
// ignora a matriz. A lista evita pedir arquivos que não existem (cada pedido gasta banda no Netlify).
export const SPRITES_PNG = {
  // Elenco da Etapa 8A (ferramentas/arte/gerar_elenco.py). A capivara continua em objetos.js.
  tiaPaula: { largura: 48, altura: 64 }, // 0-1 presa, 2-3 feliz, 4 sentada (tapete), 5-6 microfone (Final)
  claudia: { largura: 48, altura: 64 }, // 0 parada, 1 entregando ingressos, 2 parada (respira)
  jasmine: { largura: 48, altura: 64 }, // 0 parada, 1-2 pirueta
  sultao: { largura: 56, altura: 72 }, // 0 parado, 1 palmas
  genio: { largura: 88, altura: 104 }, // 0 flutuando, 1 tchan!
  abu: { largura: 36, altura: 40 }, // 0 parado, 1-2 correndo, 3 aflito
  jafar: { largura: 64, altura: 84 }, // 0-1 flutuando, 2 lançando, 3 cansado/tonto
  gaiola: { largura: 74, altura: 96 }, // grades da frente: 0 fechada, 1 aberta
  gaiolaFundo: { largura: 74, altura: 96 }, // grades de trás: 0 com o brilho do feitiço, 1 sem
  tucano: { largura: 36, altura: 24 }, // Tapete: 0-1 batendo as asas
  maritaca: { largura: 30, altura: 16 }, // Tapete: 0-1 batendo as asas
};

// Cenários em PNG (ferramentas/arte/gerar_cenarios.py), em public/assets/cenario/<nome>.png.
// Fase 1: céu, serra e casario em camadas e os lugares reais de Itajubá; Fase 3: arena ao pôr do sol;
// Fase 4: crepúsculo (céu, serra, cidade e telhados com janelas acesas), Hotel Coroados e UNIFEI.
export const CENARIO_PNG = [
  'ceu', 'morros', 'casas', 'clube', 'fonte', 'cafe', 'igreja', 'posto', 'estatua', 'helicoptero', 'arvore', 'arvore2',
  'arena',
  'ceu-crepusculo', 'serra-crepusculo', 'cidade-crepusculo', 'telhados-crepusculo', 'coroados', 'unifei', 'teatro-g9',
];

export * as ArteJogador from './jogador.js';
export * as ArteTiles from './tiles.js';
export * as ArteObjetos from './objetos.js';
export * as ArteEspaco from './espaco.js';
export * as ArteTapete from './tapete.js';

// Logo da escola: mude para true quando existir public/assets/logo.png (assim não há pedido 404).
// Sem o logo, o Título e o Final mostram o nome da escola em texto.
export const TEM_LOGO = false;
