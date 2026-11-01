// Todos os textos exibidos no jogo (CLAUDE.md, seção 2, regra 6).
// Frases curtas: no máximo 2 linhas por caixa de diálogo. Tom leve, para crianças.
export const TEXTOS = {
  // Fase 3, Resgate (chefe)
  chefe: {
    nomeFase: 'Fase 3 · Resgate',
    nomeJafar: 'Jafar',
    nomePaula: 'Tia Paula',
    jafarEntrada: 'Ha! Sem a Tia Paula, nada de espetáculo!',
    paulaSocorro: 'Socorro!',
    paulaAntes: ['Aladdin! Quando o Jafar cansar e descer, acerte maçãs nele!'],
    objetivo: 'Acerte maçãs no Jafar quando ele cansar!',
    dicaCansado: 'Agora! Jogue maçãs!',
    nomeChefe: 'JAFAR',
    ai: 'ai!',
    semMaca: 'Pegue maçãs no chão!',
    jafarDerrotado: 'Nããão! Puf!',
    paulaObrigada: ['Obrigada, Aladdin! Você foi muito corajoso!', 'Vamos de tapete mágico até o teatro. O espetáculo não pode atrasar!'],
  },
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
      'Aladdin estava passeando por Itajubá quando viu um cartaz enorme...',
      'Vai ter o espetáculo Aladdin no Teatro do Colégio G9!',
      'Mas os ingressos estão no Espaço Paula De Marco. Bora buscar!',
    ],
    proximo: 'PRÓXIMO',
    comecar: 'COMEÇAR',
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
      'Muito obrigada, Aladdin! Agora sim, todo mundo no teatro!',
      'Senhoras e senhores... o espetáculo Aladdin vai começar!',
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
  // Tutorial do começo da Fase 1 (ui/Tutorial.js): frases curtas, para quem nunca jogou.
  tutorial: {
    andarToque: 'Segure aqui para andar!',
    andarTeclado: 'Use as setas do teclado para andar!',
    pularToque: 'Toque em PULAR para pular!',
    pularTeclado: 'Aperte ESPAÇO para pular!',
    macaToque: 'Toque em MAÇÃ para jogar uma maçã!',
    macaTeclado: 'Aperte X para jogar uma maçã!',
    capivara: 'Pule em cima da capivara para ela dormir!',
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
  // Fase 2. Cada fala tem no máximo 2 linhas na caixa de diálogo (o modo dev avisa no console se passar).
  espaco: {
    nomeFase: 'Fase 2 · Espaço Paula De Marco',
    objetivo: 'Busque os ingressos com a Tia Claudia!',
    cartaz: 'ALADDIN · 20/11',
    balcao: 'INGRESSOS',
    ingressos: (n) => `+${n} ingressos!`,
    // ordem dos 'N' no mapa, da esquerda para a direita (levels/espaco.js)
    npcs: {
      jasmine: { nome: 'Jasmine', falas: ['Oi, Aladdin! Estou ensaiando o meu balé.', 'Olha só a minha pirueta!'] },
      genio: { nome: 'Gênio', falas: ['Três desejos? Hoje só um:', 'que você venha ver a gente no palco!'] },
      sultao: { nome: 'Sultão', falas: ['Ensaio é coisa séria...', 'mas dançar é muito divertido!'] },
    },
    claudia: {
      nome: 'Tia Claudia',
      antes: ['Aladdin! Que bom que você chegou!', 'Aqui estão os ingressos para o espetáculo do dia 20/11!'],
      depois: ['Guarde bem! A gente se vê no Teatro do Colégio G9.'],
    },
    abu: { nome: 'Abu', falas: ['Socorro! Socorro!', 'O Jafar levou a Tia Paula!'] },
    final: {
      nome: 'Tia Claudia',
      falas: ['Sem a Tia Paula não tem espetáculo!', 'Corre, Aladdin! Vai salvar a Tia Paula!'],
    },
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
