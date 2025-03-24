<template>
  <el-dialog
    v-model="dialogVisible"
    title="测试记录详情"
    width="800px"
    destroy-on-close
    class="history-detail-dialog"
  >
    <template v-if="record">
      <div class="detail-section">
        <h4>测试时间</h4>
        <div class="detail-content">
          {{ new Date(record.created_at).toLocaleString() }}
        </div>
      </div>

      <div class="detail-section">
        <h4>使用模型</h4>
        <div class="detail-content">
          {{ getModelName(record) }}
        </div>
      </div>

      <div class="detail-section">
        <h4>输入变量</h4>
        <div class="detail-content code-block">
          <pre>{{ JSON.stringify(record.input_data, null, 2) }}</pre>
        </div>
      </div>

      <div class="detail-section">
        <h4>生成的提示词</h4>
        <div class="detail-content code-block">
          <pre>{{
            parseTestResult(record.output_content)?.prompt || "未找到提示词"
          }}</pre>
        </div>
      </div>

      <div class="detail-section">
        <h4>输出内容</h4>
        <div
          class="detail-content markdown-content"
          v-html="
            formatMarkdown(
              parseTestResult(record.output_content)?.answer ||
                record.output_content,
            )
          "
        />
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { TemplateTest } from "@/types";
import MarkdownIt from "markdown-it";

const md = new MarkdownIt({
  linkify: true,
  typographer: true,
  breaks: true,
});

const props = defineProps<{
  visible: boolean;
  record: TemplateTest | null;
}>();

const emit = defineEmits<{
  (e: "update:visible", value: boolean): void;
}>();

const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit("update:visible", value),
});

// 获取模型名称
const getModelName = (record: TemplateTest) => {
  if (record.model) {
    return record.model;
  }
  return record.dify_response?.model || "Dify API";
};

// 解析测试结果
const parseTestResult = (content: string) => {
  try {
    return JSON.parse(content);
  } catch (e) {
    return null;
  }
};

// 格式化Markdown
const formatMarkdown = (content: string) => {
  return content ? md.render(content) : "";
};
</script>

<style lang="scss" scoped>
.history-detail-dialog {
  :deep(.el-dialog__body) {
    max-height: 70vh;
    overflow-y: auto;
  }

  .detail-section {
    margin-bottom: 24px;

    h4 {
      color: var(--primary-color);
      font-size: 16px;
      margin-bottom: 12px;
    }

    .detail-content {
      background: var(--bg-card);
      border-radius: 8px;
      padding: 16px;
      border: 1px solid var(--border-color);

      &.code-block {
        font-family: "Fira Code", monospace;
        font-size: 14px;
        line-height: 1.5;
        overflow-x: auto;
      }

      &.markdown-content {
        color: var(--text-primary);
        font-size: 14px;
        line-height: 1.6;
        white-space: pre-wrap;
        overflow-wrap: break-word;
        word-wrap: break-word;
        word-break: break-word;

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

        :deep(th), :deep(td) {
          border: 1px solid var(--border-color);
          padding: 8px;
          text-align: left;
        }
      }
    }
  }
}
</style>
