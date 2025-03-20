import request from './request'

interface LoginData {
  username: string
  password: string
}

interface RegisterData {
  username: string
  email: string
  password: string
  password2: string
}

interface LoginResponse {
  access: string
  refresh: string
  user?: {
    id: number
    username: string
    email: string
    is_staff: boolean
    date_joined: string
  }
}

interface UserInfo {
  id: number
  username: string
  email: string
  is_staff: boolean
  date_joined: string
}

export const register = (data: RegisterData) => {
  return request<UserInfo>({
    url: '/auth/register/',
    method: 'post',
    data
  })
}

export const login = (data: LoginData) => {
  return request<LoginResponse>({
    url: '/auth/token/',
    method: 'post',
    data
  })
}

export const getUserInfo = () => {
  return request<UserInfo>({
    url: '/auth/user/',
    method: 'get'
  })
}