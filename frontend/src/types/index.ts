// 用户类型
export interface User {
  id: number
  username: string
  email: string
  is_staff: boolean
  date_joined: string
}

// 提示词模版类型
export interface Template {
  id: number
  name: string
  framework_type: 'RTGO' | 'SPAR' | 'CUSTOM'
  description: string
  content: {
    role?: string
    task?: string
    goal?: string
    output?: string
    situation?: string
    purpose?: string
    action?: string
    result?: string
    custom?: string
  }
  variables: Array<{
    name: string
    default_value: string
    description: string
  }>
  order: number
  created_at: string
  updated_at: string
  created_by: number
}

export interface TemplateVersion {
  id: number
  template: number
  version_number: number
  name: string
  framework_type: 'RTGO' | 'SPAR' | 'CUSTOM'
  description: string
  content: {
    role?: string
    task?: string
    goal?: string
    output?: string
    situation?: string
    purpose?: string
    action?: string
    result?: string
    custom?: string
  }
  variables: Array<{
    name: string
    default_value: string
    description: string
  }>
  is_current: boolean
  created_at: string
  created_by: number
  created_by_username: string
}

// 业务场景类型
export interface Scene {
  id: number
  name: string
  description: string
  templates: number[]
  created_at: string
  updated_at: string
  created_by: number
}

// 生成内容类型
export interface Content {
  id: number
  title: string
  content: string
  template_id: number
  scene_id: number
  created_at: string
  updated_at: string
  created_by: number
}