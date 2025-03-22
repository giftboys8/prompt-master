import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

// 创建 axios 实例
const service: AxiosInstance = axios.create({
  baseURL: '/api/v1',  // 直接使用固定的API前缀
  timeout: 50000,
  headers: { 'Content-Type': 'application/json' }
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    // 处理 2xx 的响应
    if (response.status >= 200 && response.status < 300) {
      console.log('API Response:', response.data);
      return response.data;
    }
    return Promise.reject(new Error(response.data?.detail || '请求失败'))
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 400:
          ElMessage.error(data.detail || data.error || '请求参数错误')
          break
        case 401:
          ElMessage.error('登录已过期，请重新登录')
          localStorage.removeItem('token')
          router.push('/login')
          break
        case 403:
          ElMessage.error('没有权限访问')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error(data.error || data.detail || '服务器内部错误')
          break
        default:
          ElMessage.error(data.error || data.detail || error.message || '未知错误')
      }
    } else if (error.request) {
      ElMessage.error('网络错误，请检查网络连接')
    } else {
      ElMessage.error('请求配置错误')
    }
    
    return Promise.reject(error)
  }
)

const request = <T = any>(config: AxiosRequestConfig): Promise<T> => {
  // 处理blob响应类型
  if (config.responseType === 'blob') {
    return service(config).then(response => response as unknown as T)
  }
  return service(config)
}

export default request