// Ações dos botões do cartão do evento: WhatsApp, Instagram e Compartilhar.
// Tudo roda dentro do toque (pointerup do Botao), senão o navegador bloqueia a janela nova.
import { EVENTO, linkWhatsapp, URL_JOGO } from '../data/evento.js';

function abrir(url) {
  // Sem 'noopener' nas opções: com ele o window.open devolve sempre null e não dá para saber se abriu.
  const janela = window.open(url, '_blank');
  if (janela) janela.opener = null; // a página nova não mexe no jogo
  // bloqueador de janelas: abre na mesma aba
  else window.location.href = url;
}

export function abrirIngressos() {
  abrir(linkWhatsapp());
}

export function abrirInstagram() {
  abrir(EVENTO.instagram);
}

// Link do jogo para compartilhar: a página aberta (sem ?parâmetros), ou o endereço oficial fora da web.
export function linkDoJogo() {
  const { protocol, origin, pathname } = window.location;
  return protocol.startsWith('http') ? origin + pathname : URL_JOGO;
}

// Compartilhar: usa o menu do celular (navigator.share). Sem suporte, copia texto + link.
// Devolve 'compartilhou' | 'cancelou' | 'copiou' | 'falhou'.
export async function compartilhar(texto) {
  const url = linkDoJogo();
  if (navigator.share) {
    try {
      await navigator.share({ title: `${EVENTO.titulo} · ${EVENTO.escola}`, text: texto, url });
      return 'compartilhou';
    } catch (e) {
      if (e && e.name === 'AbortError') return 'cancelou';
      // outro erro (ex.: navegador recusou): tenta copiar
    }
  }
  return (await copiar(`${texto} ${url}`)) ? 'copiou' : 'falhou';
}

async function copiar(texto) {
  try {
    await navigator.clipboard.writeText(texto);
    return true;
  } catch {
    // navegadores antigos: copia por um campo de texto escondido
    try {
      const campo = document.createElement('textarea');
      campo.value = texto;
      campo.style.position = 'fixed';
      campo.style.opacity = '0';
      document.body.appendChild(campo);
      campo.select();
      const ok = document.execCommand('copy');
      campo.remove();
      return ok;
    } catch {
      return false;
    }
  }
}
