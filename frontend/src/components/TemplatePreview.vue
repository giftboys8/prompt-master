<template>
  <!-- 对话框模式 -->
  <el-dialog
    v-if="mode === 'dialog'"
    :model-value="modelValue"
    title="模板预览"
    width="50%"
    class="template-preview-dialog"
    :close-on-click-modal="false"
    :close-on-press-escape="true"
    @update:model-value="$emit('update:modelValue', $event)"
    @close="$emit('update:modelValue', false)"
  >
    <div v-if="template" class="preview-content scrollable">
      <div class="preview-header">
        <el-radio-group v-model="currentPreviewMode" size="large">
          <el-radio-button
            v-for="mode in previewModes"
            :key="mode.value"
            :label="mode.value"
          >
            <el-icon>
              <component :is="mode.icon" />
            </el-icon>
            {{ mode.label }}
          </el-radio-button>
        </el-radio-group>
      </div>
      <div class="preview-section">
        <h4>基本信息</h4>
        <p><strong>模板名称：</strong>{{ template.name }}</p>
        <p>
          <strong>框架类型：</strong
          >{{
            template.framework_type === "CUSTOM"
              ? "自定义"
              : template.framework_type
          }}
        </p>
        <p><strong>描述：</strong>{{ template.description }}</p>
      </div>

      <!-- 基础预览模式 -->
      <div v-if="currentPreviewMode === 'basic'" class="preview-section">
        <h4>提示词内容</h4>
        <div
          v-for="(value, key) in template.content"
          :key="key"
          class="content-item"
        >
          <h5>{{ formatContentKey(key) }}</h5>
          <p>{{ value }}</p>
        </div>
      </div>

      <!-- 对话预览模式 -->
      <div
        v-else-if="currentPreviewMode === 'chat'"
        class="preview-section chat-preview"
      >
        <div class="chat-container">
          <div class="message system">
            <el-avatar :size="40" src="/ai-avatar.png" />
            <div class="message-content">
              <p>我是您的AI助手，我将按照以下方式为您服务：</p>
              <template v-for="(value, key) in template.content" :key="key">
                <p>
                  <strong>{{ formatContentKey(key) }}：</strong>{{ value }}
                </p>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
    <el-empty v-else description="请选择一个模板" />
  </el-dialog>

  <!-- 内嵌模式 -->
  <div v-else class="template-preview">
    <div v-if="template" class="preview-content scrollable">
      <div class="preview-section">
        <h4>基本信息</h4>
        <p><strong>模板名称：</strong>{{ template.name }}</p>
        <p><strong>框架类型：</strong>{{ template.framework_type }}</p>
        <p><strong>描述：</strong>{{ template.description }}</p>
      </div>

      <div class="preview-section">
        <h4>提示词内容</h4>
        <template v-for="(value, key) in template.content" :key="key">
          <p>
            <strong>{{ formatContentKey(key) }}：</strong>{{ value }}
          </p>
        </template>
      </div>
    </div>
    <el-empty v-else description="请选择一个模板" />
  </div>
</template>

<script setup lang="ts">
import type { Template } from "@/types";
import { ref } from "vue";

defineProps<{
  modelValue?: boolean;
  template: Template | null;
  mode?: "dialog" | "inline";
}>();

defineEmits<{
  (e: "update:modelValue", value: boolean): void;
}>();

const previewModes = [
  { label: "基础预览", value: "basic", icon: "Document" },
  { label: "对话预览", value: "chat", icon: "ChatRound" },
];
const currentPreviewMode = ref("basic");

// 格式化内容键名
const formatContentKey = (key: string) => {
  // 将驼峰命名转换为空格分隔的词组，并将首字母大写
  const formatted = key
    .replace(/([A-Z])/g, " $1")
    .replace(/^./, (str) => str.toUpperCase());
  return formatted;
};
</script>

<style lang="scss" scoped>
.template-preview,
.template-preview-dialog {
  :deep(.el-dialog__body) {
    padding: 20px;
    max-height: 80vh;
    overflow-y: auto;
  }

  .preview-section {
    margin-bottom: 20px;
    overflow-wrap: break-word;
    word-wrap: break-word;
    word-break: break-word;
  }

  .preview-section:last-child {
    margin-bottom: 0;
  }

  .content-item {
    margin-bottom: 16px;
    padding: 16px;
    background-color: #f8f9fa;
    border-radius: 8px;
  }

  .content-item:last-child {
    margin-bottom: 0;
  }

  .content-item h5 {
    margin: 0 0 8px;
    color: #666;
    font-size: 14px;
  }

  .content-item p {
    margin: 0;
    color: #333;
    line-height: 1.6;
  }

  .chat-preview {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 20px;
  }

  .chat-container {
    max-width: 800px;
    margin: 0 auto;
  }

  .message {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
  }

  .message:last-child {
    margin-bottom: 0;
  }

  .message.system {
    .message-content {
      background-color: #fff;
      padding: 12px 16px;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    p {
      margin: 8px 0;
      line-height: 1.6;
    }

    p:first-child {
      margin-top: 0;
    }

    p:last-child {
      margin-bottom: 0;
    }
  }

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-thumb {
    background-color: var(--el-border-color);
    border-radius: 3px;
  }

  &::-webkit-scrollbar-track {
    background-color: transparent;
  }

  h3 {
    color: var(--el-color-primary);
    font-size: 18px;
    margin-bottom: 16px;
    font-family: "Orbitron", sans-serif;
    border-bottom: 1px solid var(--el-border-color);
    padding-bottom: 8px;
  }

  h4 {
    color: var(--el-text-color-primary);
    font-size: 16px;
    margin: 16px 0 12px;
    font-weight: 600;
  }

  .preview-section {
    margin-bottom: 24px;

    &:last-child {
      margin-bottom: 0;
    }
  }

  p {
    margin: 8px 0;
    color: var(--el-text-color-regular);
    line-height: 1.6;
    white-space: pre-wrap;
    overflow-wrap: break-word;
    word-wrap: break-word;
    word-break: break-word;

    strong {
      color: var(--el-text-color-primary);
      font-weight: 600;
      margin-right: 8px;
    }
  }
}
</style>
