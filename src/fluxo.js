// Ordem das cenas da partida:
// Título > Intro > Itajuba (Fase 1) > Espaco (Fase 2) > Chefe (Fase 3) > Tapete (Fase 4) > Final.
// Cada fase chama a seguinte no próprio arquivo; aqui ficam só a primeira e o Final.
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
  sm.bringToTop('Pausa'); // algumas fases trazem o HUD para o topo; a pausa precisa ficar por cima dele
}
