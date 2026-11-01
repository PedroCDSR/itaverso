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
  // Tela provisória até a Fase 2 existir (Etapa 4)
  emBreve: {
    titulo: 'Você chegou ao Espaço!',
    sapatilhas: (n) => `Sapatilhas: ${n}`,
    proxima: 'A Fase 2 chega na próxima etapa.',
    jogarDeNovo: 'JOGAR DE NOVO',
  },
};
