<template>
  <el-form @submit.prevent="$emit('run-test')" label-position="top" class="variable-form">
    <div class="api-key-section">
      <h3>API密钥选择</h3>
      <div class="api-key-description">
        请选择用于测试的API密钥，确保选择的密钥处于启用状态。
      </div>
      <el-form-item required>
        <el-select 
          v-model="selectedApiKey" 
          placeholder="选择API密钥"
          filterable
          class="api-key-select"
          @change="handleApiKeyChange"
        >
          <el-option
            v-for="key in apiKeys"
            :key="key.id"
            :label="`${key.platform_name} - ${key.scene_name}`"
            :value="key"
          >
            <span>{{ key.platform_name }} - {{ key.scene_name }}</span>
            <span class="key-description">{{ key.description }}</span>
          </el-option>
        </el-select>
      </el-form-item>
    </div>

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
import { ref, computed, onMounted } from 'vue'
import type { Template } from '@/types'
import { getApiKeys } from '@/api/apikeys'
import { ElMessage } from 'element-plus'

const props = defineProps<{
  template: Template
  variables: Record<string, string>
  isRunning: boolean
}>()

// API密钥相关
const apiKeys = ref<any[]>([])
const selectedApiKey = ref<any>(null)

// 获取API密钥列表
const fetchApiKeys = async () => {
  try {
    const response = await getApiKeys()
    if (response && response.results) {
      apiKeys.value = response.results.filter((key: any) => key.is_active)
    }
  } catch (error: any) {
    ElMessage.error('获取API密钥列表失败：' + (error.message || '未知错误'))
  }
}

// 处理API密钥选择
const handleApiKeyChange = (key: any) => {
  selectedApiKey.value = key
  emit('update:apiKey', key)
}

onMounted(() => {
  fetchApiKeys()
})

const emit = defineEmits<{
  (e: 'update:variables', value: Record<string, string>): void
  (e: 'update:apiKey', value: any): void
  (e: 'run-test'): void
}>();

// 计算表单是否有效
const isFormValid = computed(() => {
  return selectedApiKey.value && props.template.variables.every(
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

.api-key-section,
.variables-section {
  padding: 20px;
  border-radius: 12px;
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
  color: var(--text-primary);
  margin-bottom: 24px;

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

.api-key-select {
  width: 100%;
}

.api-key-description {
  margin-bottom: 20px;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
  padding: 12px;
  background-color: var(--bg-card);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.key-description {
  margin-left: 8px;
  font-size: 12px;
  color: var(--text-secondary);
}
</style>