import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  root: 'client',
  build: {
    outDir: '../dist/client',
    emptyOutDir: true,
    target: 'es2022',
    chunkSizeWarningLimit: 4000,
  },
  test: {
    root: fileURLToPath(new URL('.', import.meta.url)),
    include: ['test/**/*.test.ts'],
  },
  server: {
    fs: { allow: ['..'] },
    proxy: {
      '/ws': { target: 'ws://127.0.0.1:8787', ws: true },
      '/report': 'http://127.0.0.1:8787',
    },
  },
});
