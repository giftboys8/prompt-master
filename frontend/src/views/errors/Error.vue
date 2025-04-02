<template>
  <div class="error-page">
    <el-result
      icon="error"
      title="错误"
      :sub-title="errorMessage || '应用程序发生了错误'"
    >
      <template #extra>
        <el-button type="primary" @click="handleRetry">重试</el-button>
        <el-button @click="router.push('/')">返回首页</el-button>
      </template>
    </el-result>
  </div>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from "vue-router";
import { ref, onMounted } from "vue";

const router = useRouter();
const route = useRoute();
const errorMessage = ref<string>("");

onMounted(() => {
  // 从路由查询参数中获取错误信息
  if (route.query.message && typeof route.query.message === "string") {
    errorMessage.value = route.query.message;
  }
});

const handleRetry = () => {
  // 如果有from路由，则返回上一页
  if (route.query.from && typeof route.query.from === "string") {
    router.push(route.query.from);
  } else {
    router.push("/");
  }
};
</script>

<style lang="scss" scoped>
.error-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100%;
  padding: 2rem;
}
</style>