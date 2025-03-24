import request from "./request";

export interface FrameworkModule {
  id?: number;
  name: string;
  description: string;
  order?: number;
  created_at?: string;
  updated_at?: string;
}

export interface Framework {
  id?: number;
  name: string;
  description: string;
  modules: FrameworkModule[];
  created_at?: string;
  updated_at?: string;
}

// 获取所有框架
export const getFrameworks = () => {
  return request({
    method: "get",
    url: "/admin/frameworks/",
    params: {
      with_modules: true // 添加参数以获取模块信息
    }
  }).then(response => {
    // 确保返回的数据结构一致，无论是否为分页格式
    console.log("API getFrameworks raw response:", response);
    return response;
  });
};

// 获取单个框架详情
export const getFramework = (id: number) => {
  return request({
    method: "get",
    url: `/admin/frameworks/${id}/`,
  });
};

// 创建框架
export const createFramework = (data: Framework) => {
  return request({
    method: "post",
    url: "/admin/frameworks/",
    data,
  });
};

// 更新框架
export const updateFramework = (id: number, data: Framework) => {
  return request({
    method: "put",
    url: `/admin/frameworks/${id}/`,
    data,
  });
};

// 删除框架
export const deleteFramework = (id: number) => {
  return request({
    method: "delete",
    url: `/admin/frameworks/${id}/`,
  });
};

// 获取框架的所有模块
export const getFrameworkModules = (frameworkId: number) => {
  return request({
    method: "get",
    url: `/admin/frameworks/${frameworkId}/modules/`,
  });
};

// 添加模块到框架
export const addModuleToFramework = (
  frameworkId: number,
  data: FrameworkModule,
) => {
  return request({
    method: "post",
    url: `/admin/frameworks/${frameworkId}/add_module/`,
    data,
  });
};

// 获取所有模块
export const getModules = (frameworkId?: number) => {
  return request({
    method: "get",
    url: "/admin/modules/",
    params: frameworkId ? { framework_id: frameworkId } : {},
  });
};

// 获取单个模块
export const getModule = (id: number) => {
  return request({
    method: "get",
    url: `/admin/modules/${id}/`,
  });
};

// 更新模块
export const updateModule = (id: number, data: FrameworkModule) => {
  return request({
    method: "put",
    url: `/admin/modules/${id}/`,
    data,
  });
};

// 删除模块
export const deleteModule = (id: number) => {
  return request({
    method: "delete",
    url: `/admin/modules/${id}/`,
  });
};
