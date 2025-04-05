<template>
  <div class="framework-list">
    <div class="header">
      <h1>模板框架管理</h1>
      <div class="header-actions">
        <el-radio-group v-model="viewType" size="small">
          <el-radio-button value="list">列表视图</el-radio-button>
          <el-radio-button value="card">卡片视图</el-radio-button>
        </el-radio-group>
        <el-button type="primary" @click="handleCreate"> 创建框架 </el-button>
      </div>
    </div>

    <div v-loading="loading">
      <el-table v-if="viewType === 'list'" :data="frameworks" style="width: 100%" border>
      <el-table-column prop="name" label="框架名称" />
      <el-table-column
        prop="description"
        label="框架描述"
        show-overflow-tooltip
      />
      <el-table-column prop="modules" label="模块数量">
        <template #default="{ row }">
          {{ row.modules?.length || 0 }}
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column prop="updated_at" label="最后更新时间">
        <template #default="{ row }">
          {{ formatDate(row.updated_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button-group>
            <el-button type="primary" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button type="danger" @click="handleDelete(row)">
              删除
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
      </el-table>

      <div v-else-if="viewType === 'card'" class="card-view">
      <el-row :gutter="16">
        <el-col v-for="framework in frameworks" :key="framework.id" :span="4" class="mb-3">
          <el-card class="framework-card" shadow="hover">
            <div class="card-title">
              <h3>{{ framework.name }}</h3>
            </div>
            <div class="card-content">
              <p class="framework-description">{{ framework.description }}</p>
            </div>
            <div class="card-actions">
              <el-button-group>
                <el-button type="primary" size="small" @click="handleEdit(framework)">
                  编辑
                </el-button>
                <el-button type="danger" size="small" @click="handleDelete(framework)">
                  删除
                </el-button>
              </el-button-group>
            </div>
          </el-card>
        </el-col>
      </el-row>
      </div>
    </div>

    <div class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
import dayjs from "dayjs";
import {
  getFrameworks,
  deleteFramework,
  type Framework,
} from "@/api/frameworks";

const router = useRouter();
const loading = ref(false);
const frameworks = ref<Framework[]>([]);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);
const viewType = ref('list');

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return "未知";
  return dayjs(dateString).format("YYYY-MM-DD HH:mm:ss");
};

// 获取框架列表
const fetchFrameworks = async () => {
  loading.value = true;
  try {
    const response = await getFrameworks(currentPage.value, pageSize.value);
    frameworks.value = response.results;
    total.value = response.count;
  } catch (error) {
    console.error("获取框架列表失败:", error);
    ElMessage.error("获取框架列表失败");
  } finally {
    loading.value = false;
  }
};

// 创建框架
const handleCreate = () => {
  router.push("/frameworks/create");
};

// 编辑框架
const handleEdit = (row: Framework) => {
  router.push(`/frameworks/edit/${row.id}`);
};

// 删除框架
const handleDelete = (row: Framework) => {
  ElMessageBox.confirm("确认删除该框架吗？删除后将无法恢复。", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(async () => {
    try {
      await deleteFramework(row.id!);
      ElMessage.success("删除成功");
      fetchFrameworks();
    } catch (error) {
      console.error("删除失败:", error);
      ElMessage.error("删除失败");
    }
  });
};

// 处理页码变化
const handleCurrentChange = (page: number) => {
  currentPage.value = page;
  fetchFrameworks();
};

// 处理每页条数变化
const handleSizeChange = (size: number) => {
  pageSize.value = size;
  currentPage.value = 1;
  fetchFrameworks();
};

// 初始化
onMounted(() => {
  fetchFrameworks();
});
</script>

<style scoped>
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.framework-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.card-view {
  margin-top: 20px;
}

.framework-card {
  margin-bottom: 12px;
  background-color: #f8f9fa;
  height: 180px;
  display: flex;
  flex-direction: column;
}

.card-title {
  padding: 12px 16px 6px;
  border-bottom: 1px solid #f0f0f0;
}

.card-title h3 {
  margin: 0;
  color: #333;
  font-size: 14px;
  font-weight: bold;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-content {
  font-size: 12px;
  color: #666;
  padding: 8px 16px;
  flex-grow: 1;
  overflow-y: auto;
}

.card-actions {
  padding: 8px 16px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: flex-end;
}

.framework-description {
  margin: 0; /* 移除默认段落边距 */
  line-height: 1.5; /* 优化行高 */
}

.card-content p {
  margin: 6px 0; /* 减少段落间距 */
  line-height: 1.5; /* 稍微减小行高 */
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-content p:first-child {
  margin-top: 0;
}

.card-content p:last-child {
  margin-bottom: 0;
}

/* 添加悬停效果 */
.framework-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease-in-out;
}

/* 优化滚动条样式 */
.card-content::-webkit-scrollbar {
  width: 6px;
}

.card-content::-webkit-scrollbar-thumb {
  background-color: #ddd;
  border-radius: 3px;
}

.card-content::-webkit-scrollbar-track {
  background-color: #f8f9fa;
}
</style>
