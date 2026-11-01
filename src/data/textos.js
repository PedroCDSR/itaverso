// Todos os textos exibidos no jogo (CLAUDE.md, seção 2, regra 6).
// Frases curtas: no máximo 2 linhas por caixa de diálogo. Tom leve, para crianças.
// Use \n para quebrar a linha dentro de uma caixa.
export const TEXTOS = {
  mobile: {
    girar: 'Gire o celular',
    girarDetalhe: 'O jogo é com o celular deitado.',
    pausado: 'Pausado',
    tocarContinuar: 'Toque para continuar',
  },
  botoes: {
    jogar: 'JOGAR',
    pular: 'PULAR',
    maca: 'MAÇÃ',
  },

  // Tela de título
  titulo: {
    jogo: 'ALADDIN',
    subtitulo: 'o jogo do espetáculo',
    jogar: 'JOGAR',
    sobre: 'SOBRE O ESPETÁCULO',
    rodape: '20/11 · Teatro do Colégio G9 · Itajubá',
    dicaTeclado: 'Setas: andar · Espaço: pular · X: maçã · Esc: pausa',
  },

  // Intro: 3 caixas. Toque para avançar.
  intro: {
    caixas: [
      'Aladdin estava passeando por Itajubá\nquando viu um cartaz enorme...',
      'Vai ter o espetáculo Aladdin\nno Teatro do Colégio G9!',
      'Mas os ingressos estão no Espaço\nPaula De Marco. Bora buscar!',
    ],
    pular: 'PULAR',
    tocar: 'toque para continuar',
  },

  // Cartão com os dados do espetáculo (título, pausa e final)
  cartao: {
    titulo: 'ESPETÁCULO ALADDIN',
    rotuloData: 'Quando',
    rotuloHorario: 'Horário',
    rotuloLocal: 'Onde',
    rotuloIngresso: 'Ingresso',
    ingressos: 'QUERO INGRESSOS',
    compartilhar: 'COMPARTILHAR',
    instagram: 'INSTAGRAM',
    jogarDeNovo: 'JOGAR DE NOVO',
    voltar: 'VOLTAR',
    linkCopiado: 'Link copiado!',
    naoCopiou: 'Não deu certo',
  },

  // Tela final
  final: {
    falaTiaPaula: [
      'Tia Paula: Muito obrigada, Aladdin!\nAgora sim, todo mundo no teatro!',
      'Senhoras e senhores...\no espetáculo Aladdin vai começar!',
    ],
    // {n} = quantidade de sapatilhas
    sapatilhas: 'Você pegou {n} sapatilhas!',
    sapatilha1: 'Você pegou 1 sapatilha!',
    // texto do COMPARTILHAR; o link do jogo vai junto
    compartilhar: 'Peguei {n} sapatilhas no jogo do Aladdin da Paula De Marco! Jogue também:',
    compartilhar1: 'Peguei 1 sapatilha no jogo do Aladdin da Paula De Marco! Jogue também:',
  },

  // Menu de pausa
  pausa: {
    titulo: 'PAUSA',
    continuar: 'CONTINUAR',
    somLigado: 'SOM: LIGADO',
    somDesligado: 'SOM: DESLIGADO',
    telaCheia: 'TELA CHEIA',
    sairTelaCheia: 'SAIR DA TELA CHEIA',
    sobre: 'SOBRE O ESPETÁCULO',
    pularFinal: 'PULAR PARA O FINAL',
  },

  teste: {
    dicaTeclado: 'Setas ou A/D: andar · Espaço ou W: pular · X ou J: maçã · Esc: pausa',
  },
  itajuba: {
    nomeFase: 'Fase 1 · Itajubá',
    objetivo: 'Chegue ao Espaço Paula De Marco!',
    placaEspaco: 'ESPAÇO PAULA DE MARCO',
    zzz: 'zzz',
    nham: 'nham!',
    checkpoint: 'Ponto salvo!',
    semMaca: 'Sem maçãs!',
  },
  // Ponte provisória no lugar das Fases 2 e 3 (Etapas 4 e 5)
  emBreve: {
    titulo: 'Você chegou ao Espaço!',
    sapatilhas: (n) => `Sapatilhas: ${n}`,
    proxima: 'O Espaço e o resgate da Tia Paula\nchegam nas próximas etapas. Agora, de tapete!',
    continuar: 'VOAR DE TAPETE',
  },
  tapete: {
    titulo: 'VOANDO PARA O TEATRO!',
    dicaToque: 'Segure a tela para subir. Solte para descer.',
    dicaTeclado: 'Segure espaço, W ou seta para cima para subir. Solte para descer.',
    comecarToque: 'Toque para voar',
    comecarTeclado: 'Aperte espaço para voar',
    perdeu: '-{n}',
    teatro: 'TEATRO',
    teatroNome: 'Colégio G9',
    chegou: 'Chegamos ao Teatro do Colégio G9!',
  },
};

// Troca {n} pelo número, usando o texto no singular quando n = 1.
export function comNumero(plural, singular, n) {
  return n === 1 ? singular : plural.replace('{n}', n);
}
