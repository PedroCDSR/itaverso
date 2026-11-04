// Herói do ITAMANIA: gerado por ferramentas/arte/gerar_heroi.py (não editar à mão).
// Folhas PNG em public/assets/sprites/heroi-<geraldo|helena>-<normal|turbinado>.png, quadros de 48x64.
// Os primeiros NOMES.length quadros são sem boné; os seguintes, os mesmos com o boné amarelo.
export const LARGURA = 48;
export const ALTURA = 64;
export const NOMES = ["parado1", "parado2", "parado3", "parado4", "piscando", "correndo1", "correndo2", "correndo3", "correndo4", "correndo5", "correndo6", "correndo7", "correndo8", "pulando1", "pulando2", "caindo1", "caindo2", "arremessando1", "arremessando2", "arremessando3", "aterrissando", "dano", "vitoria1", "vitoria2"];
export const ANIMACOES = {
  parado: { quadros: ["parado1", "parado2", "parado3", "parado4", "parado1", "parado2", "parado3", "parado4", "piscando"], fps: 4, repetir: -1 },
  correndo: { quadros: ["correndo1", "correndo2", "correndo3", "correndo4", "correndo5", "correndo6", "correndo7", "correndo8"], fps: 16, repetir: -1 },
  pulando: { quadros: ["pulando1", "pulando2"], fps: 8, repetir: 0 },
  caindo: { quadros: ["caindo1", "caindo2"], fps: 6, repetir: -1 },
  arremessando: { quadros: ["arremessando1", "arremessando2", "arremessando3"], fps: 16, repetir: 0 },
  aterrissando: { quadros: ["aterrissando"], fps: 10, repetir: 0 },
  dano: { quadros: ["dano"], fps: 1, repetir: 0 },
  vitoria: { quadros: ["vitoria1", "vitoria2"], fps: 4, repetir: -1 },
};
