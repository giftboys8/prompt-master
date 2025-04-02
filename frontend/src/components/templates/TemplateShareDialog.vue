<template>
  <el-dialog
    v-model="dialogVisible"
    :title="title"
    width="500px"
    destroy-on-close
    @open="onDialogOpen"
    @closed="onDialogClosed"
  >
    <div class="dialog-description">
      <el-alert
        title="在此页面选择用户和权限后，点击下方的'分享'按钮完成模板分享"
        type="info"
        :closable="false"
        show-icon
      />
    </div>
    <div class="share-dialog-content">
      <ShareForm
        :form="shareForm"
        :loading="loading"
        :user-options="userOptions"
        @search="handleSearch"
      />

      <ShareList :shares="shares" @revoke="handleRevoke" />
    </div>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          :loading="shareLoading"
          class="confirm-share-button"
          @click="handleShare"
        >
          分享
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import ShareForm from "./ShareForm.vue";
import ShareList from "./ShareList.vue";
import { useTemplateShare } from "@/composables/useTemplateShare";
import type { Template } from "@/types";

const props = defineProps<{
  modelValue: boolean;
  template: Template | null;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
  (e: "shared"): void;
}>();

// 对话框状态
const title = ref("分享模板");
const dialogVisible = ref(props.modelValue);

// 使用模板分享 composable
const {
  loading,
  shareLoading,
  shares,
  userOptions,
  shareForm,
  loadShares,
  handleSearch,
  handleShare: shareTemplate,
  handleRevoke: revokeShare,
  reset,
  updateTemplate,
} = useTemplateShare();

// 监听模板变化
watch(
  () => props.template,
  (newTemplate) => {
    updateTemplate(newTemplate);
    if (dialogVisible.value) {
      loadShares();
    }
  },
  { immediate: true },
);

// 监听对话框可见性
watch(
  () => props.modelValue,
  (val) => {
    dialogVisible.value = val;
  },
);

watch(dialogVisible, (val) => {
  emit("update:modelValue", val);
});

// 对话框打开时加载数据
const onDialogOpen = () => {
  loadShares();
};

// 对话框关闭时重置状态
const onDialogClosed = () => {
  reset();
};

// 处理分享
const handleShare = async () => {
  const success = await shareTemplate();
  if (success) {
    emit("shared");
  }
};

// 处理撤销分享
const handleRevoke = async (share: any) => {
  const success = await revokeShare(share);
  if (success) {
    emit("shared");
  }
};
</script>

<style scoped>
.dialog-description {
  margin-bottom: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.confirm-share-button {
  font-weight: bold;
  padding-left: 20px;
  padding-right: 20px;
}
</style>
