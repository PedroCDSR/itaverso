// Todos os textos exibidos no jogo (CLAUDE.md, seção 2, regra 6).
// Frases curtas: no máximo 2 linhas por caixa de diálogo. Tom leve, para crianças.
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
  teste: {
    titulo: 'ALADDIN',
    tocarJogar: 'Toque em JOGAR para começar',
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
  // Fase 2. Cada fala tem no máximo 2 linhas na caixa de diálogo (o modo dev avisa no console se passar).
  espaco: {
    nomeFase: 'Fase 2 · Espaço Paula De Marco',
    objetivo: 'Busque os ingressos com a Tia Claudia!',
    cartaz: 'ALADDIN · 20/11',
    balcao: 'INGRESSOS',
    ingressos: (n) => `+${n} ingressos!`,
    // ordem dos 'N' no mapa, da esquerda para a direita (levels/espaco.js)
    npcs: {
      jasmine: { nome: 'Jasmine', falas: ['Oi, Aladdin! Estou ensaiando o meu balé.', 'Olha só o meu giro!'] },
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
  // Tela provisória até a Fase 3 existir (Etapa 5): por enquanto ela leva direto ao Tapete
  chefe: {
    titulo: 'Fase 3 · Resgate',
    aviso: 'O Jafar levou a Tia Paula!',
    proxima: 'A luta contra o Jafar chega numa próxima etapa.',
    sapatilhas: (n, total) => `Sapatilhas: ${n} / ${total}`,
    ingressos: (n) => `Ingressos: ${n}`,
    continuar: 'CONTINUAR',
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
  final: {
    titulo: 'O ESPETÁCULO VAI COMEÇAR!',
    sapatilhas: 'Você pegou {n} sapatilhas!',
    provisorio: '(tela final provisória: a de verdade vem na Etapa 7)',
    ingressos: 'QUERO INGRESSOS',
    jogarDeNovo: 'JOGAR DE NOVO',
  },
};
