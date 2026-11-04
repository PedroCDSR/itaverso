// Lista dos arquivos de arte que o Preload carrega.
import * as ArteTiles from './tiles.js';
import * as ArteObjetos from './objetos.js';
import * as ArteHeroi from './heroi.js';

export { ArteTiles, ArteObjetos, ArteHeroi };

// Cenários (public/assets/cenario/<nome>.png). Os de Itajubá vieram do jogo do Aladdin (arte própria do Pedro);
// os novos saem de ferramentas/arte/gerar_cenarios.py.
export const CENARIO_PNG = [
  'ceu', 'morros', 'casas', 'fonte', 'cafe', 'igreja', 'estatua', 'helicoptero', 'arvore', 'arvore2', 'clube',
  'coroados', 'unifei', 'posto', 'rodoviaria', 'onibus', 'locomotiva', 'vagao1', 'vagao2', 'casa-joka',
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
  'npc-motorista': [48, 64],
  'npc-guia': [48, 64],
  'npc-vovo': [48, 64],
  'npc-vendedora': [48, 64],
  'npc-tecnico': [48, 64],
  'npc-atendente': [48, 64],
  'npc-barista': [48, 64],
  'npc-estudante': [48, 64],
};
