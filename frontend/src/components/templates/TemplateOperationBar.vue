<template>
  <div class="operation-buttons">
    <el-upload
      :auto-upload="false"
      :show-file-list="false"
      accept=".json"
      @change="handleImport"
    >
      <el-button type="primary">
        <el-icon><Upload /></el-icon>导入
      </el-button>
    </el-upload>
    <el-button type="primary" @click="$emit('export')">
      <el-icon><Download /></el-icon>导出
    </el-button>
    <el-button type="primary" @click="$emit('create')">
      <el-icon><Plus /></el-icon>新增模板
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { Upload, Download, Plus } from '@element-plus/icons-vue'

const emit = defineEmits(['import', 'export', 'create'])

const handleImport = (file: any) => {
  emit('import', file)
}
</script>

<style scoped>
.operation-buttons {
  display: flex;
  gap: 10px;
}

:deep(.el-upload) {
  width: auto;
}
</style>