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
        proxy:{
            "/api":{
                target: "http://127.0.0.1:9998",
                changeOrigin: true,
            }
        }
    },
    build: {
        target: 'esnext',
        minify: 'terser',
        sourcemap: true,
        outDir: "../iterm2_shortcut_html2/html",
        emptyOutDir: true,
        rollupOptions: {
            output: {
                //拆分太大的包配置
                manualChunks(id) {
                    if (id.includes('node_modules')) {
                        return id.split('node_modules/')[1].split('/')[0].toString(); // 以模块名命名
                    }
                }
            }
        }
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
