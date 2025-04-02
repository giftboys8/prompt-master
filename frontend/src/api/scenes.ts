import request from "./request";
import type { Scene, PaginatedResponse } from "@/types";

/**
 * 获取场景列表
 */
export const getScenes = (params?: {
  page?: number;
  page_size?: number;
  search?: string;
}) => {
  return request<PaginatedResponse<Scene>>({
    url: "/scenes/",
    method: "get",
    params,
  });
};

/**
 * 获取场景详情
 */
export const getSceneDetail = (id: string | number) => {
  return request<Scene>({
    url: `/scenes/${id}/`,
    method: "get",
  });
};

/**
 * 创建场景
 */
export const createScene = (data: Partial<Scene>) => {
  return request<Scene>({
    url: "/scenes/",
    method: "post",
    data,
  });
};

/**
 * 更新场景
 */
export const updateScene = (id: string | number, data: Partial<Scene>) => {
  return request<Scene>({
    url: `/scenes/${id}/`,
    method: "put",
    data,
  });
};

/**
 * 删除场景
 */
export const deleteScene = (id: string | number) => {
  return request<void>({
    url: `/scenes/${id}/`,
    method: "delete",
  });
};
