<template>
  <div class="share-form">
    <el-form :model="form" label-width="80px">
      <el-form-item label="用户">
        <el-select
          v-model="form.userId"
          filterable
          remote
          reserve-keyword
          placeholder="请输入用户名搜索"
          :remote-method="onSearch"
          :loading="loading"
        >
          <el-option
            v-for="user in userOptions"
            :key="user.id"
            :label="user.username"
            :value="user.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="权限">
        <el-switch
          v-model="form.canEdit"
          active-text="可编辑"
          inactive-text="只读"
        />
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import type { ShareFormState } from "@/composables/useTemplateShare";
import type { User } from "@/types";

defineProps<{
  form: ShareFormState;
  loading: boolean;
  userOptions: User[];
}>();

const emit = defineEmits<{
  (e: "search", query: string): void;
  (e: "update:form", value: ShareFormState): void;
}>();

const onSearch = (query: string) => {
  emit("search", query);
};
</script>

<style scoped>
.share-form {
  margin-bottom: 20px;
}
</style>
