<template>
  <div class="test-result">
    <h3>测试结果</h3>
    <div class="test-result-content" v-html="formattedResult"></div>
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
  // 确保结果是字符串
  const result =
    typeof props.result === "string" ? props.result : String(props.result);
  return md.render(result);
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
  max-height: 60vh;
  overflow-y: auto;

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
    white-space: pre-wrap;
    overflow-wrap: break-word;
    word-wrap: break-word;
    word-break: break-all;

    :deep(pre) {
      background: var(--bg-dark);
      padding: 16px;
      border-radius: 8px;
      overflow-x: auto;
      margin: 16px 0;
      white-space: pre-wrap;
    }

    :deep(code) {
      font-family: "Fira Code", monospace;
      background: var(--bg-dark);
      padding: 2px 4px;
      border-radius: 4px;
      font-size: 0.9em;
    }

    :deep(p) {
      margin: 8px 0;
      white-space: pre-wrap;
    }

    :deep(img) {
      max-width: 100%;
      height: auto;
    }

    :deep(table) {
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0;
      overflow-x: auto;
      display: block;
    }

    :deep(th),
    :deep(td) {
      border: 1px solid var(--border-color);
      padding: 8px;
      text-align: left;
    }
  }
}
</style>
