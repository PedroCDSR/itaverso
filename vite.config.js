import { defineConfig } from 'vite';

export default defineConfig({
  // Caminhos relativos: o build funciona na raiz do Netlify e em qualquer subpasta.
  base: './',
  build: {
    // O Phaser é grande (~1,2 MB): avisar só acima disso.
    chunkSizeWarningLimit: 1500,
    assetsInlineLimit: 0,
    // Saída com hash vai para /js (cache longo no netlify.toml); public/assets fica sem cache longo.
    assetsDir: 'js',
  },
});
