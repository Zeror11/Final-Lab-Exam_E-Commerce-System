import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import 'bootstrap/dist/css/bootstrap.min.css'

const app = createApp(App)

// Dynamically add the animate.css CDN
const link = document.createElement('link')
link.rel = 'stylesheet'
link.href = 'https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css'
document.head.appendChild(link)

app.use(createPinia())
app.use(router)
app.mount('#app')
