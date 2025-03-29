import { defineStore } from "pinia";
import { ref } from "vue";
import type { User } from "@/types";
import { login as loginApi, getUserInfo } from "@/api/auth";
import { ElMessage } from "element-plus";

export const useUserStore = defineStore("user", () => {
  const user = ref<User | null>(null);
  const token = ref<string | null>(localStorage.getItem("token"));
  const permissions = ref<string[]>([]);

  // 获取用户信息
  const fetchUserInfo = async () => {
    try {
      const data = await getUserInfo();
      user.value = data;

      // 设置默认权限 - 根据用户角色设置权限
      // 这里假设所有用户至少有基本查看权限
      const defaultPermissions = [
        "template:view",
        "framework:view",
        "scene:view",
        "content:view",
      ];

      // 如果是管理员，添加更多权限
      if (data.is_staff) {
        defaultPermissions.push(
          "template:create",
          "template:edit",
          "template:delete",
          "framework:create",
          "framework:edit",
          "framework:delete",
          "scene:create",
          "scene:edit",
          "scene:delete",
          "content:create",
          "content:edit",
          "content:delete",
          "apikey:view",
          "apikey:create",
          "apikey:delete",
        );
      }

      // 如果API返回了权限，使用API返回的权限
      if (data.permissions) {
        permissions.value = data.permissions;
      } else {
        // 否则使用默认权限
        permissions.value = defaultPermissions;
      }

      return true;
    } catch (error: any) {
      console.error("获取用户信息失败:", error);
      if (error.response?.status === 401) {
        // Token 无效，清除登录状态
        logout();
        ElMessage.warning("登录已过期，请重新登录");
      } else {
        // 其他错误不影响用户体验，只记录日志
        console.error("获取用户信息失败，但不影响继续使用:", error);
      }
      return false;
    }
  };

  // 登录
  const login = async (username: string, password: string) => {
    try {
      const data = await loginApi({ username, password });
      // JWT 返回的字段是 access 或 access_token
      const accessToken = data.access || data.access_token;
      const refreshToken = data.refresh || data.refresh_token;

      if (accessToken) {
        token.value = accessToken;
        localStorage.setItem("token", accessToken);
        if (refreshToken) {
          localStorage.setItem("refresh_token", refreshToken);
        }
        // 如果响应中包含用户信息，直接使用
        if (data.user) {
          user.value = data.user;
        } else {
          // 否则获取用户信息
          await fetchUserInfo();
        }
        return true;
      }
      return false;
    } catch (error: any) {
      console.error("登录失败:", error);
      ElMessage.error(error.response?.data?.detail || "登录失败，请稍后重试");
      return false;
    }
  };

  // 登出
  const logout = (showMessage = false) => {
    user.value = null;
    token.value = null;
    permissions.value = [];
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");

    // 如果是手动登出，显示消息
    if (showMessage) {
      ElMessage.success("已成功退出登录");
    }

    // 登出后留在当前页面
    window.location.reload();
  };

  // 检查是否登录
  const isLoggedIn = () => {
    return !!token.value;
  };

  // 初始化：如果有 token 就获取用户信息
  if (token.value) {
    fetchUserInfo();
  }

  return {
    user,
    token,
    permissions,
    login,
    logout,
    isLoggedIn,
    fetchUserInfo,
  };
});
