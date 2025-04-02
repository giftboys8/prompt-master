<template>
  <div class="search-bar">
    <el-input
      v-model="searchQuery"
      placeholder="搜索模板名称、描述或提示词内容"
      clearable
      @keyup.enter.prevent="handleSearch"
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
      @change="handleFilterChange"
    >
      <el-option
        v-for="role in roleOptions"
        :key="role.value"
        :label="role.label"
        :value="role.value"
      />
    </el-select>
    <framework-select
      v-model="selectedFramework"
      placeholder="框架类型"
      class="filter-select"
      @change="handleFilterChange"
    />
    <el-button type="primary" @click="handleSearch">搜索</el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onUnmounted } from "vue";
import { Search } from "@element-plus/icons-vue";
import { roleOptions } from "@/constants/template-options";
import FrameworkSelect from "@/components/FrameworkSelect.vue";
import debounce from "lodash/debounce";

const emit = defineEmits(["search"]);

const searchQuery = ref("");
const selectedRole = ref("");
const selectedFramework = ref(null);

const emitSearch = () => {
  emit("search", {
    query: searchQuery.value?.trim() || "",
    role: selectedRole.value || "",
    framework: selectedFramework.value || null,
  });
};

const handleSearch = () => {
  emit("search", {
    query: searchQuery.value?.trim() || "",
    role: selectedRole.value || "",
    framework: selectedFramework.value || null,
    forceRefresh: true // 添加强制刷新标记
  });
};

const debouncedSearch = debounce(emitSearch, 300);

const handleFilterChange = () => {
  debouncedSearch();
};

// 监听搜索查询的变化，但不自动触发搜索
watch(searchQuery, () => {
  // 这里可以添加一些额外的逻辑，比如在输入时更新UI状态
});

// 清除防抖函数
onUnmounted(() => {
  debouncedSearch.cancel();
});
</script>

<style scoped>
.search-bar {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
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
</style>
