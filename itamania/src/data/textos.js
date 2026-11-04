// Todos os textos do jogo. Português do Brasil, frases curtas, no máximo 2 linhas por caixa de diálogo.
// Sem travessões. Marcação de gênero: {forma do Geraldo|forma da Helena} (ver src/genero.js). {nome} = nome do herói.
// Os nomes dos lugares reais vêm de src/data/vagas.js (versão real ou genérica).

export const TEXTOS = {
  jogo: 'ITAMANIA',
  subtitulo: 'uma aventura em Itajubá',
  escolha: 'Quem vai conhecer Itajubá?',
  botoes: {
    jogar: 'JOGAR',
    continuar: 'CONTINUAR',
    novo: 'NOVO JOGO',
    pular: 'PULAR',
    maca: 'PÃO', // botão de arremesso (o nome da chave vem do motor do Aladdin)
    mapa: 'MAPA',
    recomecar: 'RECOMEÇAR FASE',
    som: 'SOM',
    voltar: 'VOLTAR',
    jogarFase: 'JOGAR',
  },
  mobile: {
    girar: 'Gire o celular',
    girarDetalhe: 'O ITAMANIA é jogado com o celular deitado.',
    pausado: 'Pausado',
    tocarContinuar: 'Toque para continuar',
  },
  pausa: { titulo: 'PAUSA' },
  hud: { missao: 'Missão' },
  mapa: {
    titulo: 'ITAJUBÁ',
    embreve: 'Em breve!',
    dica: 'Toque numa fase liberada',
  },
  cartao: {
    titulo: 'Você sabia?',
    continuar: 'CONTINUAR',
  },
  avisos: {
    semBone: 'Ainda não comprei o boné amarelo!',
    semPoderes: 'Antes, vou provar o pão de queijo e o café com leite!',
    cresceu: 'Café com leite! Fiquei {forte|forte}!',
    encolheu: 'Ufa! O café com leite me protegeu.',
    retorno: 'Ponto de retorno!',
  },
  tutorial: {
    andarToque: 'Toque nas setas para andar',
    andarTeclado: 'Setas ou A e D para andar',
    pularToque: 'Toque em PULAR. Segure para ir mais alto!',
    pularTeclado: 'Espaço ou W para pular. Segure para ir mais alto!',
    paoToque: 'Toque em PÃO para jogar um pão de queijo',
    paoTeclado: 'X ou J para jogar um pão de queijo',
    pisar: 'Pule em cima para ele ir embora!',
  },
  final: {
    obrigado: 'Continua em breve!',
    detalhe: 'As próximas fases estão sendo construídas.',
  },
};

// Nomes das 14 fases no mapa (de baixo para cima) e a fase secreta.
export const NOMES_FASES = [
  null,
  'Rodoviária',
  'Praça do Soldado',
  'Rua Nova',
  'Praça Theodomiro Santiago',
  'Morro Chic',
  'Coroados',
  'Praçonha',
  'Cemitério',
  'UNIFEI',
  'Pinheirinho',
  'Agonia',
  'Kart',
  'Lago',
  'Prefeitura',
];
