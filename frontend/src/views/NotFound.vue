<template>
  <div class="not-found">
    <el-empty description="页面不存在">
      <template #image>
        <el-image src="https://element-plus.org/images/404.png" />
      </template>
      <el-button type="primary" @click="router.push('/')">返回首页</el-button>
    </el-empty>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";

const router = useRouter();
</script>

<style scoped>
.not-found {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
