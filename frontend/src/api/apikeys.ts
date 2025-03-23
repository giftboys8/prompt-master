import request from './request';

export interface ApiKeyData {
  id?: number;
  platform_name: string;
  scene_name: string;
  key: string;
  description?: string;
  is_active?: boolean;
  created_at?: string;
  updated_at?: string;
}

// 获取所有API秘钥
export function getApiKeys() {
  return request({
    url: '/apikeys/',
    method: 'get'
  });
}

// 获取单个API秘钥详情
export function getApiKey(id: number) {
  return request({
    url: `/apikeys/${id}/`,
    method: 'get'
  });
}

// 创建API秘钥
export function createApiKey(data: ApiKeyData) {
  return request({
    url: '/apikeys/',
    method: 'post',
    data
  });
}

// 更新API秘钥
export function updateApiKey(id: number, data: ApiKeyData) {
  return request({
    url: `/apikeys/${id}/`,
    method: 'put',
    data
  });
}

// 删除API秘钥
export function deleteApiKey(id: number) {
  return request({
    url: `/apikeys/${id}/`,
    method: 'delete'
  });
}

// 验证API秘钥
export function validateApiKey(id: number) {
  return request({
    url: `/apikeys/${id}/validate/`,
    method: 'post'
  });
}