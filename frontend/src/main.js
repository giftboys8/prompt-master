import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import App from './App.vue'
import router from './router'
import store from './store'
import './plugins/axios'

const app = createApp(App)

app.use(ElementPlus, {
  locale: zhCn,
})
app.use(store)
app.use(router)

// 在应用启动时获取用户信息
store.dispatch('auth/fetchUser').catch(() => {
  // 如果获取用户信息失败，不做特殊处理，让路由守卫处理未认证状态
})

app.mount('#app')