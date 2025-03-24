import request from "./request";
import type { Template, User, SharedTemplate } from "@/types";

// 共享模板
export function shareTemplate(
  templateId: number,
  data: {
    user_id: number;
    can_edit: boolean;
  },
) {
  return request({
    url: `/templates/${templateId}/share/`,
    method: "post",
    data,
  });
}

// 撤销共享
export function revokeShare(templateId: number, userId: number) {
  return request({
    url: `/templates/${templateId}/revoke_share/`,
    method: "delete",
    data: {
      user_id: userId,
    },
  });
}

// 获取待处理的共享模板列表
export function getPendingShares() {
  return request<SharedTemplate[]>({
    url: "/shared-templates/pending/",
    method: "get",
  });
}

// 接受共享
export function acceptShare(shareId: number) {
  return request<SharedTemplate>({
    url: `/shared-templates/${shareId}/accept/`,
    method: "post",
  });
}

// 拒绝共享
export function rejectShare(shareId: number) {
  return request<SharedTemplate>({
    url: `/shared-templates/${shareId}/reject/`,
    method: "post",
  });
}

// 获取共享给我的模板列表
export function getSharedWithMe() {
  return request<{
    count: number;
    results: Template[];
  }>({
    url: "/templates/shared_with_me/",
    method: "get",
  });
}

// 获取用户列表
export function getUserList(search?: string) {
  return request<{
    count: number;
    next: string | null;
    previous: string | null;
    results: User[];
  }>({
    url: "/auth/search/",
    method: "get",
    params: { search },
  });
}

// 获取模板的共享列表
export function getTemplateShares(templateId: number) {
  return request<SharedTemplate[]>({
    url: `/templates/templates/${templateId}/get_shares/`,
    method: "get",
  });
}

// 添加共享
export function addShare(data: {
  template: number;
  shared_with_id: number;
  can_edit: boolean;
}) {
  return request<SharedTemplate>({
    url: `/templates/templates/${data.template}/share/`,
    method: "post",
    data: {
      user_id: data.shared_with_id,
      can_edit: data.can_edit,
    },
  }).catch((error) => {
    if (error.response?.status === 404) {
      throw new Error("模板信息不存在");
    }
    throw error;
  });
}

// 删除共享
export function deleteShare(templateId: number, userId: number) {
  return request({
    url: `/templates/templates/${templateId}/revoke_share/`,
    method: "delete",
    data: {
      user_id: userId,
    },
  });
}
