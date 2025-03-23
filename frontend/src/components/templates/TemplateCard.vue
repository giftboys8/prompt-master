<template>
  <div class="template-item h-full">
    <el-card 
      class="box-card h-full" 
      shadow="hover"
      @click.stop="$emit('preview', template)"
    >
      <div class="template-content">
        <div class="template-info">
          <h3 class="mb-2">{{ template.name }}</h3>
          <el-tag class="mb-2">{{ template.framework_type }}</el-tag>
          <p class="description mb-2">{{ template.description }}</p>
          <p class="time mb-2">创建时间：{{ new Date(template.created_at).toLocaleString() }}</p>
        </div>
        <div class="template-actions" @click.stop>
          <el-button-group>
            <el-button type="primary" text @click="$emit('edit', template)">编辑</el-button>
            <el-button type="primary" text @click="$emit('test', template)">测试</el-button>
            <el-button type="primary" text @click="$emit('history', template)">
              <el-icon><Timer /></el-icon>
            </el-button>
            <el-button type="primary" text @click="$emit('clone', template)">
              <el-icon><CopyDocument /></el-icon>
            </el-button>
            <el-button type="danger" text @click="$emit('delete', template)">删除</el-button>
          </el-button-group>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
import { Timer, CopyDocument } from '@element-plus/icons-vue'
import type { Template } from '@/types'

defineProps({
  template: {
    type: Object as () => Template,
    required: true
  }
})

defineEmits(['edit', 'test', 'history', 'clone', 'delete', 'preview'])
</script>

<style scoped>
.template-item {
  height: 100%;
  cursor: pointer;
}

.template-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.template-info {
  flex: 1;
}

.template-info h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.template-info .description {
  color: #606266;
  font-size: 14px;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  min-height: 40px;
}

.template-info .time {
  font-size: 12px;
  color: #909399;
  margin: 0;
}

.template-actions {
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid #EBEEF5;
}

.template-actions :deep(.el-button-group) {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.template-item:hover {
  transform: translateY(-2px);
  transition: all 0.3s;
}

.box-card {
  height: 100%;
  transition: all 0.3s;
  cursor: pointer;
}

.box-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.mb-2 {
  margin-bottom: 8px;
}

.h-full {
  height: 100%;
}
</style>