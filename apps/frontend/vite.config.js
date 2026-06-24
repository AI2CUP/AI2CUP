import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const apiUrl = env.VITE_API_URL || '/api/v1'
  const isFullUrl = apiUrl.startsWith('http')

  return {
    plugins: [vue(), tailwindcss()],
    server: {
      port: 5173,
      allowedHosts: true,
      proxy: isFullUrl
        ? {}
        : {
            '/api': {
              target: 'http://localhost:8002',
              changeOrigin: true,
            },
          },
    },
  }
})
