import request from './request'
import type { Template } from '@/types'

export const createTemplate = (data: Partial<Template>) => {
  return request<Template>({
    url: '/templates/',
    method: 'post',
    data
  })
}

export const getTemplate = (id: number) => {
  return request<Template>({
    url: `/templates/${id}/`,
    method: 'get'
  })
}

export const updateTemplate = (id: number, data: Partial<Template>) => {
  return request<Template>({
    url: `/templates/${id}/`,
    method: 'put',
    data
  })
}

export const deleteTemplate = (id: number) => {
  return request({
    url: `/templates/${id}/`,
    method: 'delete'
  })
}

// 获取模板版本列表
export const getTemplateVersions = (templateId: number) => {
  return request<TemplateVersion[]>({
    url: `/templates/${templateId}/versions/`,
    method: 'get'
  })
}

// 恢复到指定版本
export const restoreTemplateVersion = (templateId: number, versionId: number) => {
  return request({
    url: `/templates/${templateId}/restore/`,
    method: 'post',
    data: { version_id: versionId }
  })
}

// 克隆模板
export const cloneTemplate = (id: number) => {
  return request<Template>({
    url: `/templates/${id}/clone/`,
    method: 'post'
  })
}

export const getTemplateList = (params?: any) => {
  return request<{
    count: number
    results: Template[]
  }>({
    url: '/templates/',
    method: 'get',
    params
  })
}