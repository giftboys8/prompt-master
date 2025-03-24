<template>
  <div class="framework-list">
    <div class="header">
      <h1>模板框架管理</h1>
      <el-button type="primary" @click="handleCreate"> 创建框架 </el-button>
    </div>

    <el-table v-loading="loading" :data="frameworks" style="width: 100%" border>
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
import dayjs from 'dayjs';
import {
  getFrameworks,
  deleteFramework,
  type Framework,
} from "@/api/frameworks";

const router = useRouter();
const loading = ref(false);
const frameworks = ref<Framework[]>([]);

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '未知';
  return dayjs(dateString).format('YYYY-MM-DD HH:mm:ss');
};

// 获取框架列表
const fetchFrameworks = async () => {
  loading.value = true;
  try {
    const response = await getFrameworks();
    frameworks.value = response.results || [];
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

// 初始化
onMounted(() => {
  fetchFrameworks();
});
</script>

<style scoped>
.framework-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>
