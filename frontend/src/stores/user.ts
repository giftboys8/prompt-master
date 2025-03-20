import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '@/types'
import { login as loginApi } from '@/api/auth'
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  const login = async (username: string, password: string) => {
    try {
      const data = await loginApi({ username, password })
      token.value = data.access
      localStorage.setItem('token', data.access)
      ElMessage.success('登录成功')
      return true
    } catch (error: any) {
      if (error.response?.status === 401) {
        ElMessage.error('用户名或密码错误')
      } else {
        ElMessage.error('登录失败，请稍后重试')
      }
      return false
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    ElMessage.success('已退出登录')
  }

  return {
    user,
    token,
    login,
    logout
  }
})