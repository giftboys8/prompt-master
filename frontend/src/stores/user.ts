import { defineStore } from "pinia";
import { ref } from "vue";
import type { User } from "@/types";
import { login as loginApi, getUserInfo, register as registerApi } from "@/api/auth";
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
      // 普通用户的基础权限：查看所有内容，创建新内容
      const defaultPermissions = [
        // 模板权限
        "template:view",
        "template:create",
        // 框架权限
        "framework:view",
        "framework:create",
        // 场景权限
        "scene:view",
        "scene:create",
        // 内容查看权限
        "content:view",
        "content:create",
        // 针对自己创建的内容的权限
        "template:edit:own",
        "template:delete:own",
        "template:clone:own",
        "template:test:own",
        "framework:edit:own",
        "framework:delete:own",
        "scene:edit:own",
        "scene:delete:own"
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
          "user:manage", // 添加用户管理权限
        );
      }

      // 如果API返回了权限，使用API返回的权限
      if (data.permissions && data.permissions.length > 0) {
        permissions.value = data.permissions;
      } else {
        // 否则使用默认权限
        permissions.value = defaultPermissions;
      }

      // 打印权限信息，方便调试
      console.log('用户信息已加载:', {
        isStaff: data.is_staff,
        permissions: permissions.value
      });

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
        // 设置基本权限，确保用户可以访问基本功能
        permissions.value = [
          "template:view",
          "framework:view",
          "scene:view",
          "content:view",
        ];
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

  // 初始化：如果有 token 就立即获取用户信息
  if (token.value) {
    // 使用setTimeout确保在Vue应用初始化完成后再获取用户信息
    setTimeout(() => {
      fetchUserInfo().catch(error => {
        console.error('初始化获取用户信息失败:', error);
      });
    }, 0);
  }

  // 注册
  const register = async (userData: { username: string; email: string; password: string; password2: string }) => {
    try {
      await registerApi(userData);
      ElMessage.success("用户创建成功");
      return true;
    } catch (error: any) {
      console.error("注册失败:", error);
      ElMessage.error(error.response?.data?.detail || "用户创建失败，请稍后重试");
      return false;
    }
  };

  // 检查是否已设置默认权限
  const hasDefaultPermissions = () => {
    return permissions.value && permissions.value.length > 0;
  };

  return {
    user,
    token,
    permissions,
    login,
    logout,
    isLoggedIn,
    fetchUserInfo,
    register,
    hasDefaultPermissions,
  };
});
