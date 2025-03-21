<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    title="模板预览"
    width="60%"
    destroy-on-close
    :modal-class="'template-preview-modal'"
    :close-on-click-modal="false"
  >
    <template v-if="template">
      <h3>基本信息</h3>
      <p><strong>模板名称：</strong>{{ template.name }}</p>
      <p><strong>框架类型：</strong>{{ template.framework_type }}</p>
      <p><strong>描述：</strong>{{ template.description }}</p>

      <h3>提示词内容</h3>
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

      <h3>变量列表</h3>
      <el-table :data="template.variables">
        <el-table-column prop="name" label="变量名称" />
        <el-table-column prop="default_value" label="默认值" />
        <el-table-column prop="description" label="描述" />
      </el-table>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import type { Template } from '@/types'

defineProps<{
  modelValue: boolean
  template?: Template
}>()

defineEmits(['update:modelValue'])
</script>

<style lang="scss" scoped>
@use '@/styles/tech-theme.scss' as *;

h3 {
  margin: 1.5rem 0 1rem;
  font-size: 1.3rem;
  color: var(--primary-color);
  font-family: 'Orbitron', sans-serif;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.5rem;
}

p {
  margin: 0.75rem 0;
  color: var(--text-primary);
  line-height: 1.6;
  
  strong {
    color: var(--neon-blue);
    font-weight: 600;
  }
}

.el-table {
  margin-top: 1rem;
  --el-table-border-color: var(--border-color);
  --el-table-header-bg-color: var(--bg-hover);
  --el-table-bg-color: var(--bg-card);
  --el-table-tr-bg-color: var(--glass-bg);
  
  :deep(.el-table__header) {
    th {
      background-color: var(--bg-hover);
      color: var(--text-primary);
      font-weight: 600;
    }
  }
  
  :deep(.el-table__row) {
    td {
      color: var(--text-secondary);
    }
  }
}

:deep(.el-dialog) {
  background: var(--bg-card);
  border-radius: 16px;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color);
  
  .el-dialog__header {
    padding: 1.5rem;
    margin-right: 0;
    border-bottom: 1px solid var(--border-color);
    
    .el-dialog__title {
      color: var(--text-primary);
      font-weight: 600;
      font-size: 1.5rem;
      font-family: 'Orbitron', sans-serif;
    }
  }
  
  .el-dialog__body {
    padding: 1.5rem;
    color: var(--text-primary);
  }
  
  .el-dialog__headerbtn {
    top: 1.5rem;
    right: 1.5rem;
    
    .el-dialog__close {
      color: var(--text-secondary);
      
      &:hover {
        color: var(--primary-color);
      }
    }
  }
}
</style>