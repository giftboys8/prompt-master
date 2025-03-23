import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import TemplateTest from '@/views/templates/TemplateTest.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: { title: '登录' }
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/Register.vue'),
      meta: { title: '注册' }
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
          component: () => import('@/views/templates/TemplateList.vue'),
          meta: { title: '提示词模板' }
        },
        {
          path: 'templates/create',
          name: 'template-create',
          component: () => import('@/views/templates/TemplateCreate.vue'),
          meta: { title: '创建模板' }
        },
        {
          path: 'templates/:id/edit',
          name: 'template-edit',
          component: () => import('@/views/templates/TemplateEdit.vue'),
          meta: { title: '编辑模板' }
        },
        {
          path: 'templates/:id?/test',
          name: 'template-test',
          component: TemplateTest,
          meta: { title: '模板测试' },
          props: true
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
        },
        {
          path: 'apikeys',
          name: 'apikey-list',
          component: () => import('@/views/apikeys/ApiKeyList.vue'),
          meta: { title: '秘钥管理' }
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
  
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - PromptMaster` : 'PromptMaster'

  // 如果是登录或注册页面，且用户已登录，则重定向到首页
  if ((to.name === 'Login' || to.name === 'Register') && userStore.isLoggedIn()) {
    next({ name: 'home' })
    return
  }

  // 对于需要认证的页面，如果没有登录，重定向到登录页
  if (requiresAuth && !userStore.isLoggedIn()) {
    next({ 
      name: 'Login',
      query: { redirect: to.fullPath } 
    })
  } else {
    next()
  }
})

export default router