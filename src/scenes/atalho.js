// Atalho para testar uma fase direto pelo endereço, sem jogar as anteriores:
//   ?fase=chefe   abre a Fase 3 (Resgate)
//   ?fase=tapete  abre a Fase 4 (Tapete)
// Sem o parâmetro (ou com um nome desconhecido), começa pela cena padrão.
const FASES = { chefe: 'Chefe', tapete: 'Tapete' };

export function cenaInicial(padrao) {
  try {
    const fase = new URLSearchParams(window.location.search).get('fase');
    return FASES[fase?.toLowerCase()] ?? padrao;
  } catch {
    return padrao;
  }
}
