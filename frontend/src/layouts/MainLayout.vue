<template>
  <el-container class="layout-container">
    <el-aside width="200px" class="aside">
      <div class="logo">
        <h1>PromptMaster</h1>
      </div>
      <el-menu
        router
        :default-active="route.path"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/" @click="handleMenuClick">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/templates" @click="handleMenuClick">
          <el-icon><Document /></el-icon>
          <span>提示词模板</span>
        </el-menu-item>
        <el-menu-item index="/scenes" @click="handleMenuClick">
          <el-icon><Grid /></el-icon>
          <span>场景管理</span>
        </el-menu-item>
        <el-menu-item index="/contents" @click="handleMenuClick">
          <el-icon><Collection /></el-icon>
          <span>内容管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <div class="breadcrumb">
          <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <template v-for="(item, index) in breadcrumbItems" :key="index">
              <el-breadcrumb-item :to="item.path">{{ item.title }}</el-breadcrumb-item>
            </template>
          </el-breadcrumb>
        </div>
        <div class="user-info">
          <el-dropdown @command="handleCommand">
            <span class="user-dropdown">
              {{ username }}
              <el-icon class="el-icon--right">
                <arrow-down />
              </el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main>
        <router-view v-slot="{ Component }">
          <component :is="Component" />
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  HomeFilled,
  Document,
  Grid,
  Collection,
  ArrowDown
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 用户名
const username = computed(() => {
  return userStore.user?.username || '用户'
})

// 面包屑导航
const breadcrumbItems = computed(() => {
  const items = []
  const path = route.path
  const query = route.query

  if (path.startsWith('/templates')) {
    items.push({ path: '/templates', title: '提示词模板' })
    if (path.includes('/create')) {
      items.push({ path: '', title: '新增模板' })
    } else if (path.includes('/edit')) {
      items.push({ path: '', title: `编辑：${query.name || ''}` })
    }
  } else if (path.startsWith('/scenes')) {
    items.push({ path: '/scenes', title: '场景管理' })
  } else if (path.startsWith('/contents')) {
    items.push({ path: '/contents', title: '内容管理' })
  }

  return items
})

// 处理菜单点击
const handleMenuClick = (menu: any) => {
  router.push(menu.index)
}

// 处理下拉菜单命令
const handleCommand = (command: string) => {
  if (command === 'logout') {
    userStore.logout()
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.aside {
  background-color: #304156;
  color: #fff;
}

.logo {
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #2b2f3a;
}

.logo h1 {
  margin: 0;
  font-size: 20px;
  color: #fff;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-dropdown {
  cursor: pointer;
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #606266;
}

:deep(.el-menu) {
  border-right: none;
}

:deep(.el-menu-item) {
  color: #bfcbd9;
}

:deep(.el-menu-item.is-active) {
  color: #409eff !important;
  background-color: #263445 !important;
}

:deep(.el-menu-item:hover) {
  background-color: #263445 !important;
}

:deep(.el-menu-item .el-icon) {
  margin-right: 10px;
}
</style>