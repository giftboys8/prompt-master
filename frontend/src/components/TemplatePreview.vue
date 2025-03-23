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
          <el-radio-button v-for="mode in previewModes" :key="mode.value" :label="mode.value">
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
        <p><strong>框架类型：</strong>{{ template.framework_type }}</p>
        <p><strong>描述：</strong>{{ template.description }}</p>
      </div>

      <!-- 基础预览模式 -->
      <div v-if="currentPreviewMode === 'basic'" class="preview-section">
        <h4>提示词内容</h4>
        <template v-if="template.framework_type === 'RTGO'">
          <div class="content-item">
            <h5>角色 (Role)</h5>
            <p>{{ template.content.role }}</p>
          </div>
          <div class="content-item">
            <h5>任务 (Task)</h5>
            <p>{{ template.content.task }}</p>
          </div>
          <div class="content-item">
            <h5>目标 (Goal)</h5>
            <p>{{ template.content.goal }}</p>
          </div>
          <div class="content-item">
            <h5>输出 (Output)</h5>
            <p>{{ template.content.output }}</p>
          </div>
        </template>

        <template v-else-if="template.framework_type === 'SPAR'">
          <div class="content-item">
            <h5>情境 (Situation)</h5>
            <p>{{ template.content.situation }}</p>
          </div>
          <div class="content-item">
            <h5>目的 (Purpose)</h5>
            <p>{{ template.content.purpose }}</p>
          </div>
          <div class="content-item">
            <h5>行动 (Action)</h5>
            <p>{{ template.content.action }}</p>
          </div>
          <div class="content-item">
            <h5>结果 (Result)</h5>
            <p>{{ template.content.result }}</p>
          </div>
        </template>

        <template v-else>
          <div class="content-item">
            <h5>自定义内容</h5>
            <p>{{ template.content.custom }}</p>
          </div>
        </template>
      </div>

      <!-- 对话预览模式 -->
      <div v-else-if="currentPreviewMode === 'chat'" class="preview-section chat-preview">
        <div class="chat-container">
          <div class="message system">
            <el-avatar :size="40" src="/ai-avatar.png" />
            <div class="message-content">
              <p>我是您的AI助手，我将按照以下方式为您服务：</p>
              <template v-if="template.framework_type === 'RTGO'">
                <p><strong>作为：</strong>{{ template.content.role }}</p>
                <p><strong>任务：</strong>{{ template.content.task }}</p>
                <p><strong>目标：</strong>{{ template.content.goal }}</p>
                <p><strong>输出：</strong>{{ template.content.output }}</p>
              </template>
              <template v-else-if="template.framework_type === 'SPAR'">
                <p><strong>情境：</strong>{{ template.content.situation }}</p>
                <p><strong>目的：</strong>{{ template.content.purpose }}</p>
                <p><strong>行动：</strong>{{ template.content.action }}</p>
                <p><strong>结果：</strong>{{ template.content.result }}</p>
              </template>
              <template v-else>
                <p>{{ template.content.custom }}</p>
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
        <template v-if="template.framework_type === 'RTGO'">
          <p><strong>角色(Role)：</strong>{{ template.content.role }}</p>
          <p><strong>任务(Task)：</strong>{{ template.content.task }}</p>
          <p><strong>目标(Goal)：</strong>{{ template.content.goal }}</p>
          <p><strong>输出(Output)：</strong>{{ template.content.output }}</p>
        </template>

        <template v-else-if="template.framework_type === 'SPAR'">
          <p><strong>情境(Situation)：</strong>{{ template.content.situation }}</p>
          <p><strong>目的(Purpose)：</strong>{{ template.content.purpose }}</p>
          <p><strong>行动(Action)：</strong>{{ template.content.action }}</p>
          <p><strong>结果(Result)：</strong>{{ template.content.result }}</p>
        </template>

        <template v-else>
          <p><strong>自定义内容：</strong>{{ template.content.custom }}</p>
        </template>
      </div>
    </div>
    <el-empty v-else description="请选择一个模板" />
  </div>
</template>

<script setup lang="ts">
import type { Template } from '@/types'

defineProps<{
  modelValue?: boolean;
  template: Template | null;
  mode?: 'dialog' | 'inline';
}>();

defineEmits<{
  (e: 'update:modelValue', value: boolean): void;
}>();
</script>

<style lang="scss" scoped>
.template-preview,
.template-preview-dialog {
  :deep(.el-dialog__body) {
    padding: 20px;
  }

  .preview-section {
    margin-bottom: 20px;
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
    font-family: 'Orbitron', sans-serif;
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

    strong {
      color: var(--el-text-color-primary);
      font-weight: 600;
      margin-right: 8px;
    }
  }
}
</style>