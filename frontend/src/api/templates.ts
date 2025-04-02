import request from "./request";
import type { Template, TemplateTest } from "@/types";

export const createTemplate = (data: Partial<Template>) => {
  return request<Template>({
    url: "/templates/templates/",
    method: "post",
    data,
  });
};

export const getTemplate = (id: number) => {
  return request<Template>({
    url: `/templates/templates/${id}`,
    method: "get",
  })
    .then((response) => {
      console.log("获取单个模板响应:", response);

      // 确保返回有效的响应数据
      if (!response) {
        throw new Error("API返回空响应");
      }

      // 如果响应是包含data属性的对象，则返回data
      if (response && typeof response === "object" && "data" in response) {
        return response.data;
      }

      // 否则直接返回响应
      return response;
    })
    .catch((error) => {
      console.error("获取模板失败:", error);
      throw error;
    });
};

export const updateTemplate = (id: number, data: Partial<Template>) => {
  return request<Template>({
    url: `/templates/templates/${id}`,
    method: "put",
    data,
  });
};

export const deleteTemplate = (id: number) => {
  return request({
    url: `/templates/templates/${id}/`,
    method: "delete",
  });
};

// 获取模板版本列表
export const getTemplateVersions = (templateId: number) => {
  return request<TemplateVersion[]>({
    url: `/templates/templates/${templateId}/versions/`,
    method: "get",
  });
};

// 恢复到指定版本
export const restoreTemplateVersion = (
  templateId: number,
  versionId: number,
) => {
  return request({
    url: `/templates/templates/${templateId}/restore/`,
    method: "post",
    data: { version_id: versionId },
  });
};

// 克隆模板
export const cloneTemplate = (id: number) => {
  return request<Template>({
    url: `/templates/templates/${id}/clone/`,
    method: "post",
  });
};

// 导出模板
export const exportTemplates = () => {
  return request({
    url: "/templates/templates/export/",
    method: "get",
    responseType: "blob",
  });
};

// 导入模板
export const importTemplates = (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  return request({
    url: "/templates/import_templates/",
    method: "post",
    data: formData,
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

export const getTemplateList = (params?: any) => {
  return request<{
    count: number;
    results: Template[];
  }>({
    url: "/templates/templates/",
    method: "get",
    params: {
      ...params,
      page: params?.page || 1,
      page_size: params?.page_size || 10,
    },
  }).catch((error) => {
    console.error("API error:", error);
    throw error;
  });
};

// 为兼容性添加 getTemplates 别名
export const getTemplates = getTemplateList;

export const reorderTemplates = (
  orderData: { id: number; order: number }[],
) => {
  return request({
    url: "/templates/templates/reorder/",
    method: "post",
    data: orderData,
  });
};

// 获取模板测试历史
export const getTemplateTests = (params?: any) => {
  console.log("调用getTemplateTests API，参数:", params);
  return request<{
    count: number;
    results: TemplateTest[];
  }>({
    url: "/templates/tests/",
    method: "get",
    params: {
      ...params,
      page: params?.page || 1,
      page_size: params?.page_size || 10,
    },
  }).then((response) => {
    console.log("获取测试历史响应:", response);
    return response;
  }).catch((error) => {
    console.error("API error:", error);
    throw error;
  });
};

// 运行模板测试
export const runTemplateTest = (data: any) => {
  return request<TemplateTest>({
    url: "/templates/tests/",
    method: "post",
    data,
  });
};
