<template>
  <el-container class="layout-container tech-theme">
    <el-header class="header">
      <div class="header-content">
        <div class="left-section">
          <div class="logo-animation">
            <span class="logo-icon">⚡</span>
            <h1>PromptMaster</h1>
          </div>
        </div>

        <div class="right-section">
          <el-menu
            router
            :default-active="route.path"
            mode="horizontal"
            class="main-menu"
            :ellipsis="false"
            @select="handleMenuClick"
          >
            <el-menu-item index="/">
              <template #title>
                <el-icon><HomeFilled /></el-icon>
                <span>首页</span>
              </template>
            </el-menu-item>
            <el-menu-item index="/templates">
              <template #title>
                <el-icon><Document /></el-icon>
                <span>提示词模板</span>
              </template>
            </el-menu-item>
            <el-menu-item index="/scenes">
              <template #title>
                <el-icon><Grid /></el-icon>
                <span>场景管理</span>
              </template>
            </el-menu-item>
            <el-menu-item index="/frameworks">
              <template #title>
                <el-icon><Folder /></el-icon>
                <span>模板框架</span>
              </template>
            </el-menu-item>
            <el-menu-item index="/contents">
              <template #title>
                <el-icon><Collection /></el-icon>
                <span>内容管理</span>
              </template>
            </el-menu-item>
            <el-menu-item index="/apikeys">
              <template #title>
                <el-icon><Key /></el-icon>
                <span>秘钥管理</span>
              </template>
            </el-menu-item>
          </el-menu>

          <div class="user-info">
            <template v-if="userStore.isLoggedIn()">
              <el-dropdown @command="handleCommand">
                <span class="user-dropdown">
                  <el-avatar :size="32" class="user-avatar">
                    {{ username.charAt(0).toUpperCase() }}
                  </el-avatar>
                  <div class="user-info-text">
                    <span class="username">{{ username }}</span>
                    <span class="user-role">{{ userRole }}</span>
                  </div>
                  <el-icon class="el-icon--right">
                    <arrow-down />
                  </el-icon>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item disabled>
                      <span class="dropdown-username">{{ username }}</span>
                    </el-dropdown-item>
                    <el-dropdown-item divided command="logout"
                      >退出登录</el-dropdown-item
                    >
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </template>
            <template v-else>
              <div class="auth-buttons">
                <el-button type="primary" @click="showLoginDialog = true">
                  登录
                </el-button>
                <el-button @click="router.push('/register')"> 注册 </el-button>
              </div>
            </template>
          </div>
        </div>
      </div>
    </el-header>

    <div class="breadcrumb-container">
      <el-breadcrumb class="breadcrumb">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <template v-for="(item, index) in breadcrumbItems" :key="index">
          <el-breadcrumb-item :to="item.path">{{
            item.title
          }}</el-breadcrumb-item>
        </template>
      </el-breadcrumb>
    </div>

    <el-main>
      <router-view v-slot="{ Component }">
        <component :is="Component" />
      </router-view>
    </el-main>

    <!-- 登录对话框 -->
    <el-dialog
      v-model="showLoginDialog"
      title="登录"
      width="400px"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-width="0"
        @keyup.enter="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            prefix-icon="User"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <div class="dialog-footer-left">
            <span class="register-link"
              >没有账号？
              <a href="#" @click.prevent="goToRegister">立即注册</a>
            </span>
          </div>
          <div class="dialog-footer-right">
            <el-button @click="showLoginDialog = false">取消</el-button>
            <el-button
              type="primary"
              :loading="loginLoading"
              @click="handleLogin"
            >
              登录
            </el-button>
          </div>
        </div>
      </template>
    </el-dialog>
  </el-container>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import {
  HomeFilled,
  Document,
  Grid,
  Collection,
  ArrowDown,
  User,
  Lock,
  Key,
  Folder,
} from "@element-plus/icons-vue";

export default defineComponent({
  name: "MainLayout",
  components: {
    HomeFilled,
    Document,
    Grid,
    Collection,
    ArrowDown,
    User,
    Lock,
    Key,
    Folder,
  },
});
</script>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
import { ElMessage } from "element-plus";
import type { FormInstance } from "element-plus";

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

// 用户信息
const username = computed(() => {
  const user = userStore.user;
  if (!user) return "未登录";
  return user.username;
});

const userRole = computed(() => {
  const user = userStore.user;
  if (!user) return "";
  return user.is_staff ? "管理员" : "普通用户";
});

// 面包屑导航
const breadcrumbItems = computed(() => {
  const matched = route.matched;
  return matched
    .filter((item) => item.meta?.title)
    .map((item) => ({
      path: item.path,
      title: item.meta?.title,
    }));
});

// 登录相关
const showLoginDialog = ref(false);
const loginLoading = ref(false);
const loginFormRef = ref<FormInstance>();
const loginForm = ref({
  username: "",
  password: "",
});

const loginRules = {
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
};

const handleLogin = () => {
  if (!loginFormRef.value) return;

  loginFormRef.value.validate((valid) => {
    if (valid) {
      loginLoading.value = true;
      userStore
        .login(loginForm.value.username, loginForm.value.password)
        .then((success) => {
          if (success) {
            showLoginDialog.value = false;
            ElMessage.success("登录成功");
          }
        })
        .finally(() => {
          loginLoading.value = false;
        });
    }
  });
};

// 菜单点击
const handleMenuClick = (index: string) => {
  // 可以添加菜单点击的处理逻辑
  console.log("Menu clicked:", index);
};

// 下拉菜单命令处理
const handleCommand = (command: string) => {
  if (command === "logout") {
    userStore.logout();
  }
};

// 跳转到注册页面
const goToRegister = () => {
  showLoginDialog.value = false;
  router.push("/register");
};
</script>

<style scoped>
.layout-container {
  height: 100vh;
  background: var(--bg-dark);
  background-image:
    radial-gradient(
      circle at 10% 20%,
      rgba(14, 165, 233, 0.05) 0%,
      transparent 20%
    ),
    radial-gradient(
      circle at 90% 80%,
      rgba(168, 85, 247, 0.05) 0%,
      transparent 20%
    );
}

.header {
  padding: 0;
  background: var(--glass-bg);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--glass-border);
  position: relative;
  z-index: 100;
}

.header-content {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}

.left-section {
  display: flex;
  align-items: center;
  gap: 32px;
}

.right-section {
  display: flex;
  align-items: center;
  gap: 24px;
}

.logo-animation {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 24px;
  animation: pulse 2s infinite;
}

.logo-animation h1 {
  margin: 0;
  font-size: 24px;
  font-family: "Orbitron", sans-serif;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 1px;
}

.breadcrumb-container {
  padding: 16px 24px;
  background: var(--glass-bg);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--glass-border);
}

.breadcrumb {
  max-width: 1200px;
  margin: 0 auto;
  color: var(--text-secondary);
  font-size: 14px;
}

.main-menu {
  display: flex;
  background: transparent !important;
  border: none;
}

.user-info {
  position: relative;
}

.user-dropdown {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: var(--text-primary);
  padding: 6px 12px;
  border-radius: 8px;
  background: var(--glass-bg);
  transition: all 0.3s ease;
  min-width: 180px;

  .user-avatar {
    background: var(--primary-gradient);
    color: var(--text-primary);
    font-weight: 600;
  }

  .user-info-text {
    display: flex;
    flex-direction: column;
    gap: 2px;
    flex: 1;

    .username {
      font-weight: 500;
    }

    .user-role {
      font-size: 12px;
      color: var(--text-secondary);
    }
  }
}

.user-dropdown:hover {
  background: var(--bg-hover);
}

.auth-buttons {
  display: flex;
  gap: 10px;
}

.dropdown-username {
  font-size: 12px;
  color: var(--text-secondary);
}

/* 登录对话框样式 */
.dialog-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  width: 100%;
}

.dialog-footer-left {
  flex: 1;
}

.dialog-footer-right {
  display: flex;
  gap: 12px;
}

.register-link {
  font-size: 14px;
  color: var(--text-secondary);
}

.register-link a {
  color: var(--primary-color);
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}

:deep(.el-dialog) {
  background: var(--glass-bg);
  backdrop-filter: blur(12px);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
}

:deep(.el-dialog__header) {
  margin: 0;
  padding: 20px 20px 10px;
  text-align: center;
}

:deep(.el-dialog__title) {
  font-size: 20px;
  color: var(--text-primary);
}

:deep(.el-dialog__body) {
  padding: 20px;
}

:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-input__wrapper) {
  background-color: var(--glass-bg);
  border: 1px solid var(--glass-border);
  box-shadow: none;
}

:deep(.el-input__wrapper:hover),
:deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 1px var(--primary-color);
}

:deep(.el-input__inner) {
  color: var(--text-primary);
}

:deep(.el-input__inner::placeholder) {
  color: var(--text-secondary);
}

:deep(.el-menu--horizontal .el-menu-item) {
  height: 64px;
  line-height: 64px;
  padding: 0 20px;
}

:deep(.el-breadcrumb__item) {
  .el-breadcrumb__inner {
    color: var(--text-secondary);
    &:hover {
      color: var(--primary-color);
    }
    &.is-link {
      color: var(--text-secondary);
      &:hover {
        color: var(--primary-color);
      }
    }
  }
  &:last-child .el-breadcrumb__inner {
    color: var(--text-primary);
  }
}

@keyframes pulse {
  0% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(0.95);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
