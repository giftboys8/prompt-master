<template>
  <div class="page-container">
    <div class="page-header">
      <h1>共享给我的提示词模板</h1>
      <div class="header-description">
        <el-alert
          title="这里展示了其他用户共享给您的所有模板"
          type="info"
          :closable="false"
          show-icon
        />
      </div>
    </div>

    <div class="operation-bar">
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
    </div>

    <el-row :gutter="20">
      <el-col
        v-for="template in sharedTemplates"
        :key="template.id"
        :xs="24"
        :sm="12"
        :md="8"
        :lg="6"
        class="mb-4"
      >
        <div class="template-item h-full">
          <el-card
            class="box-card h-full"
            shadow="hover"
            @click.stop="handlePreview(template)"
          >
            <div class="template-content">
              <div class="template-info">
                <h3>{{ template.name }}</h3>
                <div class="template-tags">
                  <el-tag class="mr-2">{{ template.framework_type }}</el-tag>
                  <el-tag type="warning" class="mr-2">共享</el-tag>
                  <el-tag :type="template.can_edit ? 'success' : 'info'">{{
                    template.can_edit ? "可编辑" : "只读"
                  }}</el-tag>
                </div>
                <p class="template-description">{{ template.description }}</p>
              </div>

              <div class="template-footer">
                <div class="template-meta">
                  <div class="meta-item">
                    <el-icon><User /></el-icon>
                    <span>共享者: {{ getOwnerName(template) }}</span>
                  </div>
                  <div class="meta-item">
                    <el-icon><Calendar /></el-icon>
                    <span>{{ formatDate(template.updated_at) }}</span>
                  </div>
                </div>

                <div class="template-actions">
                  <el-button
                    type="primary"
                    size="small"
                    @click.stop="handlePreview(template)"
                  >
                    查看
                  </el-button>
                  <el-button
                    v-if="template.can_edit"
                    type="success"
                    size="small"
                    @click.stop="handleEdit(template.id)"
                  >
                    编辑
                  </el-button>
                  <el-button
                    type="warning"
                    size="small"
                    @click.stop="handleClone(template)"
                  >
                    克隆
                  </el-button>
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </el-col>
    </el-row>

    <!-- 空状态 -->
    <el-empty
      v-if="sharedTemplates.length === 0 && !loading"
      description="暂无共享模板"
    >
      <el-button type="primary" @click="router.push('/templates')">
        返回模板列表
      </el-button>
    </el-empty>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="3" animated />
    </div>

    <!-- 预览模板对话框 -->
    <template-preview
      v-model="previewDialogVisible"
      :template="currentTemplate"
      mode="dialog"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import {
  Search,
  User,
  Calendar,
  Monitor,
  CopyDocument,
  EditPen,
} from "@element-plus/icons-vue";
import { getSharedWithMe } from "@/api/share";
import { cloneTemplate } from "@/api/templates";
import { useUserStore } from "@/stores/user";
import TemplatePreview from "@/components/TemplatePreview.vue";
import type { Template } from "@/types";

const router = useRouter();
const userStore = useUserStore();

// 数据
const sharedTemplates = ref<Template[]>([]);
const loading = ref(false);
const searchQuery = ref("");
const selectedRole = ref("");
const selectedFramework = ref("");
const previewDialogVisible = ref(false);
const currentTemplate = ref<Template | null>(null);

// 选项
const roleOptions = [
  { value: "DEVELOPER", label: "开发者" },
  { value: "PRODUCT_MANAGER", label: "产品经理" },
  { value: "TESTER", label: "测试" },
  { value: "DESIGNER", label: "设计师" },
  { value: "OPERATION", label: "运营" },
];

const frameworkOptions = [
  { value: "RTGO", label: "RTGO框架" },
  { value: "SPAR", label: "SPAR框架" },
  { value: "CUSTOM", label: "自定义框架" },
];

// 获取共享给我的模板
const fetchSharedTemplates = async () => {
  loading.value = true;
  try {
    const response = await getSharedWithMe();
    sharedTemplates.value = response.results;
  } catch (error) {
    console.error("获取共享模板失败:", error);
    ElMessage.error("获取共享模板失败");
  } finally {
    loading.value = false;
  }
};

// 搜索处理
const handleSearch = () => {
  fetchSharedTemplates();
};

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString();
};

// 获取模板所有者名称
const getOwnerName = (template: Template) => {
  // 这里应该根据实际API返回的数据结构进行调整
  // 假设API返回了所有者信息
  return template.created_by_username || "未知用户";
};

// 预览模板
const handlePreview = (template: Template) => {
  currentTemplate.value = template;
  previewDialogVisible.value = true;
};

// 测试模板
const handleTest = (template: Template) => {
  router.push({
    name: "template-test",
    query: { id: template.id.toString() },
  });
};

// 克隆模板
const handleClone = async (template: Template) => {
  // 这里应该实现克隆模板的逻辑
  ElMessage.success("克隆功能待实现");
};

// 编辑模板
const handleEdit = (id: string | number) => {
  router.push(`/templates/${id}/edit`);
};

onMounted(() => {
  fetchSharedTemplates();
});
</script>

<style scoped>
.page-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.header-description {
  margin-top: 16px;
}

.operation-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 16px;
}

.search-bar {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  flex: 1;
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

.template-description {
  color: #606266;
  font-size: 14px;
  margin: 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  min-height: 40px;
}

.template-footer {
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid var(--el-border-color-lighter);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.template-meta {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 4px;
}

.template-actions {
  display: flex;
  gap: 8px;
}

.template-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 8px 0;
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

.loading-container {
  padding: 24px;
}

/* 工具类 */
.mb-4 {
  margin-bottom: 16px;
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

/* 响应式布局 */
@media (max-width: 768px) {
  .template-actions :deep(.el-button) {
    padding: 8px;
  }

  .template-footer {
    flex-direction: column;
    gap: 12px;
  }

  .template-meta {
    order: 2;
  }

  .template-actions {
    order: 1;
    width: 100%;
    justify-content: flex-end;
  }
}
</style>
