import request from './request'

interface LoginParams {
  username: string
  password: string
}

interface LoginResult {
  access: string
  refresh: string
}

export const login = (data: LoginParams) => {
  return request<LoginResult>({
    url: '/auth/token/',
    method: 'post',
    data
  })
}

export const refreshToken = (refresh: string) => {
  return request<{ access: string }>({
    url: '/auth/token/refresh/',
    method: 'post',
    data: { refresh }
  })
}