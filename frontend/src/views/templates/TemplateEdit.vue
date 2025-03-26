<template>
  <div class="page-container">
    <div class="page-header">
      <h1>编辑提示词模版</h1>
    </div>

    <div v-loading="loading">
      <el-form
        v-if="form"
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

          <el-form-item label="框架" prop="framework">
            <FrameworkSelect
              v-model="form.framework"
              @change="handleFrameworkChange"
              :showModules="true"
            />
          </el-form-item>

          <el-form-item label="描述" prop="description">
            <el-input
              v-model="form.description"
              type="textarea"
              :rows="3"
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

          <div v-loading="loadingFrameworks" element-loading-text="加载框架内容...">
            <template v-if="form.framework?.modules?.length">
              <el-form-item
                v-for="module in form.framework.modules"
                :key="module.id"
                :label="module.name"
                :prop="'content.' + module.name.toLowerCase()"
              >
                <el-input
                  v-model="form.content[module.name.toLowerCase()]"
                  type="textarea"
                  :rows="2"
                  :placeholder="module.description"
                />
              </el-form-item>
            </template>

            <template v-else-if="!form.framework">
              <el-empty description="请先选择框架类型" />
            </template>

            <template v-else>
              <el-form-item label="自定义内容" prop="content.custom">
                <el-input
                  v-model="form.content.custom"
                  type="textarea"
                  :rows="6"
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
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            保存
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, onMounted, onBeforeUnmount } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { Plus, Delete } from "@element-plus/icons-vue";
import type { FormInstance, FormRules } from "element-plus";
import { getTemplate, updateTemplate } from "@/api/templates";
import { getFramework, getFrameworks, type Framework } from "@/api/frameworks";
import FrameworkSelect from "@/components/FrameworkSelect.vue";
import type { Template } from "@/types";

const route = useRoute();
const router = useRouter();
const formRef = ref<FormInstance>();
const loading = ref(false);
const loadingFrameworks = ref(false);
const frameworks = ref([]);
const submitting = ref(false);

// 表单数据
const form = ref<{
  name: string;
  framework: any;
  description: string;
  content: {
    role?: string;
    task?: string;
    goal?: string;
    output?: string;
    situation?: string;
    purpose?: string;
    action?: string;
    result?: string;
    custom?: string;
  };
  variables: Array<{
    name: string;
    default_value: string;
    description: string;
  }>;
} | null>(null);

// 表单验证规则
const rules = reactive<FormRules>({
  name: [
    { required: true, message: "请输入模版名称", trigger: "blur" },
    { min: 2, max: 50, message: "长度在 2 到 50 个字符", trigger: "blur" },
  ],
  framework: [
    { required: true, message: "请选择框架", trigger: "change" },
  ],
  description: [{ required: true, message: "请输入模版描述", trigger: "blur" }],
});

// 动态设置必填字段
const getContentRules = (framework: any) => {
  const rules: Record<string, any> = {};
  
  if (framework?.modules?.length) {
    framework.modules.forEach((module: any) => {
      const fieldName = `content.${module.name.toLowerCase()}`;
      rules[fieldName] = [
        { 
          required: true, 
          message: `请输入${module.name}`, 
          trigger: "blur" 
        }
      ];
    });
  } else {
    rules["content.custom"] = [
      { 
        required: true, 
        message: "请输入自定义内容", 
        trigger: "blur" 
      }
    ];
  }
  
  return rules;
};

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

// 重置内容
const resetContent = () => {
  if (!form.value) return;
  
  // 创建新的content对象而不是修改原对象
  const newContent = {};
  
  // 如果有框架模块，为每个模块创建对应的内容字段
  if (form.value.framework?.modules?.length) {
    form.value.framework.modules.forEach(module => {
      const key = module.name.toLowerCase();
      newContent[key] = "";
    });
  } else {
    // 如果没有框架模块，则设置自定义内容字段
    newContent.custom = "";
  }
  
  // 替换整个content对象，确保响应式更新
  form.value.content = newContent;
  
};

// 监听框架变化
const stopWatch = watch(
  () => form.value?.framework,
  (newFramework, oldFramework) => {
    if (!form.value) return;
    
    // 检查框架模块是否发生变化
    const newModules = newFramework?.modules || [];
    const oldModules = oldFramework?.modules || [];
    if (JSON.stringify(newModules) !== JSON.stringify(oldModules)) {
      // 保存旧的content值
      const oldContent = { ...form.value.content };
      
      // 重置content对象
      form.value.content = {};
      
      // 根据新的框架模块设置content字段
      if (newModules.length > 0) {
        newModules.forEach(module => {
          const key = module.name.toLowerCase();
          // 尝试保留原有值
          form.value.content[key] = oldContent[key] || '';
        });
      } else {
        // 如果没有模块，设置custom字段
        form.value.content.custom = oldContent.custom || '';
      }
      
      // 更新验证规则
      Object.assign(rules, getContentRules(newFramework));
      
    }
  },
  { deep: true }  // 深度监听框架对象的变化
);

// 处理框架选择变化
const handleFrameworkChange = async (framework: any) => {
  if (!form.value) return;
  
  loadingFrameworks.value = true;
  
  try {
    if (framework === null) {
      // 清空框架
      form.value.framework = null;
      
      // 设置为自定义内容
      form.value.content = {
        custom: form.value.content.custom || ""
      };
      
    } else {
      // 框架对象已经由FrameworkSelect组件传递过来，无需再次获取
      if (framework) {
        // 先保存当前content的引用
        const oldContent = { ...form.value.content };
        
        // 更新框架
        form.value.framework = framework;
        
        // 创建新的content对象
        const newContent = {};
        
        // 根据框架模块设置content字段
        if (framework.modules?.length) {
          framework.modules.forEach(module => {
            const key = module.name.toLowerCase();
            // 尝试保留原有值
            newContent[key] = oldContent[key] || "";
          });
        } else {
          // 如果没有模块，设置custom字段
          newContent.custom = oldContent.custom || "";
        }
        
        // 替换整个content对象
        form.value.content = newContent;
        
      }
    }
    
    // 更新验证规则
    Object.assign(rules, getContentRules(form.value.framework));
  } catch (error: any) {
    ElMessage.error(error.message || "获取框架详情失败");
  } finally {
    loadingFrameworks.value = false;
  }
};

// 组件卸载前清理
onBeforeUnmount(() => {
  stopWatch();
});

// 添加变量
const addVariable = () => {
  if (form.value) {
    form.value.variables.push({
      name: "",
      default_value: "",
      description: "",
    });
  }
};

// 删除变量
const removeVariable = (index: number) => {
  if (form.value) {
    form.value.variables.splice(index, 1);
  }
};

// 加载模板数据
const loadTemplate = async (id: string) => {
  loading.value = true;
  try {
    const data = await getTemplate(Number(id));
    // 确保初始化表单数据结构
    form.value = {
      name: data.name,
      framework: null, // 先设置为null，后面再更新
      description: data.description,
      content: {},  // 先设置为空对象，后面再填充
      variables: data.variables || [],
    };

    // 处理框架信息
    let framework = null;
    if (data.framework) {
      try {
        // 如果framework是数字（ID），则获取完整框架信息
        if (typeof data.framework === 'number') {
          framework = await getFramework(data.framework);
        } else {
          // 如果framework已经是完整对象，直接使用
          framework = data.framework;
        }
      } catch (error) {
        ElMessage.warning('获取框架详情失败，将使用基础框架信息');
      }
    } else if (data.framework_type && data.framework_type !== 'CUSTOM') {
      // 处理只有framework_type的情况
      const matchingFramework = frameworks.value.find(f => f.name === data.framework_type);
      if (matchingFramework) {
        try {
          framework = await getFramework(matchingFramework.id);
        } catch (error) {
          ElMessage.warning('获取匹配框架详情失败');
        }
      }
    }

    // 更新表单中的框架信息
    form.value.framework = framework;

    // 处理内容字段
    if (framework?.modules?.length) {
      // 如果有框架模块，创建对应的内容字段
      const newContent = {};
      framework.modules.forEach(module => {
        const key = module.name.toLowerCase();
        newContent[key] = data.content?.[key] || '';
      });
      form.value.content = newContent;
    } else {
      // 如果没有框架模块或是自定义框架，使用custom字段
      form.value.content = {
        custom: data.content?.custom || ''
      };
    }

  } catch (error: any) {
    ElMessage.error(error.message || "加载失败");
    router.back();
  } finally {
    loading.value = false;
  }
};

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value || !form.value) return;

  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true;
      try {
        // 深拷贝当前表单内容，避免直接修改表单数据
        const formData = JSON.parse(JSON.stringify(form.value));
        
        // 准备提交数据
        const submissionData = {
          name: formData.name,
          description: formData.description,
          framework: formData.framework?.id || null,
          content: {},
          variables: formData.variables,
          framework_type: formData.framework ? formData.framework.name : 'CUSTOM'
        };
        

        // 处理content数据
        if (formData.framework?.modules?.length) {
          // 如果有框架模块，确保只包含框架定义的字段
          const contentObj = {};
          formData.framework.modules.forEach((module: any) => {
            const key = module.name.toLowerCase();
            contentObj[key] = formData.content[key] || '';
          });
          submissionData.content = contentObj;
        } else {
          // 如果没有框架模块，使用自定义内容
          submissionData.content = {
            custom: formData.content.custom || '',
          };
        }

        
        // 发送更新请求
        const result = await updateTemplate(
          Number(route.params.id),
          submissionData,
        );
        
        if (result && result.id) {
          ElMessage.success("保存成功");
          router.push("/templates");
        } else {
          throw new Error("更新模板失败");
        }
      } catch (error: any) {
        ElMessage.error(error.message || "保存失败");
      } finally {
        submitting.value = false;
      }
    }
  });
};

onMounted(async () => {
  try {
    // 先加载框架数据
    const response = await getFrameworks();
    frameworks.value = response;
    // 等框架数据加载完成后再加载模板数据
    if (route.params.id) {
      await loadTemplate(route.params.id as string);
      // 确保表单验证规则更新
      if (form.value?.framework) {
        Object.assign(rules, getContentRules(form.value.framework));
      }
    } else {
      router.back();
    }
  } catch (error: any) {
    ElMessage.error(error.message || "页面初始化失败");
    router.back();
  }
});
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
