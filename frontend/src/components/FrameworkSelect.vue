<!-- FrameworkSelect.vue -->
<template>
  <div class="framework-select">
    <el-select
      v-model="selectedFramework"
      :placeholder="placeholder"
      :disabled="disabled"
      :loading="loading"
      clearable
      @change="handleChange"
    >
      <el-option
        v-for="framework in frameworks"
        :key="framework.id"
        :label="framework.name"
        :value="framework.id"
      >
        <div class="framework-option">
          <span>{{ framework.name }}</span>
          <small v-if="showDescription" class="description">{{ framework.description }}</small>
        </div>
      </el-option>
    </el-select>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { getFrameworks } from '@/api/frameworks'
import type { Framework } from '@/api/frameworks'

const props = defineProps({
  modelValue: {
    type: [Number, null],
    default: null
  },
  placeholder: {
    type: String,
    default: '请选择框架'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  showDescription: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const frameworks = ref<Framework[]>([])
const selectedFramework = ref(props.modelValue)
const loading = ref(false)

const fetchFrameworks = async () => {
  loading.value = true
  try {
    const response = await getFrameworks()
    console.log('Frameworks API Response:', response)
    frameworks.value = response.results || response.data || []
    console.log('Frameworks after assignment:', frameworks.value)
  } catch (error) {
    console.error('获取框架列表失败:', error)
  } finally {
    loading.value = false
  }
}

const handleChange = (value: number | null) => {
  emit('update:modelValue', value)
  if (value === null) {
    emit('change', null)
  } else {
    const selectedItem = frameworks.value.find(item => item.id === value)
    emit('change', value)  // 直接传递ID而不是整个对象
  }
}

// 监听外部传入的值变化
watch(
  () => props.modelValue,
  (newVal) => {
    selectedFramework.value = newVal
  }
)

onMounted(() => {
  fetchFrameworks()
})
</script>

<style scoped lang="scss">
.framework-select {
  width: 100%;
  
  :deep(.el-select) {
    width: 100%;
  }
}

.framework-option {
  display: flex;
  flex-direction: column;
  gap: 4px;
  
  .description {
    color: #999;
    font-size: 12px;
  }
}
</style>