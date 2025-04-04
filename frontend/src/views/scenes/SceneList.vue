<template>
  <div class="page-container">
    <div class="page-header">
      <h1>业务场景</h1>
    </div>

    <div class="operation-bar">
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索场景名称"
          clearable
          @clear="handleSearch"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
      </div>
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>新增场景
      </el-button>
    </div>

    <el-row v-loading="loading" :gutter="20" class="scene-cards">
      <el-col
        v-for="scene in scenes"
        :key="scene.id"
        :xs="24"
        :sm="12"
        :md="8"
        :lg="6"
        :xl="4"
      >
        <el-card class="scene-card" :body-style="{ padding: '0px' }" @click="showPreview(scene)">
          <div class="scene-card-content">
            <div class="scene-header">
              <h3 class="scene-name" :title="scene.name">{{ scene.name }}</h3>
              <div class="scene-actions">
                <el-dropdown trigger="click" @command="handleCommand">
                  <el-button type="primary" text @click.stop>
                    <el-icon><More /></el-icon>
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item :command="{ action: 'edit', scene }">
                        <el-icon><Edit /></el-icon>编辑
                      </el-dropdown-item>
                      <el-dropdown-item :command="{ action: 'delete', scene }">
                        <el-icon><Delete /></el-icon>删除
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
            <div class="scene-version">
              <el-tag size="small" type="info">v{{ scene.version }}</el-tag>
            </div>
            <div class="scene-description" :title="scene.description">
              {{ scene.description }}
            </div>
            <div class="scene-tags">
              <el-tag size="small" type="success">{{ scene.category }}</el-tag>
              <el-tag
                v-for="role in scene.target_roles"
                :key="role"
                size="small"
                type="warning"
                class="role-tag"
              >
                {{ role.replace(/['\[\]]/g, '') }}
              </el-tag>
            </div>
            <div class="scene-footer">
              <span class="scene-time">
                {{ new Date(scene.created_at).toLocaleDateString() }}
              </span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <div class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[12, 24, 36, 48]"
        :total="total"
        layout="total, sizes, prev, pager, next"
      />
    </div>

    <ScenePreviewModal
      :scene="selectedScene"
      :visible="previewModalVisible"
      @update:visible="previewModalVisible = $event"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { ElMessageBox, ElMessage } from "element-plus";
import { Search, Plus, More, Edit, Delete } from "@element-plus/icons-vue";
import type { Scene } from "@/types";
import { getScenes, deleteScene, getSceneDetail } from "@/api/scenes";
import ScenePreviewModal from "@/components/ScenePreviewModal.vue";

const router = useRouter();

// 状态
const loading = ref(false);
const scenes = ref<Scene[]>([]);
const total = ref(0);
const currentPage = ref(1);
const pageSize = ref(12);
const searchQuery = ref("");
const selectedScene = ref<Scene | null>(null);
const previewModalVisible = ref(false);

// 加载场景列表
const loadScenes = async () => {
  loading.value = true;
  try {
    const response = await getScenes({
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value,
    });
    // 确保我们获取了所有必要的字段，并正确处理 target_roles
    scenes.value = response.results.map(scene => ({
      ...scene,
      version: scene.version || 'N/A',
      target_roles: Array.isArray(scene.target_roles) 
        ? scene.target_roles.map(role => role.replace(/['\[\]]/g, ''))
        : typeof scene.target_roles === 'string'
          ? scene.target_roles.replace(/['\[\]]/g, '').split(',').map(r => r.trim())
          : [],
    }));
    total.value = response.count;
  } catch (error) {
    console.error("获取场景列表失败:", error);
    ElMessage.error("获取场景列表失败");
  } finally {
    loading.value = false;
  }
};

// 初始化加载
onMounted(() => {
  loadScenes();
});

// 方法
const handleSearch = () => {
  currentPage.value = 1;
  loadScenes();
};

const handleAdd = () => {
  router.push("/scenes/create");
};

const handleEdit = (row: Scene) => {
  router.push(`/scenes/${row.id}/edit`);
};

const handleDelete = async (row: Scene) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除场景 "${row.name}" 吗？此操作不可恢复。`,
      "删除确认",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      },
    );

    await deleteScene(row.id);
    ElMessage.success("删除场景成功");
    loadScenes();
  } catch (error: any) {
    if (error !== "cancel") {
      console.error("删除场景失败:", error);
      ElMessage.error("删除场景失败");
    }
  }
};

const showPreview = async (scene: Scene) => {
  console.log('Showing preview for scene:', scene);
  try {
    loading.value = true;
    // 获取包含任务信息的场景详情
    const detailedScene = await getSceneDetail(scene.id);
    console.log('Scene detail with tasks:', detailedScene);
    
    // 确保 target_roles 字段被正确处理
    const processedScene = {
      ...detailedScene,
      target_roles: Array.isArray(detailedScene.target_roles) 
        ? detailedScene.target_roles
        : typeof detailedScene.target_roles === 'string'
          ? detailedScene.target_roles.replace(/['\\[\\]]/g, '').split(',').map(r => r.trim())
          : []
    };
    
    selectedScene.value = processedScene;
    previewModalVisible.value = true;
  } catch (error) {
    console.error('Failed to fetch scene details:', error);
    ElMessage.error('获取场景详情失败');
    // 如果获取详情失败，仍然显示基本信息
    selectedScene.value = scene;
    previewModalVisible.value = true;
  } finally {
    loading.value = false;
  }
};

const handleCommand = ({ action, scene }: { action: string; scene: Scene }) => {
  if (action === 'edit') {
    handleEdit(scene);
  } else if (action === 'delete') {
    handleDelete(scene);
  }
};

// 监听分页变化
watch([currentPage, pageSize], () => {
  loadScenes();
});
</script>

<style scoped>
.scene-cards {
  margin: 20px 0;
}

.scene-card {
  height: 100%;
  margin-bottom: 20px;
  transition: all 0.3s;
}

.scene-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.scene-card-content {
  padding: 16px;
}

.scene-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.scene-name {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
  padding-right: 8px;
}

.scene-version {
  margin-bottom: 12px;
}

.scene-description {
  color: #606266;
  font-size: 14px;
  margin-bottom: 16px;
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.scene-tags {
  margin-bottom: 12px;
  min-height: 24px;
}

.role-tag {
  margin-left: 8px;
}

.scene-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #909399;
  font-size: 12px;
}

.scene-time {
  color: #909399;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>