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
          <div class="mb-2">
            <el-tag class="mr-2">{{ template.framework_type }}</el-tag>
            <el-tag type="info" size="small">{{ template.modules?.length || 0 }} 个模块</el-tag>
          </div>
          <p class="description mb-2">{{ template.description }}</p>
          <p class="time mb-2">
            创建时间：{{ formatDate(template.created_at) }}
          </p>
          <p class="time mb-2">
            最后更新：{{ formatDate(template.updated_at) }}
          </p>
        </div>
        <div class="template-actions" @click.stop>
          <el-button-group>
            <el-button type="primary" text @click="$emit('edit', template)"
              >编辑</el-button
            >
            <el-button type="primary" text @click="$emit('test', template)"
              >测试</el-button
            >
            <el-button type="primary" text @click="$emit('history', template)">
              <el-icon><Timer /></el-icon>
            </el-button>
            <el-button type="primary" text @click="$emit('clone', template)">
              <el-icon><CopyDocument /></el-icon>
            </el-button>
            <el-button
              v-if="user?.id === template.created_by"
              type="primary"
              text
              @click="$emit('share', template)"
              title="打开分享对话框"
            >
              <el-icon><Share /></el-icon>
              <span class="button-text">分享</span>
            </el-button>
            <el-button type="danger" text @click="$emit('delete', template)"
              >删除</el-button
            >
          </el-button-group>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { Timer, CopyDocument, Share } from "@element-plus/icons-vue";
import type { Template } from "@/types";
import { useUserStore } from "@/stores/user";
import { storeToRefs } from "pinia";
import dayjs from 'dayjs';

const formatDate = (dateString: string) => {
  return dayjs(dateString).format('YYYY-MM-DD HH:mm:ss');
};

const { user } = storeToRefs(useUserStore());

defineProps({
  template: {
    type: Object as () => Template,
    required: true,
  },
});

defineEmits(["edit", "test", "history", "clone", "delete", "preview", "share"]);
</script>

<style scoped>
.template-item {
  height: 100%;
  cursor: pointer;
  min-width: 0; /* 防止flex子项溢出 */
}

.template-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-width: 0; /* 防止内容溢出 */
}

.template-info {
  flex: 1;
  width: 100%;
  overflow: hidden; /* 确保内容不会溢出 */
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
  border-top: 1px solid #ebeef5;
}

.template-actions :deep(.el-button-group) {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.template-actions :deep(.button-text) {
  margin-left: 4px;
  font-size: 12px;
}

.template-item:hover {
  transform: translateY(-2px);
  transition: all 0.3s;
}

.box-card {
  height: 100%;
  transition: all 0.3s;
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.box-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.mb-2 {
  margin-bottom: 8px;
}

.mr-2 {
  margin-right: 8px;
}

.h-full {
  height: 100%;
}
</style>
