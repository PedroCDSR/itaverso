// Estado da partida, guardado no registry do Phaser (vale para todas as cenas).
// sapatilhas: quantas o jogador pegou (aparece no Final e no texto do COMPARTILHAR).

export function novaPartida(scene) {
  scene.registry.set('sapatilhas', 0);
}

export function sapatilhas(scene) {
  return scene.registry.get('sapatilhas') || 0;
}

