<template>
  <div v-if="shares.length > 0" class="share-list">
    <h4>已分享给：</h4>
    <el-table :data="shares" style="width: 100%">
      <el-table-column prop="shared_with.username" label="用户" />
      <el-table-column
        v-if="showTemplateName"
        prop="template_name"
        label="模板名称"
      />
      <el-table-column prop="can_edit" label="权限">
        <template #default="{ row }">
          <el-tag :type="row.can_edit ? 'success' : 'info'">
            {{ row.can_edit ? "可编辑" : "只读" }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button type="danger" size="small" @click="$emit('revoke', row)">
            撤销
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import type { SharedTemplate } from "@/types";
import { computed } from "vue";

const props = defineProps<{
  shares: SharedTemplate[];
}>();

defineEmits<{
  (e: "revoke", share: SharedTemplate): void;
}>();

// 检查是否有任何分享项包含模板名称
const showTemplateName = computed(() => {
  return props.shares.some((share) => share.template_name !== undefined);
});
</script>

<style scoped>
.share-list {
  margin-top: 20px;
}

.share-list h4 {
  margin-bottom: 10px;
}
</style>
