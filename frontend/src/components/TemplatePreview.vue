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
}

.preview-content {
  .scrollable {
    max-height: 60vh;
    overflow-y: auto;
    padding-right: 10px;

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