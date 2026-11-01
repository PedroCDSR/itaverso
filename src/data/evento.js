// Dados do espetáculo e links (CLAUDE.md, seção 6). Edite aqui; o jogo inteiro lê deste arquivo.
export const EVENTO = {
  titulo: 'Aladdin',
  escola: 'Paula De Marco Espaço de Artes',
  data: 'Sexta-feira, 20 de novembro de 2026',
  horario: 'A DEFINIR',
  local: 'Teatro do Colégio G9, Itajubá/MG',
  ingresso: 'A DEFINIR (valor e forma de compra)',
  whatsapp: '553584713436',
  mensagemWhatsapp:
    'Oi! Vim pelo jogo do Aladdin e quero saber dos ingressos para o espetáculo do dia 20/11.',
  instagram: 'https://www.instagram.com/espacodeartespaulademarco/',
};

// Link do botão QUERO INGRESSOS: abre o WhatsApp da escola com a mensagem pronta.
export function linkWhatsapp() {
  return `https://wa.me/${EVENTO.whatsapp}?text=${encodeURIComponent(EVENTO.mensagemWhatsapp)}`;
}
