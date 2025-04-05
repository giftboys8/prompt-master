import request from "./request";

interface UserListResponse {
  count: number;
  results: User[];
}

interface User {
  id: number;
  username: string;
  email: string;
  is_staff: boolean;
  is_active: boolean;
  date_joined: string;
}

export const getUsers = (params: { page: number; page_size: number }) => {
  return request<UserListResponse>({
    url: "/auth/users/",
    method: "get",
    params,
  });
};

export const updateUser = (id: number, data: Partial<User>) => {
  return request<User>({
    url: `/auth/users/${id}/`,
    method: "patch",
    data,
  });
};

export const deleteUser = (id: number) => {
  return request({
    url: `/auth/users/${id}/`,
    method: "delete",
  });
};