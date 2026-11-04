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
    maca: 'PÃO', // botão de arremesso (o nome da chave vem do motor original)
    mapa: 'MAPA',
    menu: 'MENU',
    praca: 'PRAÇA',
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
  // Praça andável (Centro explorável, vista de cima). Falas por chave (a mesma do mapa praca.tmj, propriedade "fala").
  praca: {
    botao: 'FALAR',
    chegada: [{ quem: 'heroi', texto: 'Cheguei em Itajubá! Vou dar uma volta na praça para conhecer a cidade.' }],
    dicaToque: 'Arraste o dedo à esquerda para andar. FALAR conversa.',
    dicaTeclado: 'Setas para andar. Espaço para conversar.',
    falas: {
      guia: [
        { quem: 'Guia da praça', texto: 'Bem-vind{o|a} à Praça Theodomiro Santiago, o coração do centro!' },
        { quem: 'Guia da praça', texto: 'A estátua da fonte lembra quem fundou a escola de engenharia daqui.' },
        { quem: 'heroi', texto: 'Uma escola de engenharia? Quero saber mais!' },
      ],
      vovo: [
        { quem: 'Dona Cida', texto: 'Ai, que delícia sentar aqui na sombra e ver a fonte.' },
        { quem: 'Dona Cida', texto: 'Já provou o pão de queijo da praça? É o melhor da cidade!' },
      ],
      barista: [
        { quem: 'Barista', texto: 'Oi! Aqui é o {cafe}. O café com leite sai quentinho!' },
        { quem: 'Barista', texto: 'Volte depois, que vou te contar um segredo dele.' },
      ],
      atendente: [
        { quem: 'Atendente', texto: 'Bem-vind{o|a} ao {lanchonete}! O cheiro de pão de queijo chega longe, né?' },
      ],
      estudante: [
        { quem: 'Estudante', texto: 'Eu estudo engenharia na UNIFEI.' },
        { quem: 'Estudante', texto: 'Muita gente de lá vai trabalhar na fábrica de helicópteros!' },
        { quem: 'heroi', texto: 'Helicóptero feito aqui? Que demais!' },
      ],
      fonte: [
        { quem: 'Placa da fonte', texto: 'Theodomiro Santiago fundou aqui, em 1913, uma escola de engenharia.' },
        { quem: 'Placa da fonte', texto: 'Hoje ela se chama UNIFEI.' },
      ],
      clube: [{ quem: 'Placa', texto: 'Club Itajubense.' }],
      cafe: [{ quem: 'Placa', texto: '{cafe}.' }],
      burg: [{ quem: 'Placa', texto: '{lanchonete}.' }],
      placaSaida: [{ quem: 'Placa', texto: 'Para baixo: Rua Nova e o mapa da cidade.' }],
      gato: [{ quem: 'heroi', texto: 'Um gatinho! Ele nem liga para mim.' }],
    },
    saida: 'Ir para o mapa da cidade?',
    moedas: 'Achei uma itacoin!',
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
