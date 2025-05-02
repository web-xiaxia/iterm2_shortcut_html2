import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import {fileURLToPath} from 'url'
import {dirname, resolve} from 'path'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

// https://vite.dev/config/
export default defineConfig({
    plugins: [vue()],
    server: {
        port: 4173, // 手动指定一个新的端口
        open: true,
    },
    build: {
        target: 'esnext',
        minify: 'terser',
        sourcemap: true
    },
    optimizeDeps: {
        esbuildOptions: {
            target: 'esnext'
        }
    },
    resolve: {
        alias: {
            '@': resolve(__dirname, './src')
        }
    }
})
