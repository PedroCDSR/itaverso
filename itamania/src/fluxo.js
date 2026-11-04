// Abre o menu de pausa por cima da cena que está rodando (Fase ou Praca); ela e o HUD pausam juntos.
// A cena de jogo atual fica no registry ('cenaJogo').
export function abrirPausa(scene) {
  const sm = scene.scene;
  const cena = scene.registry.get('cenaJogo') || 'Fase';
  if (sm.isActive('Pausa') || !sm.isActive(cena)) return;
  sm.launch('Pausa', { cena });
  sm.bringToTop('Pausa');
}
