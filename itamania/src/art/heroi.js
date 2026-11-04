// Herói do ITAMANIA: gerado por ferramentas/arte/gerar_heroi16.py a partir do desenho do Pedro (16x24).
// Folhas em public/assets/sprites/heroi-<geraldo|helena>-<normal|grande>.png (ampliadas 2x).
// Os primeiros NOMES.length quadros são sem boné; os seguintes, os mesmos com o boné amarelo.
export const TAMANHOS = {"normal": [32, 48], "grande": [32, 64]};
export const NOMES = ["parado", "piscando", "correndo1", "correndo2", "correndo3", "correndo4", "pulando", "caindo", "arremessando1", "arremessando2", "aterrissando", "dano", "vitoria1", "vitoria2"];
export const ANIMACOES = {
  parado: { quadros: ["parado", "parado", "parado", "parado", "parado", "parado", "parado", "piscando"], fps: 4, repetir: -1 },
  correndo: { quadros: ["correndo1", "correndo2", "correndo3", "correndo4"], fps: 10, repetir: -1 },
  pulando: { quadros: ["pulando"], fps: 1, repetir: 0 },
  caindo: { quadros: ["caindo"], fps: 1, repetir: 0 },
  arremessando: { quadros: ["arremessando1", "arremessando2", "arremessando2"], fps: 16, repetir: 0 },
  aterrissando: { quadros: ["aterrissando"], fps: 10, repetir: 0 },
  dano: { quadros: ["dano"], fps: 1, repetir: 0 },
  vitoria: { quadros: ["vitoria1", "vitoria2"], fps: 4, repetir: -1 },
};
