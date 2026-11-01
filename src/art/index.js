// Registro da arte do jogo.
//
// PNGs finais: quando um PNG com os MESMOS tamanhos de quadro for colocado em public/assets/sprites/<nome>.png,
// adicione o nome em SPRITES_PNG (ex.: jogador: { largura: 32, altura: 48 }). O Preload carrega o PNG e
// ignora a matriz. A lista evita pedir arquivos que não existem (cada pedido gasta banda no Netlify).
export const SPRITES_PNG = {
  // jogador: { largura: 32, altura: 48 },
};

export * as ArteJogador from './jogador.js';
export * as ArteTiles from './tiles.js';
export * as ArteObjetos from './objetos.js';
export * as ArteEspaco from './espaco.js';
export * as ArteTapete from './tapete.js';

// Logo da escola: mude para true quando existir public/assets/logo.png (assim não há pedido 404).
// Sem o logo, o Título e o Final mostram o nome da escola em texto.
export const TEM_LOGO = false;
