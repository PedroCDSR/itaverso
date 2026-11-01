// Ordem das cenas da partida:
// Título > Intro > Itajuba (Fase 1) > EmBreve (ponte provisória no lugar das Fases 2 e 3) > Tapete (Fase 4) > Final.
// Nas Etapas 4 e 5, as cenas Espaco e Chefe entram no lugar da EmBreve (o Chefe termina indo para o Tapete).
export const PRIMEIRA_FASE = 'Itajuba';
export const FINAL = 'Final';

// Cenas de jogo que o menu de pausa pode pausar (a mais alta ativa é a da vez).
export const FASES = ['Itajuba', 'Espaco', 'Chefe', 'Tapete'];
// Cenas sobrepostas que pausam e voltam junto com a fase.
export const SOBREPOSTAS = ['HUD'];

// Abre o menu de pausa por cima da fase que está rodando.
export function abrirPausa(scene) {
  const sm = scene.scene;
  if (sm.isActive('Pausa') || sm.isActive('Sobre')) return;
  const fase = FASES.find((k) => sm.get(k) && sm.isActive(k));
  if (!fase) return;
  sm.launch('Pausa', { cena: fase });
}
