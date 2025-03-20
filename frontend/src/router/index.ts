import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/Login.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/Home.vue')
        },
        {
          path: 'templates',
          name: 'template-list',
          component: () => import('@/views/templates/TemplateList.vue')
        },
        {
          path: 'templates/create',
          name: 'template-create',
          component: () => import('@/views/templates/TemplateCreate.vue')
        },
        {
          path: 'templates/:id/edit',
          name: 'template-edit',
          component: () => import('@/views/templates/TemplateEdit.vue')
        },
        {
          path: 'templates/test',
          name: 'template-test',
          component: () => import('@/views/templates/TemplateTest.vue')
        },
        {
          path: 'scenes',
          name: 'scene-list',
          component: () => import('@/views/scenes/SceneList.vue')
        },
        {
          path: 'contents',
          name: 'content-list',
          component: () => import('@/views/contents/ContentList.vue')
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFound.vue')
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const requiresAuth = to.meta.requiresAuth === true

  if (requiresAuth && !userStore.token) {
    // 对于需要认证的页面，如果没有登录，重定向到首页
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router