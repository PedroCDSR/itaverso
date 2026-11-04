// Ajuda a montar os mapas em texto (17 linhas × N colunas; chão nas 2 últimas linhas, topo da rua em y = 240).
// O resultado é a mesma lista de strings do leitor (src/levels/leitor.js); dá para imprimir com
// `console.log(mapa.join('\n'))` e conferir.
export const LINHAS = 17;
export const CHAO = 15; // primeira linha do chão

export function construir(colunas, desenhar) {
  const m = Array.from({ length: LINHAS }, (_, l) => Array(colunas).fill(l >= CHAO ? '#' : '.'));
  const api = {
    set(c, l, ch) {
      if (l >= 0 && l < LINHAS && c >= 0 && c < colunas) m[l][c] = ch;
    },
    ret(c0, l0, c1, l1, ch) {
      for (let l = l0; l <= l1; l++) for (let c = c0; c <= c1; c++) api.set(c, l, ch);
    },
    linha(c0, c1, l, ch) {
      api.ret(c0, l, c1, l, ch);
    },
    // buraco no chão (cair = volta ao ponto de retorno)
    buraco(c0, c1) {
      api.ret(c0, CHAO, c1, LINHAS - 1, '.');
    },
    // fileira de itacoins (a cada `passo` colunas)
    moedas(c0, c1, l, passo = 1) {
      for (let c = c0; c <= c1; c += passo) api.set(c, l, 'o');
    },
    // arco de itacoins sobre um pulo (meio mais alto)
    arco(c0, c1, l) {
      const meio = (c0 + c1) / 2;
      for (let c = c0; c <= c1; c++) api.set(c, l - Math.round(2 - (Math.abs(c - meio) / ((c1 - c0) / 2 || 1)) * 2), 'o');
    },
  };
  desenhar(api);
  return m.map((r) => r.join(''));
}
