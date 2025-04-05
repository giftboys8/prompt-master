<template>
  <div class="page-container">
    <div class="page-header">
      <h1>场景市场</h1>
    </div>

    <div class="operation-bar">
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索内容标题"
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
        <el-icon><Plus /></el-icon>生成内容
      </el-button>
    </div>

    <el-table v-loading="loading" :data="contents" style="width: 100%">
      <el-table-column prop="title" label="内容标题" />
      <el-table-column prop="content" label="生成内容" show-overflow-tooltip />
      <el-table-column prop="template_id" label="使用模板" />
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ new Date(row.created_at).toLocaleString() }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button type="primary" text @click="handleView(row)"
              >查看</el-button
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
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { Search, Plus } from "@element-plus/icons-vue";
import type { Content } from "@/types";

// 状态
const loading = ref(false);
const contents = ref<Content[]>([]);
const total = ref(0);
const currentPage = ref(1);
const pageSize = ref(10);
const searchQuery = ref("");

// 方法
const handleSearch = () => {
  // TODO: 实现搜索功能
};

const handleAdd = () => {
  // TODO: 实现新增功能
};

const handleView = (row: Content) => {
  // TODO: 实现查看功能
};

const handleDelete = (row: Content) => {
  // TODO: 实现删除功能
};

const handleSizeChange = (val: number) => {
  pageSize.value = val;
  // TODO: 重新加载数据
};

const handleCurrentChange = (val: number) => {
  currentPage.value = val;
  // TODO: 重新加载数据
};
</script>

<style scoped>
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
