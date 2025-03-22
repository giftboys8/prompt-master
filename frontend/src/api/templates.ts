import request from './request'
import type { Template } from '@/types'

export const createTemplate = (data: Partial<Template>) => {
  return request<Template>({
    url: '/templates/templates/',
    method: 'post',
    data
  })
}

export const getTemplate = (id: number) => {
  return request<Template>({
    url: `/templates/templates/${id}/`,
    method: 'get'
  })
}

export const updateTemplate = (id: number, data: Partial<Template>) => {
  return request<Template>({
    url: `/templates/templates/${id}/`,
    method: 'put',
    data
  })
}

export const deleteTemplate = (id: number) => {
  return request({
    url: `/templates/templates/${id}/`,
    method: 'delete'
  })
}

// 获取模板版本列表
export const getTemplateVersions = (templateId: number) => {
  return request<TemplateVersion[]>({
    url: `/templates/templates/${templateId}/versions/`,
    method: 'get'
  })
}

// 恢复到指定版本
export const restoreTemplateVersion = (templateId: number, versionId: number) => {
  return request({
    url: `/templates/templates/${templateId}/restore/`,
    method: 'post',
    data: { version_id: versionId }
  })
}

// 克隆模板
export const cloneTemplate = (id: number) => {
  return request<Template>({
    url: `/templates/templates/${id}/clone/`,
    method: 'post'
  })
}

// 导出模板
export const exportTemplates = () => {
  return request({
    url: '/templates/export/',
    method: 'get',
    responseType: 'blob'
  })
}

// 导入模板
export const importTemplates = (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return request({
    url: '/templates/import_templates/',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const getTemplateList = (params?: any) => {
  return request<{
    count: number
    results: Template[]
  }>({
    url: '/templates/templates/',
    method: 'get',
    params: {
      ...params,
      page: params?.page || 1,
      page_size: params?.page_size || 10
    }
  }).then(response => {
    console.log('API response:', response);
    return response;
  }).catch(error => {
    console.error('API error:', error);
    throw error;
  });
}

export const reorderTemplates = (orderData: { id: number; order: number }[]) => {
  return request({
    url: '/templates/reorder/',
    method: 'post',
    data: orderData
  })
}