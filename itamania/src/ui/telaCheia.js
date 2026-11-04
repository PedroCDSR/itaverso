// Tela cheia OPCIONAL, pelo botão do menu de pausa (decisão do Pedro, 01/11/2026).
// O jogo não entra mais em tela cheia sozinho: no Android o Chrome mostra por vários segundos a faixa
// "Para sair da tela cheia..." e ela atrapalhava o começo do jogo. Também não travamos a orientação.
// No iPhone a página não tem tela cheia: o botão nem aparece.
// Quem quiser o jogo sem barras pode usar "Adicionar à tela inicial" (public/manifest.webmanifest).

export function telaCheiaDisponivel(scene) {
  return scene.scale.fullscreen.available;
}

export function estaEmTelaCheia(scene) {
  return scene.scale.isFullscreen;
}

// Só funciona dentro de um toque (pointerup do Botao).
export function alternarTelaCheia(scene) {
  const escala = scene.scale;
  if (!escala.fullscreen.available) return;
  try {
    if (escala.isFullscreen) escala.stopFullscreen();
    else escala.startFullscreen({ navigationUI: 'hide' });
  } catch {
    // navegador recusou: segue sem tela cheia
  }
}
