// Herói escolhido (Geraldo ou Helena) e troca das marcações de gênero nos textos.
// Nos textos, `{animado|animada}` vira a 1ª forma para o Geraldo e a 2ª para a Helena.
// `{nome}` vira o nome do herói.

export const HEROIS = {
  geraldo: { nome: 'Geraldo', indice: 0 },
  helena: { nome: 'Helena', indice: 1 },
};

let atual = 'geraldo';

export function heroi() {
  return atual;
}

export function escolherHeroi(chave) {
  if (HEROIS[chave]) atual = chave;
}

export function nomeHeroi() {
  return HEROIS[atual].nome;
}

// Troca as marcações de um texto (ou de cada texto de uma lista).
export function g(texto) {
  if (Array.isArray(texto)) return texto.map(g);
  const i = HEROIS[atual].indice;
  return texto
    .replace(/\{nome\}/g, nomeHeroi())
    .replace(/\{([^{}|]*)\|([^{}|]*)\}/g, (_, a, b) => (i === 0 ? a : b));
}
