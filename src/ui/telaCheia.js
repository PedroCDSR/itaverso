// Tela cheia ao tocar em JOGAR (só funciona dentro de um toque).
// No Android funciona e ainda trava o celular deitado. No iPhone a página não tem tela cheia:
// a função simplesmente não faz nada e o jogo segue normal.
export function tentarTelaCheia(scene) {
  const escala = scene.scale;
  const toque = scene.sys.game.device.input.touch;
  if (!toque || !escala.fullscreen.available || escala.isFullscreen) return;
  try {
    escala.startFullscreen({ navigationUI: 'hide' });
    // a trava de orientação só é aceita depois que a tela cheia começou
    setTimeout(() => {
      if (screen.orientation && screen.orientation.lock) {
        screen.orientation.lock('landscape').catch(() => {});
      }
    }, 300);
  } catch {
    // navegador recusou: segue sem tela cheia
  }
}
