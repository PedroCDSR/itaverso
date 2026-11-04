// Abre o menu de pausa por cima da fase que está rodando (a fase e o HUD pausam juntos).
export function abrirPausa(scene) {
  const sm = scene.scene;
  if (sm.isActive('Pausa') || !sm.isActive('Fase')) return;
  sm.launch('Pausa');
  sm.bringToTop('Pausa');
}
