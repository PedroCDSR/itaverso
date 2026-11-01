// Converte sprites em matriz de texto (um caractere por pixel) em texturas do Phaser.
// Quando existir um PNG final em public/assets/sprites/, ele é usado no lugar (ver SPRITES_PNG em art/index.js).

// Desenha uma matriz num contexto 2D, a partir de (x0, y0).
function pintar(ctx, linhas, paleta, x0, y0) {
  linhas.forEach((linha, y) => {
    for (let x = 0; x < linha.length; x++) {
      const c = linha[x];
      if (c === '.') continue;
      const cor = paleta[c];
      if (!cor) throw new Error(`Cor '${c}' não está na paleta (linha ${y + 1}, coluna ${x + 1})`);
      ctx.fillStyle = cor;
      ctx.fillRect(x0 + x, y0 + y, 1, 1);
    }
  });
}

// Cria uma textura com vários quadros lado a lado, numerados 0, 1, 2... na ordem da lista.
// quadros: lista de matrizes (cada uma = lista de strings do mesmo tamanho)
export function texturaDeQuadros(scene, chave, quadros, paleta, largura, altura) {
  if (scene.textures.exists(chave)) return;
  const tex = scene.textures.createCanvas(chave, largura * quadros.length, altura);
  const ctx = tex.getContext();
  quadros.forEach((linhas, i) => {
    if (!linhas) return; // quadro vazio (ex.: tile 0)
    if (linhas.length !== altura || linhas.some((l) => l.length !== largura)) {
      throw new Error(`Quadro ${i} de '${chave}' não tem ${largura}x${altura}`);
    }
    pintar(ctx, linhas, paleta, i * largura, 0);
  });
  tex.refresh();
  quadros.forEach((_, i) => tex.add(i, 0, i * largura, 0, largura, altura));
}
