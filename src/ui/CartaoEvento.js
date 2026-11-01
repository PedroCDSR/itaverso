import { LARGURA, ALTURA, CORES, CORES_CSS, FONTES } from '../config.js';
import { EVENTO } from '../data/evento.js';
import { TEXTOS } from '../data/textos.js';
import { Botao } from './Botao.js';

// Cartão com os dados do espetáculo (Título > Sobre, Pausa > Sobre e tela Final).
// botoes: lista de { rotulo, acao, cor }. Ficam em 2 colunas; com número ímpar, o 1º ocupa a linha inteira.
// extra: uma linha opcional de destaque (ex.: "Você pegou 7 sapatilhas!").
export function criarCartaoEvento(scene, { botoes, extra = null, profundidade = 0 }) {
  const c = TEXTOS.cartao;
  const L = 412; // estreito o bastante para não encostar no botão de som do canto
  const A = 254;
  const cx = LARGURA / 2;
  const topo = (ALTURA - A) / 2;
  const cont = scene.add.container(0, 0).setDepth(profundidade).setScrollFactor(0);

  const g = scene.add.graphics();
  g.fillStyle(CORES.roxo, 0.6).fillRoundedRect(cx - L / 2 + 3, topo + 3, L, A, 8);
  g.fillStyle(CORES.branco, 1).fillRoundedRect(cx - L / 2, topo, L, A, 8);
  g.lineStyle(3, CORES.roxo, 1).strokeRoundedRect(cx - L / 2, topo, L, A, 8);
  // faixa de cima em rosa, com os quadrados concêntricos (motivo do logo) nos cantos
  g.fillStyle(CORES.rosa, 1).fillRoundedRect(cx - L / 2 + 6, topo + 6, L - 12, 28, 5);
  for (const lado of [-1, 1]) {
    const qx = cx + lado * (L / 2 - 26);
    [12, 8, 4].forEach((r, i) => {
      g.fillStyle(i % 2 ? CORES.amarelo : CORES.lilas, 1).fillRoundedRect(qx - r, topo + 20 - r, r * 2, r * 2, 2);
    });
  }
  cont.add(g);

  const texto = (x, y, t, estilo) => {
    const obj = scene.add.text(x, y, t, estilo);
    cont.add(obj);
    return obj;
  };
  texto(cx, topo + 21, c.titulo, { fontFamily: FONTES.titulo, fontSize: '12px', color: CORES_CSS.roxo }).setOrigin(0.5);
  texto(cx, topo + 47, EVENTO.escola, { fontFamily: FONTES.dialogo, fontSize: '16px', color: CORES_CSS.roxo }).setOrigin(0.5);

  const linhas = [
    [c.rotuloData, EVENTO.data],
    [c.rotuloHorario, EVENTO.horario],
    [c.rotuloLocal, EVENTO.local],
    [c.rotuloIngresso, EVENTO.ingresso],
  ];
  const xRotulo = cx - L / 2 + 24;
  const xValor = xRotulo + 82;
  linhas.forEach(([rotulo, valor], i) => {
    const y = topo + 64 + i * 19;
    texto(xRotulo, y, rotulo, { fontFamily: FONTES.titulo, fontSize: '8px', color: CORES_CSS.roxo }).setOrigin(0, 0.5);
    texto(xValor, y, valor, { fontFamily: FONTES.dialogo, fontSize: '16px', color: '#3A2F7A' }).setOrigin(0, 0.5);
  });

  if (extra) {
    texto(cx, topo + 146, extra, { fontFamily: FONTES.titulo, fontSize: '8px', color: CORES_CSS.roxo })
      .setOrigin(0.5)
      .setBackgroundColor(CORES_CSS.amarelo)
      .setPadding(6, 4, 6, 3);
  }

  // botões: 2 colunas, de baixo para cima a partir da base do cartão
  const larg = 196;
  const alt = 30;
  const passo = 38;
  const yBase = topo + A - 26;
  const lista = [...botoes];
  const objetos = [];
  const linhasBotoes = Math.ceil(lista.length / 2);
  let i = 0;
  if (lista.length % 2 === 1) {
    const b = lista[i++];
    const y = yBase - (linhasBotoes - 1) * passo;
    objetos.push(new Botao(scene, cx, y, b.rotulo, b.acao, { largura: larg * 2 + 12, altura: alt, cor: b.cor || 'lilas' }));
  }
  for (let linha = lista.length % 2; i < lista.length; linha++) {
    const y = yBase - (linhasBotoes - 1 - linha) * passo;
    for (const lado of [-1, 1]) {
      const b = lista[i++];
      if (!b) break;
      objetos.push(new Botao(scene, cx + lado * (larg / 2 + 6), y, b.rotulo, b.acao, { largura: larg, altura: alt, cor: b.cor || 'lilas' }));
    }
  }
  objetos.forEach((b) => cont.add(b.container));
  return { container: cont, botoes: objetos };
}

