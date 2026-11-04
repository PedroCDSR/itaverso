// Espera `ms` no relógio da cena (para junto com a pausa).
export function esperar(scene, ms) {
  return new Promise((ok) => scene.time.delayedCall(ms, ok));
}
