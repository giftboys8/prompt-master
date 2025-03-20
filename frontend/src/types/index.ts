export interface User {
  id: number
  username: string
  email: string
  avatar?: string
}

export interface Scene {
  id: number
  name: string
  description: string
  created_at: string
  updated_at: string
}

export interface Template {
  id: number
  name: string
  content: string
  variables: string[]
  created_at: string
  updated_at: string
}

export interface Content {
  id: number
  title: string
  content: string
  template_id: number
  created_at: string
  updated_at: string
}