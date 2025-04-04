import { RouteRecordRaw } from "vue-router";

// 错误页面路由
export const errorRoutes: RouteRecordRaw[] = [
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("@/views/errors/404.vue"),
    meta: {
      title: "页面未找到",
      requiresAuth: false,
    },
  },
  {
    path: "/error",
    name: "error",
    component: () => import("@/views/errors/Error.vue"),
    meta: {
      title: "错误",
      requiresAuth: false,
    },
  },
  {
    path: "/403",
    name: "403",
    component: () => import("@/views/Forbidden.vue"),
    meta: {
      title: "权限不足",
      requiresAuth: false,
    },
  },
];

// 认证相关路由
export const authRoutes: RouteRecordRaw[] = [
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/Login.vue"),
    meta: {
      title: "登录",
      requiresAuth: false,
      layout: "auth",
    },
  },
  {
    path: "/register",
    name: "Register",
    component: () => import("@/views/Register.vue"),
    meta: {
      title: "注册",
      requiresAuth: false,
      layout: "auth",
    },
  },
];

// 模板相关路由
export const templateRoutes: RouteRecordRaw[] = [
  {
    path: "templates",
    name: "template-list",
    component: () => import("@/views/templates/TemplateList.vue"),
    meta: {
      title: "提示词模板",
      requiresAuth: true,
      permissions: ["template:view"],
    },
  },
  {
    path: "templates/create",
    name: "template-create",
    component: () => import("@/views/templates/TemplateCreate.vue"),
    meta: {
      title: "创建模板",
      requiresAuth: true,
      permissions: ["template:create"],
    },
  },
  {
    path: "templates/:id/edit",
    name: "template-edit",
    component: () => import("@/views/templates/TemplateEdit.vue"),
    meta: {
      title: "编辑模板",
      requiresAuth: true,
      permissions: ["template:edit"],
    },
  },
  {
    path: "templates/shared",
    name: "template-shared",
    component: () => import("@/views/templates/SharedWithMe.vue"),
    meta: {
      title: "共享模板",
      requiresAuth: true,
    },
  },
  {
    path: "templates/:id?/test",
    name: "template-test",
    component: () => import("@/views/templates/TemplateTest.vue"),
    meta: {
      title: "模板测试",
      requiresAuth: true,
    },
    props: true,
  },
];

// 框架相关路由
export const frameworkRoutes: RouteRecordRaw[] = [
  {
    path: "frameworks",
    name: "framework-list",
    component: () => import("@/views/frameworks/FrameworkList.vue"),
    meta: {
      title: "模板框架",
      requiresAuth: true,
      permissions: ["framework:view"],
    },
  },
  {
    path: "frameworks/create",
    name: "framework-create",
    component: () => import("@/views/frameworks/FrameworkCreate.vue"),
    meta: {
      title: "创建框架",
      requiresAuth: true,
      permissions: ["framework:create"],
    },
  },
  {
    path: "frameworks/edit/:id",
    name: "framework-edit",
    component: () => import("@/views/frameworks/FrameworkEdit.vue"),
    meta: {
      title: "编辑框架",
      requiresAuth: true,
      permissions: ["framework:edit"],
    },
  },
];

// 场景和内容相关路由
export const contentRoutes: RouteRecordRaw[] = [
  {
    path: "scenes",
    name: "scene-list",
    component: () => import("@/views/scenes/SceneList.vue"),
    meta: {
      title: "场景列表",
      requiresAuth: true,
      permissions: ["scene:view"],
    },
  },
  {
    path: "scenes/create",
    name: "scene-create",
    component: () => import("@/views/scenes/SceneCreate.vue"),
    meta: {
      title: "创建场景",
      requiresAuth: true,
      permissions: ["scene:create"],
    },
  },
  {
    path: "scenes/:id/edit",
    name: "scene-edit",
    component: () => import("@/views/scenes/SceneEdit.vue"),
    meta: {
      title: "编辑场景",
      requiresAuth: true,
      permissions: ["scene:edit"],
    },
  },
  {
    path: "contents",
    name: "content-list",
    component: () => import("@/views/contents/ContentList.vue"),
    meta: {
      title: "场景市场",
      requiresAuth: false,
    },
  },
];

// 用户管理相关路由
export const userRoutes: RouteRecordRaw[] = [
  {
    path: "users",
    name: "user-list",
    component: () => import("@/views/users/UserList.vue"),
    meta: {
      title: "用户管理",
      requiresAuth: true,
      permissions: ["user:manage"],
    },
  },
];

// API密钥相关路由
export const apiKeyRoutes: RouteRecordRaw[] = [
  {
    path: "apikeys",
    name: "apikey-list",
    component: () => import("@/views/apikeys/ApiKeyList.vue"),
    meta: {
      title: "密钥管理",
      requiresAuth: true,
      permissions: ["apikey:view"],
    },
  },
];

// 主布局路由
export const mainRoutes: RouteRecordRaw = {
  path: "/",
  component: () => import("@/layouts/MainLayout.vue"),
  children: [
    {
      path: "",
      name: "home",
      component: () => import("@/views/Home.vue"),
      meta: {
        title: "首页",
        requiresAuth: false,
      },
    },
    ...templateRoutes,
    ...frameworkRoutes,
    ...contentRoutes,
    ...apiKeyRoutes,
    ...userRoutes,
  ],
};

// 额外的路由配置（已合并到errorRoutes中）
// 注意：原来的NotFound路由已被合并

// 导出所有路由
export const routes: RouteRecordRaw[] = [
  ...authRoutes,
  mainRoutes,
  ...errorRoutes,
];
