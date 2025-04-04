<template>
  <el-dialog
    v-model="dialogVisible"
    :title="scene ? scene.name : '场景预览'"
    width="60%"
    @close="closeDialog"
  >
    <div v-if="scene" class="scene-preview">
      <div class="scene-info">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="场景分类">{{ scene.category }}</el-descriptions-item>
          <el-descriptions-item label="版本号">{{ scene.version }}</el-descriptions-item>
          <el-descriptions-item label="场景描述" :span="2">{{ scene.description }}</el-descriptions-item>
          <el-descriptions-item label="目标角色" :span="2">
            <el-tag
              v-for="role in parsedTargetRoles"
              :key="role"
              size="small"
              type="warning"
              class="role-tag"
            >
              {{ role }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(scene.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="scene.status ? 'success' : 'danger'">
              {{ scene.status ? '启用' : '禁用' }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <div class="scene-tasks">
        <h3>任务列表</h3>
          <el-table :data="scene.tasks || []" style="width: 100%">
          <el-table-column type="expand">
            <template #default="props">
              <div class="task-detail">
                <el-descriptions :column="1" border>
                  <el-descriptions-item label="任务描述">
                    {{ props.row.description }}
                  </el-descriptions-item>
                  <el-descriptions-item label="关联模板">
                    <div v-if="props.row.template_name" class="template-info">
                      <p><strong>模板名称：</strong>{{ props.row.template_name }}</p>
                      <p v-if="props.row.template_description">
                        <strong>模板描述：</strong>{{ props.row.template_description }}
                      </p>
                    </div>
                    <span v-else>未关联模板</span>
                  </el-descriptions-item>
                  <el-descriptions-item label="创建时间">
                    {{ formatDate(props.row.created_at) }}
                  </el-descriptions-item>
                </el-descriptions>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="name" label="任务名称" min-width="120" />
          <el-table-column prop="description" label="任务描述" min-width="200">
            <template #default="scope">
              <el-tooltip :content="scope.row.description" placement="top" effect="light">
                <span>{{ truncate(scope.row.description, 50) }}</span>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column label="关联模板" min-width="180">
            <template #default="scope">
              <template v-if="scope.row.template_name">
                <el-tooltip :content="scope.row.template_description || ''" placement="top" effect="light">
                  <span>{{ scope.row.template_name }}</span>
                </el-tooltip>
              </template>
              <template v-else-if="scope.row.template">
                <span>模板ID: {{ scope.row.template }}</span>
              </template>
              <span v-else>-</span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    <div v-else class="empty-state">
      <p>暂无场景数据</p>
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits, watch, computed } from 'vue';
import { ElMessageBox } from 'element-plus';
import { Scene } from '@/types';

const props = defineProps<{
  scene: Scene | null;
  visible: boolean;
}>();

const emit = defineEmits(['update:visible']);

const dialogVisible = ref(props.visible);

// 解析目标角色
const parsedTargetRoles = computed(() => {
  if (!props.scene?.target_roles) return [];
  const roles = props.scene.target_roles;
  
  if (Array.isArray(roles)) {
    return roles.map(role => typeof role === 'string' ? role.trim() : JSON.stringify(role).replace(/^"|"$/g, '').trim());
  }
  
  if (typeof roles === 'string') {
    try {
      const parsed = JSON.parse(roles);
      if (Array.isArray(parsed)) {
        return parsed.map(role => typeof role === 'string' ? role.trim() : JSON.stringify(role).replace(/^"|"$/g, '').trim());
      }
      return [roles.trim()];
    } catch (e) {
      return [roles.trim()];
    }
  }
  
  return [JSON.stringify(roles).replace(/^"|"$/g, '').trim()];
});

watch(() => props.visible, (newValue) => {
  dialogVisible.value = newValue;
});

const closeDialog = () => {
  emit('update:visible', false);
};

// 格式化日期
const formatDate = (dateString: string) => {
  if (!dateString) return '-';
  try {
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (e) {
    return dateString;
  }
};

// 添加截断文本的过滤器
const truncate = (text: string, length: number) => {
  if (!text) return '';
  if (text.length <= length) {
    return text;
  }
  return text.slice(0, length) + '...';
};
</script>

<style scoped>
.scene-preview {
  padding: 20px;
}

.scene-info {
  margin-bottom: 20px;
}

.role-tag {
  margin: 0 5px 5px 0;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: normal;
  word-break: break-all;
  display: inline-block;
}

.empty-state {
  text-align: center;
  padding: 20px;
  color: #909399;
}

.task-detail {
  padding: 20px;
  background-color: #f8f9fa;
}

.template-info {
  margin: 0;
}

.template-info p {
  margin: 5px 0;
}

:deep(.el-descriptions) {
  margin-bottom: 20px;
}

:deep(.el-descriptions__cell) {
  padding: 12px 20px;
}

:deep(.el-table__expanded-cell) {
  padding: 20px !important;
}

:deep(.el-descriptions__label) {
  width: 120px;
  font-weight: bold;
  color: #606266;
}
</style>