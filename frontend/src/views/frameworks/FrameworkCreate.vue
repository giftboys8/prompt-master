<template>
  <div class="framework-create">
    <div class="header">
      <h1>创建框架</h1>
    </div>

    <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" class="framework-form">
      <el-form-item label="框架名称" prop="name">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="框架描述" prop="description">
        <el-input v-model="form.description" type="textarea" :rows="4" />
      </el-form-item>

      <el-divider>模块管理</el-divider>

      <div class="module-section">
        <div class="module-header">
          <el-button type="primary" @click="handleAddModule">
            添加模块
          </el-button>
        </div>

        <el-table :data="modules" border>
          <el-table-column prop="name" label="模块名称" />
          <el-table-column prop="description" label="模块描述" show-overflow-tooltip />
          <el-table-column prop="order" label="排序" width="100" />
          <el-table-column label="操作" width="200">
            <template #default="{ row, $index }">
              <el-button-group>
                <el-button type="primary" @click="handleEditModule($index)">
                  编辑
                </el-button>
                <el-button type="danger" @click="handleDeleteModule($index)">
                  删除
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="form-actions">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSubmit">创建</el-button>
      </div>
    </el-form>

    <!-- 模块表单对话框 -->
    <el-dialog
      v-model="moduleFormVisible"
      :title="isEditModule ? '编辑模块' : '添加模块'"
      width="500px"
    >
      <el-form
        ref="moduleFormRef"
        :model="moduleForm"
        :rules="moduleRules"
        label-width="100px"
      >
        <el-form-item label="模块名称" prop="name">
          <el-input v-model="moduleForm.name" />
        </el-form-item>
        <el-form-item label="模块描述" prop="description">
          <el-input
            v-model="moduleForm.description"
            type="textarea"
            :rows="4"
          />
        </el-form-item>
        <el-form-item label="排序" prop="order">
          <el-input-number
            v-model="moduleForm.order"
            :min="0"
            :max="999"
            controls-position="right"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="moduleFormVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmitModule">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import {
  createFramework,
  type Framework,
  type FrameworkModule,
} from "@/api/frameworks";

const router = useRouter();
const formRef = ref<FormInstance>();
const moduleFormRef = ref<FormInstance>();

const form = ref({
  name: "",
  description: "",
});

const modules = ref<FrameworkModule[]>([]);

const moduleForm = ref<FrameworkModule>({
  name: "",
  description: "",
  order: 0,
});

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

const moduleFormVisible = ref(false);
const isEditModule = ref(false);
const currentModuleIndex = ref<number>(-1);

// 添加模块
const handleAddModule = () => {
  isEditModule.value = false;
  moduleForm.value = {
    name: "",
    description: "",
    order: modules.value.length,
  };
  moduleFormVisible.value = true;
};

// 编辑模块
const handleEditModule = (index: number) => {
  isEditModule.value = true;
  currentModuleIndex.value = index;
  const module = modules.value[index];
  moduleForm.value = {
    name: module.name,
    description: module.description,
    order: module.order || 0,
  };
  moduleFormVisible.value = true;
};

// 删除模块
const handleDeleteModule = (index: number) => {
  modules.value.splice(index, 1);
  // 更新剩余模块的排序
  modules.value.forEach((module, idx) => {
    module.order = idx;
  });
};

// 提交模块表单
const handleSubmitModule = async () => {
  if (!moduleFormRef.value) return;

  await moduleFormRef.value.validate(async (valid) => {
    if (valid) {
      if (isEditModule.value) {
        // 更新现有模块
        modules.value[currentModuleIndex.value] = { ...moduleForm.value };
      } else {
        // 添加新模块
        modules.value.push({ ...moduleForm.value });
      }
      moduleFormVisible.value = false;
    }
  });
};

// 提交框架表单
const handleSubmit = async () => {
  if (!formRef.value) return;

  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const frameworkData = {
          ...form.value,
          modules: modules.value,
        };
        await createFramework(frameworkData);
        ElMessage.success("创建框架成功");
        router.push("/frameworks");
      } catch (error) {
        console.error("创建框架失败:", error);
        ElMessage.error("创建框架失败");
      }
    }
  });
};

// 取消创建
const handleCancel = () => {
  router.push("/frameworks");
};
</script>

<style scoped>
.framework-create {
  padding: 20px;
}

.header {
  margin-bottom: 20px;
}

.framework-form {
  max-width: 800px;
}

.module-section {
  margin-top: 20px;
}

.module-header {
  margin-bottom: 20px;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>