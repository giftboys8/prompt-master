import request from './request';

// 运行模板测试
export const runTemplateTest = (data: {
  template: number;
  model: string;
  input_data: Record<string, any>;
}) => {
  return request({
    url: '/templates/tests/run_test/',
    method: 'post',
    data
  });
};

// 获取模板测试历史
export const getTemplateTests = (params: {
  template?: number;
  model?: string;
}) => {
  return request({
    url: '/templates/tests/',
    method: 'get',
    params
  });
};

// 获取单个测试详情
export const getTemplateTestDetail = (id: number) => {
  return request({
    url: `/templates/tests/${id}/`,
    method: 'get'
  });
};

// 删除测试记录
export const deleteTemplateTest = (id: number) => {
  return request({
    url: `/templates/tests/${id}/`,
    method: 'delete'
  });
};