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

    <el-table v-loading="loading" :data="scenes" style="width: 100%">
      <el-table-column prop="name" label="场景名称" />
      <el-table-column
        prop="description"
        label="场景描述"
        show-overflow-tooltip
      />
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ new Date(row.created_at).toLocaleString() }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button type="primary" text @click="handleEdit(row)"
              >编辑</el-button
            >
            <el-button type="danger" text @click="handleDelete(row)"
              >删除</el-button
            >
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { ElMessageBox, ElMessage } from "element-plus";
import { Search, Plus } from "@element-plus/icons-vue";
import type { Scene } from "@/types";
import { getScenes, deleteScene } from "@/api/scenes";

const router = useRouter();

// 状态
const loading = ref(false);
const scenes = ref<Scene[]>([]);
const total = ref(0);
const currentPage = ref(1);
const pageSize = ref(10);
const searchQuery = ref("");

// 加载场景列表
const loadScenes = async () => {
  loading.value = true;
  try {
    const response = await getScenes({
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value,
    });
    scenes.value = response.results;
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

// 监听分页变化
watch([currentPage, pageSize], () => {
  loadScenes();
});
</script>

<style scoped>
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
