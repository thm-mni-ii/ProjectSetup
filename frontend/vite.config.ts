import { fileURLToPath, URL } from 'url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import eslintPlugin from 'vite-plugin-eslint'
import vuetify from 'vite-plugin-vuetify'

// https://vitejs.dev/config/
export default defineConfig({
  css: {
    postcss: {
      plugins: [
        {
          postcssPlugin: 'internal:charset-removal',
          AtRule: {
            charset: (atRule: import('postcss').AtRule) => {
              if (atRule.name === 'charset') {
                atRule.remove()
              }
            }
          }
        }
      ]
    },
    preprocessorOptions: {
      scss: {
        additionalData: `@use "@/assets/settings.scss" as *;`
      }
    }
  },
  plugins: [
    vue(),
    eslintPlugin({
      include: ['src/**/*.{js,ts,vue}'],
      exclude: [/node_modules/, /\.vite/, /virtual:/]
    }),
    vuetify({
      autoImport: true
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: true,
    port: 8085,
    proxy: {
      '/api': {
        target: 'http://localhost:80',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
