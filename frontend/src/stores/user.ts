import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '@/types'
import { login as loginApi } from '@/api/auth'
import { ElMessage } from 'element-plus'
import router from '@/router'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  const login = async (username: string, password: string) => {
    try {
      const data = await loginApi({ username, password })
      if (data.access) {
        token.value = data.access
        localStorage.setItem('token', data.access)
        if (data.refresh) {
          localStorage.setItem('refresh_token', data.refresh)
        }
        ElMessage.success('登录成功')
        router.push('/')
        return true
      }
      return false
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || '登录失败，请稍后重试')
      return false
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    router.push('/login')
  }

  const isLoggedIn = () => {
    return !!token.value
  }

  return {
    user,
    token,
    login,
    logout,
    isLoggedIn
  }
})