// Lista dos arquivos de arte que o Preload carrega.
import * as ArteTiles from './tiles.js';
import * as ArteObjetos from './objetos.js';
import * as ArteHeroi from './heroi.js';

export { ArteTiles, ArteObjetos, ArteHeroi };

// Cenários (public/assets/cenario/<nome>.png). Os de Itajubá são arte própria do projeto;
// os novos saem de ferramentas/arte/gerar_cenarios.py.
export const CENARIO_PNG = [
  'ceu', 'morros', 'casas', 'fonte', 'cafe', 'igreja', 'estatua', 'helicoptero', 'arvore', 'arvore2', 'clube',
  'coroados', 'unifei', 'posto', 'rodoviaria', 'onibus', 'locomotiva', 'vagao1', 'casa-joka',
  'loja-sapatos', 'loja-papelaria', 'cesar-burg',
];

// Folhas de quadros (public/assets/sprites/<nome>.png): nome -> tamanho do quadro.
export const SPRITES_PNG = {
  itacoin: [12, 12],
  paodequeijo: [12, 10],
  cafecomleite: [14, 18],
  boneitem: [18, 12],
  pombo: [24, 20],
  heliceu: [72, 30],
  placaretorno: [18, 44],
  placasaida: [26, 40],
  'npc-motorista': [32, 64],
  'npc-guia': [32, 64],
  'npc-vovo': [32, 64],
  'npc-vendedora': [32, 64],
  'npc-tecnico': [32, 64],
  'npc-atendente': [32, 64],
  'npc-barista': [32, 64],
  'npc-estudante': [32, 64],
};

// Mapa-múndi pronto (pixel art em pé, 480 px de largura) em public/assets/mapa.png. Mude para true quando o arquivo
// existir; enquanto for false, o mapa é desenhado em código (scenes/Mapa.js). Evita um pedido 404.
export const TEM_MAPA = true;
