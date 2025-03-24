<template>
  <div class="test-result">
    <h3>测试结果</h3>
    <div v-html="formattedResult" class="test-result-content"></div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import MarkdownIt from "markdown-it";

const md = new MarkdownIt({
  linkify: true,
  typographer: true,
  breaks: true,
});

const props = defineProps<{
  result: string;
}>();

// 格式化测试结果
const formattedResult = computed(() => {
  return md.render(props.result);
});
</script>

<style lang="scss" scoped>
.test-result {
  padding: 24px;
  border-radius: 12px;
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
  width: 100%;
  max-width: 100%;
  overflow-x: auto;

  h3 {
    color: var(--primary-color);
    font-size: 18px;
    margin-bottom: 16px;
    font-family: "Orbitron", sans-serif;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 8px;
  }

  .test-result-content {
    font-size: 14px;
    line-height: 1.6;
    color: var(--text-primary);

    :deep(pre) {
      background: var(--bg-dark);
      padding: 16px;
      border-radius: 8px;
      overflow-x: auto;
      margin: 16px 0;
    }

    :deep(code) {
      font-family: "Fira Code", monospace;
      background: var(--bg-dark);
      padding: 2px 4px;
      border-radius: 4px;
      font-size: 0.9em;
    }
  }
}
</style>
