import { createRouter, createWebHistory, RouteLocationNormalized } from "vue-router";
import { useUserStore } from "@/stores/user";
import { routes } from "./routes";
import NProgress from "nprogress";
import "nprogress/nprogress.css";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
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
  minimum: 0.3
});

// 权限检查函数
function checkPermissions(to: RouteLocationNormalized): boolean {
  const userStore = useUserStore();
  const requiredPermissions = to.meta.permissions as string[] || [];
  
  if (requiredPermissions.length === 0) return true;
  
  return requiredPermissions.every(permission => 
    userStore.permissions?.includes(permission)
  );
}

// 全局前置守卫
router.beforeEach(async (to, from, next) => {
  // 开始加载进度条
  NProgress.start();

  const userStore = useUserStore();
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false);

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

    // 检查权限
    if (!checkPermissions(to)) {
      next({ name: "403" }); // 假设我们有一个403页面
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
  console.error('路由错误:', error);
  NProgress.done();
});

export default router;