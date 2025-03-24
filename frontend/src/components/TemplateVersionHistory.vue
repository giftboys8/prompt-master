<template>
  <el-dialog
    v-model="dialogVisible"
    title="版本历史"
    width="70%"
    :before-close="handleClose"
    destroy-on-close
  >
    <div v-loading="loading">
      <el-table :data="versions" style="width: 100%">
        <el-table-column prop="version_number" label="版本" width="80" />
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="framework" label="框架类型" width="100">
          <template #default="{ row }">
            <el-tag>{{ row.framework?.type || '自定义' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="created_by_username"
          label="创建者"
          width="120"
        />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ new Date(row.created_at).toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button type="primary" text @click="handlePreview(row)">
                预览
              </el-button>
              <el-button
                type="primary"
                text
                :disabled="row.is_current"
                @click="handleRestore(row)"
              >
                恢复
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 预览对话框 -->
    <el-dialog
      v-model="previewDialogVisible"
      title="版本预览"
      width="50%"
      append-to-body
      destroy-on-close
    >
      <template v-if="currentVersion">
        <h3>基本信息</h3>
        <p><strong>模板名称：</strong>{{ currentVersion.name }}</p>
        <p><strong>框架类型：</strong>{{ currentVersion.framework?.type || '自定义' }}</p>
        <p><strong>描述：</strong>{{ currentVersion.description }}</p>

        <h3>提示词内容</h3>
        <template v-if="currentVersion.framework?.type === 'RTGO'">
          <p><strong>角色(Role)：</strong>{{ currentVersion.content.role }}</p>
          <p><strong>任务(Task)：</strong>{{ currentVersion.content.task }}</p>
          <p><strong>目标(Goal)：</strong>{{ currentVersion.content.goal }}</p>
          <p>
            <strong>输出(Output)：</strong>{{ currentVersion.content.output }}
          </p>
        </template>

        <template v-else-if="currentVersion.framework?.type === 'SPAR'">
          <p>
            <strong>情境(Situation)：</strong
            >{{ currentVersion.content.situation }}
          </p>
          <p>
            <strong>目的(Purpose)：</strong>{{ currentVersion.content.purpose }}
          </p>
          <p>
            <strong>行动(Action)：</strong>{{ currentVersion.content.action }}
          </p>
          <p>
            <strong>结果(Result)：</strong>{{ currentVersion.content.result }}
          </p>
        </template>

        <template v-else>
          <p>
            <strong>自定义内容：</strong>{{ currentVersion.content.custom }}
          </p>
        </template>

        <h3>变量列表</h3>
        <el-table :data="currentVersion.variables">
          <el-table-column prop="name" label="变量名称" />
          <el-table-column prop="default_value" label="默认值" />
          <el-table-column prop="description" label="描述" />
        </el-table>
      </template>
    </el-dialog>

    <!-- 恢复确认对话框 -->
    <el-dialog
      v-model="restoreDialogVisible"
      title="确认恢复"
      width="30%"
      append-to-body
      destroy-on-close
    >
      <p>
        确定要恢复到版本 v{{
          versionToRestore?.version_number
        }}
        吗？此操作将创建一个新版本。
      </p>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="restoreDialogVisible = false">取消</el-button>
          <el-button
            type="primary"
            @click="confirmRestore"
            :loading="restoring"
          >
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from "vue";
import { ElMessage } from "element-plus";
import { getTemplateVersions, restoreTemplateVersion } from "@/api/templates";
import type { TemplateVersion } from "@/types";

const props = defineProps<{
  modelValue: boolean;
  templateId: number;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
  (e: "restored"): void;
}>();

const dialogVisible = ref(props.modelValue);
const loading = ref(false);
const versions = ref<TemplateVersion[]>([]);

// 预览相关
const previewDialogVisible = ref(false);
const currentVersion = ref<TemplateVersion | null>(null);

// 恢复相关
const restoreDialogVisible = ref(false);
const versionToRestore = ref<TemplateVersion | null>(null);
const restoring = ref(false);

// 监听对话框可见性
const stopWatch = watch(
  () => props.modelValue,
  (val) => {
    dialogVisible.value = val;
    if (val && props.templateId) {
      loadVersions();
    }
  },
  { immediate: true },
);

watch(
  () => dialogVisible.value,
  (val) => {
    emit("update:modelValue", val);
    if (!val) {
      // 清理状态
      versions.value = [];
      currentVersion.value = null;
      versionToRestore.value = null;
    }
  },
);

// 加载版本历史
const loadVersions = async () => {
  if (!props.templateId) return;

  loading.value = true;
  try {
    versions.value = await getTemplateVersions(props.templateId);
  } catch (error: any) {
    ElMessage.error(error.message || "加载失败");
  } finally {
    loading.value = false;
  }
};

// 预览版本
const handlePreview = (version: TemplateVersion) => {
  currentVersion.value = version;
  previewDialogVisible.value = true;
};

// 恢复版本
const handleRestore = (version: TemplateVersion) => {
  versionToRestore.value = version;
  restoreDialogVisible.value = true;
};

// 确认恢复
const confirmRestore = async () => {
  if (!versionToRestore.value) return;

  restoring.value = true;
  try {
    await restoreTemplateVersion(props.templateId, versionToRestore.value.id);
    ElMessage.success("恢复成功");
    restoreDialogVisible.value = false;
    emit("restored");
    loadVersions(); // 重新加载版本列表
  } catch (error: any) {
    ElMessage.error(error.message || "恢复失败");
  } finally {
    restoring.value = false;
  }
};

// 关闭对话框
const handleClose = () => {
  dialogVisible.value = false;
};

// 组件卸载前清理
onBeforeUnmount(() => {
  stopWatch();
});
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

:deep(.el-dialog__body) {
  padding-top: 20px;
}

h3 {
  margin-top: 20px;
  margin-bottom: 10px;
  font-size: 16px;
  font-weight: 500;
}

p {
  margin: 8px 0;
  line-height: 1.5;
}
</style>
