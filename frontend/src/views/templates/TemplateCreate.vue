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

        <el-form-item label="框架" prop="framework">
          <FrameworkSelect
            v-model="form.framework"
            :show-modules="true"
            @change="handleFrameworkChange"
          />
        </el-form-item>

        <el-form-item label="框架类型" prop="framework_type">
          <el-select v-model="form.framework_type" placeholder="请选择框架类型">
            <el-option label="自定义" value="CUSTOM"></el-option>
            <!-- 添加其他框架类型选项 -->
          </el-select>
        </el-form-item>

        <el-form-item label="可见性" prop="visibility">
          <el-select v-model="form.visibility" placeholder="请选择可见性">
            <el-option label="私有" value="PRIVATE"></el-option>
            <el-option label="公开" value="PUBLIC"></el-option>
            <el-option label="共享" value="SHARED"></el-option>
          </el-select>
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

        <div v-loading="loading" element-loading-text="加载框架内容...">
          <!-- 动态生成框架模块表单 -->
          <template
            v-if="
              currentFramework &&
              currentFramework.modules &&
              currentFramework.modules.length > 0
            "
          >
            <el-form-item
              v-for="module in currentFramework.modules"
              :key="module.id"
              :label="module.name"
              :prop="`content.${module.name.toLowerCase()}`"
            >
              <div class="module-header">
                <span class="module-name">{{ module.name }}</span>
                <el-tooltip :content="module.description" placement="top">
                  <el-icon><InfoFilled /></el-icon>
                </el-tooltip>
              </div>
              <el-input
                v-model="form.content[module.name.toLowerCase()]"
                type="textarea"
                :rows="4"
                :placeholder="getModulePlaceholder(module)"
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
        <el-button type="primary" :loading="loading" @click="handleSubmit">
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
import { Plus, Delete, InfoFilled } from "@element-plus/icons-vue";
import type { FormInstance, FormRules } from "element-plus";
import { createTemplate } from "@/api/templates";
import { getFramework, type Framework } from "@/api/frameworks";
import FrameworkSelect from "@/components/FrameworkSelect.vue";
import { useTemplateCache } from "@/hooks/useTemplateCache";

const router = useRouter();
const { loadTemplates } = useTemplateCache();
const formRef = ref<FormInstance>();
const loading = ref(false);
const currentFramework = ref<Framework | null>(null);
// 表单数据
const form = reactive({
  name: "",
  framework: null,
  framework_type: "",
  visibility: "PRIVATE" as "PRIVATE" | "PUBLIC" | "SHARED",
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
  // 创建新的content对象
  const newContent = {};

  // 如果有框架模块，为每个模块创建对应的内容字段
  if (form.framework?.modules?.length) {
    form.framework.modules.forEach((module) => {
      const key = module.name.toLowerCase();
      newContent[key] = "";
    });
  } else {
    // 如果没有框架模块，则设置自定义内容字段
    newContent.custom = "";
  }

  // 替换整个content对象
  form.content = newContent;
};

// 处理框架选择变化
const handleFrameworkChange = async (frameworkId: number | null) => {
  console.log("Framework changed to:", frameworkId);

  // 清空之前的内容
  form.content = {};

  if (frameworkId) {
    loading.value = true;
    try {
      // 获取框架详情
      const response = await getFramework(frameworkId);
      currentFramework.value = response;
      console.log("获取到的框架详情:", response);

      // 设置框架类型
      form.framework_type = response.name;

      // 初始化各模块的内容
      if (response.modules && response.modules.length > 0) {
        response.modules.forEach((module) => {
          const moduleKey = module.name.toLowerCase();
          console.log(`初始化模块 ${moduleKey} 的内容`);
          form.content[moduleKey] = "";
        });
      } else {
        // 如果没有模块，设置默认的自定义内容字段
        console.log("框架没有模块，设置自定义内容字段");
        form.content = {
          custom: "",
        };
      }

      // 更新验证规则
      Object.assign(rules, getContentRules(response));
    } catch (error) {
      console.error("获取框架详情失败:", error);
      ElMessage.error("获取框架详情失败，请稍后重试");
    } finally {
      loading.value = false;
    }
  } else {
    // 清空框架相关数据
    currentFramework.value = null;
    form.framework_type = "CUSTOM";
    form.content = {
      custom: "",
    };
    console.log("清空框架相关数据");
    // 更新验证规则
    Object.assign(rules, getContentRules(null));
  }
};

// 获取模块的占位文本，提供更详细的指导
const getModulePlaceholder = (module: any) => {
  const basePlaceholder = module.description || `请输入${module.name}内容`;

  // 根据模块名称提供更具体的指导
  const moduleNameLower = module.name.toLowerCase();

  // 为常见模块类型提供更详细的指导
  if (moduleNameLower.includes("角色") || moduleNameLower.includes("role")) {
    return `${basePlaceholder}\n\n示例：\n你是一个专业的客服代表，负责解答用户关于我们产品的问题。\n你应该使用友好、专业的语气，提供准确的信息。`;
  } else if (
    moduleNameLower.includes("任务") ||
    moduleNameLower.includes("task")
  ) {
    return `${basePlaceholder}\n\n示例：\n根据用户提供的问题，提供清晰、准确的解答。\n如果问题超出你的知识范围，请礼貌地告知用户并建议其他解决方案。`;
  } else if (
    moduleNameLower.includes("背景") ||
    moduleNameLower.includes("background")
  ) {
    return `${basePlaceholder}\n\n示例：\n我们的产品是一款智能家居控制系统，支持语音控制、远程操作和自动化场景设置。\n用户可能会询问设备连接问题、功能使用方法或故障排除等内容。`;
  } else if (
    moduleNameLower.includes("格式") ||
    moduleNameLower.includes("format")
  ) {
    return `${basePlaceholder}\n\n示例：\n回答应包含以下部分：\n1. 简短的问题总结\n2. 详细的解答步骤\n3. 可能的后续问题建议`;
  }

  return basePlaceholder;
};

// 表单验证规则
const rules = reactive<FormRules>({
  name: [
    { required: true, message: "请输入模版名称", trigger: "blur" },
    { min: 2, max: 50, message: "长度在 2 到 50 个字符", trigger: "blur" },
  ],
  framework: [{ required: true, message: "请选择框架", trigger: "change" }],
  framework_type: [
    { required: true, message: "请选择框架类型", trigger: "change" },
  ],
  visibility: [{ required: true, message: "请选择可见性", trigger: "change" }],
  description: [{ required: true, message: "请输入模版描述", trigger: "blur" }],
});

// 动态设置必填字段
const getContentRules = (framework?: Framework | null) => {
  const contentRules: Record<string, any> = {};

  if (framework && framework.modules) {
    framework.modules.forEach((module) => {
      const fieldName = `content.${module.name.toLowerCase()}`;
      contentRules[fieldName] = [
        { required: true, message: `请输入${module.name}`, trigger: "blur" },
      ];
    });
  } else if (!form.framework) {
    contentRules["content.custom"] = [
      { required: true, message: "请输入自定义内容", trigger: "blur" },
    ];
  }

  return contentRules;
};

// 监听框架类型变化
watch(
  () => form.framework,
  () => {
    if (form.framework) {
      Object.assign(rules, getContentRules(form.framework));
    }
  },
);

// 监听当前框架变化
watch(
  () => currentFramework.value,
  () => {
    if (currentFramework.value) {
      Object.assign(rules, getContentRules(currentFramework.value));
    }
  },
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
          name: form.name.trim(),
          framework:
            typeof form.framework === "object"
              ? form.framework.id
              : form.framework,
          framework_type: form.framework_type,
          visibility: form.visibility,
          description: form.description.trim(),
          content: {},
          variables: form.variables.map((v) => ({
            name: v.name.trim(),
            default_value: v.default_value.trim(),
            description: v.description.trim(),
          })),
        };

        // 处理content字段
        if (currentFramework.value?.modules?.length > 0) {
          // 如果有框架模块，使用模块内容
          currentFramework.value.modules.forEach((module) => {
            const key = module.name.toLowerCase();
            submissionData.content[key] = form.content[key] || "";
          });
        } else {
          // 如果没有框架模块，使用自定义内容
          submissionData.content = {
            custom: form.content.custom || "",
          };
        }

        // 确保所有必需字段都存在
        if (!submissionData.framework) {
          submissionData.framework = null;
        }

        const result = await createTemplate(submissionData);
        if (result && result.id) {
          ElMessage.success("保存成功");
          // 强制刷新模板列表缓存
          await loadTemplates(true);
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
.page-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
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
  padding: 15px;
  border: 1px dashed #dcdfe6;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

.module-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  gap: 8px;
}

.module-name {
  font-weight: 500;
  color: #606266;
}

.w-full {
  width: 100%;
}
</style>
