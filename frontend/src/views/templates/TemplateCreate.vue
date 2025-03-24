<template>
  <div class="page-container">
    <div class="page-header">
      <h1>新增提示词模版</h1>
    </div>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="template-form"
    >
      <!-- 基本信息 -->
      <el-card class="form-card">
        <template #header>
          <div class="card-header">
            <span>基本信息</span>
          </div>
        </template>

        <el-form-item label="模版名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入模版名称" />
        </el-form-item>

        <el-form-item label="框架类型" prop="framework_type">
          <FrameworkSelect
            v-model="selectedFrameworkId"
            @change="handleFrameworkChange"
          />
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            rows="3"
            placeholder="请输入模版描述"
          />
        </el-form-item>
      </el-card>

      <!-- 提示词内容 -->
      <el-card class="form-card">
        <template #header>
          <div class="card-header">
            <span>提示词内容</span>
          </div>
        </template>

        <div v-loading="loading" element-loading-text="加载框架内容...">
          <!-- 动态生成框架模块表单 -->
          <template v-if="currentFramework && currentFramework.modules && currentFramework.modules.length > 0">
            <el-form-item 
              v-for="module in currentFramework.modules" 
              :key="module.id"
              :label="module.name" 
              :prop="`content.${module.name.toLowerCase()}`"
            >
              <el-input
                v-model="form.content[module.name.toLowerCase()]"
                type="textarea"
                rows="2"
                :placeholder="module.description"
              />
            </el-form-item>
          </template>

          <template v-else-if="!form.framework_type">
            <el-empty description="请先选择框架类型" />
          </template>

          <template v-else>
            <el-form-item label="自定义内容" prop="content.custom">
              <el-input
                v-model="form.content.custom"
                type="textarea"
                rows="6"
                placeholder="请输入自定义的提示词内容"
              />
            </el-form-item>
          </template>
        </div>
      </el-card>

      <!-- 变量设置 -->
      <el-card class="form-card">
        <template #header>
          <div class="card-header">
            <span>变量设置</span>
            <el-button type="primary" @click="addVariable">
              <el-icon><Plus /></el-icon>添加变量
            </el-button>
          </div>
        </template>

        <div
          v-for="(variable, index) in form.variables"
          :key="index"
          class="variable-item"
        >
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item
                :label="'变量名称'"
                :prop="'variables.' + index + '.name'"
                :rules="variableRules.name"
              >
                <el-input
                  v-model="variable.name"
                  placeholder="请输入变量名称"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item
                :label="'默认值'"
                :prop="'variables.' + index + '.default_value'"
                :rules="variableRules.default_value"
              >
                <el-input
                  v-model="variable.default_value"
                  placeholder="请输入默认值"
                />
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item
                :label="'描述'"
                :prop="'variables.' + index + '.description'"
                :rules="variableRules.description"
              >
                <el-input
                  v-model="variable.description"
                  placeholder="请输入描述"
                />
              </el-form-item>
            </el-col>
            <el-col :span="2" class="flex items-center">
              <el-button type="danger" circle @click="removeVariable(index)">
                <el-icon><Delete /></el-icon>
              </el-button>
            </el-col>
          </el-row>
        </div>
      </el-card>

      <!-- 提交按钮 -->
      <div class="form-actions">
        <el-button @click="$router.back()">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="loading">
          保存
        </el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, onMounted } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { Plus, Delete } from "@element-plus/icons-vue";
import type { FormInstance, FormRules } from "element-plus";
import { createTemplate } from "@/api/templates";
import { getFramework, type Framework } from "@/api/frameworks";
import FrameworkSelect from "@/components/FrameworkSelect.vue";

const router = useRouter();
const formRef = ref<FormInstance>();
const loading = ref(false);
const selectedFrameworkId = ref<number>();

// 当前选中的框架信息
const currentFramework = ref<Framework>();

// 表单数据
const form = reactive({
  name: "",
  framework_type: "",
  description: "",
  content: {} as Record<string, string>,
  variables: [] as Array<{
    name: string;
    default_value: string;
    description: string;
  }>,
});

// 重置表单内容
const resetContent = () => {
  form.content = {};
};

// 处理框架选择变化
const handleFrameworkChange = async (frameworkId: number | null) => {
  loading.value = true;
  try {
    // 重置表单内容
    resetContent();
    
    if (frameworkId !== null && typeof frameworkId === 'number') {
      const framework = await getFramework(frameworkId);
      if (framework) {
        currentFramework.value = framework;
        form.framework_type = framework.name;
        
        // 为每个模块创建内容字段
        if (framework.modules && framework.modules.length > 0) {
          framework.modules.forEach(module => {
            form.content[module.name.toLowerCase()] = "";
          });
        }
        
        console.log('Framework loaded:', framework);
        console.log('Current form content:', form.content);
      }
    } else {
      currentFramework.value = undefined;
      form.framework_type = "CUSTOM";
      form.content.custom = "";
    }
  } catch (error: any) {
    console.error('Framework fetch error:', error);
    ElMessage.error(error.message || "获取框架详情失败");
  } finally {
    loading.value = false;
  }
};

// 表单验证规则
const rules = reactive<FormRules>({
  name: [
    { required: true, message: "请输入模版名称", trigger: "blur" },
    { min: 2, max: 50, message: "长度在 2 到 50 个字符", trigger: "blur" },
  ],
  framework_type: [
    { required: true, message: "请选择框架类型", trigger: "change" },
  ],
  description: [{ required: true, message: "请输入模版描述", trigger: "blur" }],
});

// 动态设置必填字段
const getContentRules = () => {
  const contentRules: Record<string, any> = {};
  
  if (currentFramework.value && currentFramework.value.modules) {
    currentFramework.value.modules.forEach(module => {
      const fieldName = `content.${module.name.toLowerCase()}`;
      contentRules[fieldName] = [
        { required: true, message: `请输入${module.name}`, trigger: "blur" },
      ];
    });
  } else if (form.framework_type === "CUSTOM") {
    contentRules["content.custom"] = [
      { required: true, message: "请输入自定义内容", trigger: "blur" },
    ];
  }
  
  return contentRules;
};

// 监听框架类型变化
watch(
  () => form.framework_type,
  () => {
    if (form.framework_type) {
      Object.assign(rules, getContentRules());
    }
  },
);

// 监听当前框架变化
watch(
  () => currentFramework.value,
  () => {
    if (currentFramework.value) {
      Object.assign(rules, getContentRules());
    }
  }
);

// 变量验证规则
const variableRules = {
  name: [
    { required: true, message: "请输入变量名称", trigger: "blur" },
    {
      pattern: /^[a-zA-Z_][a-zA-Z0-9_]*$/,
      message: "变量名称只能包含字母、数字和下划线，且不能以数字开头",
      trigger: "blur",
    },
  ],
  default_value: [{ required: true, message: "请输入默认值", trigger: "blur" }],
  description: [{ required: true, message: "请输入描述", trigger: "blur" }],
};

// 添加变量
const addVariable = () => {
  form.variables.push({
    name: "",
    default_value: "",
    description: "",
  });
};

// 删除变量
const removeVariable = (index: number) => {
  form.variables.splice(index, 1);
};

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return;

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true;
      try {
        // 准备提交数据
        const submissionData = {
          ...form,
          content: { ...form.content } // 复制内容对象
        };
        
        // 如果是自定义类型且没有模块，确保有custom字段
        if (form.framework_type === "CUSTOM" && 
            (!currentFramework.value || !currentFramework.value.modules || 
             currentFramework.value.modules.length === 0)) {
          submissionData.content = {
            custom: form.content.custom || ""
          };
        }

        const result = await createTemplate(submissionData);
        if (result && result.id) {
          ElMessage.success("保存成功");
          router.push("/templates");
        } else {
          throw new Error("创建模板失败");
        }
      } catch (error: any) {
        ElMessage.error(error.message || "保存失败");
      } finally {
        loading.value = false;
      }
    }
  });
};
</script>

<style scoped>
.template-form {
  max-width: 1200px;
  margin: 0 auto;
}

.form-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.variable-item {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.variable-item:last-child {
  margin-bottom: 0;
}

.el-empty {
  padding: 40px 0;
}

.form-card :deep(.el-loading-mask) {
  background-color: rgba(255, 255, 255, 0.8);
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
}

.w-full {
  width: 100%;
}
</style>
