<template>
  <el-form @submit.prevent="$emit('run-test')" label-position="top" class="variable-form">
    <div class="variables-section">
      <h3>变量设置</h3>
      <div class="variables-description">
        请填写以下变量的值，这些值将用于生成最终的提示词。
      </div>
      
      <el-form-item
        v-for="variable in template.variables"
        :key="variable.name"
        :required="true"
      >
        <template #label>
          <div class="variable-label">
            <span>{{ variable.name }}</span>
            <span class="variable-description-inline">({{ variable.description }})</span>
          </div>
        </template>
        <div class="variable-input">
          <el-input
            :model-value="variables[variable.name]"
            @update:modelValue="handleVariableInput(variable.name, $event)"
            :placeholder="'请输入' + variable.name"
          >
            <template #append v-if="variable.default_value">
              <el-button @click="useDefaultValue(variable.name, variable.default_value)">
                使用默认值
              </el-button>
            </template>
          </el-input>
        </div>
      </el-form-item>
    </div>

    <el-form-item>
      <el-button 
        type="primary" 
        native-type="submit" 
        :disabled="!isFormValid"
        :loading="isRunning"
      >
        运行测试
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Template } from '@/types'

const props = defineProps<{
  template: Template
  variables: Record<string, string>
  isRunning: boolean
}>()

const emit = defineEmits<{
  (e: 'update:variables', value: Record<string, string>): void
  (e: 'run-test'): void
}>()

// 计算表单是否有效
const isFormValid = computed(() => {
  return props.template.variables.every(
    variable => !!props.variables[variable.name]
  )
})

// 处理变量输入
const handleVariableInput = (name: string, value: string) => {
  emit('update:variables', {
    ...props.variables,
    [name]: value
  })
}

// 使用默认值
const useDefaultValue = (variableName: string, defaultValue: string) => {
  handleVariableInput(variableName, defaultValue)
}
</script>

<style lang="scss" scoped>
.variable-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.variables-section {
  padding: 20px;
  border-radius: 12px;
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
  color: var(--text-primary);

  h3 {
    color: var(--primary-color);
    font-size: 18px;
    margin-bottom: 16px;
    font-family: 'Orbitron', sans-serif;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 8px;
  }
}

.variables-description {
  margin-bottom: 20px;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
  padding: 12px;
  background-color: var(--bg-card);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.variable-label {
  display: flex;
  align-items: center;
  gap: 8px;
  line-height: 1.4;
}

.variable-description-inline {
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: normal;
}

.variable-input {
  position: relative;
}
</style>