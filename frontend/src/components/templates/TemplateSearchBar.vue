<template>
  <div class="search-bar">
    <el-input
      v-model="searchQuery"
      placeholder="搜索模板名称、描述或提示词内容"
      clearable
      @clear="handleSearch"
      @keyup.enter="handleSearch"
    >
      <template #prefix>
        <el-icon><Search /></el-icon>
      </template>
    </el-input>
    <el-select
      v-model="selectedRole"
      clearable
      placeholder="选择角色"
      class="filter-select"
      @change="handleSearch"
    >
      <el-option
        v-for="role in roleOptions"
        :key="role.value"
        :label="role.label"
        :value="role.value"
      />
    </el-select>
    <el-select
      v-model="selectedFramework"
      clearable
      placeholder="框架类型"
      class="filter-select"
      @change="handleSearch"
    >
      <el-option
        v-for="framework in frameworkOptions"
        :key="framework.value"
        :label="framework.label"
        :value="framework.value"
      />
    </el-select>
    <el-button type="primary" @click="handleSearch">搜索</el-button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { roleOptions, frameworkOptions } from '@/constants/template-options'

const emit = defineEmits(['search'])

const searchQuery = ref('')
const selectedRole = ref('')
const selectedFramework = ref('')

const handleSearch = () => {
  emit('search', {
    query: searchQuery.value,
    role: selectedRole.value,
    framework: selectedFramework.value
  })
}
</script>

<style scoped>
.search-bar {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.filter-select {
  min-width: 160px;
}

@media (max-width: 768px) {
  .search-bar {
    flex-direction: column;
  }
  
  .filter-select {
    width: 100%;
  }
}
</style>