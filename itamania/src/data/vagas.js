// Vagas: pessoas e lugares reais (DESIGN.md, "Vagas"). O jogo funciona sempre com a versão genérica; a real só
// entra com autorização. Em 04/11/2026 o Pedro autorizou os nomes e logos dos comércios de Itajubá (ele tem o OK
// dos donos), então Casa Joka, Cesar Burg e Café do Vadinho entram como reais. A fábrica de helicópteros continua
// genérica (não entrou na autorização). Para voltar à versão genérica de um lugar, troque `real` para false.

export const VAGAS = {
  loja: { real: true, nome: 'Casa Joka', generico: 'a loja de bonés', imagem: 'casa-joka', imagemGenerica: 'loja-bones' },
  lanchonete: { real: true, nome: 'Cesar Burg', generico: 'a lanchonete da praça', imagem: 'cesar-burg', imagemGenerica: 'lanchonete' },
  cafe: { real: true, nome: 'Café do Vadinho', generico: 'o café da praça', imagem: 'cafe', imagemGenerica: 'cafe-generico' },
  fabrica: { real: false, nome: 'Helibras', generico: 'a fábrica de helicópteros' },
  // personagem histórico, em versão respeitosa (busto da praça e narração)
  theodomiro: { real: true, nome: 'Theodomiro Santiago', generico: 'o fundador da escola de engenharia' },
};

// Nome que aparece no jogo: o real (se autorizado) ou o genérico.
export function nomeVaga(chave) {
  const v = VAGAS[chave];
  return v.real ? v.nome : v.generico;
}
