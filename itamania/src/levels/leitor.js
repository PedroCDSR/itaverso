import { TILE } from '../config.js';

// Lê um mapa em texto e devolve tiles + objetos. Todas as linhas têm o mesmo comprimento.
//
// Tiles:   '#' chão/bloco sólido   '=' plataforma (atravessa por baixo)   'T' toldo (quica)
//          'x' sólido invisível (em cima de prédios e do trem)   '-' plataforma invisível
// Objetos: 'o' itacoin   'h' coração   'p' pão de queijo   'c' café com leite
//          'C' capivara  'V' pombo     'K' ponto de retorno  'P' início   'E' saída
//          'N' personagem que conversa (quem é cada um vem da lista `npcs` da fase, na ordem, da esquerda p/ direita)
//          'G' gatilho de evento (lista `gatilhos` da fase, na mesma ordem)
// x/y dos objetos = CENTRO-BAIXO do tile, em pixels.

export const TIPO_TILE = { vazio: -1, chaoTopo: 1, chao: 2, plataforma: 3, toldo: 4, invisivel: 5, plataformaInvisivel: 6 };

const OBJETOS = {
  o: 'itacoin', h: 'coracao', p: 'pao', c: 'cafe', C: 'capivara', V: 'pombo',
  K: 'retorno', P: 'inicio', E: 'saida', N: 'npc', G: 'gatilho',
};

export function lerMapa(linhas, nome = 'mapa') {
  const largura = linhas[0].length;
  linhas.forEach((l, y) => {
    if (l.length !== largura) throw new Error(`${nome}: a linha ${y + 1} tem ${l.length} caracteres, a primeira tem ${largura}`);
  });
  const tiles = [];
  const objetos = [];
  let inicio = null;
  linhas.forEach((linha, y) => {
    const fila = [];
    for (let x = 0; x < largura; x++) {
      const c = linha[x];
      let tile = TIPO_TILE.vazio;
      if (c === '#') {
        const acima = y > 0 ? linhas[y - 1][x] : '.';
        tile = acima === '#' ? TIPO_TILE.chao : TIPO_TILE.chaoTopo;
      } else if (c === '=') tile = TIPO_TILE.plataforma;
      else if (c === 'T') tile = TIPO_TILE.toldo;
      else if (c === 'x') tile = TIPO_TILE.invisivel;
      else if (c === '-') tile = TIPO_TILE.plataformaInvisivel;
      else if (OBJETOS[c]) {
        const obj = { tipo: OBJETOS[c], col: x, lin: y, x: x * TILE + TILE / 2, y: (y + 1) * TILE };
        if (c === 'P') inicio = obj;
        else objetos.push(obj);
      } else if (c !== '.') {
        throw new Error(`${nome}: caractere '${c}' desconhecido na linha ${y + 1}, coluna ${x + 1}`);
      }
      fila.push(tile);
    }
    tiles.push(fila);
  });
  if (!inicio) throw new Error(`${nome}: falta o 'P' (início do herói)`);
  // ordem da esquerda para a direita (NPCs e gatilhos casam com as listas da fase nessa ordem)
  objetos.sort((a, b) => a.col - b.col || a.lin - b.lin);
  return { nome, tiles, objetos, inicio, colunas: largura, linhas: linhas.length, larguraPx: largura * TILE, alturaPx: linhas.length * TILE };
}
