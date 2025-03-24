<template>
  <div v-if="error" class="error-boundary">
    <el-result
      icon="error"
      :title="error.message || '组件加载失败'"
      :sub-title="error.stack"
    >
      <template #extra>
        <el-button type="primary" @click="handleRetry"> 重试 </el-button>
      </template>
    </el-result>
  </div>
  <slot v-else></slot>
</template>

<script setup lang="ts">
import { ref, onErrorCaptured } from "vue";

const props = defineProps<{
  onRetry?: () => void;
}>();

const error = ref<Error | null>(null);

onErrorCaptured((err: Error) => {
  error.value = err;
  return false; // 阻止错误继续传播
});

const handleRetry = () => {
  error.value = null;
  if (props.onRetry) {
    props.onRetry();
  }
};
</script>

<style lang="scss" scoped>
.error-boundary {
  padding: 2rem;
  text-align: center;
}
</style>
