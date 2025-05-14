import {createApp} from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './element-theme.css'
import './style.css'
import App from './App.vue'

const app = createApp(App)
app.use(ElementPlus, { size: 'default', zIndex: 3000 })
app.mount('#app')
