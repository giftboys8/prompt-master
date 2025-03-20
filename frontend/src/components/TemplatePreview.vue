<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    title="模板预览"
    width="50%"
    destroy-on-close
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
h3 {
  margin: 1rem 0;
  font-size: 1.2rem;
  color: var(--el-text-color-primary);
}

p {
  margin: 0.5rem 0;
  color: var(--el-text-color-regular);
  
  strong {
    color: var(--el-text-color-primary);
  }
}

.el-table {
  margin-top: 1rem;
}
</style>