import { ArteTiles } from '../art/index.js';

// Lê um mapa em texto (CLAUDE.md, seção 10) e devolve tiles + objetos.
//
// Tiles: '#' bloco sólido, '=' plataforma que se atravessa por baixo, 'T' toldo.
// Objetos: 'F' fonte, 'C' capivara, 'a' maçã, 's' sapatilha, 'h' coração, 'K' checkpoint, 'P' início, 'E' saída.
// x/y dos objetos ficam no CENTRO-BAIXO do tile, em pixels (prontos para posicionar sprites "em pé").

const OBJETOS = { F: 'fonte', C: 'capivara', a: 'maca', s: 'sapatilha', h: 'coracao', K: 'checkpoint', P: 'inicio', E: 'saida' };
const T = Object.fromEntries(ArteTiles.ORDEM.map((nome, i) => [nome, i]));

export const TIPO_TILE = { vazio: -1, chaoTopo: T.chaoTopo, chao: T.chao, plataforma: T.plataforma, toldo: T.toldo };

export function lerMapa(linhas, nome = 'mapa') {
  const largura = linhas[0].length;
  linhas.forEach((l, y) => {
    if (l.length !== largura) {
      throw new Error(`${nome}: a linha ${y + 1} tem ${l.length} caracteres, mas a primeira tem ${largura}`);
    }
  });

  const tamanho = ArteTiles.TAMANHO;
  const tiles = [];
  const objetos = [];
  let inicio = null;

  linhas.forEach((linha, y) => {
    const fila = [];
    for (let x = 0; x < largura; x++) {
      const c = linha[x];
      let tile = TIPO_TILE.vazio;
      if (c === '#') {
        // bloco com o de cima vazio ganha o "topo" iluminado
        const acima = y > 0 ? linhas[y - 1][x] : '.';
        tile = acima === '#' ? TIPO_TILE.chao : TIPO_TILE.chaoTopo;
      } else if (c === '=') {
        tile = TIPO_TILE.plataforma;
      } else if (c === 'T') {
        tile = TIPO_TILE.toldo;
      } else if (OBJETOS[c]) {
        const obj = { tipo: OBJETOS[c], col: x, lin: y, x: x * tamanho + tamanho / 2, y: (y + 1) * tamanho };
        if (c === 'P') inicio = obj;
        else objetos.push(obj);
      } else if (c !== '.') {
        throw new Error(`${nome}: caractere '${c}' desconhecido na linha ${y + 1}, coluna ${x + 1}`);
      }
      fila.push(tile);
    }
    tiles.push(fila);
  });

  if (!inicio) throw new Error(`${nome}: falta o 'P' (início do jogador)`);
  return {
    nome,
    tiles,
    objetos,
    inicio,
    colunas: largura,
    linhas: linhas.length,
    larguraPx: largura * tamanho,
    alturaPx: linhas.length * tamanho,
  };
}
