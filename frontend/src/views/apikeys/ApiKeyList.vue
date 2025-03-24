<template>
  <div class="api-key-list">
    <div class="header">
      <h1>秘钥管理</h1>
      <el-button type="primary" @click="showAddDialog">添加秘钥</el-button>
    </div>

    <el-card class="list-card">
      <el-table v-loading="loading" :data="apiKeys" style="width: 100%">
        <el-table-column prop="platform_name" label="平台名称" width="180" />
        <el-table-column prop="scene_name" label="场景名称" width="180" />
        <el-table-column prop="key" label="秘钥">
          <template #default="scope">
            <div class="key-container">
              <span>{{ maskKey(scope.row.key) }}</span>
              <el-button link type="primary" @click="showKey(scope.row)"
                >查看</el-button
              >
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
              {{ scope.row.is_active ? "启用" : "禁用" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250">
          <template #default="scope">
            <el-button link type="primary" @click="handleEdit(scope.row)"
              >编辑</el-button
            >
            <el-button link type="primary" @click="handleValidate(scope.row)"
              >验证</el-button
            >
            <el-button link type="danger" @click="handleDelete(scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑秘钥' : '添加秘钥'"
      width="500px"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="平台名称" prop="platform_name">
          <el-input v-model="form.platform_name" placeholder="请输入平台名称" />
        </el-form-item>
        <el-form-item label="场景名称" prop="scene_name">
          <el-input v-model="form.scene_name" placeholder="请输入场景名称" />
        </el-form-item>
        <el-form-item label="秘钥" prop="key">
          <el-input v-model="form.key" placeholder="请输入API秘钥" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            placeholder="请输入描述信息"
          />
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="form.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 查看秘钥对话框 -->
    <el-dialog v-model="keyDialogVisible" title="查看秘钥" width="400px">
      <div class="view-key">
        <p><strong>平台名称:</strong> {{ currentKey.platform_name }}</p>
        <p><strong>场景名称:</strong> {{ currentKey.scene_name }}</p>
        <p><strong>秘钥:</strong> {{ currentKey.key }}</p>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="keyDialogVisible = false">关闭</el-button>
          <el-button type="primary" @click="copyKey">复制秘钥</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, reactive } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import {
  getApiKeys,
  createApiKey,
  updateApiKey,
  deleteApiKey,
  validateApiKey,
  ApiKeyData,
} from "@/api/apikeys";

const loading = ref(false);
const apiKeys = ref<ApiKeyData[]>([]);
const dialogVisible = ref(false);
const keyDialogVisible = ref(false);
const isEdit = ref(false);
const currentKey = ref<ApiKeyData>({
  platform_name: "",
  scene_name: "",
  key: "",
});

const form = reactive<ApiKeyData>({
  platform_name: "",
  scene_name: "",
  key: "",
  description: "",
  is_active: true,
});

const rules = {
  platform_name: [
    { required: true, message: "请输入平台名称", trigger: "blur" },
  ],
  scene_name: [{ required: true, message: "请输入场景名称", trigger: "blur" }],
  key: [{ required: true, message: "请输入API秘钥", trigger: "blur" }],
};

// 获取所有API秘钥
const fetchApiKeys = async () => {
  loading.value = true;
  try {
    const res = await getApiKeys();
    console.log("API Keys response:", res); // 添加日志以便调试

    // 根据实际返回的数据结构进行处理
    if (Array.isArray(res)) {
      apiKeys.value = res;
    } else if (res && res.results) {
      apiKeys.value = res.results;
    } else if (res) {
      apiKeys.value = [res]; // 如果是单个对象，转为数组
    } else {
      apiKeys.value = [];
    }
  } catch (error) {
    ElMessage.error("获取秘钥列表失败");
    console.error(error);
  } finally {
    loading.value = false;
  }
};

// 显示添加对话框
const showAddDialog = () => {
  isEdit.value = false;
  resetForm();
  dialogVisible.value = true;
};

// 处理编辑
const handleEdit = (row: ApiKeyData) => {
  isEdit.value = true;
  Object.assign(form, row);
  dialogVisible.value = true;
};

// 处理删除
const handleDelete = (row: ApiKeyData) => {
  ElMessageBox.confirm("确认删除该秘钥吗？", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        if (row.id) {
          await deleteApiKey(row.id);
          ElMessage.success("删除成功");
          fetchApiKeys();
        }
      } catch (error) {
        ElMessage.error("删除失败");
        console.error(error);
      }
    })
    .catch(() => {});
};

// 处理验证
const handleValidate = async (row: ApiKeyData) => {
  try {
    if (row.id) {
      loading.value = true;
      const res = await validateApiKey(row.id);
      if (res.data.is_valid) {
        ElMessage.success("秘钥验证成功");
      } else {
        ElMessage.warning("秘钥验证失败");
      }
    }
  } catch (error) {
    ElMessage.error("验证过程中出错");
    console.error(error);
  } finally {
    loading.value = false;
  }
};

// 提交表单
const submitForm = async () => {
  try {
    if (isEdit.value && form.id) {
      await updateApiKey(form.id, form);
      ElMessage.success("更新成功");
    } else {
      await createApiKey(form);
      ElMessage.success("添加成功");
    }
    dialogVisible.value = false;
    fetchApiKeys();
  } catch (error) {
    ElMessage.error(isEdit.value ? "更新失败" : "添加失败");
    console.error(error);
  }
};

// 重置表单
const resetForm = () => {
  form.platform_name = "";
  form.scene_name = "";
  form.key = "";
  form.description = "";
  form.is_active = true;
};

// 显示秘钥
const showKey = (row: ApiKeyData) => {
  currentKey.value = { ...row };
  keyDialogVisible.value = true;
};

// 复制秘钥
const copyKey = () => {
  navigator.clipboard
    .writeText(currentKey.value.key || "")
    .then(() => {
      ElMessage.success("秘钥已复制到剪贴板");
    })
    .catch(() => {
      ElMessage.error("复制失败，请手动复制");
    });
};

// 掩码显示秘钥
const maskKey = (key: string) => {
  if (!key) return "";
  if (key.length <= 8) {
    return "********";
  }
  return key.substring(0, 4) + "****" + key.substring(key.length - 4);
};

onMounted(() => {
  fetchApiKeys();
});
</script>

<style scoped>
.api-key-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.list-card {
  margin-bottom: 20px;
}

.key-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.view-key {
  padding: 10px;
}

.view-key p {
  margin: 10px 0;
}
</style>
