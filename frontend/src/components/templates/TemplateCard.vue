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
            <el-tag>{{
              template.framework_type === "CUSTOM"
                ? "自定义"
                : template.framework_type
            }}</el-tag>
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
              title="打开分享对话框"
              @click="$emit('share', template)"
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
import dayjs from "dayjs";

const formatDate = (dateString: string) => {
  return dayjs(dateString).format("YYYY-MM-DD HH:mm:ss");
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
  height: 320px;
  width: 100%;
  cursor: pointer;
  min-width: 0;
}

.template-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-width: 0;
}

.template-info {
  flex: 1;
  width: 100%;
  overflow-y: auto;
  padding: 16px 20px;
}

.template-info h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}

.template-info .description {
  color: #333;
  font-size: 14px;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  min-height: 40px;
  line-height: 1.5;
}

.template-info .time {
  font-size: 12px;
  color: #666;
  margin: 6px 0;
  line-height: 1.5;
}

.template-actions {
  margin-top: auto;
  padding: 12px 20px;
  border-top: 1px solid #f0f0f0;
  background-color: #fff;
}

.template-actions :deep(.el-button-group) {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: flex-end;
}

.template-actions :deep(.el-button) {
  font-weight: 500;
  color: #ffffff;
  background-color: #409eff;
  border: none;
}

.template-actions :deep(.el-button:not(.el-button--danger):hover) {
  background-color: #66b1ff;
}

.template-actions :deep(.el-button--danger) {
  background-color: #f56c6c;
}

.template-actions :deep(.el-button--danger:hover) {
  background-color: #f78989;
}

.template-actions :deep(.button-text) {
  margin-left: 4px;
  font-size: 12px;
}

.box-card {
  height: 320px;
  width: 100%;
  transition: all 0.3s ease-in-out;
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.box-card :deep(.el-card__body) {
  background-color: #f8f9fa;
  padding: 0;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.box-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

/* 优化滚动条样式 */
.template-info::-webkit-scrollbar {
  width: 6px;
}

.template-info::-webkit-scrollbar-thumb {
  background-color: #ddd;
  border-radius: 3px;
}

.template-info::-webkit-scrollbar-track {
  background-color: #f8f9fa;
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
