import {
  createRouter,
  createWebHistory,
  RouteLocationNormalized,
} from "vue-router";
import { useUserStore } from "@/stores/user";
import { routes, errorRoutes } from "./routes";
import NProgress from "nprogress";
import "nprogress/nprogress.css";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [...routes, ...errorRoutes],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

// 配置 NProgress
NProgress.configure({
  showSpinner: false,
  minimum: 0.3,
});

// 权限检查函数
function checkPermissions(to: RouteLocationNormalized): boolean {
  const userStore = useUserStore();
  const requiredPermissions = (to.meta.permissions as string[]) || [];

  // 如果路由不需要权限，直接返回true
  if (requiredPermissions.length === 0) return true;

  // 如果用户是管理员，直接返回true
  if (userStore.user?.is_staff) return true;

  // 确保权限数组存在
  if (!userStore.permissions || userStore.permissions.length === 0) {
    console.warn('用户权限未加载，尝试重新获取用户信息');
    // 即使权限未加载，如果设置了默认权限，也应该继续检查
    if (userStore.hasDefaultPermissions()) {
      return requiredPermissions.every((permission) =>
        userStore.permissions.includes(permission),
      );
    }
    return false;
  }

  return requiredPermissions.every((permission) =>
    userStore.permissions.includes(permission),
  );
}

// 全局前置守卫
router.beforeEach(async (to, from, next) => {
  // 开始加载进度条
  NProgress.start();

  const userStore = useUserStore();
  const requiresAuth = to.matched.some(
    (record) => record.meta.requiresAuth === true,
  );

  // 设置页面标题
  document.title = to.meta.title
    ? `${to.meta.title} - PromptMaster`
    : "PromptMaster";

  // 处理已登录用户访问登录/注册页面
  if (
    (to.name === "Login" || to.name === "Register") &&
    userStore.isLoggedIn()
  ) {
    next({ name: "home" });
    NProgress.done();
    return;
  }

  // 处理需要认证的页面
  if (requiresAuth) {
    if (!userStore.isLoggedIn()) {
      // 保存目标路由，登录后跳转
      next({
        name: "Login",
        query: { redirect: to.fullPath },
      });
      NProgress.done();
      return;
    }

    // 如果用户信息未加载，先加载用户信息
    if (!userStore.user) {
      try {
        await userStore.fetchUserInfo();
      } catch (error) {
        console.error('获取用户信息失败:', error);
      }
    }

    // 检查权限
    if (!checkPermissions(to)) {
      // 如果权限未加载，尝试重新获取用户信息
      try {
        await userStore.fetchUserInfo();
        // 重新检查权限
        if (checkPermissions(to)) {
          next();
          return;
        }
      } catch (error) {
        console.error('重新获取用户信息失败:', error);
        // 即使获取用户信息失败，如果设置了默认权限并满足要求，也允许访问
        if (checkPermissions(to)) {
          next();
          return;
        }
      }
      next({ name: "403" });
      NProgress.done();
      return;
    }
  }

  next();
});

// 全局后置钩子
router.afterEach(() => {
  // 结束加载进度条
  NProgress.done();
});

// 路由错误处理
router.onError((error) => {
  console.error("路由错误:", error);
  NProgress.done();
});

export default router;
