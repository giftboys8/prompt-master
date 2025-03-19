import axios from 'axios'

// 创建自定义的axios实例
const instance = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// 配置CSRF Token
instance.defaults.xsrfCookieName = 'csrftoken'
instance.defaults.xsrfHeaderName = 'X-CSRFToken'

// 配置请求拦截器
instance.interceptors.request.use(
  config => {
    // 如果有需要，在这里添加认证token等
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 配置响应拦截器
instance.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response?.status === 401) {
      // 处理未认证的情况
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default instance