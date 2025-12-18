import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  base: "/",
  plugins: [vue()],
  preview: {
    port: 8080,
    strictPort: true,
  },
  server: {
    port: 8080,
    strictPort: true,
    host: true,
    origin: "http://0.0.0.0",
    watch: {
      usePolling: true,
    },
    cors: {
			origin: ['https://ai-recipes.fi', 'http://localhost'],
			methods: ['GET', 'POST'],
			allowedHeaders: ['Content-Type']
		},
		allowedHosts: ['ai-recipes.fi'] //added this
  },
});
