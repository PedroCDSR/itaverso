// Todos os textos do jogo. Português do Brasil, frases curtas, no máximo 2 linhas por caixa de diálogo.
// Sem travessões. Marcação de gênero: {forma do Geraldo|forma da Helena} (ver src/genero.js). {nome} = nome do herói.
// Os nomes dos lugares reais vêm de src/data/vagas.js (versão real ou genérica).

export const TEXTOS = {
  jogo: 'ITAMANIA',
  subtitulo: 'uma aventura em Itajubá',
  creditos: 'Arte da cidade: LimeZu (limezu.itch.io) e Pixel-boy (Ninja Adventure)',
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
    nomeHeroi: 'Capivara exploradora',
    explorar: 'EXPLORAR A PRAÇA',
    apresentacao: 'Mochila pronta. Itajubá me espera!',
    chamada: 'Conheça os cantinhos da cidade',
    personagem: 'CAPIVARA EXPLORADORA',
    botao: 'FALAR',
    chegada: [{ quem: 'heroi', texto: 'Mochila e lenço prontos! Vou conhecer a praça, conversar e procurar itacoins.' }],
    dicaToque: 'Arraste o dedo à esquerda para andar. FALAR conversa.',
    dicaTeclado: 'Setas para andar. Espaço para conversar.',
    falas: {
      guia: [
        { quem: 'Guia da praça', texto: 'Bem-vind{o|a} à Praça Theodomiro Santiago, o coração do centro!' },
        { quem: 'Guia da praça', texto: 'Leia a placa perto do espelho d\'água. Ela conta uma história importante!' },
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
      fonte: [{ quem: 'heroi', texto: 'Que fonte bonita! Dá vontade de jogar uma moedinha.' }],
      clube: [{ quem: 'Placa', texto: 'Club Itajubense. Bailes e festas desde muito tempo!' }],
      hotel: [{ quem: 'Placa', texto: 'Hotel Centenário.' }],
      concha: [{ quem: 'heroi', texto: 'Uma concha acústica! Aposto que tem show aqui nas festas da cidade.' }],
      g5: [{ quem: 'Placa', texto: 'G5 Internet.' }],
      torre: [{ quem: 'heroi', texto: 'Que prédio alto! E cheio de lojinhas embaixo.' }],
      forum: [{ quem: 'Placa', texto: 'Fórum Cível.' }],
      acai: [{ quem: 'heroi', texto: 'Uma loja de açaí! Depois eu volto aqui.' }],
      arena: [{ quem: 'heroi', texto: 'O Five Stars! O pessoal vem aqui ver os jogos no telão.' }],
      placa: [
        { quem: 'Placa da praça', texto: 'Praça Theodomiro Santiago.' },
        { quem: 'Placa da praça', texto: 'Theodomiro fundou aqui, em 1913, a escola de engenharia que hoje é a UNIFEI.' },
      ],
      carteiro: [
        { quem: 'Carteiro', texto: 'Bom dia! Conheço cada rua desta cidade.' },
        { quem: 'Carteiro', texto: 'Desça pela rua de baixo para ver o mapa de Itajubá.' },
      ],
      cafe: [{ quem: 'Placa', texto: '{cafe}.' }],
      burg: [{ quem: 'Placa', texto: '{lanchonete}.' }],
      placaSaida: [{ quem: 'Placa', texto: 'Para baixo: Rua Nova e o mapa da cidade.' }],
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
