<template>
  <div class="framework-edit">
    <div class="header">
      <h1>编辑框架</h1>
    </div>

    <el-form
      ref="formRef"
      v-loading="loading"
      :model="form"
      :rules="rules"
      label-width="100px"
      class="framework-form"
    >
      <el-form-item label="框架名称" prop="name">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="框架描述" prop="description">
        <el-input v-model="form.description" type="textarea" :rows="4" />
      </el-form-item>

      <el-divider>模块管理</el-divider>

      <div class="module-section">
        <div class="module-list">
          <div
            v-for="(module, index) in modules"
            :key="module.id || index"
            class="module-item"
          >
            <el-card class="module-card">
              <el-form :model="module" :rules="moduleRules">
                <el-row :gutter="20">
                  <el-col :span="8">
                    <el-form-item label="模块名称" prop="name">
                      <el-input
                        v-model="module.name"
                        placeholder="请输入模块名称"
                      />
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="模块描述" prop="description">
                      <el-input
                        v-model="module.description"
                        placeholder="请输入模块描述"
                      />
                    </el-form-item>
                  </el-col>
                  <el-col :span="2">
                    <el-form-item label="排序" prop="order">
                      <el-input-number
                        v-model="module.order"
                        :min="0"
                        :max="999"
                        controls-position="right"
                        size="small"
                      />
                    </el-form-item>
                  </el-col>
                  <el-col :span="2" class="action-buttons">
                    <el-button
                      type="danger"
                      size="small"
                      circle
                      @click="handleDeleteModule(index, module)"
                    >
                      <el-icon><Delete /></el-icon>
                    </el-button>
                  </el-col>
                </el-row>
              </el-form>
            </el-card>
          </div>
        </div>

        <div class="add-module-button">
          <el-button type="primary" @click="handleAddModule">
            <el-icon><Plus /></el-icon>
            添加模块
          </el-button>
        </div>
      </div>

      <div class="form-actions">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSubmit">保存</el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
import { Delete, Plus } from "@element-plus/icons-vue";
import type { FormInstance, FormRules } from "element-plus";
import {
  getFramework,
  updateFramework,
  addModuleToFramework,
  updateModule,
  deleteModule,
  type Framework,
  type FrameworkModule,
} from "@/api/frameworks";

const router = useRouter();
const route = useRoute();
const frameworkId = route.params.id as string;

const loading = ref(true);
const formRef = ref<FormInstance>();

const form = ref({
  name: "",
  description: "",
});

const modules = ref<FrameworkModule[]>([]);

const rules: FormRules = {
  name: [
    { required: true, message: "请输入框架名称", trigger: "blur" },
    { min: 2, max: 100, message: "长度在 2 到 100 个字符", trigger: "blur" },
  ],
  description: [{ required: true, message: "请输入框架描述", trigger: "blur" }],
};

const moduleRules: FormRules = {
  name: [
    { required: true, message: "请输入模块名称", trigger: "blur" },
    { min: 2, max: 100, message: "长度在 2 到 100 个字符", trigger: "blur" },
  ],
  description: [{ required: true, message: "请输入模块描述", trigger: "blur" }],
  order: [{ required: true, message: "请输入排序值", trigger: "blur" }],
};

// 获取框架详情
const fetchFrameworkDetail = async () => {
  loading.value = true;
  try {
    const framework = await getFramework(frameworkId);
    form.value.name = framework.name;
    form.value.description = framework.description;
    modules.value = framework.modules || [];
    // 确保所有模块都有排序值
    modules.value.forEach((module, index) => {
      if (module.order === undefined || module.order === null) {
        module.order = index;
      }
    });
  } catch (error) {
    console.error("获取框架详情失败:", error);
    ElMessage.error("获取框架详情失败");
    router.push("/frameworks");
  } finally {
    loading.value = false;
  }
};

// 添加模块
const handleAddModule = () => {
  modules.value.push({
    name: "",
    description: "",
    order: modules.value.length,
  });
};

// 删除模块
const handleDeleteModule = (index: number, module: FrameworkModule) => {
  ElMessageBox.confirm("确认删除该模块吗？删除后将无法恢复。", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(async () => {
    if (module.id) {
      try {
        await deleteModule(module.id);
        ElMessage.success("删除模块成功");
      } catch (error) {
        console.error("删除模块失败:", error);
        ElMessage.error("删除模块失败");
        return;
      }
    }

    modules.value.splice(index, 1);
    // 更新剩余模块的排序
    modules.value.forEach((module, idx) => {
      module.order = idx;
    });
  });
};

// 提交框架表单
const handleSubmit = async () => {
  if (!formRef.value) return;

  // 验证所有模块是否都填写了必填字段
  const hasEmptyModules = modules.value.some(
    (module) => !module.name || !module.description,
  );

  if (hasEmptyModules) {
    ElMessage.error("请完整填写所有模块信息");
    return;
  }

  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // 更新框架基本信息
        await updateFramework(frameworkId, form.value);

        // 处理模块更新
        for (const module of modules.value) {
          if (module.id) {
            // 更新已有模块
            await updateModule(module.id, module);
          } else {
            // 添加新模块
            await addModuleToFramework(frameworkId, module);
          }
        }

        ElMessage.success("更新框架成功");
        router.push("/frameworks");
      } catch (error) {
        console.error("更新框架失败:", error);
        ElMessage.error("更新框架失败");
      }
    }
  });
};

// 取消编辑
const handleCancel = () => {
  router.push("/frameworks");
};

// 初始化
onMounted(() => {
  fetchFrameworkDetail();
});
</script>

<style scoped>
.framework-edit {
  padding: 20px;
}

.header {
  margin-bottom: 20px;
}

.framework-form {
  max-width: 1200px;
}

.module-section {
  margin-top: 20px;
}

.module-list {
  margin-bottom: 20px;
}

.module-item {
  margin-bottom: 16px;
}

.module-card {
  background-color: #f8f9fa;
}

.add-module-button {
  margin-top: 16px;
  margin-bottom: 24px;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.action-buttons {
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.el-form-item__content) {
  flex-wrap: nowrap;
}

:deep(.el-input-number) {
  width: 100%;
}
</style>
