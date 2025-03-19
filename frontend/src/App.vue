<template>
  <el-menu
    :router="true"
    mode="horizontal"
    :default-active="$route.path"
    class="nav-menu"
  >
    <el-menu-item index="/">首页</el-menu-item>
    <el-menu-item index="/about">关于我们</el-menu-item>
    
    <div class="flex-spacer"></div>
    
    <el-menu-item v-if="!isAuthenticated" index="/login">
      登录/注册
    </el-menu-item>
    <el-sub-menu v-else index="user">
      <template #title>
        <el-avatar :size="32" :src="userAvatar">
          {{ userInitials }}
        </el-avatar>
        <span class="username">{{ username }}</span>
      </template>
      <el-menu-item @click="handleLogout">退出登录</el-menu-item>
    </el-sub-menu>
  </el-menu>
  <router-view/>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

export default {
  setup() {
    const store = useStore()
    const router = useRouter()

    const isAuthenticated = computed(() => store.getters['auth/isAuthenticated'])
    const user = computed(() => store.getters['auth/user'])
    const username = computed(() => user.value?.nickname || user.value?.username || '')
    const userAvatar = computed(() => user.value?.avatar || '')
    const userInitials = computed(() => {
      const name = username.value
      return name ? name.charAt(0).toUpperCase() : '?'
    })

    const handleLogout = async () => {
      try {
        await store.dispatch('auth/logout')
        ElMessage.success('退出登录成功')
        router.push('/login')
      } catch (error) {
        ElMessage.error('退出登录失败')
      }
    }

    return {
      isAuthenticated,
      username,
      userAvatar,
      userInitials,
      handleLogout
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.nav-menu {
  padding: 0 20px;
}

.flex-spacer {
  flex-grow: 1;
}

.username {
  margin-left: 8px;
}

.el-menu--horizontal > .el-sub-menu .el-sub-menu__title {
  display: flex;
  align-items: center;
}
</style>