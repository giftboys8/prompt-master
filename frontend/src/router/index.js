import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import store from '../store'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { 
      requiresAuth: true,
      title: '首页'
    }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: {
      title: '登录'
    }
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue'),
    meta: { 
      requiresAuth: true,
      title: '关于我们'
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 导航守卫
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters['auth/isAuthenticated']) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

// 全局导航守卫 - 设置页面标题
router.afterEach((to) => {
  // 设置标题
  document.title = to.meta.title ? `${to.meta.title} - PromptMaster` : 'PromptMaster'
})

export default router